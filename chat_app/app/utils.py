
# db_utils.py
import os
from sqlalchemy import create_engine, Index  # Index を追加
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
from chat_app.app.database.models  import BlockedUser, Room, PrivateMessage, UserNGList, User

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

def find_ng_words_ini():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while True:
        settings_path = os.path.join(current_dir, 'chat_app/config/ng_words.ini')
        if os.path.exists(settings_path):
            return settings_path
        
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break  # ルートディレクトリまで到達したら終了
        current_dir = parent_dir
    
    return None  # 見つからなかった場合

def load_ng_words():
    with open(find_ng_words_ini(), "r", encoding="utf-8") as file:
        ng_words = [line.strip() for line in file if line.strip()]
    return ng_words


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
    engine = create_engine(get_dbserver_config(), pool_size=50, max_overflow=25)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # インデックスの設定
    #with engine.connect() as connection:
        # BlockedUser テーブルの blocking_user_id 列と blocked_user_id 列にインデックスを設定
        #blocked_user_index = Index('idx_blocked_user_new', BlockedUser.blocking_user_id, BlockedUser.blocked_user_id)
        #blocked_user_index.create(connection)

        # Room テーブルの owner_id 列にインデックスを設定
        #room_owner_index = Index('idx_room_owner', Room.owner_id)
        #room_owner_index.create(connection)

        # PrivateMessage テーブルの room_id 列と sent_at 列にインデックスを設定
        #private_message_index = Index('idx_private_message', PrivateMessage.room_id, PrivateMessage.sent_at)
        #private_message_index.create(connection)

        # UserNGList テーブルの user_id 列と blocked_user_id 列にインデックスを設定
        #user_ng_list_index = Index('idx_user_ng_list', UserNGList.user_id, UserNGList.blocked_user_id)
        #user_ng_list_index.create(connection)

        # User テーブルの sub 列に一意のインデックスを設定
        #user_sub_index = Index('idx_user_sub', User.sub, unique=True)
        #user_sub_index.create(connection)

    return engine, SessionLocal, declarative_base()

