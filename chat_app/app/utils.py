import os
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
