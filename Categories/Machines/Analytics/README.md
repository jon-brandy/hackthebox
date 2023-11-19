# Analytics
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b992274b-eee2-4815-9962-5968bd5498c8)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.233 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-18 20:52 PDT
Nmap scan report for 10.10.11.233
Host is up (0.084s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3eea454bc5d16d6fe2d4d13b0a3da94f (ECDSA)
|_  256 64cc75de4ae6a5b473eb3f1bcfb4e394 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://analytical.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 85.17 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh logins.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3136aba1-1488-4e1e-ba6c-88b81c97df63)


2. After ran **dirsearch** found nothing interesting.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d3b2b1e8-467b-49d7-950d-ec7fdf0a8635)


3. Enumerating subdomain for the host found one result.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ ffuf -w SecLists/Discovery/DNS/subdomains-top1million-5000.txt -u http://10.10.11.233 -H "Host: FUZZ.analytical.htb" -mc all -ac

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.0.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.11.233
 :: Wordlist         : FUZZ: /home/brandy/SecLists/Discovery/DNS/subdomains-top1million-5000.txt
 :: Header           : Host: FUZZ.analytical.htb
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
________________________________________________

[Status: 200, Size: 77883, Words: 3574, Lines: 28, Duration: 68ms]
    * FUZZ: data

:: Progress: [4989/4989] :: Job [1/1] :: 1388 req/sec :: Duration: [0:00:04] :: Errors: 0 ::
```

> data.analytical.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/781dbb51-a3be-4fd6-9e51-7ec757de690e)


4. Now we're given a metabase login page. Searching on Google about it's vuln found several results of it:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d03f3da6-473d-4bbc-850a-62f851c2f210)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/17c03739-d9ad-41a4-ab11-b17e1dae01c9)


5. Checking metasploit for this module found one result which corresponds the previous result we got.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0a24fdd5-a6ab-41e3-800c-cab67b9f1dcb)


> USING IT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/821165e6-591d-448e-9314-600ef2afbfd0)


6. Got shell! But sadly it does not have python3 running, hence we can't get a stable shell.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6fcc6953-78b7-41ed-93a0-b8c2c9191509)


7. Somehow the user.txt is not there, hence we need to enumerate dirs and files to find config file or .db file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/71123638-2235-4861-a933-e79d39935cc5)


8. At the `/` diretory found a .db directory which holds two DBs file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ca68ea08-f1c3-4acc-84b2-40c0c4be71ff)


9. The first .db file --> `metabase.db.mv.db` should be our interest (because it holds big information, but still taks long time to analyze), so I tried to enumerate other aspect.
10. Running `ls -a` shows **.dockerenv**, hence let's run **env** command.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9698d7fa-92b0-4fa7-ba90-4452c9afe490)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/34a9d2e6-5cc3-473e-9a90-031525769a75)


11. Great! We found cred --> `metalytics:An4lytics_ds20223#`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3158d08d-874e-492d-af15-7d9f458b49f7)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3caec3a3-cfc1-4c0a-9e7e-9918d9dc979b)


## USER FLAG

```
839ce638e8a39a87207f8d584fd86c45
```

12. To gained root, I ran linpeas to search for potentials privesc.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f7ac57b3-0b9f-4d4f-bf58-8a4c60959e83)


13. It does suggest several CVE exploits but the ubuntu version for the machine is --> `Ubuntu 22.04.3 LTS`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3a3e4f2c-f6a7-4076-9f10-7f57892cb808)


14. Searching on the internet about local privesc in ubuntu 22, shall resulting to this article.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/71be8c79-ea90-4a5a-9b08-67dbb7e72839)




