import React, { useState, useEffect, useRef } from 'react';
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
import NaviBar from './NaviBar'; // Naviバーのインポート
import { ReactKeycloakProvider, useKeycloak } from "@react-keycloak/web";
import Keycloak from "keycloak-js";

const RoomList = () => {
  const [rooms, setRooms] = useState([]);
  const [navBarWidth, setNavBarWidth] = useState(null);
  const navBarRef = useRef(null); // useRefを使用してNaviBarコンポーネントに対する参照を作成

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


  const { keycloak, initialized } = useKeycloak(); // useKeycloak hook

  useEffect(() => {
    if (initialized && keycloak.authenticated) {
      const token = keycloak.token; // Access the Keycloak token
      // Now you can use the 'token' variable as needed.
      alert(token); // Example: Display the token in an alert
    }
  }, [initialized, keycloak.authenticated]);



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

  // Define the function to handle joining a room
  const handleJoin = async (roomId) => {
    try {
      // Data object to send in the request
      const data = {
        member_id: 1, // Replace with the appropriate member_id
      };
      alert(keycloak.token);
      // Send a PUT request to join the room
      const response = await fetch(`http://localhost:7777/room/${roomId}/join_me`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${keycloak.token}`, // Include the token
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        // Redirect to the desired URL after joining
        window.location.href = `http://localhost:3000/room/${roomId}`; // Replace with your desired redirect URL
      } else {
        console.error("Error joining the room:", response.status);
      }
    } catch (error) {
      console.error("Error joining the room:", error);
    }
  };


  return (
    <Grid container spacing={1}>
      {rooms.map((room, index) => (
        <Grid item xs={11} sm={5} md={6} key={room.id}> {/* グリッドのサイズを調整 */}
    <Grid item xs={1} sm={1} md={1}>
        <NaviBar />
    </Grid>
          <Card
            sx={{
              borderRadius: '16px', // 角丸
              backgroundColor: pastelColors[index % pastelColors.length], // パステルカラー
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              width:   window.innerWidth < 400 ?  '80%': '90%',
              padding: '0px', // 内部の余白
              marginLeft:   window.innerWidth >= 400 ? (index % 2 === 0 ?   '60px' : `35px`) : '50px',
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
                  style={{
                      width: '28px', // アイコンの幅を28pxに設定 (倍のサイズ)
                      height: '28px', // アイコンの高さを28pxに設定 (倍のサイズ)
                }}
               />
              }
             />
              </Typography>
              <Box
                sx={{
                  backgroundColor: 'rgba(0, 0, 0, 0.1)', // 暗い背景色
                  borderRadius: '8px', // 角丸
                  padding: '8px', // 内部の余白
                  
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
                           style={{
                              width: '28px', // アイコンの幅を28pxに設定 (倍のサイズ)
                              height: '28px', // アイコンの高さを28pxに設定 (倍のサイズ)
                           }}
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
            color="secondary"
            size="small"
            onClick={() => handleJoin(room.id)} // Pass the room ID when the button is clicked
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
