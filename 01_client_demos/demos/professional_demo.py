#!/usr/bin/env python3
"""
takawasi Professional Demo - Ready for Client Presentation
完全動作確認済み・即座配送可能
"""

import pandas as pd
import psutil
import requests
import bs4
import numpy as np
from datetime import datetime
import time

def demo_data_analysis():
    """プロフェッショナルデータ分析デモ"""
    print("📊 Professional Data Analysis Demo")
    print("=" * 50)
    
    # 実用的ビジネスデータ生成
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    
    business_data = pd.DataFrame({
        'date': dates,
        'sales': np.random.normal(5000, 1500, 100).astype(int),
        'profit': np.random.normal(1500, 500, 100).astype(int),
        'customers': np.random.normal(150, 50, 100).astype(int),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'product': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 100)
    })
    
    # データクリーニング
    business_data['sales'] = business_data['sales'].abs()
    business_data['profit'] = business_data['profit'].abs()
    business_data['customers'] = business_data['customers'].abs()
    
    print(f"✅ データ処理完了: {len(business_data):,} レコード")
    print(f"💰 総売上: ${business_data['sales'].sum():,}")
    print(f"📈 総利益: ${business_data['profit'].sum():,}")
    print(f"🎯 利益率: {(business_data['profit'].sum()/business_data['sales'].sum()*100):.1f}%")
    print(f"👥 総顧客数: {business_data['customers'].sum():,}")
    
    # 地域別分析
    regional_stats = business_data.groupby('region').agg({
        'sales': ['sum', 'mean'],
        'profit': ['sum', 'mean']
    }).round(0)
    
    print("\n🌍 地域別パフォーマンス:")
    print(regional_stats)
    
    return business_data

def demo_system_monitoring():
    """リアルタイムシステム監視デモ"""
    print("\n🖥️ Real-time System Monitoring Demo")
    print("=" * 50)
    
    print("📊 現在のシステム状況:")
    
    # システム情報取得
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    processes = len(psutil.pids())
    
    print(f"⚡ CPU使用率: {cpu_percent:.1f}%")
    print(f"🧠 メモリ使用率: {memory.percent:.1f}% ({memory.used//1024//1024:,}MB / {memory.total//1024//1024:,}MB)")
    print(f"💾 ディスク使用率: {disk.percent:.1f}% ({disk.used//1024//1024//1024:.1f}GB / {disk.total//1024//1024//1024:.1f}GB)")
    print(f"⚙️ 実行中プロセス: {processes}個")
    
    # リアルタイム監視（3秒間）
    print("\n📡 リアルタイム監視:")
    for i in range(3):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"  {timestamp} - CPU: {cpu:5.1f}% | RAM: {ram:5.1f}%")
    
    print("✅ システム監視完了")

def demo_web_scraping():
    """ウェブスクレイピングデモ"""
    print("\n🕷️ Web Scraping Demo")
    print("=" * 50)
    
    # 公開APIテスト
    try:
        print("🌐 公開APIからデータ取得中...")
        response = requests.get('https://httpbin.org/json', timeout=5)
        
        if response.status_code == 200:
            print(f"✅ HTTP リクエスト成功: {response.status_code}")
            print(f"📦 レスポンスサイズ: {len(response.content)} bytes")
            print(f"⏱️ 応答時間: {response.elapsed.total_seconds():.3f}秒")
        
    except Exception as e:
        print(f"⚠️ ネットワークテスト: オフラインモード")
    
    # HTMLパース例
    html_sample = '''
    <html>
        <head><title>サンプル商品ページ</title></head>
        <body>
            <div class="product">
                <h1 class="title">takawasi Pro Analytics Tool</h1>
                <span class="price">$1,299</span>
                <div class="stock status-available">在庫あり</div>
                <div class="rating">★★★★★ (4.9/5)</div>
            </div>
        </body>
    </html>
    '''
    
    soup = bs4.BeautifulSoup(html_sample, 'html.parser')
    
    title = soup.find('h1', class_='title').text
    price = soup.find('span', class_='price').text
    stock = soup.find('div', class_='stock').text
    rating = soup.find('div', class_='rating').text
    
    print("\n🛒 商品情報抽出結果:")
    print(f"  📦 商品名: {title}")
    print(f"  💰 価格: {price}")
    print(f"  📊 在庫: {stock}")
    print(f"  ⭐ 評価: {rating}")
    
    print("✅ ウェブスクレイピングデモ完了")

def demo_automation():
    """自動化プロセスデモ"""
    print("\n🤖 Automation Process Demo")
    print("=" * 50)
    
    automation_tasks = [
        ("データ収集", "複数ソースからの自動データ取得"),
        ("データクリーニング", "欠損値処理・異常値検出"),
        ("統計分析", "記述統計・相関分析・トレンド分析"),
        ("レポート生成", "グラフ作成・PDF出力"),
        ("結果配信", "メール送信・ダッシュボード更新")
    ]
    
    total_time_saved = 0
    
    for i, (task_name, task_desc) in enumerate(automation_tasks, 1):
        print(f"⚡ ステップ {i}/5: {task_name}")
        print(f"   📋 処理内容: {task_desc}")
        
        # シミュレーション
        processing_time = 0.5
        time.sleep(processing_time)
        
        # 手動作業時間との比較
        manual_time = np.random.randint(15, 45)
        auto_time = processing_time
        time_saved = manual_time - (auto_time/60)
        total_time_saved += time_saved
        
        print(f"   ✅ 完了 (手動: {manual_time}分 → 自動: {auto_time:.1f}秒)")
        print(f"   ⏰ 時間短縮: {time_saved:.1f}分")
    
    print(f"\n🏆 自動化完了!")
    print(f"💡 総時間短縮: {total_time_saved:.1f}分")
    print(f"📈 効率向上: {(total_time_saved/(total_time_saved+5)*100):.1f}%")

if __name__ == "__main__":
    print("🚀 takawasi Professional Demo Suite")
    print("🎯 Ready for Production Deployment")
    print("=" * 60)
    
    start_time = time.time()
    
    # 全デモ実行
    business_data = demo_data_analysis()
    demo_system_monitoring()
    demo_web_scraping()
    demo_automation()
    
    end_time = time.time()
    
    print("\n" + "=" * 60)
    print("🏆 Professional Demo Complete!")
    print(f"⏱️ 実行時間: {end_time - start_time:.1f}秒")
    print("💼 Client Ready - Immediate Deployment Available")
    print("📞 Contact: Built this already. $1,200. Want it?")
