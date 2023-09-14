import React, { useState, useEffect } from 'react';
import { Modal, Box, Typography, TextField, Button } from '@mui/material';

const UserProfileModal = ({ user, onClose, onSave, userToken }) => {
  const [editedUser, setEditedUser] = useState({ ...user });
  const [avatarUrl, setAvatarUrl] = useState(''); // アバター画像のURLを格納するステート

  // データを取得する関数
  const fetchUserProfileData = async () => {
    try {
      const response = await fetch('http://localhost:7777/user/profile', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${userToken}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setAvatarUrl(
          process.env.NODE_ENV === 'development'
            ? `http://localhost:7777/static/img/${userData.avatar_url}`
            : `https://ron-the-rocker.net/ndrr/api/static/img/${userData.avatar_url}`
        );

        setEditedUser(userData.user_profile); // アバター画像のURLをステートに設定
      } else {
        // エラーハンドリング
        console.error('Failed to fetch user profile data');
      }
    } catch (error) {
      console.error('An error occurred while fetching user profile data', error);
    }
  };

  useEffect(() => {
    // モーダルが開かれた時にデータを取得する
    fetchUserProfileData();
  }, []); // 空の依存リストを指定して一度だけ実行

  const handleClose = () => {
    setEditedUser({ ...user });
    onClose();
  };

  const handleSave = () => {
    onSave(editedUser);
    onClose();
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditedUser({ ...editedUser, [name]: value });
  };

  return (
    <Modal open={true} onClose={handleClose}>
      <Box
        sx={{
          position: 'absolute',
          width: '300px',
          bgcolor: 'background.paper',
          border: '2px solid #000',
          boxShadow: 24,
          p: 2,
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
        }}
      >
        <Typography variant="h6">Edit User Profile</Typography>
        {/* アバター画像を表示し、中央に揃える */}
        <img
          src={avatarUrl}
          alt="Avatar"
          style={{ width: '100px', height: '100px', margin: '0 auto', display: 'block' }}
        />
        <form>
          <TextField
            label="Username"
            name="username"
            value={editedUser.username}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Profile"
            name="profile"
            value={editedUser.profile}
            onChange={handleInputChange}
            fullWidth
            multiline
            rows={4}
            margin="normal"
          />
          <TextField
            label="Trip"
            name="trip"
            value={editedUser.trip}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Life"
            name="life"
            value={editedUser.life}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Karma"
            name="karma"
            value={editedUser.karma}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <Button variant="contained" color="primary" onClick={handleSave}>
            Save
          </Button>
          <Button variant="outlined" color="secondary" onClick={handleClose}>
            Cancel
          </Button>
        </form>
      </Box>
    </Modal>
  );
};

export default UserProfileModal;
