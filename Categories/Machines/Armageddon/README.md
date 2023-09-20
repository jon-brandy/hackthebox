# Armageddon
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c0898996-3c1f-46ef-a4dd-fcb8960b6b3f)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.233 --min-rate 1000       
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-20 04:49 PDT
Nmap scan report for 10.10.10.233
Host is up (0.030s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 82c6bbc7026a93bb7ccbdd9c30937934 (RSA)
|   256 3aca9530f312d7ca4505bcc7f116bbfc (ECDSA)
|_  256 7ad4b36879cf628a7d5a61e7060f5f33 (ED25519)
80/tcp open  http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-generator: Drupal 7 (http://drupal.org)
| http-robots.txt: 36 disallowed entries (15 shown)
| /includes/ /misc/ /modules/ /profiles/ /scripts/ 
| /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt 
| /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt 
|_/LICENSE.txt /MAINTAINERS.txt
|_http-title: Welcome to  Armageddon |  Armageddon
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 122.15 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8338bf80-93a6-4b1e-a6fe-1f141d0fba93)


2. Noticed the webapp using **Drupal 7** CMS.

> DRUPAL 7 EXPLOIT DOCUMENTATION --> https://www.exploit-db.com/exploits/44449

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/70860b11-e9cc-4653-bab6-ebb1f17e8230)


3. Great! Based from the documentation and the chall's title. We seems in the correct approach.
4. Found a 2 github POCs we can use here.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f04f5a98-3fea-46d2-aa49-2a997e20f43e)


5. I used the most starred github repo --> https://github.com/dreadlocked/Drupalgeddon2
6. Let's clone the repo and run the ruby solver.

> RESULT




