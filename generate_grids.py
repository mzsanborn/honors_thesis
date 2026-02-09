import networkx as nx 
import matplotlib.pyplot as plt 
import math

def generate_network_grid(height=500, width=2):
    edge_dict = {}
    print(height, width)
    # Each node connects to its top, bottom, left, and right neighbors if they exist
    for i in range(height):
        for j in range(width):
            node = i * width + j
            neighbors = []

            # Up
            if i > 0:
                neighbors.append((i - 1) * width + j)
            # Down
            if i < height - 1:
                neighbors.append((i + 1) * width + j)
            # Left
            if j > 0:
                neighbors.append(i * width + (j - 1))
            # Right
            if j < width - 1:
                neighbors.append(i * width + (j + 1))

            edge_dict[node] = neighbors

    return edge_dict


def dict_to_list(edge_dict):
    """
    Converts adjacency dictionary to a list of undirected edges (tuples).
    Each edge is represented once (smaller node first).
    """
    edge_list = []
    seen = set()

    for node, neighbors in edge_dict.items():
        for nbr in neighbors:
            edge = tuple(sorted((node, nbr)))
            if edge not in seen:
                seen.add(edge)
                edge_list.append(edge)

    return edge_list


def generate_grid(height, width):
    edge_dict = generate_network_grid(height, width)
    edge_list = dict_to_list(edge_dict)
    return edge_list


if __name__ == "__main__":
    n = 1000
    for height in range (1,int(math.sqrt(n))): 
        if (n/height).is_integer(): 
            width = int(n/height)
            edge_list = generate_grid(height, width)
            with open(f"grids/grid_{height}.txt", "w") as f:
                for n1, n2 in edge_list:
                    f.write(f"{n1} {n2}\n")

                    G = nx.Graph()
                    total_nodes = n
                    G.add_nodes_from(range(total_nodes))   # ensures all nodes are included, even if isolated
                    G.add_edges_from(edge_list)

                    # grid-based layout
                pos = {}
                for i in range(height):
                    for j in range(width):
                        node = i * width + j
                        pos[node] = (j, -i)  # x=j, y=i; negative y to flip vertically

                # Plot
                plt.figure(figsize=(8, height / 10))  # adjustable scale
                nx.draw(
                    G,
                    pos,
                    node_size=20,
                    width=0.5,
                    with_labels=False
                )

                plt.savefig(f"pngs/grid_network_level_{height}.png", dpi=300, bbox_inches="tight")
                plt.close()
 
