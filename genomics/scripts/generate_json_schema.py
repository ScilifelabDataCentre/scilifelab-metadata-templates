import json

def generate_json_schema(json_data, title="Genomics Template Schema"):

    required = []
    required_if_paired = []
    d = {}

    for el in json_data["fields"]:
        if isinstance(el, dict):
            if el["field_type"] in ["TEXT_FIELD", "TEXT_AREA_FIELD"]:
                d[el["name"]] = {
                    "type": "string",
                    "description": el["description"]
                }
            elif el["field_type"] == "TEXT_CHOICE_FIELD":
                d[el["name"]] = {
                    "type": "string",
                    "description": el["description"],
                    "enum": el["controlled_vocabulary"]                            
                }
            elif el["field_type"] == "DATE_FIELD":
                d[el["name"]] = {
                    "type": "string",
                    "description": el["description"],
                    "format": "date"
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
        "if": {
            "properties": { "library_layout": { "string": "PAIRED" } }
        },
        "then": {
            "required": required_if_paired
        }
    }
    
    return schema

def main():
    # Load the single read JSON file
    with open('../genomics_technical_metadata.json', 'r') as file:
        json_data = json.load(file)

    # Generate the JSON schema
    json_schema = generate_json_schema(json_data["genomics_template"], "Genomics template schema")

    # Save the JSON schema to a file
    with open('../genomics_template_schema.json', 'w') as file:
        json.dump(json_schema, file, indent=4)

    print("JSON schema generated and saved to genomics_template_schema.json")

if __name__ == "__main__":
    main()