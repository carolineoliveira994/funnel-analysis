from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
file_path = project_root / "data" / "raw" / "events.csv"

df = pd.read_csv(
    file_path,
    nrows=100000,
    dtype={"category_id": str}
)

# ======================
# DIM PRODUCT
# ======================
dim_product = df[["product_id", "category_code", "brand"]].drop_duplicates()

# ======================
# DIM USER
# ======================
dim_user = df[["user_id"]].drop_duplicates()

# ======================
# DIM TIME
# ======================
df["event_time"] = pd.to_datetime(df["event_time"])

dim_time = df[["event_time"]].drop_duplicates().copy()
dim_time["date"] = dim_time["event_time"].dt.date
dim_time["hour"] = dim_time["event_time"].dt.hour
dim_time["day_of_week"] = dim_time["event_time"].dt.day_name()

# cria ID de tempo
dim_time["time_id"] = dim_time.index

# ======================
# FACT EVENTS
# ======================
fact_events = df.merge(
    dim_time[["event_time", "time_id"]],
    on="event_time",
    how="left"
)

fact_events = fact_events[
    ["user_id", "product_id", "event_type", "time_id", "price"]
]

# ======================
# SALVAR
# ======================
output_path = project_root / "data" / "processed"
output_path.mkdir(parents=True, exist_ok=True)

dim_product.to_csv(output_path / "dim_product.csv", index=False)
dim_user.to_csv(output_path / "dim_user.csv", index=False)
dim_time.to_csv(output_path / "dim_time.csv", index=False)
fact_events.to_csv(output_path / "fact_events.csv", index=False)

print("Modelo dimensional criado com sucesso 🚀")