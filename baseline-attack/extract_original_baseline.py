import json

file1= ""
file2= ""

# Load the first JSON file
with open('file1.json', 'r') as f1:
    data1 = json.load(f1)

# Load the second JSON file
with open('file2.json', 'r') as f2:
    data2 = json.load(f2)

# Create a set of (lang, id) pairs from the first file
match_set = {(entry['lang'], entry['id']) for entry in data1}

# Filter entries in the second file based on matches
filtered_data = [entry for entry in data2 if (entry['lang'], entry['id']) in match_set]

# Save the filtered data to a new JSON file
with open('filtered_file2.json', 'w') as outfile:
    json.dump(filtered_data, outfile, indent=4)

print(f"Filtered {len(filtered_data)} entries saved to 'filtered_file2.json'")
