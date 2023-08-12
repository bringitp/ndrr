-- users テーブル
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    avatar VARCHAR(100),
    trip VARCHAR(32) NOT NULL,
    privilege ENUM('user', 'premium') NOT NULL DEFAULT 'user',
    ng_list TEXT
);

-- user_sessions テーブル
CREATE TABLE user_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id INT NOT NULL,
    access_token VARCHAR(128) NOT NULL,
    refresh_token VARCHAR(128) NOT NULL,
    expiration_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- rooms テーブル
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    owner_id INT NOT NULL,
    max_capacity INT NOT NULL DEFAULT 20,
    status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    last_activity TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- room_members テーブル
CREATE TABLE room_members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    user_id INT NOT NULL,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- messages テーブル
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- blocked_users テーブル
CREATE TABLE blocked_users (
    block_id INT AUTO_INCREMENT PRIMARY KEY,
    blocking_user_id INT NOT NULL,
    blocked_user_id INT NOT NULL,
    FOREIGN KEY (blocking_user_id) REFERENCES users(id),
    FOREIGN KEY (blocked_user_id) REFERENCES users(id)
);

-- images テーブル
CREATE TABLE images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    sender_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- spam_users テーブル
CREATE TABLE spam_users (
    spam_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    spam_points INT NOT NULL,
    last_spam_activity TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- banned_users テーブル
CREATE TABLE banned_users (
    ban_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ban_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ban_end_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- spam_messages テーブル
CREATE TABLE spam_messages (
    spam_message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);