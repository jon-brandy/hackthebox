# Under Construction
> Write-up author: jon-brandy
## DESCRIPTION:
A company that specialises in web development is creating a new site that is currently under construction. Can you obtain the flag?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/210695249-a0047975-519f-4265-b447-5552c223b59f.png)


2. Let's try with simple sqli.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210695761-c8be0828-3ed5-4ed2-b312-d63c3a62ce54.png)


3. Let's choose **register** then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210696037-fe5b590e-0ef7-4fb8-a03d-f4a82457eb5e.png)


![image](https://user-images.githubusercontent.com/70703371/210696064-847bee50-7860-4ce5-b51f-49a4a9364a39.png)


4. Hmm.. let's check our cookies then to see if we can get any clue.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210696419-4dbfc61e-b6de-4217-ad1a-a1ee6c9557f3.png)


5. Seems like it's a JWT token. Let's open with [this]() online tool.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210696572-f3ea875e-33c6-4851-bf83-82ceb5206f13.png)


6. Based on it, we know that this is an asymmetric JWT token (using private & public keys instead secret key).
7. So i did a small outsource about JWT token vulnerability, found out that we can do **JWT Key Confusion Exploit**.

> NOTES

```
JWT Key Confusion Exploit is an attack that simply using the pub key as our new signing secret key.
```
