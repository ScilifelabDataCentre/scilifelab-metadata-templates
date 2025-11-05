"""
Run generate_genomics_template.py to generate the SciLifeLab internal template 
for the technical metadata of genomics data.

It will read the organisational metadata fields from the file 
'organisational_metadata_fields.yml' and the description and version fields 
for the genomics template from the file 'genomics_template_wrapper.yml', as 
well as the relevant ENA fields from the file 'ENA_experiment_metadata_fields.json'.
"""

import csv
import yaml
import json
import os


import update_ENA_controlled_vocabs as ena_cv   # Import the module to update controlled vocabularies

def get_dynamic_path(filename, directory=None):
    """
    Find a file by name anywhere under the current working directory.
    If `directory` is provided, search only inside that directory (relative to cwd or absolute),
    ensuring you don't accidentally return a file with the same name from another directory.
    Returns the first matching path or None if not found.
    """
    # Determine search root
    if directory:
        root_dir = directory if os.path.isabs(directory) else os.path.join(os.getcwd(), directory)
        if not os.path.isdir(root_dir):
            return None
        search_roots = [root_dir]
    else:
        search_roots = [os.getcwd()]

    for root in search_roots:
        for rd, dirs, files in os.walk(root):
            if filename in files:
                return os.path.join(rd, filename)
    return None


def generate_markdown_table(data_dict):
    # Generate a Markdown table from a dictionary
    table_content = '| Field Name | Requirement | Description | Controlled vocabulary |\n| ---------- | ---------- | ------------ | ---------- |\n'
    for field in data_dict:
        table_content += f"| {field['name']} | {field['requirement']} | {field['description']}  | {', '.join(str(x) for x in field['controlled_vocabulary'])} \n"
    return table_content

def update_markdown_table(file_path, table_start, table_end, data_dict):
    # Read the content of the Markdown file
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return

    # Find the start and end indices of the table using a marker
    start_index = content.find(table_start)
    end_index = content.find(table_end)

    # Generate the updated table content from the dictionary
    new_table_content = generate_markdown_table(data_dict)

    # Replace the old table content with the updated one
    content = f"{content[:start_index]}{table_start}\n{new_table_content}{content[end_index:]}"

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

def get_fields_from_yaml(file_path, label):
    try:
        with open(file_path, mode='r') as f:
            data = yaml.safe_load(f)
            fields = data.get(label, {}).get('fields', [])
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        fields = []
    except yaml.YAMLError as e:
        print("Error reading YAML:", e)
        fields = []
    return fields


def get_fields_from_json(file_path, label):
    try:
        with open(file_path, mode='r') as f:
            data = json.load(f)
            fields = data.get(label, {}).get('fields', [])
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        fields = []
    except json.JSONDecodeError as e:
        print("Error reading JSON:", e)
        fields = []
    return fields

def collect_fields():

    orga_file_path = get_dynamic_path('organisational_metadata_fields.yml')
    orga_fields = get_fields_from_yaml(orga_file_path, 'organisational_metadata')

    # get relevant yaml fields prefilled with CV terms fetched from ENA
    yaml_file_path_technical_fields = get_dynamic_path('technical_metadata_fields_incl_ENA_CVs.yml')
    technical_metadata_fields = get_fields_from_yaml(yaml_file_path_technical_fields, 'technical_metadata_fields')

    return technical_metadata_fields + orga_fields

def write_fields_to_json(output_file_path, all_fields):
    
    internal_metadata_file_path = get_dynamic_path('genomics_template_wrapper.yml')
    try:
        with open(internal_metadata_file_path, mode='r') as f:
            internal_metadata = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"File '{internal_metadata_file_path}' not found.")
        return
    except yaml.YAMLError as e:
        print("Error reading YAML:", e)
        return
   
    # add the fields and save to file
    internal_metadata['genomics_template']['fields'] = all_fields
    with open(output_file_path+".json", mode='w') as f:
        json.dump(internal_metadata, f, indent=4)
    
    print(f"Genomics template written to {output_file_path}.json")

def write_field_names_to_tsv(output_file_path, all_fields):

    with open(output_file_path+".tsv", mode='w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([field['name'] for field in all_fields])

    print(f"Genomics template field names written to {output_file_path}.tsv")


if __name__ == "__main__":
    
    output_file_path = 'genomics/genomics_technical_metadata'

    # update the controlled vocabularies from ENA. Writes to 'technical_metadata_fields_incl_ENA_CVs.json'
    ena_cv.update_controlled_vocabularies()

    all_fields = collect_fields()
    
    write_fields_to_json(output_file_path, all_fields)

    write_field_names_to_tsv(output_file_path, all_fields)

    # update readme
    readme_file_path = get_dynamic_path('README.md', directory='genomics/')
    table_start = '<!-- START OF OVERVIEW TABLE -->'
    table_end = '<!-- END OF OVERVIEW TABLE -->'
    update_markdown_table(readme_file_path, table_start, table_end, all_fields)





 
