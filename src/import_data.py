"""
Реализация python-комманды импорта из csv в БД через SQLAlchemy.

Запуск:
python import_data.py [-h] [-f FILE] [-t TABLE]
"""

import argparse

import pandas as pd

from app.database.session import sync_engine


def import_data(file_name, table_name):
    data = pd.read_csv(file_name)
    data.to_sql(table_name, con=sync_engine, index=False, if_exists="append")


def main():
    parser = argparse.ArgumentParser(
        description="Import data from CSV to database.",
    )
    parser.add_argument(
        "-f", "--csv-file", required=True, help="Path to the CSV file"
    )
    parser.add_argument(
        "-t", "--table-name", required=True, help="Name of the database table"
    )

    args = parser.parse_args()
    csv_filename = args.csv_file
    table_name = args.table_name
    import_data(csv_filename, table_name)


if __name__ == "__main__":
    main()
