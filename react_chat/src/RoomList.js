import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Box,
  Chip,
  Avatar,
} from '@mui/material';

const RoomList = () => {
  const [rooms, setRooms] = useState([]);

  const apiUrl = window.location.href.startsWith(
    'https://ron-the-rocker.net/'
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

  // ラベルを30文字までに制限する関数
  const truncateLabel = (label) => {
    if (label.length <= 30) {
      return label;
    } else {
      return label.slice(0, 30) + '...';
    }
  };

  return (
    <Grid container spacing={2}>
      {rooms.map((room) => (
        <Grid item xs={12} sm={6} md={4} key={room.id}>
          <Card
            sx={{
              borderRadius: '16px', // 角丸
              backgroundColor: '#FFE4E1', // パステルカラー
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <CardContent>
              <Box display="flex" justifyContent="space-between">
                <Typography variant="h5" gutterBottom>
                  {room.name}
                </Typography>
                <Box display="flex" alignItems="center">
                  <strong>Owner:</strong>
                  <Avatar
                    alt={room.owner.username}
                    src={room.owner.avatar_id} // ここにユーザのアバター画像のURLを設定
                    sx={{ ml: 1, width: 32, height: 32 }} // アイコンのスタイリング
                  />
                  <span style={{ marginLeft: '4px' }}>
                    ✩{room.owner.username}
                  </span>
                </Box>
              </Box>
              <Typography variant="body2">
                <strong>Capacity:</strong> {room.max_capacity}
              </Typography>
              <Typography variant="body2">
                <strong>Status:</strong> {room.status}
              </Typography>
              <Typography variant="body2">
                <strong>Last Activity:</strong> {room.last_activity}
              </Typography>
              {room.label && (
                <Typography variant="body2">
                  <strong>Label:</strong> {truncateLabel(room.label)}
                </Typography>
              )}
              {room.room_members.length > 0 && (
                <Box mt={2}>
                  <Typography variant="body2">
                    <strong>Members:</strong>
                  </Typography>
                  <Box display="flex" alignItems="center" flexWrap="wrap">
                    {room.room_members.map((member) => (
                      <Chip
                        key={member.id}
                        label={member.username}
                        avatar={
                          <Avatar>
                            {member.username.charAt(0).toUpperCase()}
                          </Avatar>
                        }
                        style={{ margin: '4px' }}
                      />
                    ))}
                  </Box>
                </Box>
              )}
            </CardContent>
            <Box m={1}>
              <Button variant="contained" color="primary" fullWidth>
                Join
              </Button>
            </Box>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default RoomList;
