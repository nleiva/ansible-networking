from jsonschema import validate
import json

with open('files/schema.json') as f:
  schema = json.load(f)

with open('files/neighbors.json') as f:
  data = json.load(f)

for neighbor in data:
    print(json.dumps(neighbor, indent=2))
    validate(instance=neighbor, schema=schema)

# with open('files/schema-array.json') as f:
#   schema = json.load(f)

# validate(instance=data, schema=schema)