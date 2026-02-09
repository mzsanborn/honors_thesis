import networkx as nx
import random
import matplotlib.pyplot as plt

def save_edge_list_txt(G, filename):
    with open(filename, "w") as f:
        for u, v in G.edges():
            f.write(f"{u} {v}\n")

def plot_graph_png(G, clusters, filename_png):
    pos = {}
    cluster_offsets = [(0,0), (5,-5)]
    for c_idx, cluster in enumerate(clusters):
        x0, y0 = cluster_offsets[c_idx]
        side = int(len(cluster)**0.5)
        for i, node in enumerate(cluster):
            row = i // side
            col = i % side
            pos[node] = (x0 + col * 0.1, y0 - row * 0.1)

    colors = ["red", "blue"]
    node_colors = {}
    for c_idx, cluster in enumerate(clusters):
        for node in cluster:
            node_colors[node] = colors[c_idx]
    color_list = [node_colors[n] for n in G.nodes()]

    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_color=color_list, node_size=80, edge_color="black", width=1.5, with_labels=False)
    plt.tight_layout()
    plt.savefig(filename_png, dpi=300)
    plt.close()        
# ============================================================
# Main generator
# ============================================================
def generate_bottleneck_graphs(generations):
    for gen in range(1, generations + 1):
        cluster1 = nx.random_regular_graph(gen, 500)
        cluster2 = nx.random_regular_graph(gen, 500)
        print(f"\n=== Generation {gen} ===")
        cluster2_nodes = [i+500 for i in cluster2.nodes()]

        U = nx.disjoint_union(cluster1, cluster2)

        for i in range (0,500):
            U.add_edge(i, i+500)
            conn = nx.algebraic_connectivity(U, method="lanczos", normalized=True)
            if (conn < 0.006 and conn >=0.005): 
                break

        avg_degree = sum(dict(U.degree()).values()) / U.number_of_nodes()
        conn = nx.algebraic_connectivity(U, method="lanczos", normalized=True)

        print("Average degree:", avg_degree)
        print("Connectivity", conn)
        # Step 3 — save graph
        filename = f"bottlenecks_regular/bottleneck_{gen}.txt"
        save_edge_list_txt(U, filename)
        plot_graph_png(U, [cluster1,cluster2_nodes], f"pngs_regular/bottleneck_{gen}.png")
        
if __name__ == "__main__":
    generate_bottleneck_graphs(100)