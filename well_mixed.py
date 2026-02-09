import networkx as nx
if __name__ == "__main__":
    n = 100
    G = nx.complete_graph(n)
    nx.write_edgelist(G, f"wellmixed.txt", data=False)