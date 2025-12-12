from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def parse_input(data: str) -> Tuple[List[List[str]], List[Tuple[int, int, List[int]]]]:
    parts = [block.strip() for block in data.strip().split("\n\n") if block.strip()]
    shape_blocks: List[str] = []
    region_lines: List[str] = []
    for block in parts:
        first_line = block.splitlines()[0]
        if first_line.endswith(":") and "x" not in first_line:
            shape_blocks.append(block)
        else:
            region_lines.extend(block.splitlines())

    shapes: Dict[int, List[str]] = {}
    for block in shape_blocks:
        lines = block.splitlines()
        idx = int(lines[0][:-1])
        shapes[idx] = lines[1:]

    if not shapes:
        raise ValueError("No shapes parsed from the input")

    # Sort shapes by their numeric id to align with the counts listed per region.
    ordered_shape_ids = sorted(shapes)
    shape_rows = [trim_shape(shapes[idx]) for idx in ordered_shape_ids]

    regions: List[Tuple[int, int, List[int]]] = []
    for line in region_lines:
        if not line.strip():
            continue
        dims, counts_str = line.split(":")
        w, h = map(int, dims.split("x"))
        counts = list(map(int, counts_str.strip().split()))
        regions.append((w, h, counts))

    return shape_rows, regions


def trim_shape(rows: Sequence[str]) -> List[str]:
    if not rows:
        return []
    width = max(len(row) for row in rows)
    padded = [row.ljust(width, ".") for row in rows]

    top = 0
    while top < len(padded) and set(padded[top]) == {"."}:
        top += 1
    bottom = len(padded) - 1
    while bottom >= 0 and set(padded[bottom]) == {"."}:
        bottom -= 1

    left = 0
    while left < width and all(row[left] == "." for row in padded):
        left += 1
    right = width - 1
    while right >= 0 and all(row[right] == "." for row in padded):
        right -= 1

    return [row[left : right + 1] for row in padded[top : bottom + 1]]


def rotate(mat: Sequence[str]) -> List[str]:
    h, w = len(mat), len(mat[0])
    return ["".join(mat[h - 1 - r][c] for r in range(h)) for c in range(w)]


def flip(mat: Sequence[str]) -> List[str]:
    return [row[::-1] for row in mat]


def generate_variants(shape_rows: List[List[str]]) -> Tuple[List[List[Tuple[List[Tuple[int, int]], int, int]]], List[int]]:
    variant_cells: List[List[Tuple[List[Tuple[int, int]], int, int]]] = []
    areas: List[int] = []
    for rows in shape_rows:
        areas.append(sum(row.count("#") for row in rows))
        mats: List[List[str]] = [rows]
        for _ in range(3):
            mats.append(rotate(mats[-1]))
        mats = mats[:4]
        mats += [flip(mat) for mat in mats]

        seen: set[Tuple[str, ...]] = set()
        cells_for_shape: List[Tuple[List[Tuple[int, int]], int, int]] = []
        for mat in mats:
            key = tuple(mat)
            if key in seen:
                continue
            seen.add(key)
            coords = [(x, y) for y, row in enumerate(mat) for x, ch in enumerate(row) if ch == "#"]
            if not coords:
                continue
            width = len(mat[0])
            height = len(mat)
            cells_for_shape.append((coords, width, height))
        variant_cells.append(cells_for_shape)
    return variant_cells, areas


@dataclass
class PlacementCache:
    variant_cells: List[List[Tuple[List[Tuple[int, int]], int, int]]]

    def __post_init__(self) -> None:
        self._cache: Dict[Tuple[int, int], List[List[int]]] = {}

    def get(self, w: int, h: int) -> List[List[int]]:
        key = (w, h)
        if key in self._cache:
            return self._cache[key]

        placements: List[List[int]] = []
        for variants in self.variant_cells:
            masks: List[int] = []
            for cells, width, height in variants:
                if width > w or height > h:
                    continue
                max_y = h - height + 1
                max_x = w - width + 1
                for y in range(max_y):
                    row_offset = y * w
                    for x in range(max_x):
                        base_index = row_offset + x
                        mask = 0
                        for dx, dy in cells:
                            mask |= 1 << ((y + dy) * w + (x + dx))
                        masks.append(mask)
            masks.sort()
            placements.append(masks)
        self._cache[key] = placements
        return placements


def greedy_fit(counts: Sequence[int], placements: Sequence[Sequence[int]], orders: Sequence[Sequence[int]]) -> bool:
    for order in orders:
        board = 0
        success = True
        for t in order:
            need = counts[t]
            if need == 0:
                continue
            masks = placements[t]
            if len(masks) < need:
                success = False
                break
            placed = 0
            for mask in masks:
                if mask & board:
                    continue
                board |= mask
                placed += 1
                if placed == need:
                    break
            if placed < need:
                success = False
                break
        if success:
            return True
    return False


def backtrack(
    counts: Tuple[int, ...],
    used_mask: int,
    placements: Sequence[Sequence[int]],
    areas: Sequence[int],
    total_cells: int,
    memo: Dict[Tuple[Tuple[int, ...], int], bool] | None,
) -> bool:
    if all(c == 0 for c in counts):
        return True
    if memo is not None:
        key = (counts, used_mask)
        if key in memo:
            return False

    remaining_cells = total_cells - used_mask.bit_count()
    required_area = sum(counts[i] * areas[i] for i in range(len(counts)))
    if required_area > remaining_cells:
        if memo is not None:
            memo[(counts, used_mask)] = False
        return False

    best_type = None
    best_options: List[int] | None = None
    min_options = float("inf")
    for t, need in enumerate(counts):
        if need == 0:
            continue
        options: List[int] = []
        for mask in placements[t]:
            if mask & used_mask:
                continue
            options.append(mask)
        if len(options) < need:
            if memo is not None:
                memo[(counts, used_mask)] = False
            return False
        if len(options) < min_options:
            best_type = t
            best_options = options
            min_options = len(options)
            if len(options) == need:
                break

    assert best_type is not None and best_options is not None
    counts_list = list(counts)
    counts_list[best_type] -= 1
    next_counts = tuple(counts_list)
    for mask in best_options:
        if mask & used_mask:
            continue
        if backtrack(next_counts, used_mask | mask, placements, areas, total_cells, memo):
            return True
    if memo is not None:
        memo[(counts, used_mask)] = False
    return False


def count_fittable_regions(data: str) -> int:
    shape_rows, regions = parse_input(data)
    variant_cells, areas = generate_variants(shape_rows)
    placement_cache = PlacementCache(variant_cells)

    num_types = len(shape_rows)
    orders: List[List[int]] = []
    desc_order = sorted(range(num_types), key=lambda t: (-areas[t], t))
    orders.append(desc_order)
    orders.append(list(reversed(desc_order)))
    orders.append(list(range(num_types)))
    orders.append(list(reversed(range(num_types))))

    total = 0
    for w, h, counts in regions:
        if len(counts) < num_types:
            # The input always lists counts for every shape, but guard just in case.
            counts = counts + [0] * (num_types - len(counts))
        counts = counts[:num_types]

        required_area = sum(counts[i] * areas[i] for i in range(num_types))
        if required_area > w * h:
            continue

        placements = placement_cache.get(w, h)
        if any(counts[i] > len(placements[i]) for i in range(num_types)):
            continue

        if greedy_fit(counts, placements, orders):
            total += 1
            continue

        memo = {} if w * h <= 64 else None
        if backtrack(tuple(counts), 0, placements, areas, w * h, memo):
            total += 1

    return total


def main() -> None:
    input_path = Path(__file__).with_name("input.txt")
    data = input_path.read_text()
    result = count_fittable_regions(data)
    print(result)


if __name__ == "__main__":
    main()
