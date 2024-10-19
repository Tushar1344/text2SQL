import re

# To DO: Make this LLM driven
def expand_metrics_in_sql(sql_query, metrics):
    for metric in metrics:
        pattern = r'\b' + re.escape(metric['name']) + r'\b'
        sql_query = re.sub(pattern, f"({metric['calculation']})", sql_query)
    return sql_query
