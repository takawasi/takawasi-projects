#!/usr/bin/env python3
"""
takawasi個人開発分析ダッシュボード
dev-analytics-dashboard

Git活動分析・コード品質分析・生産性可視化システム
"""

import os
import subprocess
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import re
from pathlib import Path
from collections import Counter, defaultdict
import sys

class DevAnalyticsDashboard:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.path.expanduser("~")
        self.git_repos = []
        self.analysis_data = {}
        self.output_dir = "analytics_output"
        
        # takawasi語録リスト（コミットメッセージ分析用）
        self.takawasi_keywords = [
            "電撃戦", "現場猫", "グデーリアン", "一撃", "完璧",
            "TSL", "takawasi", "ヨシ", "エラーなし", "品質管理",
            "AI協働", "WSL", "Claude", "収益化", "営業"
        ]
        
        # ファイル拡張子と言語のマッピング
        self.language_mapping = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript', 
            '.cpp': 'C++',
            '.c': 'C',
            '.java': 'Java',
            '.sh': 'Bash',
            '.md': 'Markdown',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.yml': 'YAML',
            '.yaml': 'YAML'
        }
    
    def discover_git_repositories(self):
        """Git リポジトリの自動発見"""
        print("🔍 Git リポジトリを検索中...")
        
        git_repos = []
        
        # ホームディレクトリから検索
        for root, dirs, files in os.walk(self.base_dir):
            # .git ディレクトリを発見した場合
            if '.git' in dirs:
                repo_path = root
                repo_name = os.path.basename(repo_path)
                
                # .vscode-server など除外
                if not any(skip in repo_path for skip in ['.vscode', 'node_modules', '__pycache__']):
                    git_repos.append({
                        'name': repo_name,
                        'path': repo_path,
                        'relative_path': os.path.relpath(repo_path, self.base_dir)
                    })
                
                # サブディレクトリの .git は除外
                dirs.remove('.git')
        
        self.git_repos = git_repos
        print(f"✅ 発見したリポジトリ: {len(git_repos)}件")
        
        for repo in git_repos:
            print(f"  📁 {repo['name']} ({repo['relative_path']})")
        
        return git_repos
    
    def analyze_git_activity(self, repo_path):
        """Git活動分析"""
        try:
            os.chdir(repo_path)
            
            # Git log 取得 (最近30日)
            since_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            # コミット情報取得
            git_log_cmd = [
                'git', 'log', 
                f'--since={since_date}',
                '--pretty=format:%H|%an|%ad|%s|%ai',
                '--date=iso'
            ]
            
            result = subprocess.run(git_log_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return None
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        commit_hash, author, date, message, iso_date = parts
                        commits.append({
                            'hash': commit_hash,
                            'author': author,
                            'date': date,
                            'message': message,
                            'iso_date': iso_date,
                            'takawasi_keywords': [kw for kw in self.takawasi_keywords if kw in message]
                        })
            
            # ファイル統計取得
            stats_cmd = ['git', 'log', f'--since={since_date}', '--numstat', '--pretty=format:']
            stats_result = subprocess.run(stats_cmd, capture_output=True, text=True)
            
            file_changes = {'additions': 0, 'deletions': 0, 'files_changed': 0}
            
            if stats_result.returncode == 0:
                for line in stats_result.stdout.strip().split('\n'):
                    if line and '\t' in line:
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            additions = parts[0]
                            deletions = parts[1]
                            
                            if additions.isdigit():
                                file_changes['additions'] += int(additions)
                            if deletions.isdigit():
                                file_changes['deletions'] += int(deletions)
                            file_changes['files_changed'] += 1
            
            return {
                'commits': commits,
                'file_changes': file_changes,
                'total_commits': len(commits),
                'active_days': len(set(c['date'][:10] for c in commits))
            }
            
        except Exception as e:
            print(f"⚠️ Git分析エラー ({repo_path}): {e}")
            return None
    
    def analyze_code_quality(self, repo_path):
        """コード品質分析"""
        try:
            code_stats = {
                'total_files': 0,
                'total_lines': 0,
                'languages': defaultdict(int),
                'file_sizes': [],
                'python_complexity': {}
            }
            
            for root, dirs, files in os.walk(repo_path):
                # .git, __pycache__ などを除外
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    file_path = os.path.join(root, file)
                    file_ext = os.path.splitext(file)[1].lower()
                    
                    # 言語判定
                    language = self.language_mapping.get(file_ext, 'Other')
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            line_count = len(lines)
                            
                            code_stats['total_files'] += 1
                            code_stats['total_lines'] += line_count
                            code_stats['languages'][language] += line_count
                            code_stats['file_sizes'].append(line_count)
                            
                            # Python ファイルの場合、簡易複雑性分析
                            if file_ext == '.py':
                                complexity = self.analyze_python_complexity(lines)
                                code_stats['python_complexity'][file] = complexity
                                
                    except Exception:
                        continue
            
            return code_stats
            
        except Exception as e:
            print(f"⚠️ コード品質分析エラー ({repo_path}): {e}")
            return None
    
    def analyze_python_complexity(self, lines):
        """Python コードの簡易複雑性分析"""
        complexity_indicators = {
            'functions': 0,
            'classes': 0,
            'imports': 0,
            'comments': 0,
            'conditionals': 0,
            'loops': 0
        }
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('def '):
                complexity_indicators['functions'] += 1
            elif line.startswith('class '):
                complexity_indicators['classes'] += 1
            elif line.startswith('import ') or line.startswith('from '):
                complexity_indicators['imports'] += 1
            elif line.startswith('#'):
                complexity_indicators['comments'] += 1
            elif any(keyword in line for keyword in ['if ', 'elif ', 'else:']):
                complexity_indicators['conditionals'] += 1
            elif any(keyword in line for keyword in ['for ', 'while ']):
                complexity_indicators['loops'] += 1
        
        return complexity_indicators
    
    def generate_productivity_insights(self):
        """生産性インサイト生成"""
        insights = []
        total_commits = sum(data.get('total_commits', 0) for data in self.analysis_data.values())
        total_files = sum(data['code_quality'].get('total_files', 0) 
                         for data in self.analysis_data.values() 
                         if 'code_quality' in data)
        
        # 基本統計
        insights.append(f"📊 総コミット数: {total_commits}")
        insights.append(f"📁 総ファイル数: {total_files}")
        
        # 最もアクティブなリポジトリ
        if self.analysis_data:
            most_active = max(self.analysis_data.items(), 
                            key=lambda x: x[1].get('total_commits', 0))
            insights.append(f"🔥 最アクティブ: {most_active[0]} ({most_active[1].get('total_commits', 0)} commits)")
        
        # takawasi語録使用頻度
        keyword_usage = Counter()
        for data in self.analysis_data.values():
            if 'git_activity' in data:
                for commit in data['git_activity']['commits']:
                    keyword_usage.update(commit['takawasi_keywords'])
        
        if keyword_usage:
            top_keyword = keyword_usage.most_common(1)[0]
            insights.append(f"⚡ 頻出takawasi語録: '{top_keyword[0]}' ({top_keyword[1]}回)")
        
        # 言語別分析
        language_stats = defaultdict(int)
        for data in self.analysis_data.values():
            if 'code_quality' in data:
                for lang, lines in data['code_quality']['languages'].items():
                    language_stats[lang] += lines
        
        if language_stats:
            top_language = max(language_stats.items(), key=lambda x: x[1])
            insights.append(f"💻 主要言語: {top_language[0]} ({top_language[1]:,} lines)")
        
        # 改善提案
        insights.append("\n🎯 改善提案:")
        if total_commits < 10:
            insights.append("  • コミット頻度を上げて細かい進捗を記録しましょう")
        if keyword_usage.get('品質管理', 0) < keyword_usage.get('電撃戦', 0):
            insights.append("  • 品質管理への言及を増やすとバランスが良くなります")
        if language_stats.get('Markdown', 0) < language_stats.get('Python', 0) * 0.1:
            insights.append("  • ドキュメント作成（Markdown）を増やすと良いでしょう")
        
        return insights
    
    def create_visualizations(self):
        """可視化グラフ作成"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        plt.style.use('default')
        
        # 1. リポジトリ別コミット数
        plt.figure(figsize=(12, 6))
        
        repo_names = list(self.analysis_data.keys())
        commit_counts = [data.get('total_commits', 0) for data in self.analysis_data.values()]
        
        plt.subplot(2, 2, 1)
        plt.bar(repo_names, commit_counts, color='skyblue')
        plt.title('📊 リポジトリ別コミット数 (30日間)')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('コミット数')
        
        # 2. 言語別コード行数
        language_stats = defaultdict(int)
        for data in self.analysis_data.values():
            if 'code_quality' in data:
                for lang, lines in data['code_quality']['languages'].items():
                    language_stats[lang] += lines
        
        if language_stats:
            plt.subplot(2, 2, 2)
            languages = list(language_stats.keys())[:5]  # 上位5言語
            line_counts = [language_stats[lang] for lang in languages]
            plt.pie(line_counts, labels=languages, autopct='%1.1f%%')
            plt.title('💻 言語別コード行数')
        
        # 3. ファイルサイズ分布
        all_file_sizes = []
        for data in self.analysis_data.values():
            if 'code_quality' in data:
                all_file_sizes.extend(data['code_quality']['file_sizes'])
        
        if all_file_sizes:
            plt.subplot(2, 2, 3)
            plt.hist(all_file_sizes, bins=20, color='lightcoral', alpha=0.7)
            plt.title('📁 ファイルサイズ分布')
            plt.xlabel('行数')
            plt.ylabel('ファイル数')
        
        # 4. takawasi語録使用頻度
        keyword_usage = Counter()
        for data in self.analysis_data.values():
            if 'git_activity' in data:
                for commit in data['git_activity']['commits']:
                    keyword_usage.update(commit['takawasi_keywords'])
        
        if keyword_usage:
            plt.subplot(2, 2, 4)
            keywords = list(keyword_usage.keys())[:5]
            counts = [keyword_usage[kw] for kw in keywords]
            plt.bar(keywords, counts, color='lightgreen')
            plt.title('⚡ takawasi語録使用頻度')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('使用回数')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/dev_analytics_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ 可視化グラフ保存: {self.output_dir}/dev_analytics_dashboard.png")
    
    def export_detailed_report(self):
        """詳細レポート出力"""
        report_file = f"{self.output_dir}/dev_analytics_report.json"
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'analysis_period': '30 days',
            'repositories': self.analysis_data,
            'insights': self.generate_productivity_insights()
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 詳細レポート出力: {report_file}")
        
        # 簡易版レポート（コンソール出力）
        print("\n" + "="*60)
        print("🚀 takawasi開発分析ダッシュボード レポート")
        print("="*60)
        
        insights = self.generate_productivity_insights()
        for insight in insights:
            print(insight)
        
        print("\n📈 詳細データ:")
        for repo_name, data in self.analysis_data.items():
            print(f"\n📁 {repo_name}:")
            if 'git_activity' in data:
                git_data = data['git_activity']
                print(f"  • コミット数: {git_data['total_commits']}")
                print(f"  • アクティブ日数: {git_data['active_days']}")
                print(f"  • 追加行数: {git_data['file_changes']['additions']:,}")
                print(f"  • 削除行数: {git_data['file_changes']['deletions']:,}")
            
            if 'code_quality' in data:
                code_data = data['code_quality']
                print(f"  • ファイル数: {code_data['total_files']}")
                print(f"  • 総行数: {code_data['total_lines']:,}")
                
                if code_data['languages']:
                    top_lang = max(code_data['languages'].items(), key=lambda x: x[1])
                    print(f"  • 主要言語: {top_lang[0]} ({top_lang[1]:,} lines)")
    
    def run_analysis(self):
        """分析実行メイン"""
        print("🚀 takawasi開発分析ダッシュボード開始")
        print("="*50)
        
        # Git リポジトリ発見
        repositories = self.discover_git_repositories()
        
        if not repositories:
            print("❌ Git リポジトリが見つかりませんでした")
            return
        
        # 各リポジトリを分析
        for repo in repositories:
            print(f"\n📊 分析中: {repo['name']}")
            
            # Git 活動分析
            git_activity = self.analyze_git_activity(repo['path'])
            
            # コード品質分析
            code_quality = self.analyze_code_quality(repo['path'])
            
            self.analysis_data[repo['name']] = {
                'path': repo['path'],
                'git_activity': git_activity,
                'code_quality': code_quality,
                'total_commits': git_activity['total_commits'] if git_activity else 0
            }
            
            if git_activity:
                print(f"  ✅ Git分析完了: {git_activity['total_commits']} commits")
            if code_quality:
                print(f"  ✅ コード分析完了: {code_quality['total_files']} files")
        
        # 結果出力
        self.create_visualizations()
        self.export_detailed_report()
        
        print(f"\n🏆 分析完了! 結果は {self.output_dir}/ に保存されました")


def main():
    """メイン実行"""
    print("🎯 takawasi個人開発分析ダッシュボード")
    print("=" * 50)
    
    # ダッシュボード初期化・実行
    dashboard = DevAnalyticsDashboard()
    dashboard.run_analysis()
    
    print("\n💡 使用方法:")
    print("  • 可視化グラフ: analytics_output/dev_analytics_dashboard.png")
    print("  • 詳細レポート: analytics_output/dev_analytics_report.json")
    print("  • 定期実行推奨: 週1回程度")
    
    print("\n🚀 takawasi式開発分析完了!")
    print("⚡ 電撃戦最強！現場猫品質管理ヨシ！")


if __name__ == "__main__":
    main()