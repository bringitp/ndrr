// src/NaviBar.js

import React, { useState, useEffect, useRef } from 'react';
import { Drawer, List, ListItem, ListItemText, Divider } from '@mui/material';

const NaviBar = () => {
  const dummyData = ['🏠', '⚙', '🔌']; // ダミーデータ
   const navBarRef = useRef(null);

  return (
    <div ref={navBarRef}>
    <Drawer variant="permanent" anchor="left">
      <List>
        {dummyData.map((item, index) => (
          <ListItem button key={index}>
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
