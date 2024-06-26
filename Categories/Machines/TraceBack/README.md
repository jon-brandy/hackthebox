# TraceBack
> Write-up author: jon-brandy


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a5389983-7994-42b7-87d6-c39c262b8597)


## Lessons Learned:
1. sdas

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC traceback.htb --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2024-06-25 19:53 PDT
Nmap scan report for traceback.htb (10.10.10.181)
Host is up (0.017s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9625518e6c830748ce114b1fe56d8a28 (RSA)
|   256 54bd467114bdb242a1b6b02d94143b0d (ECDSA)
|_  256 4dc3f852b885ec9c3e4d572c4a82fd86 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Help us
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 56.67 seconds
```

1. Based from the nmap results above, seems the machine runs web application at port 80 and opens ssh login at port 22.
