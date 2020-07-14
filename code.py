def allowed(adj, color, result):
    for x in adj:
        if result[x] == color:
            return False
    return True

def coloring(graph, vertex, colors, result, flag, solutions):
    if vertex >= len(graph):
        print(result)
        if flag and solutions == 1:
            flag = True
        else:
            flag = False
        return
    for i in range(len(colors)):
        if allowed(graph[vertex], colors[i], result):
            result[vertex] = colors[i]
            coloring(graph, vertex + 1, colors, result, flag, solutions)
            if flag == False:
                return
            result[vertex] = ""
            
graph = list()
n = int(input("\nEnter the number of vertices in the undirected graph: "))
e = int(input("\nEnter the number of edges present in the undirected graph: "))
solutions = int(input("\nDo you want all solutions ? [Press: 1 for Yes and 0 for No]: "))
for i in range(n):
    graph.append(list())
for i in range(e):
    print("\nEdge", i, ">> ", end = "")
    a = [int(x) for x in input().split(" ")]
    graph[a[0]].append(a[1])
    graph[a[1]].append(a[0])
nc = int(input("\nEnter the number of colors for coloring the undriected graph: "))
colors = list()
for i in range(nc):
    cs = "C-" + str(i + 1) 
    colors.append(cs)
result = [str("") for i in range(n)]
if solutions == 1:
    flag = True
else:
    flag = False
print("")
coloring(graph, 0, colors, result, flag, solutions)
print("")