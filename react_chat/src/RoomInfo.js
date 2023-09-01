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
  const handleModalOpen = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

 const apiUrl = window.location.href.startsWith(
  "https://ron-the-rocker.net/"
)
  ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/condition`
  : `http://localhost:7777/room/${roomId}/condition`;
const headers = new Headers();
headers.append("Authorization", `Bearer ${keycloak.token}`);

useEffect(() => {
  fetch(apiUrl, { headers })
    .then(response => response.json())
    .then(data => setRoomMembers(data.room_member))
    .catch(error => console.error('ルームメンバーの取得中にエラーが発生しました:', error));
}, [apiUrl]); // Dependency array with apiUrl

 const handleStartChat = (userId) => {
  // Simulate starting a chat with the selected user
  console.log(`Starting chat with user ${userId}`);
  
  // You can implement your actual chat logic here, such as opening a chat window or navigating to a chat page
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
            top: '90%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '40%', // Set width to 40% of the screen size
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
        <TableCell>Start Chat</TableCell> {/* Add a new column for the chat button */}
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
              </div>
            )}
          </TableCell>
          <TableCell>{member.username}</TableCell>
          <TableCell>
            <input type="checkbox" />
          </TableCell>
          <TableCell>
            <Button
              variant="contained"
              color="primary"
              onClick={() => handleStartChat(member.user_id)} // Call your start chat function here
            >
              Start Chat
            </Button>
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
