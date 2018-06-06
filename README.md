# udacity-linux-server-configuration

### Project Description

Take a baseline installation of a Linux distribution on a virtual machine and prepare it to host your web applications, to include installing updates, securing it from a number of attack vectors and installing/configuring web and database servers.

- IP address: 34.226.152.103

- Accessible SSH port: 2200

- Application URL: http://34.226.152.103.xip.io/

### Walkthrough

1. Create new user named grader and give it the permission to sudo
  - SSH into the server through `ssh -i ~/.ssh/LightsailDefaultPrivateKey-us-east-1.pem ubuntu@34.226.152.103`
  - Run `$ sudo adduser grader` to create a new user named grader
  - Create a new file in the sudoers directory with `sudo nano /etc/sudoers.d/grader`
  - Add the following text `grader ALL=(ALL:ALL) NOPASSWD:ALL`

    
2. Update all currently installed packages
  - Download package lists with `sudo apt-get update`
  - Fetch new versions of packages with `sudo apt-get upgrade`

3. Change SSH port from 22 to 2200
  - Run `sudo nano /etc/ssh/sshd_config`
  - Change the port from 22 to 2200
  - Confirm by running `ssh -i ~/.ssh/LightsailDefaultPrivateKey-us-east-1.pem -p 2200 ubuntu@34.226.152.103`

### ssh login using user 'grader'
1. Generate public and private keys using `ssh-keygen` and save the key as "authorized_keys"
2. Move the private key in ~/.ssh
3. On VM copy the public key to

```
$ su - grader
$ mkdir .ssh
$ sudo nano .ssh/authorized_keys
```

4. Copy public key to this file

5. Give following permissions
```
$ chmod 700 .ssh
$ chmod 644 .ssh/authorized_keys
```



________________________________________________________


4. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
  - `sudo ufw allow 2200/tcp`
  - `sudo ufw allow 80/tcp`
  - `sudo ufw allow 123/udp`
  - `sudo ufw enable`
  
5. Configure the local timezone to UTC
  - Run `sudo dpkg-reconfigure tzdata` and then choose UTC
 
6. Configure key-based authentication for grader user
  - Run this command `cp /ubuntu/.ssh/authorized_keys /home/grader/.ssh/authorized_keys`

7. Disable ssh login for root user [ubuntu]
  - Run `sudo nano /etc/ssh/sshd_config`
  - Change `PermitRootLogin without-password` line to `PermitRootLogin no`
  - Restart ssh with `sudo service ssh restart`
  - Now you are only able to login using `ssh -i ~/.ssh/LightsailDefaultPrivateKey-us-east-1.pem -p 2200 grader@34.226.152.103`
 
8. Install Apache
  - `sudo apt-get install apache2`

9. Install mod_wsgi
  - Run `sudo apt-get install libapache2-mod-wsgi python-dev`
  - Enable mod_wsgi with `sudo a2enmod wsgi`
  - Start the web server with `sudo service apache2 start`

  
10. Clone the Catalog app from Github
  - Install git using: `sudo apt-get install git`
  - `cd /var/www/ItemCatalog`
  - Clone your project from github `git clone https://github.com/hanyhesham/catalog.git`
  - Change owner of the newly created catalog folder `sudo chown -R grader:grader catalog`
  - Create a catalog.wsgi file, then add this inside:
  ```
  #!/usr/bin/python
  import sys
  import logging
  logging.basicConfig(stream=sys.stderr)
  sys.path.insert(0,"/var/www/ItemCatalog/")

  from catalog import app as application
  application.secret_key = 'Add your secret key'

  - Rename project.py to __init__.py `mv project.py __init__.py`
  
11. Install virtual environment
  - Install the virtual environment `sudo pip install virtualenv`
  - Create a new virtual environment with `sudo virtualenv venv`
  - Activate the virutal environment `source venv/bin/activate`
  - Change permissions `sudo chmod -R 777 venv`

12. Install Flask and other dependencies
  - Install pip with `sudo apt-get install python-pip`
  - Install Flask `pip install Flask`
  - Install other project dependencies `sudo pip install httplib2 oauth2client sqlalchemy psycopg2 sqlalchemy_utils request`

13. Update path of client_secrets.json file
  - `nano __init__.py`
  - Change client_secrets.json path to `/var/www/ItemCatalog/catalog/client_secrets.json`
  
14. Configure and enable a new virtual host
  - Run this: `sudo nano /etc/apache2/sites-available/catalog.conf`
  - Paste this code: 
  ```
  <VirtualHost *:80>
    ServerName 34.226.152.103.xip.io
    ServerAdmin syal.anuj@gmail.com
    WSGIDaemonProcess catalog python-path=/var/www/ItemCatalog/catalog:/var/www/ItemCatalog/catalog/venv/lib/python2.7/site-packages
    WSGIProcessGroup catalog
    WSGIScriptAlias / /var/www/ItemCatalog/catalog/catalog.wsgi
    <Directory /var/www/ItemCatalog/catalog/>
        Order allow,deny
        Allow from all
    </Directory>
    Alias /static /var/www/ItemCatalog/catalog/static
    <Directory /var/www/ItemCatalog/catalog/static/>
        Order allow,deny
        Allow from all
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
  ```
  - Enable the virtual host `sudo a2ensite catalog`

15. Install and configure PostgreSQL
  - `sudo apt-get install libpq-dev python-dev`
  - `sudo apt-get install postgresql postgresql-contrib`
  - `sudo su - postgres`
  - `psql`
  - `CREATE USER catalog WITH PASSWORD 'password';`
  - `ALTER USER catalog CREATEDB;`
  - `CREATE DATABASE catalog WITH OWNER catalog;`
  - `\c catalog`
  - `REVOKE ALL ON SCHEMA public FROM public;`
  - `GRANT ALL ON SCHEMA public TO catalog;`
  - `\q`
  - `exit`
  - Change create engine line in your `__init__.py` and `database_setup.py` and 'lotsofitems.py' to: 
  `engine = create_engine('postgresql://catalog:password@localhost/catalog')`
  - `python /var/www/catalog/catalog/database_setup.py`
  - Make sure no remote connections to the database are allowed. Check if the contents of this file `sudo nano /etc/postgresql/9.3/main/pg_hba.conf` looks like this:
  ```
  local   all             postgres                                peer
  local   all             all                                     peer
  host    all             all             127.0.0.1/32            md5
  host    all             all             ::1/128                 md5
  ```
  
16. Restart Apache 
  - `sudo service apache2 restart`
  
17. Visit site at http://34.226.152.103.xip.io/


Resources :
_____________

.Github
.OAuth
.Xip
.Postgresql
.flask

* After finish running project.py you can use your favorite browser to visit [this link](http://localhost:8000/)

### How to use
* You can browse through the website to find out the different categories of movies.
> [![Image](gif/catalog1.gif)](Image)
* You can also create you own items after you login.
> [![Image](gif/catalog2.gif)](Image)
* Only the users who created the item have the ability to post, edit, and delete it.
> [![Image](gif/catalog3.gif)](Image)
* Once you log out. You can lost your right to change it.
> [![Image](gif/catalog4.gif)](Image)
