#!/usr/bin/env python3
"""
Upwork案件監視システム メインコントローラー
全機能統合実行
"""

import sys
import os
from scraper import UpworkScraper
from analyzer import UpworkAnalyzer
from notifier import UpworkNotifier
from datetime import datetime

class UpworkTracker:
    def __init__(self):
        self.scraper = UpworkScraper()
        self.analyzer = UpworkAnalyzer()
        self.notifier = UpworkNotifier()
        
    def run_full_cycle(self):
        """完全サイクル実行"""
        print("🚀 Upwork案件監視システム開始")
        print(f"⏰ 実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: 案件収集
        print("\n📡 Step 1: 案件データ収集")
        jobs = self.scraper.run_collection()
        
        # Step 2: データ分析
        print("\n📊 Step 2: データ分析・レポート生成")
        report = self.analyzer.generate_report()
        self.analyzer.save_report(report)
        
        # Step 3: 高スコア案件通知
        print("\n🔔 Step 3: 高スコア案件チェック・通知")
        notification_sent = self.notifier.run_notification_check()
        
        # 完了サマリー
        print(f"\n✅ 監視サイクル完了")
        print(f"📈 収集案件数: {len(jobs)}")
        print(f"🎯 高スコア案件: {len([j for j in jobs if j.takawasi_score >= 70])}")
        print(f"🔔 通知送信: {'あり' if notification_sent else 'なし'}")
        
        return {
            "jobs_collected": len(jobs),
            "high_score_jobs": len([j for j in jobs if j.takawasi_score >= 70]),
            "notification_sent": notification_sent
        }
    
    def run_quick_check(self):
        """クイックチェック (分析・通知のみ)"""
        print("⚡ クイックチェック実行")
        
        # 既存データの分析
        report = self.analyzer.generate_report()
        print(report)
        
        # 通知チェック
        self.notifier.run_notification_check()

if __name__ == "__main__":
    tracker = UpworkTracker()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        tracker.run_quick_check()
    else:
        tracker.run_full_cycle()
