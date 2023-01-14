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


5. Now check the `LoginForm()` function.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212461745-e7bf873b-8b3a-4bb7-95f5-d6fb726526fb.png)


6. Hmm.. Let's check the button1_Click

![image](https://user-images.githubusercontent.com/70703371/212461900-1b1d6609-5617-45b2-9e4f-fe06c1a4d71f.png)


7. Seems the line 11 shall be our interest, so let's set a breakpoint at that line, then run the program.

> RESULT (Enter both username and password as ADMIN)

![image](https://user-images.githubusercontent.com/70703371/212462008-2d9cb60d-bbdb-4bc3-b28b-75e6a510e053.png)


8. Because we want to see the `this.` so let's check that and search for **username**.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212462115-60215074-9ece-49d8-b8d9-551cdba80756.png)


9. Found it! Now let's run it again but this time enter the pass as `test`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212462149-61c1d2aa-58a6-43e5-ab2c-4460c6d9b564.png)


![image](https://user-images.githubusercontent.com/70703371/212462174-6dddb2bf-00aa-48bd-8a35-81fd52e75290.png)


10. Hmm.. Our password input is saved as the username.
11. 

