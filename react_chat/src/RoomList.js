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

  // パステルカラーの配列
  const pastelColors = ['#E6E6FA', '#B0C4DE', '#FFDAB9'];

  // 時刻を簡略な形式に変換する関数
  const simplifyTime = (timestamp) => {
    const date = new Date(timestamp);
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const timeString = `${hours}:${minutes < 10 ? '0' : ''}${minutes}`;
    return timeString;
  };

  return (
    <Grid container spacing={2}>
      {rooms.map((room, index) => (
        <Grid item xs={12} sm={6} md={4} key={room.id}>
<Card
  sx={{
    borderRadius: '16px', // 角丸
    backgroundColor: pastelColors[index % pastelColors.length], // パステルカラー
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    width: '90%', // カードの幅を90%に設定
    marginLeft: '5%', // カードの左側に5%の余白を持たせる
    padding: '2px', // 内部の余白
    marginTop: '0px', // 上のマージンを短くする
    marginBottom: '0px', // 下のマージンを短くする
  }}
>
            <CardContent>
              <Typography
                variant="h8"
                gutterBottom
                sx={{
                  fontSize: '1.2rem', // 部屋名のフォントサイズを大きく
                  fontWeight: 'bold', // 部屋名を太字に
                  color: '#333', // 部屋名のカラーを暗い色に設定
                  display: 'flex', // 横並びにする
                  alignItems: 'center', // 縦方向の中央揃え
                }}
              >
                {room.name} : 
           <Chip
              label={room.owner_username}
              style={{ margin: '4px' }}
               avatar={
               <Avatar
                  src={
                     process.env.NODE_ENV === 'development'
                     ? `http://localhost:7777/static/img/${room.owner_avatar_url}`
                     : `https://ron-the-rocker.net/ndrr/api/static/img/${room.owner_avatar_url}`
                }
               />
              }
             />
              </Typography>
              <Box
                sx={{
                  backgroundColor: 'rgba(0, 0, 0, 0.1)', // 暗い背景色
                  borderRadius: '8px', // 角丸
                  padding: '8px', // 内部の余白
                  mt: 1, // 上の余白
                }}
              >
                <Typography variant="body2">
                     <strong>🚪:</strong> {room.status} <strong>🪣:</strong> {room.max_capacity}　<strong>⌚:</strong> {simplifyTime(room.last_activity)}
                </Typography>
              </Box>
              {room.label && (
                <Box
                  sx={{
                    backgroundColor: 'rgba(0, 0, 0, 0.1)', // 暗い背景色
                    borderRadius: '8px', // 角丸
                    padding: '8px', // 内部の余白
                    mt: 1, // 上の余白
                  }}
                >
                  <Typography variant="body2">
                    <strong>📝:</strong> {truncateLabel(room.label)}
                  </Typography>
                </Box>
              )}
              {room.room_members.length > 0 && (
                <Box mt={2}>
                  <Box display="flex" alignItems="center" flexWrap="wrap">
                    {room.room_members.map((member) => (
                      <Chip
                        key={member.id}
                        label={member.username}
                        style={{ margin: '4px' , 
                               fontSize: '1.0rem', // 部屋名のフォントサイズを大きく
                                }}
                        avatar={
                          <Avatar
                            src={
                              process.env.NODE_ENV === 'development'
                                ? `http://localhost:7777/static/img/${member.avatar_url}`
                                : `https://ron-the-rocker.net/ndrr/api/static/img/${member.avatar_url}`
                            }
                          />
                        }
                      />
                    ))}
                  </Box>
                </Box>
              )}
            </CardContent>
            <Box m={1} sx={{ alignSelf: 'flex-end' }}>
              <Button
                variant="contained"
                color="secondary" // ボタンのカラーを赤に設定
                size="small" // ボタンのサイズを小さく
              >
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
