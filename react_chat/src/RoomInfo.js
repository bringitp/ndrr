import React, { useState, useEffect } from 'react';
import { useLocation, useParams } from "react-router-dom";
import { Card, CardContent, Typography, Grid, Modal, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import Box from '@mui/material/Box';
import { ReactKeycloakProvider, useKeycloak } from "@react-keycloak/web";
// UserModal.jsをインポート
import UserModal from './UserModal';
import EditRoomModal from './EditRoomModal';
import EditAdminModal from './EditAdminModal';

function RoomInfo({ room }) {
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const [roomMembers, setRoomMembers] = useState([]);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックの使用
  const [isChatWindowOpen, setIsChatWindowOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [isUserModalOpen, setUserModalOpen] = useState(false);
  const [isEditRoomModalOpen, setEditRoomModalOpen] = useState(false);
  const [isEditAdminModalOpen, setEditAdminModalOpen] = useState(false); // 新しく追加

  const handleEditAdminModalOpen = () => {
    setEditAdminModalOpen(true);
  };

  const handleEditAdminModalClose = () => {
    setEditAdminModalOpen(false);
  };

  const handleUserModalOpen = () => {
    setUserModalOpen(true);
  };

  const handleUserModalClose = () => {
    setUserModalOpen(false);
  };

  const handleEditRoomModalOpen = () => {
    setEditRoomModalOpen(true);
  };

  const handleEditRoomModalClose = () => {
    setEditRoomModalOpen(false);
  };

 const headers = new Headers();
 headers.append("Authorization", `Bearer ${keycloak.token}`);

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
          <Typography>
            <strong>Login: {room.room_login_user_name}</strong>
          </Typography>
          <Typography>
            <strong>Host: {room.room_owner_name}</strong>
          </Typography>
        </Grid>
        <Grid item xs={7}>
          <Typography>
            <strong>
              {room.room_name} 🌟 ⬆️ {room.room_restricted_karma_over_limit} ⬇️ {room.room_restricted_karma_under_limit} ({room.room_member_count}/{room.room_max_capacity})
            </strong>
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>{room.room_label}</Typography>
        </Grid>
      </Grid>
    </CardContent>
    <Button onClick={handleUserModalOpen}>🔊</Button>
    {/* ⚙ ボタンの表示を制御 */}
    {room.room_owner_id === room.room_login_user_id && (
      <Button onClick={handleEditRoomModalOpen}>⚙</Button>
    )}
    {/* 🔨 ボタンの表示を制御 */}
    {room.room_owner_id === room.room_login_user_id && (
      <Button onClick={handleEditAdminModalOpen}>🔨</Button>
    )}
    {/* UserModalコンポーネントを使用 */}
    <UserModal
      isUserModalOpen={isUserModalOpen}
      handleModalClose={handleUserModalClose}
      token={keycloak.token}
    />
    {/* EditRoomModalコンポーネントを使用 */}
    <EditRoomModal
      isOpen={isEditRoomModalOpen}
      onClose={handleEditRoomModalClose}
      maxCapacity={room.room_max_capacity}
      roomTitle={room.room_name}
      roomLabel={room.room_label}
      token={keycloak.token}
    />
    <EditAdminModal
      isOpen={isEditAdminModalOpen}
      onClose={handleEditAdminModalClose}
      roomMembers={roomMembers}
      token={keycloak.token}
    />
  </Card>
);
}

export default RoomInfo;
