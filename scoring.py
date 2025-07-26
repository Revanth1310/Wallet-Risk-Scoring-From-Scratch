import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load CSV
df = pd.read_csv("compound_wallet_data.csv")

# Group by wallet and sum USD value
df_grouped = df.groupby("wallet_id").agg({
    "value_usd": "sum",
    "symbol": "nunique"
}).rename(columns={
    "value_usd": "total_usd_value",
    "symbol": "token_diversity"
}).reset_index()

# Raw score: combine value and diversity
df_grouped["score_raw"] = (
    df_grouped["total_usd_value"] * 0.8 + df_grouped["token_diversity"] * 100
)

# Normalize to 0–1000
scaler = MinMaxScaler(feature_range=(0, 1000))
df_grouped["score"] = scaler.fit_transform(df_grouped[["score_raw"]]).round().astype(int)

# Output
df_grouped[["wallet_id", "score"]].to_csv("wallet_scores.csv", index=False)
print("✅ Done. Scores saved to wallet_scores.csv")
