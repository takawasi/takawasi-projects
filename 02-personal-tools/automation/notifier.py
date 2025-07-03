#!/usr/bin/env python3
"""
Upwork案件通知システム
高スコア案件発見時の自動通知
"""

import json
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import os
from datetime import datetime

class UpworkNotifier:
    def __init__(self):
        self.notification_threshold = 80  # 80点以上で通知
        
    def check_high_score_jobs(self):
        """高スコア案件チェック"""
        try:
            with open("data/jobs.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            high_score_jobs = [job for job in data['jobs'] 
                             if job['takawasi_score'] >= self.notification_threshold]
            
            return high_score_jobs
        except FileNotFoundError:
            return []
    
    def format_notification_message(self, jobs):
        """通知メッセージ作成"""
        if not jobs:
            return "注目案件はありません"
            
        message = f"""
🚨 高スコア案件アラート ({len(jobs)}件)
発見時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        for job in sorted(jobs, key=lambda x: x['takawasi_score'], reverse=True):
            message += f"""
🎯 [{job['takawasi_score']:.1f}点] {job['title']}
💰 予算: ${job['budget_amount']:.0f}/{job['budget_type']}
👥 提案数: {job['proposals']}件
⭐ クライアント: {job['client_rating']:.1f}★ ({job['client_location']})
📝 説明: {job['description'][:100]}...

"""
        
        return message
    
    def send_terminal_notification(self, message):
        """ターミナル通知"""
        print("=" * 50)
        print(message)
        print("=" * 50)
    
    def send_file_notification(self, message, filename="logs/notifications.log"):
        """ファイル通知ログ"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(message)
            f.write(f"\n{'='*50}\n")
    
    def run_notification_check(self):
        """通知チェック実行"""
        high_score_jobs = self.check_high_score_jobs()
        
        if high_score_jobs:
            message = self.format_notification_message(high_score_jobs)
            self.send_terminal_notification(message)
            self.send_file_notification(message)
            return True
        else:
            print("📋 現在、通知対象の高スコア案件はありません")
            return False

if __name__ == "__main__":
    notifier = UpworkNotifier()
    notifier.run_notification_check()
