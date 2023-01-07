# No Place To Hide
> Write-up author: jon-brandy
## DESCRIPTION:
We found evidence of a password spray attack against the Domain Controller, and identified a suspicious RDP session. We'll provide you with our RDP logs and other files. Can you see what they were up to?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211130806-fb17c411-8590-4417-9098-8a4e2a7a9b0b.png)


2. Let's strings the `.bmc` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211130814-0e3eba3f-d05a-4d38-8c0b-7dde1ba68623.png)


3. Hmm.. Let's open the other file using hexedit.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211130841-36d65954-fc65-43cf-bf4f-bc465e3d33ee.png)


5. Based from the result we can conclude that it's RDP bitmap cache file.
6. We can use [this](https://github.com/ANSSI-FR/bmc-tools) python script to extract the bitmaps from cache file.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211131148-d7775196-59f9-4aeb-9361-c172e0af4b36.png)


![image](https://user-images.githubusercontent.com/70703371/211131169-d125cb37-22d8-4675-afd4-b3ba35d5057b.png)


7. Let's collage all of them.

```
eog *.bin_collage.bmp
```

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211131214-b96b73c1-0519-41f8-b01b-79cdddb1bc0c.png)


![image](https://user-images.githubusercontent.com/70703371/211131242-032429fc-6c9f-4d2e-a54d-3d7cc7e01cb5.png)


8. Got the flag!

## FLAG

```
HTB{w47ch_y0ur_c0Nn3C71}
```
