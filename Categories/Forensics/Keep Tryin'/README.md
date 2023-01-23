# Keep Tryin'
> Write-up author: jon-brandy
## DESCRIPTION:
This packet capture seems to show some suspicious traffic
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT - GOT A PCAP FILE

![image](https://user-images.githubusercontent.com/70703371/213477611-28eea42c-6d90-4355-9af5-403302ca0522.png)

![image](https://user-images.githubusercontent.com/70703371/213479041-fc738215-664a-4456-a343-69125eff7d07.png)


2. Notice there's 2 packets with `url-encoded`.
3. After open both, one of them have this encoded base64 strings.

![image](https://user-images.githubusercontent.com/70703371/213479222-812c30c6-046f-4e55-88b8-0f4c5c355379.png)


![image](https://user-images.githubusercontent.com/70703371/213479321-fee244ea-697e-4d44-bba4-09dec1cce1d8.png)


4. Hmm.. The DNS packets caught my attention here.
5. Let's try to decode this strings.

![image](https://user-images.githubusercontent.com/70703371/213479845-6d0ddc2e-5b67-4c51-84c4-3b78f144ba58.png)


> RESULT

![image](https://user-images.githubusercontent.com/70703371/213479945-1b9c58f6-b5e0-4106-b4bc-c6721fec33a3.png)


6. Now let's follow this request.

![image](https://user-images.githubusercontent.com/70703371/213480122-06d662a1-5a7f-4e1c-b62b-555b42f1e72d.png)


![image](https://user-images.githubusercontent.com/70703371/213480223-7e6b6e30-2eb7-4562-9c17-e2bfd4a107f0.png)


> OUR INTEREST

![image](https://user-images.githubusercontent.com/70703371/213480563-b996a98a-2438-410f-9199-bdc313f4846f.png)


7. When i pasted that on cyberchef, we got nothing.
8. Then, when i checking the packets, found a request sent to /flag.

![image](https://user-images.githubusercontent.com/70703371/214080864-386e5093-2387-4f64-8ba5-9cf7a362fcec.png)


![image](https://user-images.githubusercontent.com/70703371/214080908-7f3ebee0-f193-4dc4-b956-61862cda57dd.png)


![image](https://user-images.githubusercontent.com/70703371/214083462-16dd4a60-d510-4f09-bc45-6b59bf103e97.png)


9. Let's focus on the DNS packets here, based on the packets and results we got here, what comes to my mind is, we need to do **DNS Exfiltration**, but before use that approach, let's try to find an easy way to solve this (if there is).
10. Well the previous text we got must be base64 text, but there are `.` that got in the way and makes it looks corrupted.

![image](https://user-images.githubusercontent.com/70703371/214082790-bb75be24-5682-42dc-9a91-9c5608798791.png)


11. Let's remove the domain name and the `.` also the text behind it (first) and in front of it (last).

> RESULT

```
0ejXWsr6TH-P_1xkEstaVwi7WDy8AcxufnGotWXH3ckb2Lh5A-qFljIWOAOLUS0?T1W8P4CpiCZbCM7_QKcv-r0JG29RpsyYY5YkZRxo7YDIYUJpHlGgxu5PWV1G_DA?KNrmnrktfbeDgzcpPJBjPTeMYx3Qs1Q6bAuFhROWXemJ80gPTYIz0xl8usJQN3m
```


11. Well i tried to read the forum and found out that sometext related to `RC4` (?)
12. What comes to my mind is let's add RC4 to the cyberchef and use `TryHarder` as the key.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214084187-233be9c2-81fd-46d0-b5a4-272b9ffaec45.png)


13. Great! Based from the header we know it's a zip file.

> HEADER

![image](https://user-images.githubusercontent.com/70703371/214084594-c85a9756-53ff-4cc5-8be2-e176b65bb2ab.png)


```
https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html
```

14. Let's add unzip.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214084815-5e57c4be-b238-42d5-9a8d-1d79770c3691.png)


15. One file found.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214084900-60f8d193-7cde-4056-97e6-3842940918cc.png)


16. Got the flag!


## FLAG

```
HTB{$n3aky_DN$_Tr1ck$}
```

