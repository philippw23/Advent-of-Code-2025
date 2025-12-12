import sys
from typing import Dict, Iterable, List, Sequence, Set, Tuple

sys.setrecursionlimit(50_000)

DEFAULT_INPUT = "input.txt"
START_NODE = "svr"
TARGET_NODE = "out"
REQUIRED_NODES: Tuple[str, ...] = ("dac", "fft")


def parse_graph(path: str) -> Dict[str, List[str]]:
    graph: Dict[str, List[str]] = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            node, _, rest = line.partition(":")
            graph[node.strip()] = rest.strip().split()
    return graph


def count_paths_with_requirements(
    graph: Dict[str, List[str]],
    start: str,
    target: str,
    required_nodes: Sequence[str],
) -> int:
    masks = {node: 1 << idx for idx, node in enumerate(required_nodes)}
    required_mask = (1 << len(required_nodes)) - 1
    memo: Dict[Tuple[str, int], int] = {}
    active: Set[Tuple[str, int]] = set()

    def dfs(node: str, mask: int) -> int:
        state = (node, mask)
        if state in memo:
            return memo[state]
        if state in active:
            raise ValueError(f"Cycle detected involving {node} with mask {mask}")

        active.add(state)
        next_mask = mask | masks.get(node, 0)
        if node == target:
            total = 1 if next_mask == required_mask else 0
        else:
            total = 0
            for neighbor in graph.get(node, []):
                total += dfs(neighbor, next_mask)
        active.remove(state)
        memo[state] = total
        return total

    return dfs(start, 0)


def main(args: Iterable[str]) -> None:
    arg_list = list(args)
    input_path = arg_list[0] if arg_list else DEFAULT_INPUT
    graph = parse_graph(input_path)

    total_paths = count_paths_with_requirements(
        graph, START_NODE, TARGET_NODE, ()
    )
    required_paths = count_paths_with_requirements(
        graph, START_NODE, TARGET_NODE, REQUIRED_NODES
    )

    print(f"Total paths from {START_NODE} to {TARGET_NODE}: {total_paths}")
    nodes = ", ".join(REQUIRED_NODES)
    print(f"Paths visiting {nodes}: {required_paths}")


if __name__ == "__main__":
    main(sys.argv[1:])
