# Grandpa
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4a55d683-a2ad-4aa9-bcea-6b43ddda95b3)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.14 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 21:47 PDT
Nmap scan report for 10.10.10.14
Host is up (0.025s latency).
Not shown: 65534 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    Microsoft IIS httpd 6.0
| http-webdav-scan: 
|   Allowed Methods: OPTIONS, TRACE, GET, HEAD, COPY, PROPFIND, SEARCH, LOCK, UNLOCK
|   Server Type: Microsoft-IIS/6.0
|   Public Options: OPTIONS, TRACE, GET, HEAD, DELETE, PUT, POST, COPY, MOVE, MKCOL, PROPFIND, PROPPATCH, LOCK, UNLOCK, SEARCH
|   WebDAV type: Unknown
|_  Server Date: Fri, 08 Sep 2023 04:49:20 GMT
| http-methods: 
|_  Potentially risky methods: TRACE COPY PROPFIND SEARCH LOCK UNLOCK DELETE PUT MOVE MKCOL PROPPATCH
|_http-server-header: Microsoft-IIS/6.0
|_http-title: Error
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 146.43 seconds

```

1. Based from the nmap result, the machine runs a web application and opening it, you shall realized it's the same webapp as the other machine challenge named "Grandma".
2. Dunno why HTB makes 2 same machine, but what comes to my mind, might be the intended solve is different.
3. Anyway I managed to solved this challenge using the **SAME** method as solving **Grandma**.
4. But maybe there's one little notes I forgot to write, to do privesc, I migrated first to davcdata.exe at session 1.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4fffe441-e0a4-46eb-9947-c3f2b0eeef3a)


5. Migrating to davcdata.exe is a common tech to evade detection and improve privesc. Here's the example if I tried to do privesc without migrating the session to davcdata.exe:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f179ab68-4ee1-4f05-8d2b-ef2e5f5ecf1a)


6. Anyway, just like what I said before, the rest is the same as **Granny** machine.

> GETTING USER FLAG


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fc7911a2-bded-4c76-bb02-8ba13cb50045)


## USER FLAG

```
bdff5ec67c3cff017f2bedc146a5d869
```


> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f87a034f-1524-43c9-bae7-faa4a1aa0877)


## ROOT FLAG

```
9359e905a2c35f861f6a57cecf28bb7b
```
