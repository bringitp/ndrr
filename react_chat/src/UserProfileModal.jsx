import React, { useState } from 'react';
import { Modal, Box, Typography, TextField, Button } from '@mui/material';

const UserProfileModal = ({ user, onClose, onSave }) => {
  const [editedUser, setEditedUser] = useState({ ...user });

  const handleClose = () => {
    setEditedUser({ ...user }); // 編集をキャンセルして元のユーザ情報に戻す
    onClose();
  };

  const handleSave = () => {
    // データを保存するための処理を実行
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
          {/* 新しいフィールドを追加 */}
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
          {/* 他のフィールドも同様に追加 */}
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
