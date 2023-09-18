# Mirai
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7f6ce7fc-c2e5-4f81-ba24-a4de384b6a40)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.48 --min-rate 1000 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-17 22:58 PDT
Warning: 10.10.10.48 giving up on port because retransmission cap hit (10).
Nmap scan report for 10.10.10.48
Host is up (0.18s latency).
Not shown: 65136 closed tcp ports (conn-refused), 393 filtered tcp ports (no-response)
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u3 (protocol 2.0)
| ssh-hostkey: 
|   1024 aaef5ce08e86978247ff4ae5401890c5 (DSA)
|   2048 e8c19dc543abfe61233bd7e4af9b7418 (RSA)
|   256 b6a07838d0c810948b44b2eaa017422b (ECDSA)
|_  256 4d6840f720c4e552807a4438b8a2a752 (ED25519)
53/tcp    open  domain  dnsmasq 2.76
| dns-nsid: 
|_  bind.version: dnsmasq-2.76
80/tcp    open  http    lighttpd 1.4.35
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: lighttpd/1.4.35
1982/tcp  open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
32400/tcp open  http    Plex Media Server httpd
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Server returned status 401 but no WWW-Authenticate header.
|_http-title: Unauthorized
|_http-favicon: Plex
|_http-cors: HEAD GET POST PUT DELETE OPTIONS
32469/tcp open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.83 seconds
```

1. Based from the nmap result, the machine runs a web application.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bb26fee6-88bc-495e-93c9-2b61cf28bd41)


2. After ran dirbuster, there's a directory named "admin".

> Opens /admin

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9640f3ec-bff8-4843-8bba-a7331ed24262)


3. Interesting, based from the results we can conclude that the remote server is running a Raspberry PI machine.
4. Again here, we're making an interpretation where the admin **could** be using default creds.
5. Checking the internet for Raspberry PI default creds, shall resulting to --> `pi:raspberry`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8248eac6-5354-4370-a879-b37332f651aa)


6. Let's try run ssh to the remote server.

> We're logged in!!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/52979401-d760-48ea-a6de-7bc450600b8c)


> GETTING USER FLAG -> it's in the user home dir, then go to /desktop.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6c8f8433-f08c-4728-b2f1-5761f91fa238)


## USER FLAG

```
ff837707441b257a20e32199d7c8838d
```
