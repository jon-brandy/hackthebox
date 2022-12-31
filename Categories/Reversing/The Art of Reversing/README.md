# The Art of Reversing
> Write-up author: jon-brandy
## DESCRIPTION:
This is a program that generates Product Keys for a specific Software Brand.

The input is the client UserName and the Number of Days that the sofware will remain active on the client.
The output is the product key that client will use to activate the software package.

We just have the following product key 'cathhtkeepaln-wymddd'
Could you find the corresponding Username say A and the number of activation days say B given as input?

The flag you need to enter must follow this format: HTB{AB}
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210127447-b3e96236-2280-42f6-bcbe-5f032be1aa44.png)


2. First, let's strings the file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210127579-f57de7af-4de5-43d1-bd85-c20492565f54.png)


3. Based from it, now we know, we need to decompile the file using DNSpy.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210127674-4b0c7d7c-5358-46df-992c-ace0ca4eac85.png)


4. 

