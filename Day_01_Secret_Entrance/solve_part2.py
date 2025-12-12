
import math

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
    if delta > 0:
        zero_hits += (position + delta) // 100
    elif delta < 0:
        zero_hits += math.ceil(position / 100) - math.ceil((position + delta) / 100) 
    position = (position + delta) % 100

    
print(f"Final position: {position}")
print(f"Password (times at 0): {zero_hits}")
