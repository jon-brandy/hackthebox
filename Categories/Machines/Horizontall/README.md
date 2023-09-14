![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e41ec789-f6c2-4ee0-95a8-9712ed595967)# Horizontall
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

9. 
