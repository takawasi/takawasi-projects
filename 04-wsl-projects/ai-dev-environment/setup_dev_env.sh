#!/bin/bash
# AI協働開発環境電撃セットアップ

echo "🚀 AI協働開発環境構築開始"

# 必須ツールインストール
sudo apt update
sudo apt install -y git curl wget build-essential python3 python3-pip nodejs npm

# VS Code WSL拡張対応確認
echo "✅ VS Code WSL拡張を確認してください"
echo "Remote - WSL拡張がインストール済みか確認"

# Git設定
git config --global user.name "takawasi"
git config --global user.email "takawasi@example.com"

# Claude連携用ディレクトリ構築
mkdir -p {projects,scripts,tools,docs}

# プロジェクトテンプレート作成
cat << 'TEMPLATE' > projects/template_project.py
#!/usr/bin/env python3
"""
AI協働開発テンプレート
Claude生成コード実行用
"""

def main():
    print("🤖 Claude & takawasi 協働プロジェクト")
    print("WSL2環境での電撃戦開発")

if __name__ == "__main__":
    main()
TEMPLATE

echo "🏆 AI協働開発環境構築完了"
echo "次コマンド: code . でVS Code起動"
