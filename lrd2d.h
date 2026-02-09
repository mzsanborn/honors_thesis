#ifndef LRD_H
#define LRD_H

#include <vector>
#include <set>
#include <unordered_map>
#include <random>
#include <numeric>
#include <cmath>
#include <iostream>
#include <fstream>
#include <cstdio>
#include <algorithm>
#include <map>
#include <valarray>

typedef std::valarray<double> Point;
typedef std::vector<Point>    PointArray;

#ifdef LONGINTARRAY
typedef long lint;
#define ptround(arg) std::lround(arg)
#else
typedef int  lint;
#define ptround(arg) std::round(arg)
#endif

// Each lattice site is uniquely identified by a single integer [0 .. L*L-1]
typedef int quantizedPoint;

typedef int color;
typedef std::vector<color> colorArray;

// Keyed by flat site ids
typedef std::map<quantizedPoint, std::vector<quantizedPoint>> qpDict;
typedef std::map<quantizedPoint, int>                         qpIntDict;

typedef std::size_t indextype;
typedef std::pair<quantizedPoint, color> qpColorPair;
typedef std::pair<color,indextype>       colorIndexPair;
typedef std::vector<indextype>           indexList;
typedef std::vector<colorIndexPair>      colorList;

#define EMPTY_CELL -1

class quantizedPointArray {
private:
    std::vector<int> colors;   // color per site; EMPTY_CELL => unoccupied
    std::vector<int> empties;  // compact list of CURRENTLY empty site IDs
    std::vector<int> pos_of;   // pos_of[site] = index in 'empties', or -1 if occupied
    indextype N;               // occupied count

public:
    using iterator = void*;            // kept only for API compatibility
    using const_iterator = const void*;

    void* begin() { return nullptr; }
    void* end()   { return nullptr; }

    // Construct a pool with 'total_sites' sites (0..total_sites-1), all empty.
    explicit quantizedPointArray(std::size_t total_sites)
        : colors(total_sites, EMPTY_CELL),
          empties(total_sites),
          pos_of(total_sites),
          N(0) {
        for (std::size_t i = 0; i < total_sites; ++i) {
            empties[i] = static_cast<int>(i);
            pos_of[i]  = static_cast<int>(i);
        }
    }

    // --- basic stats ---
    indextype size()   { return N; }                    // # occupied
    indextype capacity() const { return colors.size(); } // # total sites
    indextype Nempty() { return empties.size(); }       // # empty

    // --- queries ---
    color colorAtPoint(const quantizedPoint &pt) const {
        return colors[static_cast<std::size_t>(pt)];
    }

    // Kept for compatibility (treat 'idx' as site id)
    color colorAtIdx(const indextype idx) const {
        return colors[static_cast<std::size_t>(idx)];
    }

    // Return the site id stored at position 'k' in the empties array
    indextype emptyptlongAtPos(indextype k) const {
        return static_cast<indextype>(empties[static_cast<std::size_t>(k)]);
    }

    // --- mutation ---
    // Insert color at site 'pt'. Returns false if already occupied.
    bool insert(quantizedPoint pt, color newcolor) {
        std::size_t s = static_cast<std::size_t>(pt);
        if (colors[s] != EMPTY_CELL) return false;  // occupied

        colors[s] = newcolor;                        // occupy

        // remove from 'empties' in O(1) via swap-with-last
        int pos = pos_of[s];
        if (pos != -1) {
            int last_idx  = static_cast<int>(empties.size()) - 1;
            int last_site = empties[static_cast<std::size_t>(last_idx)];

            std::swap(empties[static_cast<std::size_t>(pos)],
                      empties[static_cast<std::size_t>(last_idx)]);
            pos_of[last_site] = pos;

            empties.pop_back();
            pos_of[s] = -1;                         // mark as occupied
        }

        ++N;
        return true;
    }

    // Identity (kept for API symmetry with old code)
    quantizedPoint idxtopt(const indextype idx) const {
        return static_cast<int>(idx);
    }
};

typedef std::vector<quantizedPointArray::iterator> quantizedPointIteratorArray;

class latticeLongRangeSim {
public:
    int    d;     // kept for compatibility; implementation assumes d=2 for geometry tasks
    double mu;

    quantizedPointArray           sites;
    std::vector<quantizedPoint>   siteidxs;  // flat ids in insertion order
    std::vector<double>           times;

    bool  isColored;
    Point sumsq;

    qpDict    network;      // adjacency keyed by flat id
    qpIntDict accesscounts; // per-node counters

    std::uniform_real_distribution<double> rand01, randm11;
    std::uniform_int_distribution<>        randintFlat; // 0..L*L-1 when L>0 else full int range
    std::mt19937 rng;

    latticeLongRangeSim(int dim=2, double decay=1.,
                        lint finalsize=1000, bool colored=false, lint lattSize=-1);

    void set_seed(int seed) { rng.seed(seed); }

    // topology
    inline static int wrap_mod(int x, int m) {
        int r = x % m;
        return (r < 0) ? (r + m) : r;
    }



    // generation & access
    quantizedPoint randomLatticePoint();
    quantizedPoint GenerateLevyFlight();

    quantizedPoint randomEmptyPoint();
    std::pair<quantizedPoint,int> randomPoint();     // {flat, color}
    std::pair<quantizedPoint,int> randomPoint(int);  // by color

    quantizedPoint randomNeighbor(quantizedPoint&, qpDict&);

    int  randomIndex();
    int  randomIndex(int col);

    lint N();
    color netColor();

    bool addPoint(quantizedPoint, color=0, double time=0.);
    int  populateHomeland(int diameter, int ncolor);

    double Rg();

    void wrap(quantizedPoint&);

    // access functions
    quantizedPoint pointByIdx(int);
    color          colorByIdx(int);

    // random colors
    color randomTwoColor(double);
    int num_occurs(int,double);

    // I/O
    void readfile(std::string initfile, bool isColored=false);
    void output(std::ostream& outstream=std::cout);
};

void output_site_freq_spectrum(latticeLongRangeSim &sim, int nbins=100, bool logbin=false);

#endif /* LRD_H */