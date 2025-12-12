# Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those big rolls of paper around."

# If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

# The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.

from collections import deque

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

h, w = len(grid), len(grid[0])
dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def inside(y, x): return 0 <= y < h and 0 <= x < w

# Precompute adjacency counts
adj = [[0]*w for _ in range(h)]
for y in range(h):
    for x in range(w):
        if grid[y][x] != '@': continue
        for dy, dx in dirs:
            ny, nx = y+dy, x+dx
            if inside(ny, nx):
                adj[ny][nx] += 1

def try_mark(y, x, q):
    if grid[y][x] == '@' and adj[y][x] < 4:
        grid[y][x] = 'x'
        # @ got removed -> adjacent count down, check neighbors
        for dy, dx in dirs:
            ny, nx = y+dy, x+dx
            if inside(ny, nx):
                adj[ny][nx] -= 1
                if grid[ny][nx] == '@' and adj[ny][nx] < 4:
                    q.append((ny, nx))
        return True
    return False

q = deque()

# starting candidates: all currently exposed rolls
for y in range(h):
    for x in range(w):
        if grid[y][x] == '@' and adj[y][x] < 4:
            q.append((y, x))

x_counter = 0
while q:
    y, x = q.popleft()
    if try_mark(y, x, q):
        x_counter += 1

# Ausgabe wie gehabt

def print_grid(grid):
    for row in grid:
        print("".join(row))

print_grid(grid)
print(f"Total exposed paper rolls: {x_counter}")
