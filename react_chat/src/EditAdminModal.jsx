import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
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

function MemberRow({ user, selectedUser, handleUserClick, handleTransferAdmin, handleRemoveFromRoom }) {
  return (
    <TableRow
      key={user.user_id}
      onClick={() => handleUserClick(user)}
      selected={selectedUser && selectedUser.user_id === user.user_id}
    >
      <TableCell>
        {user.avatar_url && (
          <Avatar
            alt={user.username}
            src={process.env.NODE_ENV === 'development'
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
  );
}

function EditAdminModal({ isOpen, onClose, token ,jsonData}) {
  const { roomId } = useParams();
  const [selectedUser, setSelectedUser] = useState(null);
  const [roomMembers, setRoomMembers] = useState([]);

  useEffect(() => {
    if (isOpen) {
      const membersWithCheckbox = jsonData.room_members.filter(member => !member.ami).map(member => ({
        ...member,
        checked: member.blocked,
      }));
      setRoomMembers(membersWithCheckbox);
    }
  }, [isOpen, jsonData]);

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
      const apiUrl = window.location.href.startsWith(
        "https://ron-the-rocker.net/"
      )
        ? `https://ron-the-rocker.net/ndrr/api/room/${roomId}/change_owner`
        : `http://localhost:7777/room/${roomId}/change_owner`;
      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      };
      const data = {
        'new_owner_id': user.user_id, // ユーザーのIDを指定します
      };

      fetch(apiUrl, {
        method: 'PUT',
        headers: headers,
        body: JSON.stringify(data),
      })
        .then(response => {
          if (response.ok) {
            console.log(`Transferred admin to user: ${user.username}`);
            // TODO: 成功時の処理を追加する
          } else {
            console.error(`Failed to transfer admin to user: ${user.username}`);
          }
        })
        .catch(error => {
          console.error('Error while transferring admin:', error);
        });
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
                  key={user.user_id} // ユーザーIDをキーとして使用
                  onClick={() => handleUserClick(user)}
                  selected={selectedUser && selectedUser.user_id === user.user_id} // ユーザーIDで選択を管理
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
