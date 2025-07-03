#!/usr/bin/env python3
"""
Upwork案件自動収集システム
takawasi専用カスタマイズ版
"""

import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import re
from dataclasses import dataclass, asdict
from typing import List, Dict
import os

@dataclass
class UpworkJob:
    id: str
    title: str
    description: str
    budget_type: str  # "fixed" or "hourly"
    budget_amount: float
    skills: List[str]
    posted: str
    proposals: int
    client_rating: float
    client_spent: float
    client_location: str
    takawasi_score: float = 0.0
    
class UpworkScraper:
    def __init__(self):
        self.search_keywords = ["python", "ai", "machine learning", "automation", "wsl", "linux", "data analysis"]
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def calculate_takawasi_score(self, job: UpworkJob) -> float:
        """takawasi適合度スコア計算 (100点満点)"""
        score = 0
        
        # スキル適合度 (40点満点)
        target_skills = ["python", "ai", "machine learning", "wsl", "linux", "automation", "data"]
        skill_matches = sum(1 for skill in target_skills 
                          if any(s.lower() in job.title.lower() + job.description.lower() 
                                for s in [skill]))
        score += min(skill_matches * 6, 40)
        
        # 価格適合度 (30点満点) 
        if job.budget_type == "hourly":
            rate = job.budget_amount
            if 65 <= rate <= 200:
                score += 30
            elif 50 <= rate < 65 or 200 < rate <= 250:
                score += 20
            else:
                score += 10
        else:  # fixed
            if job.budget_amount >= 500:
                score += 25
            elif job.budget_amount >= 200:
                score += 20
            else:
                score += 10
                
        # 競合状況 (20点満点)
        if job.proposals < 5:
            score += 20
        elif job.proposals < 15:
            score += 15
        elif job.proposals < 25:
            score += 10
        else:
            score += 5
            
        # クライアント品質 (10点満点)
        if job.client_rating >= 4.5:
            score += 10
        elif job.client_rating >= 4.0:
            score += 7
        else:
            score += 3
            
        return min(score, 100)
    
    def create_sample_jobs(self) -> List[UpworkJob]:
        """サンプル案件データ生成 (デモ・テスト用)"""
        sample_jobs = [
            UpworkJob(
                id="job_001",
                title="Python Data Analysis and Automation Script",
                description="Need a Python expert to create data analysis scripts with automation features. Must have experience with pandas, numpy, and web scraping.",
                budget_type="hourly",
                budget_amount=85.0,
                skills=["Python", "Data Analysis", "Automation", "Pandas"],
                posted="2025-07-03",
                proposals=3,
                client_rating=4.8,
                client_spent=15000.0,
                client_location="United States"
            ),
            UpworkJob(
                id="job_002", 
                title="AI/ML Model Development for Business Analytics",
                description="Looking for machine learning expert to develop predictive models. Python, scikit-learn, TensorFlow experience required.",
                budget_type="fixed",
                budget_amount=2500.0,
                skills=["Python", "Machine Learning", "AI", "TensorFlow"],
                posted="2025-07-03",
                proposals=12,
                client_rating=4.6,
                client_spent=8500.0,
                client_location="United Kingdom"
            ),
            UpworkJob(
                id="job_003",
                title="Linux System Administration and WSL2 Setup",
                description="Need help setting up WSL2 development environment and Linux system administration tasks.",
                budget_type="hourly", 
                budget_amount=75.0,
                skills=["Linux", "WSL", "System Administration"],
                posted="2025-07-03",
                proposals=8,
                client_rating=4.2,
                client_spent=3200.0,
                client_location="Canada"
            ),
            UpworkJob(
                id="job_004",
                title="Web Scraping and Data Collection",
                description="Build web scraping solution for e-commerce data collection. Python, BeautifulSoup, requests needed.",
                budget_type="fixed",
                budget_amount=800.0,
                skills=["Python", "Web Scraping", "BeautifulSoup", "Data Collection"],
                posted="2025-07-03",
                proposals=25,
                client_rating=3.9,
                client_spent=1200.0,
                client_location="Australia"
            ),
            UpworkJob(
                id="job_005",
                title="Custom Python Development and AI Integration",
                description="Develop custom Python application with AI features integration. Modern development practices required.",
                budget_type="hourly",
                budget_amount=120.0,
                skills=["Python", "AI", "Custom Development", "Integration"],
                posted="2025-07-03",
                proposals=6,
                client_rating=4.9,
                client_spent=25000.0,
                client_location="United States"
            )
        ]
        
        # スコア計算
        for job in sample_jobs:
            job.takawasi_score = self.calculate_takawasi_score(job)
            
        return sample_jobs
    
    def save_jobs(self, jobs: List[UpworkJob], filename: str = "data/jobs.json"):
        """案件データ保存"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        jobs_data = {
            "last_updated": datetime.datetime.now().isoformat(),
            "total_jobs": len(jobs),
            "jobs": [asdict(job) for job in jobs]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ {len(jobs)} jobs saved to {filename}")
    
    def load_jobs(self, filename: str = "data/jobs.json") -> List[UpworkJob]:
        """保存済み案件データ読み込み"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            jobs = []
            for job_data in data['jobs']:
                job = UpworkJob(**job_data)
                jobs.append(job)
                
            print(f"✅ {len(jobs)} jobs loaded from {filename}")
            return jobs
        except FileNotFoundError:
            print(f"⚠️  File {filename} not found")
            return []
    
    def run_collection(self):
        """案件収集実行"""
        print("🔍 Upwork案件収集開始...")
        
        # 現在はサンプルデータを使用 (実際のスクレイピングは後で実装)
        jobs = self.create_sample_jobs()
        
        # 高スコア案件のフィルタリング
        high_score_jobs = [job for job in jobs if job.takawasi_score >= 70]
        
        print(f"📊 収集結果: {len(jobs)} 案件中 {len(high_score_jobs)} 案件が高スコア (70点以上)")
        
        # データ保存
        self.save_jobs(jobs)
        
        return jobs

if __name__ == "__main__":
    scraper = UpworkScraper()
    jobs = scraper.run_collection()
    
    # 高スコア案件表示
    high_score = [j for j in jobs if j.takawasi_score >= 70]
    print(f"\n🎯 注目案件 ({len(high_score)} 件):")
    for job in sorted(high_score, key=lambda x: x.takawasi_score, reverse=True):
        print(f"  {job.takawasi_score:.1f}点 - {job.title} (${job.budget_amount}/{job.budget_type})")
