# Hackerman
> Write-up author: jon-brandy
## DESCRIPTION:
There should be something hidden inside this photo... Can you find out?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210074730-a1d287c4-b633-4324-bab1-1f57c208541c.png)


2. Let's check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210074770-26cab8dc-8b03-4139-a409-9326739aba6a.png)


3. Let's strings it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210074834-8f51c83e-8ab7-4df1-bed3-a3e14a63e079.png)


4. Notice there's a strings that looks like a hash (?) Let's assume it's md5 since it's the common one in CTF.
5. Let's try to crack it with online md5 [cracker](https://crackstation.net/).

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210075005-3a82762f-1041-42d5-a0f2-dd670ebc87c9.png)


6. Hmm.. Not the flag, but a string.
7. What comes to my mind is, we shall use `steghide` to extract hidden file's inside since the string could be the pass.
8. Let's try it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210075174-802d8712-4d7c-41d4-ab47-f5edf39fb1c4.png)


9. Nice! Exactly as what we thought.
10. Now, strings the `.txt` file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210075245-45eb403b-7427-4424-9ca0-d03d3d2842d8.png)


11. Might be encoded in base64, let's try to decode it anyway.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210075309-0c1f6cc6-95b8-4e1b-9cab-b51b6bd8ca6b.png)


12. Got the flag!


## FLAG

```
HTB{3v1l_c0rp}
```
