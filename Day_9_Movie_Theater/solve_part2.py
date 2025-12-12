from __future__ import annotations

from collections import deque
from itertools import combinations
from pathlib import Path
import sys


def read_coords(path: Path):
    coords = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(","))
                coords.append((x, y))
    if not coords:
        raise ValueError("No coordinates found")
    return coords


def build_compression(coords):
    xs = set()
    ys = set()
    all_x = [x for x, _ in coords]
    all_y = [y for _, y in coords]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # include buffer outside the loop so flood fill can reach "outside"
    xs.update({min_x - 1, max_x + 2})
    ys.update({min_y - 1, max_y + 2})

    for x, y in coords:
        xs.add(x)
        xs.add(x + 1)
        ys.add(y)
        ys.add(y + 1)

    xs = sorted(xs)
    ys = sorted(ys)
    x_index = {val: idx for idx, val in enumerate(xs)}
    y_index = {val: idx for idx, val in enumerate(ys)}
    widths = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    heights = [ys[i + 1] - ys[i] for i in range(len(ys) - 1)]

    return xs, ys, x_index, y_index, widths, heights


def mark_boundary(coords, x_index, y_index, grid):
    rows = len(grid)
    cols = len(grid[0])
    assert rows and cols

    for (x1, y1), (x2, y2) in zip(coords, coords[1:] + coords[:1]):
        if x1 == x2:
            x_idx = x_index[x1]
            x_next = x_index[x1 + 1]
            y_start = min(y1, y2)
            y_end = max(y1, y2) + 1
            r0 = y_index[y_start]
            r1 = y_index[y_end]
            for r in range(r0, r1):
                for c in range(x_idx, x_next):
                    grid[r][c] = True
        elif y1 == y2:
            y_idx = y_index[y1]
            y_next = y_index[y1 + 1]
            x_start = min(x1, x2)
            x_end = max(x1, x2) + 1
            c0 = x_index[x_start]
            c1 = x_index[x_end]
            for r in range(y_idx, y_next):
                for c in range(c0, c1):
                    grid[r][c] = True
        else:
            raise ValueError("Adjacent tiles are not aligned")


def flood_fill_outside(boundary):
    rows = len(boundary)
    cols = len(boundary[0])
    outside = [[False] * cols for _ in range(rows)]
    dq = deque()

    def enqueue(r, c):
        if 0 <= r < rows and 0 <= c < cols:
            if not boundary[r][c] and not outside[r][c]:
                outside[r][c] = True
                dq.append((r, c))

    for r in range(rows):
        enqueue(r, 0)
        enqueue(r, cols - 1)
    for c in range(cols):
        enqueue(0, c)
        enqueue(rows - 1, c)

    while dq:
        r, c = dq.popleft()
        enqueue(r - 1, c)
        enqueue(r + 1, c)
        enqueue(r, c - 1)
        enqueue(r, c + 1)

    return outside


def build_allowed_area(boundary, widths, heights):
    outside = flood_fill_outside(boundary)
    rows = len(boundary)
    cols = len(boundary[0])
    allowed = [[not outside[r][c] for c in range(cols)] for r in range(rows)]

    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            cell_area = widths[c] * heights[r] if allowed[r][c] else 0
            prefix[r + 1][c + 1] = (
                prefix[r][c + 1]
                + prefix[r + 1][c]
                - prefix[r][c]
                + cell_area
            )
    return prefix


def query(pref, x0, x1, y0, y1):
    return pref[y1][x1] - pref[y0][x1] - pref[y1][x0] + pref[y0][x0]


def max_rectangle_area(coords):
    xs, ys, x_index, y_index, widths, heights = build_compression(coords)
    rows = len(ys) - 1
    cols = len(xs) - 1
    boundary = [[False] * cols for _ in range(rows)]
    mark_boundary(coords, x_index, y_index, boundary)

    prefix = build_allowed_area(boundary, widths, heights)
    best = 0
    for (x1, y1), (x2, y2) in combinations(coords, 2):
        x_lo = min(x1, x2)
        x_hi = max(x1, x2) + 1
        y_lo = min(y1, y2)
        y_hi = max(y1, y2) + 1
        area_total = (x_hi - x_lo) * (y_hi - y_lo)
        if area_total <= best:
            continue
        xi0 = x_index[x_lo]
        xi1 = x_index[x_hi]
        yi0 = y_index[y_lo]
        yi1 = y_index[y_hi]
        allowed_area = query(prefix, xi0, xi1, yi0, yi1)
        if allowed_area == area_total:
            best = area_total
    return best


def main():
    fn = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    coords = read_coords(Path(__file__).parent / fn)
    area = max_rectangle_area(coords)
    print(area)


if __name__ == "__main__":
    main()
