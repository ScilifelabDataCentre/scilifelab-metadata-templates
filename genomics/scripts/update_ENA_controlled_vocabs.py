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

def update_controlled_vocabularies():

    mapping = { "run":["FILE"], "experiment":["LIBRARY_SELECTION", "LIBRARY_SOURCE", "LIBRARY_STRATEGY", "LOCUS", "LIBRARY_LAYOUT"], "common":["PLATFORM"], "study":["STUDY_TYPE"]}
    template_names= ["ENA.project", "SRA.common", "SRA.experiment", "SRA.run", "SRA.sample", "SRA.study", "SRA.submission"]
    yaml_file_path = "technical_metadata_fields.yml"
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
                elif template_block == "LIBRARY_LAYOUT":
                    query_dict = (list(findkeys(xsd_dict, 'LIBRARY_LAYOUT')))[0]
                    xml_tree['library_layout'] = list(query_dict['complexType']['choice'].keys())
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
    
    # populate objects with controlled vocabularies where applicable
    for ena_object_name, ena_cv in fixed_fields.items():
        create_attributes(ena_object_name, ena_cv, xml_tree)
 
    root_dir = "./"
    folder_name = ""
    folder_path = os.path.join(root_dir, folder_name)
        
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
         
    # Write json file with all information
    json_file_path = os.path.join(folder_path, "technical_metadata_fields_incl_ENA_CVs.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(fixed_fields, json_file, indent=4)
    print(f"Controlled vocabularies updated and saved to {json_file_path}")

    # Write to yaml file 
    yaml_file_path = os.path.join(folder_path, "technical_metadata_fields_incl_ENA_CVs.yml")
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(fixed_fields, yaml_file, sort_keys=False)
    print(f"Controlled vocabularies updated and saved to {yaml_file_path}")

if __name__ == "__main__":

    update_controlled_vocabularies()

