import React, { useState, useEffect, useRef } from "react";
import { useLocation, useParams } from "react-router-dom";
import { Send as SendIcon } from "@mui/icons-material"; // SendIconをインポート

import { ReactKeycloakProvider, useKeycloak } from "@react-keycloak/web";
import Keycloak from "keycloak-js";
import Alert from "@mui/material/Alert";
import {Button,CircularProgress,Container,Paper,Typography,TextareaAutosize} from "@mui/material";
import RoomInfo from "./RoomInfo";
import UserProfilePopup from "./UserProfilePopup";
import RoomComponent from "./RoomComponent"; // 新しく作成したコンポーネントをインポート

function Room() {
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const location = useLocation();
  const [jsonData, setJsonData] = useState(null);

  const messageContainerRef = useRef(null);

  const [error, setError] = useState(null);
   const messageInputRef = useRef(null); // useRefを使ってmessageInputRefを定義

  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックの使用
 

  useEffect(() => {
    if (initialized && keycloak.authenticated) {
      const apiUrl = window.location.href.startsWith(
        "https://ron-the-rocker.net/",
      )
        ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/messages`
        : `http://localhost:7777/room/${roomId}/messages`;
      const headers = new Headers();
      headers.append("Authorization", `Bearer ${keycloak.token}`);

      const fetchData = async () => {
        try {
          const timeoutPromise = new Promise((_, reject) =>
            setTimeout(() => reject(new Error('timeout')), 2500),
          );
          const response = await Promise.race([
            fetch(apiUrl, { headers }),
            timeoutPromise,
          ]);

          if (response.ok) {
            const data = await response.json();
            setJsonData(data);
            if (messageContainerRef.current) {
              messageContainerRef.current.scrollTop =
                messageContainerRef.current.scrollHeight;
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
          clearInterval(fetchInterval); // エラーが発生したらintervalを解除する

        }
      };
      fetchData();
      const fetchInterval = setInterval(fetchData, 1000);
      return () => {
        clearInterval(fetchInterval);
      };
    }
  }, [initialized, keycloak.authenticated]);

  if (!initialized) {
    return <CircularProgress />;
  }

  if (!keycloak.authenticated) {
    return (
      <Container>
        <Button
          variant="contained"
          color="primary"
          onClick={() => keycloak.login()}
        >
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
    <RoomComponent
      jsonData={jsonData}
      messageInputRef={messageInputRef}
      messageContainerRef={messageContainerRef}
      error={error}
      keycloak={keycloak}
      initialized={initialized}
    />);
 }

export default Room;
