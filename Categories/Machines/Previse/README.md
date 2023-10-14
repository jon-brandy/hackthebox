# Previse
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/66cdadd8-4e5d-4b69-847e-30c752492d73)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- 10.10.11.104 -sVC --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-13 22:52 PDT
Nmap scan report for 10.10.11.104
Host is up (0.032s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 53ed4440116e8bda698579c081f23a12 (RSA)
|   256 bc5420ac1723bb5020f4e16e620f01b5 (ECDSA)
|_  256 33c189ea5973b1788438a421100c91d8 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-title: Previse Login
|_Requested resource was login.php
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.77 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6bb0b815-8bd3-4226-a432-cb09d1e8e1f5)


2. After ran **dirbuster** shall found several files.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b24922d9-109a-4158-9315-c1ddf4565688)


3. Checking every endpoint with **200** as it status code, turns out **nav.php** should be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6757eaa8-b94d-41d2-81c0-bb8884bb4ea2)


4. Click the `CREATE ACCOUNT` option shall redirect you to the login page.
5. Interesting.
6. 
