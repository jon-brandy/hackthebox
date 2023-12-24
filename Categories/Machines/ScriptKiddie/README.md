# ScriptKiddie
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/66991b94-aab3-4665-8830-1f017dc36df5)


## LESSONS LEARNED:
- asdjkasnd

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~/Downloads]
└─$ nmap -p- -sV -sC 10.10.10.226 --min-rate 1000    
Starting Nmap 7.93 ( https://nmap.org ) at 2023-12-24 01:47 PST
Nmap scan report for scriptkiddie.htb (10.10.10.226)
Host is up (0.019s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 3c656bc2dfb99d627427a7b8a9d3252c (RSA)
|   256 b9a1785d3c1b25e03cef678d71d3a3ec (ECDSA)
|_  256 8bcf4182c6acef9180377cc94511e843 (ED25519)
5000/tcp open  http    Werkzeug httpd 0.16.1 (Python 3.8.5)
|_http-server-header: Werkzeug/0.16.1 Python/3.8.5
|_http-title: k1d'5 h4ck3r t00l5
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 73.05 seconds
```

1. Based from the nmap results, the machine runs a web application at port 5000 hosted with **Werkzeug httpd 0.16.1** webserver and it opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e977c852-6d17-410e-8dc0-7fbc752feddd)


2. Let's see if we can get the same result as our previous nmap scans by submitting localhost ip.

> Turns out we get the same result.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a5154aa3-a693-4e22-9fd6-0a9d1b3988f4)


3. Well, I assume this webapp provides the same functional as our own tools in kali.
4. 
