#!/bin/bash
set -e

# 设置输入文件夹和输出根目录
INPUT_FOLDER="results/demo"
INPUT_KEY="LevelAttack"
MODE="attack"
SUB="one-round-eval"
MODEL="Default"

# 记录开始时间
START_TIME=$(date +%s)
echo "Processing started at: $(date)"

# 如果只想处理一个文件夹，可以 leave as-is.
# 如果需要遍历多个子目录，请 uncomment the next line and comment out the for-loop below.
# for sub_dir in "$INPUT_FOLDER"/*; do

# For a single folder:
for sub_dir in "$INPUT_FOLDER"/*; do
    if [ -d "$sub_dir" ]; then
    # 遍历当前文件夹中的每个 JSON 文件
        for FILE in "$sub_dir"/*.json; do
            if [ -f "$FILE" ]; then
                echo "Processing file: $FILE with model: $MODEL"
                # 调用 Python 脚本，后台执行任务
                python main.py --question_input_path "$FILE" \
                                --answer_save_path "$FILE" \
                                --model "$MODEL" \
                                --mode "$MODE" \
                                --task_type "$INPUT_KEY" \
                                --sub_task "$SUB" &
            fi
        done
    fi
done

# 等待所有后台任务完成
wait

END_TIME=$(date +%s)
echo "All files processed."
echo "Total processing time: $((END_TIME - START_TIME)) seconds."
