#!/bin/bash
# run_experiments.sh
# Automatically runs ./main on all input files in random_geometric/

# --- Fixed Parameters ---
EXECUTABLE="./main"
INT_PARAM_1="100000"
FLOAT_PARAM_1="0.001"

# --- Input / Output Directories ---
INPUT_DIR="random_geometric"
OUTPUT_ROOT_DIR="amp_acc"

# Ensure output root exists
mkdir -p "$OUTPUT_ROOT_DIR"

echo "Starting batch execution of $EXECUTABLE"
echo "-------------------------------------"

# Loop over all .txt files in the input directory
for INPUT_FILE in "$INPUT_DIR"/*.txt; do
    # Skip if no files match
    [ -e "$INPUT_FILE" ] || continue

    # Construct output prefix: amp_acc/random_geometric/filename.txt
    DYNAMIC_PREFIX="$OUTPUT_ROOT_DIR/$INPUT_FILE"

    # Create necessary output directories
    OUTPUT_DIR_PATH=$(dirname "$DYNAMIC_PREFIX")
    mkdir -p "$OUTPUT_DIR_PATH"

    # Print the command
    echo "Running command:"
    echo "$EXECUTABLE $INPUT_FILE $DYNAMIC_PREFIX $INT_PARAM_1 $FLOAT_PARAM_1"

    # Run the executable
    "$EXECUTABLE" "$INPUT_FILE" "$DYNAMIC_PREFIX" "$INT_PARAM_1" "$FLOAT_PARAM_1"

    # Check result
    if [ $? -eq 0 ]; then
        echo "--> SUCCESS: $(basename "$INPUT_FILE")"
    else
        echo "--> ERROR: $(basename "$INPUT_FILE") run failed."
    fi

    echo "-------------------------------------"
done

echo "Batch execution complete."