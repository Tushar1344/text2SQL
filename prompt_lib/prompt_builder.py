
import openai
from openai import OpenAI

def generate_prompt(schema_representation, user_question, api_key):
    openai.api_key = api_key
    client = OpenAI()
    # Define the system-level instructions for the model
    system_instruction = """
    You are an expert and helpful SQL assistant. 
    Your task is to help users generate optimized SQL queries based on provided database schemas.
    Always ensure:
    - Use predefined metrics when appropriate.
    - Ensure all table and column names match the schema.
    - Use proper JOINs based on foreign key relationships.
    - Be precise and optimize the query for performance.
    """

    # Define the user prompt
    user_prompt = f"""\
    Database Schema and Metrics:
        {schema_representation}

    Question: "{user_question}"

    Please generate the SQL query to answer the above question.
    """
    messages = [{"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ]
    return messages

