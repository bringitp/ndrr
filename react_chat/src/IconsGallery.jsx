import React, { useState, useEffect } from 'react';
import { Modal, Box, Grid, Paper, Typography } from '@mui/material';

const IconsGallery = ({ onClose }) => {
  const [icons, setIcons] = useState({});
  const [openModal, setOpenModal] = useState(true);
  const [selectedIcon, setSelectedIcon] = useState(true);

  useEffect(() => {
    const fetchIcons = async () => {
      try {
             const apiUrl = window.location.href.startsWith(
               "https://ron-the-rocker.net/"
             )
            ? `https://ron-the-rocker.net/ndrr/api/system/icons`
            : `http://localhost:7777/system/icons`;

        const response = await fetch(apiUrl);
        const data = await response.json();
        setIcons(data);
      } catch (error) {
        console.error('Error fetching icons:', error);
      }
    };

    fetchIcons();
  }, []);

  const handleIconGalleryCloseModal = () => {
    if (onClose) {
      onClose(); // モーダルを閉じる関数を呼び出す
    }
  };

  // アイコンをクリックしたときの処理
  const handleIconClick = (iconId) => {
    // アイコンのIDを表示する
    alert(`Icon ID: ${iconId}`);
  };

  return (
    <div>
      {/* モーダルの内容 */}
      <Modal open={true} onClose={handleIconGalleryCloseModal}>
        <Box
          sx={{
            position: 'absolute',
            width: '300px', //aquos4 
            maxHeight: '65vh',
            overflowY: 'auto',
            bgcolor: 'background.paper',
            border: '2px solid #000',
            boxShadow: 24,
            p: 2,
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
          }}
        >
          <Grid container spacing={2}>
            {Object.keys(icons).map((iconId) => (
              <Grid item xs={3} key={iconId}>
                <Paper elevation={3} onClick={() => handleIconClick(iconId)}>
                  <img
                    src={
                      process.env.NODE_ENV === 'development'
                        ? `http://localhost:7777/static/img/${icons[iconId]}`
                        : `https://ron-the-rocker.net/ndrr/api/static/img/${icons[iconId]}`
                    }
                    alt="Selected Icon"
                    style={{ width: '100%', height: 'auto' }}
                  />
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Modal>
    </div>
  );
};

export default IconsGallery;
