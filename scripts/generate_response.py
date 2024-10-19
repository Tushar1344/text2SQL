import openai
from openai import OpenAI
def generate_response(results, user_question, api_key):
    openai.api_key = api_key
    client = OpenAI()
    # ToDo: this should be dynamic to the datamodel
    system_instructions = """
    Given the SQL query results below, provide a concise and clear summary that answers the user's question.
    """
    prompt = f"""
    User Question:
    "{user_question}"
    Results:
    {results}
    Summary:
    """
    messages = [{'role': 'system', 'content': system_instructions},
                {'role': 'user', 'content': prompt}]
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        max_tokens=150,
        temperature=0.7,
        # stop=["\n\n"]
    )
    summary = response.choices[0].message.content.strip()
    return summary
