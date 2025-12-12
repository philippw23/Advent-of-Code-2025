
# Read every battery bank (one per line) as a string of digits.
battery_bank = []
with(open("input.txt", "r", encoding="utf-8") as f):
    for line in f:
        line = line.strip()
        if not line:
            continue
        battery_bank.append(line)

joltage = []
JOLTAGE_AMOUNT = 2

# For each bank pick the two strongest digits, scanning left-to-right without reusing positions.
for bank in battery_bank:
    best_key = -1
    joltage_val = ""
    for i in range(JOLTAGE_AMOUNT):
        best_key = best_key + 1
        start = best_key
        best_val = int(bank[start])
        # limit keeps enough digits on the right for the remaining picks (e.g. with two picks left we stop at len-1).
        limit = len(bank) - (JOLTAGE_AMOUNT - i - 1)
        # Scan forward from the current start up to limit to find the best digit we can take at this position.
        for offset, value in enumerate(bank[start:limit]):
            value = int(value)
            if value > best_val:
                best_val = value
                best_key = start + offset
            if best_val == 9:
                break
        joltage_val = joltage_val + str(best_val)
        
    joltage.append(int(joltage_val))
    
# The answer is the sum of all per-bank joltage values.
joltage = sum(joltage)
print(joltage)
