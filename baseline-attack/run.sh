#!/bin/bash

# 设置输入文件夹
INPUT_FOLDER="../dataset/FP-base"

# 设置模型列表
# MODELS=("gpt-4o-mini" "gpt-4o")
MODELS=("qwen2.5-72b-instruct") #3b, 7b的chinese没跑完, 32b english没跑完

# 遍历文件夹中的每个 JSON 文件
for FILE in "$INPUT_FOLDER"/*.json; do
    if [ -f "$FILE" ]; then
        # 获取文件名（不含路径）
        BASENAME=$(basename -- "$FILE")
        
        # 遍历每个模型并运行 Python 脚本
        for MODEL in "${MODELS[@]}"; do
            echo "Processing $FILE with model $MODEL..."
            # 生成输出文件名（在文件名后添加 "_result"）
            OUTPUT_FILE="./fp_base_result/${MODEL}/${BASENAME%.json}-result.json"

            # 确保输出目录存在
            mkdir -p "$(dirname "$OUTPUT_FILE")"

            # 运行 Python 脚本并在后台执行
            python ./attacking.py --input_file "$FILE" --model "$MODEL" --output_file "$OUTPUT_FILE" &
        done
    fi
done

# 等待所有后台任务完成
wait

echo "All files processed."

