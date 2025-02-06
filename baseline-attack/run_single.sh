#!/bin/bash

# 设置输入文件夹
cn="../dataset/FP-base/FP-base-Chinese.json"
en="../dataset/FP-base/FP-base-English.json"

# 定义模型变量
declare -A MODELS
MODELS["3b"]="qwen2.5-3b-instruct"
MODELS["7b"]="qwen2.5-7b-instruct"
MODELS["32b"]="qwen2.5-32b-instruct"

# 遍历模型
for key in "${!MODELS[@]}"; do
    MODEL_NAME="${MODELS[$key]}"
    
    cn_OUTPUT_FILE="./fp_base_result/${MODEL_NAME}/FP-base-Chinese-result.json"
    en_OUTPUT_FILE="./fp_base_result/${MODEL_NAME}/FP-base-English-result.json"

    mkdir -p "$(dirname "$cn_OUTPUT_FILE")"  # 确保目录存在
    mkdir -p "$(dirname "$en_OUTPUT_FILE")"

    if [[ "$key" == "3b" || "$key" == "7b" ]]; then
        python ./attacking.py --input_file "$cn" --model "$MODEL_NAME" --output_file "$cn_OUTPUT_FILE" &
    fi

    if [[ "$key" == "32b" ]]; then
        python ./attacking.py --input_file "$en" --model "$MODEL_NAME" --output_file "$en_OUTPUT_FILE" &
    fi
done

# 等待所有后台进程完成
wait

echo "All files processed."

