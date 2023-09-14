import React, { useState ,useEffect} from 'react';
import { Drawer, List, ListItem, ListItemText, Divider, Button } from '@mui/material';
import IconsGallery from './IconsGallery';
import UserProfileModal from './UserProfileModal';
import { useKeycloak } from '@react-keycloak/web'; // useKeycloak フックをインポート

const NaviBar = () => {
  const dummyData = ['🏠', '⚙', '🔌'];
  const [isIconsGalleryModalOpen, setIconsGalleryModalOpen] = useState(false);
  const [isIconsUserProfileModalOpen, setIconsUserProfileModalOpen] = useState(false);
  const { keycloak, initialized } = useKeycloak(); // useKeycloak フックを使用
  const [userToken, setUserToken] = useState(null); // トークンをstateとして管理




  const handleUserProfileModalOpenModal = () => {
    // Keycloakから取得したトークンを渡す
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
        <UserProfileModal 
         onClose={handleUserProfileModalCloseModal} 
         userToken={userToken} // トークンをUserProfileModalに渡す
         />
      )}

          {initialized && keycloak.authenticated ? ( // Keycloak が初期化されており、ユーザーが認証済みかどうかをチェック
            dummyData.map((item, index) => (
              <ListItem
                button
                key={index}
                onClick={() => {
                  if (item === '🏠') {
                    handleUserProfileModalOpenModal();
                    setUserToken(keycloak.token);
                  }
                  if (item === '⚙') {
                    handleIconGalleryOpenModal();
                    setUserToken(keycloak.token);
                  }
                  if (item === '🔌') {
                    handleLogout(); // 🔌をクリックしたらログアウト
                    setUserToken(null);
                  }
                }}
              >
                <ListItemText primary={item} />
              </ListItem>
            ))
          ) : (
<Button
  onClick={() => keycloak.login()}
  style={{
    width: '15px',
    fontFamily: '"Material Symbols Outlined", sans-serif', // Google Fontsで追加したフォントファミリー
    fontSize: '10px'
  }}
>
<span class="material-symbols-outlined">
login
</span>
</Button>
          )}
        </List>
        <Divider />
      </Drawer>
    </div>
  );
};

export default NaviBar;
