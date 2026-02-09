# Simulation code associated with manuscript _Spatial soft sweeps: patterns of adaptation in
populations with long-range dispersal_

## Description

This code generates computer programs that simulate spatial soft sweeps with
long-distance dispersal events, as described in the Methods section of the
manuscript _Spatial soft sweeps: patterns of adaptation in populations with
long-range dispersal_ by Jayson Paulose, Joachim Hermisson, and Oskar
Hallatschek. The code is intended to allow scientific results to be checked and
reproduced. Please let the authors know if the code finds use in other contexts.

## Compilation

The code has been written in `C++` under the `C++11` standard. It has been
tested on `GNU g++ 7.3.0`.

Dependencies: 

 - `BOOST C++` libraries (tested on version 1.65)
 - `GNU Scientific Library` (tested on version 2.4)
	
The header files for the above dependencies must be on the include path of the
compiler.

A `Makefile` has been provided for use with `GNU Make`. The two executables
`spatialsoft1d` and `spatialsoft2d` for linear and planar habitats respectively can
be compiled by executing the commands `make spatialsoft1d` and `make spatialsoft2d`.


## Execution

The commands below work for both `spatialsoft1d` and `spatialsoft2d`. Parameters
are passed to the program using command-line arguments with flags, defined
below. See accompanying manuscript for parameter definitions.


**Flag**     | **Definition**
-------------|--------------------------------------------------------------------------
`--help`     | List command-line arguments
`--L`        | Set linear range size $L$
`--mutrate`  | Set rescaled mutation rate $\tilde{u}$
`--mu`       | Set dispersal kernel exponent $\mu$
`--seed`     | Set seed for random number generator (if none provided, uses random seed)

### Examples:

 - `spatialsoft1d --L 1000 --mu 1.2 --mutrate 0.0001`: Run a 1d soft sweep with
   $L=1000$, $\mu = 1.2$, $\tilde{u} = 0.0001$, and a seed generated at random
 - `spatialsoft2d --L 1000 --mu 2 --mutrate 1e-5 --seed 27`: Run a 2d soft sweep with
   $L=1000$, $\mu = 2$, $\tilde{u} = 0.00001$, and random number generator
   initialized to 27 (repeating the command with the same parameters and seed
   generates exactly the same output).


## Output

The final state of the simulation after the soft sweep has completed (i.e. every
deme has acquired a mutation) is output to `stdout` as follows:

 - `spatialsoft1d`: Output has $L$ rows with three columns. Each row represents a
   deme; rows are ordered by the order of colonization of demes. In each row,
   the first column represents the deme position in the 1D range (an integer
   between 0 and $L-1$); the second column represents the clone identity of the
   deme (an integer between 0 and $n-1$ for $n$ unique clones in the final
   state); the third column represents the time of colonization.
 - `spatialsoft2d`: Output has $L^2$ rows with three columns. Each row represents a
   deme; rows are ordered by the order of colonization of demes. In each row,
   the first two columns represents the deme position in $L\times L$ lattice (an integer
   between 0 and $L-1$ in each dimension); the third column represents the clone identity of the
   deme (an integer between 0 and $n-1$ for $n$ unique clones in the final
   state).
   
After the raw range output, a summary line prefixed with a `#` displays the
final size (number of demes) and the number $n$ of unique clones.

## Licence
Copyright (c) 2018 Jayson Paulose

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. 

If use of the Software or derived works leads to scientific publications, the
associated manuscript shall be cited in the publication.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
