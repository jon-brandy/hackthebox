# Chase
> Write-up author: jon-brandy
## DESCRIPTION:
One of our web servers triggered an AV alert, but none of the sysadmins say they were logged onto it. 
We've taken a network capture before shutting the server down to take a clone of the disk. Can you take a look at the PCAP and see if anything is up?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209457506-194ba11c-78d7-42d0-b5bd-80b616efd0b5.png)


2. Now open the `.pcapng` file in wireshark.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209457561-d792df82-78c0-4061-91c3-f359776d8711.png)


3. Let's follow the `tcp` stream.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209457579-dab7185c-7122-4cef-83ab-2fbd862643d6.png)


4. Based on it we can conclude that the webserver IP Address is `22.22.22.5`.
5. We know that the attacker uploaded a webshell (?) with the authKey=admin.

![image](https://user-images.githubusercontent.com/70703371/209457664-4bb0f69c-aeca-4371-ac0f-b169510433db.png)

![image](https://user-images.githubusercontent.com/70703371/209457672-3f674fe1-46c2-4e3c-9a73-c8a414a1bfd7.png)


6. Next, the attacker executed a command line.

![image](https://user-images.githubusercontent.com/70703371/209457707-8266ea5b-4c2b-4a92-a50c-5a1e06151644.png)


7. Then download the **netcat.exe** via `certutil`.

![image](https://user-images.githubusercontent.com/70703371/209457720-fe679898-9872-4b6b-b463-a50d17c4c2e7.png)


8. Now let's follow this TCP stream.

![image](https://user-images.githubusercontent.com/70703371/209457751-67c5e868-c3f1-4749-b6a9-2259a5976a1d.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/209457758-1d0be9fc-1c35-4b93-9cee-d8ae22070036.png)


9. Based from it, we know the attacker executed **whoami** and **ipconfig**.
10. Then the attacker upload a `.txt` file twice.
11. By using **powershell** and **certutil**.
12. To see what's inside the `.txt` file, i filtered the tcp stream to 5.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209457808-d39e1ea4-b594-4c17-a941-f3873c44338a.png)


13. Nothing interesting from the inside.
14. I kind of lucky, because i think the filename is look like a encoded text (?)
15. I pasted the text to cyberchef and got this result.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209457861-66b5ce62-ebf8-48cf-97a5-bb9aa8c470f2.png)


16. Turns out the text is encoded in base32.
17. Got the flag!

## FLAG

```
HTB{MAn_8lu3_73aM_R0cX}  
```



 
