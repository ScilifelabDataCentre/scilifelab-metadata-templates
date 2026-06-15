import json
import csv
import jsonschema
from importlib.resources import files


def load_json_schema(package, schema_file):
    """
    Load a JSON schema from a file.
    """
    schema_file = files(package).joinpath(schema_file)
    with open(schema_file) as f:
        return json.load(f)


def load_tsv_data(tsv_file):
    """
    Load TSV data from a file and return it as a list of dictionaries.
    Each dictionary represents a row in the TSV file, with keys as column headers.
    """
    with open(tsv_file, "r") as file:
        reader = csv.DictReader(file, delimiter="\t")
        return list(reader)


def validate_against_schema(package, schema_file, tsv_file):
    """Validate TSV data against a JSON schema and return a list of errors."""
    errors = []

    # Load the JSON schema
    schema = load_json_schema(package, schema_file)

    # Load the TSV data
    tsv_data = load_tsv_data(tsv_file)
    validator = jsonschema.Draft7Validator(schema)

    for i, row in enumerate(tsv_data):
        for error in validator.iter_errors(row):
            errors.append({"row": i + 1, "message": error.message})
    return errors
