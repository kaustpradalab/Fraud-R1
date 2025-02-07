import json
json_file_path = 'baseline-attack/baseline_extract/baseline.json' 

with open(json_file_path, 'r') as file:
    data = json.load(file)

if isinstance(data, list):
    print(f"The file contains {len(data)} entries.")
elif isinstance(data, dict):
    print(f"The file contains 1 entry.")
else:
    print("Unsupported JSON structure.")
