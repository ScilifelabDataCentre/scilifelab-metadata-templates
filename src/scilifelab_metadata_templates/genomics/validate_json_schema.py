import json
import csv
import jsonschema
import argparse
from importlib.resources import files

def load_json_schema(schema_file=None):
    if schema_file is None:
        # Load bundled schema from package data
        schema_file = files("scilifelab_metadata_templates.genomics.templates").joinpath(
            "genomics_technical_metadata_schema.json"
        )
    with open(schema_file) as f:
        return json.load(f)

def load_tsv_data(tsv_file):
    """
    Load TSV data from a file and return it as a list of dictionaries.
    Each dictionary represents a row in the TSV file, with keys as column headers."""
    with open(tsv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        return list(reader)

def validate_data(tsv_data, schema):
    """Validate each row in the TSV data against the schema"""
    errors = []
    validator = jsonschema.Draft7Validator(schema)
    for i, row in enumerate(tsv_data):
        for error in validator.iter_errors(row):
            errors.append({"row": i + 1, "message": error.message})
    return errors

def main():
    parser = argparse.ArgumentParser(description="Validate TSV data against the genomics template JSON schema.")
    parser.add_argument("tsv_file", help="Path to the TSV data file")
    parser.add_argument("--schema", default=None, help="Path to the JSON schema file (default: bundled schema)")
    args = parser.parse_args()

    # Load the JSON schema
    schema = load_json_schema(args.schema)

    # Load the TSV data
    tsv_data = load_tsv_data(args.tsv_file)

    for error in validate_data(tsv_data, schema):
        print(f"Validation error in Row {error['row']}: {error['message']}")

if __name__ == "__main__":
    main()