#!/bin/bash
set -e

# 设置输入文件夹和输出根目录
INPUT_FOLDER="./dataset/FP-base"
INPUT_KEY="base"
OUTPUT_ROOT="results"
MODE="attack"

# 设置模型列表
#MODELS=("TA/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo" "TA/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo" "TA/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" "o3-mini-2025-01-31" "gpt-4o" "qwen2.5-7b-instruct" "qwen2.5-14b-instruct" "qwen2.5-32b-instruct" "qwen2.5-72b-instruct")
MODELS=("TA/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo")

# 记录开始时间
START_TIME=$(date +%s)
echo "Processing started at: $(date)"

# 遍历输入文件夹中的每个 JSON 文件
for FILE in "$INPUT_FOLDER"/*.json; do
    if [ -f "$FILE" ]; then
        # 获取不含路径的文件名
        BASENAME=$(basename -- "$FILE")
        
        # 遍历每个模型并运行 Python 脚本
        for MODEL in "${MODELS[@]}"; do
            echo "Processing file: $FILE with model: $MODEL"
            # 构造输出文件路径（在原文件名后添加 "-result"）
            OUTPUT_FILE="./${OUTPUT_ROOT}/${INPUT_KEY}/${MODEL}/${BASENAME%.json}-result.json"

            # 确保输出目录存在
            mkdir -p "$(dirname "$OUTPUT_FILE")"

            # 调用 Python 脚本，后台执行任务
            python main.py --question_input_path "$FILE" \
                           --answer_save_path "$OUTPUT_FILE" \
                           --model "$MODEL" \
                           --mode "$MODE" \
                           --task_type "$INPUT_KEY" &
        done
    fi
done

# 等待所有后台任务完成
wait

END_TIME=$(date +%s)
echo "All files processed."
echo "Total processing time: $((END_TIME - START_TIME)) seconds."
