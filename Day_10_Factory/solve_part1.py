import re


def parse_line(line: str):
    pattern_match = re.search(r"\[([.#]+)\]", line)
    if not pattern_match:
        raise ValueError("No indicator pattern found")
    pattern = pattern_match.group(1)
    lights = len(pattern)
    target = 0
    for idx, ch in enumerate(pattern):
        if ch == "#":
            target |= 1 << idx

    button_masks = []
    for group in re.findall(r"\(([^)]*)\)", line):
        if group.strip() == "":
            button_masks.append(0)
            continue
        mask = 0
        for val in group.split(","):
            pos = int(val)
            mask |= 1 << pos
        button_masks.append(mask)

    return lights, target, button_masks


def min_presses(target: int, button_masks):
    n = len(button_masks)
    total_states = 1 << n
    combined = [0] * total_states
    print(total_states)
    best = None

    for state in range(1, total_states):
        lsb = state & -state
        idx = lsb.bit_length() - 1
        prev = state ^ lsb
        combined[state] = combined[prev] ^ button_masks[idx]

    for state, mask in enumerate(combined):
        if mask == target:
            presses = state.bit_count()
            if best is None or presses < best:
                best = presses
    if best is None:
        raise ValueError("No solution found")
    return best


def solve(lines):
    total = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        _, target, masks = parse_line(line)
        total += min_presses(target, masks)
    return total


def main():
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()
    print(2<<3)