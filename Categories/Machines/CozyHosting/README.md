# CozyHosting
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fa4c16d1-f3fe-47c6-810f-466d37c566a6)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.230 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-30 22:59 PDT
Nmap scan report for 10.10.11.230
Host is up (0.032s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4356bca7f2ec46ddc10f83304c2caaa8 (ECDSA)
|_  256 6f7a6c3fa68de27595d47b71ac4f7e42 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://cozyhosting.htb
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.72 seconds
```

1. Based from the nmap results, the machine runs a webapp and opens ssh logins.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd9b7161-dbf0-4b00-b073-ef80301da3e2)


2. The wappalyzer itself shows us minimum info (for version).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1850a964-0b31-4a53-961a-1beee364802c)


3. Hence i ran dirsearch to list all directories or files available for this webapp.

> RESULTS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5697fb2f-fb43-476f-8efc-705146d76b30)


4. `admin` page and `actuator` directory should be our interest here.
5. Opens `actuator/sessions` shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/617cbf55-e5f0-470d-a54c-53965f5817bb)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e95e9939-f036-4f73-af4a-6a7330e23f2c)


6. Noticed there's a user session with name `kanderson` (Informatin Disclosure).
7. Let's change our session to kanderson's, then refresh the page.

 ![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a7c8c241-4cfa-4d95-a058-7c0bdd8b7d4f)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fac50408-3393-41e8-8df3-b4d2f3cf9604)


8. Scrolling down you shall see an input box.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dbbc52af-baf7-45d6-9dd8-036986c88b27)


9. This should be our interest. To identify what's the vuln, let's capture the request we send using burpsuite.

> RESULT


