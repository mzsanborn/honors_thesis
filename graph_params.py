import pandas as pd
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.optimize import fsolve

def overwrite_amp(
    csv_file="params.csv",
    amp_root="amplification",
    graph_type="PA_assortative"
):
    csv_file = Path(csv_file)
    df = pd.read_csv(csv_file)

    mask = df["graph_type"] == graph_type
    subset = df.loc[mask]

    if subset.empty:
        print(f"No rows found for graph_type={graph_type}")
        return df

    updated = 0

    for idx, row in subset.iterrows():
        name = row["graph_name"]
        amp_file = Path(amp_root) / graph_type / f"{name}.txt"

        if not amp_file.exists():
            print(f"Missing amp file: {amp_file}")
            continue

        try:
            with open(amp_file, "r") as f:
                amp = float(f.read().strip())

            df.at[idx, "amp"] = amp
            updated += 1

        except Exception as e:
            print(f"Failed reading {amp_file}: {e}")

    df.to_csv(csv_file, index=False)
    print(f"Updated amp for {updated} {graph_type} graphs")

    return df


def add_graph_type_to_csv(
    graph_type: str,
    graphs_root="graphs",
    output_file="params.csv"
):
    """
    Adds a new graph type to params.csv without recomputing existing graphs.
    """
    graph_dir = Path(graphs_root) / graph_type
    output_file = Path(output_file)

    if not graph_dir.exists():
        raise FileNotFoundError(f"Graph directory not found: {graph_dir}")

    # Load existing CSV if it exists
    if output_file.exists():
        df = pd.read_csv(output_file)
    else:
        df = pd.DataFrame()

    existing = set(
        zip(df.get("graph_type", []), df.get("graph_name", []))
    )

    new_rows = []

    for path in graph_dir.iterdir():
        name = path.stem

        if (graph_type, name) in existing:
            continue  # already in CSV

        G = nx.read_edgelist(path, nodetype=int)

        degrees = [d for _, d in G.degree()]
        amp_file = Path("amplification") / graph_type / f"{name}.txt"
        acc_file = Path("acceleration") / graph_type / f"{name}.txt"

        result = amplification_and_acceleration(amp_file, acc_file)
        #if result is None:
            #continue

        amp, acc = result

        new_rows.append({
            "graph_type": graph_type,
            "graph_name": name,
            "degree_mean": np.mean(degrees),
            "degree_var": np.var(degrees),
            "amp": amp,
            "acc": float(acc),
            "connectivity": nx.algebraic_connectivity(G, method="lanczos", normalized=True),
            "transitivity": nx.transitivity(G), 
            "degree_assortativity": nx.degree_assortativity_coefficient(G)
        })

    if not new_rows:
        print("No new graphs")
        return df

    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(output_file, index=False)

    print(f"Added {len(new_rows)} graphs of type '{graph_type}'")
    return df

def add_degree_assortativity(
    csv_file="params.csv",
    graphs_root="graphs"
):
    """
    Adds NetworkX degree_assortativity_coefficient to an existing params.csv.
    Assumes params.csv has columns: graph_type, graph_name
    """
    csv_file = Path(csv_file)
    df = pd.read_csv(csv_file)

    # Create column if it doesn't exist
    if "degree_assortativity" not in df.columns:
        df["degree_assortativity"] = np.nan

    for idx, row in df.iterrows():
        graph_type = row["graph_type"]
        graph_name = row["graph_name"]

        graph_path = Path(graphs_root) / graph_type / f"{graph_name}.txt"

        if not graph_path.exists():
            print(f"Missing graph file: {graph_path}")
            continue

        try:
            G = nx.read_edgelist(graph_path, nodetype=int)

            assort = nx.degree_assortativity_coefficient(G)

            df.at[idx, "degree_assortativity"] = assort

        except Exception as e:
            print(f"Failed on {graph_type}/{graph_name}: {e}")

    df.to_csv(csv_file, index=False)
    print(f"Updated {csv_file} with degree_assortativity_coefficient")

    return df


def amplification_and_acceleration(amp_file: Path, acc_file: Path):
    amp = 0
    acc = 0
    try:
        with open(amp_file, "r") as f:
            amp = float(f.read().strip())
        with open(acc_file, "r") as f:
            acc = float(f.read().strip())
        return amp, acc
    except FileNotFoundError as e:
        print(f"Missing file: {e.filename}")
        return amp, acc
    
def generate_add(base_dirs, output_file="cons.csv"):
    all_results = []

    for base_dir in base_dirs:
        print(base_dir)
        base_dir = Path(base_dir)

        for path in base_dir.iterdir():
            name = path.stem
            G = nx.read_edgelist(path, nodetype=int)

            degrees = [deg for _, deg in G.degree()]
            degree_variance = np.var(degrees)
            degree_mean = np.mean(degrees)

            typee = base_dir.name

            amp_file = Path("amplification") / typee / f"{name}.txt"
            acc_file = Path("acceleration") / typee / f"{name}.txt"

            result = amplification_and_acceleration(amp_file, acc_file)
            if result is None:
                print(f"Skipping {typee}/{name}")
                continue

            amp, acc = result
            conn = nx.algebraic_connectivity(G, method="lanczos", normalized=True)
            trans = nx.transitivity(G)

            all_results.append({
                "graph_type": typee,
                "graph_name": name,
                "degree_mean": degree_mean,
                "degree_var": degree_variance,
                "amp": amp,
                "acc": float(acc),
                "connectivity": conn,
                "transitivity": trans
            })

    new_df = pd.DataFrame(all_results)

    output_file = Path(output_file)

    if output_file.exists():
        existing_df = pd.read_csv(output_file)
        df = pd.concat([existing_df, new_df], ignore_index=True)

        # avoid duplicate graph entries
        df = df.drop_duplicates(subset=["graph_type", "graph_name"], keep="last")
    else:
        df = new_df

    df = df.set_index("graph_name")
    df.to_csv(output_file, index_label="graph_name")

    print(f"Saved {len(new_df)} new rows. Total rows now: {len(df)}")
    return df

def generate(base_dirs, output_file="cons.csv"):
    all_results = []

    for base_dir in base_dirs:
        print(base_dir)
        base_dir = Path(base_dir)
        for path in base_dir.iterdir():
            #name =  path.stem
            _,_,name = str(path).rsplit("/", 2)
            G = nx.read_edgelist(path, nodetype=int)
            degrees = [deg for _, deg in G.degree()]
            degree_variance = np.var(degrees)
            degree_mean = np.mean(degrees)
            
            typee =  base_dir.name

            """
            amp_file = Path("amplification") / typee / f"{name}.txt"
            acc_file = Path("acceleration") / typee / f"{name}.txt"

            result = amplification_and_acceleration(amp_file, acc_file)
            if result is None:
                print(f"Skipping {typee}/{name}")
                continue
            amp, acc = result
            """
            amp, acc = 0,0
            conn = nx.algebraic_connectivity(G, method="lanczos", normalized=True)
            trans = nx.transitivity(G)
            ass = nx.degree_assortativity_coefficient(G)

            all_results.append({  
                    "graph_type":  typee,               
                    "graph_name": name,
                    "degree_mean" : degree_mean,
                    "degree_var" : degree_variance,
                    "amp" : amp,
                    "acc" : float(acc),
                    "connectivity": conn,
                    "transitivity": trans, 
                    "degree_assortativity": ass
            })
    df = pd.DataFrame(all_results).set_index("graph_name")
    df.to_csv(output_file, index_label="graph_name")
    print(f"Saved {len(df)} total connectivities from {len(base_dirs)} directories to {output_file}")

    return df
"""
for graph in ["bottlenecks_2", "bottlenecks_4", "bottlenecks_regular", "fingers", "grids", "lines_2",  "random_geometric_1", "random_geometric_2", "regular_graphs_4",  "regular_graphs_10", "regular_graphs", "PA"]:
    overwrite_amp(
        csv_file="params.csv",
        graph_type=graph
    )
"""
#dirs = ["graphs/bottlenecks_2", "graphs/bottlenecks_4", "graphs/bottlenecks_regular", "graphs/fingers", "graphs/grids", "graphs/lines_2",  "graphs/random_geometric_1", "graphs/random_geometric_2", "graphs/regular_graphs_4",  "graphs/regular_graphs_10", "graphs/regular_graphs", "graphs/PA"]
#dirs = ["graphs/regular_4_regular_10"]
#df = generate(dirs, output_file="assortative.csv")
#df = generate_add(dirr, output_file="params.csv" )
#add_graph_type_to_csv("PA_assortative")
df = add_degree_assortativity()
"""
overwrite_amp_for_pa_assortative(
    csv_file="params.csv",
    graph_type="PA_assortative"
)
"""



"""
import pandas as pd
from pathlib import Path
import networkx as nx
import numpy as np


def amplification_and_acceleration(amp_file: Path, acc_file: Path):
    with open(amp_file, "r") as f:
        amp = float(f.read().strip())
    with open(acc_file, "r") as f:
        acc = float(f.read().strip())
    return amp, acc


def generate_or_update(
    base_dirs,
    input_csv="graph_params_old.csv",
    output_csv="graph_params.csv",
):
    # Load existing CSV if present
    if Path(input_csv).exists():
        df = pd.read_csv(input_csv, index_col="graph_name")
        print(f"Loaded {len(df)} existing graphs")
    else:
        df = pd.DataFrame()

    for base_dir in base_dirs:
        base_dir = Path(base_dir)
        dir_name = base_dir.name 
        print(f"Processing {dir_name}")

        for path in base_dir.iterdir():
            if not path.is_file():
                continue

            name = path.stem

            amp_file = Path("amplification") / dir_name / f"{name}.txt"
            acc_file = Path("acceleration") / dir_name / f"{name}.txt"

            # Case 1: graph already exists → only update amp/acc
            if name in df.index:
                if amp_file.exists() and acc_file.exists():
                    amp, acc = amplification_and_acceleration(amp_file, acc_file)
                    df.loc[name, "amp"] = amp
                    df.loc[name, "acc"] = acc
                continue

            # Case 2: graph is new → fully compute everything
            G = nx.read_edgelist(path, nodetype=int)

            degrees = [deg for _, deg in G.degree()]
            degree_mean = np.mean(degrees)
            degree_var = np.var(degrees)

            try:
                connectivity = nx.algebraic_connectivity(
                    G, method="lanczos", normalized=True
                )
            except Exception:
                connectivity = np.nan

            transitivity = nx.transitivity(G)

            amp = acc = np.nan
            if amp_file.exists() and acc_file.exists():
                amp, acc = amplification_and_acceleration(amp_file, acc_file)

            df.loc[name] = {
                "degree_mean": degree_mean,
                "degree_var": degree_var,
                "amp": amp,
                "acc": acc,
                "connectivity": connectivity,
                "transitivity": transitivity,
            }

    df.to_csv(output_csv, index_label="graph_name")
    print(f"Saved {len(df)} total graphs to {output_csv}")
    return df


dirs = [
    "graphs/bottlenecks_2",
    "graphs/bottlenecks_4",
    "graphs/bottlenecks_regular",
    "graphs/grids",
    "graphs/lines_2",
    "graphs/fingers",
    "graphs/random_geometric_1",
    "graphs/random_geometric_2",
    "graphs/PA",
    "graphs/regular_graphs_4",
    "graphs/regular_graphs",
    "graphs/regular_graphs_10",
]

df = generate_or_update(dirs)
print(df.head())
"""