import React from "react";
import { Typography, Button, CircularProgress, Container, Paper, TextareaAutosize } from "@mui/material";
import RoomInfo from "./RoomInfo";
import UserProfilePopup from "./UserProfilePopup";
import { Send as SendIcon } from "@mui/icons-material";

function RoomComponent(props) {
  const {
    jsonData,
    newMessage,
    messageInputRef,
    handleNewMessageChange,
    handleSendMessage,
    handleUserIconClick,
    handleUserClick,
    handleClosePopup,
    selectedUser,
    messageContainerRef,
    error,
    keycloak,
    initialized
  } = props;

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
                        onClick={(event) => handleUserIconClick(message.sender, event)}
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
                            <Typography variant="subtitle1"  onClick={(event) =>  handleUserClick(message.sender, event)} style={{ whiteSpace: 'pre-wrap' }}>
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
                      {selectedUser && (
                          <UserProfilePopup user={selectedUser} onClose={handleClosePopup} anchorEl={messageContainerRef.current} />
                      )}
                        </div>
                      </div>
              ))}
            </div>
          </div>
        </Paper>
      ) : (
        <CircularProgress />
      )}
    </Container>
  );
}

export default RoomComponent;