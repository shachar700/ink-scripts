import re

def remove_ruby_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Use regular expression to remove [ruby=...] [/ruby] tags
            clean_line = re.sub(r'\[ruby=[^\]]+\]|\[/ruby\]', '', line)
            outfile.write(clean_line)

# Repeat process for both adjective and subject titles
# Replace 'input.txt' and 'output.txt' with your input and output file paths
input_file = 'C:/Users/User/Documents/githubrepositories/ink-scripts/py/s3/Leaderboards/util/HelpingScripts/titles_sbj.txt'
output_file = 'C:/Users/User/Documents/githubrepositories/ink-scripts/py/s3/Leaderboards/util/HelpingScripts/titles_sbj2.txt'

remove_ruby_tags(input_file, output_file)