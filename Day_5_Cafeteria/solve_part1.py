ingredient_ranges = []
ingriedients = []
with open("input.txt", "r", encoding="utf-8") as f:
    for key, line in enumerate(f):
        if line.strip() == "":  # empty line => end of paragraph
            end_of_first_paragraph = key
            break
        ingredient_ranges.append(line.rstrip("\n"))

    for line in f:
        ingriedients.append(line.rstrip("\n"))

fresh_counter = 0
for id in ingriedients:
    for ingredient_range in ingredient_ranges:
        start, end = map(int, ingredient_range.split("-"))
        if start <= int(id) <= end:
            fresh_counter += 1
            #print(f"Ingredient ID {id} is allowed in range {ingredient_range}")
            break
        else:
            pass
            #print(f"Ingredient ID {id} is NOT allowed in any range")

print(f"Number of fresh ingredients: {fresh_counter}") 

