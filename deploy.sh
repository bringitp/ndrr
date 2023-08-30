#!/bin/bash

bash /root/ndrr/server_control.sh stop
rm -r /root/ndrr
git clone https://github.com/bringitp/ndrr.git
cp -r /root/ndrr/react_chat/build/* /var/www/ron-the-rocker.net
bash /root/ndrr/server_control.sh start debug
