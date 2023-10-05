#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'
sudo mkdir -p /data/web_static/releases/test/
sudo sh -c 'echo "simple content, to test your Nginx configuration" > /data/web_static/releases/test/index.html'
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '/server_name _;/ a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-enabled/default
sudo service nginx restart
