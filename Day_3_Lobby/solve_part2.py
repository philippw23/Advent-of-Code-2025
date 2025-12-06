
# Read all battery bank strings (one per line) so we can process each independently.
battery_bank = []
with(open("input.txt", "r", encoding="utf-8") as f):
    for line in f:
        line = line.strip()
        if not line:
            continue
        battery_bank.append(line)

joltage = []
JOLTAGE_AMOUNT = 12

for bank in battery_bank:
    best_key = -1
    joltage_val = ""
    for i in range(JOLTAGE_AMOUNT):
        best_key = best_key + 1
        start = best_key
        best_val = int(bank[start])
        # We must leave enough digits on the right for the remaining selections.
        limit = len(bank) - (JOLTAGE_AMOUNT - i - 1)
        # Search from `start` up to `limit` for the strongest digit we can still pick.
        for offset, value in enumerate(bank[start:limit]):
            value = int(value)
            if value > best_val:
                best_val = value
                best_key = start + offset
            if best_val == 9:
                break
        joltage_val = joltage_val + str(best_val)
        
    joltage.append(int(joltage_val))
    
# Sum all constructed joltage codes to produce the final answer.
joltage = sum(joltage)
print(joltage)
