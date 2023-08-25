# Bashed

> Write-up author: jon-brandy
 
## STEPS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/06d890ab-a95a-4c82-bc6f-c774d0792714)

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.68 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-25 02:31 PDT
Stats: 0:00:13 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 0.00% done
Nmap scan report for 10.10.10.68
Host is up (0.019s latency).
Not shown: 65534 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Arrexel's Development Site

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.82 seconds
```

1. Based from the result, the machine is running a web application.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bda28df5-de80-4de6-aff5-d6e891c3015e)


2. Found an interesting directory --> `/dev` which leads to a file named `phpbash.php`.
3. Why it's interesting, because the webpage documented about it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/02196f2f-b47e-4490-8a0a-275115c0bb24)


> GITHUB DOCUMENTATION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c7329fd1-1c43-40c2-8020-5c5ced9658f6)


4. 
