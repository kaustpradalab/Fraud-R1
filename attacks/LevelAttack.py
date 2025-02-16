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
        if not self.file_name.endswith(".json"):
            return

        with open(self.file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if self.task == "one-round":
            print("Processing one-round attacking now~")
            model_response_key = "one-round response"
        elif self.task == "multi-round":
            print("Processing multi-round attacking now~")
            model_response_key = "GPT judge"
        elif self.task == "one-round-eval":
            print("Processing one-round GPT checking now~")
            model_response_key = "one-round judge"
        else:
            print("unknown task")
            return

        for index, entry in tqdm(enumerate(data), total=len(data)):
            # For multi-round tasks, we need an extra check:
            if self.task == "multi-round":
                if "GPT judge" in entry and entry.get("GPT judge") != "":
                    multi_rounds = entry.get("multi-rounds fraud", [])
                    all_filled = True
                    for round_item in multi_rounds:
                        # If any round has an empty "model response", we need to re-run this entry.
                        if "model response" in round_item and round_item["model response"] == "":
                            all_filled = False
                            break
                    if all_filled:
                        print(f"skip item{index}，due to exist '{model_response_key}' and all round's model response completed")
                        continue
            else:
                if model_response_key in entry and entry.get(model_response_key) != "":
                    print(f"skip item {index}，due to exist '{model_response_key}'。")
                    continue

            print(f"Processing item {index}...")
            if self.task == "one-round":
                self.process_one_round(entry)
            elif self.task == "multi-round":
                self.process_multi_round(entry)
            elif self.task == "one-round-eval":
                self.process_one_round_judge(entry)
            
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
 
        prompt = start_prompt(entry, self.scenario, self.task)  
        messages = [
            {"role": "user", "content": prompt}
        ]
        client = self.init_model(self.model)

        response = self.get_response(messages, client, self.model)
        if not response or not hasattr(response, "choices") or not response.choices:
            response_content = ""
        else:
            try:
                response_content = response.choices[0].message.content.strip()
            except (AttributeError, IndexError, json.JSONDecodeError) as e:
                print(f"Error extracting response: {e}")
                response_content = ""

        try:
            entry["one-round response"] = json.loads(response_content)
        except json.JSONDecodeError:
            entry["one-round response"] = response_content

    def _truncate_text(self, text, max_length=512):
        return text[:max_length] if len(text) > max_length else text

    def truncate_conversation_messages(self, messages, max_length=512):
        truncated = []
        for msg in messages:
            new_msg = {"role": msg["role"], "content": ""}
            truncated_text = self._truncate_text(msg["content"], max_length)
            new_msg["content"] = truncated_text
            truncated.append(new_msg)
        return truncated


    def process_multi_round(self, entry):
        checker = GPTCheck()
        language = entry.get("language")
        
        conversation_messages = []
        
        client = self.init_model(self.model)
        
        total_rounds = 4
        if "multi-rounds fraud" not in entry or not isinstance(entry["multi-rounds fraud"], list):
            entry["multi-rounds fraud"] = []
        while len(entry["multi-rounds fraud"]) < total_rounds:
            entry["multi-rounds fraud"].append({})
        
        for round_num in range(1, total_rounds + 1):
            if round_num == 1 and entry.get("one-round response", "").strip() != "" and entry.get("one-round judge", "").strip() in ["YES", "NO", "NEXT ROUND"]:
                prompt = start_prompt(entry, self.scenario, self.task, rounds=1)
                current_user_message = {
                    "role": "user",
                    "content": prompt
                }
                conversation_messages.append(current_user_message)
                assistant_message = {
                    "role": "assistant",
                    "content": entry["one-round response"]
                }
                conversation_messages.append(assistant_message)
                
                round_dict = entry["multi-rounds fraud"][0]
                round_dict["round"] = 1
                round_dict["model response"] = entry["one-round response"]
                round_dict["GPT check"] = entry["one-round judge"]
                
                if "NEXT ROUND" in entry["one-round judge"] or entry["one-round judge"] == "NEXT ROUND":
                    print("Round 1: Using pre-computed one-round response, GPT check returned 'NEXT ROUND', proceeding to next round.")
                else:
                    print(f"Round 1: Using pre-computed one-round response, GPT check returned '{entry['one-round judge']}', stopping further rounds.")
                    break
                continue  

            if round_num == 1:
                prompt = start_prompt(entry, self.scenario, self.task, rounds=1)
            else:
                prompt = more_prompt(entry, self.scenario, self.task, rounds=round_num)
            
            current_user_message = {
                "role": "user",
                "content": prompt
            }
            messages_to_send = self.truncate_conversation_messages(conversation_messages, 512) + [current_user_message]
            
            response = self.get_response(messages_to_send, client, self.model)
            if not response or not hasattr(response, "choices") or not response.choices:
                response_content = ""
            else:
                try:
                    response_content = response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"Round {round_num}: Error extracting response: {e}")
                    response_content = ""
            
            round_dict = entry["multi-rounds fraud"][round_num - 1]
            round_dict["round"] = round_num
            round_dict["model response"] = response_content
            
            if not response_content:
                print(f"Round {round_num}: response is empty, skipping GPT check and proceeding to next round.")
                empty_assistant_message = {
                    "role": "assistant",
                    "content": ""
                }
                conversation_messages.append(current_user_message)
                conversation_messages.append(empty_assistant_message)
                continue
            
            assistant_message = {
                "role": "assistant",
                "content": response_content
            }
            conversation_messages.append(current_user_message)
            conversation_messages.append(assistant_message)
            
            check_result = checker.judge(response_content, language)
            round_dict["GPT check"] = check_result
            
            if "NEXT ROUND" in check_result or check_result == "NEXT ROUND":
                print(f"Round {round_num}: GPT check returned 'NEXT ROUND', proceeding to next round.")
            else:
                print(f"Round {round_num}: GPT check returned '{check_result}', stopping further rounds.")
                break
        
        final_result = None
        for r in entry["multi-rounds fraud"]:
            if "GPT check" in r and r["GPT check"] in ["YES", "NO"]:
                final_result = r["GPT check"]
                break
        if final_result is None:
            final_result = "NO"
        entry["GPT judge"] = final_result
        entry["truncated conversation history"] = conversation_messages
