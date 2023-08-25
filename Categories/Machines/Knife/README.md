# Knife

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b047d79-69bf-4a4d-aec3-f51ced0790a9)


> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.242 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 23:19 PDT
Nmap scan report for 10.10.10.242
Host is up (0.019s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 be549ca367c315c364717f6a534a4c21 (RSA)
|   256 bf8a3fd406e92e874ec97eab220ec0ee (ECDSA)
|_  256 1adea1cc37ce53bb1bfb2b0badb3f684 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title:  Emergent Medical Idea
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.65 seconds
```

Found 2 ports open, and the machine is running a web application with PHP version 8.1.0.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6970c5b2-6643-4afc-ae61-ce75826b97ca)


Turns out the PHP version is vulnerable to Backdoor RCE.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fe82c05d-6479-4eae-90d8-c06224a807d2)

