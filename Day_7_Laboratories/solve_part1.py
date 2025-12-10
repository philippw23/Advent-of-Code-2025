l = []
counter = 0
with open("input.txt", "r", encoding="utf-8") as f:
    lines = f.read().splitlines()
    for element in lines:
        sub_list = []
        for char in element:
            sub_list.append(char)
        l.append(sub_list)

length = len(l)
S_key = length//2-1

l[1][S_key] = "|"
#strokes = [[],[S_key]]
counter = 0
#print(strokes)

for key, line in enumerate(l[1:-1]):
    row = key + 1
    below = row + 1
    above = key
    sub_strokes = set()
    for index, char in enumerate(line):
        if char == "^":
            for col in (index-1, index+1):
                if 0 <= col < len(line):
                    #sub_strokes.add(col)
                    l[row][col] = "|"
                    l[below][col] = "|"
            if l[above][index] == "|":
                counter += 1
        if l[row][index] == "|" and l[below][index] != "^":
            #sub_strokes.add(index)
            l[below][index] = "|"
        
    #strokes.append(sub_strokes)

#print(strokes)
for el in l:
    print(el)

print(counter)