# Keeper
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2ee9d4d2-b21e-4238-88c9-b487c0a65923)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.227 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 06:14 PDT
Nmap scan report for keeper.htb (10.10.11.227)
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3539d439404b1f6186dd7c37bb4b989e (ECDSA)
|_  256 1ae972be8bb105d5effedd80d8efc066 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.01 seconds
```

1. Based from the nmap results, we know that the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e8f6e209-5fbb-4a76-bcfc-58913a0aa156)


2. To open the subdomain --> tickets.keeper.htb, we need to add that hostname to /etc/passwd first.

> tickets.keeper.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/faa6354d-d019-40a9-a75e-d99b94e4977c)


3. Noticing there's no register option, I searched on the internet for request tracker default cred.

> RESULT --> root:password

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cc541995-9be8-47f0-b8c6-1f7d49061711)


4. 



