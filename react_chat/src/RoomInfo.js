import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid, Modal, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import Box from '@mui/material/Box';
import { ReactKeycloakProvider, useKeycloak } from "@react-keycloak/web";

function RoomInfo({ room }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [roomMembers, setRoomMembers] = useState([]);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックの使用
  const handleModalOpen = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  useEffect(() => {
    fetch('http://localhost:7777/room/1/condition', {
      headers: {
        'Authorization':  `Bearer ${keycloak.token}`
      }
    })
    .then(response => response.json())
    .then(data => setRoomMembers(data.room_member))
    .catch(error => console.error('ルームメンバーの取得中にエラーが発生しました:', error));
  }, []);

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
            width: '50%', // Set width to 50% of the screen size
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
                </TableRow>
              </TableHead>
              <TableBody>
                {roomMembers.map(member => (
                  <TableRow key={member.user_id}>
                    <TableCell>
                      {member.avatar_url && (
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
                      )}
                    </TableCell>
                    <TableCell>{member.username}</TableCell>
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
