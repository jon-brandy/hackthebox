# Paper
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d312cd0a-ada9-42d0-8b02-1f81a3135a4f)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.143 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-22 20:39 PDT
Nmap scan report for 10.10.11.143
Host is up (0.077s latency).
Not shown: 64783 closed tcp ports (conn-refused), 749 filtered tcp ports (no-response)
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.0 (protocol 2.0)
| ssh-hostkey: 
|   2048 1005ea5056a600cb1c9c93df5f83e064 (RSA)
|   256 588c821cc6632a83875c2f2b4f4dc379 (ECDSA)
|_  256 3178afd13bc42e9d604eeb5d03eca022 (ED25519)
80/tcp  open  http     Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_http-generator: HTML Tidy for HTML5 for Linux version 5.7.28
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: HTTP Server Test Page powered by CentOS
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
443/tcp open  ssl/http Apache httpd 2.4.37 ((centos) OpenSSL/1.1.1k mod_fcgid/2.3.9)
|_http-generator: HTML Tidy for HTML5 for Linux version 5.7.28
|_http-title: HTTP Server Test Page powered by CentOS
| http-methods: 
|_  Potentially risky methods: TRACE
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=Unspecified/countryName=US
| Subject Alternative Name: DNS:localhost.localdomain
| Not valid before: 2021-07-03T08:52:34
|_Not valid after:  2022-07-08T10:32:34
|_http-server-header: Apache/2.4.37 (centos) OpenSSL/1.1.1k mod_fcgid/2.3.9
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 56.47 seconds
```

1. Based from the nmap result, the machine runs a webapp (http and https), also it opens a ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/52cd7818-42c6-4054-a486-4b94ee512928)


2. Capturing the request using burpsuite, found another endpoint --> office.paper.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c717a342-3924-47de-bf10-b9791290463c)


> office.paper

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/216618a5-7286-4bdd-8651-0247707b638f)


3. It's a wordpress blog. Found an interesting comment at this post:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/713eaccc-e8f9-4e76-af24-446e70e76c15)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f22900f1-cd57-41dc-b9b3-03e4e31ec810)


4. This should be a hint, we can interpretes that there's must be a confidential information around.
5. Anyway this took me a while until I realized the wordpress version has CVE documentation.

> WORDPRESS VERSION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3d5773e3-0cb6-47a8-85e9-109afa3dcd02)


> CVE DOCUMENTATION --> https://www.exploit-db.com/exploits/47690

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d113940c-037b-4dd1-8a8b-3a75ef2d03fe)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7373e087-aa12-44ab-a359-48708f4a8a61)


6. Great! We can view a private posts.

> RESULT - FOUND ANOTHER SUBDOMAIN for office.paper

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a25e00cc-37ab-48c1-b030-4b085e5349a4)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eda07e2d-83f3-4965-b553-7db8e53ede0b)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fcb86fb5-7c80-46b1-b313-8b0ac96531f5)


7. It seems we need to use --> `http://chat.office.paper/register/8qozr226AhkCHZdyY` , so we can register.
8. After registering account, login with the same cred.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/32c5be69-e358-4226-847d-99c3a3ff84c4)


9. Reading the `general` you shall find a bot named **Recycle**, based from the chat history we can chatting with bot.
10. There's several commands we can use.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/498a2656-94bf-475e-b52c-12790d9873b8)


11. We can list files at the remote server and we can see the content.
12. Long story short, found the **user.txt** at the `/` directory.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed31160c-97e1-4858-b2e4-51ceaf782b00)


13. But we can't see the content, because only root can read the file.
14. As we know, we're accessing the server as **dwight**.
15. Running --> `reyclops file../../../../../etc/passwd`, we can identified another user named **rocketchat**.
16. Stuck for a while, until I realized there's a directory named **hubot** that dwight can access.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9e8baec9-cbe2-4e90-a478-31713af789fe)


17. Checking the **.env** file we shall find a password for **rocketchat** (?)
18. Here's what's unique, we found 2 users -> rocketchat & dwight. Somehow the password we found is the correct password for dwight when running ssh.

> .env

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/650feda6-9831-4e68-a947-3cce3f565a5a)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a0f376f7-0c06-4a49-a8b0-c079f79bd1ed)


## USER FLAG

```
6276e48a3644fba299956c0a72ad4c7e
```


19. 
