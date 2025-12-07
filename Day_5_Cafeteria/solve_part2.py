ingredient_ranges = []

with open("input.txt", "r", encoding="utf-8") as f:
    for key, line in enumerate(f):
        if line.strip() == "":  # empty line => end of paragraph
            end_of_first_paragraph = key
            break
        ingredient_ranges.append(line.rstrip("\n"))

ranges = []
for ingredient_range in ingredient_ranges:
    start, end = map(int, ingredient_range.split("-"))
    ranges.append((start, end))
        #print(f"Ingredient ID {id} is allowed in range {ingredient_range}")
        # break

ranges.sort(key=lambda r: r[0])  # sort by start of range

merged_ranges = []
current_start, current_end = ranges[0]
for start, end in ranges[1:]:
    if start <= current_end + 1:  # overlapping or contiguous ranges
        current_end = max(current_end, end)
    else:
        merged_ranges.append((current_start, current_end))
        current_start, current_end = start, end

merged_ranges.append((current_start, current_end))  # add the last range
ids = []
for start, end in merged_ranges:
    ids.append(end - start + 1)
    
print(f"Number of fresh ingredients ids: {sum(ids)}")


