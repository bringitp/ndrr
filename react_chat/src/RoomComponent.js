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

    // PUT リクエストを送信
    const response = await fetch(`http://localhost:7777/room/${roomId}/depart_me`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${keycloak.token}`, // トークンを含める必要があります
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      // リクエストが成功した場合、リダイレクトを行います
      window.location.href = "http://localhost:3000/rooms"; // リダイレクト先の URL を指定してください
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
          <RoomInfo room={jsonData.room} />

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

            <div style={{ marginTop: '20px', overflowY: 'auto' }}>
              {jsonData.messages.map((message) => (
              <div
               key={message.id}
               style={{
                 display: 'flex',
                 alignItems: 'center',
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
                        width="60"
                        height="60"
                        style={{ borderRadius: '15%' , borderRadius: '15%', marginLeft: '0px' }} 
                        onClick={(event) => handleUserIconMouseDown(message.sender, event)}
                        onMouseUp={() => handleUserIconMouseUp(message.sender)}
                      />
                      
                       <div
                         style={{
                           marginLeft: '10px',
                           backgroundColor:'#e0e0e0', // プライベートメッセージの場合、フォントカラーを明るい文字に設定
                           borderRadius: '8px',
                           padding: '8px',
                           width: 'calc(100%)',
                           backgroundColor: message.is_private ? '#83A4D9' :'#d0d0d0'  ,

                         }}
                       >
                      <div
                        style={{
                           display: "flex",
                           justifyContent: "space-between",
                           alignItems: "center",
                         }}
                      > 
                              <Typography variant="subtitle1"  onClick={(event) =>   handleNameMouseDown (message.sender, event)} style={{ whiteSpace: 'pre-wrap' }}>
                              <strong>{message.is_private ? ' 📧 ' : ' '}</strong> 
                              <strong>{message.sender.username}</strong>
                              <strong>{message.is_private ? ' ⇒ ' + message.sender.sender_username + " "  : ' '}</strong> 
   
                              <Typography variant="caption">
                                {message.sender.trip}
                              </Typography>
                            </Typography>
                                   <Typography variant="caption" onClick={(event) => handleLabelTailMouseDown(message.sender, event)}>
                                     {window.innerWidth > 1100 ? `${message.sent_at} ( ★ ${message.sender.karma} : login ${message.sender.lastlogin_at} )` : `${message.short_sent_at} ★ ${message.sender.karma}`} 
                                   </Typography>
                          </div>
                          <Typography variant="body1" dangerouslySetInnerHTML={{ __html: message.content }} />
                      {selectedUser && isSelectedName && (
                          <UserProfilePopup user={selectedUser} onClose={handleIconMouseUP} anchorEl={messageContainerRef.current} />
                      )}

                        </div>
                      </div>
              ))}
            </div>
          </div>

                       {isDirectChatWindowOpen && selectedUser && (
                        <div
                          style={{
                            position: 'fixed',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            width: '80%', // Adjust the width as needed
                            backgroundColor: 'lightgreen', // 白色の背景色
                            boxShadow: 24,
                            p: 4,
                            cursor: 'move', // カーソルを移動アイコンに変更
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

                                const messageData = { message_content: privateMessage, receiver_id: selectedUser.user_id }; // メッセージと受信者IDをセット
                                const response = await fetch(apiUrl, {
                                  method: 'POST',
                                  headers,
                                  body: JSON.stringify(messageData),
                                });

                                if (response.ok) {
                                  setPrivateMessage('');
                                  handleCloseChatModal(); // ウィンドウを閉じる
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
                                width: '95%', // 幅を30%に設定
                                outline: 'none', // フォーカス時の枠線を無効にする
                              }}
                              onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                  e.preventDefault();
                                  // フォームのサブミット時にAPIを呼び出してメッセージを送信
                                  const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/')
                                    ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/private_messages`
                                    : `http://localhost:7777/room/${roomId}/private_messages`;

                                  const headers = new Headers();
                                  headers.append('Authorization', `Bearer ${keycloak.token}`);
                                  headers.append('Content-Type', 'application/json');
  
                                  const messageData = { message_content: privateMessage, receiver_id: selectedUser.id }; // メッセージと受信者IDをセット

                                  fetch(apiUrl, {
                                    method: 'POST',
                                    headers,
                                    body: JSON.stringify(messageData),
                                  })
                                    .then((response) => {
                                      if (response.ok) {
                                        setPrivateMessage('');
                                        handleCloseChatModal(); // ウィンドウを閉じる
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