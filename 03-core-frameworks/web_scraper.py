#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_prices(self, urls, selectors):
        """価格情報取得 - EC比較案件対応"""
        results = []
        
        for url in urls:
            try:
                response = self.session.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                data = {'url': url, 'timestamp': datetime.now().isoformat()}
                
                for key, selector in selectors.items():
                    element = soup.select_one(selector)
                    data[key] = element.text.strip() if element else None
                
                results.append(data)
                time.sleep(1)  # レート制限対応
                
            except Exception as e:
                results.append({'url': url, 'error': str(e)})
        
        return results
    
    def save_results(self, results, filename=None):
        """結果保存"""
        if not filename:
            filename = f"scraping_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return filename

# 使用例設定ファイル
scraping_config = {
    "ec_price_comparison": {
        "urls": [
            "https://example-shop1.com/product/123",
            "https://example-shop2.com/product/123"
        ],
        "selectors": {
            "title": ".product-title",
            "price": ".price",
            "availability": ".stock-status"
        }
    }
}

with open('scraping_config.json', 'w') as f:
    json.dump(scraping_config, f, indent=2)
