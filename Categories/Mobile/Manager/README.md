# Manager
> Write-up author: jon-brandy
## DESCRIPTION:
A client asked me to perform security assessment on this password management application. Can you help me?
## HINT:
- NONE
## STEPS:
1. After installed the apk and opened it, enter your host then intercept the request you send at the login page.

> INTERCEPT USING BURP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/560be545-6474-4322-bc41-77822acef9ed)

> REPEATER

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/869047cc-a44f-4f98-a923-0af9c15ab141)


2. Let's create a user then.

> CREATING USER (REGISTER)

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/859a7b5a-f716-4ae2-b8cf-4ba521c07b30)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/a91e7a13-02bd-4515-86d1-b44e0649ec4d)


3. Great at the response tab we can see our role and id.
4. This could be IDOR vuln, but there's no id parameter at the request.
5. After logged in, we have an `update` feature which we can utilize to change other user password by their id, if there is id parameter when we do update request.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ebfef68a-a3af-4900-b41f-7cd697482898)


> DO REQUEST - Opened manage.php - turns out there is no id param.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/66e9f433-cdd4-40d6-8689-0e24b32eba04)


6. Stuck for a while until i tried to register a username `admin` and it says `username already taken`.

> CREDS ENUMERATION VULN

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bff4f3b1-517f-4457-a813-e45616fcb3c9)


7. Knowing this, let's try to change the password again but this time change the username as admin and the password as random strings.

> Do login again using the account we've made before and intercept request for update account.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/c8d725df-d2b7-46b6-ba1c-d4d1cc8640f2)


8. Great! Now let's do login again.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5d8b9bc7-97d8-48b9-a43a-a9204216ef0c)


9. Got the flag!

## FLAG

```
HTB{b4d_p@ss_m4n@g3m3nT_@pp}
```

