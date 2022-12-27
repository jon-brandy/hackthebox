# baby nginxatsu
> Write-up author: jon-brandy
## DESCRIPTION:
Can you find a way to login as the administrator of the website and free nginxatsu?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209687786-96ac8eda-3095-46c2-941b-ef975cd742c7.png)


2. Let's try to create new account.

![image](https://user-images.githubusercontent.com/70703371/209688548-a28a86d9-bff7-463c-aabe-83f4b66f7a21.png)


3. Input the name & pass as `admin`, the email as `admin123@gmail.com`.
4. Now login with that creds.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209688707-d3f7274b-8ab7-4ae0-be05-8d0e9d81bc70.png)


5. Let's click generate config.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209688952-3ea8da1c-3b1b-4e59-a0c1-2d407288f39f.png)


6. Click the config.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209688998-a1b80883-41c5-418a-ba9a-95320be5b750.png)


7. The comment caught my attention here.

![image](https://user-images.githubusercontent.com/70703371/209689039-a4e0bab4-f38d-4b1c-8d44-9fee343f60f2.png)


8. Now add `/storage/` at the url.

```
http://142.93.37.215:30822/storage/
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209689251-f10000b3-51b8-4563-97f3-5374575c24fd.png)


9. Hmm.. Let's check the bottom one.

![image](https://user-images.githubusercontent.com/70703371/209689297-f7d7a844-633d-4861-b849-1db47fa3b101.png)


![image](https://user-images.githubusercontent.com/70703371/209689536-c63cf044-30e2-44ed-bcf0-1fb29576d52f.png)


10. Let's download the file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209689598-cf9162b4-19a5-45c6-89f6-dd5b2560268b.png)


![image](https://user-images.githubusercontent.com/70703371/209689635-397ec4e8-557d-4309-a298-65eab2a78ae7.png)


![image](https://user-images.githubusercontent.com/70703371/209689654-181fd960-0037-46bf-a044-2a2989b81c19.png)


11. Since it's a sqlite database, we can use online [tools](https://sqliteviewer.app/) to view the data.

> RESULT - OPEN "USERS" TABLE

![image](https://user-images.githubusercontent.com/70703371/209690234-a233033a-ae96-4488-9981-0b09b1df49ef.png)


12. Check the hash algorithm used for jr's password. To copy it, click this symbol first.

![image](https://user-images.githubusercontent.com/70703371/209690603-5f325214-70ac-43ec-8909-eda641558d94.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/209690626-ac8bed95-12c4-430e-a830-601d2c40eb6b.png)


13. 

