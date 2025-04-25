import heapq

def dijkstra(graph, start, end):
    """
    Inputs:
        graph: a dictionary {node: {neighbor: weight, ...}, ...}
        start: starting node
        end: destination node

    Output:
        A list of nodes representing the shortest path from start to end
    """

    distances = {vertex: float('inf') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path from end to start
    route = []
    current_vertex = end

    if previous_vertices[current_vertex] is None and start != end:
        return []  # No path exists

    while current_vertex is not None:
        route.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    route.reverse()
    return route
