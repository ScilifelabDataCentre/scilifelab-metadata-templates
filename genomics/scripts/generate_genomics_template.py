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

def generate_markdown_table(data_dict):
    # Generate a Markdown table from a dictionary
    table_content = '| Field Name | Requirement | Description | Controlled vocabulary |\n| ---------- | ---------- | ------------ | ---------- |\n'
    for field in data_dict:
        table_content += f"| {field['name']} | {field['requirement']} | {field['description']}  | {', '.join(str(x) for x in field['controlled_vocabulary'])} \n"
    return table_content

def update_markdown_table(file_path, table_start, table_end, data_dict):
    # Read the content of the Markdown file
    with open(file_path, 'r') as file:
        content = file.read()

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
    with open(file_path, mode='r') as f:
        data = yaml.safe_load(f)
        fields = data.get(label, {}).get('fields', [])
    return fields

def get_fields_from_json(file_path, label):
    with open(file_path, mode='r') as f:
        data = json.load(f)
        fields = data.get(label, {}).get('fields', [])
    return fields

def collect_fields():

    orga_file_path = '../../organisational_metadata_fields.yml'
    orga_fields = get_fields_from_yaml(orga_file_path, 'organisational_metadata')

    # get relevant json fields prefilled with CV terms fetched from ENA
    json_file_path_technical_fields = 'technical_metadata_fields_incl_ENA_CVs.json'
    technical_metadata_fields = get_fields_from_json(json_file_path_technical_fields, 'technical_metadata_fields')
 

    all_fields_single_read = (
        technical_metadata_fields[:8] + technical_metadata_fields[9:13] # leave out insert_size, paired file fields
        + orga_fields
    )
    all_fields_paired_reads = (
        technical_metadata_fields[:11] + technical_metadata_fields[13:] # leave out single file fields
        + orga_fields
    )

    return all_fields_single_read, all_fields_paired_reads

def write_fields_to_json(output_file_path, all_fields_single_read, all_fields_paired_reads):
    
    # get the metadata wrapper for the genomics template
    internal_metadata_file_path = '../genomics_template_wrapper.yml'
    with open(internal_metadata_file_path, mode='r') as f:
        internal_metadata = yaml.safe_load(f)
   
    # add the fields for single read and save to file
    internal_metadata['genomics_template']['fields'] = all_fields_single_read
    with open(output_file_path+"_single_read.json", mode='w') as f:
        json.dump(internal_metadata, f, indent=4)

    # add the fields for paired reads and save to file 
    internal_metadata['genomics_template']['fields'] = all_fields_paired_reads
    with open(output_file_path+"_paired_reads.json", mode='w') as f:
        json.dump(internal_metadata, f, indent=4)
    
    print(f"Genomics template written to {output_file_path}_single_read.json and {output_file_path}_paired_reads.json")

def write_field_names_to_tsv(output_file_path, all_fields_single_read, all_fields_paired_reads):

    with open(output_file_path+"_single_read.tsv", mode='w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([field['name'] for field in all_fields_single_read])

    with open(output_file_path+"_paired_reads.tsv", mode='w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([field['name'] for field in all_fields_paired_reads])

    print(f"Genomics template field names written to {output_file_path}_single_read.tsv and {output_file_path}_paired_reads.tsv")


if __name__ == "__main__":
    
    output_file_path = '../genomics_technical_metadata'

    all_fields_single_read, all_fields_paired_reads = collect_fields()
    
    write_fields_to_json(output_file_path, all_fields_single_read, all_fields_paired_reads)

    write_field_names_to_tsv(output_file_path, all_fields_single_read, all_fields_paired_reads)

    # update readme
    readme_file_path = '../README.md'
    table_start = '<!-- START OF SINGLE READ TABLE -->'
    table_end = '<!-- END OF SINGLE READ TABLE -->'
    update_markdown_table(readme_file_path, table_start, table_end, all_fields_single_read)

    table_start = '<!-- START OF PAIRED READS TABLE -->'
    table_end = '<!-- END OF PAIRED READS TABLE -->'
    update_markdown_table(readme_file_path, table_start, table_end, all_fields_paired_reads)




 
