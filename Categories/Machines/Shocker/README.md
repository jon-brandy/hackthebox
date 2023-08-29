# Shocker
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6a3d07d8-d7ff-47dc-bc67-8d520eff6f0d)


## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.56 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-29 06:17 PDT
Nmap scan report for shocker.htb (10.10.10.56)
Host is up (0.034s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4f8ade8f80477decf150d630a187e49 (RSA)
|   256 228fb197bf0f1708fc7e2c8fe9773a48 (ECDSA)
|_  256 e6ac27a3b5a9f1123c34a55d5beb3de9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 56.02 seconds
```

1. Based from the nmap result, we know the machine runs a web application and ssh service.
2. Since there's no interesting info currently, i ran dirbuster and found a directory named `cgi-bin`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/98b50867-ce6d-4244-8830-f178eda7757d)


3. Which is interesing, it's forbidden. Judging from the challenge title and the directory we found.
4. This challenge could be related to `shellshock exploit` --> `Apache mod CGI`.
5. This should be the one --> `https://www.exploit-db.com/exploits/34766` (since there's .sh files).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/969a041f-98d0-4122-9947-bf198467955e)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/304bbb31-bc3f-474b-aeda-5a7407448e56)


6. Let's use 1.



