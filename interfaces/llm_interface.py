import re
import openai
from functools import partial
from openai import OpenAI
import google.generativeai as genai

class LLMInterface:
    def __init__(self, api_key, model_name:str = 'gpt-4o-mini'):
        self.api_key = api_key
        self.model_name = model_name
        self.setup()

    def setup(self):
        if re.match(r'^gpt', self.model_name):
            client = OpenAI()
            self.query_fn = partial(client.chat.completions.create, model=self.model_name)
        elif re.search(r'gemini', self.model_name):
            genai.configure(api_key=self.api_key)
            client = genai.GenerativeModel(self.model_name)
            self.query_fn = client.generate
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")


    def __call__(self, messages):
        response = self.query_fn(
            messages,
            max_tokens=150,
            temperature=0,
            # stop=["\n\n"]
        )

