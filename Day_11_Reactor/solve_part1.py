machine_id = []
output = []
with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        id = line.strip().split(":")[0]
        out = line.strip().split(":")[1].split(" ")
        machine_id.append(id)
        output.append(out[1:])

start = [key for key in range(len(machine_id)) if machine_id[key] == "you"][0]

# adjacency map keyed by machine name (handles missing nodes like "out")
graph = {machine_id[idx]: output[idx] for idx in range(len(machine_id))}
start_name = machine_id[start]
TARGET = "out"

cache = {}
active = set()


def count_paths(node):
    if node == TARGET:
        return 1
    if node in cache:
        return cache[node]
    if node in active:
        raise ValueError(f"Cycle detected involving {node}")
    active.add(node)
    total = 0
    for neighbor in graph.get(node, []):
        total += count_paths(neighbor)
    active.remove(node)
    cache[node] = total
    return total


paths = count_paths(start_name)
print(paths)
