from collections import namedtuple, deque, defaultdict
from pprint import pprint as pp
import heapq

inf = float('inf')
Edge = namedtuple('Edge', ['start', 'end', 'cost'])

class Graph():
    def __init__(self, edges):
        self.edges = [Edge(*edge) for edge in edges]
        self.vertices = {e.start for e in self.edges} | {e.end for e in self.edges}

    def dijkstra(self, source, dest):
        assert source in self.vertices
        dist = {vertex: inf for vertex in self.vertices}
        previous = defaultdict(list)  # Store multiple predecessors
        dist[source] = 0
        q = []
        heapq.heappush(q, (0, source))
        neighbours = {vertex: set() for vertex in self.vertices}
        for start, end, cost in self.edges:
            neighbours[start].add((end, cost))
            neighbours[end].add((start, cost))  # For undirected graphs

        while q:
            current_dist, u = heapq.heappop(q)
            if u == dest:
                break
            if current_dist > dist[u]:
                continue
            for v, cost in neighbours[u]:
                alt = dist[u] + cost
                if alt < dist[v]:
                    dist[v] = alt
                    previous[v] = [u]  # Reset predecessors
                    heapq.heappush(q, (alt, v))
                elif alt == dist[v]:
                    previous[v].append(u)  # Add additional predecessor

        # Reconstruct all shortest paths
        def reconstruct_paths(vertex):
            if vertex == source:
                return [[source]]
            paths = []
            for pred in previous[vertex]:
                for path in reconstruct_paths(pred):
                    paths.append(path + [vertex])
            return paths

        return reconstruct_paths(dest)