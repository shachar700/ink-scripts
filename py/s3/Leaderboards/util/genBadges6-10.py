import re

with open("badgemap_old.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

pattern = re.compile(r'^(\d+):(.+?) (\d+)$')

seen_ids = set()
seen_name_levels = set()
parsed_lines = []

for line in lines:
    match = pattern.match(line)
    if not match:
        parsed_lines.append((line, None, None, None))
        continue
    id_num = int(match.group(1))
    name = match.group(2).strip()
    level = int(match.group(3))

    seen_ids.add(id_num)
    seen_name_levels.add((name, level))
    parsed_lines.append((line, id_num, name, level))

output_lines = []
for original, id_num, name, level in parsed_lines:
    output_lines.append((id_num, original)) if id_num is not None else output_lines.append((float('inf'), original))

    if level in (4, 5):
        current_id = id_num
        for new_level in range(level + 1, 11):
            key = (name, new_level)
            if key in seen_name_levels:
                continue
            current_id += 1
            while current_id in seen_ids:
                current_id += 1

            new_line = f"{current_id}:{name} {new_level}"
            output_lines.append((current_id, new_line))
            seen_ids.add(current_id)
            seen_name_levels.add(key)

# Sort by numeric ID
output_lines.sort(key=lambda x: x[0])

# Write sorted output
with open("badgemap_extended.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(line for _, line in output_lines))

print("✅ Extended badge map sorted by ID saved to badgemap_extended.txt")
