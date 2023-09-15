![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e142b66e-ea17-4117-aa3c-ba53ceee9dd6)# Nunchucks 
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/07260abf-8e6f-49eb-86fa-aefb6913930f)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~/Downloads]
└─$ nmap -p- -sVC 10.10.11.122 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-15 03:41 PDT
Nmap scan report for 10.10.11.122
Host is up (0.042s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 6c146dbb7459c3782e48f511d85b4721 (RSA)
|   256 a2f42c427465a37c26dd497223827271 (ECDSA)
|_  256 e18d44e7216d7c132fea3b8358aa02b3 (ED25519)
80/tcp  open  http     nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to https://nunchucks.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
443/tcp open  ssl/http nginx 1.18.0 (Ubuntu)
|_http-title: Nunchucks - Landing Page
| ssl-cert: Subject: commonName=nunchucks.htb/organizationName=Nunchucks-Certificates/stateOrProvinceName=Dorset/countryName=UK
| Subject Alternative Name: DNS:localhost, DNS:nunchucks.htb
| Not valid before: 2021-08-30T15:42:24
|_Not valid after:  2031-08-28T15:42:24
| tls-nextprotoneg: 
|_  http/1.1
| tls-alpn: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 43.76 seconds
```

1. Based from the nmap results, the machine runs a web applicatoin and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0e52b16f-9ae9-402b-8691-25f5011ffc30)


2. Trying every feature, resulting to nothing interesting. Even when tried to register account, they said it's closed already.
3. Running **dirbuster** found nothing interesting again.
4. But checking the subdomain, by running **gobuster**, found one domain that should be our interest --> `store.nunchucks.htb`.

#### NOTES:
```
Since nunchuck is https --> hence need to add -k

gobuster vhost -u host -w wordlists -k
```

5.




