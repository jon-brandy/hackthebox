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
4. 


