
with open("input.txt", "r", encoding="utf-8") as f:
    tiles = []
    for line in f:
        tile = list(map(int, line.strip().split(",")))
        tiles.append(tile)
best_area = 0
best_tiles = None
for key in range(len(tiles)):
    for other_key in range(len(tiles)):
        if key < other_key:
            a = tiles[key]
            b = tiles[other_key]
            row_1, col_1 = a[0], a[1]
            row_2, col_2 = b[0], b[1]

            area = (abs(row_1 - row_2)+1) * (abs(col_1 - col_2)+1)
            if area > best_area:
                best_area = area
                best_tiles = (a, b)

print(f"Best area: {best_area} from tiles {best_tiles}")