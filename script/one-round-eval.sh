#!/bin/bash
set -e

INPUT_FOLDER="YOUR RESULT PATH"
INPUT_KEY="LevelAttack"
MODE="attack"
SUB="one-round-eval"
MODEL="Default"

START_TIME=$(date +%s)
echo "Processing started at: $(date)"


# For a single folder:
for sub_dir in "$INPUT_FOLDER"/*; do
    if [ -d "$sub_dir" ]; then
        for sub_sub_dir in "$sub_dir"/*; do
            if [ -d "$sub_sub_dir" ]; then
                for FILE in "$sub_sub_dir"/*.json; do
                    if [ -f "$FILE" ]; then
                        echo "Processing file: $FILE with model: $MODEL"
                        python main.py --question_input_path "$FILE" \
                                        --answer_save_path "$FILE" \
                                        --model "$MODEL" \
                                        --mode "$MODE" \
                                        --attack_type "$INPUT_KEY" \
                                        --sub_task "$SUB" &
                    fi
                done
            fi
        done
    fi
done

wait

END_TIME=$(date +%s)
echo "All files processed."
echo "Total processing time: $((END_TIME - START_TIME)) seconds."
