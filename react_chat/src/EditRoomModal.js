import React, { useState, useEffect} from 'react';
import { useLocation, useParams } from "react-router-dom";
import {
  Box,
  Typography,
  Modal,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';

function EditRoomModal({ isOpen, onClose,  roomTitle, roomLabel, maxCapacity, token }) {
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const [editedRoomTitle, setEditedRoomTitle] = useState(roomTitle);
  const [editedRoomLabel, setEditedRoomLabel] = useState(roomLabel);
  const [editedMaxCapacity, setEditedMaxCapacity] = useState(maxCapacity);

  const handleSave = () => {
    // 保存ボタンがクリックされたときの処理
    onClose();
    // API へデータを送信
    const apiUrl = window.location.href.startsWith("https://ron-the-rocker.net/")
      ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}`
      : `http://localhost:7777/room/${roomId}`;
    
    const data = {
      room_name: editedRoomTitle,
      max_capacity: editedMaxCapacity,
      room_label: editedRoomLabel,
    };

    postData(apiUrl, data, token)
      .then(response => {
        if (response.ok) {
          console.log('Room data saved successfully.');
        } else {
          console.error('Failed to save room data.');
        }
      })
      .catch(error => {
        console.error('Error while saving room data:', error);
      });
  };

  // APIへのPOSTリクエストを送信する関数
  const postData = async (url, data, token) => {
    const headers = new Headers({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    });

    const response = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(data),
    });

    return response;
  };

  return (
    <Modal open={isOpen} onClose={onClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '90%',
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
          maxHeight: '80vh',
          overflowY: 'auto',
        }}
      >
        <Typography variant="h6" component="h2" gutterBottom>
          Edit Room
        </Typography>

        <TextField
          label="Room Title"
          fullWidth
          margin="normal"
          value={editedRoomTitle}
          onChange={(e) => setEditedRoomTitle(e.target.value)}
        />

        <TextField
          label="Room Label"
          fullWidth
          margin="normal"
          value={editedRoomLabel}
          onChange={(e) => setEditedRoomLabel(e.target.value)}
        />

        <FormControl fullWidth margin="normal">
          <InputLabel style={{ marginBottom: '8px' }}>Max Capacity</InputLabel>
          <Select
            value={editedMaxCapacity}
            onChange={(e) => setEditedMaxCapacity(e.target.value)}
          >
            {[...Array(19).keys()].map((num) => (
              <MenuItem key={num + 2} value={num + 2}>
                {num + 2}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button onClick={handleSave} variant="contained" color="primary">
          Save
        </Button>

        <Button onClick={onClose} variant="contained" color="secondary">
          Cancel
        </Button>
      </Box>
    </Modal>
  );
}

export default EditRoomModal;
