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


9. Well based on the packets we got and the approach we've done, what comes to my mind is we need to do **DNS Exfiltration**.
9. So 
