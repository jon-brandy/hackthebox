# Juggling facts
> Write-up author: jon-brandy
## DESCRIPTION:
An organization seems to possess knowledge of the true nature of pumpkins. 
Can you find out what they honestly know and uncover this centuries-long secret once and for all?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209683531-bb407c39-c57c-4084-8775-cb75e376a15a.png)


2. Click the `secret` button.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209683588-46661da2-8063-45bc-92e3-b3eaf9920a15.png)

3. Now let's check the source code given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209684610-54b8fc5a-70a2-4408-90a0-83bf9b3c9348.png)


4. Looks like the flag is in the `secrets` page.
5. Then when i analyzed the `IndexController.php` file.

![image](https://user-images.githubusercontent.com/70703371/209685062-e0fe2664-5fb8-4d3e-b5e1-430a4fb91450.png)


6. What comes to my mind is, the vuln here is `type juggling`. Notice there's 3 equal signs, which means not only the value must be the same but the type also. Not only that, we know that in PHP , the switch-case statement does `loose comparison`.

> SOURCE

```
https://www.php.net/manual/en/control-structures.switch.php
```

![image](https://user-images.githubusercontent.com/70703371/209686422-e4aa3d18-0463-45b7-a295-216b49c651da.png)


7. Based of the documentation from the link above. We can't send the type value at json as `true`. Hence we got the false bool, then we can get the flag.
8. Let's implement this using burpsuite and set the intercept to on when entering the `secrets` page.
9. Choose send to repeater, click send.
10. Change the type value as `true`, without the quote, otherwise the webapp shall think that we request a type.

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/e201aeb2-889d-4d79-80d9-7dc50752bf47)


11. Got the flag!

## FLAG

```
HTB{juggl1ng_1s_d4ng3r0u5!!!}
```

