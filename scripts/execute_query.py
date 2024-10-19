import sqlite3
def execute_sql_query(sql_query, db_connection, params=None):
    try:
        cursor = db_connection.cursor()
        if params:
            cursor.execute(sql_query, params)
        else:
            cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
        return "Couldn't run the SQL query" # Extract from error

