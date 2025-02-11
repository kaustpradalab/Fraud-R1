import json
import os
import pandas as pd

# Folder containing the JSON files
folder_path = 'dataset/FP-base'

# List to store combined data
combined_data = []

# Iterate through all JSON files with "Chinese" in the filename
for filename in os.listdir(folder_path):
    if 'English' in filename and filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            # Ensure data is a list and add to combined_data
            if isinstance(data, list):
                combined_data.extend(data)
            elif isinstance(data, dict):
                combined_data.append(data)

# Convert combined data to a DataFrame
df = pd.DataFrame(combined_data)

# Descriptive analytics for 'category'
category_counts = df['category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']
category_counts['Percentage'] = (category_counts['Count'] / category_counts['Count'].sum()) * 100

# Descriptive analytics for 'subcategory'
subcategory_counts = df['subcategory'].value_counts().reset_index()
subcategory_counts.columns = ['Subcategory', 'Count']
subcategory_counts['Percentage'] = (subcategory_counts['Count'] / subcategory_counts['Count'].sum()) * 100

# Calculate average length of 'raw_data'
def calculate_raw_data_length(raw_data):
    if isinstance(raw_data, str):
        return len(raw_data)
    elif isinstance(raw_data, dict):
        return sum(len(str(k)) + len(str(v)) for k, v in raw_data.items())
    else:
        return 0

# Apply the function to calculate the length
df['raw_data_length'] = df['raw_data'].apply(calculate_raw_data_length)

# Calculate average length
average_length = df['raw_data_length'].mean()

# Display the results
print("Category Analysis:")
print(category_counts.to_string(index=False))

print("\nSubcategory Analysis:")
print(subcategory_counts.to_string(index=False))

print(f"\nAverage Length of 'raw_data': {average_length:.2f} characters")