# Downgrade
> Write-up author: jon-brandy
## DESCRIPTION:
During recent auditing, we noticed that network authentication is not forced upon remote connections to our Windows 2012 server. 
That led us to investigate our system for suspicious logins further. 
Provided the server's event logs, can you find any suspicious successful login? To get the flag, connect to the docker service and answer the questions.\
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212055814-facb3757-c6f9-4a87-95e4-9e072d943ebf.png)


2. Hmm.. Let's run the host given using netcat.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212055984-6bc85c32-0896-4824-bb8f-dfe578f20f0b.png)


3. It seems we need to enumerate the log file to find the correct answer, let's open the event log file using event viewer
4. Based on the question asked, let's open event log file related to it, found event log `security`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212056906-66b596d9-1f6a-479d-a3fc-90ed424da252.png)


5. Yep got it right, let's answer `security`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212057062-4663cfaf-319c-4293-905b-b9752d15afab.png)


6. Notice, we can traverse this:

![image](https://user-images.githubusercontent.com/70703371/212057743-d9577352-448a-4adb-908a-5abe710d717f.png)

![image](https://user-images.githubusercontent.com/70703371/212058016-761330b8-e421-45d8-baa2-04f7a72fbc28.png)


7. Since it's about successfull logon, then we need to search about **successfull logon**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212058262-5906a8df-dcbb-464f-893a-7b443d1fb214.png)


8. This should be the correct one, because the example ans is an id, let's enter the event id.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212058430-bb028a83-0cf0-41a7-8285-c9c63310b45d.png)


9. To answer this question, scroll down and you'll find this:

![image](https://user-images.githubusercontent.com/70703371/212062334-aeb28320-f68e-4e73-b4cc-a6cf0e90939c.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/212062375-ae5925e4-f3ec-4082-bba3-215a314e8353.png)


10. Let's search authPackage that stands out different.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212062870-7ac0d514-9e0c-4224-9275-6834c08dfdf2.png)


![image](https://user-images.githubusercontent.com/70703371/212062915-8a42247c-8345-48a7-b221-40705f9f4bd4.png)


11. When i traverse again, found this one:

![image](https://user-images.githubusercontent.com/70703371/212064751-a5cfb728-e554-483d-840e-c82bb2fe220e.png)


![image](https://user-images.githubusercontent.com/70703371/212064814-1e46620d-1f0d-4c9d-8147-ec0c82991f5f.png)


![image](https://user-images.githubusercontent.com/70703371/212065020-5cff5216-5a6c-4dc8-b324-444bf7e786b4.png)


12. Let's enter `2022-09-28T13:10:57`. The reason i put 15, because i'm in Indonesia and the time stamp is 7 hours ahead, so i need to reduce 7 hours.

![image](https://user-images.githubusercontent.com/70703371/212065938-df70cbcb-e877-4677-9453-e1123804bb0a.png)


13. Got the flag!

## FLAG

```
HTB{34sy_t0_d0_4nd_34asy_t0_d3t3ct}
```

