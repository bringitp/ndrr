import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { ReactKeycloakProvider, useKeycloak } from '@react-keycloak/web';
import Keycloak from 'keycloak-js';
import Alert from '@mui/material/Alert';
import MainComponent from './MainComponent';
import {
  Button,
  CircularProgress,
  Container,
  Paper,
  Typography,
  TextareaAutosize,
} from '@mui/material';
import RoomInfo from './RoomInfo';


function Room() {
  const { roomId } = useParams(); // URLパラメータからroomIdを取得

  const location = useLocation();
  const [jsonData, setJsonData] = useState(null);
  const [newMessage, setNewMessage] = useState('');
  const messageContainerRef = useRef(null);
  const [error, setError] = useState(null);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックの使用

  useEffect(() => {
    if (initialized && keycloak.authenticated) {
      const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/')
        ? `https://ron-the-rocker.net/ndrr/api/rooms/${roomId}/messages`
        : `http://localhost:7777/rooms/${roomId}/messages`;

      const headers = new Headers();
      headers.append('Authorization', `Bearer ${keycloak.token}`);

const fetchData = async () => {
  try {
    const timeoutPromise = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 2500));
    const response = await Promise.race([
      fetch(apiUrl, { headers }),
      timeoutPromise,
    ]);

    if (response.ok) {
      const data = await response.json();
      setJsonData(data);
      if (messageContainerRef.current) {
        messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
      }
    } else if (response.status === 403 || response.status === 406) {
      setError(`部屋の許可がありません: ${response.status}`);
    }
  } catch (error) {
    if (error.message === 'Failed to fetch') {
      setError('通信がタイムアウトしました');
    } else {
      setError(`その他のエラーが発生しました ${error.message}`);
      console.error('Error fetching data:', error);
    }
  }
};
      fetchData();
      const fetchInterval = setInterval(fetchData, 1000);
      return () => {
        clearInterval(fetchInterval);
      };
    }
  }, [initialized, keycloak.authenticated]);

  const handleNewMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSendMessage = async () => {
    const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/')
      ? `https://ron-the-rocker.net/ndrr/api/rooms/${roomId}/messages`
      : `http://localhost:7777/rooms/${roomId}/messages`;

    const headers = new Headers();
    headers.append('Authorization', `Bearer ${keycloak.token}`);
    headers.append('Content-Type', 'application/json');

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers,
        body: JSON.stringify({ message_content: newMessage }),
      });
      if (response.ok) {
        setNewMessage('');
      } else {
        console.error('Error sending message:', response.status);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  if (!initialized) {
    return <CircularProgress />;
  }

  if (!keycloak.authenticated) {
    return (
      <Container>
        <Button variant="contained" color="primary" onClick={() => keycloak.login()}>
          Login
        </Button>
      </Container>
    );
  }

if (error) {
  return (
    <Container>
      <h4> エラー </h4>
      <Alert severity="warning">{error}</Alert>
    </Container>
  );
}

  return (
    <Container>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Typography variant="h4" gutterBottom>
          Welcome!
        </Typography>
        <Button variant="contained" color="secondary" onClick={() => keycloak.logout()}>
          Logout
        </Button>
      </div>

      {jsonData ? (
        <Paper elevation={9} style={{ padding: '20px', marginTop: '20px', height: '900px' }}>
          <RoomInfo room={jsonData.room} />
          <div style={{ marginTop: '20px' }}>
            <TextareaAutosize
              rowsMin={3}
              placeholder="Type your message..."
              value={newMessage}
              onChange={handleNewMessageChange}
              style={{ width: '89%', height: '100px' }}

              onKeyDown={e => {
                if (e.key === 'Enter') {
                  handleSendMessage();
                }
              }}
            />
            <br />
            <Button variant="contained" color="primary" onClick={handleSendMessage}>
              Send Message
            </Button>
          </div>

          <div style={{ marginTop: '20px' }}>
            {jsonData.messages.map((message) => (
              <div
                key={message.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '10px',
                  width: '89%',
                }}
              >
                <img src={
                  process.env.NODE_ENV === 'development'
                    ? `http://localhost:7777/static/img/${message.sender.avatar_url}`
                    : `https://ron-the-rocker.net/ndrr/static/img/${message.sender.avatar_url}`
                }
                  alt="Icon"
                  width="60"
                  height="60"
                />
                <div
                  style={{
                    marginLeft: '10px',
                    backgroundColor: '#e0e0e0',
                    borderRadius: '8px',
                    padding: '8px',
                    width: 'calc(100% - 60px)',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="subtitle1"><strong>{message.sender.username}</strong> <Typography variant="caption">{message.sender.trip}</Typography></Typography>
                    <Typography variant="caption">{message.sent_at}  ( karma {message.sender.karma} - {message.sender.privilege} : login {message.sender.lastlogin_at} )</Typography>
                  </div>
                  <Typography variant="body1">{message.content}</Typography>
                </div>
              </div>
            ))}
          </div>
        </Paper>
      ) : (
        <CircularProgress />
      )}
    </Container>
  );
}

export default Room;