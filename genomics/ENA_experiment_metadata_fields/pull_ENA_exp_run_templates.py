'''
This script is based on the script https://github.com/ELIXIR-Belgium/ENA-metadata-templates/blob/main/scripts/template_updater.py, copyright @ Elixir Belgium and licensed under the MIT license, 
modifying it to only fetch the ENA experiment and run metadata templates.
'''

from lxml import etree
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import xlsxwriter
import os
import pandas as pd
import yaml
import json
import copy


def fetch_object(url):
    print('  GET ' + url)
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=15)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    r = session.get(url)
    # Covering internal server errors by retrying one more time
    if r.status_code == 500:
        time.sleep(5)
        r = requests.get(url, allow_redirects=True)
    elif r.status_code != 200:
        print(f"Problem with request: {str(r)}")
        raise RuntimeError("Non-200 status code")
    return r

def elem2dict(node):
    """
    Convert an lxml.etree node tree into a dict.
    """
    result = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        if element.tag:
            key = element.tag.split('}')[1] if '}' in element.tag else element.tag
            if element.attrib and 'name' in element.attrib:
                key= element.attrib['name']
            # Process element as tree element if the inner XML contains non-whitespace content
            if element.attrib and 'value' in element.attrib:
                value = element.attrib['value']
            elif element.text and element.text.strip():
                value = element.text.strip().rstrip()
            elif element.attrib and 'type' in element.attrib:
                value = element.attrib['type']
            else:
                value = elem2dict(element)
            if key in result:
                if type(result[key]) is list:
                    result[key].append(value)
                else:
                    if type(result[key]) is dict:
                        tempvalue = result[key].copy
                    else:
                        tempvalue = result[key]
                    result[key] = [tempvalue, value]
            else:
                result[key] = value
    return result


def findkeys(node, query):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, query):
               yield x
    elif isinstance(node, dict):
        if query in node:
            yield node[query]
        for j in node.values():
            for x in findkeys(j, query):
                yield x


def create_attributes(ena_object_name, ena_cv, xml_tree):
    for attribute in ena_cv['fields']:
        if attribute['name'] in xml_tree.keys():
            attribute['controlled_vocabulary'] = xml_tree[attribute['name']]
        yield attribute


def index_to_letter(index):
    """Converts a 0-based index to an Excel column letter."""
    column_letter = ""
    while index >= 0:
        remainder = index % 26
        column_letter = chr(65 + remainder) + column_letter
        index = (index - remainder) // 26 - 1

    return column_letter

def create_alphanum (attrib):
    return ''.join(char for char in attrib if char.isalnum())


def main():

    mapping = { "run":["FILE"], "experiment":["LIBRARY_SELECTION", "LIBRARY_SOURCE", "LIBRARY_STRATEGY", "LOCUS"], "common":["PLATFORM"], "study":["STUDY_TYPE"]}
    template_names= ["ENA.project", "SRA.common", "SRA.experiment", "SRA.run", "SRA.sample", "SRA.study", "SRA.submission"]
    yaml_file_path = "ENA_target_metadata_fields.yml"
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            fixed_fields = yaml.safe_load(yaml_file)
    except FileNotFoundError:
        print(f"File '{yaml_file_path}' not found.")
    except yaml.YAMLError as e:
        print("Error reading YAML:", e)

    xml_tree = {}
    for template_name in template_names:
        template_name_sm = template_name.split(".")[1]
        print(f"Downloading {template_name_sm} template")
        # Getting the xml checklist from ENA
        url = f"https://raw.githubusercontent.com/enasequence/webin-xml/master/src/main/resources/uk/ac/ebi/ena/sra/schema/{template_name}.xsd"
        response = fetch_object(url)
        
        if template_name_sm in mapping.keys():
            for template_block in mapping[template_name_sm]:
                # Parsing XSD
                parser = etree.XMLParser(recover=True, encoding='utf-8',remove_comments=True, remove_blank_text=True)
                root = etree.fromstring(response.content, parser)
                incl = etree.XInclude()
                incl(root)
                xsd_dict = elem2dict(root)
                
                if template_block == "FILE":
                    query_dict = (list(findkeys(xsd_dict, 'filetype')))[0]
                    xml_tree['file_type'] = query_dict['simpleType']['restriction']['enumeration']
                elif template_block == "LIBRARY_SELECTION":
                    query_dict = (list(findkeys(xsd_dict, 'typeLibrarySelection')))[0]
                    xml_tree['library_selection'] = query_dict['restriction']['enumeration']
                elif template_block == "LIBRARY_SOURCE":
                    query_dict = (list(findkeys(xsd_dict, 'typeLibrarySource')))[0]
                    xml_tree['library_source'] = query_dict['restriction']['enumeration']
                elif template_block == "LOCUS":
                    query_dict = (list(findkeys(xsd_dict, 'locus_name')))[0]
                    xml_tree['locus'] = query_dict['simpleType']['restriction']['enumeration']
                elif template_block == "STUDY_TYPE":
                    query_dict = (list(findkeys(xsd_dict, 'existing_study_type')))[0]
                    xml_tree['study_type'] = query_dict['simpleType']['restriction']['enumeration']
                elif template_block == "LIBRARY_STRATEGY":
                    query_dict = (list(findkeys(xsd_dict, 'typeLibraryStrategy')))[0]
                    xml_tree['library_strategy'] = query_dict['restriction']['enumeration']
                elif template_block == "PLATFORM":
                    platformtype_dict = (list(findkeys(xsd_dict, 'PlatformType')))[0]
                    xml_tree['platform'] = []
                    xml_tree['instrument_model'] = []
                    for platformtype, instrument_models in platformtype_dict['choice'].items():
                        xml_tree['platform'].append(platformtype)
                        instrument_models_dict = (list(findkeys(xsd_dict, instrument_models['complexType']['sequence']['INSTRUMENT_MODEL'].strip('com:'))))[0]
                        xml_tree['instrument_model'].extend(instrument_models_dict['restriction']['enumeration'])
                    xml_tree['instrument_model'] = sorted(list(set(xml_tree['instrument_model'])))


                else:
                    break

 
    root_dir = "./"
    folder_name = ""
    folder_path = os.path.join(root_dir, folder_name)

        
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
        
    # Create the TSV files
    for ena_object_name, ena_cv in fixed_fields.items():
        tsv_file_name = f"{ena_object_name}.tsv"
        tsv_file_path = os.path.join(folder_path, tsv_file_name)
        header_list = []
        for attrib in create_attributes(ena_object_name, ena_cv, xml_tree):
            header_list.append(f"\"{attrib['name']}\"")
        
        header_string = '\t'.join(header_list) + '\n'    
        # Create or overwrite the TSV file
        with open(tsv_file_path, 'w') as tsv_file:
            tsv_file.write(header_string)
        
    # Create or overwrite the README.md file
    readme_file_path = os.path.join(folder_path, "README.md")
    readme_file = open(readme_file_path, 'w')
    readme_file.write("# ENA Experiment Metadata Fields\n\n")

    # Create the XLSX
    xlsx_file_name = "ENA_experiment_metadata_template.xlsx"
    xlsx_file_path = os.path.join(folder_path, xlsx_file_name)

    workbook = xlsxwriter.Workbook(xlsx_file_path)
        
    header_format = workbook.add_format({'bold': True, 'align': 'center'})
    description_format = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign':'top'})

    # Create instructions worksheet
    worksheet = workbook.add_worksheet(f"Instructions")
    worksheet.set_column(0, 300, 15)
    worksheet.write(0,0, f"Instructions how to fill the metadata template", header_format)



    for ena_object_name, ena_cv in fixed_fields.items():

        # Initiate table to README
        readme_file.write(f"## {ena_object_name.title()}\n\n")
        readme_file.write( ena_cv['description'] + "\n\n")

        df = pd.DataFrame(columns=["Field name", "Cardinality", "Description", "Controlled vocabulary"])

        # Create worksheet
        worksheet = workbook.add_worksheet(ena_object_name)
        worksheet.set_column(0, 300, 15)
        col_index = 0

        # Create worksheet for the controlled vocabulary
        cv_worksheet = workbook.add_worksheet(f"cv_{ena_object_name}")
        cv_worksheet.hide()
        
        for i, attrib in enumerate(create_attributes(ena_object_name, ena_cv, xml_tree)):
            # Populate pandas dataframe with attributes
            units = ''
            if 'units' in attrib and attrib['units']:
                units = f" (Units: {attrib['units']})"
            
            header = [attrib['name'], attrib['cardinality'], attrib['description']]
            if 'controlled_vocabulary' in attrib and attrib['controlled_vocabulary']:
                header.append(", ".join(attrib['controlled_vocabulary']))
            else:
                header.append("")
            df.loc[i] = header

            # Populate the CV worksheet with values
            if 'controlled_vocabulary' in attrib and attrib['controlled_vocabulary']:
                for row_index, value in enumerate(attrib['controlled_vocabulary']):
                    cv_worksheet.write(row_index, col_index, str(value))
                # Define a named range for the valid values.
                range = f"'cv_{ena_object_name}'!${index_to_letter(col_index)}$1:${index_to_letter(col_index)}${len(attrib['controlled_vocabulary'])}"
                name = create_alphanum(attrib['name'])
                workbook.define_name(name, range)

            # Write the header
            worksheet.write(0, col_index, attrib['name'], header_format)
            # Write the description row
            worksheet.set_row(1, 150)
            worksheet.write(1, col_index, f"({attrib['cardinality'].capitalize()}) {attrib['description'].capitalize()}{units}", description_format)
            # Add data validation
            if 'controlled_vocabulary' in attrib and attrib['controlled_vocabulary']:
                name = create_alphanum(attrib['name'])
                worksheet.data_validation(2, col_index, 100, col_index, {'validate': 'list', 'source': f'={name}'})
            col_index += 1
        # Write data table to README
        readme_file.write(df.to_markdown(index=False, tablefmt='pipe'))
        readme_file.write("\n\n")

    readme_file.close()
    workbook.close()

    # Combine sample attributes with fixed fields
    fixed_fields_copy = copy.deepcopy(fixed_fields)
    # sample_attrib_merged = fixed_fields_copy['sample']['fields'] 
    # fixed_fields_copy['sample']['fields'] = sample_attrib_merged

    # Write json file with all information
    json_file_path = os.path.join(folder_path, "ENA_experiment_metadata_fields.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(fixed_fields_copy, json_file, indent=4)

if __name__ == "__main__":

    main()

