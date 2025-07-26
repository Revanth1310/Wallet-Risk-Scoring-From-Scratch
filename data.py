import requests
import pandas as pd
import time

# === CONFIG ===
API_KEY = "cqt_rQRmVqFQdQrb7pPDjV4h6tf7rXHD"  # 🔐 Replace with your Covalent API Key
CHAIN_ID = 1  # Ethereum Mainnet
OUTPUT_CSV = "compound_wallet_data.csv"
WALLET_FILE = "wallet_id.xlsx"

# === Load Wallets ===
df_wallets = pd.read_excel(WALLET_FILE)
wallets = df_wallets['wallet_id'].dropna().unique().tolist()

results = []

# === Fetch Function ===
def fetch_wallet_balance(wallet):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet}/balances_v2/?key={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        if not data.get("data") or not data["data"].get("items"):
            print(f"❌ No data for {wallet[:6]}...")
            return

        for item in data["data"]["items"]:
            decimals = item.get("contract_decimals")
            if decimals is None:
                print(f"⚠️ Missing decimals for {item.get('contract_ticker_symbol')} — skipping")
                continue

            balance_raw = int(item.get("balance", 0))
            balance_normalized = balance_raw / (10 ** decimals)

            results.append({
                "wallet_id": wallet,
                "contract_name": item.get("contract_name"),
                "symbol": item.get("contract_ticker_symbol"),
                "balance": balance_normalized,
                "quote_rate": item.get("quote_rate", 0),
                "value_usd": item.get("quote", 0)
            })

    except Exception as e:
        print(f"Error fetching {wallet[:6]}...: {e}")


# === Main Runner ===
print("🔍 Fetching wallet balances via Covalent...")
for i, wallet in enumerate(wallets):
    print(f"[{i+1}/{len(wallets)}] {wallet[:10]}...")
    fetch_wallet_balance(wallet)
    time.sleep(0.25)  # API rate limit protection

# === Save to CSV ===
df_out = pd.DataFrame(results)
df_out.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Data saved to {OUTPUT_CSV}")
