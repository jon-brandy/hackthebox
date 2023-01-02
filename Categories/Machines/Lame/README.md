# Lame
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, run nmap to the machine's host, so we can see all open ports and the service's running.

```sh
nmap -p- -sV -O -sVC 10.10.10.3
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210200834-fd61ad0f-e57d-4c34-af0c-663fc0e4ce31.png)

![image](https://user-images.githubusercontent.com/70703371/210200847-3663931c-6d30-429b-adde-26fe9fe58565.png)


2. Notice there's 2 ports that might be running some type of network shares. Not only that, we're allowed to login in ftp as anonymous.

![image](https://user-images.githubusercontent.com/70703371/210200591-280e0c35-7e9a-450f-b3cd-b5c7f448ff71.png)


![image](https://user-images.githubusercontent.com/70703371/210200876-cff53d63-2281-4b0f-a3e6-21591c5f1b3a.png)


3. Now let's login with ftp.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210200952-d0d2836b-dd36-4f60-8059-bb07a61edbe1.png)


4. Let's check are there any files or directories.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210201004-e1acce9b-8363-4406-9b9b-31b33d1c3fd4.png)


5. Got nothing.
6. Now let's do SMB enumeration.

```sh
smbmap -H 10.10.10.3
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210201182-4a75571d-55ba-4bc2-a37b-9ddd8ec454d4.png)


7. Notice there's 2 different directories than the others -> tmp, opt (doesn't have any dollar sign).

![image](https://user-images.githubusercontent.com/70703371/210201218-80dff691-4b63-47a0-9a08-9f84e40c5de4.png)

#### NOTES: 

```
tmp and opt doesn't have any dollar sign, means it can be accessed by regular use privileges.
```

8. Since only **tmp** directory with permissions to read and write, means **tmp** shall be our interest now. But the problem is we don't have any user credentials for this tmp directory.
9. Even though it's open here, but still we need user credentials to login to it.
10. Now let's use **search split** to potentially see if there's an exploit associated with the service version of samba that's running on this machine.

> RESULT

```sh
searchsploit samba 3.0.2
```

![image](https://user-images.githubusercontent.com/70703371/210201595-fb83c002-b0ef-4450-a9ca-d9d777b80f2e.png)


11. Based from the first output.

![image](https://user-images.githubusercontent.com/70703371/210201674-557895a0-5f71-4919-a613-913b2c2829ab.png)


12. We can use metasploit, but let's not use that tools, we want to dive in manually, let's start by find where this exploit stored on our kali linux (THE CVE NUMBER).

![image](https://user-images.githubusercontent.com/70703371/210201783-447f9a3f-ff63-4905-a77a-8a4a93f8e7f3.png)


> RESULT

```sh
cat /usr/share/exploitdb/exploits/unix/remote/16320.rb | grep CVE
```

![image](https://user-images.githubusercontent.com/70703371/210201888-d40c6da4-5683-446c-bdab-5fb2e9b36b70.png)








