import sqlite3
import pandas as pd

conn = sqlite3.connect(r"C:\Users\kasir\PyCharmProjects\PythonProject4\db\nifty100.db")

df = pd.read_sql("SELECT * FROM documents LIMIT 10;", conn)

print(df)

conn.close()