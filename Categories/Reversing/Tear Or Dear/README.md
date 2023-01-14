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
11. Now `add watch` to that variable to see what will the program do with the variable as the it running.

![image](https://user-images.githubusercontent.com/70703371/212462250-58542e84-ae61-4078-a10f-87fbca9faffd.png)


12. Now search for `o`, since the username is compared to `o`.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212462267-122ecfd4-6800-45da-b31e-4fb483576a41.png)


13. Let's watch that as well, not forget to watch the `s` too.

> RESULT - WATCH

![image](https://user-images.githubusercontent.com/70703371/212462371-e898ff9c-c5b6-46d4-91b1-17c4862c675c.png)


14. Set the breakpoint at `check1` function at line 528.

![image](https://user-images.githubusercontent.com/70703371/212462435-4cf7579c-eb32-47b6-9b52-5c0cc3a5a65f.png)


15. Now run the program again. Then modify the value of our username (which is the pass) as the leaked pass we got.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212462727-484a64a7-4b54-4bf9-b7b0-c8dae48ed644.png)


> PRESS CONTINUE

![image](https://user-images.githubusercontent.com/70703371/212462752-ee55afd5-1423-4e56-b9ff-eb0c38ea71a3.png)


> PRESS STEP OVER

![image](https://user-images.githubusercontent.com/70703371/212462762-7feaf4db-b752-48ee-8aae-b16d69dc6de4.png)


![image](https://user-images.githubusercontent.com/70703371/212462769-0485400f-680c-4a9b-ada3-0b485179b88d.png)


16. Got s2, add that to watch,then do the same thing with the `check2()` function.

![image](https://user-images.githubusercontent.com/70703371/212462965-69a5af9d-1869-496b-af84-4149bd43c470.png)


![image](https://user-images.githubusercontent.com/70703371/212463005-39e848ec-5db4-4112-967d-4e821c3ed833.png)


17. The s3 gave us the same value, confused here. Let's check the `check4()`.
18. It still gave us the same value, how about the last check.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/212463148-d1fc2822-9644-4d3b-b1e7-e564a2151704.png)


![image](https://user-images.githubusercontent.com/70703371/212463132-a693adf2-099c-415c-8180-6c17c2d64fc8.png)


19. Add to watch for `.aa` value.
20. Well actually i'm stucked here for a while and tried to input the password as `roiw!@#` and the username as `roiw` it says wrong but when i entered the username as `piph` and pass as `roiw!@#`. It says correct!

![image](https://user-images.githubusercontent.com/70703371/212463325-8ff26f81-dec4-4e86-acb0-534889b266af.png)

21. Hence we got the flag!

## FLAG

```
HTB{piph:roiw!@#}
```
