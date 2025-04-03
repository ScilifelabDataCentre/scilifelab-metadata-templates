import json

def generate_json_schema(json_data, title="Genomics Template Schema"):

    required = []
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
            if el["cardinality"] == "mandatory":
                required.append(el["name"])

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": title,
        "description": json_data["description"],
        "version": json_data["version"],
        "properties": d,
        "required": required
    }
    
    return schema

def main():
    # Load the single read JSON file
    with open('../genomics_technical_metadata_single_read.json', 'r') as file:
        json_data = json.load(file)

    # Generate the JSON schema
    json_schema = generate_json_schema(json_data["genomics_template"], "Genomics template schema for single reads")

    # Save the JSON schema to a file
    with open('../genomics_template_schema_single_read.json', 'w') as file:
        json.dump(json_schema, file, indent=4)

    print("JSON schema generated and saved to genomics_template_schema_single_read.json")

if __name__ == "__main__":
    main()