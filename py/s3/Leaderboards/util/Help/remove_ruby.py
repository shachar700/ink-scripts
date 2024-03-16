import re

def remove_ruby_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Use regular expression to remove [ruby=...] [/ruby] tags
            clean_line = re.sub(r'\[ruby=[^\]]+\]|\[/ruby\]', '', line)
            outfile.write(clean_line)

# Replace 'input.txt' and 'output.txt' with your input and output file paths
<<<<<<< HEAD:py/s3/Leaderboards/util/HelpingScripts/remove_ruby.py
input_file = 'C:/Users/User/Documents/github repositories/ink-scripts/py/s3/Leaderboards/util/HelpingLists/titles_sub2.txt'
output_file = 'C:/Users/User/Documents/github repositories/ink-scripts/py/s3/Leaderboards/util/HelpingLists/titles_sub_out.txt'
=======
input_file = 'C:/Users/Admin/OneDrive/מסמכים/ink-scripts/py/s3/Leaderboards/util/HelpingScripts/titles_sub.txt'
output_file = 'C:/Users/Admin/OneDrive/מסמכים/ink-scripts/py/s3/Leaderboards/util/HelpingScripts/titles_sub_out.txt'
>>>>>>> a04447490dfe7f18de43ab6b40c63532a7dee696:py/s3/Leaderboards/util/Help/remove_ruby.py

remove_ruby_tags(input_file, output_file)