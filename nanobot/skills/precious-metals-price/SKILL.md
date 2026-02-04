---
name: precious-metals-price
description: Query real-time prices for precious metals (gold, silver, platinum, palladium) using Playwright and convert to CNY per gram. Use when user asks for: gold/silver prices, precious metals prices, 贵金属价格, 黄金价格, 白银价格, or similar queries.
---

# Precious Metals Price

Query real-time precious metals prices and convert to CNY per gram.

## Quick Start

Get gold and silver prices in CNY per gram:

```bash
cd /Users/ryan/mycode/Nanobot/nanobot/skills/precious-metals-price
python3 scripts/get_precious_metals_price.py
```

## How It Works

The script uses Playwright to:
1. Scrape real-time prices from GoldPrice.org (USD/oz)
2. Get USD to CNY exchange rate from x-rates.com
3. Convert to CNY per gram (1 oz = 31.1035 g)

## Output Format

The script returns a markdown table with:
- Gold and silver prices in USD and CNY
- Per ounce, per gram, and per kilogram prices
- Current exchange rate

## Requirements

- Python 3
- Playwright (`pip install playwright`)
- Chromium browser (`playwright install chromium`)
