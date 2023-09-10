import React, { useState, useEffect, useRef } from "react";
import { useLocation, useParams } from "react-router-dom";
import { Typography, Button, CircularProgress, Container, Paper, TextareaAutosize } from "@mui/material";
import RoomInfo from "./RoomInfo";
import UserProfilePopup from "./UserProfilePopup";
import { Send as SendIcon } from "@mui/icons-material";

function RoomComponent(props) {

const {
    jsonData,
    messageInputRef,
    messageContainerRef,
    error,
    keycloak,
    initialized
  } = props;
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const [isDirectChatWindowOpen, setDirectChatWindowOpen] = useState(false);
  const [selectedChatUser, setSelectedChatUser] = useState(null);
  const [eventUserIconMouseEvent, setEventUserIconMouseEvent] = useState("");
  const [selectedUser, setSelectedUser] = useState(null);
  const [isSelectedName, setSelectedName] = useState(false);

 const handleIconMouseDown        = (user) => {
    setSelectedUser(user);
    setSelectedName(true);
  };

 const handleIconMouseUP           = (user) => {
    setSelectedUser(user);
    setSelectedName(false);
  };

const handleNameMouseDown        = (user) => {
    setSelectedUser(user);
    setSelectedName(true);
  };

 const handleNameMouseUP           = (user) => {
    setSelectedUser(user);
     setSelectedName(false);
  };

  const handleLabelTailMouseDown  = (user) => {
    setSelectedUser(user);
    setDirectChatWindowOpen(true);
  };

 const handleLabelTailMouseUP     = (user) => {
    setSelectedUser(user);
    setDirectChatWindowOpen(false);
  };

  const [newMessage, setNewMessage] = useState("");
      const handleNewMessageChange = (event) => {
       setNewMessage(event.target.value);
    };

  const [isChatWindowOpen, setIsChatWindowOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState("");
  const [privateMessage, setPrivateMessage] = useState("");
      const handlePrivateMessageChange = (event) => {
       setPrivateMessage(event.target.value);
    };

const handleSendMessage = async (messageData) => {
  const apiUrl = window.location.href.startsWith(
    "https://ron-the-rocker.net/"
  )
    ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/messages`
    : `http://localhost:7777/room/${roomId}/messages`;

  const headers = new Headers();
  headers.append("Authorization", `Bearer ${keycloak.token}`);
  headers.append("Content-Type", "application/json");

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers,
      body: JSON.stringify(messageData),
    });
    if (response.ok) {
      setNewMessage("");
    } else {
      console.error("Error sending message:", response.status);
    }
  } catch (error) {
    console.error("Error sending message:", error);
  }
};

  // モーダルを閉じる関数
  const handleCloseChatModal = () => {
    setDirectChatWindowOpen(false);
    setSelectedChatUser(null);
    setIsChatWindowOpen(false);
  };

const handleUserIconMouseDown = (user, event) => {
};

const handleUserIconMouseUp = (user) => {
     setIsChatWindowOpen(false);
     const input = messageInputRef.current;
     const startPos = input.selectionStart;
     const endPos = input.selectionEnd;
     const beforeText = newMessage.substring(0, startPos);
     const afterText = newMessage.substring(endPos);
     const insertedText = `@${user.username} `;
     setNewMessage(beforeText + insertedText + afterText);
    // カーソル位置を更新
     const newCursorPos = startPos + insertedText.length;
     input.setSelectionRange(newCursorPos, newCursorPos); 
};

const handleDepart = async () => {
  try {
    // データオブジェクトを作成
    const data = {
      member_id: jsonData.room.room_login_user_id, // current_user はログイン中のユーザーを表すオブジェクトです
    };

  const apiUrl = window.location.href.startsWith(
    "https://ron-the-rocker.net/"
  )
    ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/depart_me`
    : `http://localhost:7777/room/${roomId}/depart_me`;

    // PUT リクエストを送信
    const response = await fetch(apiUrl, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${keycloak.token}`, // トークンを含める必要があります
      },
      body: JSON.stringify(data),
    });

  const jumpUrl = window.location.href.startsWith(
    "https://ron-the-rocker.net/"
  )
    ? `https://ron-the-rocker.net/rooms/`
    : `http://localhost:3000/rooms/`;

    if (response.ok) {
      // リクエストが成功した場合、リダイレクトを行います
      window.location.href = jumpUrl; // リダイレクト先の URL を指定してください
    } else {
      console.error("Error departing from the room:", response.status);
    }
  } catch (error) {
    console.error("Error departing from the room:", error);
  }
};



  return (
    <Container>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Typography variant="h4" gutterBottom></Typography>

        <Button
          variant="contained"
          color="secondary"
           onClick={handleDepart}
        >
          Depart
        </Button>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => keycloak.logout()}
        >
          Logout
        </Button>
      </div>

      {jsonData ? (
        <Paper
          elevation={9}
          sx={{
            padding: "11px",
            marginTop: "20px",
            display: "flex",
            flexDirection: "column",
            backgroundColor: "#bce2e8", // ここに背景色を設定
          }}
        >
          <RoomInfo jsonData={jsonData} />

          <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '8px',
                borderRadius: '4px',
                border: '1px solid #ccc',
                boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
                width: 'calc(96%)',
              }}
            >
              <TextareaAutosize
                ref={messageInputRef}
                placeholder="..."
                value={newMessage}
                onChange={handleNewMessageChange}
                style={{
                  flexGrow: 1,
                  marginTop: '10px',
                  marginBottom: '10px',
                  border: 'none',
                  resize: 'none',
                  padding: '0',
                  width: '100%', // 幅を30%に設定
                  backgroundColor: '#fcfcfc', // 明るい緑色の背景色
                  outline: 'none', // フォーカス時の枠線を無効にする
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage({message_content: newMessage});
                  }
                }}
              />
             <Button
               variant="contained"
               color="success"
               onClick={() => handleSendMessage({ message_content: newMessage })}
               endIcon={<SendIcon style={{ color: 'white' }} />}
               style={{ minWidth: '30px', backgroundColor: '#61c051' }}
             />
            </div>

                    <div style={{ marginTop: '15px', overflowY: 'auto' }}>

                      {jsonData.messages.map((message) => {

                        if (message.message_type === 'system') {
                        return (
                        <div
                          key={message.id}
                          style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            marginBottom: '10px',
                            width: '98%',
                            borderRadius: '8px',
                            backgroundColor: '#dbd0d0',
                          }}
                        >
<img
  src={
    process.env.NODE_ENV === 'development'
      ? `http://localhost:7777/static/img/${message.sender.avatar_url}`
      : `https://ron-the-rocker.net/ndrr/api/static/img/${message.sender.avatar_url}`
  }
  alt="Icon"
  width="30"
  height="30"
  style={{ borderRadius: '75%', marginLeft: '17px' }}
  onClick={(event) => handleUserIconMouseDown(message.sender, event)}
  onMouseUp={() => handleUserIconMouseUp(message.sender)}
/>
                          <div
                            style={{
                              marginLeft: '30px',
                              backgroundColor: '#dbd0d0',
                              borderRadius: '8px',
                              paddingRight: '9px',
                              marginBottom: '0px',
                              width: 'calc(100%)',
                            }}
                          >

                            <div
                              style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                paddingRight: '9px',
                                margin: '0px',
                              }}
                            >
                              <Typography variant="subtitle1" onClick={(event) => handleNameMouseDown(message.sender, event)} style={{ fontSize: '85%',whiteSpace: 'pre-wrap' }}>
                                <strong>{message.sender.username}</strong>
                                <Typography variant="caption">
                                  {message.is_private ? ` (${message.sender.trip})` : ' '}
                                </Typography>
                                <strong>{message.message_type === 'private' ? ` ⇒ ${message.sender.receiver_username} ` : ''}</strong>

                                <Typography variant="caption">
                                  {message.message_type === 'private'  ? ' ' : `(system)`}
                                </Typography>
                              </Typography>

                              <Typography variant="caption" onClick={(event) => handleLabelTailMouseDown(message.sender, event)}>
                                {(() => {
                                  const sentAt = new Date(message.sent_at);

                                  const iso8601String = sentAt.toISOString();
                                  const formattedString = iso8601String.replace('T', ' ').replace('.000Z', '');
                                  const date = sentAt.toLocaleDateString([], { day: '2-digit' });
                                  const time = sentAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                                  if (window.innerWidth > 1100) {
                                    return `✪ ${formattedString}`;
                                  } else {
                                    return `✪ ${date}${time}`;
                                  }
                                })()}
                              </Typography>
                            </div>


                            <Typography variant="body1"                               style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                paddingTop: '0px',
                                paddingBottom: '0px',
                                fontSize: '85%'
                              }}
                               dangerouslySetInnerHTML={{ __html: message.content }} />
                            {selectedUser && isSelectedName && (
                              <UserProfilePopup user={selectedUser} onClose={handleIconMouseUP} anchorEl={messageContainerRef.current} />
                            )}
                          </div>
                        </div>
                      );
                   }


                        if (message.message_type === 'private' || message.message_type === 'public') {
return (
  <div
    key={message.id}
    style={{
      display: 'flex',
      alignItems: 'flex-start', // 上寄せに変更
      justifyContent: 'space-between',
      marginBottom: '10px',
      width: '98%',
      borderRadius: '8px',
    }}
  >
    <img
      src={
        process.env.NODE_ENV === 'development'
          ? `http://localhost:7777/static/img/${message.sender.avatar_url}`
          : `https://ron-the-rocker.net/ndrr/api/static/img/${message.sender.avatar_url}`
      }
      alt="Icon"
      width="50"
      height="50"
      style={{ borderRadius: '15%', marginLeft: '0px' }}
      onClick={(event) => handleUserIconMouseDown(message.sender, event)}
      onMouseUp={() => handleUserIconMouseUp(message.sender)}
    />

    <div
      style={{
        marginLeft: '10px',
        display: 'flex',
        flexDirection: 'column', // 列方向に変更
        alignItems: 'flex-start', // 左寄せに変更
        backgroundColor: message.message_type === 'private' ? '#93B4E9' : '#E0E0E0',
        borderRadius: '8px',
        paddingTop: '2px',
        paddingLeft: '2px',
        width: 'calc(100%)',
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
           marginLeft: '0px',
        }}
      >
        <Typography variant="subtitle1" onClick={(event) => handleNameMouseDown(message.sender, event)} style={{ whiteSpace: 'pre-wrap' }}>
          <strong style={{ fontSize: '100%' }}>{message.message_type === 'private' ? ' 📧 ' : ' '}</strong>
          <strong style={{ fontSize: '100%' }}>{message.sender.username} </strong>
          <strong style={{ fontSize: '85%' }}>{message.message_type === 'private' ? ` ⇒ ${message.sender.receiver_username} ` : ''}</strong>
        </Typography>
      </div>
      <Typography variant="body1" style={{ fontSize: '92%' ,  marginLeft: '9px',}} dangerouslySetInnerHTML={{ __html: message.content }} />
      {selectedUser && isSelectedName && (
        <UserProfilePopup user={selectedUser} onClose={handleIconMouseUP} anchorEl={messageContainerRef.current} />
      )}

<div style={{ textAlign: 'right', width: '98%', boxSizing: 'border-box' }}>
  <Typography variant="caption">
    {(() => {
      const sentAt = new Date(message.sent_at);

      const iso8601String = sentAt.toISOString();
      const formattedString = iso8601String.replace('T', ' ').replace('.000Z', '');
      const date = sentAt.toLocaleDateString([], { day: '2-digit' });
      const time = sentAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

      if (window.innerWidth > 1100) {
        return `(${message.sender.trip}) - ${formattedString}`;
      } else {
        return `(${message.sender.trip}) - ${formattedString}`;
      }
    })()}
  </Typography>

</div>
    </div>
  </div>
);
                   }
                   return null;

                   })}


                    </div>
                </div>
                 {isDirectChatWindowOpen && selectedUser && (
                      <div
                        style={{
                          position: 'fixed',
                          top: '50%',
                          left: '50%',
                          transform: 'translate(-50%, -50%)',
                          width: '80%',
                          backgroundColor: 'lightgreen',
                          boxShadow: 24,
                          p: 4,
                          cursor: 'move',
                        }}
                      >
                        <Typography variant="h6" component="h2" gutterBottom>
                          @{selectedUser.username}
                        </Typography>
                        {/* Display the chat message */}
                        <p>{chatMessage}</p>
                        {/* Chat form */}
                        <form
                          onSubmit={async (e) => {
                            e.preventDefault();
                            try {
                              // プライベートメッセージを送信
                              const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/')
                                ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/private_messages`
                                : `http://localhost:7777/room/${roomId}/private_messages`;

                              const headers = new Headers();
                              headers.append('Authorization', `Bearer ${keycloak.token}`);
                              headers.append('Content-Type', 'application/json');

                              const messageData = { message_content: privateMessage, receiver_id: selectedUser.user_id };
                              const response = await fetch(apiUrl, {
                                method: 'POST',
                                headers,
                                body: JSON.stringify(messageData),
                              });

                              if (response.ok) {
                                setPrivateMessage('');
                                handleCloseChatModal();
                              } else {
                                console.error('Error sending private message:', response.status);
                              }
                            } catch (error) {
                              console.error('Error sending private message:', error);
                            }
                          }}
                        >
                          <TextareaAutosize
                            placeholder="..."
                            value={privateMessage}
                            onChange={(e) => {
                              setPrivateMessage(e.target.value);
                            }}
                            style={{
                              width: '95%',
                              outline: 'none',
                            }}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/')
                                  ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/private_messages`
                                  : `http://localhost:7777/room/${roomId}/private_messages`;

                                const headers = new Headers();
                                headers.append('Authorization', `Bearer ${keycloak.token}`);
                                headers.append('Content-Type', 'application/json');

                                const messageData = { message_content: privateMessage, receiver_id: selectedUser.id };

                                fetch(apiUrl, {
                                  method: 'POST',
                                  headers,
                                  body: JSON.stringify(messageData),
                                })
                                  .then((response) => {
                                    if (response.ok) {
                                      setPrivateMessage('');
                                      handleCloseChatModal();
                                    } else {
                                      console.error('Error sending private message:', response.status);
                                    }
                                  })
                                  .catch((error) => {
                                    console.error('Error sending private message:', error);
                                  });
                              }
                            }}
                          />
                          <Button variant="contained" color="primary" type="submit">
                            Send
                          </Button>
                        </form>
                        <Button onClick={() => handleCloseChatModal()}>Close</Button>
                      </div>
                    )}
        </Paper>
      ) : (
        <CircularProgress />
      )}
    </Container>
  );
}

export default RoomComponent;