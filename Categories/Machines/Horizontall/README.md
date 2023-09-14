# Horizontall
> Write-up author: jon-brandy
## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.105 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-14 04:24 PDT
Nmap scan report for 10.10.11.105
Host is up (0.031s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ee774143d482bd3e6e6e50cdff6b0dd5 (RSA)
|   256 3ad589d5da9559d9df016837cad510b0 (ECDSA)
|_  256 4a0004b49d29e7af37161b4f802d9894 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-title: Did not follow redirect to http://horizontall.htb
|_http-server-header: nginx/1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 29.63 seconds
```

1. Based from the nmap results, the machine runs a web application and opens a ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/92d91808-156d-4127-89ee-42ab039f7154)


2. After clicking and checking every feature available there, none of the button redirecting us to a homepage.
3. Then I ran dirbuster.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/03dbee97-db70-4c65-953f-80018286079e)


4. `http://horizontall.htb/js/app.c68eb462.js` should be our interest.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b63f25b8-1c99-48c5-84f7-8a57b2671de6)


5. Let's deobfuscate the js with --> https://deobfuscate.io/

> DEOBFUSCATE RESULT -> Found a subdomain that could be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2d13022f-2c63-47dd-ac13-60cdbd1178c9)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b84c94d1-4d50-4de5-907f-ce13a8d01ac6)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e76066e2-cd5c-49a0-9f18-fa652380cccf)



6. Found nothing, let's run dirbuster.

> RESULT - admin directory seems interesting - strapi CMS login page

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5529234-b1b3-48d8-967c-2ca87c71272c)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/04960678-f4e0-4145-a645-8071fe489ba5)


7. This could be our foothold, strapi is an open source node.js Headless CMS (separates the presentation layer `where content is presented` from the backend `where content is managed`.

> use searchsploit

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ea596842-0cb4-4ada-b1c7-af6a87c681ea)


8. Seems we need to identify the strapi version used. The problem is, I already used burpsuite and `whatweb` to do information gathering.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ whatweb http://api-prod.horizontall.htb/admin/auth/login
http://api-prod.horizontall.htb/admin/auth/login [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][nginx/1.14.0 (Ubuntu)], IP[10.10.11.105], Script[text/javascript], Strict-Transport-Security[max-age=31536000; includeSubDomains], Title[Strapi Admin], UncommonHeaders[content-security-policy], X-Frame-Options[SAMEORIGIN], X-Powered-By[Strapi <strapi.io>], X-XSS-Protection[1; mode=block], nginx[1.14.0]
```

9. Anyway we can make an interpretation, since we don't have any cred. Our interest shall be around the 3rd and 4th exploit.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7f7c1cc5-0e48-494f-8f8f-eedd294d0fb6)


10. To copy the script to our current directory, run --> `searchsploit -m 50239.py`.
11. Reading the script at glance, seems we can check the strapi version by changing the url to --> /admin/init.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fc69ec36-6eec-4fff-b7d0-05ce69ec8b8a)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3727ba97-7fb0-4d28-b35c-023c646a78cd)


12. Great we found the version --> `3.0.0-beta.17.4`.
13. Based from the `main()` function we can run --> `python3 script url` to execute the script (because there's `sys.argv[1]`).

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d7c453a1-2e29-4940-8906-43e21e352f2b)


14. Great! Let's run a listener to do reverse shell and send our template bash reverse shell.

> RESULT - GOT SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a0977b61-e195-4ec8-8af9-1cda291d3f44)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e813ec72-4a3f-4741-a35d-0bc06bc2b446)


## USER FLAG

```
b541b4deaf34b257c3f33ee472d67bb2
```

15. Running `sudo -l` to check the sudo permission for user strapi shall resulting to nothing because we logged in as strapi without providing the password.

```
strapi@horizontall:/home/developer$ sudo -l
sudo -l
sudo: no tty present and no askpass program specified
```

16. Stuck for a while, until I ran --> ss -anlp | grep "127.0.0.1"

```
strapi@horizontall:/home/developer$ ss -anlp | grep "127.0.0.1"
ss -anlp | grep "127.0.0.1"
tcp  LISTEN 0      128                                     127.0.0.1:1337                     0.0.0.0:*              users:(("node",pid=1754,fd=31))            
tcp  LISTEN 0      128                                     127.0.0.1:8000                     0.0.0.0:*                                                         
tcp  LISTEN 0      80                                      127.0.0.1:3306                     0.0.0.0:*
```

17. To open each of it, we can just do ssh tunneling. But before, that let's check port that could be our interest. Port 3306 should not be our interest (MySQL) port. To check it run --> curl ip:port.
18. Long story short, port 8000 is our interest. To render it we can do ssh tunneling.
19. But to do it we need to set the shell stable first using ssh-keygen. Let's do it.

> GETTING STABLE SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/764248db-8ef2-45db-84af-26e585559d62)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2ee037a7-b025-4453-8f8e-4346a42eec75)




20. So based from the curl result on port 8000, we can identified the laravel version is 8.

> SEARCHING THE CVE RELATED TO LARAVEL V8 - version 8.4.2 should be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd833cf7-f1ab-48b4-b2f6-48b443fe461a)












