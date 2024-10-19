import sqlite3
import json
import os
from utils.parse_schema import load_schema, generate_schema_representation
from utils.metric_expander import *
from prompt_lib.prompt_builder import *
from prompt_lib.explain_query import *
from interfaces.llm_interface import *
from .execute_query import *
from .generate_response import *

def get_sql_query(user_question, base_path):
    # get api key
    api_key = os.environ['API_KEY']
    # Load schema
    yaml_path = f"{base_path}/schema.yaml"
    schema = load_schema(yaml_path)
    schema_representation = generate_schema_representation(schema)
    metrics = schema.get('metrics', [])

    # Generate prompt
    prompt = generate_prompt(schema_representation, user_question, api_key)

    # Get SQL query from LLM
    llm = LLMInterface(api_key, model_name = 'gpt-4o-mini')
    response = llm(prompt)
    response = json.loads(response)
    sql_query = response['sql_query']
    print(f"\nGenerated SQL Query:\n{sql_query}\n")

    explanation = explain_sql_query(sql_query, user_question, api_key)
    print(f"\nExplanation of SQL Query:\n{explanation}\n")
    sql_query_expanded = expand_metrics_in_sql(sql_query, metrics)
    print(f"\nSQL Query after expanding metrics:\n{sql_query_expanded}\n")
    # To Do: LLM as a relevancy judge

    return sql_query, sql_query_expanded, explanation

def run(user_question: str, base_path: str = None, db_name: str = None):
    if not db_name:
        db_name = 'fake_data.pb'
    api_key = os.environ['API_KEY']
    db_path = f"{base_path}/data/databases/fake_data.db"
    # user_question = "What is the total sales amount?"
    sql_query, sql_query_expanded, explanation = get_sql_query(user_question, base_path)
    db_connection = sqlite3.connect(db_path)
    results = execute_sql_query(sql_query, db_connection)
    if results is not None:
        # Generate natural language response
        summary = generate_response(results, user_question, api_key)
        print(f"Summary:\n{summary}")
    else:
        print("No results returned or an error occurred.")

    # Close the database connection
    db_connection.close()
    return results

def main():
    # Get user question
    user_question = input("Enter your question: ")
    if len(user_question.strip()) == 0:
        user_question = "What is the total sales amount?"
    run(user_question, base_path = repo_path)
if __name__ == '__main__':
    import os
    import sys
    import sqlite3
    import json
    os.environ['API_KEY'] = os.getenv('OPENAI_API_KEY')
    main()


