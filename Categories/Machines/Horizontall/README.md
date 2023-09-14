# Horizontall
> Write-up author: jon-brandy
## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.105 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-14 04:24 PDT
Nmap scan report for 10.10.11.105
Host is up (0.031s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ee774143d482bd3e6e6e50cdff6b0dd5 (RSA)
|   256 3ad589d5da9559d9df016837cad510b0 (ECDSA)
|_  256 4a0004b49d29e7af37161b4f802d9894 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-title: Did not follow redirect to http://horizontall.htb
|_http-server-header: nginx/1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 29.63 seconds
```

1. Based from the nmap results, the machine runs a web application and opens a ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/92d91808-156d-4127-89ee-42ab039f7154)


2. After clicking and checking every feature available there, none of the button redirecting us to a homepage.
3. Then I ran dirbuster.

