# 📘 Wallet Risk Scoring

This project implements a DeFi wallet risk scoring model using publicly accessible wallet data from the Ethereum blockchain (via Covalent API). The goal is to assign a **risk score (0–1000)** to each wallet, reflecting its relative financial health and behavior.

---

## 🧩 1. Data Collection Method

We used the [Covalent API](https://www.covalenthq.com/docs/) to fetch token balance and valuation data for wallets listed in `wallet_id.xlsx`. Specifically:

* **Endpoint Used:** `/v1/{chain_id}/address/{wallet}/balances_v2/`
* **Chain:** Ethereum Mainnet (Chain ID: 1)
* **Fields Extracted:**

  * `contract_ticker_symbol`
  * `balance` (adjusted with `contract_decimals`)
  * `quote` (USD value of the token holding)
  * `quote_rate` (per-token USD rate)

---

## 🧮 2. Feature Selection Rationale

To reflect wallet behavior and portfolio structure, we selected the following features:

| Feature Name       | Description                    | Rationale                                  |
| ------------------ | ------------------------------ | ------------------------------------------ |
| `total_usd_value`  | Sum of all token USD values    | Indicates asset holding strength           |
| `token_count`      | Number of distinct tokens held | Measures diversification                   |
| `max_token_weight` | Proportion of dominant token   | Measures concentration risk                |
| `avg_token_value`  | Average USD value per token    | Proxy for uniformity and active management |

---

## ⚙️ 3. Scoring Method

**Step 1:** Aggregate wallet features from token-level data
**Step 2:** Normalize all numeric features using `MinMaxScaler`
**Step 3:** Calculate raw score:

```python
score = (
    0.4 * norm_total_value +
    0.2 * norm_token_count +
    0.2 * (1 - norm_max_weight) +
    0.2 * norm_avg_value
)
```

**Step 4:** Rescale to 0–1000:

```python
final_score = int(score * 1000)
```

---

## 🔍 4. Justification of Risk Indicators

| Indicator        | Justification                                            |
| ---------------- | -------------------------------------------------------- |
| Total USD Value  | More value → more skin in the game → less likely to rug  |
| Token Count      | Diversification reduces volatility exposure              |
| Max Token Weight | High weight → concentrated risk in 1 asset               |
| Avg Token Value  | Smooth spread may signal manual asset allocation vs dust |

We assume responsible, risk-averse users tend to be more diversified, hold stable-value assets, and don’t concentrate in single tokens excessively.

---

## 🚀 Scalability

* Works for **any EVM-compatible chain** (just change `chain_id`)
* Accepts **any wallet list** in `.xlsx` or `.csv`
* Can extend to include **behavioral features** (Compound/Aave borrowing, liquidation, etc.)

---

## 📁 Output

* `compound_wallet_data.csv`: Token holdings & USD values
* `wallet_scores.csv`: Final risk score per wallet
