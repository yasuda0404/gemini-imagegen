import os
import sys
from dotenv import load_dotenv
import datetime

class EnvSettings:
    base_dir:str = os.path.dirname(__file__)
    
    def __init__(self, load_env: bool = False):
        if load_env:
            self.load_envvars()
    
    def get_absolute_path(self, relative_path: str) -> str:
        """相対パスから絶対パスを取得する。"""
        return os.path.join(self.base_dir, relative_path)
    
    def load_envvars(self):
        """.env を読み込み、環境変数を設定する。"""
        load_dotenv(override=True)   #.env ファイルを読み込む 引数で上書き可能に
    
    def get_api_key(self, var_name ) -> str:   
        """指定された環境変数からAPIキーを取得する。未設定ならエラー終了。"""
        api_key = os.getenv(var_name)   #環境変数が設定されているかを確認
        if not api_key:
            sys.stderr.write(
                f"エラー: {var_name} が見つかりません。.env に {var_name}=... を設定してください。\n"
            )
            sys.exit(1)
        return api_key
    
    def get_timestamp(self) -> str:
        """現在の日時を 'YYYYMMDD_HHMMSS' 形式で取得する。"""
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_filename(self, prefix :str= "out", ext: str = "png") -> str:
        """接頭辞と拡張子を使って、タイムスタンプ付きの出力ファイル名を生成する。"""
        timestamp = self.get_timestamp()
        return f"{prefix}_{timestamp}.{ext}"