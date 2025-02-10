#!/bin/bash
set -e

# 设置输入文件夹和输出根目录
INPUT_FOLDER="./dataset/FP-base"
INPUT_KEY="FP-level"
OUTPUT_ROOT="./dataset"
MODE="data"

# 记录开始时间
START_TIME=$(date +%s)
echo "Processing started at: $(date)"

# 遍历输入文件夹中的每个 JSON 文件
for FILE in "$INPUT_FOLDER"/*.json; do
    if [ -f "$FILE" ]; then
        # 获取不含路径的文件名
        BASENAME=$(basename -- "$FILE")
        
        # 构造输出文件路径（在原文件名后添加 "-result"）
        OUTPUT_FILE="./${OUTPUT_ROOT}/${INPUT_KEY}/${BASENAME%.json}.json"

        # 确保输出目录存在
        mkdir -p "$(dirname "$OUTPUT_FILE")"

        # 调用 Python 脚本，后台执行任务
        python main.py --question_input_path "$FILE" \
                        --answer_save_path "$OUTPUT_FILE" \
                        --mode "$MODE" 
    fi
done

END_TIME=$(date +%s)
echo "All files processed."
echo "Total processing time: $((END_TIME - START_TIME)) seconds."
