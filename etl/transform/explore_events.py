import pandas as pd

df = pd.read_csv(
    "data/raw/events.csv",
    nrows=100000,
    dtype={"category_id": str}
)

print("Colunas:")
print(df.columns)

print("\nTipos:")
print(df.dtypes)

print("\nEventos:")
print(df["event_type"].value_counts())



