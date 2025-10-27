import json

class JSONHelper:
        
    def LoadFromFile(self, filename = 'input.json'):
        # JSONファイルを読み込む
        json_str = open(filename, 'r') 
        dic = self.LoadFromString(json_str)
        return dic
    
    def LoadFromString(self, json_str):
        # JSON文字列を辞書変数にロード
        dic = json.load(json_str) 
        #print('JSON Loaded:',dic)
        return dic
    
    def ConvertToStr(self, json_dict):
        # 辞書変数をJSON文字列に変換
        json_str = json.dumps(json_dict)
        return json_str
        
    def SaveToFile(self, target_dict, filename = 'output.json'):
        # 辞書変数をJSONとして保存
        with open(filename, mode="w", encoding="utf-8") as f:
            json.dump(target_dict, f)
            print('JSON saved', filename)