"""
Run create_genomics_template.py to create a SciLifeLab internal template 
for the technical metadata of genomics data.

It will read the organisational metadata fields from the file 
'organisational_metadata_fields.yml' and the description and version fields 
for the genomics template from the file 'genomics_template_wrapper.yml', as 
well as the relevant ENA fields from the file 'ENA_experiment_metadata_fields.json'.
"""

import csv
import yaml
import json

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

def collect_fields(output_file_path):

    orga_file_path = '../../organisational_metadata_fields.yml'
    orga_fields = get_fields_from_yaml(orga_file_path, 'organisational_metadata')

    # get relevant json fields prefilled with CV terms fetched from ENA
    json_file_path_ENA_fields = 'ENA_technical_metadata_fields.json'
    experiment_fields = get_fields_from_json(json_file_path_ENA_fields, 'experiment')
    run_fields = get_fields_from_json(json_file_path_ENA_fields, 'run')
 
    all_fields_single_read = (
        experiment_fields[:10] + experiment_fields[11:] # leave out insert_size
        + run_fields[2:5] # use single file fields, leave out alias and experiment_alias fields
        + orga_fields
    )
    all_fields_paired_reads = (
        experiment_fields 
        + [ run_fields[2] ] + run_fields[5:] # use forward and reverse file fields
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

    all_fields_single_read, all_fields_paired_reads = collect_fields(output_file_path)
    
    write_fields_to_json(output_file_path, all_fields_single_read, all_fields_paired_reads)

    write_field_names_to_tsv(output_file_path, all_fields_single_read, all_fields_paired_reads)

    




 
