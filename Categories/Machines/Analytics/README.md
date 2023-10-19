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


5. Checking metasploit about it found one module.



