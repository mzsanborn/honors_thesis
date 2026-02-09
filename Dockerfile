FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt update && apt install -y \
    build-essential \
    g++ \
    libboost-program-options-dev \
    libgsl-dev \
    && apt clean

# Set workdir
WORKDIR /app

# Copy source files
COPY . .

# Compile static binary
RUN g++ spatialsoft2d.cpp lrd2d.cpp -o spatialsoft2d\
    -std=c++17 -O3 -static \
    -lboost_program_options -lgsl -lgslcblas -lstdc++fs

    