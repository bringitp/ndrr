#!/bin/bash

# Node.jsサーバーを起動
node <<EOF &
const http = require('http');
const fs = require('fs');

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/submit') {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
    });

    req.on('end', () => {
      console.log('受信データ:', data);
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end('データを受け取りました');
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

const port = 3000;
server.listen(port, () => {
  console.log(\`サーバーがポート\${port}で起動しました\`);
});
EOF

# ブラウザでHTMLフォームを表示
xdg-open index.html
