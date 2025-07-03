#!/usr/bin/env python3
"""
takawasi営業メトリクス追跡システム
"""

import pandas as pd
from datetime import datetime
import json

class SalesTracker:
    def __init__(self):
        self.proposals = []
        self.projects = []
        
    def add_proposal(self, client, project_type, rate, status="sent"):
        proposal = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'client': client,
            'project_type': project_type,
            'rate': rate,
            'status': status
        }
        self.proposals.append(proposal)
        print(f"✅ 提案追加: {client} - {project_type} (${rate}/hour)")
        
    def add_project(self, client, project_type, rate, hours, status="completed"):
        project = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'client': client,
            'project_type': project_type,
            'rate': rate,
            'hours': hours,
            'revenue': rate * hours,
            'status': status
        }
        self.projects.append(project)
        print(f"✅ プロジェクト完了: {client} - ${rate * hours:.0f}")
        
    def get_metrics(self):
        if not self.proposals and not self.projects:
            return "データがありません"
            
        metrics = {}
        
        if self.proposals:
            metrics['提案数'] = len(self.proposals)
            
        if self.projects:
            total_revenue = sum(p['revenue'] for p in self.projects)
            total_hours = sum(p['hours'] for p in self.projects)
            avg_rate = total_revenue / total_hours if total_hours > 0 else 0
            
            metrics.update({
                '完了プロジェクト': len(self.projects),
                '総収益': f"${total_revenue:,.0f}",
                '平均時給': f"${avg_rate:.0f}",
                '総作業時間': f"{total_hours:.1f}時間"
            })
            
            if self.proposals:
                success_rate = len(self.projects) / len(self.proposals) * 100
                metrics['成約率'] = f"{success_rate:.1f}%"
        
        return metrics
    
    def save_data(self, filename="sales_data.json"):
        data = {
            'proposals': self.proposals,
            'projects': self.projects,
            'last_updated': datetime.now().isoformat()
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 データ保存完了: {filename}")
    
    def load_data(self, filename="sales_data.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.proposals = data.get('proposals', [])
            self.projects = data.get('projects', [])
            print(f"📂 データ読み込み完了: {filename}")
        except FileNotFoundError:
            print(f"⚠️ ファイルが見つかりません: {filename}")

# 使用例とテストデータ
if __name__ == "__main__":
    tracker = SalesTracker()
    
    print("📊 takawasi営業メトリクス追跡システム")
    print("=" * 40)
    
    # サンプルデータ追加
    tracker.add_proposal("TechCorp", "Data Analysis", 85, "accepted")
    tracker.add_proposal("StartupXYZ", "System Monitoring", 95, "sent")
    tracker.add_proposal("BigRetail", "Web Scraping", 70, "accepted")
    
    tracker.add_project("TechCorp", "Data Analysis", 85, 8, "completed")
    tracker.add_project("BigRetail", "Web Scraping", 70, 6, "completed")
    
    print("\n📈 現在のメトリクス:")
    print("-" * 30)
    metrics = tracker.get_metrics()
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    # データ保存
    tracker.save_data()
    
    print("\n🎯 営業状況サマリー:")
    print("- 提案活動: 積極的")
    print("- 成約率: 良好")
    print("- 収益: 順調")
    print("- 次のアクション: 新規提案継続")
