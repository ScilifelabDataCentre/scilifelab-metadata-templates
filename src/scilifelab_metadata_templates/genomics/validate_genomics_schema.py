import argparse
from scilifelab_metadata_templates.common.validate_against_schema import (
    validate_against_schema,
)


def validate_genomics_data(tsv_file, schema_file):
    """Validate TSV data against the genomics template JSON schema."""
    if not schema_file:
        print("No schema file provided. Using bundled schema from package data.")
        schema_file = "genomics_technical_metadata_schema.json"
    return validate_against_schema(
        "scilifelab_metadata_templates.genomics.templates", schema_file, tsv_file
    )


def main():
    parser = argparse.ArgumentParser(
        description="Validate TSV data against the genomics template JSON schema."
    )
    parser.add_argument("tsv_file", help="Path to the TSV data file")
    parser.add_argument(
        "--schema",
        default=None,
        help="Path to the JSON schema file (default: bundled schema)",
    )
    args = parser.parse_args()

    for error in validate_genomics_data(args.tsv_file, args.schema):
        print(f"Validation error in Row {error['row']}: {error['message']}")


if __name__ == "__main__":
    main()
