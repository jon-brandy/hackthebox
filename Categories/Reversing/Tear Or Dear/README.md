# Tear Or Dear
> Write-up author: jon-brandy
## DESCRIPTION:
Find the username and password and put them in the flag in the format: HTB{username:password}
Warning: It can produce false positives.
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212461568-6f99e9a5-2a5b-47dc-bed9-afcc0bf5e4d8.png)


2. Since it's a PE file, let's decompile the PE using dnSpy. But before that let's run it on windows.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212461616-0511d26b-51bb-4cd6-ad54-89733071ea92.png)


![image](https://user-images.githubusercontent.com/70703371/212461635-b25ea661-bc38-4edf-87f6-7f4516ac4a8d.png)


3. Yep, let's decompile it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212461670-f019b8da-8e19-40f2-8b88-e08634364318.png)


4. Let's check the `main()` function.

![image](https://user-images.githubusercontent.com/70703371/212461707-35c81cb2-c170-435c-b63a-aea659124d85.png)


5. 
