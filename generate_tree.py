import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generate_network_grid(height, width):
    edge_dict = {}
    for i in range(height):
        for j in range(width):
            node = i * width + j
            neighbors = []
            if i > 0:
                neighbors.append((i - 1) * width + j)
            if i < height - 1:
                neighbors.append((i + 1) * width + j)
            if j > 0:
                neighbors.append(i * width + (j - 1))
            if j < width - 1:
                neighbors.append(i * width + (j + 1))
            edge_dict[node] = neighbors
    return edge_dict

def remove_edge(node, edge_dict):
    if node in edge_dict and (node + 1) in edge_dict[node]:
        edge_dict[node].remove(node + 1)
    if (node + 1) in edge_dict and node in edge_dict[node + 1]:
        edge_dict[node + 1].remove(node)
    return edge_dict

def dict_to_list(edge_dict):
    edge_list = []
    seen = set()
    for node, neighbors in edge_dict.items():
        for nbr in neighbors:
            edge = tuple(sorted((node, nbr)))
            if edge not in seen:
                seen.add(edge)
                edge_list.append(edge)
    return edge_list

def generate_tree(num_levels, height, width):
    edge_dict = generate_network_grid(height, width)

    # Compute row indices for each level (evenly split, last level takes any extra rows)
    level_rows = np.linspace(0, height, num_levels + 1, dtype=int)

    for level in range(num_levels):
        start_row = level_rows[level]
        end_row = level_rows[level + 1]

        num_segments = 2 ** level
        # Compute aligned horizontal cut positions
        step_positions = np.linspace(0, width, num_segments + 1, dtype=int)[1:-1]  # exclude 0 and width

        for i in range(start_row, end_row):
            for j in step_positions:
                node = i * width + (j - 1)
                edge_dict = remove_edge(node, edge_dict)

    return dict_to_list(edge_dict)


if __name__ == "__main__":
    height = 201
    width = 201

    for level in range(1, 9):
        edge_list = generate_tree(level, height, width)

        with open(f"trees/tree_{level}.txt", "w") as f:
            for n1, n2 in edge_list:
                f.write(f"{n1} {n2}\n")

        G = nx.Graph()
        total_nodes = height * width
        G.add_nodes_from(range(total_nodes))
        G.add_edges_from(edge_list)
        pos = {i: (i % width, -i // width) for i in range(total_nodes)}

        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, node_size=1, node_color="skyblue", edge_color="gray", with_labels=False)
        plt.title(f"Grid Tree Network - Level {level}")
        plt.savefig(f"trees_pngs/grid_network_level_{level}.png", dpi=300, bbox_inches="tight")
        plt.close()
