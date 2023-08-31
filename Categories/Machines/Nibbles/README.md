# Nibbles
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ecef1d4d-8619-447a-ab65-02edffd61d40)


## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.75 --min-rate 1000        
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-31 04:18 PDT
Nmap scan report for 10.10.10.75
Host is up (0.020s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4f8ade8f80477decf150d630a187e49 (RSA)
|   256 228fb197bf0f1708fc7e2c8fe9773a48 (ECDSA)
|_  256 e6ac27a3b5a9f1123c34a55d5beb3de9 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.73 seconds
```

1. Based from the result, the machine runs a web application.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bfa46a9d-2375-4e66-82d2-627c3e3874e5)


2. Viewing the page source, we know there's a directory named `nibbleblog`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4ed35387-6a77-4c0f-9524-8a00eb907724)


3. At this point, I have an assumption the vuln might be either SQLi or Arbitrary File Upload.

> Searching in msf about nibble shall showed the vuln's history.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/57c291fa-f000-4380-9531-a5c96088559d)


4. After ran dirbuster to list all the files within the `/nibbleblog/` directory, found several files that could be our interest.

### NOTES:

```
I did not find any interesting files outside the /nibbleblog/ direcotry.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ecfe8140-b08d-4b39-9b15-84438ae833bb)


5. Long story short, the `admin.php` opens up a login page and there's no SQLi vuln at all.
6. So we need to find a valid cred.
7. Found the potential username at --> `http://nibbles.htb/nibbleblog/content/private/users.xml`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a1f233d6-ae4c-4b7a-a1e2-0cbb98c6616c)



