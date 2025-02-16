#!/bin/bash
set -e

INPUT_FOLDER="YOUR DATA PATH"
INPUT_KEY="LevelAttack"
OUTPUT_ROOT="results"
MODE="attack"
SUB="one-round"
SCEN="assistant"

#MODELS=("o3-mini-2025-01-31" "TA/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo" "TA/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo" "TA/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" "qwen2.5-7b-instruct" "qwen2.5-14b-instruct" "qwen2.5-32b-instruct" "qwen2.5-72b-instruct")
MODELS=("qwen2.5-72b-instruct")

START_TIME=$(date +%s)
echo "Processing started at: $(date)"

for FILE in "$INPUT_FOLDER"/*.json; do
    if [ -f "$FILE" ]; then
        BASENAME=$(basename -- "$FILE")

        for MODEL in "${MODELS[@]}"; do
            echo "Processing file: $FILE with model: $MODEL"
            OUTPUT_FILE="./${OUTPUT_ROOT}/one-round-${INPUT_KEY}/${SCEN}/${MODEL}/${BASENAME%.json}.json"

            mkdir -p "$(dirname "$OUTPUT_FILE")"

            python main.py --question_input_path "$FILE" \
                           --answer_save_path "$OUTPUT_FILE" \
                           --model "$MODEL" \
                           --mode "$MODE" \
                           --attack_type "$INPUT_KEY" \
                           --sub_task "$SUB" \
                           --scenario "$SCEN" &
        done
    fi
done

wait

END_TIME=$(date +%s)
echo "All files processed."
echo "Total processing time: $((END_TIME - START_TIME)) seconds."
