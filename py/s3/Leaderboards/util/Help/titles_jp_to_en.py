import json

def create_japanese_english_mapping(json_file_japanese, json_file_english, output_file_adj, output_file_sub):
    with open(json_file_japanese, 'r', encoding='utf-8') as jap_file, open(json_file_english, 'r',
                                                                           encoding='utf-8') as eng_file:
        japanese_data = json.load(jap_file)
        english_data = json.load(eng_file)

    # Define the fields to extract
    fields_to_extract = ["CommonMsg/Byname/BynameAdjective", "CommonMsg/Byname/BynameSubject"]

    # Create mappings for Adjective and Subject
    adjective_mapping = {}
    subject_mapping = {}

    for field in fields_to_extract:
        japanese_values = japanese_data.get(field, {})
        english_values = english_data.get(field, {})

        for key, japanese_text in japanese_values.items():
            english_text = english_values.get(key, '')  # Corresponding English text
            if japanese_text and english_text:
                if field == "CommonMsg/Byname/BynameAdjective":
                    adjective_mapping[japanese_text] = english_text
                elif field == "CommonMsg/Byname/BynameSubject":
                    subject_mapping[japanese_text] = english_text

    # Write the mappings to the output files
    with open(output_file_adj, 'w', encoding='utf-8') as out_file_adj:
        for japanese, english in adjective_mapping.items():
            out_file_adj.write(f'{japanese}:{english}\n')

    with open(output_file_sub, 'w', encoding='utf-8') as out_file_sub:
        for japanese, english in subject_mapping.items():
            out_file_sub.write(f'{japanese}:{english}\n')


# Replace 'japanese.json', 'english.json', 'titles_adj.txt', and 'titles_sub.txt' with your file paths
<<<<<<< HEAD:py/s3/Leaderboards/util/HelpingScripts/titles_jp_to_en.py
json_file_japanese = 'C:/Users/User/Documents/github repositories/ink-scripts/py/s3/Leaderboards/util/FromLean/JPja_full_unicode.json'
json_file_english = 'C:/Users/User/Documents/github repositories/ink-scripts/py/s3/Leaderboards/util/FromLean/USen_full_unicode.json'
output_file_adj = 'titles_adj2.txt'
output_file_sub = 'titles_sub2.txt'
=======
json_file_japanese = 'C:/Users/Admin/OneDrive/מסמכים/ink-scripts/py/s3/Leaderboards/util/FromLean/JPja_full_unicode.json'
json_file_english = 'C:/Users/Admin/OneDrive/מסמכים/ink-scripts/py/s3/Leaderboards/util/FromLean/USen_full_unicode.json'
output_file_adj = 'titles_adj.txt'
output_file_sub = 'titles_sub.txt'
>>>>>>> a04447490dfe7f18de43ab6b40c63532a7dee696:py/s3/Leaderboards/util/Help/titles_jp_to_en.py

create_japanese_english_mapping(json_file_japanese, json_file_english, output_file_adj, output_file_sub)
