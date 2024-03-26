# CandyVault
> Write-up author: jon-brandy

## Lessons Learned:
- Source Code Review.
- Basic NoSQL Injection.

## DESCRIPTION:
The malevolent spirits have concealed all the Halloween treats within their secret vault, 
and it's imperative that you decipher its enigmatic seal to reclaim the candy before the spooky night arrives.

## HINT:
- NONE

## STEPS:
1. In this challenge we're given the source code which we will review later.

> WEB APP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ac08c716-07c9-4132-a45a-bf01337fca53)


2. Seems there is no register option, hence the objective might be to bypass the login page.
3. Upon reviewing the source code, seems after successfully bypass the login page, the webserver shall renders **candy.html** page and the flag shall rendered there.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/227bfe0b-a196-42f0-9008-e69a23a71608)


4. Great! Now let's identify what DB type it used so we can choose the correct SQLi payload.
5. Reviewing the **config.py** file, we can identify that the webserver using `MONGODB`.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d95bd337-9212-4d9b-8ecf-f9c40f1acd54)


6. Next, reviewing the **migrate.py** source, it's clear that the DB used is MONGODB.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3eca6a77-1b5a-461b-9713-f86d585ebf9c)


7. Searching on the internet for nosql payload, found these results.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8457370d-d755-4eef-a538-b9d024e0dbdf)


8. Nice! Let's try to intercept the request using burpsuite then change the value for email and password.

> IN BURPSUITE

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a43defca-58c1-4538-91a0-fd846d7b1221)


9. Noticed the input format is not in JSON, hence we need to manipulate the **content-type** header.
10. And used this payload:

#### NOTE:

```
Change the JSON paramater --> username, to email.
```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/27ea8847-05f5-4d01-b462-583a5944b024)


> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a9370c11-81ef-4210-a9d4-7d8c4dd24b38)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/6b0fde17-dfc5-49f9-b2a7-44f4cebee7bb)


11. Got the flag!

## FLAG

```
HTB{s4y_h1_t0_th3_c4andy_v4u1t!}
```

## IMPORTANT LINKS

```
https://book.hacktricks.xyz/pentesting-web/nosql-injection
```
