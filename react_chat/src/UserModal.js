import React, { useState, useEffect } from 'react';
import { useLocation, useParams } from "react-router-dom";
import {
  Box,
  Typography,
  Modal,
  TableContainer,
  Paper,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Button,
} from '@mui/material';

function UserModal({ isUserModalOpen, handleModalClose, token ,jsonData}) {
  const [roomMembers, setRoomMembers] = useState([]);
  
  const headers = new Headers({
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  });

  // addToBlockList 関数を定義
  const addToBlockList = (userId) => {
    const apiUrl = window.location.href.startsWith(
      "https://ron-the-rocker.net/"
    )
      ? `https://ron-the-rocker.net/ndrr/api/users/ng-list`
      : `http://localhost:7777/users/ng-list`;

    const data = {
      "blocked_user_id": userId,
    };
    fetch(apiUrl, {
      method: 'POST', // または 'DELETE'
      headers: headers,
      body: JSON.stringify(data),
    })
      .then(response => {
        if (response.ok) {
          // 成功した場合の処理
          console.log(`User ${userId} has been blocked/unblocked.`);
        } else {
          // エラーレスポンスをハンドル
          if (response.status === 401) {
            // 認証エラーの場合の処理
            console.error('認証エラーが発生しました。');
          } else if (response.status === 500) {
            // サーバーエラーの場合の処理
            console.error('ユーザブロック中にサーバーエラーが発生しました。');
          } else {
            // その他のエラーの場合の処理
            console.error('ユーザブロックのAPIエラーが発生しました。');
          }
        }
      })
      .catch(error => {
        // ネットワークエラーなど、fetch自体のエラーをハンドル
        console.error('APIリクエスト中にエラーが発生しました:', error);
      });
  };

  // removeFromBlockList 関数を定義
  const removeFromBlockList = (userId) => {
    const apiUrl = window.location.href.startsWith(
      "https://ron-the-rocker.net/"
    )
      ? `https://ron-the-rocker.net/ndrr/api/users/ng-list`
      : `http://localhost:7777/users/ng-list`;

    const data = {
      "blocked_user_id": userId,
    };

    fetch(apiUrl, {
      method: 'DELETE',
      headers: headers,
      body: JSON.stringify(data),
    })
      .then(response => {
        if (response.ok) {
          // 削除が成功した場合の処理
          console.log(`User ${userId} has been unblocked.`);
        } else {

          if (response.status === 401) {
            // 認証エラーの場合の処理
            console.error('認証エラーが発生しました。');
          } else if (response.status === 500) {
          // エラーハンドリング
          console.error('ブロック解除中にエラーが発生しました。');
        }
      }
      })
      .catch(error => {
        console.error('ブロック解除中にエラーが発生しました:', error);
      });
  };

  useEffect(() => {
    // isUserModalOpenがtrueのときにのみ実行
    if (isUserModalOpen) {
      // jsonDataからroom_membersデータを取得して設定 ただし自分のIDは表示しない
      const membersWithCheckbox = jsonData.room_members.filter(member => !member.ami).map(member => ({
        ...member,
        checked: member.blocked, // blockedフラグがtrueの場合、チェックをつける
      }));
      setRoomMembers(membersWithCheckbox);
    }
  }, [isUserModalOpen, jsonData]);


  return (
    <Modal open={isUserModalOpen} onClose={handleModalClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '90%', // Set width to 95% of the screen size
          bgcolor: 'background.paper',
          boxShadow: 24,
          p: 4,
          maxHeight: '80vh', // Set maximum height of the modal content
          overflowY: 'auto', // Enable vertical scrolling if content overflows
        }}
      >
        <Typography variant="h6" component="h2" gutterBottom>
          User Menu
        </Typography>
        {/* Display the room member data in a table */}
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Avatar</TableCell>
                <TableCell>Username</TableCell>
                <TableCell>Ignore</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {roomMembers.map((member) => (
                <TableRow key={member.user_id}>
                  <TableCell>
                    {member.avatar_url && (
                      <div
                        style={{
                          position: 'relative',
                          display: 'inline-block',
                          width: 50,
                          height: 50,
                        }}
                      >
                        <img
                          src={
                            process.env.NODE_ENV === 'development'
                              ? `http://localhost:7777/static/img/${member.avatar_url}`
                              : `https://ron-the-rocker.net/ndrr/api/static/img/${member.avatar_url}`
                          }
                          alt={`Avatar of ${member.username}`}
                          width="50"
                          height="50"
                          style={{ borderRadius: '15%' }}
                        />
                        {/* Cross symbol */}
                        {member.checked && (
                          <div
                            style={{
                              position: 'absolute',
                              top: 0,
                              left: 0,
                              width: '100%',
                              height: '100%',
                              display: 'flex',
                              justifyContent: 'center',
                              alignItems: 'center',
                              fontSize: '4em', // Increase font size for a larger cross
                              color: 'red',
                            }}
                          >
                            &#10060; {/* Unicode for the cross symbol */}
                          </div>
                        )}
                      </div>
                    )}
                  </TableCell>
                  <TableCell>{member.username}</TableCell>
                  <TableCell>
                    <input
                      type="checkbox"
                      checked={member.checked}
                      onChange={() => {
                        // チェックボックスの状態をトグル
                        const updatedMembers = roomMembers.map((m) => {
                          if (m.user_id === member.user_id) {
                            return { ...m, checked: !m.checked };
                          }
                          return m;
                        });
                        setRoomMembers(updatedMembers);

                        if (member.checked) {
                          // チェックを外した場合にブロックリスト解除
                          removeFromBlockList(member.user_id);
                        } else {
                          // チェックを付けた場合にブロックリストに追加
                          addToBlockList(member.user_id);
                        }
                      }}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <Button onClick={handleModalClose}>Close</Button>
      </Box>
    </Modal>
  );
}

export default UserModal;