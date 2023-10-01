# CozyHosting
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fa4c16d1-f3fe-47c6-810f-466d37c566a6)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.230 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-30 22:59 PDT
Nmap scan report for 10.10.11.230
Host is up (0.032s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4356bca7f2ec46ddc10f83304c2caaa8 (ECDSA)
|_  256 6f7a6c3fa68de27595d47b71ac4f7e42 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://cozyhosting.htb
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.72 seconds
```

1. Based from the nmap results, the machine runs a webapp and opens ssh logins.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd9b7161-dbf0-4b00-b073-ef80301da3e2)
