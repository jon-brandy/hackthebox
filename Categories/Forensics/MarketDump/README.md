# MarketDump
> Write-up author: jon-brandy
## DESCRIPTION:
We have got informed that a hacker managed to get into our internal network after pivoiting through the web platform that runs in public internet. 
He managed to bypass our small product stocks logging platform and then he got our costumer database file. 
We believe that only one of our costumers was targeted. Can you find out who the customer was?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209420791-8d4f34da-0397-46d8-9f39-27e79d1b0f02.png)


2. Let's open the file in wireshark.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209420910-27995dce-1139-4959-9871-e181b08e3907.png)


3. Let's start by follow the `TCP` stream.
4. Found nothing good here.

![image](https://user-images.githubusercontent.com/70703371/209420989-7e13a14d-6279-4921-9b64-2a67aa17f414.png)


5. Let's try to filter the `HTTP` stream.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209421013-08b1f15e-3f3c-48f7-9c1b-4a2de78720ab.png)


6. The bottom one quite interesting.

![image](https://user-images.githubusercontent.com/70703371/209421024-cca980ab-61a6-4ed2-8b81-b8661a276321.png)


7. Let's follow the stream.
8. Notice found unique string there.

![image](https://user-images.githubusercontent.com/70703371/209421048-59479f7b-93b0-4f93-a188-af435b3321b0.png)


9. Decode it using cyberchef.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209421062-12f3aea9-1eb1-49dc-b3cb-5862ee36bbe2.png)


10. Got the flag!

## FLAG

```
HTB{DonTRuNAsRoOt!MESsEdUpMarket}
```
