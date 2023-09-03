import React, { useState, useEffect } from 'react';
import { useLocation, useParams } from "react-router-dom";
import { Card, CardContent, Typography, Grid, Modal, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import Box from '@mui/material/Box';
import { ReactKeycloakProvider, useKeycloak } from "@react-keycloak/web";

function RoomInfo({ room }) {
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [roomMembers, setRoomMembers] = useState([]);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックの使用
  const [isChatWindowOpen, setIsChatWindowOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');

  const handleModalOpen = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
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
      <Modal open={isModalOpen} onClose={handleModalClose}>
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '90%', // Set width to 95% of the screen size
            bgcolor: 'background.paper',
            boxShadow: 24,
            p: 4,
            maxHeight: '80vh', // Set maximum height of the modal content
            overflowY: 'auto', // Enable vertical scrolling if content overflows
          }}
        >
          <Typography variant="h6" component="h2" gutterBottom>
            Control Menu
          </Typography>
          {/* Display the room member data in a table */}
<TableContainer component={Paper}>
  <Table>
    <TableHead>
      <TableRow>
        <TableCell>Avatar</TableCell>
        <TableCell>Username</TableCell>
        <TableCell>Ignore</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {roomMembers.map(member => (
        <TableRow key={member.user_id}>
          <TableCell>
            {member.avatar_url && (
              <div
                style={{
                  position: 'relative',
                  display: 'inline-block',
                  width: 50,
                  height: 50,
                }}
              >
                <img
                  src={
                    process.env.NODE_ENV === 'development'
                      ? `http://localhost:7777/static/img/${member.avatar_url}`
                      : `https://ron-the-rocker.net/ndrr/api/static/img/${member.avatar_url}`
                  }
                  alt={`Avatar of ${member.username}`}
                  width="50"
                  height="50"
                  style={{ borderRadius: '15%' }}
                />
                {/* Cross symbol */}
                {member.checked && (
                  <div
                    style={{
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      width: '100%',
                      height: '100%',
                      display: 'flex',
                      justifyContent: 'center',
                      alignItems: 'center',
                      fontSize: '4em', // Increase font size for a larger cross
                      color: 'red',
                    }}
                  >
                    &#10060; {/* Unicode for the cross symbol */}
                  </div>
                )}
              </div>
            )}
          </TableCell>
          <TableCell>{member.username}</TableCell>
          <TableCell>
            <input
              type="checkbox"
              checked={member.checked}
              onChange={() => {
                // チェックボックスの状態をトグル
                const updatedMembers = roomMembers.map(m => {
                  if (m.user_id === member.user_id) {
                    return { ...m, checked: !m.checked };
                  }
                  return m;
                });
                setRoomMembers(updatedMembers);

                if (member.checked) { // 注意。イベントが逆になってる
                  // チェックを外した場合にブロックリスト解除
                   removeFromBlockList(member.user_id);
                } else {
                  // チェックを付けた場合にブロックリストに追
                   addToBlockList(member.user_id);
                }
              }}
            />
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
</TableContainer>

          <Button onClick={handleModalClose}>Close</Button>
        </Box>
      </Modal>
    </Card>
  );
}

export default RoomInfo;
