import re

def remove_ruby_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Use regular expression to remove [ruby=...] [/ruby] tags
            clean_line = re.sub(r'\[ruby=[^\]]+\]|\[/ruby\]', '', line)
            outfile.write(clean_line)

# Replace 'input.txt' and 'output.txt' with your input and output file paths
input_file = 'C:/Users/User/Documents/github repositories/ink-scripts/py/s3/Leaderboards/util/HelpingLists/titles_sub2.txt'
output_file = 'C:/Users/User/Documents/github repositories/ink-scripts/py/s3/Leaderboards/util/HelpingLists/titles_sub_out.txt'

remove_ruby_tags(input_file, output_file)