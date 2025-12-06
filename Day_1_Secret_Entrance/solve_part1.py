
moves = []
position = 50
zero_hits = 0

with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        movement = line.strip()
        if not movement:
            continue
        distance = int(movement[1:])
        moves.append(distance if movement[0] == "R" else -distance)

for delta in moves:
    position = (position + delta) % 100
    if position == 0:
        zero_hits += 1
    
print(f"Final position: {position}")
print(f"Password (times at 0): {zero_hits}")