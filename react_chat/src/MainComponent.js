import React, { useState, useEffect, useRef } from 'react';
import { useKeycloak } from '@react-keycloak/web'; // 追加

import {
  Button,
  CircularProgress,
  Container,
  Paper,
  Typography,
  TextareaAutosize,
} from '@mui/material';
import RoomInfo from './RoomInfo';

function MainComponent() {
  const { keycloak, initialized } = useKeycloak(); // useKeycloakを使用
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
      const fetchInterval = setInterval(fetchData, 2000);

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


      <div style={{ marginTop: '20px' }}>
        <TextareaAutosize
          rowsMin={3}
          placeholder="Type your message..."
          value={newMessage}
          onChange={handleNewMessageChange}
          style={{ width: '100%' }}
        />
        <Button variant="contained" color="primary" onClick={handleSendMessage} style={{ marginTop: '10px' }}>
          Send Message
        </Button>
      </div>
    </Container>
  );
}

export default MainComponent;
