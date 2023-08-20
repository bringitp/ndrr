import os
import sys
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # 必要なモデルをすべてインポート
from pathlib import Path

# 現在のスクリプトのディレクトリを取得
script_dir = Path(__file__).resolve().parent
ndrr_path = script_dir.parent.parent.parent.parent / 'ndrr'
sys.path.append(str(ndrr_path))
from chat_app.app.utils import get_dbserver_config
from chat_app.app.utils import find_sql_folder
# データベースエンジンの作成
engine = create_engine(get_dbserver_config())

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

# dummy_data.sql のパス
sql_file_path = find_sql_folder() + "/dummy_data.sql"

# dummy_data.sql の内容を読み込み、実行
with open(sql_file_path, 'r') as sql_file:
    sql_statements = sql_file.read()

# SQL ステートメントをセミコロンで分割
statements = sql_statements.split(';')

# 各ステートメントを実行
for statement in statements:
    if statement.strip():
        session.execute(statement)
    session.commit()




