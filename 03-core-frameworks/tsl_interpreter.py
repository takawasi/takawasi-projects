#!/usr/bin/env python3
# TSL基礎品詞システム実装

class TSLInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        
    def 実行(self, command):
        """TSL実行関数"""
        print(f"[TSL実行] {command}")
        return f"実行完了: {command}"
    
    def 作成(self, object_type, name):
        """TSLオブジェクト作成"""
        self.variables[name] = {"type": object_type, "value": None}
        return f"作成完了: {name} ({object_type})"
    
    def 設定(self, name, value):
        """TSL値設定"""
        if name in self.variables:
            self.variables[name]["value"] = value
            return f"設定完了: {name} = {value}"
        return f"エラー: 変数 {name} が存在しません"
    
    def 取得(self, name):
        """TSL値取得"""
        if name in self.variables:
            return self.variables[name]["value"]
        return f"エラー: 変数 {name} が存在しません"
    
    def parse_and_execute(self, tsl_code):
        """TSLコード解析・実行"""
        lines = tsl_code.strip().split('\n')
        results = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # 簡易構文解析
            if '作成(' in line:
                # 例: 作成("変数", "test_var")
                parts = line.replace('作成(', '').replace(')', '').split(',')
                if len(parts) >= 2:
                    obj_type = parts[0].strip().strip('"')
                    name = parts[1].strip().strip('"')
                    result = self.作成(obj_type, name)
                    results.append(result)
            
            elif '設定(' in line:
                # 例: 設定("test_var", "Hello World")
                parts = line.replace('設定(', '').replace(')', '').split(',', 1)
                if len(parts) >= 2:
                    name = parts[0].strip().strip('"')
                    value = parts[1].strip().strip('"')
                    result = self.設定(name, value)
                    results.append(result)
                    
            elif '実行(' in line:
                # 例: 実行("echo Hello")
                command = line.replace('実行(', '').replace(')', '').strip().strip('"')
                result = self.実行(command)
                results.append(result)
        
        return results

# TSLテストコード
if __name__ == "__main__":
    interpreter = TSLInterpreter()
    
    test_code = '''
作成("文字列", "greeting")
設定("greeting", "Hello WSL World!")
実行("echo TSL動作確認")
'''
    
    print("🚀 TSL基礎インタープリター実行開始")
    results = interpreter.parse_and_execute(test_code)
    
    for result in results:
        print(f"  ✅ {result}")
    
    print("\n📊 変数状態:")
    for name, var in interpreter.variables.items():
        print(f"  {name}: {var}")
