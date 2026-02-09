import networkx as nx

if __name__ == "__main__":
    """"""
    n = 2520 * 512
    for i in range (0,100): 
        G = nx.random_geometric_graph(n, i/100000)

        sum_of_degrees = sum(dict(G.degree()).values())
        num_nodes = G.number_of_nodes()
        average_degree = sum_of_degrees / num_nodes
        nx.write_edgelist(G, "graphs/geometric" + str(i) + ".txt", data=False)

