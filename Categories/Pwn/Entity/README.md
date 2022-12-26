# Entity
> Write-up author: jon-brandy
## DESCRIPTION:
This Spooky Time of the year, what's better than watching a scary film on the TV? Well, a lot of things, like playing CTFs but you know what's definitely not better? Something coming out of your TV!
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209522517-7a401e37-62f0-4021-950e-64449c6813da.png)


2. Check the binary type and it's protection.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209522571-ab2210fc-f940-44cb-b4bb-c2b992fc68a4.png)


![image](https://user-images.githubusercontent.com/70703371/209522593-88d78533-fac9-4613-b6ea-f534afb22f95.png)


3. Now let's decompile the binary using ghidra and check the `main()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209522722-df2a5570-e7ca-48e9-8157-3b7565989100.png)


![image](https://user-images.githubusercontent.com/70703371/209522747-4fd32eeb-fef5-47d7-91b9-772acea684b0.png)


4. Open the `get_flag()` function.

![image](https://user-images.githubusercontent.com/70703371/209522805-52823e93-d05a-4bf1-9f84-76b7c56a031f.png)


5. 
