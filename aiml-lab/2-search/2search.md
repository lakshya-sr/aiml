Name: Lakshya Shrivastav


# Search Strategies on Different Types of Graphs

```python




import random
import time
import math
import heapq
from collections import deque

N = 100
TRIALS = 5
random.seed(42)


def generate_graph(n, density):
    points = [(random.random() * 100, random.random() * 100)
              for _ in range(n)]
    graph = {i: {} for i in range(n)}

    def distance(u, v):
        return math.dist(points[u], points[v])

    def add_edge(u, v):
        w = distance(u, v)
        graph[u][v] = w
        graph[v][u] = w

    # Spanning tree ensures connectivity
    for v in range(1, n):
        add_edge(v, random.randrange(v))

    for u in range(n):
        for v in range(u + 1, n):
            if v not in graph[u] and random.random() < density:
                add_edge(u, v)

    return graph, points


def heuristic(points, u, goal):
    return math.dist(points[u], points[goal])


def path_cost(graph, path):
    if path is None:
        return float("inf")
    return sum(graph[u][v] for u, v in zip(path, path[1:]))


def bfs(graph, start, goal, points):
    queue = deque([(start, [start])])
    visited = {start}
    explored = 0

    while queue:
        u, path = queue.popleft()
        explored += 1

        if u == goal:
            return path, explored

        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                queue.append((v, path + [v]))

    return None, explored


def dfs(graph, start, goal, points):
    stack = [(start, [start])]
    visited = set()
    explored = 0

    while stack:
        u, path = stack.pop()

        if u in visited:
            continue

        visited.add(u)
        explored += 1

        if u == goal:
            return path, explored

        for v in graph[u]:
            if v not in visited:
                stack.append((v, path + [v]))

    return None, explored


def ucs(graph, start, goal, points):
    pq = [(0, start, [start])]
    best = {start: 0}
    explored = 0

    while pq:
        cost, u, path = heapq.heappop(pq)

        if cost > best[u]:
            continue

        explored += 1

        if u == goal:
            return path, explored

        for v, w in graph[u].items():
            new_cost = cost + w

            if new_cost < best.get(v, float("inf")):
                best[v] = new_cost
                heapq.heappush(pq, (new_cost, v, path + [v]))

    return None, explored


def greedy(graph, start, goal, points):
    pq = [(heuristic(points, start, goal), start, [start])]
    visited = set()
    explored = 0

    while pq:
        _, u, path = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)
        explored += 1

        if u == goal:
            return path, explored

        for v in graph[u]:
            if v not in visited:
                h = heuristic(points, v, goal)
                heapq.heappush(pq, (h, v, path + [v]))

    return None, explored


def astar(graph, start, goal, points):
    pq = [(heuristic(points, start, goal), 0, start, [start])]
    best = {start: 0}
    explored = 0

    while pq:
        f, cost, u, path = heapq.heappop(pq)

        if cost > best[u]:
            continue

        explored += 1

        if u == goal:
            return path, explored

        for v, w in graph[u].items():
            new_cost = cost + w

            if new_cost < best.get(v, float("inf")):
                best[v] = new_cost
                h = heuristic(points, v, goal)
                heapq.heappush(
                    pq, (new_cost + h, new_cost, v, path + [v])
                )

    return None, explored


def hill_climbing(graph, start, goal, points):
    current = start
    path = [start]
    visited = {start}
    explored = 0

    while current != goal:
        explored += 1
        neighbors = [v for v in graph[current] if v not in visited]

        if not neighbors:
            return None, explored

        next_node = min(
            neighbors, key=lambda v: heuristic(points, v, goal)
        )

        if heuristic(points, next_node, goal) >= heuristic(
            points, current, goal
        ):
            return None, explored

        current = next_node
        visited.add(current)
        path.append(current)

    return path, explored + 1


def csp_backtracking(graph, start, goal, points):
    # Variables are successive nodes in a path.
    # Constraints: adjacent nodes and no repeated vertices.
    explored = 0
    visited = {start}
    path = [start]

    def backtrack(u):
        nonlocal explored
        explored += 1

        if u == goal:
            return True

        neighbors = sorted(
            graph[u],
            key=lambda v: heuristic(points, v, goal)
        )

        for v in neighbors:
            if v not in visited:
                visited.add(v)
                path.append(v)

                if backtrack(v):
                    return True

                path.pop()
                visited.remove(v)

        return False

    if backtrack(start):
        return path[:], explored

    return None, explored


algorithms = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Greedy": greedy,
    "A*": astar,
    "Hill Climbing": hill_climbing,
    "CSP Backtracking": csp_backtracking
}

graph_types = {
    "Sparse": 0.02,
    "Medium": 0.15,
    "Dense": 0.60,
    "Complete": 1.0
}


def evaluate():
    for graph_type, density in graph_types.items():
        results = {
            name: {"time": 0, "nodes": 0, "cost": 0, "success": 0}
            for name in algorithms
        }

        for trial in range(TRIALS):
            graph, points = generate_graph(N, density)
            start, goal = 0, N - 1

            for name, algorithm in algorithms.items():
                t0 = time.perf_counter()
                path, explored = algorithm(graph, start, goal, points)
                elapsed = (time.perf_counter() - t0) * 1000

                r = results[name]
                r["time"] += elapsed
                r["nodes"] += explored

                if path is not None:
                    r["success"] += 1
                    r["cost"] += path_cost(graph, path)

        print(f"\n{graph_type.upper()} GRAPH (density={density})")
        print("-" * 83)
        print(f"{'Algorithm':<19} {'Time(ms)':>10} "
              f"{'Nodes':>10} {'Cost':>12} {'Success':>12}")
        print("-" * 83)

        for name, r in results.items():
            success = r["success"]
            avg_cost = r["cost"] / success if success else float("inf")

            print(f"{name:<19} "
                  f"{r['time']/TRIALS:>10.4f} "
                  f"{r['nodes']/TRIALS:>10.1f} "
                  f"{avg_cost:>12.2f} "
                  f"{100*success/TRIALS:>11.0f}%")

        print("-" * 83)


if __name__ == "__main__":
    evaluate()

```


# Output

```


SPARSE GRAPH (density=0.02)
-----------------------------------------------------------------------------------
Algorithm             Time(ms)      Nodes         Cost      Success
-----------------------------------------------------------------------------------
BFS                     0.1011       73.2       155.67         100%
DFS                     0.0850       40.2      1809.35         100%
UCS                     0.2504       69.0       139.40         100%
Greedy                  0.2287       35.2       225.31         100%
A*                      0.2518       31.2       139.40         100%
Hill Climbing           0.0290        1.6          inf           0%
CSP Backtracking        0.1594       19.4       821.42         100%
-----------------------------------------------------------------------------------

MEDIUM GRAPH (density=0.15)
-----------------------------------------------------------------------------------
Algorithm             Time(ms)      Nodes         Cost      Success
-----------------------------------------------------------------------------------
BFS                     0.1518       46.6        77.55         100%
DFS                     0.0455        5.8       226.98         100%
UCS                     0.4649       44.0        56.87         100%
Greedy                  0.1789        6.8        87.63         100%
A*                      0.1824        6.6        56.87         100%
Hill Climbing           0.0505        2.2        42.05          40%
CSP Backtracking        0.1793        7.8       156.55         100%
-----------------------------------------------------------------------------------

DENSE GRAPH (density=0.6)
-----------------------------------------------------------------------------------
Algorithm             Time(ms)      Nodes         Cost      Success
-----------------------------------------------------------------------------------
BFS                     0.4280       83.6        67.05         100%
DFS                     0.0478        2.8        82.54         100%
UCS                     1.0507       46.0        45.37         100%
Greedy                  0.1626        2.6        47.92         100%
A*                      0.2119        3.0        45.37         100%
Hill Climbing           0.1324        2.6        47.92         100%
CSP Backtracking        0.1484        2.6        47.92         100%
-----------------------------------------------------------------------------------

COMPLETE GRAPH (density=1.0)
-----------------------------------------------------------------------------------
Algorithm             Time(ms)      Nodes         Cost      Success
-----------------------------------------------------------------------------------
BFS                     0.7351      100.0        47.40         100%
DFS                     0.0373        2.0        47.40         100%
UCS                     1.7463       49.4        47.40         100%
Greedy                  0.1690        2.0        47.40         100%
A*                      0.2407        2.0        47.40         100%
Hill Climbing           0.1334        2.0        47.40         100%
CSP Backtracking        0.1515        2.0        47.40         100%
-----------------------------------------------------------------------------------

```
