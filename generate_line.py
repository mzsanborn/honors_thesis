import networkx as nx
import matplotlib.pyplot as plt
import os

def build_graph_and_save(output_folder="lines_2", plot_folder="pngs"):
    # Create folders
    # Create folders
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(plot_folder, exist_ok=True)

    # Step 1: line graph of 1000 nodes
    G = nx.path_graph(1000)

    # Step 2: center points
    left = 499
    right = 500

    # --- BENT-LINE LAYOUT ---
    # Left half rises upward, right half slopes downward
    pos = {}
    for i in range(1000):
        if i <= 499:
            # left half slopes up
            pos[i] = (i, (499 - i) * 0.01)
        else:
            # right half slopes down
            pos[i] = (i, (i - 500) * 0.01)

    step = 0
    while left >= 0 and right <= 999:

        # Add cross-edge
        G.add_edge(left, right)

        # Save edge list
        filename = os.path.join(output_folder, f"line_{step}.txt")
        with open(filename, "w") as f:
            for u, v in G.edges():
                f.write(f"{u} {v}\n")

        # Plot every 10 iterations
        if step % 10 == 0:
            plt.figure(figsize=(14, 4))
            nx.draw(G, pos, node_size=10, width=0.5, with_labels=False)
            plot_name = os.path.join(plot_folder, f"iteration_{step}.png")
            plt.savefig(plot_name, dpi=200, bbox_inches="tight")
            plt.close()

        step += 1
        left -= 1
        right += 1



if __name__ == "__main__":
    build_graph_and_save()
