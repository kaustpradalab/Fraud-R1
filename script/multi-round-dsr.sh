#!/bin/bash
set -e

INPUT_FOLDER="results/multi-round-LevelAttack"
OUTPUT_Folder="results/multi-round-score"
MODE="eval"
EVAL_TYPE="multi-round"

mkdir -p "$(dirname "$OUTPUT_FILE")"

python main.py --eval_input_folder "$INPUT_FOLDER" \
                           --eval_output_file "$OUTPUT_Folder" \
                           --mode "$MODE" \
                           --eval_type "$EVAL_TYPE"