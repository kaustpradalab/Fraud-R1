from openai import OpenAI
from utils import config
import os
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"
class Attack:
    def __init__(self):
        super()
    def init_model(self, model):
        if "gpt-4o" in model:
            client = OpenAI(api_key=config.OPENAI_KEY)
        elif  "o3-mini" in model or "Llama" in model:
            client = OpenAI(api_key=config.OHMYGPT_KEY, base_url=config.OHMYGPT_URL)
        else:
            client = OpenAI(api_key=config.ZHI_KEY, base_url=config.ZHI_URL)
        return client

    def get_response(self, messages, client, model):
        response = client.chat.completions.create(
                model=model,
                messages=messages
                )
        return response