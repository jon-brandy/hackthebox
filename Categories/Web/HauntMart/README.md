# HauntMart
> Write-up author: jon-brandy

## Lessons Learned:
- Source Code Review.
- Bypassing SSRF Filter (filter for localhost IP usage).
- Execute Server-Side Request Forgery.

## DESCRIPTION:
HauntMart, a beloved Halloween webstore, has fallen victim to a curse, bringing its products to life. 
You must explore its ghostly webpages, and break the enchantment before Halloween night. 
Can you save Spooky Surprises from its supernatural woes?.

## HINT:
- NONE

## STEPS:
1. In this challenge we're given the source code of the webapp.

> WEBAPP

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/34f4b839-23ec-46bf-af6f-dd4df4a658d8)


2. Noticed there's a register option, hence the objective is to not bypass the login page or achieved admin role with bypassing the DB logic.
3. Upon registering an account, we're redirected to `/home` endpoint.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cbca3127-57f4-48e1-b571-d12a1c0c896b)


4. After clicking every available feature, turns out only one feature accessible. The sell product.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f4536a13-c409-4e82-8e34-a7f86cdc1a47)


5. Interesting! Let's review the source code handling the logic behind this endpoint.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/501b0644-6440-459b-8aa0-399958c4314f)


6. The first step involves employing the @isAuthenticated middleware, followed by an endpoint that anticipates a JSON body containing specific keys.
7. Subsequently, the `downloadManual` function is invoked, taking the manualUrl value from the JSON body as an argument.
8.  Should this call yield a False result, the request is halted with a status of 400.
9.  Conversely, if it returns True, the addProduct function is triggered, accepting parameters such as name, description, and price. Upon successful execution of this function, the request is terminated satisfactorily.
10. Let's review the `@isAuthenticated` middleware code.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/884edfc9-743c-4161-a725-62ebfb0337c9)


11. Based from the code, the middleware checks if a session token exists. If it does, it verifies it and passes the user information to the decorated function. If it does not exist, it returns a 401 HTTP error indicating unauthorized access.
12. Next, let's review the `downloadManual` function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/96f81287-2dac-4539-bbe7-8094a200d9de)


13. This code, checks whether the url does contain a blocked host, then it returns false. Otherwrise, it makes a request to the specified url.
14. Let's review the `isSafeUrl` function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/28678127-40ce-4fbf-8b71-698c17d0dc60)


15. It filtered for localhost, interesting.
16. Reviewing the other code, found a code that to make an admin user and seems the flag shall rendered if our role is admin. The flag itself shall rendered at the `/home` endpoint.
17. The `/addAdmin` endpoint should be our interest.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/8bf9e14a-22f2-42b9-982f-6d27c1d03a31)


18. Noticed there is a middleware called --> `@isFromLocalhost`, which handle that the `/addAdmin` endpoint is only reachable from localhost request.
19. However, noticing there is a filter which blocks several localhost form, it's not quite robust. We can easily bypass it using `0`.
20. Seems now we're clear, the objective for this challenge is to do **Server-Side Request Forgery**.

```
Manual URL:
http://0:1337/api/addAdmin?username=vreshco
```

#### NOTES:

```
- Remember to use port 1337, based from the Dockerfile, that port is reachable.
Also the run.py code specified that the port for localhost is 1337.
- WHY adding /api/ at the manual URL? Because /addAdmin endpoint is one of api.route.

api = Blueprint('api', __name__)
...
...
...

@api.route('/addAdmin', methods=['GET'])
@isFromLocalhost
def addAdmin():
    username = request.args.get('username')
    
    if not username:
        return response('Invalid username'), 400
    
    result = makeUserAdmin(username)

    if result:
        return response('User updated!')
    return response('Invalid username'), 400

```

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9fa01f07-167b-4c09-9727-28b4d5280d42)


![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cc755798-60fa-4975-9343-26a89812c9c5)


> EXECUTION

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f3fa1fa6-70b5-4438-af62-00ffe2feb12d)


21. Great! Now logout then login again, our user account shall upgraded to admin.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ac2782f6-5dc1-4fce-90dd-9a5c0480f0f5)


22. Got the flag!

## FLAG

```
HTB{s5rf_m4d3_m3_w3t_my_p4nts!}
```
