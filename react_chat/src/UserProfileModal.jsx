import React, { useState, useEffect } from 'react';
import { Modal, Box, Typography, TextField, Button, InputLabel } from '@mui/material';

const UserProfileModal = ({ user, onClose, onSave, userToken }) => {
  const [editedUser, setEditedUser] = useState({
    username: '',
    profile: '',
    trip: '',
    life: '',
    karma: '',
    // 他のフィールドも同様に初期値を設定
  });
  const [avatarUrl, setAvatarUrl] = useState('');

  // データを取得する関数
  const fetchUserProfileData = async () => {
    try {
      const apiUrl = window.location.href.startsWith(
        "https://ron-the-rocker.net/"
      )
        ? `https://ron-the-rocker.net/ndrr/api/user/profile`
        : `http://localhost:7777/user/profile`;

      const response = await fetch(apiUrl, {
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

        // ユーザー情報を更新
        setEditedUser({
          username: userData.user_profile.username,
          profile: userData.user_profile.profile,
          trip: userData.user_profile.trip,
          life: userData.user_profile.life,
          karma: userData.user_profile.karma,
          // 他のフィールドも同様に設定
        });
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
    setEditedUser({
      username: '',
      profile: '',
      trip: '',
      life: '',
      karma: '',
      // 他のフィールドも同様に初期値に戻す
    });
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
          <InputLabel htmlFor="karma">Karma</InputLabel> {/* KarmaのInputLabel */}
          <TextField
            id="karma"
            name="karma"
            value={editedUser.karma}
            onChange={handleInputChange}
            fullWidth
            margin="normal"
          />
          <InputLabel htmlFor="life">Life</InputLabel> {/* LifeのInputLabel */}
          <TextField
            id="life"
            name="life"
            value={editedUser.life}
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
