import operator

def complete(destination_nodes, visited_nodes):
    for n in destination_nodes:
        if n not in visited_nodes:
            return False
    return True

def dijkstra_multiple(edges, nodes, origin_node, destination_nodes):
    visited_nodes = set()
    unvisited_nodes = nodes | {origin_node}
    distances = {n: float('inf') for n in unvisited_nodes}
    distances[origin_node] = 0

    current_node = origin_node

    while not complete(destination_nodes, visited_nodes):
        neighbours = edges[current_node]
        unvisited_neighbours = [n for n in neighbours if n[0] in unvisited_nodes]

        for n in unvisited_neighbours:
            neighbour_coordinate = n[0]
            current_distance_to_neighbour = distances[neighbour_coordinate]
            new_distance = distances[current_node] + n[1]
            if new_distance < current_distance_to_neighbour:
                distances[neighbour_coordinate] = new_distance
        
        visited_nodes.add(current_node)
        unvisited_nodes.remove(current_node)

        if not unvisited_nodes:
            break

        unvisited_node_distances = {n: distances[n] for n in unvisited_nodes}
        unvisited_node_with_shortest_distance = min(unvisited_node_distances.items(), key=operator.itemgetter(1))[0]
        current_node = unvisited_node_with_shortest_distance
    return {key: value for (key, value) in distances.items() if key in destination_nodes}

def dijkstra(edges, nodes, origin_node, destination_node):
    visited_nodes = set()
    unvisited_nodes = nodes | {origin_node}
    distances = {n: float('inf') for n in unvisited_nodes}
    distances[origin_node] = 0

    current_node = origin_node

    while destination_node not in visited_nodes:
        neighbours = edges[current_node]
        unvisited_neighbours = [n for n in neighbours if n[0] in unvisited_nodes]

        for n in unvisited_neighbours:
            neighbour_coordinate = n[0]
            current_distance_to_neighbour = distances[neighbour_coordinate]
            new_distance = distances[current_node] + n[1]
            if new_distance < current_distance_to_neighbour:
                distances[neighbour_coordinate] = new_distance
        
        visited_nodes.add(current_node)
        unvisited_nodes.remove(current_node)

        if not unvisited_nodes:
            break

        unvisited_node_distances = {n: distances[n] for n in unvisited_nodes}
        unvisited_node_with_shortest_distance = min(unvisited_node_distances.items(), key=operator.itemgetter(1))[0]
        current_node = unvisited_node_with_shortest_distance
    return distances[destination_node]