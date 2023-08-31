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

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/28fa372d-50d5-4f6b-915f-11efb9b5d0a9)


8. For the password, it's kinda guessing. It took me a while, until I have assumptions that the password must be `nibbles`.
9. Judging from the email I found in --> `http://nibbles.htb/nibbleblog/content/private/config.xml`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f663ce16-89b1-4f10-8600-dc3d0c1d8066)


10. So the cred is --> `admin:nibbles`.

> ADMIN.PHP --> LOGGED IN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8849b27c-a2bc-44df-a23e-2692c1ce8fca)


11. TIME SKIP.. Found a potential file upload vuln at the `plugins` option. Go to plugins -> choose the **about** plugin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1226a725-96bc-45ad-b4f2-b8364c3e7caf)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1777ead7-4cf1-4619-b19b-d27160480dd5)


12. We can upload PHP reverse shell. Let's upload the template payload from **pentest-monkeys**.
13. Set a listener on the port you specified, then access the endpoint of our reverse shell payload.
14. BUT, dunno why I can't get RCE.
15. So, there's 2 plugins path, one is /plugins/ and the other one is /content/private/plugins/.
16. But somehow I failed for both, our file won't show up there, and when I think we only can overwrite the content of the files with our reverse shell payload, I still failed to get RCE anyway.
17. So I give up to get shell manually and I use metasploit.

> USING METASPLOIT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e37fa01f-d506-462a-adf7-ff6f271b5ace)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fb55af8f-879a-4e85-8a67-b5cda594f953)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5d240cf9-213d-4ca7-8854-cf031d5d8977)


18. Noticed the vuln is at my_image plugins (?) Already tried to upload the reverse shell manually there, but still failed.

> GETTING USER.TXT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e9693654-6d7c-4141-97a3-62079ad6f212)


## USER FLAG

```
a6e9e4dc81df37229881e55cfa4fc658
```

> GETTING ROOT FLAG






