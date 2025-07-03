#!/usr/bin/env python3
"""
takawasi Projects 統合管理システム
全プロジェクトの概要・ステータス・実行管理
"""

import json
import os
from datetime import datetime

class ProjectManager:
    def __init__(self):
        self.db_file = "projects_database.json"
        self.projects_root = "/mnt/c/Users/heint/Desktop/takawasi_projects"
        # データベース初期化
        self.initialize_database()
        
    def initialize_database(self):
        """データベース初期化"""
        if not os.path.exists(self.db_file):
            initial_data = {
                "last_updated": datetime.now().isoformat(),
                "projects": {
                    "upwork_monitor_personal": {
                        "category": "02_personal_tools",
                        "name": "Upwork案件監視システム (個人用)",
                        "status": "稼働中",
                        "type": "営業自動化",
                        "language": "Python",
                        "last_used": "2025-07-03",
                        "priority": "高",
                        "description": "Upwork案件の自動収集・分析・通知システム。takawasi営業活動の効率化。",
                        "location": "02_personal_tools/monitoring/upwork_monitor_personal",
                        "commands": {
                            "run": "python3 src/main.py --quick",
                            "analyze": "python3 src/analyzer.py",
                            "config": "nano config/settings.json"
                        },
                        "value": "年間334時間節約、営業効率向上"
                    },
                    "upwork_monitor_demo": {
                        "category": "01_client_demos",
                        "name": "Upwork案件監視システム (デモ版)",
                        "status": "展示用",
                        "type": "営業材料",
                        "language": "Python", 
                        "last_used": "2025-07-03",
                        "priority": "中",
                        "description": "クライアント向けデモ。Built this already. Want it?営業用システム。",
                        "location": "01_client_demos/demos/upwork_monitor_demo",
                        "commands": {
                            "demo": "python3 src/main.py",
                            "show": "cat README_SALES.md"
                        },
                        "value": "$300-800 営業材料、技術力証明"
                    },
                    "claude_wsl_powerhouse": {
                        "category": "04_wsl_projects",
                        "name": "Claude×WSL2協働開発環境",
                        "status": "完成",
                        "type": "開発基盤",
                        "language": "Python",
                        "last_used": "2025-07-03",
                        "priority": "高",
                        "description": "AI協働開発環境実証プロジェクト。WSL2統合開発システム。",
                        "location": "04_wsl_projects/ai-dev-environment",
                        "commands": {
                            "run": "python3 src/main.py",
                            "test": "python3 tests/test_integration.py"
                        },
                        "value": "開発効率25-45倍向上実証"
                    },
                    "takawasi_portfolio": {
                        "category": "01_client_demos",
                        "name": "takawasi収益化ポートフォリオ",
                        "status": "稼働中",
                        "type": "営業システム",
                        "language": "Python",
                        "last_used": "2025-07-03", 
                        "priority": "最高",
                        "description": "収益化特化システム。完品営業・価格設定・メトリクス管理。",
                        "location": "01_client_demos",
                        "commands": {
                            "demo": "find . -name 'professional_demo.py' -exec python3 {} +",
                            "track": "find . -name 'sales_tracker.py' -exec python3 {} +"
                        },
                        "value": "$65-200/時間 収益化システム"
                    }
                }
            }
            
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, ensure_ascii=False)
    
    def load_projects(self):
        """プロジェクトデータベース読み込み"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"projects": {}}
    
    def show_overview(self):
        """プロジェクト概要表示"""
        data = self.load_projects()
        projects = data.get("projects", {})
        
        print("🎯 takawasi Projects Overview")
        print("=" * 50)
        print(f"📅 最終更新: {data.get('last_updated', 'Unknown')}")
        print(f"📊 総プロジェクト数: {len(projects)}")
        print()
        
        # カテゴリ別表示
        categories = {
            "01_client_demos": "🎪 クライアント向けデモ",
            "02_personal_tools": "🔧 個人用ツール", 
            "03_core_frameworks": "⚡ コア骨格システム",
            "04_wsl_projects": "🐧 WSL協働プロジェクト",
            "05_experiments": "🧪 実験プロジェクト"
        }
        
        for cat_id, cat_name in categories.items():
            cat_projects = [p for p in projects.values() if p.get("category") == cat_id]
            if cat_projects:
                print(f"{cat_name} ({len(cat_projects)}件)")
                for project in cat_projects:
                    status_icon = "✅" if project["status"] == "稼働中" else "📋" if project["status"] == "完成" else "🎭"
                    priority_icon = "🔥" if project["priority"] == "最高" else "⭐" if project["priority"] == "高" else "📌"
                    print(f"  {status_icon}{priority_icon} {project['name']}")
                    print(f"    💡 {project['description']}")
                    print(f"    💰 価値: {project['value']}")
                    print()
    
    def show_active_projects(self):
        """稼働中プロジェクト表示"""
        data = self.load_projects()
        projects = data.get("projects", {})
        
        active = [p for p in projects.values() if p["status"] == "稼働中"]
        
        print("🚀 稼働中プロジェクト")
        print("=" * 30)
        
        for project in active:
            print(f"📋 {project['name']}")
            print(f"   📂 場所: {project['category']}")
            if "run" in project.get("commands", {}):
                print(f"   ▶️  実行: {project['commands']['run']}")
            print(f"   💰 価値: {project['value']}")
            print()
    
    def quick_access_menu(self):
        """クイックアクセスメニュー"""
        print("⚡ クイックアクセス")
        print("=" * 20)
        print("1. Upwork監視 (個人用)")
        print("2. Upwork監視 (デモ版)")
        print("3. 収益化ポートフォリオ")
        print("4. WSL協働開発環境")
        print("5. 全プロジェクト概要")
        print("0. 終了")
        
        choice = input("\n選択してください (0-5): ")
        
        commands = {
            "1": "cd 02_personal_tools/monitoring/upwork_monitor_personal && python3 src/main.py --quick",
            "2": "cd 01_client_demos/demos/upwork_monitor_demo && python3 src/main.py",
            "3": "cd 01_client_demos && find . -name 'professional_demo.py' -exec python3 {} +",
            "4": "cd 04_wsl_projects && find . -name 'main.py' -exec python3 {} +",
            "5": ""
        }
        
        if choice in commands:
            if choice == "5":
                self.show_overview()
            elif choice == "0":
                print("👋 管理システム終了")
                return
            else:
                print(f"\n🚀 実行コマンド: {commands[choice]}")
                print("📋 上記コマンドをコピーして実行してください")
        else:
            print("❌ 無効な選択です")

if __name__ == "__main__":
    manager = ProjectManager()
    print("🎯 takawasi Projects 統合管理システム")
    print()
    manager.show_overview()
    print()
    manager.show_active_projects()
    print()
    manager.quick_access_menu()
