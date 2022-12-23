# Space pirate: Going Deeper
> Write-up author: jon-brandy
## DESCRIPTION:
We are inside D12! We bypassed the scanning system, and now we are right in front of the Admin Panel. 
The problem is that there are some safety mechanisms enabled so that not everyone can access the admin panel and become the user right below Draeger. 
Only a few of his intergalactic team members have access there, and they are the mutants that Draeger trusts. 
Can you disable the mechanisms and take control of the Admin Panel?

## HINT:
- NONE
## STEPS:
1. First, unzipt the `.zip` file given, then jump to the extracted directory.

> INSIDE

![image](https://user-images.githubusercontent.com/70703371/209360739-725aaa02-8f61-4120-8fe3-a89e10e29d4f.png)


2. Check the `sp` file type.

![image](https://user-images.githubusercontent.com/70703371/209360801-f1ee46de-d6b9-441f-8716-d216f4f64f87.png)


3. It's a 64 bit binary file, dynamically linked, and not stripped.
4. Since it's not stripped, it's easier for us to debug the binary when decompiled.
5. Now, let's check the binary's protection.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209361035-8d8bd5e7-d939-4437-b3cd-6a96cdd17b8c.png)


6. **No canary found** and **no PIE**.
7. Anyway let's run the binary.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209361238-af164417-35ed-446c-b160-d24c630fa7c7.png)


8. 
