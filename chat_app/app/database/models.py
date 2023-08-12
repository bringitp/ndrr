from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import text

Base = declarative_base()

class BlockedUser(Base):
    __tablename__ = 'blocked_users'
    
    block_id = Column(Integer, primary_key=True)
    blocking_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blocked_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # blocking_user と blocked_user の関係性を分割
    blocking_user = relationship('User', foreign_keys=[blocking_user_id], back_populates='blocking_users')
    blocked_user = relationship('User', foreign_keys=[blocked_user_id], back_populates='blocked_users')

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    avatar = Column(String(100))
    trip = Column(String(32), nullable=False)
    privilege = Column(Enum('user', 'premium'), nullable=False, default='user')
    ng_list = Column(Text)
    
    sessions = relationship('UserSession', back_populates='user')
    rooms_owned = relationship('Room', back_populates='owner')
    room_memberships = relationship('RoomMember', back_populates='user')
    sent_messages = relationship('Message', back_populates='sender')
    # blocked_users の関係性を外部キーを用いて2つに分割する
    blocking_users = relationship('BlockedUser', foreign_keys=[BlockedUser.blocking_user_id], back_populates='blocking_user')
    blocked_users = relationship('BlockedUser', foreign_keys=[BlockedUser.blocked_user_id], back_populates='blocked_user')

    images = relationship('Image', back_populates='sender')
    spam_users = relationship('SpamUser', back_populates='user')
    banned_users = relationship('BannedUser', back_populates='user')
    spam_messages = relationship('SpamMessage', back_populates='user')

class UserSession(Base):
    __tablename__ = 'user_sessions'
    
    session_id = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_token = Column(String(128), nullable=False)
    refresh_token = Column(String(128), nullable=False)
    expiration_date = Column(TIMESTAMP, nullable=False)
    
    user = relationship('User', back_populates='sessions')

class Room(Base):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    max_capacity = Column(Integer, nullable=False, default=20)
    status = Column(Enum('active', 'inactive'), nullable=False, default='active')
    last_activity = Column(TIMESTAMP, nullable=False, default=func.now())
    
    owner = relationship('User', back_populates='rooms_owned')
    members = relationship('RoomMember', back_populates='room')
    messages = relationship('Message', back_populates='room')

# 各テーブルに対するモデルクラスの定義を続けて書きます...
class RoomMember(Base):
    __tablename__ = 'room_members'
    
    member_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    joined_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    
    user = relationship('User')
    room = relationship('Room')

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    
    sender = relationship('User')
    room = relationship('Room')


class Image(Base):
    __tablename__ = 'images'
    
    image_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image_url = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    
    sender = relationship('User')
    room = relationship('Room')

class SpamUser(Base):
    __tablename__ = 'spam_users'
    
    spam_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    spam_points = Column(Integer, nullable=False)
    last_spam_activity = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    
    user = relationship('User')

class BannedUser(Base):
    __tablename__ = 'banned_users'
    
    ban_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    ban_start_date = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    ban_end_date = Column(TIMESTAMP, nullable=False)
    
    user = relationship('User')

class SpamMessage(Base):
    __tablename__ = 'spam_messages'
    
    spam_message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    
    user = relationship('User')
