# Traverxec
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d8c34a13-fe79-45bf-9a19-19faf531ca67)


## Lessons Learned:
- sdada

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.10.165 --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2024-01-22 01:12 PST
Nmap scan report for 10.10.10.165
Host is up (0.25s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 aa99a81668cd41ccf96c8401c759095c (RSA)
|   256 93dd1a23eed71f086b58470973a388cc (ECDSA)
|_  256 9dd6621e7afb8f5692e637f110db9bce (ED25519)
80/tcp open  http    nostromo 1.9.6
|_http-server-header: nostromo 1.9.6
|_http-title: TRAVERXEC
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 147.43 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login at port 22.

> WEB APP

