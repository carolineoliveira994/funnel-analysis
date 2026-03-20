from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
file_path = project_root / "data" / "raw" / "events.csv"

df = pd.read_csv(
    file_path,
    nrows=100000,
    dtype={"category_id": str}
)

# total de eventos por tipo
event_counts = df["event_type"].value_counts()

views = int(event_counts.get("view", 0))
carts = int(event_counts.get("cart", 0))
purchases = int(event_counts.get("purchase", 0))

# métricas simples
cart_rate_vs_view = (carts / views * 100) if views else 0
purchase_rate_vs_view = (purchases / views * 100) if views else 0
purchase_rate_vs_cart = (purchases / carts * 100) if carts else 0

print("=== FUNIL BÁSICO ===")
print(f"Views: {views}")
print(f"Carts: {carts}")
print(f"Purchases: {purchases}")

print("\n=== TAXAS ===")
print(f"Cart / View: {cart_rate_vs_view:.2f}%")
print(f"Purchase / View: {purchase_rate_vs_view:.2f}%")
print(f"Purchase / Cart: {purchase_rate_vs_cart:.2f}%")

# receita estimada
purchase_df = df[df["event_type"] == "purchase"].copy()
total_revenue = purchase_df["price"].sum()

print("\n=== RECEITA ===")
print(f"Receita total estimada: {total_revenue:.2f}")

# top marcas por compras
top_brands = (
    purchase_df.groupby("brand", dropna=False)
    .agg(
        purchases=("event_type", "count"),
        revenue=("price", "sum")
    )
    .sort_values(["purchases", "revenue"], ascending=False)
    .head(10)
)

print("\n=== TOP MARCAS POR COMPRA ===")
print(top_brands)

# top categorias por compra
top_categories = (
    purchase_df.groupby("category_code", dropna=False)
    .agg(
        purchases=("event_type", "count"),
        revenue=("price", "sum")
    )
    .sort_values(["purchases", "revenue"], ascending=False)
    .head(10)
)

print("\n=== TOP CATEGORIAS POR COMPRA ===")
print(top_categories)