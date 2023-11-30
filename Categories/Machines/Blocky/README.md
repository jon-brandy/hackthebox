# Blocky
> Write-up author: jon-brandy

## Lesson learned:
- Directory listing using dirbuster.
- Decompile a .jar file using JADX-GUI.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2029e728-fc4a-4513-8896-a723cb5aef66)

## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.37 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-29 20:21 PDT
Nmap scan report for 10.10.10.37
Host is up (0.019s latency).
Not shown: 65530 filtered tcp ports (no-response)
PORT      STATE  SERVICE   VERSION
21/tcp    open   ftp       ProFTPD 1.3.5a
22/tcp    open   ssh       OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d62b99b4d5e753ce2bfcb5d79d79fba2 (RSA)
|   256 5d7f389570c9beac67a01e86e7978403 (ECDSA)
|_  256 09d5c204951a90ef87562597df837067 (ED25519)
80/tcp    open   http      Apache httpd 2.4.18
|_http-title: Did not follow redirect to http://blocky.htb
|_http-server-header: Apache/2.4.18 (Ubuntu)
8192/tcp  closed sophos
25565/tcp open   minecraft Minecraft 1.11.2 (Protocol: 127, Message: A Minecraft Server, Users: 0/20)
Service Info: Host: 127.0.1.1; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 113.29 seconds
```

1. Interesting, the machine runs a minecraft server on port 25565. Noticing the ftp version, it's famous for the RCE vuln.
2. But let's keep that assumption first. After i ran dirbuster, found 2 files that could be our interest.

> Dirbusting for .jar, .py, .txt, .php, .sh, .pl.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b9bbd36d-b13c-4b65-a8a8-07aee6f3a40d)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7c652bda-3133-44f2-b422-7d16a1cefc35)


3. This interest is supported by the argument from `/wiki`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5442d02a-3184-443e-8669-5d1d80269051)


> DECOMPILED BLOCKYCORE.JAR FILE WITH JADX-GUI | the other .jar file is not our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/aea4b081-0d99-49bb-81c7-d2aa0533c0f0)


4. It exposes the credentials for the root MySQL user.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0b5b64c9-0f3a-4be4-9952-449b945b3d4e)


5. It hangs, confused here. Took me a while until i found a username --> `notch`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b6b4f88-7c16-436b-adfa-c7df972d255b)


6. Kinda guessy, i tried to login ssh using the username notch and the sql's root password.

> notch:8YsqfCTnvxAUeduzjNSXe22

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/eb0fd3c8-4a4d-41fd-9e4f-a919077a1ced)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7b3763fd-580d-45e1-a014-22ab90e07d74)


## USER FLAG

```
4e6d91752cf5832e2b3573374c25aad9
```

> GETTING ROOT FLAG

7. Let's check sudo permission for notch.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8323459f-36a8-4356-a59b-c8a444b126e7)


8. Amazing!

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/50357bca-984c-4a39-afa9-085f6596b830)


## ROOT FLAG

```
06f2b8fd21272c07fb1995977fa0fbfb
```
