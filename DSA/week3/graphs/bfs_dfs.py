#Implementation of DFS
from graph import Graph
import queue
import random
import time

def dfs(G, visited, order, u):
    # The actual dfs recursive behavior
    visited.add(u)
    order.append(u)
    for v in G.adj_list[u]:
        if v not in visited:
            dfs(G, visited, order, v)
    return visited, order

def dfs_setup(G, start):
    VS = set()
    order = []
    final_vs, final_order = dfs(G, VS, order, start)
    return final_vs, final_order

def bfs(G, start):
    #ONLY look at adjacent vertices that have NOT been visited
    VS = set()
    order = []
    q = queue.Queue()
    VS.add(start)
    q.put(start)
    while not q.empty():
        v = q.get()
        order.append(v)
        for u in G.adj_list[v]:
            if u not in VS:
                VS.add(u)
                q.put(u)
    return VS, order

def main():
    G = Graph()
    for i in range(5):
        G.add_vertex(i)
    edges = [(1,2), (1,4), (2,1), (2,3), (2,0), (3,1), (3,0), (3,4), (4,0), (4,1)]
    for u,v in edges:
        G.add_edge(u,v)
    start = time.perf_counter()
    vs,order = dfs_setup(G, 0)
    total_time = time.perf_counter() - start
    print("DFS results...")
    print(f"Total time elapsed: {total_time}")
    print(vs)
    print(order)
    print()
    start = time.perf_counter()
    bvs, border = bfs(G, 0)
    total_time = time.perf_counter() - start
    print("BFS results...")
    print(f"Total time elapsed: {total_time}")
    print(bvs)
    print(border)


if __name__ == "__main__":
    main()