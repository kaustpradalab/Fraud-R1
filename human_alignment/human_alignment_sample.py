import os
import json
import random

language = 'Chinese'

def find_json_files(directory):
    json_files = {}
    for root, _, files in os.walk(directory):
        folder_name = os.path.basename(root)
        for file in files:
            if file.endswith('.json') and language in file:
                if folder_name not in json_files:
                    json_files[folder_name] = []
                json_files[folder_name].append(os.path.join(root, file))
    return json_files


def sample_json_entries(folder_json_files, total_samples=51):
    samples = []
    folders_with_data = {}

    # Read and collect data from each folder
    for folder, files in folder_json_files.items():
        folder_data = []
        for file_path in files:
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list) and data:
                        # Add folder name to each entry
                        for entry in data:
                            entry['folder_name'] = folder
                        folder_data.extend(data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file: {file_path}")
        if folder_data:
            folders_with_data[folder] = folder_data

    # Calculate how many samples to take from each folder
    num_folders = len(folders_with_data)
    if num_folders == 0:
        print("No valid JSON files found with 'Chinese' in the name.")
        return []

    samples_per_folder = total_samples // num_folders
    extra_samples = total_samples % num_folders

    # Sample from each folder
    for i, (folder, data) in enumerate(folders_with_data.items()):
        n_samples = samples_per_folder + (1 if i < extra_samples else 0)
        samples.extend(random.sample(data, min(n_samples, len(data))))

    return samples


def save_samples(samples, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(samples, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_directory = "results/one-round-LevelAttack/assistant"  # Replace with your directory path
    output_file = "human_alignment/50sample_oneRound_" + language + ".json"

    folder_json_files = find_json_files(input_directory)
    sampled_entries = sample_json_entries(folder_json_files)

    if sampled_entries:
        save_samples(sampled_entries, output_file)
        print(f"Saved {len(sampled_entries)} samples to {output_file}")
    else:
        print("No samples were saved.")
