from openai import OpenAI
from utils import config
import random
import time


class Attack:
    def __init__(self):
        super()

    def init_model(self, model):
        if "gpt-4o" in model:
            api_key = random.choice(config.OPENAI_KEYS)
            client = OpenAI(api_key=api_key)
        elif "o3-mini" in model or "Llama" in model:
            client = OpenAI(
                api_key=random.choice(config.OHMYGPT_KEYS), base_url=config.OHMYGPT_URL
            )
        else:
            client = OpenAI(
                api_key=random.choice(config.ZHI_KEYS), base_url=config.ZHI_URL
            )
        return client

    def get_response(self, messages, client, model):
        retry_count = 0
        while retry_count < 5:
            try:
                response = client.chat.completions.create(
                    model=model, messages=messages
                )
                return response
            except Exception as e:
                retry_count += 1
                print(f"Error occurred: {e}. Retrying {retry_count}/5...")
                time.sleep(2)  # Add a delay between retries (e.g., 2 seconds)

        # If retry count exceeds 5, return an empty response
        print("Max retries reached. Returning empty response.")
        return {}