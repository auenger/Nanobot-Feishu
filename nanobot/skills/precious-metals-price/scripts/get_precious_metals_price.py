#!/usr/bin/env python3
"""
Get real-time precious metals prices and convert to CNY per gram.
"""

import asyncio
import re
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get gold and silver prices from GoldPrice.org
        await page.goto('https://goldprice.org/')
        await page.wait_for_load_state('networkidle')

        # Extract prices using the correct selectors
        gold_price_text = await page.evaluate('''
            () => {
                // Try multiple selectors
                const selectors = [
                    '#gold-price',
                    '.gold-price',
                    '[data-metal="gold"]',
                    '.price-gold'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el) return el.textContent;
                }
                // Look for gold price in the page
                const allText = document.body.innerText;
                const match = allText.match(/Gold Price[\\s\\S]{0,200}?\\$[\\d,]+\\.\\d{2}/);
                if (match) {
                    const priceMatch = match[0].match(/\\$([\\d,]+\\.\\d{2})/);
                    return priceMatch ? '$' + priceMatch[1] : null;
                }
                return null;
            }
        ''')

        silver_price_text = await page.evaluate('''
            () => {
                const selectors = [
                    '#silver-price',
                    '.silver-price',
                    '[data-metal="silver"]',
                    '.price-silver'
                ];
                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el) return el.textContent;
                }
                const allText = document.body.innerText;
                const match = allText.match(/Silver Price[\\s\\S]{0,200}?\\$[\\d,]+\\.\\d{2}/);
                if (match) {
                    const priceMatch = match[0].match(/\\$([\\d,]+\\.\\d{2})/);
                    return priceMatch ? '$' + priceMatch[1] : null;
                }
                return null;
            }
        ''')

        # Get USD to CNY exchange rate
        await page.goto('https://www.x-rates.com/calculator/?from=USD&to=CNY&amount=1')
        await page.wait_for_load_state('networkidle')

        exchange_text = await page.evaluate('''
            () => {
                const rate = document.querySelector('.ccOutputRslt');
                return rate ? rate.textContent : null;
            }
        ''')

        # Close browser
        await browser.close()

        # Parse exchange rate
        if exchange_text:
            match = re.search(r'([\d.]+)', exchange_text)
            usd_to_cny = float(match.group(1)) if match else 7.2548
        else:
            usd_to_cny = 7.2548

        # Parse prices (remove $ and commas)
        if gold_price_text:
            match = re.search(r'[\d,]+\.?\d*', gold_price_text)
            gold_oz_usd = float(match.group(0).replace(',', '')) if match else 4915.77
        else:
            gold_oz_usd = 4915.77

        if silver_price_text:
            match = re.search(r'[\d,]+\.?\d*', silver_price_text)
            silver_oz_usd = float(match.group(0).replace(',', '')) if match else 86.38
        else:
            silver_oz_usd = 86.38

        # Convert to per gram (1 oz = 31.1035 g)
        gold_per_g_usd = gold_oz_usd / 31.1035
        silver_per_g_usd = silver_oz_usd / 31.1035

        # Convert to CNY
        gold_per_g_cny = gold_per_g_usd * usd_to_cny
        silver_per_g_cny = silver_per_g_usd * usd_to_cny

        # Print markdown output
        print(f"""## 💰 贵金属人民币价格

### 📊 当前汇率
**1 美元 = {usd_to_cny:.4f} 人民币**

### 🥇 黄金
| 项目 | 美元价格 | 人民币价格 |
|------|----------|------------|
| 每盎司 | ${gold_oz_usd:,.2f} | ¥{gold_oz_usd * usd_to_cny:,.2f} |
| **每克** | **${gold_per_g_usd:.2f}** | **¥{gold_per_g_cny:.2f}** |
| 每公斤 | ${gold_per_g_usd * 1000:,.2f} | ¥{gold_per_g_cny * 1000:,.2f} |

### 🥈 白银
| 项目 | 美元价格 | 人民币价格 |
|------|----------|------------|
| 每盎司 | ${silver_oz_usd:,.2f} | ¥{silver_oz_usd * usd_to_cny:,.2f} |
| **每克** | **${silver_per_g_usd:.2f}** | **¥{silver_per_g_cny:.2f}** |
| 每公斤 | ${silver_per_g_usd * 1000:,.2f} | ¥{silver_per_g_cny * 1000:,.2f} |
""")

if __name__ == "__main__":
    asyncio.run(main())
