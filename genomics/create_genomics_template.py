import csv
import yaml
import json
import copy

def get_fields_from_tsv(file_path):
    with open(file_path, mode='r') as f:
        reader = csv.reader(f, delimiter='\t')
        fields = next(reader)
    return fields

def write_fields_to_tsv(file_path, fields):
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(fields)

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

if __name__ == "__main__":

    # Step 0: get organisational metadata fields
    orga_file_path = '../organisational_metadata_fields.yml'
    orga_fields = get_fields_from_yaml(orga_file_path, 'organisational_metadata')
    orga_field_names = [field['name'] for field in orga_fields]

    # Step 1: generate tsv files for genomics technical metadata template

    # get ENA experiment and run metadata fields
    ena_exp_file_path = 'ENA_experiment_metadata_fields/experiment.tsv'
    ena_exp_field_names = get_fields_from_tsv(ena_exp_file_path)

    ena_run_file_path = 'ENA_experiment_metadata_fields/run.tsv'
    ena_run_field_names = get_fields_from_tsv(ena_run_file_path)

    # for single read use single file fields, leave out alias and experiment_alias fields
    single_read_field_names = ena_run_field_names[2:5]
    # for paired reads use forward and reverse file fields
    paired_reads_field_names = [ena_run_field_names[2]] + ena_run_field_names[5:]

    # leave out insert_size for single reads
    all_field_names_single_read = ena_exp_field_names[:10] + ena_exp_field_names[11:] + single_read_field_names + orga_field_names
    all_field_names_paired_reads = ena_exp_field_names + paired_reads_field_names + orga_field_names

    # write to individual tsv files
    output_file_path = 'genomics_technical_metadata'
    write_fields_to_tsv(output_file_path+"_single_read.tsv", all_field_names_single_read)
    write_fields_to_tsv(output_file_path+"_paired_reads.tsv", all_field_names_paired_reads)
    print(f"Genomics template field names written to {output_file_path}_single_read.tsv and {output_file_path}_paired_reads.tsv")

    # Step 2: generate json schema for genomics technical metadata template

    # get relevant json schema fields prefilled with CV terms fetched from ENA
    json_file_path_ENA_fields = 'ENA_experiment_metadata_fields/ENA_experiment_metadata_fields.json'
    experiment_fields = get_fields_from_json(json_file_path_ENA_fields, 'experiment')
    run_fields = get_fields_from_json(json_file_path_ENA_fields, 'run')
    
    # merge them to one json schema
    all_fields_merged = experiment_fields + run_fields + orga_fields

    # for single read use single file fields, leave out alias and experiment_alias fields
    single_read_fields = run_fields[2:5]
    # for paired reads use forward and reverse file fields
    paired_reads_fields = [ run_fields[2] ] + run_fields[5:]

    # leave out insert_size for single reads
    all_fields_single_read = experiment_fields[:10] + experiment_fields[11:] + single_read_fields + orga_fields
    all_fields_paired_reads = experiment_fields + paired_reads_fields + orga_fields
    
    # get the metadata wrapper for the genomics template
    internal_metadata_file_path = 'genomics_template_wrapper.yaml'
    with open(internal_metadata_file_path, mode='r') as f:
        internal_metadata = yaml.safe_load(f)
   
    # add the fields for single read and save to file
    internal_metadata['genomics_template']['fields'] = all_fields_single_read
    with open(output_file_path+"_single_read.json", mode='w') as f:
        json.dump(internal_metadata, f, indent=4)

    # add the fields for paired reads  and save to file 
    internal_metadata['genomics_template']['fields'] = all_fields_paired_reads
    with open(output_file_path+"_paired_reads.json", mode='w') as f:
        json.dump(internal_metadata, f, indent=4)
    
    print(f"Genomics template written to {output_file_path}_single_read.json and {output_file_path}_paired_reads.json")


 
