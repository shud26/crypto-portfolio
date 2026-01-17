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

COIN_INFO = {
    "BTC": "비트코인",
    "ETH": "이더리움",
    "SOL": "솔라나"
}

def update_readme(prices):
    # KST 시간
    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst).strftime("%Y-%m-%d %H:%M KST")

    rows = []
    for coin in COINS:
        price = prices.get(coin, "N/A")
        name = COIN_INFO.get(coin, coin)
        if price != "N/A":
            formatted = format_price(price)
            rows.append(f"| {coin} | {formatted} | {name} |")
        else:
            rows.append(f"| {coin} | N/A | {name} |")

    table_content = "\n".join(rows)

    readme = f"""# 🚀 암호화폐 포트폴리오

Hyperliquid 거래소 기준 실시간 암호화폐 가격을 추적합니다.

## 💰 현재 가격

| 코인 | 가격 (USD) | 설명 |
|------|-----------|------|
{table_content}

> 📅 마지막 업데이트: {now}

## 📊 추적 중인 코인

| 코인 | 이름 | 설명 |
|------|------|------|
| BTC | 비트코인 | 최초의 암호화폐, 디지털 금 |
| ETH | 이더리움 | 스마트 컨트랙트 플랫폼 |
| SOL | 솔라나 | 고속 블록체인 네트워크 |

## ⚙️ 자동 업데이트

- GitHub Actions를 통해 **매 시간** 자동으로 가격이 업데이트됩니다
- 수동 업데이트: Actions 탭 → "Update Crypto Prices" → "Run workflow"

## 🛠️ 기술 스택

- **데이터 소스**: [Hyperliquid API](https://hyperliquid.xyz)
- **자동화**: GitHub Actions
- **언어**: Python 3.11

---

*이 포트폴리오는 [Claude Code](https://claude.ai)와 함께 만들었습니다* 🤖
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
