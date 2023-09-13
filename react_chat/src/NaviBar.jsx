// src/NaviBar.js

import React, { useState, useEffect, useRef } from 'react';
import { Drawer, List, ListItem, ListItemText, Divider } from '@mui/material';
import IconsGallery from './IconsGallery';
import UserProfileModal from './UserProfileModal';

const NaviBar = () => {
  const dummyData = ['🏠', '⚙', '🔌']; // ダミーデータ
  const [isIconsGalleryModalOpen, setIconsGalleryModalOpen] = useState(false);
  const [isIconsUserProfileModalOpen, setIconsUserProfileModalOpen] = useState(false);

  // ボタンがクリックされたときにモーダルを開く関数
  const handleUserProfileModalOpenModal = () => {
    setIconsUserProfileModalOpen(true);
  };

  // モーダルが閉じられたときに呼び出される関数
  const handleUserProfileModalCloseModal = () => {
    setIconsUserProfileModalOpen(false);
  };

  // ボタンがクリックされたときにモーダルを開く関数
  const handleIconGalleryOpenModal = () => {
    setIconsGalleryModalOpen(true);
  };

  // モーダルが閉じられたときに呼び出される関数
  const handleIconGalleryCloseModal = () => {
    setIconsGalleryModalOpen(false);
  };

  return (
    <div>
      <Drawer variant="permanent" anchor="left">
   
        <List>
      {/* モーダルをアイコンがクリックされたときに表示 */}
      {isIconsGalleryModalOpen && (
        <IconsGallery onClose={handleIconGalleryCloseModal} />
      )}

      {isIconsUserProfileModalOpen && (
        <UserProfileModal onClose={handleUserProfileModalCloseModal} />
      )}

          {dummyData.map((item, index) => (
            <ListItem
              button
              key={index}
              onClick={() => {
                if (item === '🏠') {
                  handleUserProfileModalOpenModal();
                }
                if (item === '⚙') {
                  handleIconGalleryOpenModal();
                }
              }}
            >
              <ListItemText primary={item} />
            </ListItem>
          ))}
        </List>
        <Divider />
      </Drawer>


    </div>
  );
};

export default NaviBar;
