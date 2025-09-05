import json
import csv
import jsonschema
from jsonschema import validate
import argparse

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
        for error in errors:
            print(f"Validation error in row {i+1}:", error.message)

def main():
    parser = argparse.ArgumentParser(description="Validate TSV data against the genomics template JSON schema.")
    parser.add_argument("tsv_file", help="Path to the TSV data file")
    parser.add_argument("--schema", default="../genomics_template_schema.json", help="Path to the JSON schema file")
    args = parser.parse_args()

    # Load the JSON schema
    schema = load_json_schema(args.schema)

    # Load the TSV data
    tsv_data = load_tsv_data(args.tsv_file)

    validate_data(tsv_data, schema)

if __name__ == "__main__":
    main()