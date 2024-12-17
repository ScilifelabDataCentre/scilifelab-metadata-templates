import csv
import yaml

def get_fields_from_tsv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file, delimiter='\t')
        fields = next(reader)
    return fields

def get_fields_from_yaml(file_path):
    with open(file_path, mode='r') as file:
        data = yaml.safe_load(file)
        fields = list(data.keys())
    return fields

if __name__ == "__main__":
    ena_exp_file_path = 'ENA_experiment_metadata_fields/experiment.tsv'
    ena_exp_fields = get_fields_from_tsv(ena_exp_file_path)

    ena_run_file_path = 'ENA_experiment_metadata_fields/run.tsv'
    ena_run_fields = get_fields_from_tsv(ena_run_file_path)

    single_read_fields = ena_run_fields[2:5]
    paired_reads_fields = [ena_run_fields[2]] + ena_run_fields[5:]

    orga_file_path = '../organisational_metadata_fields.yml'
    orga_fields = get_fields_from_yaml(orga_file_path)

    # leave out alias and title in general, as well as insert_size for single reads
    all_fields_single_read = ena_exp_fields[2:10] + ena_exp_fields[11:] + single_read_fields + orga_fields
    all_fields_paired_reads = ena_exp_fields[2:] + paired_reads_fields + orga_fields

    output_file_path = 'genomics_technical_metadata'

    with open(output_file_path+"_single_read.tsv", mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(all_fields_single_read)

    with open(output_file_path+"_paired_reads.tsv", mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(all_fields_paired_reads)
    print(f"Genomics template fields written to {output_file_path}_single_read.tsv and {output_file_path}_paired_reads.tsv")