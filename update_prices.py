#!/usr/bin/env python3
import urllib.request
import json
import ssl
from datetime import datetime, timezone, timedelta

COINS = ["BTC", "ETH", "SOL"]

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def get_prices():
    url = "https://api.hyperliquid.xyz/info"
    data = json.dumps({"type": "allMids"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    with urllib.request.urlopen(req, context=get_ssl_context()) as response:
        return json.loads(response.read().decode("utf-8"))

def format_price(price):
    p = float(price)
    if p >= 1000:
        return f"${p:,.2f}"
    elif p >= 1:
        return f"${p:.2f}"
    else:
        return f"${p:.4f}"

def update_readme(prices):
    # KST 시간
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).strftime("%Y-%m-%d %H:%M KST")

    rows = []
    for coin in COINS:
        price = prices.get(coin, "N/A")
        if price != "N/A":
            formatted = format_price(price)
            rows.append(f"| {coin} | {formatted} | - |")
        else:
            rows.append(f"| {coin} | N/A | - |")

    table_content = "\n".join(rows)

    readme = f"""# 🚀 Crypto Portfolio

실시간 암호화폐 가격 트래커 (Hyperliquid)

## 💰 현재 가격

| 코인 | 가격 (USD) | 24h 변동 |
|------|-----------|----------|
{table_content}

> 마지막 업데이트: {now}

## 📊 트래킹 코인

- **BTC** - Bitcoin
- **ETH** - Ethereum
- **SOL** - Solana

## ⚙️ 자동 업데이트

GitHub Actions로 1시간마다 자동 업데이트됩니다.

---

*Powered by [Hyperliquid API](https://hyperliquid.xyz)*
"""

    with open("README.md", "w") as f:
        f.write(readme)

    print(f"✅ README 업데이트 완료: {now}")
    for coin in COINS:
        price = prices.get(coin, "N/A")
        if price != "N/A":
            print(f"   {coin}: {format_price(price)}")

if __name__ == "__main__":
    prices = get_prices()
    update_readme(prices)
