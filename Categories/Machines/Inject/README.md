# Inject
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/badbc336-8df3-4625-b604-12ca012c8b9a)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.204 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-26 04:39 PDT
Nmap scan report for inject.htb (10.10.11.204)
Host is up (0.065s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 caf10c515a596277f0a80c5c7c8ddaf8 (RSA)
|   256 d51c81c97b076b1cc1b429254b52219f (ECDSA)
|_  256 db1d8ceb9472b0d3ed44b96c93a7f91d (ED25519)
8080/tcp open  nagios-nsca Nagios NSCA
|_http-title: Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.33 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/18855496-990c-492c-825c-109b1ea4644b)


2. Long story short, of all the existing features this website have. Only upload feature which could be our foothold.
3. When I tried to upload a ELF file, it showed this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/112575ec-8f40-4b71-83e6-171fe53fc405)


4. It does validate the extension file uploaded but does it sanitize the contents??
5. This could be our foothold. Anyway let's try to upload a normal image file there.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e72d5d5c-6d6a-491b-ba12-8eecd27ada69)


6. Interesting! We can view it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7fc88b50-5f42-4114-be89-e9d0fdc0f1a5)


7. Great! More interestingly there's a URL parameter! We can send our reverse shell and access it to trigger it.
8. 
