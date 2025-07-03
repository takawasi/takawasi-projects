#!/usr/bin/env python3
"""
Upwork案件分析システム
データ分析・トレンド・レポート生成
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import Counter
import os

class UpworkAnalyzer:
    def __init__(self):
        self.data_file = "data/jobs.json"
        
    def load_data(self):
        """データ読み込み"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data['jobs'])
        except FileNotFoundError:
            print(f"⚠️  データファイルが見つかりません: {self.data_file}")
            return pd.DataFrame()
    
    def analyze_price_trends(self, df):
        """価格動向分析"""
        if df.empty:
            return {}
            
        # 時間単価案件の分析
        hourly_jobs = df[df['budget_type'] == 'hourly']
        fixed_jobs = df[df['budget_type'] == 'fixed']
        
        analysis = {
            "hourly_stats": {
                "count": len(hourly_jobs),
                "avg_rate": hourly_jobs['budget_amount'].mean() if len(hourly_jobs) > 0 else 0,
                "median_rate": hourly_jobs['budget_amount'].median() if len(hourly_jobs) > 0 else 0,
                "max_rate": hourly_jobs['budget_amount'].max() if len(hourly_jobs) > 0 else 0,
                "min_rate": hourly_jobs['budget_amount'].min() if len(hourly_jobs) > 0 else 0
            },
            "fixed_stats": {
                "count": len(fixed_jobs),
                "avg_budget": fixed_jobs['budget_amount'].mean() if len(fixed_jobs) > 0 else 0,
                "median_budget": fixed_jobs['budget_amount'].median() if len(fixed_jobs) > 0 else 0,
                "max_budget": fixed_jobs['budget_amount'].max() if len(fixed_jobs) > 0 else 0,
                "min_budget": fixed_jobs['budget_amount'].min() if len(fixed_jobs) > 0 else 0
            }
        }
        
        return analysis
    
    def analyze_competition(self, df):
        """競合状況分析"""
        if df.empty:
            return {}
            
        return {
            "avg_proposals": df['proposals'].mean(),
            "median_proposals": df['proposals'].median(), 
            "low_competition": len(df[df['proposals'] < 5]),  # 提案5件未満
            "high_competition": len(df[df['proposals'] > 20]),  # 提案20件超
            "total_jobs": len(df)
        }
    
    def get_top_opportunities(self, df, min_score=70, limit=10):
        """注目案件抽出"""
        if df.empty:
            return []
            
        top_jobs = df[df['takawasi_score'] >= min_score].nlargest(limit, 'takawasi_score')
        return top_jobs.to_dict('records')
    
    def generate_report(self):
        """総合レポート生成"""
        df = self.load_data()
        
        if df.empty:
            return "データが見つかりません"
            
        # 各種分析実行
        price_analysis = self.analyze_price_trends(df)
        competition_analysis = self.analyze_competition(df) 
        top_opportunities = self.get_top_opportunities(df)
        
        # レポート生成
        report = f"""
🎯 Upwork案件分析レポート
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 概要
- 総案件数: {len(df)}
- 高スコア案件 (70点以上): {len(df[df['takawasi_score'] >= 70])}
- 平均スコア: {df['takawasi_score'].mean():.1f}点

💰 価格動向
時間単価案件 ({price_analysis['hourly_stats']['count']}件):
- 平均時給: ${price_analysis['hourly_stats']['avg_rate']:.0f}
- 中央値: ${price_analysis['hourly_stats']['median_rate']:.0f}
- 範囲: ${price_analysis['hourly_stats']['min_rate']:.0f} - ${price_analysis['hourly_stats']['max_rate']:.0f}

固定価格案件 ({price_analysis['fixed_stats']['count']}件):
- 平均予算: ${price_analysis['fixed_stats']['avg_budget']:.0f}
- 中央値: ${price_analysis['fixed_stats']['median_budget']:.0f}

🏁 競合状況
- 平均提案数: {competition_analysis['avg_proposals']:.1f}件
- 低競合案件 (<5提案): {competition_analysis['low_competition']}件
- 高競合案件 (>20提案): {competition_analysis['high_competition']}件

🎯 注目案件 TOP 5:
"""
        
        for i, job in enumerate(top_opportunities[:5], 1):
            report += f"{i}. [{job['takawasi_score']:.1f}点] {job['title']}\n"
            report += f"   ${job['budget_amount']:.0f}/{job['budget_type']} | {job['proposals']}提案 | {job['client_location']}\n\n"
        
        return report
    
    def save_report(self, report, filename="reports/daily_report.txt"):
        """レポート保存"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"✅ レポート保存完了: {filename}")

if __name__ == "__main__":
    analyzer = UpworkAnalyzer()
    report = analyzer.generate_report()
    print(report)
    analyzer.save_report(report)
