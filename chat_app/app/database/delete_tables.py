import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # 必要なモデルをすべてインポート
from pathlib import Path

# 現在のスクリプトのディレクトリを取得
script_dir = Path(__file__).resolve().parent
ndrr_path = script_dir.parent.parent.parent.parent / 'ndrr'
sys.path.append(str(ndrr_path))
from chat_app.app.utils import get_dbserver_config

# データベースエンジンの作成
engine = create_engine(get_dbserver_config())

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

# テーブルを削除
Base.metadata.drop_all(engine)