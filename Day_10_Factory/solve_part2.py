import re
from fractions import Fraction
from pathlib import Path


def parse_line(line: str):
    """Return target vector and button index lists."""
    target_match = re.search(r"\{([^}]*)\}", line)
    if not target_match:
        raise ValueError("No target found")
    targets = [int(x.strip()) for x in target_match.group(1).split(",") if x.strip()]
    counters = len(targets)

    buttons = []
    for group in re.findall(r"\(([^)]*)\)", line):
        values = [val.strip() for val in group.split(",") if val.strip()]
        if not values:
            buttons.append([])
            continue
        buttons.append([int(x) for x in values])

    return counters, targets, buttons


def independent_row_indices(matrix):
    """Return indices of linearly independent rows."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    frac_matrix = [[Fraction(val) for val in row] for row in matrix]
    row_order = list(range(rows))
    pivots = []
    current = 0

    for col in range(cols):
        pivot = None
        for r in range(current, rows):
            if frac_matrix[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        frac_matrix[current], frac_matrix[pivot] = frac_matrix[pivot], frac_matrix[current]
        row_order[current], row_order[pivot] = row_order[pivot], row_order[current]
        pivot_val = frac_matrix[current][col]
        for c in range(col, cols):
            frac_matrix[current][c] /= pivot_val
        for r in range(rows):
            if r != current and frac_matrix[r][col] != 0:
                factor = frac_matrix[r][col]
                for c in range(col, cols):
                    frac_matrix[r][c] -= factor * frac_matrix[current][c]
        pivots.append(row_order[current])
        current += 1
        if current == rows:
            break

    pivots.sort()
    return pivots


def pivot_columns(matrix, column_order):
    """Return column indices forming a basis for the rows in matrix."""
    row_count = len(matrix)
    if row_count == 0:
        return []
    cols = len(column_order)
    frac_matrix = [[Fraction(matrix[r][column_order[c]]) for c in range(cols)] for r in range(row_count)]
    basis = []
    current = 0

    for idx, col in enumerate(column_order):
        pivot = None
        for r in range(current, row_count):
            if frac_matrix[r][idx] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        frac_matrix[current], frac_matrix[pivot] = frac_matrix[pivot], frac_matrix[current]
        pivot_val = frac_matrix[current][idx]
        for c in range(idx, cols):
            frac_matrix[current][c] /= pivot_val
        for r in range(row_count):
            if r != current and frac_matrix[r][idx] != 0:
                factor = frac_matrix[r][idx]
                for c in range(idx, cols):
                    frac_matrix[r][c] -= factor * frac_matrix[current][c]
        basis.append(col)
        current += 1
        if current == row_count:
            break
    return basis


def invert_square_matrix(matrix):
    """Return the inverse of a square matrix using Fraction arithmetic."""
    size = len(matrix)
    if size == 0:
        return []
    frac_matrix = [[Fraction(matrix[r][c]) for c in range(size)] for r in range(size)]
    identity = [[Fraction(int(r == c)) for c in range(size)] for r in range(size)]

    for col in range(size):
        pivot = None
        for row in range(col, size):
            if frac_matrix[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return None
        frac_matrix[col], frac_matrix[pivot] = frac_matrix[pivot], frac_matrix[col]
        identity[col], identity[pivot] = identity[pivot], identity[col]
        pivot_val = frac_matrix[col][col]
        for j in range(size):
            frac_matrix[col][j] /= pivot_val
            identity[col][j] /= pivot_val
        for row in range(size):
            if row != col and frac_matrix[row][col] != 0:
                factor = frac_matrix[row][col]
                for j in range(size):
                    frac_matrix[row][j] -= factor * frac_matrix[col][j]
                    identity[row][j] -= factor * identity[col][j]
    return identity


def solve_with_basis(inv_matrix, rhs):
    """Use a precomputed inverse to solve for the basis variables."""
    if not inv_matrix:
        return []
    size = len(inv_matrix)
    vec = [Fraction(val) for val in rhs]
    solution = []
    for r in range(size):
        total = Fraction(0)
        for c in range(size):
            total += inv_matrix[r][c] * vec[c]
        solution.append(total)
    return solution


def min_presses(targets, buttons):
    counters = len(targets)
    if all(v == 0 for v in targets):
        return 0

    filtered_buttons = []
    for idxs in buttons:
        cleaned = sorted({i for i in idxs if 0 <= i < counters})
        if cleaned:
            filtered_buttons.append(cleaned)
    n = len(filtered_buttons)
    if n == 0:
        raise ValueError("No usable buttons to configure counters")

    coverage = [0] * counters
    for idxs in filtered_buttons:
        for idx in idxs:
            coverage[idx] += 1
    for idx, target in enumerate(targets):
        if target > 0 and coverage[idx] == 0:
            raise ValueError("Unreachable counter requirement")

    # Build full coefficient matrix
    full_matrix = [[0] * n for _ in range(counters)]
    for col, idxs in enumerate(filtered_buttons):
        for row in idxs:
            full_matrix[row][col] = 1

    row_indices = independent_row_indices(full_matrix)
    if not row_indices:
        return 0
    reduced_matrix = [full_matrix[row][:] for row in row_indices]
    reduced_targets = [targets[row] for row in row_indices]

    column_order = sorted(range(n), key=lambda idx: (len(filtered_buttons[idx]), idx))
    basis_cols = pivot_columns(reduced_matrix, column_order)
    if len(basis_cols) != len(reduced_matrix):
        raise ValueError("Insufficient independent buttons for constraints")
    basis_set = set(basis_cols)
    free_cols = [idx for idx in range(n) if idx not in basis_set]

    # Heuristic ordering for free variables
    def free_limit(col):
        return min((targets[i] for i in filtered_buttons[col]), default=0)

    free_cols.sort(key=lambda idx: (free_limit(idx), len(filtered_buttons[idx]), idx))

    basis_matrix = [[reduced_matrix[r][col] for col in basis_cols] for r in range(len(reduced_matrix))]
    basis_inverse = invert_square_matrix(basis_matrix)
    if basis_inverse is None:
        raise ValueError("Basis matrix is singular")

    row_positions = {row: pos for pos, row in enumerate(row_indices)}
    reduced_supports = {
        col: [row_positions[row] for row in filtered_buttons[col] if row in row_positions]
        for col in range(n)
    }

    total_targets = sum(targets)
    free_lengths = [len(filtered_buttons[col]) for col in free_cols]
    suffix_max = [0] * (len(free_cols) + 1)
    for i in range(len(free_cols) - 1, -1, -1):
        suffix_max[i] = max(free_lengths[i], suffix_max[i + 1])
    basis_max_len = max((len(filtered_buttons[col]) for col in basis_cols), default=0)

    def verify_solution(counts):
        for row in range(counters):
            total = 0
            row_entries = full_matrix[row]
            for col, presses in enumerate(counts):
                if presses and row_entries[col]:
                    total += presses
            if total != targets[row]:
                return False
        return True

    if not free_cols:
        rhs = reduced_targets[:]
        base_solution = solve_with_basis(basis_inverse, rhs)
        base_counts = []
        for val in base_solution:
            if val.denominator != 1 or val < 0:
                raise ValueError("No integer solution for constraints")
            base_counts.append(int(val))
        counts = [0] * n
        for pos, col in enumerate(basis_cols):
            counts[col] = base_counts[pos]
        if not verify_solution(counts):
            raise ValueError("Computed solution fails verification")
        return sum(base_counts)

    partial_full = [0] * counters
    partial_reduced = [0] * len(reduced_matrix)
    delivered_sum = 0
    free_values = [0] * len(free_cols)
    best = [float("inf")]

    def dfs(idx, press_sum):
        nonlocal delivered_sum
        if press_sum >= best[0]:
            return
        remaining = total_targets - delivered_sum
        max_len_available = max(basis_max_len, suffix_max[idx])
        if max_len_available == 0:
            max_len_available = 1
        lower_bound = (remaining + max_len_available - 1) // max_len_available
        if press_sum + lower_bound >= best[0]:
            return

        if idx == len(free_cols):
            rhs = [reduced_targets[i] - partial_reduced[i] for i in range(len(reduced_matrix))]
            if any(val < 0 for val in rhs):
                return
            base_solution = solve_with_basis(basis_inverse, rhs)
            base_counts = []
            for val in base_solution:
                if val.denominator != 1 or val < 0:
                    return
                base_counts.append(int(val))
            total_presses = press_sum + sum(base_counts)
            if total_presses >= best[0]:
                return
            counts = [0] * n
            for pos, col in enumerate(free_cols):
                counts[col] = free_values[pos]
            for pos, col in enumerate(basis_cols):
                counts[col] = base_counts[pos]
            if verify_solution(counts):
                best[0] = total_presses
            return

        col = free_cols[idx]
        support = filtered_buttons[col]
        if not support:
            free_values[idx] = 0
            dfs(idx + 1, press_sum)
            return
        reduced_rows = reduced_supports[col]
        limit = min(targets[row] - partial_full[row] for row in support)
        if limit < 0:
            return

        prev = 0
        support_size = len(support)
        for cnt in range(limit + 1):
            if press_sum + cnt >= best[0]:
                break
            delta = cnt - prev
            if delta:
                for row in support:
                    partial_full[row] += delta
                for pos in reduced_rows:
                    partial_reduced[pos] += delta
                delivered_sum += delta * support_size
            free_values[idx] = cnt
            dfs(idx + 1, press_sum + cnt)
            prev = cnt

        if prev:
            delta = -prev
            for row in support:
                partial_full[row] += delta
            for pos in reduced_rows:
                partial_reduced[pos] += delta
            delivered_sum += delta * support_size
        free_values[idx] = 0

    dfs(0, 0)
    if best[0] == float("inf"):
        raise ValueError("No configuration satisfies the constraints")
    return best[0]


def solve(lines):
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        _, targets, buttons = parse_line(line)
        total += min_presses(targets, buttons)
    return total


def main():
    input_path = Path(__file__).with_name("input.txt")
    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    print(solve(lines))


if __name__ == "__main__":
    main()
