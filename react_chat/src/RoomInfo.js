import React from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import Box from '@mui/material/Box';

function RoomInfo({ room }) {
  return (
    <Card sx={{ width: '92%', maxWidth: 970 }}>
      <CardContent>
        <Grid container spacing={1}>
          <Grid item xs={5}>
            <Typography><strong>Login : {room.room_login_user_name}</strong></Typography>
            <Typography><strong>Host : {room.room_owner_name}</strong></Typography>
          </Grid>

          <Grid item xs={7}>
            <Typography><strong>{room.room_name} ({room.room_count}/{room.room_max_capacity}) 🌟 ⬆️ {room.room_restricted_karma_over_limit} ⬇️ {room.room_restricted_karma_under_limit}</strong></Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography>{room.room_label}</Typography>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}

export default RoomInfo;
