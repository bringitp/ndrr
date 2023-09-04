import React, { useState, useEffect } from 'react';
import { useLocation, useParams } from "react-router-dom";
import { Card, CardContent, Typography, Grid, Modal, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import Box from '@mui/material/Box';
import { ReactKeycloakProvider, useKeycloak } from "@react-keycloak/web";
// UserModal.jsをインポート
import UserModal from './UserModal';
function RoomInfo({ room }) {
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const [isUserModalOpen, setUserModalOpen] = useState(false);
  const [roomMembers, setRoomMembers] = useState([]);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックの使用
  const [isChatWindowOpen, setIsChatWindowOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');


  const handleModalOpen = () => {
    setUserModalOpen(true);
  };

  const handleModalClose = () => {
    setUserModalOpen(false);
  };

 const headers = new Headers();
headers.append("Authorization", `Bearer ${keycloak.token}`);

  const addToBlockList = (userId) => {
  const apiUrl = window.location.href.startsWith(
  "https://ron-the-rocker.net/"
   )
     ? `https://ron-the-rocker.net/ndrr/api/users/ng-list`
     : `http://localhost:7777/users/ng-list`;

  const headers = new Headers({
    'Authorization': `Bearer ${keycloak.token}`,
    'Content-Type': 'application/json',
  });

  const data = {
    "blocked_user_id": userId,
  };

  fetch(apiUrl, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data),
  })
    .then(response => {
      if (response.ok) {
        // ブロックが成功した場合の処理
        console.log(`User ${userId} has been blocked.`);
      } else {
        // エラーハンドリング
        console.error('ブロック中にエラーが発生しました。');
      }
    })
    .catch(error => {
      console.error('ブロック中にエラーが発生しました:', error);
    });
};

const removeFromBlockList = (userId) => {
 const apiUrl = window.location.href.startsWith(
  "https://ron-the-rocker.net/"
)
  ? `https://ron-the-rocker.net/ndrr/api/users/ng-list`
  : `http://localhost:7777/users/ng-list`;

  const headers = new Headers({
    'Authorization': `Bearer ${keycloak.token}`,
    'Content-Type': 'application/json',
  });

  const data = {
    "blocked_user_id": userId,
  };

  fetch(apiUrl, {
    method: 'DELETE',
    headers: headers,
    body: JSON.stringify(data),
  })
    .then(response => {
      if (response.ok) {
        // 削除が成功した場合の処理
        console.log(`User ${userId} has been unblocked.`);
      } else {
        // エラーハンドリング
        console.error('ブロック解除中にエラーが発生しました。');
      }
    })
    .catch(error => {
      console.error('ブロック解除中にエラーが発生しました:', error);
    });
};

const openChatWindow = () => {
  setIsChatWindowOpen(true);
};
const closeChatWindow = () => {
  setIsChatWindowOpen(false);
};

const apiUrl = window.location.href.startsWith(
    "https://ron-the-rocker.net/"
   )
     ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/condition`
     : `http://localhost:7777/room/${roomId}/condition`;

useEffect(() => {
  fetch(apiUrl, { headers })
    .then(response => response.json())
    .then(data => {
      // チェックボックスの初期状態を設定
      const membersWithCheckbox = data.room_member.map(member => ({
        ...member,
        checked: member.blocked, // blockedフラグがtrueの場合、チェックをつける
      }));
      setRoomMembers(membersWithCheckbox);
    })
    .catch(error => console.error('ルームメンバーの取得中にエラーが発生しました:', error));
}, [apiUrl]);

 const handleStartChat = (userId) => {
  // Simulate starting a chat with the selected user
  console.log(`Starting chat with user ${userId}`);  
  setChatMessage(`Hello, ${userId}!`); // Replace with your own message
  openChatWindow();
};

  return (
    <Card sx={{ width: '98%' }}>
      <CardContent>
        <Grid container spacing={1}>
          <Grid item xs={5}>
            <Typography><strong>Login: {room.room_login_user_name}</strong></Typography>
            <Typography><strong>Host: {room.room_owner_name}</strong></Typography>
          </Grid>
          <Grid item xs={7}>
            <Typography>
              <strong>
                {room.room_name}  🌟 ⬆️ {room.room_restricted_karma_over_limit} ⬇️ {room.room_restricted_karma_under_limit} ({room.room_member_count}/{room.room_max_capacity})
              </strong>
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography>{room.room_label}</Typography>
          </Grid>
        </Grid>
      </CardContent>
      <Button onClick={handleModalOpen}>🔨</Button>
      <Button onClick={handleModalOpen}>⚙</Button>
      {/* UserModalコンポーネントを使用 */}
      <UserModal
        isUserModalOpen={isUserModalOpen}
        handleModalClose={handleModalClose}
        roomMembers={roomMembers}
        setRoomMembers={setRoomMembers}
        removeFromBlockList={removeFromBlockList}
        addToBlockList={addToBlockList}
      />
    </Card>
  );
}

export default RoomInfo;
