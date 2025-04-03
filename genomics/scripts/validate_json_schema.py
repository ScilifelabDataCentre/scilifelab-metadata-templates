import json
import csv
import jsonschema
from jsonschema import validate

def load_json_schema(schema_file):
    with open(schema_file, 'r') as file:
        return json.load(file)

def load_tsv_data(tsv_file):
    """
    Load TSV data from a file and return it as a list of dictionaries.
    Each dictionary represents a row in the TSV file, with keys as column headers."""
    with open(tsv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        return list(reader)

def validate_data(tsv_data, schema):
    # Validate each row in the TSV data against the schema
    for i, row in enumerate(tsv_data):
        errors = list(jsonschema.Draft7Validator(schema).iter_errors(row))
        if errors:
            for error in errors:
                print(f"Validation error in row {i+1}:", error.message)
        else:
            print("Validation successful!")

def main():
    # Load the JSON schema
    schema = load_json_schema('../genomics_template_schema_single_read.json')

    # Load the TSV data
    tsv_data = load_tsv_data('../example_data/example-genomics_technical_metadata_single_read.tsv')

    validate_data(tsv_data, schema)

if __name__ == "__main__":
    main()