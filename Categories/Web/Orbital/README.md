# Orbital
> Write-up author: vreshco
## DESCRIPTION:
In order to decipher the alien communication that held the key to their location, 
she needed access to a decoder with advanced capabilities - a decoder that only The Orbital firm possessed. Can you get your hands on the decoder?
## HINT:
- NONE
## STEPS:
1. In this challenge we're given the source code.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/4d3de66e-cfc1-474d-b4a0-4ec8c81d60bc)


2. Let's start by analyzing the Dockerfile.

> Dockerfile

```Dockerfile
FROM python:3.8-alpine

# Install packages
RUN apk add --no-cache --update mariadb mariadb-client supervisor gcc musl-dev mariadb-connector-c-dev

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install Flask flask_mysqldb pyjwt colorama

# Setup app
RUN mkdir -p /app
RUN mkdir -p /communication

# Switch working environment
WORKDIR /app

# Add application
COPY challenge .

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 1337

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# copy flag
COPY flag.txt /signal_sleuth_firmware
COPY files /communications/

# create database and start supervisord
COPY --chown=root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

3. Notice the "copy flag" seems to be our interest here, it seems the flag stored in /signal_sleuth_firmware directory.
4. Next i checked the other files and found another interesting part inside **entrypoint.sh** file.

```sh
#!/bin/ash

# Secure entrypoint
# Initialize & Start MariaDB
mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld
mysql_install_db --user=mysql --ldata=/var/lib/mysql
mysqld --user=mysql --console --skip-networking=0 &

# Wait for mysql to start
while ! mysqladmin ping -h'localhost' --silent; do echo 'not up' && sleep .2; done

function genPass() {
    echo -n 'ichliebedich' | md5sum | head -c 32
}

mysql -u root << EOF
CREATE DATABASE orbital;
CREATE TABLE orbital.users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);
CREATE TABLE orbital.communication (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    source varchar(255) NOT NULL,
    destination varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    downloadable varchar(255) NOT NULL
);
INSERT INTO orbital.users (username, password) VALUES ('admin', '$(genPass)');
INSERT INTO orbital.communication (source, destination, name, downloadable) VALUES ('Titan', 'Arcturus', 'Ice World Calling Red Giant', 'communication.mp3');
INSERT INTO orbital.communication (source, destination, name, downloadable) VALUES ('Andromeda', 'Vega', 'Spiral Arm Salutations', 'communication.mp3');
INSERT INTO orbital.communication (source, destination, name, downloadable) VALUES ('Proxima Centauri', 'Trappist-1', 'Lone Star Linkup', 'communication.mp3');
INSERT INTO orbital.communication (source, destination, name, downloadable) VALUES ('TRAPPIST-1h', 'Kepler-438b', 'Small World Symposium', 'communication.mp3');
INSERT INTO orbital.communication (source, destination, name, downloadable) VALUES ('Winky', 'Boop', 'Jelly World Japes', 'communication.mp3');
CREATE USER 'user'@'localhost' IDENTIFIED BY 'M@k3l@R!d3s$';
GRANT SELECT ON orbital.users TO 'user'@'localhost';
GRANT SELECT ON orbital.communication TO 'user'@'localhost';
FLUSH PRIVILEGES;
EOF

/usr/bin/supervisord -c /etc/supervisord.conf
```

5. The admin creds hardcoded, the strings stored as the password is from the genPass() call.
6. As we can see from the Dockerfile, the password must be -> `ichliebedich`.

![do](https://github.com/Bread-Yolk/hackthebox/assets/70703371/e9f45da0-62c5-4677-916b-bb8697cb8f99)


7. Let's open the web app.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/3c65982d-a8c2-4bb4-ad28-deca50c708f9)


8. Looks like the intended solution is **SQL Injection** to retrieve the admin password.
9. Anyway let's enter the creds.

> RESULT

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/38fae77d-f314-4210-9638-b40cd848601c)


10. Tried to click every nav options but does not redirect me to another page, the only thing work is the logout option.
11. Then i tried to click everything until i found the exported button is functional.
12. It pops us to download a mp3 music, which means it do some request, let's intercept the request and tamper it using burpsuite.

#### NOTES: The mp3 does not relevant to this challenge.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/a6fefa63-ff98-4162-afdd-b9139e55cdf1)


13. Send it to repeater.

![image](https://github.com/Bread-Yolk/hackthebox/assets/70703371/f9c59d1e-e420-47d8-b105-64d75d90ee2b)


15. 


