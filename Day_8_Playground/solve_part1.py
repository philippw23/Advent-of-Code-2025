coordinates = []
with open("input.txt", "r", encoding="utf-8") as f:
    for line in f:
        coord = list(map(int, line.strip().split(",")))
        coordinates.append(coord)


def euclidean_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5

distances = {}
for key, element in enumerate(coordinates):
    for other_key, other_element in enumerate(coordinates):
        if key < other_key:
            dist = euclidean_distance(element, other_element)
            #distances.setdefault(dist,[]).append([element, other_element])
            distances[dist] = [key, other_key]

# Sorting distances
distances = dict(sorted(distances.items()))

# Initialize circuits and adding first two coordinates keys
circuits = []
first_item = next(iter(distances))
first_values = distances.pop(first_item)
circuits.append(first_values)



for _ in range(1000-1):
    if not distances:
        break

    dist, value = next(iter(distances.items()))
    distances.pop(dist)
    a, b = value

    idx_a = idx_b = None
    for idx, circuit in enumerate(circuits):
        if a in circuit:
            idx_a = idx
        if b in circuit:
            idx_b = idx

    if idx_a is None and idx_b is None:
        circuits.append([a, b])
    elif idx_a is not None and idx_b is None:
        if b not in circuits[idx_a]:
            circuits[idx_a].append(b)
    elif idx_a is None and idx_b is not None:
        if a not in circuits[idx_b]:
            circuits[idx_b].append(a)
    else:
        if idx_a != idx_b:
            circuits[idx_a].extend([v for v in circuits[idx_b] if v not in circuits[idx_a]])
            circuits.pop(idx_b)

circuits.sort(key=len, reverse=True)

res = []
for curcuit in circuits[:3]:
    res.append(len(curcuit))

print(res[0]*res[1]*res[2])
#print(f"Circuits: {circuits}")

