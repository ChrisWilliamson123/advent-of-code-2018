import itertools, operator
from heapq import *

REMOVED = '<removed-task>'

class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def add_task(self, task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = REMOVED

    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')

def complete(destination_nodes, visited_nodes):
    for n in destination_nodes:
        if n not in visited_nodes:
            return False
    return True

def dijkstra_p_queue(edges, nodes, origin, destination):
    visited_nodes = set()
    unvisited_nodes = nodes | {origin}
    distances = {n: float('inf') for n in unvisited_nodes}
    distances[origin] = 0
    pri_queue = PriorityQueue()

    # Build the queue
    for n in unvisited_nodes:
        pri_queue.add_task(n, distances[n])
    
    while len(pri_queue.pq) > 0:
        # print(len(pri_queue.pq))
        try:
            u = pri_queue.pop_task()
        except:
            break
        for neighbour in edges[u]:
            v = neighbour[0]
            length = neighbour[1]
            alt = distances[u] + length
            if alt < distances[v]:
                distances[v] = alt
                pri_queue.add_task(v, alt)
        print('here')

    return distances


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