# Insider
> Write-up author: jon-brand
## DESCRIPTION:
A potential insider threat has been reported, and we need to find out what they accessed. Can you help?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210196671-25e60442-4b18-44fa-9b8c-e42a12465ece.png)


![image](https://user-images.githubusercontent.com/70703371/210196684-3ac7554c-1357-422d-ab92-1f0484aa6850.png)


![image](https://user-images.githubusercontent.com/70703371/210196691-a2494275-6967-458c-8b40-9c58d41565e5.png)


2. Notice we have few .sqlite database and there's cookies.sqlite database inside the `2542z9mo.default-release` directory.
3. Let's open that database using `DBbrowser`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210198555-730b02d0-4fa1-417d-a6d6-f7919d03a397.png)


4. Hmm.. Got nothing interesting here.
5. Let's see if there are any other files that can be our interest.
6. Let's check the `login.json`.

![image](https://user-images.githubusercontent.com/70703371/210198681-8f8933de-0617-45a4-91bf-31a4e0377a3c.png)

> USE PRETTY PRINT

![image](https://user-images.githubusercontent.com/70703371/210198754-7797f844-61ba-4e1a-9a14-0ceb6ff60e98.png)


```json
{
  "nextId": 2,
  "logins": [
    {
      "id": 1,
      "hostname": "http://acc01:8080",
      "httpRealm": "Tomcat Manager Application",
      "formSubmitURL": null,
      "usernameField": "",
      "passwordField": "",
      "encryptedUsername": "MDIEEPgAAAAAAAAAAAAAAAAAAAEwFAYIKoZIhvcNAwcECF+d3kuwB9ZWBAj5QRmuUB+gqg==",
      "encryptedPassword": "MEIEEPgAAAAAAAAAAAAAAAAAAAEwFAYIKoZIhvcNAwcECBqsTKru3+k8BBgCXKb5CRSS4SF6O3Dh4jUKFRBtxfiabQk=",
      "guid": "{69f06e46-1ffa-42a0-9166-0ca4b8fac057}",
      "encType": 1,
      "timeCreated": 1604509320314,
      "timeLastUsed": 1604509320314,
      "timePasswordChanged": 1604509320314,
      "timesUsed": 1
    }
  ],
  "potentiallyVulnerablePasswords": [],
  "dismissedBreachAlertsByLoginGUID": {},
  "version": 3
}
```

7. Stuck here, so i did a small outsource about this, found out that we can use **firefox_decrypt.py** to decrypt the password.

```
firefox_decrypt.py github link

https://github.com/unode/firefox_decrypt
```

> PAYLOAD

```sh
python3 firefox_decrypt.py foren/Mozilla/Firefox/Profiles/2542z9mo.default-release
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210199398-e6374758-1d9c-4520-b80c-7a6462ecbd7b.png)


8. Got the flag!

## FLAG

```
HTB{ur_8RoW53R_H157Ory}
```


