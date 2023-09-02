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
  const [pressTimer, setPressTimer] = useState(null);
  const [isChatModalOpen, setChatModalOpen] = useState(false);
  const [selectedChatUser, setSelectedChatUser] = useState(null);
  const [eventUserIconMouseEvent, setEventUserIconMouseEvent] = useState("");
  const [selectedUser, setSelectedUser] = useState(null);
  const [isSelectedName, setisSelectedName] = useState(false);

 const handleNameMouseDown= (user) => {
    setSelectedUser(user);
    setisSelectedName(true);
  };

 const handleNameMouseUP = (user) => {
    setSelectedUser(user);
    setisSelectedName(false);
  };

  const [newMessage, setNewMessage] = useState("");
      const handleNewMessageChange = (event) => {
       setNewMessage(event.target.value);
    };
  const [isChatWindowOpen, setIsChatWindowOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState("");

  const handleSendMessage = async () => {
    const apiUrl = window.location.href.startsWith(
      "https://ron-the-rocker.net/",
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
        body: JSON.stringify({ message_content: newMessage }),
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
    setChatModalOpen(false);
    setSelectedChatUser(null);
    setIsChatWindowOpen(false);
  };

const handleUserIconMouseDown = (user, event) => {
  if (isChatModalOpen===true ){
    handleCloseChatModal();
  }

    setSelectedUser(user);
    setEventUserIconMouseEvent("shortEvent");
    setPressTimer(
      setTimeout(() => {
        setEventUserIconMouseEvent("longEvent");
      }, 1300)
    );
};

const handleUserIconMouseUp = (user) => {

    clearTimeout(pressTimer);
    if (eventUserIconMouseEvent === "shortEvent") {
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

    } else if (eventUserIconMouseEvent === "longEvent") {
     setIsChatWindowOpen(true);
    }
    setSelectedUser(null);
 
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
                    handleSendMessage();
                  }
                }}
              />
              <Button
                variant="contained"
                color="success" // 明るい緑色に
                onClick={handleSendMessage}
                endIcon={<SendIcon style={{ color: 'white' }} />}
                style={{ minWidth: '30px', backgroundColor: '#61c051' }} // 明るい緑色に
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
                            backgroundColor: '#e0e0e0',
                            borderRadius: '8px',
                            padding: '8px',
                            width: 'calc(100%)',
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
                            }}
                          >
                            <Typography variant="subtitle1"  onClick={(event) =>  handleNameMouseDown(message.sender, event)} style={{ whiteSpace: 'pre-wrap' }}>
                              <strong>{message.sender.username}</strong>{' '}
                              <Typography variant="caption">
                                {message.sender.trip}
                              </Typography>
                            </Typography>
                                   <Typography variant="caption">
                                     
                                     {window.innerWidth > 1100 ? `${message.sent_at} ( ★ ${message.sender.karma} : login ${message.sender.lastlogin_at} )` : `${message.short_sent_at} ★ ${message.sender.karma}`} 
                                   </Typography>
                          </div>
                          <Typography variant="body1" dangerouslySetInnerHTML={{ __html: message.content }} />
                      {selectedUser && isSelectedName && (
                          <UserProfilePopup user={selectedUser} onClose={handleNameMouseUP} anchorEl={messageContainerRef.current} />
                      )}
                        </div>
                      </div>
              ))}
            </div>
          </div>

{isChatWindowOpen && selectedUser && (
  <div
    style={{
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: '40%', // Adjust the width as needed
      backgroundColor: 'white', // 白色の背景色
      boxShadow: 24,
      p: 4,
    }}
  >
    <Typography variant="h6" component="h2" gutterBottom>
      Chat Window to @{selectedUser.username}
    </Typography>
    {/* Display the chat message */}
    <p>{chatMessage}</p>
    {/* Chat form */}
    <form>
      <textarea
        rows="4"
        cols="50"
        placeholder="Type your message..."
        value={chatMessage}
        onChange={(e) => setChatMessage(e.target.value)}
        style={{ marginBottom: '10px' }}
      ></textarea>
      <Button variant="contained" color="primary" type="submit">
        Send
      </Button>
    </form>
    <Button onClick={handleCloseChatModal}>Close</Button>
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