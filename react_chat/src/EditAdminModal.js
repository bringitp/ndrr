import React, { useState, useEffect } from 'react';
import { useLocation, useParams } from "react-router-dom";
import {
  Modal,
  Box,
  Typography,
  Button,
  TableContainer,
  Paper,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Avatar,
} from '@mui/material';

function EditAdminModal({ isOpen, onClose, token }) {
  const { roomId } = useParams(); // URLパラメータからroomIdを取得
  const [selectedUser, setSelectedUser] = useState(null);
  const [roomMembers, setRoomMembers] = useState([]);

  const headers = new Headers({
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  });

  useEffect(() => {
    if (isOpen) {
    const apiUrl = window.location.href.startsWith(
      "https://ron-the-rocker.net/"
    )
      ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/condition`
      : `http://localhost:7777/room/${roomId}/condition`;

    fetch(apiUrl, { headers: { Authorization: `Bearer ${token}` } })
      .then(response => response.json())
      .then(data => {
        // チェックボックスの初期状態を設定
        const membersWithCheckbox = data.room_member.map(member => ({
          ...member,
          checked: member.blocked, // blockedフラグがtrueの場合、チェックをつける
        }));
        setRoomMembers(membersWithCheckbox);
      })
      .catch(error => console.error('ルームメンバーの取得中にエラーが発生しました:', error));
    }
  }, [roomId, isOpen,token]); // roomIdまたはtokenが変更されたときだけ実行されます


const handleRemoveFromRoom = (user) => {
  // ユーザーを部屋から追い出すAPI呼び出しを行います。
  if (user) {
    const apiUrl = window.location.href.startsWith(
      "https://ron-the-rocker.net/"
    )
      ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/remove_member`
      : `http://localhost:7777/room/${roomId}/remove_member`;
    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
    const data = {
      'member_id': user.user_id, // ユーザーのIDを指定します
    };

    fetch(apiUrl, {
      method: 'PUT',
      headers: headers,
      body: JSON.stringify(data),
    })
      .then(response => {
        if (response.ok) {
          console.log(`Successfully removed user ${user.username} from the room.`);
          // TODO: リストからユーザーを削除するなどの処理を追加する
        } else {
          console.error(`Failed to remove user ${user.username} from the room.`);
        }
      })
      .catch(error => {
        console.error('Error while removing user from the room:', error);
      });
  }
  setSelectedUser(null);
  onClose();
};

  const handleUserClick = (user) => {
    setSelectedUser(user);
  };

  const handleTransferAdmin = (user) => {
    // 選択されたユーザーを新しい管理者に設定するAPI呼び出しを行うことができます。
    if (user) {
      // TODO: API呼び出しを実装する
      console.log(`Transfer admin to user: ${user.username}`);
    }
    setSelectedUser(null);
    onClose();
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
          Edit Admin and Manage Members
        </Typography>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Avatar</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {roomMembers.map((user) => (
                <TableRow
                  key={user.id}
                  onClick={() => handleUserClick(user)}
                  selected={selectedUser && selectedUser.id === user.id}
                >
                  <TableCell>
                    {user.avatar_url && (
                      <Avatar
                        alt={user.username}
                        src={
                          process.env.NODE_ENV === 'development'
                            ? `http://localhost:7777/static/img/${user.avatar_url}`
                            : `https://ron-the-rocker.net/ndrr/api/static/img/${user.avatar_url}`
                        }
                      />
                    )}
                  </TableCell>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>
                    <Button
                      variant="outlined"
                      color="primary"
                      onClick={() => handleTransferAdmin(user)}
                    >
                      Transfer Admin
                    </Button>
                    <Button
                      variant="outlined"
                      color="secondary"
                      onClick={() => handleRemoveFromRoom(user)}
                    >
                      Remove from Room
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Button onClick={onClose} variant="contained">
          Cancel
        </Button>
      </Box>
    </Modal>
  );
}

export default EditAdminModal;
