import networkx as nx
from scipy.stats import pareto
import math, random
import sys
import matplotlib.pyplot as plt

n = 1000

def generate_positions(n, box_size=512):
    positions = []
    while len(positions) < n:
        x, y = random.uniform(1, box_size), random.uniform(1, box_size)
        positions.append((x, y))
    return {i: positions[i] for i in range(n)}

def geometric_random(u):
    print(f"Generating for μ={u} ...")

    def p_dist(distance):
        r = max(1, distance)
        return u * (r)**(-(1+u))
    
    pos = generate_positions(n, box_size=512)
    G = nx.soft_random_geometric_graph(n, radius=512, pos=pos, p_dist=p_dist)

    print("Graph generated:", G.number_of_nodes(), "nodes")
    nx.write_edgelist(G, f"graphs/random_geometric_{u}.txt", data=False)

    # visualize
    visualize_graph(G, pos, title=f"soft geometric μ={u}")

def generate_graph(u): 
    def p_dist(r):
        if r < 1: 
            return 1 
        return u * ((r)**(-(1 + u)))

    G = nx.Graph()
    pos = generate_positions(n, box_size=32)
    G.add_nodes_from(pos)
    # local edges
    for i0, (x0,y0) in pos.items(): 
        for i1, (x1, y1) in pos.items(): 
            dist = math.dist((x0,y0), (x1, y1))
            if dist < 1 and i0 != i1: 
                G.add_edge(i0,i1)

    nodes = list(pos.items())

    # long-range edges
    while G.number_of_edges() < 4000: 
        i0, (x0, y0) = random.choice(nodes)
        i1, (x1, y1) = random.choice(nodes)
        dist = math.dist((x0,y0), (x1, y1))
        prob = p_dist(dist) 
        rn = random.random() 
        if rn < prob and i0 != i1: 
            G.add_edge(i0,i1)

    return G, pos

def geometric_random_2(u):
    print(f"\nGenerating for μ={u} ...")
        
    G, pos = generate_graph(u)
    while(not nx.is_connected(G)): 
        print("again!")
        G, pos = generate_graph(u)        

    print("Graph generated:", G.number_of_nodes(), "nodes,", G.number_of_edges(), "edges")

        # Save
    nx.write_edgelist(G, f"graphs/random_geometric_{u}.txt", data=False)
            # Sum of degrees
    sum_degrees = sum(dict(G.degree()).values())

        # Average degree
    avg_degree = sum_degrees / G.number_of_nodes()

        # Average geometric distance between nodes connected by an edge
    total_dist = 0
    for u0, v0 in G.edges():
        x0, y0 = pos[u0]
        x1, y1 = pos[v0]
        total_dist += math.dist((x0, y0), (x1, y1))
    avg_edge_distance = total_dist / G.number_of_edges()

        # Print stats
    print(f"  Sum of degrees:             {sum_degrees}")
    print(f"  Average degree:             {avg_degree:.4f}")
    print(f"  Avg distance per edge:      {avg_edge_distance:.4f}")
        # Visualize
    visualize_graph(G, pos, title=f"μ={u}")

def visualize_graph(G, pos, title="Graph"):
    plt.figure(figsize=(7,7))

    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=5)

    nx.draw_networkx_edges(G, pos, alpha=0.2)

    plt.title(title)
    plt.savefig(f"graphs_images/random_geometric_{u}.png", dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    #[0.1, 0.2, 0.3, 0.4, 0.5, 0.75,1.0,1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
    for u in [0.5, 1.5, 3.0, 5.0]:
        geometric_random_2(u)
