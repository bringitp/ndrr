# chat_app/tests/test_main.py
from app.main import app
import os
import pytest

from sqlalchemy import inspect
from app.database.models import Base  # 必要なモデルをすべてインポート

def test_os_vars_check():
# 環境変数からデータベース接続文字列を取得
    dbserver = os.environ.get("dbserver")
    assert len(dbserver) >= 1

# テスト用のセッション作成
@pytest.fixture
def test_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    dbserver = os.environ.get("dbserver")
    engine = create_engine(dbserver)  # インメモリデータベースを使用する例
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    engine.dispose()

# テーブル存在確認のテスト
def test_users_table_exists(test_session):
    inspector = inspect(test_session.bind)
    table_names = inspector.get_table_names()

    # テーブル名を確認
    assert 'users' in table_names  # your_table_name に実際のテーブル名を置き換えてください

def test_rooms_table_exists(test_session):
    inspector = inspect(test_session.bind)
    table_names = inspector.get_table_names()

    # テーブル名を確認
    assert 'rooms' in table_names  # your_table_name に実際のテーブル名を置き換えてください


