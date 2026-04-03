import argparse
import os
import sys
from typing import Optional

from wSnowflake import ConnectionManager, QueryBuilder, TableSync, WSnowflake
from wSnowflake.exceptions import WSnowflakeError
from wSnowflake.types.sql_types import SnowflakeType, ColumnDefinition


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wsnowflake",
        description="wSnowflake CLI - Snowflake SQL ORM Tool",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    parser_connect = subparsers.add_parser(
        "connect", help="Test connection to Snowflake"
    )
    parser_connect.add_argument("--user", required=True, help="Snowflake user")
    parser_connect.add_argument("--password", required=True, help="Snowflake password")
    parser_connect.add_argument("--account", required=True, help="Snowflake account")
    parser_connect.add_argument("--warehouse", help="Snowflake warehouse")
    parser_connect.add_argument("--database", help="Snowflake database")
    parser_connect.add_argument("--schema", help="Snowflake schema")
    parser_connect.add_argument("--role", help="Snowflake role")

    parser_list = subparsers.add_parser("list", help="List databases/tables")
    parser_list.add_argument(
        "--warehouses", action="store_true", help="List warehouses"
    )
    parser_list.add_argument("--databases", action="store_true", help="List databases")
    parser_list.add_argument("--schemas", help="List schemas in a database")
    parser_list.add_argument("--tables", help="List tables in database.schema")

    parser_query = subparsers.add_parser("query", help="Execute a query")
    parser_query.add_argument("sql", help="SQL query to execute")
    parser_query.add_argument("--params", help="Query parameters (comma-separated)")

    parser_create = subparsers.add_parser("create-table", help="Create a table")
    parser_create.add_argument("table", help="Table name")
    parser_create.add_argument(
        "--columns", required=True, help="Columns as 'name:type,name:type'"
    )
    parser_create.add_argument(
        "--primary-key", help="Primary key columns (comma-separated)"
    )
    parser_create.add_argument("--comment", help="Table comment")

    parser_describe = subparsers.add_parser("describe", help="Describe a table")
    parser_describe.add_argument("table", help="Table name to describe")

    return parser


def get_connection_manager(args) -> ConnectionManager:
    kwargs = {}
    for key in [
        "user",
        "password",
        "account",
        "warehouse",
        "database",
        "schema",
        "role",
    ]:
        value = getattr(args, key, None)
        if value:
            kwargs[key] = value
    return ConnectionManager(**kwargs)


def handle_connect(args) -> int:
    try:
        cm = get_connection_manager(args)
        if cm.ping():
            print("Connection successful!")
            print(f"  Warehouse: {cm.get_current_warehouse()}")
            print(f"  Database: {cm.get_current_database()}")
            print(f"  Schema: {cm.get_current_schema()}")
            return 0
        else:
            print("Connection failed!", file=sys.stderr)
            return 1
    except WSnowflakeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_list(args) -> int:
    try:
        cm = get_connection_manager(args)
        if args.warehouses:
            warehouses = cm.list_warehouses()
            print("Warehouses:")
            for w in warehouses:
                print(f"  - {w}")
        elif args.databases:
            databases = cm.list_databases()
            print("Databases:")
            for db in databases:
                print(f"  - {db}")
        elif args.schemas:
            schemas = cm.list_schemas(args.schemas)
            print(f"Schemas in {args.schemas}:")
            for s in schemas:
                print(f"  - {s}")
        elif args.tables:
            parts = args.tables.split(".")
            db = WSnowflake(cm)
            if len(parts) == 2:
                tables = db.list_tables(database=parts[0], schema=parts[1])
            else:
                tables = db.list_tables()
            print(f"Tables in {args.tables}:")
            for t in tables:
                print(f"  - {t}")
        return 0
    except WSnowflakeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_query(args) -> int:
    try:
        cm = get_connection_manager(args)
        db = WSnowflake(cm)
        params = None
        if args.params:
            params = tuple(args.params.split(","))
        result = db.execute(args.sql, params)
        if result:
            for row in result:
                print(row)
        return 0
    except WSnowflakeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def parse_column_type(col_type: str) -> str:
    type_map = {
        "string": SnowflakeType.VARCHAR(16777216),
        "text": SnowflakeType.TEXT,
        "int": SnowflakeType.INTEGER,
        "integer": SnowflakeType.INTEGER,
        "bigint": SnowflakeType.BIGINT,
        "float": SnowflakeType.FLOAT,
        "double": SnowflakeType.DOUBLE,
        "bool": SnowflakeType.BOOLEAN,
        "boolean": SnowflakeType.BOOLEAN,
        "date": SnowflakeType.DATE,
        "timestamp": SnowflakeType.TIMESTAMP_NTZ,
        "datetime": SnowflakeType.DATETIME,
        "binary": SnowflakeType.BINARY,
        "array": SnowflakeType.ARRAY,
        "object": SnowflakeType.OBJECT,
    }
    col_type_lower = col_type.lower()
    if col_type_lower in type_map:
        return type_map[col_type_lower]
    return col_type


def handle_create_table(args) -> int:
    try:
        cm = get_connection_manager(args)
        ts = TableSync(cm)

        columns = []
        for col_spec in args.columns.split(","):
            parts = col_spec.split(":")
            if len(parts) != 2:
                print(
                    f"Invalid column format: {col_spec}. Use name:type", file=sys.stderr
                )
                return 1
            name, col_type = parts
            sql_type = parse_column_type(col_type)
            columns.append(ColumnDefinition(name, sql_type))

        primary_key = None
        if args.primary_key:
            primary_key = args.primary_key.split(",")

        ts.create_table_if_not_exists(
            args.table,
            columns,
            primary_key=primary_key,
            comment=args.comment,
        )
        print(f"Table '{args.table}' created successfully!")
        return 0
    except WSnowflakeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_describe(args) -> int:
    try:
        cm = get_connection_manager(args)
        db = WSnowflake(cm)
        columns = db.describe_table(args.table)
        print(f"Columns in {args.table}:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
        return 0
    except WSnowflakeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    handlers = {
        "connect": handle_connect,
        "list": handle_list,
        "query": handle_query,
        "create-table": handle_create_table,
        "describe": handle_describe,
    }

    handler = handlers.get(args.command)
    if handler:
        return handler(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
