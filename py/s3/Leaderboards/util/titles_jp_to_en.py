import json
import os

def create_japanese_english_mapping(output_file_adj, output_file_sub):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define paths relative to the current directory
    json_file_japanese = os.path.join(current_dir, '..', 'preprocessed_data', 'JPja_full_unicode.json')
    json_file_english = os.path.join(current_dir, '..', 'preprocessed_data', 'USen_full_unicode.json')

    # Load JSON files
    with open(json_file_japanese, 'r', encoding='utf-8') as jap_file, open(json_file_english, 'r', encoding='utf-8') as eng_file:
        japanese_data = json.load(jap_file)
        english_data = json.load(eng_file)

    fields_to_extract = ["CommonMsg/Byname/BynameAdjective", "CommonMsg/Byname/BynameSubject"]
    adjective_mapping = {}
    subject_mapping = {}

    for field in fields_to_extract:
        japanese_values = japanese_data.get(field, {})
        english_values = english_data.get(field, {})

        for key, japanese_text in japanese_values.items():
            english_text = english_values.get(key, '')
            if japanese_text and english_text:
                if field == "CommonMsg/Byname/BynameAdjective":
                    adjective_mapping[japanese_text] = english_text
                elif field == "CommonMsg/Byname/BynameSubject":
                    subject_mapping[japanese_text] = english_text

    # Output directory in preprocessed_data
    output_dir = os.path.join(current_dir, '..', 'processed_data')

    # Write the mappings to output files
    with open(os.path.join(output_dir, output_file_adj), 'w', encoding='utf-8') as out_file_adj:
        for japanese, english in adjective_mapping.items():
            out_file_adj.write(f'{japanese}:{english}\n')

    with open(os.path.join(output_dir, output_file_sub), 'w', encoding='utf-8') as out_file_sub:
        for japanese, english in subject_mapping.items():
            out_file_sub.write(f'{japanese}:{english}\n')


# Usage example with relative paths
create_japanese_english_mapping('titles_adj.txt', 'titles_sbj.txt')
