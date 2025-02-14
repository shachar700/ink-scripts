import re
import os

def remove_tags(input_filename, output_filename):
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Define input and output paths
    input_file = os.path.join(current_dir, '..', 'processed_data', input_filename)
    output_dir = os.path.join(current_dir, '..', 'processed_data')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_filename)

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Remove [ruby=...] [/ruby] tags
            clean_line = re.sub(r'\[ruby=[^\]]+\]|\[/ruby\]', '', line)
            # Remove [group=0001 type=0002 params=]:[group=0001 type=0002 params=]
            clean_line = re.sub(r'\[group=0001 type=0002 params=\]:\[group=0001 type=0002 params=\]', '', clean_line)
            # Skip empty lines
            if clean_line.strip():
                outfile.write(clean_line)

# Process for subject titles
remove_tags('titles_sbj.txt', 'titles_sbj2.txt')

# Process for adjective titles
remove_tags('titles_adj.txt', 'titles_adj2.txt')
