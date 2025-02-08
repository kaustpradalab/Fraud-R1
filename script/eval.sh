#!/bin/bash

# 设置输入文件夹
EVAL_FOLDER="./results/baseline"
OUTPUT_FILE="./results/eval/asr_baseline.xlsx"

python main.py --eval_input_folder "$EVAL_FOLDER"  --eval_output_file "$OUTPUT_FILE" --mode eval