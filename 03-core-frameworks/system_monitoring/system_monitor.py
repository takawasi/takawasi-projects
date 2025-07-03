#!/usr/bin/env python3
import psutil
import json
import time
from datetime import datetime
import subprocess

class SystemMonitor:
    def __init__(self):
        self.monitoring = True
    
    def get_system_stats(self):
        """システム統計取得"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free
            },
            'network': dict(psutil.net_io_counters()._asdict()),
            'processes': len(psutil.pids())
        }
    
    def check_wsl_performance(self):
        """WSL特有のパフォーマンス確認"""
        try:
            # Windows側メモリ使用量確認
            result = subprocess.run(['powershell.exe', '-Command', 
                                   'Get-Process | Where-Object {$_.ProcessName -eq "Vmmem"} | Select-Object WorkingSet'],
                                  capture_output=True, text=True)
            wsl_memory = result.stdout.strip() if result.returncode == 0 else "N/A"
            
            return {
                'wsl_memory_usage': wsl_memory,
                'wsl_processes': len([p for p in psutil.process_iter() if 'wsl' in p.name().lower()])
            }
        except:
            return {'wsl_info': 'Unable to retrieve WSL-specific info'}
    
    def generate_alert(self, stats):
        """アラート生成"""
        alerts = []
        
        if stats['cpu_percent'] > 80:
            alerts.append(f"High CPU usage: {stats['cpu_percent']}%")
        
        if stats['memory']['percent'] > 85:
            alerts.append(f"High memory usage: {stats['memory']['percent']}%")
        
        if psutil.disk_usage('/').percent > 90:
            alerts.append(f"High disk usage: {psutil.disk_usage('/').percent}%")
        
        return alerts
    
    def monitor_loop(self, duration=60, interval=5):
        """監視ループ"""
        start_time = time.time()
        results = []
        
        while time.time() - start_time < duration:
            stats = self.get_system_stats()
            wsl_info = self.check_wsl_performance()
            alerts = self.generate_alert(stats)
            
            entry = {
                'stats': stats,
                'wsl_info': wsl_info,
                'alerts': alerts
            }
            
            results.append(entry)
            
            if alerts:
                print(f"⚠️  ALERT: {', '.join(alerts)}")
            else:
                print(f"✅ System OK - CPU: {stats['cpu_percent']}%, RAM: {stats['memory']['percent']}%")
            
            time.sleep(interval)
        
        # 結果保存
        report_file = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        return report_file

if __name__ == "__main__":
    monitor = SystemMonitor()
    print("🚀 WSL System Monitor 開始")
    report = monitor.monitor_loop(duration=300, interval=10)  # 5分間監視
    print(f"📊 監視完了: {report}")
