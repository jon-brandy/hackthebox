# Space pirate: Retribution
> Write-up author: jon-brandy
## DESCRIPTION:
We got access to the Admin Panel! The last part of the mission is to change the target location of the missiles. 
We can probably target Draeger's HQ or some other Golden Fang's spaceships. 
Draeger's HQ might be out of the scope for now, but we can certainly cause significant damage to his army.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/209497738-32a56db3-32a7-475f-ab4f-cbea45a002c8.png)


2. Check the executeable file type.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209497773-fafc8c84-b0a3-44a8-b7c5-ac09859a123c.png)


3. It's a 64 bit binary file, dynamically linked, and **not stripped**. Since it's not stripped, then it's easier for us to debug and identify the binary flow.
4. Now check the binary's protection.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209497848-65826f66-73bd-4457-bbe7-7e34f27f8ba6.png)


5. Since there's **No canary found**, hence we can do bufferoverflow concept.
6. Now let's open the binary in GDB.
7. Check, all the functions available.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209498001-9f803ee7-0461-4a3d-976d-7e2f8a467064.png)


8. Looks like there's 3 functions to analyze -> main, show_missiles, missile_launcher.
9. Let's run the file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209498097-90e2ae7c-6e98-4528-942a-8b58153cff4f.png)


10. Choose option 1.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209498134-486b9e0f-5408-48f4-ac37-eb51cfd2a840.png)


11. Choose option 2.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209498163-b0ca7905-542d-40d2-9c98-ef2b5160c439.png)


![image](https://user-images.githubusercontent.com/70703371/209498188-d12112d0-1c66-4e71-9c2a-83496fd9bfba.png)


![image](https://user-images.githubusercontent.com/70703371/209498211-f18250dc-7adc-4dee-9755-c4e278bb01bb.png)


12. I'm confused here, because we already have the `flag.txt` file from extracting the `.zip` file.

![image](https://user-images.githubusercontent.com/70703371/209498348-90b08ebf-7009-4192-92b9-3c24607bc55c.png)


13. Anyway let's open the binary in ghidra and open the `main()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209498508-1253825b-1e8a-4208-b6f6-ac0841ab575f.png)


14. 
