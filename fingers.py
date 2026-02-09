import networkx as nx
import matplotlib.pyplot as plt


def save_edge_list_txt(G, filename):
    with open(filename, "w") as f:
        for u, v in G.edges():
            f.write(f"{u} {v}\n")

def plot_grid(G, rows=40, cols=25, title="Grid"):
    # Map integer node to (x, y) position
    pos = {n: (n % cols, n // cols) for n in G.nodes()}
    
    plt.figure(figsize=(10, 16))
    nx.draw(
        G,
        pos=pos,
        with_labels=False,  # shows integer labels
        node_size=50,
        node_color="skyblue",
        edge_color="gray"
    )
    plt.gca().invert_yaxis()  # top row at top
    plt.savefig(f"fingers_pngs/finger_{i}.png", dpi=300, bbox_inches="tight")
    plt.close()

def generate_grid_generations(rows=40, cols=25):
    """
    Returns a list of graphs.
    Generation k has horizontal edges in rows [0, k-1]
    and all vertical edges present.
    """
    generations = []

    # Create a mapping: (row, col) -> node integer
    def node_id(r, c):
        return r * cols + c

    # Precompute vertical edges (always present)
    vertical_edges = [
        (node_id(r, c), node_id(r + 1, c))
        for r in range(rows - 1)
        for c in range(cols)
    ]

    for k in range(1, rows + 1):
        G = nx.Graph()
        G.add_nodes_from(range(rows * cols))

        # Add all vertical edges
        G.add_edges_from(vertical_edges)

        # Add horizontal edges for rows 0 through k-1
        horizontal_edges = [
            (node_id(r, c), node_id(r, c + 1))
            for r in range(k)
            for c in range(cols - 1)
        ]
        G.add_edges_from(horizontal_edges)

        generations.append(G)
        filename = f"fingers/finger_{k}.txt"
        save_edge_list_txt(G, filename)

    return generations

if __name__ == "__main__":
    generations = generate_grid_generations()
    i = 1
    for G in generations: 
        plot_grid(G,i)
        i+=1