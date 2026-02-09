#include "lrd2d.h"
#include <cassert>
#include <sstream>
#include <limits>

latticeLongRangeSim::latticeLongRangeSim(int dim, double decay,
                                         lint /*finalsize*/, bool colored, lint lattSize)
: d(2), mu(decay), sites(static_cast<unsigned int>(lattSize)),
  isColored(colored), sumsq(Point(2)) {

    rand01    = std::uniform_real_distribution<double>(0,1);
    randm11   = std::uniform_real_distribution<double>(-1,1);
  }


quantizedPoint latticeLongRangeSim::randomNeighbor(quantizedPoint& origin, qpDict& network) {
    auto &neighbors = network[origin];
    assert(!neighbors.empty() && "randomNeighbor called on isolated node (degree 0)");   

    int idx = std::uniform_int_distribution<>(
    0, static_cast<int>(neighbors.size()) - 1
    )(rng);
    quantizedPoint pick = neighbors[idx];

    accesscounts[pick] += 1;
    return pick;
}


std::pair<quantizedPoint,int> latticeLongRangeSim::randomPoint() 
{ int ridx = randomIndex(); return std::make_pair(pointByIdx(ridx) ,colorByIdx(ridx)); } ///added pointByIdx??

// access functions
quantizedPoint latticeLongRangeSim::pointByIdx(int idx) {
    return siteidxs[static_cast<std::size_t>(idx)];
}

color latticeLongRangeSim::colorByIdx(int idx) {
    return sites.colorAtPoint(siteidxs[static_cast<std::size_t>(idx)]);
}

bool latticeLongRangeSim::addPoint(quantizedPoint newpt, color newcolor, double time) {
    if (sites.insert(newpt, newcolor)) {
        siteidxs.push_back(newpt);
        assert(sites.size() == siteidxs.size());
        times.push_back(time);
        return true;
    }
    return false;
}

lint latticeLongRangeSim::N() {
    return sites.size();
}

color latticeLongRangeSim::netColor() {
    color nc = 0;
    for (lint i = 0; i < N(); i++) nc += colorByIdx(static_cast<int>(i));
    return nc;
}

int latticeLongRangeSim::randomIndex() {
    return std::uniform_int_distribution<>(0, static_cast<int>(N()) - 1)(rng);
}

quantizedPoint latticeLongRangeSim::randomEmptyPoint() {
    indextype idx = sites.emptyptlongAtPos(std::uniform_int_distribution<>(0, static_cast<int>(sites.Nempty()) - 1)(rng));
    
    return sites.idxtopt(idx); // identity
}



double latticeLongRangeSim::Rg() {
    // Keep your existing definition (sumsq not updated in this snippet).
    return std::sqrt(sumsq.sum() / std::max<lint>(1, N()));
}

color latticeLongRangeSim::randomTwoColor(double frac) {
    return rand01(rng) < frac;
}

int latticeLongRangeSim::num_occurs(int n, double prob) {
    int num =0;
    for (int i = 0; i < n; ++i) {
        if (rand01(rng) < prob) {
            num++;
        }
    }
    return num;
}


// read-write functions


