# BoardLight
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/94b13718-713e-4ced-9845-07002d1f95ff)


## Lessons Learned:
- sdasda

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC boardlight.htb --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2024-05-26 09:12 PDT
Nmap scan report for boardlight.htb (10.10.11.11)
Host is up (0.016s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 062d3b851059ff7366277f0eae03eaf4 (RSA)
|   256 5903dc52873a359934447433783135fb (ECDSA)
|_  256 ab1338e43ee024b46938a9638238ddf4 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 85.17 seconds
```

1. 
