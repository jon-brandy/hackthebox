# Shoppy
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's check all open ports and it's services from the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211156757-ffc29c1e-ca8b-4356-81d9-e57e9f4fefdc.png)


![image](https://user-images.githubusercontent.com/70703371/211156772-35992686-8ca0-4af9-a7aa-bb1ae5b67907.png)


![image](https://user-images.githubusercontent.com/70703371/211156783-c2a9d9e4-edd5-4584-9e05-96a3fa631fe1.png)


![image](https://user-images.githubusercontent.com/70703371/211156792-6d339608-4cf9-4200-956a-51d2978c037f.png)


2. Based from the open ports. We know the machine is running a web application and there's port 9093 which has **copycat** service.
3. I did a small outsource about **copycat** service. Turns out it's a database replication service.


![image](https://user-images.githubusercontent.com/70703371/211157148-a3c8ae69-154d-430b-917e-97ccd2e1fb3a.png)


![image](https://user-images.githubusercontent.com/70703371/211157611-b22b085b-9482-4baa-b626-370ec4c0f8d4.png)



4. In general the data stored in JSON format, hence we know the vuln here is `no sql injection`.
5. Let's run **gobuster** to see all availables directories and files.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211157918-7e05df5a-a458-4016-b0e7-8cfb1074b208.png)


6. Actually we got many directories and files, but we only can open the `admin`, `Admin`, `login`, and `Login`.
7. All of it leads to this webpage.

![image](https://user-images.githubusercontent.com/70703371/211158015-f32866a9-fa8f-478b-a1d1-e6ee06808edd.png)


8. Since we already know the vuln is `nosqli` i use [this](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection) as my references.
9. Let's enter both username and pass as `admin'||'1==1'`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211158093-b48d31fe-f077-49aa-92f7-b4e02010eca4.png)


10. Now click the `search` button.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211158165-fb6cb2d3-dc0e-4458-9c22-d419630a1dbf.png)


11. Enter the same input as before to textbox.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211158191-d1ea9092-a6a0-4e47-b598-47009e27a9a2.png)


![image](https://user-images.githubusercontent.com/70703371/211158201-f586b991-61d5-4bce-8f94-87e044cb8322.png)


12. When i tried to cracked the admin's hash, seems the plaintext is not leaked in the internet. Then i tried for `josh`. Got this:

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211158641-d0655d32-dd09-4d98-946e-dc5ccb46ad25.png)


13. I tried to login ssh with josh as the username and the password as the plaintext we cracked.
14. But it says wrong password.
15. Let's use another approach.
16. Maybe let's use `fuff` to checks if there are any subdomains available.

```
ffuf -u http://shoppy.htb -H "Host: FUZZ.shoppy.htb" -w /usr/share/wordlists/SecLists-master/Discovery/DNS/bitquark-subdomains-top100000.txt -mc all
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211184219-9d499667-64d4-4315-97f6-b9911d1446d2.png)



17. Since there's many responses with size of 169. Let's filter it.

```
ffuf -u http://shoppy.htb -H "Host: FUZZ.shoppy.htb" -w /usr/share/wordlists/SecLists-master/Discovery/DNS/bitquark-subdomains-top100000.txt -mc all -fs 169

-u -> stands for target URL
-H -> stands for header.
-w -> stands for wordlist file path.
-mc -> stands for match http status code.
-fs -> stands for filter http response size.

```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211184255-429d8b8f-503b-406f-96a1-130a5c6fd4d3.png)


18. Got it!
19. Now place the subdomain to `/etc/hosts` first, then open it on the web browser.

> ON THE WEB BROWSER

![image](https://user-images.githubusercontent.com/70703371/211184365-e5b45f9c-220f-48e7-b05c-4ca0fe604e8d.png)


20. Now let's enter `josh` creds.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211184404-80d11564-9a2b-4f05-a474-26c78bbc5a49.png)


21. It looks like we have another username here.

![image](https://user-images.githubusercontent.com/70703371/211184425-7be4abe0-da8d-43c1-8e9c-a9a71aef931b.png)


22. Let's check every channels here.

![image](https://user-images.githubusercontent.com/70703371/211184450-3961c296-c0d1-4e7c-97eb-6707435dd859.png)


23. Got a creds at `Deploy Machine` channel.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211184468-1fd3a951-c8c1-41e6-bca0-d86e7be070e3.png)


24. Let's try **ssh** to login now.

```
username: josh
password: Sh0ppyBest@pp!
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211185372-2a85a52f-f126-4326-b0d1-fff33fd90eb4.png)



![image](https://user-images.githubusercontent.com/70703371/211184512-0d4e95ae-f62d-43ac-b6ac-c6a00ab1e880.png)


![image](https://user-images.githubusercontent.com/70703371/211184558-e6dfb4e7-df2a-483b-9152-f69b42228c25.png)


![image](https://user-images.githubusercontent.com/70703371/211184566-03584828-22cf-4f7b-9054-d9c012869f1e.png)


25 Got the user flag!

## USER FLAG

```
ad6c565914c1420ed389310014cd19c1
```


26. Let's find the root now.
27. Go back twice, then jump to the root directory.

> GO BACK TWICE - RESULT

![image](https://user-images.githubusercontent.com/70703371/211184711-d1f6459c-fdca-4603-9f5c-250fe2debfb7.png)


> THE ROOT

![image](https://user-images.githubusercontent.com/70703371/211184744-9d14dd3d-9d9c-4860-a065-e1aed1f11d1a.png)


28. I already tried `sudo su` and obviouly we can't do that in ssh mode.
29. Remember there's `deploy` directory inside the `home` directory, let's jump there.

![image](https://user-images.githubusercontent.com/70703371/211184814-76055ce6-95b2-43fb-b0e4-6fd046632104.png)


![image](https://user-images.githubusercontent.com/70703371/211184825-0c68b57c-d400-4a54-b15c-b51438c54591.png)


![image](https://user-images.githubusercontent.com/70703371/211184836-e1884eeb-7fff-4bf5-a93c-dcd5c8b6d804.png)


30. Can't cat the creds, notice there's an executeable binary file.

![image](https://user-images.githubusercontent.com/70703371/211184847-e4acc254-f673-44c2-94c3-2da18187e2f7.png)


31. Let's try to run it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211184851-52c6a90e-8a90-4fa9-9f52-c77afe5930b2.png)


32. Cat it then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211184878-8db2afd6-8a8c-4f4f-b9d9-a3865e3b110b.png)


33. Hmm.. got a password there (Sample).
34. I think we need to find a way to run the binary.
35. Well the logic here is, the username to run sudo mode must be `deploy` (because we're in the "deploy" directory, not in "jaeger" directory). 
36. However, remember this warning:

![image](https://user-images.githubusercontent.com/70703371/211185111-6c0aca0f-5d0b-4c9e-a0fd-da2aa5ff5e41.png)


37. Hence we need to run the sudomode for `deploy` using this command:

```
sudo -u deploy /home/deploy/password-manager
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211185175-5b10073b-2777-4385-a0ee-a52a39441d7d.png)

> GREAT! Now enter the pass we found before when cat the binary -> Sample.

![image](https://user-images.githubusercontent.com/70703371/211185236-439e56cf-041c-4cc0-bb45-b1a0c3db5adb.png)


38. Nice! Got the creds. Let's login as "deploy" via ssh.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211185274-5d7d1107-dd08-4049-871a-f4a4758559e4.png)


![image](https://user-images.githubusercontent.com/70703371/211185292-14188fe5-096a-4154-9292-94f5251f8113.png)


![image](https://user-images.githubusercontent.com/70703371/211185382-def4ac8f-d23c-4a21-9ac4-9d0d599ca619.png)


39. Notice when i enter `id`. It seems we are in a docker container.
40. To get into the root mode. Let's enter `bash` first.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211185447-a6a41396-26a7-4f3f-adba-eb5b95614f71.png)


41. Then i did a used [this](https://gtfobins.github.io/#) website to search about docker command that gets us a root shell.

![image](https://user-images.githubusercontent.com/70703371/211185498-a201ce6c-f76b-417e-b136-780e1176e5d8.png)


```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```


> RESULT

![image](https://user-images.githubusercontent.com/70703371/211185516-cb2d9fdc-31fb-4028-ba35-de8923cbf343.png)


![image](https://user-images.githubusercontent.com/70703371/211185525-42e27219-7081-4051-b884-bc318e403ead.png)


42. Got the root flag!


## ROOT FLAG

```
66ca567a8cf4694e15ce2a52f9466d34
```


## LEARNING REFERENCES:

```
https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection
https://gtfobins.github.io/#
```
