"""
Run generate_genomics_template.py to generate the SciLifeLab internal template
for the technical metadata of genomics data.

It will read the organisational metadata fields from the file
'organisational_metadata_fields.yml' and the description and version fields
for the genomics template from the file 'genomics_template_wrapper.yml', as
well as the relevant ENA fields from the file 'ENA_experiment_metadata_fields.json'.
"""

from pathlib import Path
from scilifelab_metadata_templates.common.generate_template import (
    collect_fields,
    update_markdown_table,
    wrap_fields_in_template_metadata,
    write_fields_to_json,
    write_field_names_to_tsv,
    generate_json_schema,
    find_repo_root
)

from scilifelab_metadata_templates.genomics import update_ENA_controlled_vocabs as ena_cv  # Import the module to update controlled vocabularies


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "templates"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file_path = output_dir / "genomics_technical_metadata"
    
    repo_root = find_repo_root(base_dir)
    public_templates_dir_file_path = None
    if repo_root:
        public_templates_dir = repo_root / base_dir.name /"templates"
        public_templates_dir.mkdir(exist_ok=True)
        public_templates_dir_file_path = public_templates_dir / output_file_path.name

    # update the controlled vocabularies from ENA. Writes to 'technical_metadata_fields_incl_ENA_CVs.json'
    output_paths = [x for x in (output_file_path, public_templates_dir_file_path) if x]
    ena_cv.update_controlled_vocabularies()

    # Collect both technical and organisational fields
    all_fields = collect_fields(
        package="genomics",
        technical_fields_file="technical_metadata_fields_incl_ENA_CVs.yml",
    )

    write_field_names_to_tsv(
        package="genomics", 
        output_file_paths=output_paths, 
        all_fields=all_fields
    )

    # wrap in template metadata (name + version) for json file
    wrapped_fields = wrap_fields_in_template_metadata(
        package="genomics", all_fields=all_fields
    )

    # write template to json in both package and public templates directory
    write_fields_to_json(
        package="genomics",
        output_file_paths=output_paths,
        json_data=wrapped_fields,
    )

    # generate schema
    schema = generate_json_schema(
        wrapped_fields["genomics_template"],
        title="Genomics Technical Metadata Template Schema",
    )

    # Save the JSON schema to files in both package and public templates directory
    write_fields_to_json(
        package="genomics",
        output_file_paths=[x.with_name(x.name + "_schema.json") for x in output_paths],
        json_data=schema,
    )
    
    print(
        f"JSON schema generated and saved to {', '.join([str(x.with_name(x.name+ '_schema.json')) for x in output_paths])}"
    )

    # update readme
    readme_file_path = base_dir / "README.md"
    table_start = "<!-- START OF OVERVIEW TABLE -->"
    table_end = "<!-- END OF OVERVIEW TABLE -->"
    update_markdown_table(readme_file_path, table_start, table_end, all_fields)
