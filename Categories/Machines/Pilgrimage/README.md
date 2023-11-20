# Pilgrimage
> Write-up author: jon-brandy
## Lesson learned:
- ImageMagick LFI.
- git-dumper.
- 


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dfb8e16e-4ed7-4561-a81f-d29317b75673)


## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.219 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-27 23:37 PDT
Nmap scan report for pilgrimage.htb (10.10.11.219)
Host is up (0.051s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
| ssh-hostkey: 
|   3072 20be60d295f628c1b7e9e81706f168f3 (RSA)
|   256 0eb6a6a8c99b4173746e70180d5fe0af (ECDSA)
|_  256 d14e293c708669b4d72cc80b486e9804 (ED25519)
80/tcp open  http    nginx 1.18.0
| http-git: 
|   10.10.11.219:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Pilgrimage image shrinking service initial commit. # Please ...
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: Pilgrimage - Shrink Your Images
|_http-server-header: nginx/1.18.0
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.57 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.
2. Noticed based from the nmap result, /.git/ is found. We can dump that using **git-dumper** later.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7efd6bef-7ebc-4379-ad5f-cde52a4283e4)


3. Using **git-dumper**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/88e34d8d-17f9-42ce-9762-88e0b73bb743)


```
┌──(brandy㉿bread-yolk)-[~/Downloads/machine/machine_pilgrimage]
└─$ ls                  
assets  dashboard.php  index.php  login.php  logout.php  magick  register.php  vendor
```

4. After uploaded an image file, it shows us where it stores our image file.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/502576c5-935b-4606-9c58-ab56adc0cc76)


5. Well, analyzing **index.php** source code, shall found an interesting tool used by the webapp (ImageMagick).

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4ad6b78b-4722-454e-91ff-a04df08e9732)


6. Searching in metasploit for **Image Magick** shall resuulting to these:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fd001312-48fe-4886-ba14-9d879ac7931d)


7. Got bunch of results, searching on the internet shall found these:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c2274c43-9806-488a-8bf4-a48dabcdd7a4)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2c22af4a-a45d-44cd-a4a5-abb26235ef7a)


> CVE's POC --> https://github.com/voidz0r/CVE-2022-44268


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5989ddf0-3238-42cf-aeb0-f8276e5bda0c)


8. Quite promising, let's try use that CVE in metasploit -->  CVE-2022-44268

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/098ad4d4-0817-462b-a517-0d39870929b5)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8b064e7b-0bd5-40b2-b487-bbc729848071)


9. It seems we need to exploit this manually.
10. I did not want to use the CVE's POC we found before because it runs cargo.
11. Searching for another POC, found this POC where it uses python script --> `https://github.com/Sybil-Scan/imagemagick-lfi-poc`.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1704d401-9494-47d2-9d08-e9d342be8fee)


12. Let's just follow the steps listed there.

> RESULT


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/07f93215-ecfc-4a4d-b7af-cd3428f3e421)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/facd5578-f3fd-42cb-b1fd-dc65756df7bc)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/83a9a115-20f9-4ed2-97d5-527b16dc1953)


13. Running `identify -verbose 651533fa137a0.png` and scrolling down, shall found this hexes:


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d69cc67-0fa6-4637-b69a-c49ce75026e9)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/06e4e2fe-4f84-4aac-984d-817eaea774a3)


14. Great we found the foothold. Anyway we leaked a username --> `emily`.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6f3c0764-79ba-4f45-a12e-cb2f68b6e21d)


15. However because we're not in a webshell or a shell, we can't read .txt file, so there must be a creds somewhere we can use to login as emily.
16. But how come?? Here's the situation. We can read /home/emily/user.txt, and we just found out that the vuln is LFI not SSTI. That's why the approach must be hardcoded creds somewhere or reuse password scenario.
17. Remembering it's a webapp and we got the source code by dumping the `.git` vulnerability. Hence it's much easier for us to found where database might be located.
18. Reviewing login.php source code, found our potential interest.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7811c50d-7f16-4c3e-9a7c-27916436dfce)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/912da23e-fb4e-4916-a9d5-3a57da2dcf5c)


19. Running the same method as before by grabbing the hexes and decode them in Cyberchef, found this:


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ea3701b9-604a-4e3e-9c03-018b1f423a9d)


20. Great! After tried ssh login with `emily:abigchonkyboi123`, we logged in!

> RESULT


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5203e367-f992-420d-bfd1-f6053d68c204)


> GETTING USER FLAG


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ae2d2531-3028-4ded-aa01-c77d6a7eae14)


## USER FLAG

```
6779af2316ab81439521d378340a224d
```

21. When checking sudo permission for emily, sadly emily does not run sudo on pilgrimage.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c5272a64-e51b-44c7-b367-b3e35569b36a)


22. Running **linpeas.sh** we found this interesting result.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/08583d7e-34dc-4af3-996c-611dcfa97411)


23. Noticed 2 tools used here -> `inotifywait` and `binwalk`.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8e7741a5-67eb-418d-a120-4ccd2774c15f)


24. Reviewing the source code again, it looks like monitor newly created files in `/var/www/pilgrimage.htb/shrunk/` directory. The **monitoring** itself using binwalk and it auto deletes file which match with what defined inside the blacklist array.
25. So our foothold can be at binwalk.
26. Let's run **pspy64** to check whether the process is being run as root or not.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c13c9658-0a0e-4b24-8c34-43b146ba430d)


27. Great! Searching on the internet about binwalk exploit shall resulting to this --> `https://www.exploit-db.com/exploits/51249`.
28. The binwalk version itself does the same as the documentation.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5890061-468c-4680-b3b5-61c9d889aef1)


29. Great! Seems binwalk is indeed our foothold.
30. Searching on the internet for POCs found this --> `https://github.com/adhikara13/CVE-2022-4510-WalkingPath`.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b3fc8307-f307-42f5-8477-11db943a6976)


31. The github POCs itself referencing to another POC.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0d8295ab-ef29-4957-8cc6-9ef19578f7af)



![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7c5906ab-c33b-45b8-b85d-972da1145824)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2ac92000-bfa7-4ab2-94e4-e88ca9f4755c)


32. Let's use the **RCE_binwalk.py**.


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/26281827-ed8c-47a7-98c5-f9e1874f58a9)


33. Now download the newly created image file from the script --> `binwalk_exploit.png` to the remote server, then copy it to --> `/var/www/pilgrimage.htb/shrunk/`.

#### NOTES: Remembering there's a blacklist char, naming "gambar.png" shall safe.

> RESULT


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ebd5a634-ef1e-4785-8896-07220f4a9f1e)


34. Nice!

> GETTING ROOT FLAG


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/372d35c0-986f-4a8e-85d4-0c8e37e0c3ff)


## ROOT FLAG

```
bb8702d5c401f0995582469c48d7169e
```




