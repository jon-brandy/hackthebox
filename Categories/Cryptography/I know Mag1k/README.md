# I know mag1k
> Write-up author: jon-brandy
## DESCRIPTION:
Can you get to the profile page of the admin?
## HINT:
- NONE
## STEPS:
1. Open the host given.

> RESULT - login page

![image](https://user-images.githubusercontent.com/70703371/212724640-768390d1-47f0-4874-b91b-efa03dd38637.png)


2. Since we don't have any creds, let's try to register and login.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212725291-69e814d9-60ad-462a-807b-9f23c3ad0e5e.png)


3. There's nothing interesting here, so i tried to check the cookies storage.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212733561-8b573d58-fa4e-4d4d-b207-9f48f73a96bc.png)


4. When i tried to decode the mag1k cookie, got random text.

![image](https://user-images.githubusercontent.com/70703371/212733458-5633e3d6-9937-408e-9584-9f866a534130.png)


5. Since i stuck here, i read the forum and found out the challenge related to `padding oracle` attack.
6. Hence, i tried to use **padbuster**.

```
padbuster http://188.166.148.162:32617/profile.php 9gH0dY2dcbIcTGya8Oe08osnxYExeoXx4ZnLS1hltFWNxYCJ2hWTdQ%3D%3D 8 -cookies iknowmag1k=9gH0dY2dcbIcTGya8Oe08osnxYExeoXx4ZnLS1hltFWNxYCJ2hWTdQ%3D%3D
```

> RESULT

