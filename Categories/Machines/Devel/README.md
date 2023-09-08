# Devel
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/08fa0240-d04c-403e-8edd-e524f901862f)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.5 --min-rate 1000  
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-08 07:35 PDT
Nmap scan report for 10.10.10.5
Host is up (0.026s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  02:06AM       <DIR>          aspnet_client
| 03-17-17  05:37PM                  689 iisstart.htm
|_03-17-17  05:37PM               184946 welcome.png
80/tcp open  http    Microsoft IIS httpd 7.5
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/7.5
|_http-title: IIS7
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 113.08 seconds
```

1. Based from the nmap results, the machine runs a web application and opens a anonymous ftp login.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/56e020b6-16b2-4033-9849-e486a2b6f17f)


2. Did a small research about the service version for http, found a CVE that could be our interest -> https://www.exploit-db.com/exploits/15803


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e88dcd00-0758-481f-98d1-98661800d40d)


3. Anyway, let's login to ftp first.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bd844e68-ee68-4ff0-a8fd-af981fb44c59)


4. Traversing the directory found no files at all.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/90f5c1ab-37e1-4bbe-8e45-be4c8db31907)


