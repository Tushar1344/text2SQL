import openai
from openai import OpenAI
def explain_sql_query(sql_query, user_question, api_key):
    openai.api_key = api_key
    client = OpenAI()
    system_instructions = f"""\
    You are an expert in SQL and database systems. 
    Your role is to help users understand SQL queries by providing clear, step-by-step explanations. 
    When a query is provided, analyze it thoroughly and explain each part, including what the query does, how the clauses work together, and what results can be expected.
    If possible, identify potential issues, inefficiencies, or improvements. 
    Make sure your responses are easy to understand, even for users who might be new to SQL. 
    If additional context (such as table schemas) is provided, incorporate that into your explanation. 
    If the user requests, offer suggestions to optimize or correct the query."
    """
    prompt = f"""User Question:
    "{user_question}"
    SQL Query:
    {sql_query}
    Explanation:
    """
    messages = [{"role": "system", "content": system_instructions},
            {"role": "user", "content": prompt}
        ]
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        max_tokens=200,
        temperature=0.5,
        # stop=["\n\n"]
    )
    explanation = response.choices[0].message.content.strip()
    return explanation
