from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
file_path = project_root / "data" / "raw" / "events.csv"

df = pd.read_csv(
    file_path,
    nrows=100000,
    dtype={"category_id": str}
)

# agrupar por sessão
session_events = df.groupby("user_session")["event_type"].apply(set)

# criar flags
sessions = pd.DataFrame({
    "view": session_events.apply(lambda x: "view" in x),
    "cart": session_events.apply(lambda x: "cart" in x),
    "purchase": session_events.apply(lambda x: "purchase" in x),
})

# contagem
views = sessions["view"].sum()
carts = sessions["cart"].sum()
purchases = sessions["purchase"].sum()

print("=== FUNIL POR SESSÃO ===")
print(f"Sessões com view: {views}")
print(f"Sessões com cart: {carts}")
print(f"Sessões com purchase: {purchases}")

# taxas
print("\n=== TAXAS ===")
print(f"Cart / View: {(carts/views)*100:.2f}%")
print(f"Purchase / Cart: {(purchases/carts)*100:.2f}%" if carts else 0)