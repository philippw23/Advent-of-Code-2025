grid = []
with(open(("input.txt"), "r", encoding="utf-8")) as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue
        sub_grid = []
        for element in line:
            sub_grid.append(element)
        grid.append(sub_grid)

new_grid = [row.copy() for row in grid]
height = len(grid)
width = len(grid[0])

def fewer_than_four_adjacent_paper_rolls(x, y):
    adjacent_trees = 0
    # Check all eight directions around (x, y).
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the tree itself.
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx] == '@':
                    adjacent_trees += 1
    return adjacent_trees < 4

x_counter = 0

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == '@':
            if fewer_than_four_adjacent_paper_rolls(j, i):
                new_grid[i][j] = 'x'
                x_counter += 1

def print_grid(grid):
    for row in grid:
        print("".join(row))

print_grid(new_grid)
print(f"Total exposed paper rolls: {x_counter}")