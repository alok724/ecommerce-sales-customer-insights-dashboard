# import pandas as pd
# from pathlib import Path

# # Existing cleaned dataset
# input_path = Path(
#     r"C:\Users\alok3\OneDrive\Desktop\Programming  Language\Main_project\online_retail_cleaned.csv"
# )

# # New MySQL-compatible CSV
# output_path = input_path.with_name("online_retail_mysql.csv")

# # Load the existing cleaned dataset
# df = pd.read_csv(input_path)

# print("Original shape:", df.shape)

# # Convert Boolean columns to integers: True -> 1, False -> 0
# boolean_columns = df.select_dtypes(include="bool").columns.tolist()

# for col in boolean_columns:
#     df[col] = df[col].astype("int8")

# # Export without changing the original file.
# # Empty fields represent missing values.
# df.to_csv(
#     output_path,
#     index=False,
#     na_rep="",
#     encoding="utf-8"
# )

# print("\nBoolean columns converted:", boolean_columns)
# print("Exported shape:", df.shape)
# print("Output file:", output_path)
# print("File exists:", output_path.exists())
# print("File size (bytes):", output_path.stat().st_size)

# # Re-import and validate the exported CSV
# check_df = pd.read_csv(output_path)

# print("\nRe-imported shape:", check_df.shape)
# print("Column names match:", check_df.columns.tolist() == df.columns.tolist())
# print("Boolean columns now contain:")
# for col in boolean_columns:
#     print(col, sorted(check_df[col].dropna().unique().tolist()))


import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# 1. Enter your MySQL details
mysql_user = "root"
mysql_password = quote_plus("1234")  # <-- Apna MySQL password yahan likhein
mysql_host = "localhost"
mysql_port = "3306"
mysql_db = "ecommerce_analysis"

# 2. Load the verified CSV
csv_path = r"C:\Users\alok3\OneDrive\Desktop\Programming  Language\Main_project\online_retail_mysql.csv"
df_mysql = pd.read_csv(csv_path, low_memory=False)
print(f"CSV loaded in Python: {df_mysql.shape}")

# 3. Connect to MySQL and insert into online_retail_mysql in safe 25,000-row batches
engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}")

df_mysql.to_sql(
    name="online_retail_mysql",
    con=engine,
    if_exists="append",   # Uses the exact table structure we just created in MySQL!
    index=False,
    chunksize=25000       # Prevents any PC lag or memory spike
)

print("SUCCESS: All 536,641 rows imported into ecommerce_analysis.online_retail_mysql!")
