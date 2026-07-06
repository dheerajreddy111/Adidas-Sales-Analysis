import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

CSV_PATH = os.environ.get(
    "ADIDAS_CSV_PATH",
    str(Path(__file__).parent / "Data" / "adidas_sales_dataset.csv"),
)

SERVER = os.environ["ADIDAS_DB_SERVER"]
DATABASE = os.environ["ADIDAS_DB_NAME"]
USERNAME = os.environ["ADIDAS_DB_USER"]
PASSWORD = os.environ["ADIDAS_DB_PASSWORD"]
DRIVER = os.environ.get("ADIDAS_DB_DRIVER", "ODBC Driver 17 for SQL Server")

df = pd.read_csv(CSV_PATH)
df.drop(columns=[c for c in df.columns if c.startswith("Unnamed:")], inplace=True)

connection_string = (
    f"mssql+pyodbc://{USERNAME}:{urllib.parse.quote_plus(PASSWORD)}"
    f"@{SERVER}/{DATABASE}?driver={urllib.parse.quote_plus(DRIVER)}"
)
engine = create_engine(connection_string)

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
    raise SystemExit(1)

table_name = "sales"
try:
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print("Data loaded successfully!")
except Exception as e:
    print(f"Data load failed: {e}")
