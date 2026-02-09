#include "popl.hpp"
#include <random>
#include <iostream>
#include <iomanip>
#include <map>
#include "lrd2d.h"

#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <filesystem>
#include <cassert>


using namespace popl;

// weights are over flat sites [0, L^d)
using weightMap = std::map<double, int>;  // key: cumulative length, value: quantizedPoint (int)

double P_BARE = 1;
int lastcolor = 0;
weightMap weights;

double lastweightKey = 0.0;

void addToEnd(int pt, double length) {
    if (weights.empty()) {
        weights[length] = pt;
        lastweightKey = length;
        return;
    }
    auto it = weights.end();
    --it;
    double newKey = it->first + length;
    weights[newKey] = pt;
    lastweightKey = newKey;
}


void print_weights() {
    for (auto it = weights.begin(); it != weights.end(); ++it) {
        std::cout << it->first << ' ' << it->second << '\n';
    }
}

void initialize_weights(latticeLongRangeSim &sim, double weight) {
    // Give every site an initial weight segment of length `weight`
    const long long total = sizeof(sim.network);
    for (long long i = 0; i < total; ++i) {
        addToEnd(static_cast<int>(i), weight);
    }
}

// Reset access counts for all nodes in the current network
void initialize_counts(latticeLongRangeSim &sim) {
    qpIntDict accesscountstemp;
    for (const auto &pair : sim.network) {
        accesscountstemp[pair.first] = 0;
    }
    sim.accesscounts = std::move(accesscountstemp);
}


// Read adjacency list where file is flat indices, like: "key n1 n2 n3 ..."
/*
qpDict initialize_network(int num) {
    std::ifstream inFile("param_graphs/" +  std::to_string(num)+ ".txt");

    qpDict adjList;
    std::string line;

    while (std::getline(inFile, line)) {
        std::istringstream iss(line);
        int key;
        if (!(iss >> key)) continue;

        std::vector<quantizedPoint> neighbors;
        int neighbor_flat;
        while (iss >> neighbor_flat) {
            neighbors.push_back(neighbor_flat);
        }
        adjList[key] = std::move(neighbors);
    }

    inFile.close();
    return adjList;
}
*/

qpDict initialize_network(std::string out_file, std::string name) {
    std::ifstream inFile(out_file + "/" + name + ".txt");
    if (!inFile) {
        throw std::runtime_error("Could not open edge list file: " + name);
    }

    qpDict adjList;  // e.g., std::unordered_map<int, std::vector<quantizedPoint>>

    std::string line;
    int u, v;

    while (std::getline(inFile, line)) {
        // skip empty lines and comments
        if (line.empty() || line[0] == '#') continue;

        std::istringstream iss(line);
        if (!(iss >> u >> v)) {
            // malformed line, skip (or throw if you prefer strict parsing)
            continue;
        }

        // Add both directions since it's an undirected graph.
        adjList[u].push_back(static_cast<quantizedPoint>(v));
        adjList[v].push_back(static_cast<quantizedPoint>(u));
    }
    return adjList;
}

weightMap::iterator randomFromWeights(latticeLongRangeSim &sim) {
    // pick uniformly in [0, lastweightKey)
    double randomKey = sim.rand01(sim.rng) * lastweightKey;
    return weights.upper_bound(randomKey);
}

// Find the iterator corresponding to a given flat site `pt` when every site’s
// segment length is `weight`. The segment center is at (pt + 0.5) * weight.
weightMap::iterator weight_position(int pt, double weight) {
    const double center = (static_cast<double>(pt) + 0.5) * weight;
    return weights.lower_bound(center);
}

// Mark a weighted entry as “claimed” (store negative index) and add a new segment
void addNewMutation(latticeLongRangeSim &sim, weightMap::iterator basept, int color, double mutrate) {
    sim.addPoint(basept->second, color);                 // occupy site with new color
    basept->second = -static_cast<int>(sim.sites.size()); // mark as linked to current index
    addToEnd(basept->second, P_BARE - mutrate);          // append new weight segment
}

bool tryCopyMutation(latticeLongRangeSim &sim, int newpt, int color, double mutrate) {
    if (sim.addPoint(newpt, color)) {
        int newidx = static_cast<int>(sim.sites.size());
        auto it = weight_position(newpt, mutrate);
        if (it != weights.end()) {
            it->second = -newidx;    // mark source weight slot
        }
        int marker = -newidx;
        addToEnd(marker, P_BARE - mutrate);
        return true;
    }
    return false;
}

// Populate a disk of radius diameter/2 around the center for d == 2,
// using flat indices. (For other d, adjust as needed.)

void saveToTxt(const std::string& filename, const std::vector<std::vector<double>>& data) {
    std::ofstream out(filename);
    if (!out) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return;
    }

    for (const auto& row : data) {
        for (size_t i = 0; i < row.size(); ++i) {
            out << std::setprecision(8) << row[i];
            if (i < row.size() - 1)
                out << " ";
        }
        out << "\n";
    }
    out.close();
}

int main(int argc, char* argv[]) {
    namespace fs = std::filesystem;
    //namespace fs = std::__fs::filesystem;
    OptionParser op("Allowed options");
    auto help_option    = op.add<Switch>("h","help","produce help message");
    auto d_option       = op.add<Value<int>>("d","d","dimension", 2);
    auto seed_option    = op.add<Value<int>>("s","seed","random number seed", -1);
    auto mutrate_option = op.add<Value<double>>("u","mutrate","mutation rate", 0.);
    auto file = op.add<Value<std::string>>("f","file", "file name", "");
    auto graph_type = op.add<Value<std::string>>("g","graph", "graph_file", "");

    op.parse(argc, argv);

    int d  = d_option->value();
    int seed  = seed_option->value();
    std::string graph = file->value();
    double mutrate = mutrate_option->value();
    std::string type = graph_type->value();

    std::string out_dir = type + "_output";
    fs::create_directories(out_dir);  // safe if multiple jobs call it
    std::string summary_filename = out_dir + "/" + graph + "_" + std::to_string(mutrate) + ".txt";
    std::ofstream summary(summary_filename);

double avg_match_prob = 0.0;
double avg_lastcolor  = 0.0;
int avg_count = 0;

for (int i = 0; i < 100000; i++) {
    // Reset globals
    weights.clear();
    lastweightKey = 0.0;
    lastcolor = 0;

    int seed  = seed_option->value();
    if (seed < 0) {
        std::random_device rd;
        seed = rd();
    }

    qpDict adjList = initialize_network(type, graph);
    int n = adjList.size();

    for (int i = 0; i < n; ++i) {
        assert(adjList.count(i) == 1 && "Graph nodes must be labeled 0..n-1 with no gaps");
    }   

    latticeLongRangeSim lrs = latticeLongRangeSim(d, 0, n, true, n);
    lrs.network = std::move(adjList);
    lrs.rng.seed(seed);

    // Add dummy zero-length seed weight
    addToEnd(0, 0.0);

    if (mutrate > 0) initialize_weights(lrs, mutrate);

    if (mutrate == 0) {
        std::cerr << " bad initialization (nonstarter)" << std::endl;
        return 0;
    }

    // Process simulation as before...
    while (lrs.N() < n) {
        bool mutateNotJump = lrs.randomTwoColor(mutrate * (n - lrs.N()) / lrs.N()); //want to double check right equation
        bool addedPoint = false; 

        if (mutateNotJump) { 
            int newmutpt = lrs.randomEmptyPoint();
            addedPoint = lrs.addPoint(newmutpt, lastcolor++);
        } else {
            auto randompt = lrs.randomPoint();
            int newpt = lrs.randomNeighbor(randompt.first, lrs.network);
            addedPoint = lrs.addPoint(newpt, randompt.second);
        }
    }

    std::map<color, int> clonect;
    for (int i = 0; i < lrs.N(); i++)
        clonect[lrs.colorByIdx(i)]++;

    double match_prob = 0.0;
    int total = lrs.N();
    for (const auto &elem : clonect) {
        double freq = static_cast<double>(elem.second) / total;
        match_prob += freq * freq;
    }

    avg_count++;

    avg_match_prob += (match_prob - avg_match_prob) / avg_count;
    avg_lastcolor  += (static_cast<double>(lastcolor) - avg_lastcolor) / avg_count;
  
}
    summary << std::setprecision(11)
        << "average probability of softsweep: " << 1 - avg_match_prob << "\n"
        << "average num clones:  " << avg_lastcolor  << "\n";
    summary.close();

}
