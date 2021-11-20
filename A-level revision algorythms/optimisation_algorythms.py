def dfs(graph, vertex): #depth-first traversal iterative version
    path = [vertex]
    visited = [vertex]
    while path != []:
        vertex = path[-1]
        found = False
        neighbours = graph[vertex]
        index = 0
        while not found and index<len(neighbours):
            if not neighbours[index] in visited:
                found = True
                vertex = neighbours[index] #move to next vertex
                path.append(vertex) #add it to path
                visited.append(vertex) #mark it as visited
            index += 1
        if not found:
            path.pop()
    return visited

def bfs(graph, vertex): #breadth-first trversal iterative version
    to_visit = graph[vertex]
    visited = [vertex]
    while to_visit != []:
        vertex = to_visit.pop(0)
        visited.append(vertex)
        for neighbour in graph[vertex]:
            if not neighbour in visited and not neighbour in to_visit:
                to_visit.append(neighbour)
    return visited

graph = {"A": ["B", "D", "E"], "B": ["A", "C", "D"], "C": ["B", "G"], 
        "D": ["A", "B", "E", "F"], "E": ["A", "D", "F"], "F": ["D"], "G": ["C"]}

print(dfs(graph, "A"))
print(bfs(graph, "A"))

