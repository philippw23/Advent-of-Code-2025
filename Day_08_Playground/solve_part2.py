from itertools import combinations
from math import sqrt
from pathlib import Path


def read_coords(path: Path):
    coords = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                coords.append(tuple(map(int, line.strip().split(","))))
    return coords


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


def main():
    base = Path(__file__).parent
    coords = read_coords(base / "test.txt")

    edges = []
    for (i, a), (j, b) in combinations(enumerate(coords), 2):
        dist = sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
        edges.append((dist, i, j))

    edges.sort(key=lambda x: x[0])

    uf = UnionFind(len(coords))
    last_edge = None
    for dist, i, j in edges:
        merged = uf.union(i, j)
        if merged:
            last_edge = (i, j)
            if uf.components == 1:
                break

    if last_edge is None:
        raise RuntimeError("No edge created a single circuit")

    x_product = coords[last_edge[0]][0] * coords[last_edge[1]][0]
    print(f"Last connection between {coords[last_edge[0]]} and {coords[last_edge[1]]}")
    print(f"X product: {x_product}")


if __name__ == "__main__":
    main()
