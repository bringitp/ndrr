import React, { useState } from 'react';
import { Drawer, List, ListItem, ListItemText, Divider, Button } from '@mui/material';
import IconsGallery from './IconsGallery';
import UserProfileModal from './UserProfileModal';
import { useKeycloak } from '@react-keycloak/web'; // useKeycloak フックをインポート

const NaviBar = () => {
  const dummyData = ['🏠', '⚙', '🔌'];
  const [isIconsGalleryModalOpen, setIconsGalleryModalOpen] = useState(false);
  const [isIconsUserProfileModalOpen, setIconsUserProfileModalOpen] = useState(false);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックを使用

  const handleUserProfileModalOpenModal = () => {
    setIconsUserProfileModalOpen(true);
  };

  const handleUserProfileModalCloseModal = () => {
    setIconsUserProfileModalOpen(false);
  };

  const handleIconGalleryOpenModal = () => {
    setIconsGalleryModalOpen(true);
  };

  const handleIconGalleryCloseModal = () => {
    setIconsGalleryModalOpen(false);
  };

const handleLogout = () => {
    keycloak.logout(); // Keycloakからログアウト
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

        
          {initialized && keycloak.authenticated ? ( // Keycloak が初期化されており、ユーザーが認証済みかどうかをチェック



            dummyData.map((item, index) => (
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
                  if (item === '🔌') {
                     handleLogout(); // 🔌をクリックしたらログアウト
                  }
                }}
              >
                <ListItemText primary={item} />
              </ListItem>
            ))
          ) : (
<Button
  onClick={() => keycloak.login()}
  style={{ width: '15px', fontSize: '10px' }} // フォントサイズを大きくするスタイルを設定
>
⚡ログイン
</Button>
          )}
        </List>
        <Divider />
      </Drawer>
    </div>
  );
};

export default NaviBar;
