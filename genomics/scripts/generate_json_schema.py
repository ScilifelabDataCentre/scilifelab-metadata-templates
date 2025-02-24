import json

def generate_json_schema(json_data):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {}
    }

    for key, value in json_data.items():
        if isinstance(value, str):
            schema["properties"][key] = {
                "type": "string",
                "description": value
            }
        elif isinstance(value, list):
            d = {}
            required = []
            for el in value:
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
            print(d)
            schema["properties"][key] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": d,
                    "required": required
                }
            }
        elif isinstance(value, dict):
            schema["properties"][key] = generate_json_schema(value)
        else:
            schema["properties"][key] = {
                "type": "string"
            }

    return schema

def main():
    # Load the single read JSON file
    with open('../genomics_technical_metadata_single_read.json', 'r') as file:
        json_data = json.load(file)

    # Generate the JSON schema
    json_schema = generate_json_schema(json_data["genomics_template"])

    # Save the JSON schema to a file
    with open('../genomics_template_schema_single_read.json', 'w') as file:
        json.dump(json_schema, file, indent=4)

    print("JSON schema generated and saved to genomics_template_schema_single_read.json")

if __name__ == "__main__":
    main()