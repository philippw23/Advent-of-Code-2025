from pathlib import Path


def read_grid(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f.read().splitlines()]


def count_paths(grid):
    rows, cols = len(grid), len(grid[0])
    start_col = grid[0].index("S")

    active = {start_col: 1}
    for row in range(rows - 1):
        next_counts = {}
        for col, count in active.items():
            target = grid[row + 1][col]
            if target == "^":
                for new_col in (col - 1, col + 1):
                    if 0 <= new_col < cols:
                        next_counts[new_col] = next_counts.get(new_col, 0) + count
            else:
                next_counts[col] = next_counts.get(col, 0) + count
        active = next_counts

    return sum(active.values())


base = Path(__file__).parent
grid = read_grid(base / "input.txt")
path_count = count_paths(grid)
print(f"Anzahl Paths: {path_count}")
