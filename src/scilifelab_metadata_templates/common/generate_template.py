"""
generate_template.py contains functions to generate the SciLifeLab internal template
for the technical metadata of omics data.

It will read the organisational metadata fields from the file
'organisational_metadata_fields.yml' and the description and version fields
for the relevant template from the file '{package}_template_wrapper.yml'
"""

import csv
import yaml
import json
from importlib.resources import files


def collect_fields(package, technical_fields_file):

    orga_file_path = files("scilifelab_metadata_templates.data").joinpath(
        "organisational_metadata_fields.yml"
    )
    orga_fields = get_fields_from_yaml(orga_file_path, "organisational_metadata")

    # get relevant yaml fields prefilled with CV terms fetched from ENA
    yaml_file_path_technical_fields = files(
        f"scilifelab_metadata_templates.{package}.data"
    ).joinpath(technical_fields_file)
    technical_metadata_fields = get_fields_from_yaml(
        yaml_file_path_technical_fields, "technical_metadata_fields"
    )

    return technical_metadata_fields + orga_fields


def get_fields_from_yaml(file_path, label):
    try:
        with open(file_path, mode="r") as f:
            data = yaml.safe_load(f)
            fields = data.get(label, {}).get("fields", [])
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        fields = []
    except yaml.YAMLError as e:
        print("Error reading YAML:", e)
        fields = []
    return fields


def write_field_names_to_tsv(package, output_file_paths, all_fields):
    for output_file_path in output_file_paths:
        with open(output_file_path.with_suffix(".tsv"), mode="w", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow([field["name"] for field in all_fields])

        print(
            f"{package} template field names written to {output_file_path.with_suffix('.tsv')}"
        )


def wrap_fields_in_template_metadata(package, all_fields):

    wrapper_file_path = files(f"scilifelab_metadata_templates.{package}.data").joinpath(
        f"{package}_template_wrapper.yml"
    )
    try:
        with open(wrapper_file_path, mode="r") as f:
            omics_template = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"File '{wrapper_file_path}' not found.")
        return
    except yaml.YAMLError as e:
        print("Error reading YAML:", e)
        return

    # add the fields
    omics_template[f"{package}_template"]["fields"] = all_fields

    return omics_template


def write_fields_to_json(package, output_file_paths, json_data):

    for output_file_path in output_file_paths:
        with open(output_file_path.with_suffix(".json"), mode="w") as f:
            json.dump(json_data, f, indent=4)

    print(f"{package} template written to {[str(path.with_suffix('.json')) for path in output_file_paths]}")


def generate_json_schema(json_data, title):

    required = []
    required_if_paired = []
    d = {}

    for el in json_data["fields"]:
        if isinstance(el, dict):
            if el["field_type"] in ["TEXT_FIELD", "TEXT_AREA_FIELD"]:
                d[el["name"]] = {"type": "string", "description": el["description"]}
            elif el["field_type"] == "TEXT_CHOICE_FIELD":
                d[el["name"]] = {
                    "type": "string",
                    "description": el["description"],
                    "enum": el["controlled_vocabulary"],
                }
            elif el["field_type"] == "DATE_FIELD":
                d[el["name"]] = {
                    "type": "string",
                    "description": el["description"],
                    "format": "date",
                }
            if el["requirement"] == "mandatory_for_data_producer":
                required.append(el["name"])
            elif el["requirement"] == "mandatory_for_data_producer_if_paired_reads":
                required_if_paired.append(el["name"])

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": title,
        "description": json_data["description"],
        "version": json_data["version"],
        "properties": d,
        "required": required,
        "if": {"properties": {"library_layout": {"string": "PAIRED"}}},
        "then": {"required": required_if_paired},
    }

    return schema


def generate_markdown_table(data_dict):
    # Generate a Markdown table from a dictionary
    table_content = "| Field Name | Requirement | Description | Controlled vocabulary |\n| ---------- | ---------- | ------------ | ---------- |\n"
    for field in data_dict:
        table_content += f"| {field['name']} | {field['requirement']} | {field['description']}  | {', '.join(str(x) for x in field['controlled_vocabulary'])} \n"
    return table_content


def update_markdown_table(file_path, table_start, table_end, data_dict):
    # Read the content of the Markdown file
    try:
        with open(file_path, "r") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return

    # Find the start and end indices of the table using a marker
    start_index = content.find(table_start)
    end_index = content.find(table_end)

    # Generate the updated table content from the dictionary
    new_table_content = generate_markdown_table(data_dict)

    # Replace the old table content with the updated one
    content = f"{content[:start_index]}{table_start}\n{new_table_content}{content[end_index:]}"

    # Write the modified content back to the file
    with open(file_path, "w") as file:
        file.write(content)


def get_fields_from_json(file_path, label):
    try:
        with open(file_path, mode="r") as f:
            data = json.load(f)
            fields = data.get(label, {}).get("fields", [])
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        fields = []
    except json.JSONDecodeError as e:
        print("Error reading JSON:", e)
        fields = []
    return fields

def find_repo_root(start):
    for path in [start, *start.parents]:
        if (path/ ".git").exists() and (path / "pyproject.toml").exists():
            return path
    return None