# The big cephalopods come back to check on how things are going. When they see that your grand total doesn't match the one expected by the worksheet, they realize they forgot to explain how to read cephalopod math.

# Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the most significant digit at the top and the least significant digit at the bottom. (Problems are still separated with a column consisting only of spaces, and the symbol at the bottom of the problem is still the operator to use.)
file_name = "input.txt"

with open(file_name, "r", encoding="utf-8") as file:
    lines = file.read().splitlines()

max_len = max(len(line) for line in lines)
padded = [line.ljust(max_len) for line in lines]
value_rows = len(padded) - 1
op_row = padded[-1]

total = 0
current_numbers = []
current_op = None

for col in range(max_len - 1, -1, -1):
    digits = "".join(
        padded[row][col] for row in range(value_rows) if padded[row][col].isdigit()
    )
    op_char = op_row[col]

    if digits or op_char != " ":
        if digits:
            current_numbers.append(int(digits))
        if op_char != " ":
            current_op = op_char
    else:
        if current_numbers and current_op:
            if current_op == "+":
                total += sum(current_numbers)
            elif current_op == "*":
                product = 1
                for number in current_numbers:
                    product *= number
                total += product
        current_numbers = []
        current_op = None

if current_numbers and current_op:
    if current_op == "+":
        total += sum(current_numbers)
    elif current_op == "*":
        product = 1
        for number in current_numbers:
            product *= number
        total += product

print(f"Total sum: {total}")
