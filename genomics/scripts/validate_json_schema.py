import json
import csv
import jsonschema
from jsonschema import validate

def load_json_schema(schema_file):
    with open(schema_file, 'r') as file:
        return json.load(file)

def load_tsv_data(tsv_file):
    with open(tsv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        return list(reader)

def validate_data(data, schema):
    try:
        validate(instance=data, schema=schema)
        print("Validation successful!")
    except jsonschema.exceptions.ValidationError as err:
        print("Validation error:", err)

def main():
    # Load the JSON schema
    schema = load_json_schema('../genomics_template_schema_single_read.json')

    # Load the TSV data
    tsv_data = load_tsv_data('../example_data/example-genomics_technical_metadata_single_read.tsv')

    # Validate each row in the TSV data against the schema
    for row in tsv_data:
        validate_data(row, schema)

if __name__ == "__main__":
    main()