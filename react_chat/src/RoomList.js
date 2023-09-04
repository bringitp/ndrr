import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Box,
} from '@mui/material';

const RoomList = () => {
  const [rooms, setRooms] = useState([]);

  const apiUrl = window.location.href.startsWith(
    "https://ron-the-rocker.net/"
   )
     ? `https://ron-the-rocker.net/ndrr/api/rooms`
     : `http://localhost:7777/rooms`;

  useEffect(() => {
    // APIから部屋一覧を取得する処理を追加
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        setRooms(data.rooms);
      })
      .catch((error) => {
        console.error('部屋一覧を取得中にエラーが発生しました:', error);
      });
  }, []);

  return (
    <Grid container spacing={2}>
      {rooms.map((room) => (
        <Grid item xs={12} sm={6} md={4} key={room.id}>
          <Card
            sx={{
              borderRadius: '16px', // 角丸
              backgroundColor: '#f3f3f3', // パステルカラー
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
            }}
          >
            <CardContent>
              <Typography variant="h5" gutterBottom>
                {room.name}
              </Typography>
              <Typography variant="body2">
                <strong>Owner:</strong> {room.owner.username}
              </Typography>
              <Typography variant="body2">
                <strong>Capacity:</strong> {room.max_capacity}
              </Typography>
              <Typography variant="body2">
                <strong>Status:</strong> {room.status}
              </Typography>
              <Typography variant="body2">
                <strong>Last Activity:</strong> {room.last_activity}
              </Typography>
              <Box mt={2}>
                <Button variant="outlined" color="primary">
                  Join
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default RoomList;
