import networkx as nx
if __name__ == "__main__":
    n = 1000
    for d in range (101, 1000): 
        for i in range(0,1):
            G = nx.random_regular_graph(d, n)
            nx.write_edgelist(G, f"regular_graphs/d{d}_{i}.txt", data=False)