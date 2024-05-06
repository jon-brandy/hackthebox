# Stocker
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cd24459d-4e7c-4550-9217-ff3ef8c9f02e)


## Lessons Learned:
- sdasda

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC stocker.htb --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2024-05-06 01:43 PDT
Nmap scan report for stocker.htb (10.10.11.196)
Host is up (0.020s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 3d12971d86bc161683608f4f06e6d54e (RSA)
|   256 7c4d1a7868ce1200df491037f9ad174f (ECDSA)
|_  256 dd978050a5bacd7d55e827ed28fdaa3b (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-generator: Eleventy v2.0.0
|_http-title: Stock - Coming Soon!
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.52 seconds
```

1. Based from the nmap results, the machine runs a web application on port 80 and it opens ssh logins on port 22.

> WEB APP

