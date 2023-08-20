import os

# db_utils.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser

def get_dbserver_config():
    settings_path = find_settings_ini()
# settings.iniから接続情報を読み込む
    config = configparser.ConfigParser()
    config.read(settings_path)

# 環境変数が設定されている場合はそれを優先
    value = os.environ.get('dbserver')
    if value is None:
        value = config.get('database', 'dbserver')

    return value

def find_settings_ini():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        settings_path = os.path.join(current_dir, 'chat_app/config/settings.ini')
        if os.path.exists(settings_path):
            return settings_path
        
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break  # ルートディレクトリまで到達したら終了
        current_dir = parent_dir
    
    return None  # 見つからなかった場合


def find_sql_folder():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        settings_path = os.path.join(current_dir, 'chat_app/sql/')
        if os.path.exists(settings_path):
            return settings_path
        
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break  # ルートディレクトリまで到達したら終了
        current_dir = parent_dir
    
    return None  # 見つからなかった場合


def get_db_config():
    settings_path = find_settings_ini()
    if settings_path:
        config = configparser.ConfigParser()
        config.read(settings_path)
        return config['database']
    else:
        return None


# 設定を読み込む関数
def get_db_settings():
    settings_path = find_settings_ini()
    config = configparser.ConfigParser()
    config.read(settings_path)
    dbserver = config['database']['dbserver']
    return dbserver

# データベースエンジンとセッションを作成する関数
def create_db_engine_and_session():
    dbserver = get_db_settings()
    engine = create_engine(dbserver)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal, declarative_base()

