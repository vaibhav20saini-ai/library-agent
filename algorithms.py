"""Graph search algorithms: BFS, DFS, and A*."""

from collections import deque
import heapq
import math


def available_graph(graph, closed_sections=None, restricted_shelves=None, crowded_aisles=None,
                    crowd_penalty=3):
    """Return a graph with blocked nodes removed and crowd penalties added to edge costs."""
    closed_sections = set(closed_sections or [])
    restricted_shelves = set(restricted_shelves or [])
    crowded_aisles = set(crowded_aisles or [])
    blocked = closed_sections | restricted_shelves
    result = {}
    for node, neighbours in graph.items():
        if node in blocked:
            continue
        result[node] = {}
        for neighbour, distance in neighbours.items():
            if neighbour in blocked:
                continue
            penalty = 0
            if node in crowded_aisles or neighbour in crowded_aisles:
                penalty = crowd_penalty
            result[node][neighbour] = distance + penalty
    return result


def bfs(graph, start, goal):
    """Breadth-first search. Returns a path and the search trace."""
    if start not in graph or goal not in graph:
        return None, [], []
    queue = deque([[start]])
    visited = {start}
    open_list = [start]
    closed_list = []
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node in open_list:
            open_list.remove(node)
        if node == goal:
            return path, open_list + [n for n in queue_nodes(queue)], closed_list
        closed_list.append(node)
        for neighbour in graph.get(node, {}):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])
                open_list.append(neighbour)
    return None, open_list, closed_list


def queue_nodes(queue):
    """Get queued endpoint names for display."""
    return [path[-1] for path in queue]


def dfs(graph, start, goal):
    """Depth-first search. Returns a path and the search trace."""
    if start not in graph or goal not in graph:
        return None, [], []
    stack = [[start]]
    visited = set()
    open_list = [start]
    closed_list = []
    while stack:
        path = stack.pop()
        node = path[-1]
        if node in visited:
            continue
        visited.add(node)
        if node in open_list:
            open_list.remove(node)
        if node == goal:
            return path, open_list, closed_list
        closed_list.append(node)
        # Reverse neighbours so the displayed exploration is stable and easy to follow.
        for neighbour in reversed(list(graph.get(node, {}).keys())):
            if neighbour not in visited:
                stack.append(path + [neighbour])
                if neighbour not in open_list:
                    open_list.append(neighbour)
    return None, open_list, closed_list


def astar(graph, start, goal, positions=None):
    """A* search using Euclidean distance between sample node positions as heuristic."""
    if start not in graph or goal not in graph:
        return None, [], [], float("inf")
    positions = positions or {}

    def heuristic(node):
        if node not in positions or goal not in positions:
            return 0
        x1, y1 = positions[node]
        x2, y2 = positions[goal]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    frontier = [(heuristic(start), 0, start)]
    came_from = {}
    g_score = {start: 0}
    open_nodes = {start}
    closed_list = []
    while frontier:
        _, cost, current = heapq.heappop(frontier)
        if current not in open_nodes:
            continue
        open_nodes.remove(current)
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, sorted(open_nodes), closed_list, cost
        closed_list.append(current)
        for neighbour, edge_cost in graph.get(current, {}).items():
            new_cost = g_score[current] + edge_cost
            if new_cost < g_score.get(neighbour, float("inf")):
                came_from[neighbour] = current
                g_score[neighbour] = new_cost
                heapq.heappush(frontier, (new_cost + heuristic(neighbour), new_cost, neighbour))
                open_nodes.add(neighbour)
    return None, sorted(open_nodes), closed_list, float("inf")


def path_cost(graph, path):
    """Calculate the total edge cost for a path."""
    if not path or len(path) < 2:
        return 0
    return sum(graph[a][b] for a, b in zip(path, path[1:]))
