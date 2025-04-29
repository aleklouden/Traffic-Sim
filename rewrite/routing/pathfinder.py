import heapq

def dijkstra(map, start, end):
    """
    Dijkstra's algorithm to find the shortest path from start to end, with roads and turn directions.

    Inputs:
        map: The graph object with roads and nodes
        start: Starting node
        end: Destination node

    Output:
        A list of roads representing the shortest path from start to end along with turn directions
    """
    graph = map.graph
    distances = {vertex: float('inf') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    previous_roads = {vertex: None for vertex in graph}  # Keep track of the road leading to each vertex
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, road in graph[current_vertex].items():
            distance = current_distance + road.length
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                previous_roads[neighbor] = road  # Track the road that leads to 'neighbor'
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path from end to start, including roads
    route = []
    current_vertex = end

    if previous_vertices[current_vertex] is None and start != end:
        return []  # No path exists

    while current_vertex is not None:
        route.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    route.reverse()

    # Now that we have the route, let's get the roads and turn directions
    route_with_roads_and_turns = []
    for i in range(len(route) - 1):
        from_vertex = route[i]
        to_vertex = route[i + 1]
        
        # Get the road connecting from_vertex to to_vertex
        road1 = previous_roads[to_vertex]  # The road that led to 'to_vertex'
        if i + 2 < len(route):  # Check if there's a next road
            road2 = graph[to_vertex].get(route[i + 2])  # The road from 'to_vertex' to the next vertex
        else:
            road2 = None  # No next road, this is the last road segment

        # Get the turn direction
        if road2:
            turn_direction = map.get_turn_direction(road1, road2)
        else:
            turn_direction = "none"  # No turn direction for the last road

        # Append the road with turn direction
        route_with_roads_and_turns.append((road1, turn_direction))

    return route_with_roads_and_turns
