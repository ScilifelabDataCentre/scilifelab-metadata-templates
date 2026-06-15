"""
Run generate_genomics_template.py to generate the SciLifeLab internal template
for the technical metadata of genomics data.

It will read the organisational metadata fields from the file
'organisational_metadata_fields.yml' and the description and version fields
for the genomics template from the file 'genomics_template_wrapper.yml', as
well as the relevant ENA fields from the file 'ENA_experiment_metadata_fields.json'.
"""

import json
from pathlib import Path
from importlib.resources import files
from scilifelab_metadata_templates.common.generate_template import (
    collect_fields,
    update_markdown_table,
    wrap_fields_in_template_metadata,
    write_fields_to_json,
    write_field_names_to_tsv,
    generate_json_schema,
)


import update_ENA_controlled_vocabs as ena_cv  # Import the module to update controlled vocabularies


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "templates"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_path = output_dir / "genomics_technical_metadata"

    # update the controlled vocabularies from ENA. Writes to 'technical_metadata_fields_incl_ENA_CVs.json'
    ena_cv.update_controlled_vocabularies()

    # Collect both technical and organisational fields
    all_fields = collect_fields(
        package="genomics",
        technical_fields_file="technical_metadata_fields_incl_ENA_CVs.yml",
    )

    write_field_names_to_tsv(
        package="genomics", output_file_path=output_file_path, all_fields=all_fields
    )

    # wrap in template metadata (name + version) for json file
    wrapped_fields = wrap_fields_in_template_metadata(
        package="genomics", all_fields=all_fields
    )

    # write template to json
    write_fields_to_json(
        package="genomics",
        output_file_path=output_file_path,
        wrapped_fields=wrapped_fields,
    )

    # generate schema
    schema = generate_json_schema(
        wrapped_fields["genomics_template"],
        title="Genomics Technical Metadata Template Schema",
    )

    # Save the JSON schema to a file
    with open(
        output_file_path.with_name(output_file_path.name + "_schema.json"), "w"
    ) as file:
        json.dump(schema, file, indent=4)

    print(
        f"JSON schema generated and saved to {output_file_path.with_name(output_file_path.name + '_schema.json')}"
    )

    # update readme
    readme_file_path = base_dir / "README.md"
    table_start = "<!-- START OF OVERVIEW TABLE -->"
    table_end = "<!-- END OF OVERVIEW TABLE -->"
    update_markdown_table(readme_file_path, table_start, table_end, all_fields)
