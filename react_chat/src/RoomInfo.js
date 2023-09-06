import React, { useState, useEffect, useCallback } from 'react';
import { useLocation, useParams } from "react-router-dom";
import { Card, CardContent, Typography, Grid, Modal, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import Box from '@mui/material/Box';
import { ReactKeycloakProvider, useKeycloak } from "@react-keycloak/web";
// UserModal.jsをインポート
import UserModal from './UserModal';
import EditRoomModal from './EditRoomModal';
import EditAdminModal from './EditAdminModal';


const RoomHeader = React.memo(({ room }) => {
  return (
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
  );
});

function RoomInfo({jsonData}) {
  const [room, setRoom] = useState(jsonData.room);
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const [roomMembers, setRoomMembers] = useState([]);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックの使用
  const [isChatWindowOpen, setIsChatWindowOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [isUserModalOpen, setUserModalOpen] = useState(false);
  const [isEditRoomModalOpen, setEditRoomModalOpen] = useState(false);
  const [isEditAdminModalOpen, setEditAdminModalOpen] = useState(false); // 新しく追加

  const handleUserModalOpen = useCallback(() => setUserModalOpen(true), []);
  const handleUserModalClose = useCallback(() => setUserModalOpen(false), []);
  const handleEditRoomModalOpen = useCallback(() => setEditRoomModalOpen(true), []);
  const handleEditRoomModalClose = useCallback(() => setEditRoomModalOpen(false), []);
  const handleEditAdminModalOpen = useCallback(() => setEditAdminModalOpen(true), []);
  const handleEditAdminModalClose = useCallback(() => setEditAdminModalOpen(false), []);

  const headers = new Headers();
  headers.append("Authorization", `Bearer ${keycloak.token}`);

  return (
    <Card sx={{ width: '98%' }}>
      <CardContent>
        <RoomHeader room={jsonData.room} />
      </CardContent>
      <Button onClick={handleUserModalOpen}>🔊</Button>
      {jsonData.room.room_owner_id === jsonData.room.room_login_user_id && (
        <Button onClick={handleEditRoomModalOpen}>⚙</Button>
      )}
      {jsonData.room.room_owner_id === jsonData.room.room_login_user_id && (
        <Button onClick={handleEditAdminModalOpen}>🔨</Button>
      )}
      <UserModal
        isUserModalOpen={isUserModalOpen}
        handleModalClose={handleUserModalClose}
        token={keycloak.token}
        jsonData={jsonData}
      />
      <EditRoomModal
        isOpen={isEditRoomModalOpen}
        onClose={handleEditRoomModalClose}
        maxCapacity={jsonData.room.room_max_capacity}
        roomTitle={jsonData.room.room_name}
        roomLabel={jsonData.room.room_label}
        token={keycloak.token}
        jsonData={jsonData}
      />
      <EditAdminModal
        isOpen={isEditAdminModalOpen}
        onClose={handleEditAdminModalClose}
        roomMembers={jsonData.roomMembers}
        token={keycloak.token}
        jsonData={jsonData}
      />
    </Card>
  );
}

export default RoomInfo;
