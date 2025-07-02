#Graph Self-Implemented Class
import json

class Graph:
    def __init__(self):
        self.adj_list = {}
    def add_vertex(self, v):
        """
        if v not in self.adj_list:
            self.adj_list[v] = []  # Empty list of adj. vertices
        else:
            pass  # Do nothing if the vertex is already in the adjacency list
        """
        self.adj_list.setdefault(v, [])
    def add_edge(self, v, u):
        if v not in self.adj_list:
            self.adj_list[v] = [u]
        else:  # v is already a vertex in the Graph
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)
        if u not in self.adj_list:
            self.adj_list[u] = [v]
        else:  # u is already a vertex in the Graph
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
    def __str__(self):
        return json.dumps(self.adj_list, indent=2)

"""
Structure of the data:
{
v1: [v2,v3,...]
v2: [v1,v5,...]
...
vn: [v3,v4,...]
}
"""