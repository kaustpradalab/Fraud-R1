import json
import os
from difflib import SequenceMatcher


folder_path = 'baseline-attack/fp_base_result/o3-mini'  
combined_data = []

for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):
                combined_data.extend(data)
            elif isinstance(data, dict):
                combined_data.append(data)

# Save the combined data into a new JSON file
with open('baseline-attack/baseline_extract/temp.json', 'w') as outfile:
    json.dump(combined_data, outfile, indent=4)

print(f"Combined {len(combined_data)} entries saved to 'baseline-attack/baseline_extract/temp.json'")




with open('baseline-attack/baseline_extract/baseline.json', 'r') as f1:
    data1 = json.load(f1)

with open('baseline-attack/baseline_extract/temp.json', 'r') as f2:
    data2 = json.load(f2)

def compute_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to find the most similar entry
def find_most_similar(entry1, candidates):
    max_similarity = 0
    best_match = None

    for entry2 in candidates:
        if (entry1.get('language') == entry2.get('language') and
            entry1.get('subcategory') == entry2.get('subcategory') and
            entry1.get('data_type') == entry2.get('data_type')):

            raw_data1 = entry1.get('raw_data', '')
            raw_data2 = entry2.get('raw_data', '')

            if isinstance(raw_data1, dict):
                raw_data1_str = raw_data1.get('description', '')
            else:
                raw_data1_str = str(raw_data1)

            if isinstance(raw_data2, dict):
                raw_data2_str = raw_data2.get('description', '')
            else:
                raw_data2_str = str(raw_data2)

            similarity = compute_similarity(raw_data1_str, raw_data2_str)
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = entry2
    return best_match if best_match else {}

# Find most similar entries for each entry in file1
selected_entries = []
for entry1 in data1:
    best_match = find_most_similar(entry1, data2)
    selected_entries.append(best_match)

with open('baseline-attack/baseline_extract/filtered_output.json', 'w') as outfile:
    json.dump(selected_entries, outfile, indent=4)

print(f"Selected {len(selected_entries)} entries saved to 'baseline-attack/baseline_extract/filtered_output.json'")
