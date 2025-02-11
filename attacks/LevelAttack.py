import os
import json
from tqdm import tqdm
from attacks.Attack import Attack
from attacks.attack_utils.GPTCheck import GPTCheck 
from attacks.attack_utils.PromptStorage import start_prompt, more_prompt
import time 

class LevelAttack(Attack):
    def __init__(self, file_name, model, output_file, task, scenario):
        super().__init__()
        self.model = model
        self.output_file = output_file
        self.file_name = file_name
        self.task = task
        self.scenario = scenario

    def process_fraud_data(self):
        """
        主函数：加载数据，确定起始处理位置，并根据任务类型分别调用 process_one_round 或 process_multi_round
        """
        if not self.file_name.endswith(".json"):
            return

        with open(self.file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 根据任务确定存储 response 的键名
        if self.task == "one-round":
            print("Processing one-round attacking now~")
            model_response_key = "one-round response"
        elif self.task == "multi-round":
            print("Processing multi-round attacking now~")
            model_response_key = "multi-round response"
        elif self.task == "one-round-eval":
            print("Processing one-round GPT checking now~")
            model_response_key = "one-round judge"
        else:
            print("unknown task")
            return

        # 如果文件中存在已处理的条目（包含 model_response_key），
        # 则选择其中任意一个作为起点，下面选择第一个出现的条目的索引
        for index, entry in tqdm(enumerate(data), total=len(data)):
            if model_response_key in entry:
                print(f"跳过第 {index} 项，因为已存在 '{self.model_response_key}'。")
                continue
            else:
                print(f"正在处理第 {index} 项...")
            self.process_one_round(entry)
            if self.task == "one-round":
                self.process_one_round(entry)
            elif self.task == "multi-round":
                self.process_multi_round(entry)
            elif self.task == "one-round-eval":
                self.process_one_round_judge(entry)
            
            # 每处理一个条目后写入文件，防止中断导致数据丢失
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    
    def process_one_round_judge(self, entry):
        checker = GPTCheck()
        language = entry.get("language")
        response_content = entry.get("one-round response")

        judge_result = checker.judge(response_content, language)
        entry["one-round judge"] = judge_result

    def process_one_round(self, entry):
        """
        处理 one-round 任务的函数：
          1. 拼接提示词与 generated text，调用模型生成回答；
          2. 使用 GPTCheck.judge 检查回答，将结果分别存储到 "one-round response" 与 "one-round judge" 中。
        """

        # 获取起始提示文本并与 generated_text 拼接  
        prompt = start_prompt(entry, self.scenario)  
        messages = [
            {"role": "user", "content": prompt}
        ]
        # 调用模型生成回答
        client = self.init_model(self.model)

        response = self.get_response(messages, client, self.model)
        if not response or not hasattr(response, "choices") or not response.choices:
            response_content = ""
        else:
            try:
                # 尝试提取回答内容
                response_content = response.choices[0].message.content.strip()
            except (AttributeError, IndexError, json.JSONDecodeError) as e:
                print(f"Attempt {attempt}: Error extracting response: {e}")
                response_content = ""

        # 将回答存储到 "one-round response" 键中（尝试解析为 JSON）
        try:
            entry["one-round response"] = json.loads(response_content)
        except json.JSONDecodeError:
            entry["one-round response"] = response_content

    def process_multi_round(self, entry):
        """
        预留 multi-round 任务的处理函数，具体逻辑另行实现。
        注意：请不要将具体 multi-round 代码直接写在 process_fraud_data 中。
        """
        # TODO: 实现 multi-round 模式下的具体逻辑
        pass