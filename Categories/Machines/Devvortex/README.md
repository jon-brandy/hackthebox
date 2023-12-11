# Devvortex
> Write-up author: jon-brandy

## Lesson Learned:
- Enumerating subdomain using ffuf.
- Directory listing using dirsearch.
- Exploiting CMS Joomla v4.2

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c8f39e13-398d-457a-9e4c-144fc3b34e35)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.11.242 --min-rate 1000     
Starting Nmap 7.93 ( https://nmap.org ) at 2023-12-11 01:23 PST
Nmap scan report for 10.10.11.242
Host is up (0.018s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48add5b83a9fbcbef7e8201ef6bfdeae (RSA)
|   256 b7896c0b20ed49b2c1867c2992741c1f (ECDSA)
|_  256 18cd9d08a621a8b8b6f79f8d405154fb (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://devvortex.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 46.07 seconds
```

1. Based from the nmap results, the machine runs a web application on port 80 and opens ssh logins on port 22.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/255c310a-13f0-45ae-b577-c6595e09a3bc)


2. Next, I tried to do directory listing and enumerating subdomains using **dirsearch** and **ffuf**.  

> Found a subdomain --> dev.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0be7379d-60e0-4c59-bb60-b7fac8d2d383)


> dev.devvortex.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/39af9892-c655-4589-a4aa-7fd5ac5af7dc)


3. Running dirsearch again, found bunch of endpoint but one of them **administrator** shall be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b40a7b83-edad-493e-ac79-e66d4e1bcc81)


4. Turns out, it is **Joomla login page**. The webapp using **Joomla** CMS.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/452101aa-1232-4b6c-8fca-f411881795e0)


5. Searching on the internet for joomla login's default creds, shall leads to nothing.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b745f33-12bd-4216-a328-395676b9a3c4)


6. Running dirsearch again but this time without wordlist, found **README.txt** file and other interesting files.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/84bd48f3-803b-44f2-91f6-d30a454f1321)


7. Accessing it, shows us the joomla's version.


> VERSION 4.2

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0c30845a-a544-42f6-a3fb-063287bfbb21)


8. Searching on the internet about the exploit for Joomla v4.2, found this promising github's POC.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b5c4a4e5-aff2-4256-b7b7-4be768cbabf9)


9. 

## IMPORTANT LINKS

```
https://github.com/Acceis/exploit-CVE-2023-23752
https://www.exploit-db.com/exploits/51334
```
