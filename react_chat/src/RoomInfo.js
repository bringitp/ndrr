import React from 'react';
import { Card, CardContent, Typography, CardActions, Button, Grid } from '@mui/material';
import Box from '@mui/material/Box';

const bull = (
  <Box
    component="span"
    sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
  >
    •
  </Box>
);

function RoomInfo({ room }) {
  return (
<Card sx={{ maxWidth: 970 }}>
  <CardContent>
    <Grid container spacing={3}>
      <Grid item xs={2}>
        <Typography><strong>host : {room.room_owner_name}</strong></Typography>
      </Grid>

      <Grid item xs={4}>
        <Typography><strong>{room.room_name} ({room.room_count}/{room.room_max_capacity}) 🌟 ⬆️ {room.room_restricted_karma_over_limit} ⬇️ {room.room_restricted_karma_under_limit}</strong></Typography>
      </Grid>
      <Grid item xs={4}>
        <Typography>{room.room_label}</Typography>
      </Grid>

    </Grid>
  </CardContent>
</Card>

  );
}

export default RoomInfo;
