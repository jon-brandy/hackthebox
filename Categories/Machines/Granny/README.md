# Granny
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/23b1c014-091f-42b7-b238-7a51c5ebef54)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.15 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 20:57 PDT
Nmap scan report for granny.htb (10.10.10.15)
Host is up (0.024s latency).
Not shown: 65534 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 6.0
| http-methods: 
|_  Potentially risky methods: TRACE DELETE COPY MOVE PROPFIND PROPPATCH SEARCH MKCOL LOCK UNLOCK PUT
| http-webdav-scan: 
|   WebDAV type: Unknown
|   Server Date: Fri, 08 Sep 2023 03:59:06 GMT
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   Server Type: Microsoft-IIS/6.0
|_  Allowed Methods: OPTIONS, TRACE, GET, HEAD, DELETE, COPY, MOVE, PROPFIND, PROPPATCH, SEARCH, MKCOL, LOCK, UNLOCK
|_http-server-header: Microsoft-IIS/6.0
|_http-title: Under Construction
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 125.23 seconds
```

1. Based from the nmap resulst, the machine runs a web application.
2. We got the service version too --> Microsoft IIS httpd 6.0.
3. Did a small research about it on the internet, there's many CVE documentation.
