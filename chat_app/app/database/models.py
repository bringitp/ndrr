from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    Text,
    TIMESTAMP,
    Float,
    Table,
    Index,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import text

Base = declarative_base()


class BlockedUser(Base):
    __tablename__ = "blocked_users"

    id = Column(Integer, primary_key=True)
    blocking_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blocked_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # ブロックしているユーザーへの関連性
    blocking_user = relationship(
        "User", foreign_keys=[blocking_user_id], back_populates="blocked_users"
    )
    # ブロックされているユーザーへの関連性
    blocked_user = relationship(
        "User", foreign_keys=[blocked_user_id], back_populates="blocked_by_users"
    )


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    label = Column(String(300), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    max_capacity = Column(Integer, nullable=False, default=20)
    over_karma_limit = Column(Integer, nullable=True, default=0)
    under_karma_limit = Column(Integer, nullable=True, default=0)
    lux = Column(Integer, nullable=True, default=0)
    room_type = Column(Enum("public", "private"), nullable=False, default="public") 
    room_password = Column(String(50), nullable=True, default="") 
    status = Column(Enum("active", "inactive"), nullable=False, default="active")
    last_activity = Column(TIMESTAMP, nullable=False)
    owner = relationship("User", back_populates="owned_rooms", foreign_keys=[owner_id])
    room_members = relationship("RoomMember", back_populates="room")
    messages = relationship("Message", back_populates="room")
    images = relationship("Image", back_populates="room")

class AvatarList(Base):
    __tablename__ = "avatar_list"
    avatar_id = Column(Integer, primary_key=True)
    avatar_url = Column(String(255), nullable=False)

class UserNGList(Base):
    __tablename__ = "user_ng_lists"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    blocked_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="ng_lists", foreign_keys=[user_id])
    blocked_user = relationship("User", foreign_keys=[blocked_user_id])

# avatr_url_signatue
# signatue
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    sent_at = Column(TIMESTAMP, nullable=False, index=True)
    content = Column(Text, nullable=False)
    message_type = Column(
        Enum("public", "private", "system"), nullable=False
    )  # メッセージタイプを区別

    toxicity = Column(Float(precision=6), nullable=True)
    sentiment = Column(Float(precision=6), nullable=True)
    constructive = Column(Float(precision=6), nullable=True)
    incendiary = Column(Float(precision=6), nullable=True)
    foxy = Column(Float(precision=6), nullable=True)
    fluence = Column(Float(precision=6), nullable=True)

    signature_writer_name = Column(String(255), nullable=True)
    signature_recipient_name = Column(String(255), nullable=True)
    signature_avatar_url = Column(String(255), nullable=True)
    signature_trip = Column(String(255), nullable=True)
    signature_karma = Column(String(255), nullable=True)
    signature_profile = Column(String(200))

    room = relationship("Room", back_populates="messages")
    sender = relationship(
        "User", back_populates="sent_private_messages", foreign_keys=[sender_id]
    )
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_private_messages"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    allowed_name_changes = Column(Integer, nullable=False)
    sub = Column(String(100), unique=True, nullable=False)
    avatar_id = Column(Integer, ForeignKey("avatar_list.avatar_id"), nullable=True)
    profile = Column(String(200))
    trip = Column(String(32), nullable=False)
    life = Column(Integer, nullable=False)

    # 新しいカラム：ペナルティポイント
    penalty_points = Column(Integer, default=0, nullable=False)
    spam_activity_score = Column(Float(precision=6), nullable=False)
    karma = Column(Float(precision=6), nullable=False)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    lastlogin_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    lastlogout_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    privilege = Column(
        Enum("guest", "user", "premium", name="privilege_enum"),
        nullable=False,
        default="user",
    )
    owned_rooms = relationship(
        "Room", back_populates="owner", foreign_keys=[Room.owner_id]
    )
    room_memberships = relationship("RoomMember", back_populates="user")
    # 新しいカラム：プライベートメッセージのNGリスト
    # プライベートメッセージの関連性
    received_private_messages = relationship(
        "Message", back_populates="receiver", foreign_keys=[Message.receiver_id]
    )
    sent_private_messages = relationship(
        "Message", back_populates="sender", foreign_keys=[Message.sender_id]
    )
    sessions = relationship("UserSession", back_populates="user")

    room_memberships = relationship("RoomMember", back_populates="user")
    images = relationship("Image", back_populates="sender")
    spam_users = relationship("SpamUser", back_populates="user")
    # blocked_usersの関連定義にforeign_keys引数を追加
    banned_users = relationship("BannedUser", back_populates="user")
    spam_messages = relationship("SpamMessage", back_populates="user")
    suspicious_messages = relationship(
        "SuspiciousMessage", back_populates="user"
    )  # ここに関連性を追加

    ng_lists = relationship(
        "UserNGList", back_populates="user", foreign_keys=[UserNGList.user_id]
    )

    # ブロックしているユーザー
    blocked_users = relationship(
        "BlockedUser",
        back_populates="blocking_user",
        foreign_keys="[BlockedUser.blocking_user_id]",
    )

    # ブロックされているユーザー
    blocked_by_users = relationship(
        "BlockedUser",
        back_populates="blocked_user",
        foreign_keys="[BlockedUser.blocked_user_id]",
    )


class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), default=5, nullable=False)
    access_token = Column(String(128), nullable=False)
    refresh_token = Column(String(128), nullable=False)
    expiration_date = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="sessions")


class RoomMember(Base):
    __tablename__ = "room_members"

    member_id = Column(Integer, index=True, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(TIMESTAMP, nullable=False)

    room = relationship("Room", back_populates="room_members")
    user = relationship("User", back_populates="room_memberships")


class Image(Base):
    __tablename__ = "images"

    image_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    room = relationship("Room", back_populates="images")
    sender = relationship("User", back_populates="images")


class SpamUser(Base):
    __tablename__ = "spam_users"

    spam_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    spam_points = Column(Integer, nullable=False)
    last_spam_activity = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="spam_users")


class BannedUser(Base):
    __tablename__ = "banned_users"

    ban_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ban_start_date = Column(TIMESTAMP, nullable=False)
    ban_end_date = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="banned_users")


class SpamMessage(Base):
    __tablename__ = "spam_messages"

    spam_message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    spam_type = Column(Integer, nullable=False)
    score = Column(Float(precision=6), nullable=True)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="spam_messages")


class SuspiciousMessage(Base):
    __tablename__ = "suspicious_messages"

    suspicious_message_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    spam_type = Column(Integer, nullable=False)
    score = Column(Float(precision=6), nullable=True)

    content  = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="suspicious_messages")
