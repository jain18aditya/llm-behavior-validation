
from openai import OpenAI
from config import MODEL
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def generate(prompt, temperature):
    response = client.responses.create(model=MODEL, input=prompt,
                                       temperature=temperature, max_output_tokens=80)
    return response.output_text.strip()
