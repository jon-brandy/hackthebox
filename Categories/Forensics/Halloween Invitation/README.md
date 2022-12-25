# Halloween Invitation
> Write-up author: jon-brandy
## DESCRIPTION:
An email notification pops up. It's from your theater group. Someone decided to throw a party. 
The invitation looks awesome, but there is something suspicious about this document. Maybe you should take a look before you rent your banana costume.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209462344-f26d2097-760a-4820-ac20-36b075e73780.png)


2. Check the file type with exiftool.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209462403-36d24f8d-c924-40eb-a1d3-cd016229fa0f.png)


3. From the MIME Type description, i think we can extract the VBA macro.
4. Anyway let's check any hidden files inside.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209462433-d884f9a3-92d8-425c-a62a-cfee045f77d2.png)


5. Now let's extract the VBA macro using `oletools`.

```sh
Command -> olevba --deobf invitation.docm > olevba.out
```

> RESULT 

![image](https://user-images.githubusercontent.com/70703371/209462802-fb7f5e43-9b75-460e-a9d3-2250b23b208c.png)


