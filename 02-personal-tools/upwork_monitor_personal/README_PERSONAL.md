# Upwork案件監視システム - takawasi個人用

## 日常使用方法
```bash
# 朝の案件チェック
cd /mnt/c/Users/heint/Desktop/takawasi_projects/02_personal_tools/upwork_monitor_personal
python3 src/main.py --quick

# 詳細分析
python3 src/analyzer.py

# 設定調整
nano config/settings.json
```

## 定期実行設定
```bash
# crontab設定例
# 平日朝夕のチェック
0 9,17 * * 1-5 cd /mnt/c/Users/heint/Desktop/takawasi_projects/02_personal_tools/upwork_monitor_personal && python3 src/main.py --quick
```

## カスタマイズ履歴
- takawasi専用スコア基準
- 個人的優先キーワード
- 実際の応募・成約データ連携
- 収益最大化設定

STATUS: 個人用実用システム稼働中
