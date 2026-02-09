import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import statistics
def save_edge_list_txt(G, filename):
    with open(filename, "w") as f:
        for u, v in G.edges():
            f.write(f"{u} {v}\n")

def preferential_attachment_graph(N, m=1, beta=1.0, seed=None):
    """
    Generate a generalized preferential attachment (PA) graph.
    
    Parameters:
    - N: int, total number of nodes
    - m: int, number of edges each new node adds
    - beta: float, preferential attachment exponent
        beta=0 -> random attachment (exponential degree)
        0<beta<1 -> stretched exponential
        beta=1 -> scale-free / power law
    - seed: int, random seed
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    # Start with a single node
    G = nx.Graph()
    G.add_node(0)
    
    # Keep track of the degrees
    degrees = [0]  # degree of node 0
    
    for new_node in range(1, N):
        G.add_node(new_node)
        targets = set()
        
        # Compute attachment probabilities
        deg_array = np.array(degrees)
        if deg_array.sum() == 0:
            # If all degrees are zero, attach randomly
            probs = np.ones(len(degrees)) / len(degrees)
        else:
            probs = deg_array**beta
            probs = probs / probs.sum()
        
        # Choose m distinct nodes to connect to
        while len(targets) < min(m, len(degrees)):
            chosen = np.random.choice(len(degrees), p=probs)
            targets.add(chosen)
        
        # Add edges
        for target in targets:
            G.add_edge(new_node, target)
        
        # Update degrees
        degrees.append(len(targets))
        for target in targets:
            degrees[target] += 1
    
    return G

N = 1000

"""
beta
m = 10
for i in range (0, 101):
    beta = i/100
    G = preferential_attachment_graph(N, m, beta)

    # Plot the graph
    plt.figure(figsize=(8,6))  
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_size=5, node_color='skyblue', with_labels=False)
    plt.savefig(f"PA_beta_pngs/PA_{beta}.png", dpi=300, bbox_inches="tight")

    degrees = dict(G.degree())
    degree_values = list(degrees.values())
    print(statistics.mean(degree_values))
    degree_variance = statistics.variance(degree_values)
    print(f"Degree Variance: {degree_variance}")

    filename = f"PA_beta/PA_{beta}.txt"
    save_edge_list_txt(G, filename)
"""

beta = 0.5
for m in range (5, 105, 5):
    beta = 1
    G = preferential_attachment_graph(N, m, beta)

    # Plot the graph
    #plt.figure(figsize=(8,6))  
    #pos = nx.spring_layout(G)
    #nx.draw(G, pos, node_size=5, node_color='skyblue', with_labels=False)
    #plt.savefig(f"PA_m_pngs/PA_{beta}.png", dpi=300, bbox_inches="tight")

    degrees = dict(G.degree())
    degree_values = list(degrees.values())
    print(statistics.mean(degree_values))
    degree_variance = statistics.variance(degree_values)
    print(f"Degree Variance: {degree_variance}")

    filename = f"PA_m/PA_{beta}.txt"
    save_edge_list_txt(G, filename)