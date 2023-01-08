# Ransom
> Write-up author: jon-brandy
## DESCRIPTION:
We received an email from Microsoft Support recommending that we apply a critical patch to our Windows servers. 
A system administrator downloaded the attachment from the email and ran it, and now all our company data is encrypted. Can you help us decrypt our files?
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211203385-3c367240-5e4c-47b8-b454-c2cee37e3c49.png)


2. Hmm.. We got PE32+ file and encoded `.exe` file.
3. Let's decompile the PE32+ file.

> RESULT - MAIN FUNCTION


![image](https://user-images.githubusercontent.com/70703371/211203782-99e84329-a7a0-4822-8db2-44c150a10fea.png)


4. When i tried to check few functions, i found this `encrypt` function that could be our interest.


![image](https://user-images.githubusercontent.com/70703371/211205977-b2d4e2ea-c6d7-40ec-9da2-af2d124bd7bc.png)




