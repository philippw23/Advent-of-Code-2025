# The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-).

# Since the young Elf was just doing silly patterns, you can find the invalid IDs by looking for any ID 
# which is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.

# None of the numbers have leading zeroes; 0101 isn't an ID at all. (101 is a valid ID that you would ignore.)

# Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:

# 11-22 has two invalid IDs, 11 and 22.
# 95-115 has one invalid ID, 99.
# 998-1012 has one invalid ID, 1010.
# 1188511880-1188511890 has one invalid ID, 1188511885.
# 222220-222224 has one invalid ID, 222222.
# 1698522-1698528 contains no invalid IDs.
# 446443-446449 has one invalid ID, 446446.
# 38593856-38593862 has one invalid ID, 38593859.
# The rest of the ranges contain no invalid IDs.
# Adding up all the invalid IDs in this example produces 1227775554.

ids = []

with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read().strip()
    for element in text.split(","):
        id = element.split("-")
        ids.append(id)
        #start, end = map(int, id_range.split("-"))

def is_invalid_id(n: int) -> bool:
    s = str(n)
    length = len(s)
    if length % 2 != 0:
        return False
    half = length // 2
    return s[:half] == s[half:]

total_invalid_sum = 0
for id_range in ids:
    for id in range(int(id_range[0]), int(id_range[1]) + 1):
        if is_invalid_id(id):
            total_invalid_sum += id

# What is the sum of all invalid IDs that appear in the given ranges?
print(f"Sum of all invalid IDs: {total_invalid_sum}")


