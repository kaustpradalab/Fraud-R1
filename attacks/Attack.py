from openai import OpenAI
from utils import config
import random
import time


class Attack:
    def __init__(self):
        super()

    def init_model(self, model):
        if "gpt-4o" in model:
            print("Processing with OPENAI API")
            if hasattr(config, 'OPENAI_KEY'):
                api_key = config.OPENAI_KEY
            elif hasattr(config, 'OPENAI_KEYS'):
                api_key = random.choice(config.OPENAI_KEYS)
            else:
                raise ValueError("Neither OPENAI_KEY nor OPENAI_KEYS found in config")
            client = OpenAI(api_key=api_key)
        else:
            print("Processing with OHMYGPT")
            if hasattr(config, 'OHMYGPT_KEY'):
                api_key = config.OHMYGPT_KEY
            elif hasattr(config, 'OHMYGPT_KEYS'):
                api_key = random.choice(config.OHMYGPT_KEYS)
            else:
                raise ValueError("Neither OHMYGPT_KEY nor OHMYGPT_KEYS found in config")
            client = OpenAI(
                api_key=api_key, base_url=config.OHMYGPT_URL
            )
        return client
        """   
        else:
            print("Processing with ZHIZZ")
            if hasattr(config, 'ZHI_KEY'):
                api_key = config.ZHI_KEY
            elif hasattr(config, 'ZHI_KEYS'):
                api_key = random.choice(config.ZHI_KEYS)
            else:
                raise ValueError("Neither ZHI_KEY nor ZHI_KEYS found in config")
            client = OpenAI(
                api_key=api_key, base_url=config.ZHI_URL
            )
        """  

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
                time.sleep(2) 

        print("Max retries reached. Returning empty response.")
        return {}