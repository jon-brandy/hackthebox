# Optimum
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/335450dc-5359-4fbd-b549-351de3bcb35b)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.8 --min-rate 1000 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 18:18 PDT
Nmap scan report for optimum.htb (10.10.10.8)
Host is up (0.023s latency).
Not shown: 65534 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    HttpFileServer httpd 2.3
|_http-title: HFS /
|_http-server-header: HFS 2.3
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 112.60 seconds
```

1. Based from the nmap result, the machine's runs a web application, also we know the version of the HttpFileServer.
2. Throw it on Google, I found an exploit DB about this HttpFileServer's version --> https://www.exploit-db.com/exploits/39161.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31a90ece-0307-4970-92a4-999a992f1137)


3. To solve this challenge, I used metasploit.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/59a6e933-3fe4-4a9d-8edd-43ac141274c9)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1f0e92d2-7daf-40ee-818b-177f8957554b)


> GOT SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e00ce7ff-9cae-4e1c-9ee6-4f5e2e97e895)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/54fd1549-419b-4faf-ad25-41d2c308e7eb)


## USER FLAG

```
0b23283b94bcc32baf7b03ab44beda7b
```
