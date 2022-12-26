# sanitize
> Write-up author: jon-brandy
## DESCRIPTION:
Can you escape the query context and log in as admin at my super secure login page?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209567760-bef767ed-2e37-45fd-a506-213a613a7d5a.png)


2. Based from the `html` title, let's try to inject simple Sqli payload.
3. Input the username as `admin'--` and the password as `admin'--`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209567852-9d9b35d4-506e-4b44-afbf-ad3622832b10.png)


4. Got the flag!

## FLAG

```
HTB{SQL_1nj3ct1ng_my_w4y_0utta_h3r3}
```
