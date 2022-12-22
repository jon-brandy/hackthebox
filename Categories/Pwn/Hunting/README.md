# Hunting
> Write-up author: jon-brandy
## DESCRIPTION:
I've hidden the flag very carefully, you'll never manage to find it! 
Please note that the goal is to find the flag, and not to obtain a shell.
## HINT:
- NONE
## STEPS:
1. First, unzip the file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207770543-41aad8d6-ba8a-42c0-9945-98ef3da51705.png)


2. Jump to the extracted folder.

![image](https://user-images.githubusercontent.com/70703371/207770678-bb6f3f88-d1cb-473c-b3a0-534a6edbd299.png)


3. Check the file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207770732-66521a26-8a9a-4225-958a-23d728416d17.png)


4. Since, the binary is stripped, it's harder for us to debug the binary.
5. Now, check the binary protection.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207771226-3271d1ea-91bb-403e-bd9d-5dbcadd9868d.png)


6. Let's run the binary.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/207774738-424fdd40-88fc-4bf1-b61e-d7c6b97a324c.png)


7. Got segmentation fault even though i entered a char.
8. Hmm.. Let's run the file in GDB.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/207774916-f15f8ed6-2720-45b9-9b50-e7f8f897a9f7.png)


![image](https://user-images.githubusercontent.com/70703371/207775532-1572f788-568e-4384-a624-85e311f41a35.png)



9. I tried to enter longer strings, but the program crashed at the same offset.

> PROOF

![image](https://user-images.githubusercontent.com/70703371/207775439-62f5cdc6-f57b-4206-bf97-d68a45121969.png)


10. When i tried to analyze the main function, i found the dummy flag.


![image](https://user-images.githubusercontent.com/70703371/207776126-2d91f200-04f8-4426-88bf-d65669dcb2b5.png)


11. I think the dummy flag is accessed in the `main()` function (?).
12. 

