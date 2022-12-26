# baby auth
> Write-up author: jon-brandy
## DESCRIPTION:
Who needs session integrity these days?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568013-d2099f8e-d51d-48a2-b459-29cb003af21e.png)


2. First, let's try to input simple SQLi payload.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568134-a82029fc-de23-478a-9bf8-c42249914fcf.png)


3. Hmm.. Let's register account then.
4. Input both username & pass as admin.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568180-e497bcf1-de7a-4c10-a684-9e94fd505d3d.png)


5. Let's create account, with both username & password value as `hi`. Then login.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568315-3f80db0d-ea83-4114-99c5-54fb9e4b5b6c.png)


6. Now to bypass the login page, let's get our cookie by run `document.cookie` at the console.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568435-d02f74db-e1e8-438a-b153-f3d57ecf155b.png)


7. Copy our cookie then decode it using `base64` encoding.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568549-845df6dd-91b3-473a-adb0-5cb7c9b129f1.png)


8. Now change the username value as admin. Next encode it with `base64` then add `urlencoding`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568659-b2d94644-05ea-474d-9aac-ba56f17ac52e.png)


9. Now copy the cookie and set it as our cookie value.

```
document.cookie="PHPSESSID-eyJ1c2VybmFtZSI6ImFkbWluIn0" 
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568837-5cd11809-0375-4ea1-9468-6f94e66591d1.png)


10. Refresh the page.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209568876-ae3fde2e-f0d8-4170-9757-24f1dd7820b3.png)


11. Got the flag!

## FLAG

```
HTB{s3ss10n_1nt3grity_1s_0v3r4tt3d_4nyw4ys}
```
