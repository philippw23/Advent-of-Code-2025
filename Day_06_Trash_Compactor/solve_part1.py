import re

items = []
with open("input.txt", "r", encoding="utf-8") as file:
    for line in file:
        parts = re.split(r"\s+", line.strip())
        items.append(parts)

length = len(items)
total = 0

for col, op in enumerate(items[-1]):
    column_values = [int(row[col]) for row in items[:-1]]

    if op == "+":
        total += sum(column_values)
    elif op == "*":
        product = 1
        for value in column_values:
            product *= value
        total += product

print(f"Total sum: {total}")