import React from 'react';
import { Typography } from '@mui/material';

function ChatMessage({ message, isMyMessage }) {
  const messageStyle = isMyMessage ? styles.myMessage : styles.otherMessage;

  return (
    <div key={message.id} style={{ ...styles.messageContainer, ...messageStyle, marginBottom: '0px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', width: '100%' }}>
        <div>
          <Typography variant="subtitle1">{message.sender.username}</Typography>
          <Typography variant="body1">{message.content}</Typography>
        </div>
        <div>
          <Typography variant="caption">{formatDate(message.sent_at)}</Typography>
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;
