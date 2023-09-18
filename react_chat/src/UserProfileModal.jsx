import React, { useState, useEffect } from 'react';
import { Modal, Box, Typography, TextField, Button, InputLabel, Grid ,Alert,AlertTitle} from '@mui/material';

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
          sub: userData.user_profile.sub,
          created_at: userData.user_profile.created_at,
          allowed_name_changes: userData.user_profile.allowed_name_changes,
          penalty_points : userData.user_profile.penalty_points,
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


const handleSave = async () => {
  try {
    const apiUrl = window.location.href.startsWith(
      "https://ron-the-rocker.net/"
    )
      ? `https://ron-the-rocker.net/ndrr/api/user/profile`
      : `http://localhost:7777/user/profile`;

    const response = await fetch(apiUrl, {
      method: 'PUT', // PUTメソッドを使用して更新
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${userToken}`,
      },
      body: JSON.stringify({
        username: editedUser.username,
        profile: editedUser.profile,
        // 他のフィールドも必要に応じて追加
      }),
    });

    if (response.ok) {
      // 更新が成功した場合の処理
      console.log('User profile updated successfully');
      // オプションとして、必要に応じてUIを更新するなどの処理を追加できます
    } else {
      // 更新が失敗した場合の処理
      console.error('Failed to update user profile');
      alert("something going wrong");
    }
  } catch (error) {
    console.error('An error occurred while updating user profile', error);
  }

  onClose();
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
      sub: '',
      created_at: '',
      allowed_name_changes : '',   
      penalty_points : ''
      // 他のフィールドも同様に初期値に戻す
    });
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
        <Alert severity="error">カルマの値が低いので名前は囚人番号が表示されます。ユーザは設定できません。</Alert>
        <div>（上限３多分9日で１回増える）</div>
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
            label="Trip"
            name="trip"
            value={editedUser.trip}
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
            rows={3}
            margin="normal"
          />

<Alert  severity="error">
  <div><strong> User status </strong></div>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <div style={{ textAlign: 'right' }}>囚人番号 5963</div>
  </div>
</Alert>
<div style={{ marginTop: '10px' }}></div> {/* スペースを追加 */}

<Alert variant="outlined" severity="info">
  <div><strong> User status </strong></div>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <div style={{ textAlign: 'left' }}> karma</div>
    <div style={{ textAlign: 'right' }}>-99999999999</div>
  </div>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <div style={{ textAlign: 'left' }}> life</div>
    <div style={{ textAlign: 'right' }}>{editedUser.life}</div>
  </div>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <div style={{ textAlign: 'left' }}> created_at</div>
    <div style={{ textAlign: 'right' }}>{editedUser.created_at}</div>
  </div>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <div style={{ textAlign: 'left' }}> penalty_points</div>
    <div style={{ textAlign: 'right' }}>{editedUser.penalty_points}</div>
  </div>
  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
    <div style={{ textAlign: 'left' }}> sub</div>
    <div style={{ textAlign: 'right' }}>{editedUser.sub}</div>
  </div>
</Alert>

<div style={{ marginTop: '20px' }}> {/* スペースを追加 */}
  <Button variant="contained" color="primary" onClick={handleSave}>
    Save
  </Button>
          <Button variant="outlined" color="secondary" onClick={handleClose}>
            Cancel
          </Button>
</div>

        </form>
      </Box>
    </Modal>
  );
};

export default UserProfileModal;
