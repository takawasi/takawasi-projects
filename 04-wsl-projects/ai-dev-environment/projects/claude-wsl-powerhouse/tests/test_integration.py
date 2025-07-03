#!/usr/bin/env python3
"""
統合テストスイート
WSL2環境での動作確認
"""

import unittest
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from main import ClaudeWSLPowerhouse
except ImportError:
    print("main.pyのインポートに失敗しました")
    sys.exit(1)

class TestClaudeWSLIntegration(unittest.TestCase):
    def setUp(self):
        self.powerhouse = ClaudeWSLPowerhouse()
    
    def test_system_info(self):
        """システム情報取得テスト"""
        info = self.powerhouse.system_info()
        self.assertIn("OS", info)
        self.assertIn("Python", info)
        self.assertIn("User", info)
    
    def test_project_initialization(self):
        """プロジェクト初期化テスト"""
        self.assertIsNotNone(self.powerhouse.project_name)
        self.assertIsNotNone(self.powerhouse.start_time)

if __name__ == "__main__":
    print("統合テストスイート実行")
    unittest.main()
