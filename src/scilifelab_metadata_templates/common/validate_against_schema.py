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


def validate_against_schema(package, schema_file, *, tsv_file_path=None, tsv_data=None):
    """Validate TSV data against a JSON schema and return a list of errors.

    Provide either `tsv_file_path=` (a path to a TSV file) or `tsv_data=` (already
    loaded rows, as a list of dicts like `load_tsv_data` returns), not both.
    """
    if (tsv_file_path is None) == (tsv_data is None):
        raise ValueError("Provide exactly one of tsv_file_path or tsv_data.")

    errors = []

    # Load the JSON schema
    schema = load_json_schema(package, schema_file)

    # Load the TSV data from file unless it was passed in directly
    if tsv_data is None:
        tsv_data = load_tsv_data(tsv_file_path)
    validator = jsonschema.Draft7Validator(schema)

    for i, row in enumerate(tsv_data):
        for error in validator.iter_errors(row):
            if error.validator == "required":
                # "required" errors have an empty path, and jsonschema raises one error
                # per missing property. validator_value is the full list of required
                # names, so pick the one that is missing from the row and matches this
                # error's message.
                field = next(
                    (
                        name
                        for name in error.validator_value
                        if name not in error.instance
                        and error.message == f"{name!r} is a required property"
                    ),
                    None,
                )
            elif error.path:
                # For other errors (type, enum, pattern, etc.), error.path is the
                # sequence of keys leading to the failing value; its last element is
                # the offending field's name in the row.
                field = error.path[-1]
            else:
                field = None
            errors.append(
                {
                    "row": i + 1,
                    "message": error.message,
                    "field": field,
                }
            )
    return errors
