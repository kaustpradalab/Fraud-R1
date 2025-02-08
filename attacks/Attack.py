from openai import OpenAI
from attacks import config

class Attack:
    def __init__(self):
        super()
    def init_model(self, model):
        if "gpt-4o" in model:
            client = OpenAI(api_key=config.OPENAI_KEY)
        elif  "o3-mini" in model:
            client = OpenAI(api_key=config.OPENAI_o3_KEY)
        else:
            client = OpenAI(api_key=config.ZHI_KEY, base_url=config.ZHI_URL)
        return client

    def get_response(self, messages, client, model):
        response = client.chat.completions.create(
                model=model,
                messages=messages
                )
        return response