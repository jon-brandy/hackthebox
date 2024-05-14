# Blunder
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b254294e-6b45-4741-8c64-c1855f41aeb2)


## Lessons Laerned:
- Bludit CMS Exploitation.

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC blunder.htb --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2024-05-13 20:47 PDT
Nmap scan report for blunder.htb (10.10.10.191)
Host is up (0.017s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE  SERVICE VERSION
21/tcp closed ftp
80/tcp open   http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Blunder | A blunder of interesting facts
|_http-generator: Blunder

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 133.26 seconds
```

1. Based from the nmap results above, the machine runs web application at port 80 and opens ssh login at port 21.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/55feec7a-d102-45ce-9741-c2b096750349)


2. Checking each feature available at the website, none of it seems to be our interest. Upon running **dirsearch** found several endpoints.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ce69db0-af21-4ec4-8537-21d206d2403d)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5ea0847c-4bd0-461d-92a8-eec60179dbc3)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ca4e0c7c-1a36-414b-86b8-019d33111871)


3. Accessing `/todo.txt` endpoint, noticed that CMS is not updated yet. Hence the CMS seems should be exploited. Also noticed it stated a person named `fergus`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5db8b5fd-53a5-44b1-a168-e893d38ad917)


4. Great! Now let's access the `/admin` endpoint.

> BLUDIT CMS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a4528b7f-bc2a-474c-9599-d0e75005c2f0)


5. Checking the page source, we can identified the CMS version is **3.9.2**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/442521a4-a533-4e67-ab3a-e82abeb85c77)


6. Searcing on the internet and using searchsploit to identified vulns for the related version, resulting to these:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/94ef0d9f-17bf-46e6-b062-42d6c6b1a6cd)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/676588dd-658c-4a69-89f2-ad271213830a)


7. Interesting, we got few options. However, among all of it seems **bruteforce** should be our interest.


## IMPORTANT LINKS

```
https://www.hackingarticles.in/wordlists-for-pentester/
```
