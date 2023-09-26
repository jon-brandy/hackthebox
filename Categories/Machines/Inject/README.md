# Inject
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/badbc336-8df3-4625-b604-12ca012c8b9a)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.204 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-26 04:39 PDT
Nmap scan report for inject.htb (10.10.11.204)
Host is up (0.065s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 caf10c515a596277f0a80c5c7c8ddaf8 (RSA)
|   256 d51c81c97b076b1cc1b429254b52219f (ECDSA)
|_  256 db1d8ceb9472b0d3ed44b96c93a7f91d (ED25519)
8080/tcp open  nagios-nsca Nagios NSCA
|_http-title: Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.33 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/18855496-990c-492c-825c-109b1ea4644b)


2. Long story short, of all the existing features this website have. Only upload feature which could be our foothold.
3. When I tried to upload a ELF file, it showed this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/112575ec-8f40-4b71-83e6-171fe53fc405)


4. It does validate the extension file uploaded but does it sanitize the contents??
5. This could be our foothold. Anyway let's try to upload a normal image file there.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e72d5d5c-6d6a-491b-ba12-8eecd27ada69)


6. Interesting! We can view it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7fc88b50-5f42-4114-be89-e9d0fdc0f1a5)


7. Great! More interestingly there's a URL parameter! We can send our reverse shell and access it to trigger it.
8. But anyway based from the wappalyzer info the webapps seems can't execute any file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4b21490e-e7c2-4012-ab4c-b23895dd0424)


9. And we don't know whether it sanitizes the image content or not.
10. Anyway, found a `File Traversal` vuln when capturing the request using burpsuite and changing the parameter value.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/833033a0-4f0e-4a11-b02c-dff45dbf7f74)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/42acb84c-42b9-412f-8f93-5748e4ac10e4)


11. Succeed access /etc/passwd. Great! This means we can access the user directory and get the user flag there.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5c71ee41-1931-4839-a588-fe3707403df0)


12. Found 2 users, let's see which one has the user flag.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cb963b88-6bc2-42e9-a250-82b6ba08faf5)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c1458e84-d17f-4342-afd7-c5cfe45a0b33)


13. Found the user flag at **phil**, but the web browser can't read the user.txt file.
14. Going back to **frank** directory and checking `.m2` directory, we found a file named **settings.xml**, opening it shall resulting to this:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/588b0f85-3f14-41f3-b288-717d744655fa)


15. Noticed there's a cred hardcoded there.
16. Anyway can't login to phil and frank using that password.
17. Then I go to `var/www` to see if there's any interesting directories or files inside it.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5a935911-b8be-4a54-9f12-6f3e8d15c0a5)


> FOUND NOTHING IN HTML

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/967fae62-dd94-4785-b9db-4437abb39498)


> FOUND FILES IN WEBAPP DIR

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a1ca30cd-44bb-49b8-9364-3c6ca1d819ef)


18. Checking **pom.xml** which covering about **spring framework** we can see the web version.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/40f83c6b-64c9-48b3-a67c-f55a950fb587)


19. Great! This shall helps us find CVEs.
20. Diving in the internet found 2 CVEs close to this --> `CVE-2022-22965` and `CVE-2022-22963`.
21. Analyze further the **poc.xml** shall realized the CVE for this challenge should be --> `CVE-2022-22963`. Because there's several things not there to use `CVE-2022-22965`.
22. Checking the metasploit, the targeturi seems at `/functionRouter`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ecb48e81-8ecf-4212-8aa3-3e53c74e9db6)


> USING METASPLOIT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/00deb14f-45c8-41a5-ac95-661cd0dbf4d5)


23. This time I tried to change to phil using the password we failed to use at ssh before.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/78af3178-61ea-43a8-8703-77c6db813b3c)


24. Turns out we succeed! Confused why failed before.

> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8b7c7463-3f0a-44cf-ad9d-27560363150a)


## USER FLAG

```
fc6d1634e2f5babf342a0cf22ac541bd
```

25. Run --> `python3 -c 'import pty;pty.spawn("/bin/sh")'` so we can check sudo permission for phil.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3386bf5c-8d74-4c7e-b3a1-29c08e19e919)


26. Sadly we can't, let's use linpeas to check whether there is files or directories we can use to escalate our privilege.

> RESULT


