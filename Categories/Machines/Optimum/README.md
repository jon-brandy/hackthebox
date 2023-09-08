# Optimum
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/335450dc-5359-4fbd-b549-351de3bcb35b)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.8 --min-rate 1000 
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-07 18:18 PDT
Nmap scan report for optimum.htb (10.10.10.8)
Host is up (0.023s latency).
Not shown: 65534 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
80/tcp open  http    HttpFileServer httpd 2.3
|_http-title: HFS /
|_http-server-header: HFS 2.3
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 112.60 seconds
```

1. Based from the nmap result, the machine's runs a web application, also we know the version of the HttpFileServer.
2. Throw it on Google, I found an exploit DB about this HttpFileServer's version --> https://www.exploit-db.com/exploits/39161.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31a90ece-0307-4970-92a4-999a992f1137)


3. To solve this challenge, I used metasploit.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/59a6e933-3fe4-4a9d-8edd-43ac141274c9)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1f0e92d2-7daf-40ee-818b-177f8957554b)


> GOT SHELL

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e00ce7ff-9cae-4e1c-9ee6-4f5e2e97e895)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/54fd1549-419b-4faf-ad25-41d2c308e7eb)


## USER FLAG

```
0b23283b94bcc32baf7b03ab44beda7b
```

4. Not a fond in windows pentesting yet, so maybe there's another way to get privesc manually.
5. So I used a metasploit module again.
6. First I ran `sysinfo` first to gather basic information about the target system or session.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ef9ac133-ec5e-4617-8134-fb6f1af983f7)


7. Based from the results, our target is -> Windows 2012 R2 (6.3 Build 9600) and it's arch is x64.
8. On the other side, our meterpreter is x86.
9. Let's migrate first to x64.
10. Run `ps` --> migrate to explorer.exe.
11. Then run `background` to make a new session (since we want to use another module).
12. Next run --> `search exploit/windows/local`.
13. It shows many results, but the one that should be our interest is this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e3096c04-fb36-4349-ab4f-8e33a2d290d4)


14. Use it. Then set the rhosts and lhost again.
15. BUT, also run `set TARGET 1` (1 is windows x64) and lastly run `set SESSION 1` (referring to our previous session, to do privesc auto).


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d0b91350-ed52-4599-b1a7-0994730b53dc)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c71623ab-6e3e-4b6e-a9b9-43dbd511fddc)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d0cec63d-6bfe-4c2d-9063-b4ffbfb1ff81)


17. Then run exploit.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e3cd3b53-08b4-46f9-bf86-2382d8619bfd)


> RESULT


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9ad59386-b792-48c8-a066-3e3412e9c379)


> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/efd7a915-2fdf-4b00-87aa-871021235fac)


## ROOT FLAG

```
bd8f4a12e2ac0815ac63f48aafa5b860
```
