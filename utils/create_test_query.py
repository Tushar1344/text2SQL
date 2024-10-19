import sqlite3
def run_test_queries(db_name='fake_data.db'):
    """Connects to the SQLite database and runs test queries for each table."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    tables = ['sales', 'products', 'customers']  # Add more table names if needed

    for table_name in tables:
        try:
            print(f"--- Running test query for table: {table_name} ---")

            # Primary Key Constraint Check
            pk_column = None
            # Get primary key column name (assuming only one primary key per table)
            cursor.execute(f"PRAGMA table_info({table_name});")
            for column_info in cursor.fetchall():
                if column_info[5] == 1:  # Column is primary key
                    pk_column = column_info[1]
                    break

            if pk_column:
                print(f"Checking primary key constraint for column: {pk_column}")
                cursor.execute(f"SELECT COUNT(*) FROM (SELECT DISTINCT {pk_column} FROM {table_name}) AS T1, {table_name} AS T2 WHERE T1.{pk_column} = T2.{pk_column};")
                num_distinct_pk = cursor.fetchone()[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                total_rows = cursor.fetchone()[0]
                if num_distinct_pk == total_rows:
                    print("Primary key constraint is satisfied.")
                else:
                    print("Primary key constraint is violated!")

            # Foreign Key Constraint Check (example for 'sales' table)
            if table_name == 'sales':
                print("Checking foreign key constraint: sales.product_id -> products.product_id")
                cursor.execute("SELECT COUNT(*) FROM sales WHERE product_id NOT IN (SELECT product_id FROM products);")
                num_violations = cursor.fetchone()[0]
                if num_violations == 0:
                    print("Foreign key constraint is satisfied.")
                else:
                    print(f"Foreign key constraint is violated! {num_violations} violations found.")

                print("Checking foreign key constraint: sales.customer_id -> customers.customer_id")
                cursor.execute("SELECT COUNT(*) FROM sales WHERE customer_id NOT IN (SELECT customer_id FROM customers);")
                num_violations = cursor.fetchone()[0]
                if num_violations == 0:
                    print("Foreign key constraint is satisfied.")
                else:
                    print(f"Foreign key constraint is violated! {num_violations} violations found.")

            # Fetch and print some data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")  # Fetch 5 rows for testing
            results = cursor.fetchall()
            for row in results:
                print(row)
            print("\n")

        except sqlite3.Error as e:
            print(f"Error querying table {table_name}: {e}")

    conn.close()
