#!/bin/bash
sudo apt update
sudo apt install -y apache2 python3 python3-pip libapache2-mod-wsgi-py3
sudo pip3 install virtualenv
cd my-app
virtualenv venv
source venv/bin/activate
sudo pip3 install -r requirements.txt

mydir=${PWD##*/}

cat > myapp.wsgi << EOF
import sys 
sys.path.insert(0, '/var/www/html/$mydir')
from app import app as application
EOF

sudo ln -sT /home/ubuntu/$mydir /var/www/html/$mydir

cat > /etc/apache2/sites-enabled/000-default.conf << EOF
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        WSGIDaemonProcess app threads=5
        WSGIScriptAlias / /var/www/html/$mydir/myapp.wsgi
        WSGIApplicationGroup %{GLOBAL}
        <Directory $mydir>
             WSGIProcessGroup app
             WSGIApplicationGroup %{GLOBAL}
             Order deny,allow
             Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

sudo service apache2 restart

