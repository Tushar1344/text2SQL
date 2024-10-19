
import logging
import yaml
# Setup logging configuration
logging.basicConfig(level=logging.INFO)


def load_schema(yaml_file):
    with open(yaml_file, 'r') as file:
        schema = yaml.safe_load(file)
    return schema


def generate_schema_representation(schema: dict) -> str:
    """
    Generates a human-readable schema representation.
    """
    schema_str = ''
    schema_str += process_tables(schema.get('tables', []))
    schema_str += process_metrics(schema.get('metrics', []))
    return schema_str


def process_tables(tables: list) -> str:
    """
    Processes the list of tables in the schema and returns a formatted string.
    """
    table_lines = []

    for table in tables:
        table_lines.append(f"Table: {table['name']} ({table.get('type', 'table')})")
        table_lines.append("Columns:")
        table_lines.append(process_columns(table.get('columns', [])))
        table_lines.append(process_dimensions(table.get('dimensions', [])))
        table_lines.append("")  # Newline after each table

    return "\n".join(table_lines)


def process_columns(columns: list) -> str:
    """
    Processes the columns of a table and returns a formatted string.
    """
    column_lines = []

    for column in columns:
        try:
            column_name = column.get('name', 'Unnamed Column')
            data_type = column.get('data_type', 'Unknown Type')
            column_line = f"  - {column_name} ({data_type})"
            if column.get('primary_key'):
                column_line += " [PK]"
            if 'foreign_key' in column:
                fk = column['foreign_key']
                column_line += f" [FK -> {fk.get('table', 'Unknown Table')}.{fk.get('column', 'Unknown Column')}]"
            if 'description' in column:
                column_line += f" - {column.get('description', 'No description')}"
            column_lines.append(column_line)
        except Exception as e:
            logging.error(f"Error processing column: {column}. Error: {str(e)}")
            continue

    return "\n".join(column_lines)


def process_dimensions(dimensions: list) -> str:
    """
    Processes the dimensions of a table and returns a formatted string.
    """
    dimension_lines = []

    if dimensions:
        dimension_lines.append("Dimensions:")
        for dimension in dimensions:
            dimension_lines.append(f"  - Type: {dimension.get('type')}, SCD Type: {dimension.get('scd_type')}")

    return "\n".join(dimension_lines)


def process_metrics(metrics: list) -> str:
    """
    Processes the metrics in the schema and returns a formatted string.
    """
    metric_lines = []

    if metrics:
        metric_lines.append("Metrics:")
        for metric in metrics:
            metric_lines.append(f"  - Name: {metric['name']}")
            metric_lines.append(f"    Expression: {metric['calculation']}")
            if 'description' in metric:
                metric_lines.append(f"    Description: {metric['description']}")
            metric_lines.append("")  # Newline between metrics

    return "\n".join(metric_lines)
