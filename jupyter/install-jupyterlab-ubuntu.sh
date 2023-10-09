#!/bin/bash
# Tim H 2023

# installing and configuring Jupyter Lab
# Ubuntu 20.04
# https://jupyter.int.butters.me:8443/lab

# https://jupyter.org/install
# https://www.digitalocean.com/community/tutorials/how-to-set-up-a-jupyterlab-environment-on-ubuntu-18-04


# set PATH so it includes user's private bin if it exists
# seems to be required:
echo 'PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile

# required:
python3 -m pip install --upgrade pip

# install it, doesn't matter if pip or pip3 on my golden image
python3 -m pip install --upgrade jupyterlab jupyter-server voila

# create config file:
jupyter-lab server --generate-config 
#? is this right, should server be removed?

# set a password:
jupyter-lab password


# manually launch it:
jupyter-lab

# https://towardsdatascience.com/how-to-connect-to-jupyterlab-remotely-9180b57c45bb

# generate HTTPS keypairs for communication

# source activate base
jupyter-lab --port=8000 --ip="*" --no-browser --autoreload --allow-root
# http://jupyter.int.butters.me:8000

# http://jupyter.int.butters.me:8000

pip install voila

# make it an autostarting service:
sudo mkdir -p /opt/jupyterlab/etc/systemd
sudo touch /opt/jupyterlab/etc/systemd/jupyterlab.service

[Unit]
Description=JupyterLab
After=syslog.target network.target
[Service]
User=thrawn
Environment="PATH=/home/thrawn/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
ExecStart=/home/thrawn/.local/bin/jupyter-lab 
#  --ip 0.0.0.0 --port 8443 --no-browser --autoreload --certfile=/home/thrawn/nfs_synology_jupyter/ssl_certs/jupyter_ssl_public.cert --keyfile=/home/thrawn/nfs_synology_jupyter/ssl_certs/jupyter_ssl_private.key
# --allow-root
[Install]
WantedBy=multi-user.target

sudo vim ^^


sudo ln -s /opt/jupyterlab/etc/systemd/jupyterlab.service /etc/systemd/system/jupyterlab.service
sudo systemctl daemon-reload
sudo systemctl enable jupyterlab.service
sudo systemctl restart  jupyterlab.service
sudo systemctl status jupyterlab.service

# http://jupyter.int.butters.me:8000/login


# change what directory it starts in, use an NFS mount or something so backups
# happen

#mkdir ~/nfs_synology_jupyter


NFS_MOUNT_NAME="nfs_synology_jupyter"
NFS_SERVER_IP="10.0.1.35"
NFS_MOUNT_PATH="/nfs_synology_jupyter"

showmount -e "$NFS_SERVER_IP" | grep -q "$NFS_MOUNT_NAME"

sudo mkdir -p "$NFS_MOUNT_PATH"
sudo chown $(id --user) "$NFS_MOUNT_PATH"
cd "$NFS_MOUNT_PATH" || exit 1
sudo chmod +x "$NFS_MOUNT_PATH"

echo "$NFS_SERVER_IP:/volume1/$NFS_MOUNT_NAME $NFS_MOUNT_PATH      nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0" | sudo tee --append /etc/fstab

sudo mount --fake
sudo mount "$NFS_MOUNT_PATH"

# verify it mounted
mount | grep "$NFS_MOUNT_PATH" &&  ls -lah "$NFS_MOUNT_PATH"

# create symbolic link to specific path
ln -s "$NFS_MOUNT_PATH" "$HOME/nfs_synology_jupyter"
cd "$HOME/nfs_synology_jupyter" || exit 4
date > nfs_write_test.txt

# create directory for SSL certs
mkdir -p "$HOME/nfs_synology_jupyter/ssl_certs"
cd "$HOME/nfs_synology_jupyter/ssl_certs"

# create the keypair
openssl req  -nodes -new -x509 -keyout jupyter_ssl_private.key -out jupyter_ssl_public.cert

# make the files read only
chmod -w jupyter_ssl_public.cert jupyter_ssl_private.key

# move over the config files
cp -r ~/.jupyter/ ~/nfs_synology_jupyter/
rm -Rf ~/.jupyter
ln -s /home/thrawn/nfs_synology_jupyter/.jupyter /home/thrawn/.jupyter

# /home/thrawn/.jupyter/jupyter_server_config.py
c.ServerApp.keyfile =  '/home/thrawn/nfs_synology_jupyter/ssl_certs/jupyter_ssl_private.key'
c.ServerApp.certfile = '/home/thrawn/nfs_synology_jupyter/ssl_certs/jupyter_ssl_public.cert'
c.ServerApp.allow_remote_access = True
c.ServerApp.ip = '*'
c.ServerApp.port = 8443
c.ServerApp.preferred_dir = '/home/thrawn/nfs_synology_jupyter'

# c.ServerApp.allow_root = True
# NotebookApp.max_buffer_size = your desired value

sudo systemctl restart  jupyterlab.service


# https://jupyter.int.butters.me:8443/login


# next up, RAM settings, CPU stuff?


# me guessing
pip install tensorflow
pip install pandas
pip install matplotlib
pip install sklearn
pip install joblib


python -m pip install sklearn
cd

git clone https://github.com/sa-mw-dach/manuela-dev

import sys
!{sys.executable} -m pip install -U sklearn

/usr/bin/python3.8
