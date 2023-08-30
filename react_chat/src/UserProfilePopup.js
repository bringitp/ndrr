// UserProfilePopup.js

import React from "react";
import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import Typography from "@mui/material/Typography";

function UserProfilePopup({ user, onClose }) {
  return (
    <Dialog open={Boolean(user)} onClose={onClose}>
      <DialogContent>
        <Typography variant="h6">{user.username}'s Profile</Typography>
        <Typography>{`Trip: ${user.trip}`}</Typography>
        <Typography>{`Karma: ${user.karma}`}</Typography>
        {/* Add more user information as needed */}
      </DialogContent>
    </Dialog>
  );
}

export default UserProfilePopup;
