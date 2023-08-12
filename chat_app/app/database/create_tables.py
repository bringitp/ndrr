import os,sys
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # 必要なモデルをすべてインポート
from pathlib import Path

# 現在のスクリプトのディレクトリを取得
script_dir = Path(__file__).resolve().parent
ndrr_path = script_dir.parent.parent.parent.parent / 'ndrr'
sys.path.append(str(ndrr_path))
from chat_app.app.utils import find_settings_ini

settings_path = find_settings_ini()

# settings.iniから接続情報を読み込む
config = configparser.ConfigParser()
config.read(settings_path)
dbserver = config['database']['dbserver']

# データベースエンジンの作成
engine = create_engine(dbserver)

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

# テーブルを作成
Base.metadata.create_all(engine)