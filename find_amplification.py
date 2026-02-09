from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.optimize import fsolve

# Parameters
N = 1000
s = 0.001
runs = 100_000

# Input directories
INPUT_DIRS = [
    Path("graphs/PA"),
    Path("graphs/bottlenecks_2"),
    Path("graphs/bottlenecks_4"),
    Path("graphs/bottlenecks_regular"),
    Path("graphs/fingers"),
    Path("graphs/grids"),
    Path("graphs/lines_2"),
    Path("graphs/random_geometric_1"),
    Path("graphs/random_geometric_2"),
    Path("graphs/regular_graphs_4"),
    Path("graphs/regular_graphs"),
    Path("graphs/regular_graphs_10"),
]

# Output base directory
OUTPUT_BASE = Path("amp_acc/amplification")
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)


def parse_type(path: Path) -> str:
    """
    Extract graph type from filenames like:
    '12_PA.txt' -> 'PA'
    """
    return path.stem.split("_", 1)[1]


def amplification(filepath: Path) -> float:
    """
    Compute alpha for a single run file.
    """
    data = []

    with open(filepath, "r") as f:
        for line in f:
            values = [float(v) for v in line.strip().split("\t")]
            data.append(values)

    data = np.array(data)
    averages = data.mean(axis=0)

    fixated = averages[2]
    probability_fixated = fixated / runs

    alpha_guess = 1.0

    def func(alpha):
        return (
            (1 - (1 + s) ** (-alpha))
            / (1 - (1 + s) ** (-alpha * N))
            - probability_fixated
        )

    alpha = fsolve(func, alpha_guess)[0]
    return alpha


def process_all_directories():
    for input_dir in INPUT_DIRS:
        if not input_dir.exists():
            print(f"Skipping missing directory: {input_dir}")
            continue

        output_dir = OUTPUT_BASE / input_dir.name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Collect alphas by graph type
        alpha_by_type = defaultdict(list)

        for filepath in input_dir.glob("*.txt"):
            graph_type = parse_type(filepath)
            alpha = amplification(filepath)
            alpha_by_type[graph_type].append(alpha)

        # Write averaged alpha per graph type
        for graph_type, alphas in alpha_by_type.items():
            mean_alpha = np.mean(alphas)

            output_file = output_dir / f"{graph_type}.txt"
            with open(output_file, "w") as f:
                f.write(f"{mean_alpha}\n")

            # Optional debug
            # print(f"{input_dir.name}/{graph_type}: "
            #       f"{len(alphas)} runs → mean alpha = {mean_alpha}")


if __name__ == "__main__":
    process_all_directories()