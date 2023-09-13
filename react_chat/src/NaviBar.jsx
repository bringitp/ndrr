// src/NaviBar.js

import React, { useState, useEffect, useRef } from 'react';
import { Drawer, List, ListItem, ListItemText, Divider } from '@mui/material';
import IconsGallery from './IconsGallery';


const NaviBar = () => {
  const dummyData = ['🏠', '⚙', '🔌']; // ダミーデータ
  const [isModalOpen, setIsModalOpen] = useState(false);


  // ボタンがクリックされたときにモーダルを開く関数
  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  // モーダルが閉じられたときに呼び出される関数
  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  return (
    <div>
      <Drawer variant="permanent" anchor="left">
   

        <List>
      {/* モーダルをアイコンがクリックされたときに表示 */}
      {isModalOpen && (
        <IconsGallery onClose={handleCloseModal} />
      )}
          {dummyData.map((item, index) => (
            <ListItem
              button
              key={index}
              onClick={() => {
                if (item === '⚙') {
                  handleOpenModal();
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
