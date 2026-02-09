from pathlib import Path
import numpy as np
from scipy.optimize import fsolve

N = 1000
s = 0.001
runs= 100000

# List of directories to process
INPUT_DIRS = [
    Path("amp_acc/graphs/PA"),
    Path("amp_acc/graphs/bottlenecks_2"),
    Path("amp_acc/graphs/bottlenecks_4"),
    Path("amp_acc/graphs/bottlenecks_regular"),
    Path("amp_acc/graphs/fingers"),
    Path("amp_acc/graphs/grids"),
    Path("amp_acc/graphs/lines_2"),
    Path("amp_acc/graphs/random_geometric_1"),
    Path("amp_acc/graphs/random_geometric_2"),
    Path("amp_acc/graphs/regular_graphs_4"),
    Path("amp_acc/graphs/regular_graphs"),
    Path("amp_acc/graphs/regular_graphs_10")
]


INPUT_BASE = Path("amp_acc_wm")
OUTPUT_BASE = Path("amp_acc/acceleration")
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)


def acceleration(filepath, filepathwm):
    try:
        # Check if either file exists
        if not filepath.exists() or not filepathwm.exists():
            print(f"Missing file(s), returning NaN: {filepath}, {filepathwm}")
            return np.nan

        data = []
        datawm = []

        with open(filepath, "r") as f:
            for line in f:
                values = [float(v) for v in line.strip().split("\t")]
                data.append(values)

        with open(filepathwm, "r") as f:
            for line in f:
                valueswm = [float(v) for v in line.strip().split("\t")]
                datawm.append(valueswm)

        data = np.array(data)
        datawm = np.array(datawm)  # fixed: was previously data

        averages = data.mean(axis=0)
        averageswm = datawm.mean(axis=0)

        fixated_times = averages[4]
        average_fixated_times = fixated_times / runs
        fixated_timeswm = averageswm[4]
        average_fixated_timeswm = fixated_timeswm / runs

        return average_fixated_timeswm / average_fixated_times

    except Exception as e:
        print(f"Error processing {filepath.name} / {filepathwm.name}: {e}. Returning NaN.")
        return np.nan


def process_all_directories():
    for input_dir in INPUT_DIRS:
        if not input_dir.exists():
            print(f"Skipping missing directory: {input_dir}")
            continue

        # Mirror directory structure
        output_dir = OUTPUT_BASE / input_dir.name
        output_dir.mkdir(parents=True, exist_ok=True)

        for filepath in input_dir.glob("*.txt"):
            filepathwm = INPUT_BASE / input_dir.name / filepath.name
            alpha = acceleration(filepath,filepathwm)

            output_file = output_dir / f"{filepath.stem}.txt"
            with open(output_file, "w") as f:
                f.write(f"{alpha}\n")

            #print(f"{input_dir.name}/{filepath.name} → alpha = {alpha}")


if __name__ == "__main__":
    process_all_directories()
