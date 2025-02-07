#!/bin/bash

# 设置输入文件夹
INPUT_FOLDER="./dataset/baseline"
INPUT_KEY="baseline"
OUTPUT_ROOT="results"


# 设置模型列表
MODELS=("o3-mini-2025-01-31")
#MODELS=("o3-mini-2025-01-31" "qwen2.5-3b-instruct" "qwen2.5-7b-instruct" "qwen2.5-14b-instruct" "qwen2.5-32b-instruct" "qwen2.5-72b-instruct")


# 遍历文件夹中的每个 JSON 文件
for FILE in "$INPUT_FOLDER"/*.json; do
    if [ -f "$FILE" ]; then
        # 获取文件名（不含路径）
        BASENAME=$(basename -- "$FILE")
        
        # 遍历每个模型并运行 Python 脚本
        for MODEL in "${MODELS[@]}"; do
            echo "Processing $FILE with model $MODEL..."
            # 生成输出文件名（在文件名后添加 "_result"）
            OUTPUT_FILE="./${OUTPUT_ROOT}/${INPUT_KEY}/${MODEL}/${BASENAME%.json}-result.json"

            # 确保输出目录存在
            mkdir -p "$(dirname "$OUTPUT_FILE")"

            # 运行 Python 脚本并在后台执行
            python main.py --question_input_path "$FILE" --model "$MODEL" --answer_save_path "$OUTPUT_FILE" --mode attack --task_type baseline &
        done
    fi
done

# 等待所有后台任务完成
wait

echo "All files processed."

