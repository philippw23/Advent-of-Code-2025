# Now, an ID is invalid if it is made only of some sequence of digits repeated at least twice. So, 12341234 (1234 two times), 123123123 (123 three times), 1212121212 (12 five times), and 1111111 (1 seven times) are all invalid IDs.

# From the same example as before:

# 11-22 still has two invalid IDs, 11 and 22.
# 95-115 now has two invalid IDs, 99 and 111.
# 998-1012 now has two invalid IDs, 999 and 1010.
# 1188511880-1188511890 still has one invalid ID, 1188511885.
# 222220-222224 still has one invalid ID, 222222.
# 1698522-1698528 still contains no invalid IDs.
# 446443-446449 still has one invalid ID, 446446.
# 38593856-38593862 still has one invalid ID, 38593859.
# 565653-565659 now has one invalid ID, 565656.
# 824824821-824824827 now has one invalid ID, 824824824.
# 2121212118-2121212124 now has one invalid ID, 2121212121.
# Adding up all the invalid IDs in this example produces 4174379265.

ids = []
with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read().strip()
    for element in text.split(","):
        id = element.split("-")
        ids.append(id)

def is_invalid_id(n: int) -> bool:
    s = str(n)
    length = len(s)
    for size in range(1, length // 2 + 1):
        if length % size == 0:
            if s[:size] * (length // size) == s:
                return True
    return False

total_invalid_sum = 0
for id_range in ids:
    for id in range(int(id_range[0]), int(id_range[1]) + 1):
        if is_invalid_id(id):
            total_invalid_sum += id

# What is the sum of all invalid IDs that appear in the given ranges?
print(f"Sum of all invalid IDs: {total_invalid_sum}")