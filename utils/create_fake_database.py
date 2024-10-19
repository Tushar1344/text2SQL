import sqlite3
from faker import Faker
import random
import yaml
from datetime import datetime, timedelta

def create_fake_database(yaml_content, db_name='fake_data.db'):
    """
    Creates a fake SQLite database based on the provided YAML schema.
    Handles primary and foreign key relationships using Faker's providers.
    """
    fake = Faker()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create tables based on the schema
    for table_data in yaml_content['tables']:
        table_name = table_data['name']
        columns = table_data['columns']
        column_definitions = ', '.join([f"{col['name']} {get_sql_data_type(col['data_type'])}" for col in columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")

    # Insert fake data, respecting foreign key constraints and SCD
    for table_data in yaml_content['tables']:
        table_name = table_data['name']
        columns = table_data['columns']
        num_rows = 10  # Adjust the number of rows to generate

        for _ in range(num_rows):
            values = []
            for col in columns:
                if col.get('primary_key', False):  # Check if the column is marked as a primary key
                    values.append(fake.unique.random_int(min=1, max=1000))  # Generate unique IDs
                elif 'foreign_key' in col:
                    fk_table = col['foreign_key']['table']
                    fk_column = col['foreign_key']['column']
                    # Fetch a random existing value from the foreign key table
                    cursor.execute(f"SELECT {fk_column} FROM {fk_table} ORDER BY RANDOM() LIMIT 1")
                    fk_value_row = cursor.fetchone()
                    fk_value = fk_value_row[0] if fk_value_row else None  # Handle missing foreign key
                    values.append(fk_value)
                elif col['data_type'].lower() == 'integer':
                    values.append(fake.random_int(min=1, max=1000))
                elif col['data_type'].lower() == 'string':
                    values.append(fake.word())
                elif col['data_type'].lower() == 'date':
                    values.append(fake.date_this_year().strftime('%Y-%m-%d'))
                elif col['data_type'].lower() == 'decimal':  # Handling decimals
                    # Convert decimal.Decimal to float before insertion
                    values.append(float(fake.pydecimal(left_digits=5, right_digits=2, positive=True)))
            placeholders = ', '.join(['?'] * len(values))
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
    conn.commit()
    conn.close()

def get_sql_data_type(data_type):
    """Maps data types from the YAML schema to SQLite data types."""
    type_mapping = {
        'integer': 'INTEGER',
        'string': 'TEXT',
        'date': 'DATE',
        'decimal': 'REAL'  # SQLite uses REAL for decimals
    }
    return type_mapping.get(data_type.lower(), 'TEXT')  # Default to TEXT if not found
