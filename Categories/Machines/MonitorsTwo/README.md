# MonitorsTwo
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c72614be-89d7-47e2-9832-ecfe0e74fa20)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.211 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-24 01:20 PDT
Nmap scan report for monitorstwo (10.10.11.211)
Host is up (0.039s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48add5b83a9fbcbef7e8201ef6bfdeae (RSA)
|   256 b7896c0b20ed49b2c1867c2992741c1f (ECDSA)
|_  256 18cd9d08a621a8b8b6f79f8d405154fb (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Login to Cacti
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.73 seconds
```

1. Based from the nmap result, the machine runs a web application and opens ssh logins.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/53b65fe9-1ee3-4e5c-8c83-634fb95abb35)


2. Luckily we can see the Cacti version. Researching on the internet shall leads to this CVE documentation --> https://vulners.com/exploitdb/EDB-ID:51166.
3. Reviewing the source code, seems the attack approach is we need to access `/remote_agent.php` and add another request header parameter --> `X-Forwarded-For`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eb78bab2-139c-4e4f-9040-dc9ff5726d57)


4. This should be our foothold to do reverse shell.
5. Let's set a listener on port 1337, setup python server at port 80 so we can curl our bash reverse shell file to the remote server using burpsuite.
6. Don't forget to do URL encoding for the curl command.

> PAYLOAD TO SEND

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8c48a934-d1d6-46ec-b001-d7b822716533)


> REQUEST TO SEND

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2bd9e2e9-81bf-4d29-b00c-4bcd7fd66aab)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8c3bea1c-6112-438a-bb1a-85551df7e81e)


7. Running `ls` you shall see bunch files. Tbh took me a while until I found a directory which holds **config.php** file -> it has MySQL cred.

> /var/www/html/include/config.php

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6ebdc88f-d949-4423-a1ec-18a0181197e0)


8. Great! Using this information, we can connect to **Cacti** database on MySQL.
9. This should allows us to enumerate the tables.

> CONNECTING TO CACTI DB

```
mysql -h db -u root -proot cacti -e 'show databases;'
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/28d53539-dfaf-486d-b8c9-5308dfffd821)


> Use cacti

```
mysql -h db -u root -proot cacti -e 'use cacti; show tables;'
```

10. Got bunch results again, but **user_auth** could be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/17807b61-e02d-44bc-99c8-512d91ef5039)


> Dumping user_auth

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7af579cc-004c-4a59-83f1-aba3c55c7eed)


11. Great! Found the **admin** cred, let's make it more clear by selecting username and password only.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/907d3990-d079-4942-b8a4-859b5798b638)


12. Noticed there's 2 creds that should be our interest --> admin and marcus.
13. Let's use john to crack both hashes.
14. Long story short, only marcus hash can be cracked by john.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7dafa110-a8b4-4747-af0d-05d3bd16fd97)


> LOGIN AS MARCUS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/50483c1e-af8a-4b22-8d4e-36c61c377fbb)


15. Sadly we can't check sudo permission for marcus.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f73d2c85-445f-4bd6-8359-0897ad9a714b)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8df43a00-29fe-4693-9737-14faf8d68aca)


## USER FLAG

```
fa555eb52270bc288bd5b972c955debc
```

16. To do privesc, I download linpeas.sh to the remote server.
17. Running linpeas.sh obviously shall showing you bunch of potential files that **could** help us to gain root, included with the CVE version.
18. Anyway things to remember, marcus can't run sudo.
19. Checking another linpeas result, found mails.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5d74fa6f-9bbb-43f2-b584-1fbc1911d709)


20. Both mails have the same contents.

> CONTENTS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2b42d503-66e0-4818-bf67-173c7a2891b6)


21. Checking all the CVE version listed at the mail, the most potential is --> CVE-2021-41091.
22. Seems the goal is to exploit **Moby Docker Engine**.
23. Did a research shall resulting to these references:

```
https://exploit-notes.hdks.org/exploit/container/docker/moby-docker-engine-privesc/
https://github.com/UncleJ4ck/CVE-2021-41091
```

24. Let's follow the steps in the documentation and clone the git repository to use the solver.
25. Then moved it to the remote server and run the script.

> RESULT


