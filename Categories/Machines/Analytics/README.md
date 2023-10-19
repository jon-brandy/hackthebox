# Analytics
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b992274b-eee2-4815-9962-5968bd5498c8)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.233 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-18 20:52 PDT
Nmap scan report for 10.10.11.233
Host is up (0.084s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3eea454bc5d16d6fe2d4d13b0a3da94f (ECDSA)
|_  256 64cc75de4ae6a5b473eb3f1bcfb4e394 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://analytical.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 85.17 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh logins.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3136aba1-1488-4e1e-ba6c-88b81c97df63)


2. 
