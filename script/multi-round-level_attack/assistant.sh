#!/bin/bash
set -e

INPUT_FOLDER="YOUR DATA PATH"
INPUT_KEY="LevelAttack"
OUTPUT_ROOT="results"
MODE="attack"
SUB="multi-round"
SCEN="assistant"

MODELS=("o3-mini-2025-01-31" "gpt-4o" "claude-3.5-haiku-20241022" "gemini-1.5-flash-latest" "gemini-1.5-pro" "gpt-3.5-turbo" "TA/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo" "TA/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo" "TA/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" "doubao-lite-32k-240828" "TA/deepseek-ai/DeepSeek-R1-Distill-Llama-70B" "deepseek-chat" "glm-3-turbo" "glm-4-air" "claude-3-5-sonnet-latest")
FOLDER_NAMES=("o3-mini" "gpt-4o" "claude-3.5-haiku" "gemini-1.5-flash" "gemini-1.5-pro" "gpt-3.5-turbo" "Meta-Llama-3.1-8B-Instruct-Turbo" "Meta-Llama-3.1-70B-Instruct-Turbo" "Meta-Llama-3.1-405B-Instruct-Turbo" "Doubao-lite-32k" "DeepSeek-R1-Distill-Llama-70B" "DeepSeek-V3" "glm-3-turbo" "glm-4" "claude-3-5-sonnet-latest")

START_TIME=$(date +%s)
echo "Processing started at: $(date)"

for MODEL_FOLDER in "$INPUT_FOLDER"/*; do
    if [ -d "$MODEL_FOLDER" ]; then
        FOLDER_BASENAME=$(basename "$MODEL_FOLDER")
        
        MODEL=""
        for i in "${!FOLDER_NAMES[@]}"; do
            if [ "${FOLDER_NAMES[i]}" == "$FOLDER_BASENAME" ]; then
                MODEL="${MODELS[i]}"
                break
            fi
        done
        
        if [ -z "$MODEL" ]; then
            echo "No corresponding model found for folder $FOLDER_BASENAME. Skipping."
            continue
        fi
        
        echo "Processing folder: $MODEL_FOLDER with model: $MODEL"
        
        for FILE in "$MODEL_FOLDER"/FP-base-*.json; do
            if [ -f "$FILE" ]; then
                BASENAME=$(basename -- "$FILE")
                
                OUTPUT_FILE="./${OUTPUT_ROOT}/multi-round-${INPUT_KEY}/${SCEN}/${MODEL}/${BASENAME%.json}.json"
                
                mkdir -p "$(dirname "$OUTPUT_FILE")"
                
                echo "Processing file: $FILE with model: $MODEL"
                
                python main.py --question_input_path "$FILE" \
                               --answer_save_path "$OUTPUT_FILE" \
                               --model "$MODEL" \
                               --mode "$MODE" \
                               --attack_type "$INPUT_KEY" \
                               --sub_task "$SUB" \
                               --scenario "$SCEN" &
            fi
        done
    fi
done

wait

END_TIME=$(date +%s)
echo "All files processed."
echo "Total processing time: $((END_TIME - START_TIME)) seconds."
