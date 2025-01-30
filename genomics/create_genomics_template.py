import csv
import yaml
import json
import copy
import yaml

def get_fields_from_tsv(file_path):
    with open(file_path, mode='r') as f:
        reader = csv.reader(file, delimiter='\t')
        fields = next(reader)
    return fields

def get_fields_from_yaml(file_path):
    with open(file_path, mode='r') as f:
        data = yaml.safe_load(f)
        fields = list(data.keys())
    return fields

if __name__ == "__main__":
    # get ENA experiment metadata fields
    ena_exp_file_path = 'ENA_experiment_metadata_fields/experiment.tsv'
    ena_exp_fields = get_fields_from_tsv(ena_exp_file_path)

    # get ENA run metadata fields
    ena_run_file_path = 'ENA_experiment_metadata_fields/run.tsv'
    ena_run_fields = get_fields_from_tsv(ena_run_file_path)

    # for single read use single file fields, leave out alias and experiment_alias fields
    single_read_fields = ena_run_fields[2:5]
    # for paired reads use forward and reverse file fields
    paired_reads_fields = [ena_run_fields[2]] + ena_run_fields[5:]

    # get organisational metadata fields
    orga_file_path = '../organisational_metadata_fields.yml'
    orga_fields = get_fields_from_yaml(orga_file_path)

    # leave out insert_size for single reads
    all_fields_single_read = ena_exp_fields[:10] + ena_exp_fields[11:] + single_read_fields + orga_fields
    all_fields_paired_reads = ena_exp_fields + paired_reads_fields + orga_fields

    # write to individual tsv files
    output_file_path = 'genomics_technical_metadata'
    
    with open(output_file_path+"_single_read.tsv", mode='w', newline='') as f:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(all_fields_single_read)

    with open(output_file_path+"_paired_reads.tsv", mode='w', newline='') as f:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(all_fields_paired_reads)
    print(f"Genomics template fields written to {output_file_path}_single_read.tsv and {output_file_path}_paired_reads.tsv")

    # get relevant json schema fields
    json_file_path_ENA_fields = 'ENA_experiment_metadata_fields/ENA_experiment_metadata_fields.json'
    with open(json_file_path_ENA_fields, mode='r') as f:
        data = json.load(f)
        experiment_fields = data.get('experiment', {})
        run_fields = data.get('run', {})

    json_file_path_orga_fields = '../organisational_metadata_fields.json'
    with open(json_file_path_orga_fields, mode='r') as f:
        data = json.load(f)
        orga_fields = data.get('organisational_metadata', {})
    
    ## Keep only the fields and merge them to one json schema
    experiment_run_merged = experiment_fields['fields'] + run_fields['fields'] 
    experiment_run_orga_merged= experiment_run_merged+ orga_fields['fields']

    
    # get the internal metadata
    internal_metadata_file_path = 'genomics_technical_metadata.yaml'
    with open(internal_metadata_file_path, mode='r') as f:
        internal_metadata = yaml.safe_load(f)
   
   #add the fields to the internal_metadata    
    internal_metadata['fields']=experiment_run_orga_merged

    with open(output_file_path+".json", mode='w') as f:
        json.dump(internal_metadata, f, indent=4)

 
