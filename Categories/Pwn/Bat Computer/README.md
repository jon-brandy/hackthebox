# Bat Computer
> Write-up author: jon-brandy
## DESCRIPTION:
It's your time to save the world!
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209466124-165c91d7-782c-43fe-95f3-f1c4d5b5b6df.png)


2. Next, check the file type.

> RESULT - 64 bit, stripped

![image](https://user-images.githubusercontent.com/70703371/209466133-9ea11e4c-167c-4750-b406-ca376c95304b.png)


3. Since it's a binary file, check the file's protection.

> RESULT - No Canary Found (means we can do bufferoverflow), NX disabled (means we can inject shellcode)

![image](https://user-images.githubusercontent.com/70703371/209466161-d860d603-e2a9-48d0-a588-ee38d583ad16.png)


4. Let's run chmod first to make the executable then run the file in gdb.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209466201-78001337-1429-44e0-90c8-93364aff7f8d.png)


5. Let's choose to track joker first.

![image](https://user-images.githubusercontent.com/70703371/209466212-8febfab0-ab55-4c1d-a3fc-a1b845c263a5.png)


6. Now let's chase him.

![image](https://user-images.githubusercontent.com/70703371/209466227-ab9face8-c56f-4af1-a53a-739bdf206574.png)


![image](https://user-images.githubusercontent.com/70703371/209466238-3a283a09-0eee-4510-840a-cdb19c4de183.png)


7. Let's decompile the file in ghidra.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209466257-86061308-c0aa-4a0d-98dc-26d65b4c0a6e.png)


8. Since the binary stripped, hence it's harder for us identify the function.
9. Anyway i think i found the `main()` function.

![image](https://user-images.githubusercontent.com/70703371/209466274-44f2c43b-1e89-4460-94e5-48b2c77dbd77.png)


10. We found the password here, but i don't think the program will give us a flag when we entered the correct pass.

![image](https://user-images.githubusercontent.com/70703371/209466369-2685fcf5-5bef-462f-83b2-e3c13f0f3cae.png)


12.
