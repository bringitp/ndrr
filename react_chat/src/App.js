import React, { useState, useEffect, useRef } from 'react';
import { ReactKeycloakProvider, useKeycloak } from '@react-keycloak/web';
import Keycloak from 'keycloak-js';
import {
  Button,
  CircularProgress,
  Container,
  Paper,
  Typography,
  TextareaAutosize,
} from '@mui/material';
import RoomInfo from './RoomInfo';

const keycloakConfigLocal = {
  url: 'https://ron-the-rocker.net/auth',
  realm: 'ndrr',
  clientId: 'react-local',
  resource: 'test',
};

const useKeycloakConfig = keycloakConfigLocal;
const keycloak = new Keycloak(useKeycloakConfig);

function App() {
  return (
    <ReactKeycloakProvider authClient={keycloak}>
      <MainComponent />
    </ReactKeycloakProvider>
  );
}

function ChatMessage({ message, isMyMessage }) {
  const messageStyle = isMyMessage ? styles.myMessage : styles.otherMessage;

  return (
    <div key={message.id} style={{ ...styles.messageContainer, ...messageStyle, marginBottom: '0px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', width: '100%' }}>
        <div>
          <Typography variant="subtitle1">{message.sender.username}</Typography>
          <Typography variant="body1">{message.content}</Typography>
        </div>
        <div>
          <Typography variant="caption">{formatDate(message.sent_at)}</Typography>
        </div>
      </div>
    </div>
  );
}

function formatDate(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleString();
}

function MainComponent() {
  const { keycloak, initialized } = useKeycloak();
  const [jsonData, setJsonData] = useState(null);
  const [newMessage, setNewMessage] = useState('');
  const messageContainerRef = useRef(null);

  useEffect(() => {
    if (initialized && keycloak.authenticated) {
      const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/ndrr/static')
        ? 'https://ron-the-rocker.net/ndrr/api/rooms/1/messages'
        : 'http://localhost:7777/rooms/1/messages';

      const headers = new Headers();
      headers.append('Authorization', `Bearer ${keycloak.token}`);

      const fetchData = async () => {
        try {
          const response = await fetch(apiUrl, { headers });
          if (response.ok) {
            const data = await response.json();
            setJsonData(data);
            if (messageContainerRef.current) {
              messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
            }
          } else {
            console.error('Error fetching data:', response.status);
          }
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      };

      fetchData();
      const fetchInterval = setInterval(fetchData, 1500);
      return () => {
        clearInterval(fetchInterval);
      };
    }
  }, [initialized, keycloak.authenticated]);

  const handleNewMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSendMessage = async () => {
    const apiUrl = window.location.href.startsWith('https://ron-the-rocker.net/ndrr/static')
      ? 'https://ron-the-rocker.net/ndrr/api/rooms/1/messages'
      : 'http://localhost:7777/rooms/1/messages';

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
                <img src="http://flat-icon-design.com/f/f_event_98/s128_f_event_98_0bg.png" alt="Icon" width="60" height="60" />
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
                    <Typography variant="subtitle1">{message.sender.username}</Typography>
                    <Typography variant="caption">{message.sent_at}  ( karma {message.sender.karma} )</Typography>
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

const styles = {
  messageContainer: {
    display: 'flex',
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
  },
  myMessage: {
    backgroundColor: '#007bff',
    color: '#fff',
    padding: '8px 16px',
    borderRadius: '20px',
    position: 'relative',
    maxWidth: '60%',
  },
  otherMessage: {
    backgroundColor: '#eee',
    color: '#333',
    padding: '8px 16px',
    borderRadius: '20px',
    position: 'relative',
    margin: '0 auto 0 8px',
    maxWidth: '60%',
  },
};

export default App;
