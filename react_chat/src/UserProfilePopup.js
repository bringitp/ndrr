import React from "react";
import Popover from "@mui/material/Popover";
import Typography from "@mui/material/Typography";

function UserProfilePopup({ user, onClose, anchorEl }) {

  const open = Boolean(user);

  const popoverStyle = {
    background: "rgba(255, 255, 255, 0.9)", // 半透明な白
    borderRadius: "8px",
    padding: "20px",
    boxShadow: "0px 2px 6px rgba(0, 0, 0, 0.1)", // 薄い影
    width: "300px", // ポップアップの幅
    textAlign: "center", // コンテンツを中央に配置
  };

  return (
    <Popover
      open={open}
      onClose={onClose}
      anchorEl={anchorEl} // アンカー要素を指定
      anchorOrigin={{
        vertical: "bottom",
        horizontal: "center",
      }}
      transformOrigin={{
        vertical: "top",
        horizontal: "center",
      }}
    >
      <div style={popoverStyle}>
        <Typography variant="h6">{user?.username} ({user?.trip})</Typography>
        <Typography variant="h6">{user?.profile}</Typography>

        {/* Add more user information as needed */}
      </div>
    </Popover>
  );
}

export default UserProfilePopup;
