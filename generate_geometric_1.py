import networkx as nx
from scipy.stats import pareto
import math, random
import sys
import matplotlib.pyplot as plt

n=1000
def geometric_random(r):
    print(f"Generating for r={r} ...")
    for i in range(1,11):
        G = nx.random_geometric_graph(n, radius = r)
        while(not nx.is_connected(G)): 
            G = nx.random_geometric_graph(n, radius = r)
        nx.write_edgelist(G, f"random_geometric_1/random_geometric_{r}_{i}.txt", data=False)

if __name__ == "__main__":
    for i in range (5, 100):
        geometric_random(i/100)