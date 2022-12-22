# Behind the Scenes
> Write-up author: jon-brandy

## DESCRIPTION:
After struggling to secure our secret strings for a long time, we finally figured out the solution to our problem: Make decompilation harder. 
It should now be impossible to figure out how our programs work!

## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given.
2. Next, jump to the extracted directory and run the binary file inside.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209165981-236d3ffc-0a00-4474-a6f0-bd3279ddc11d.png)


3. Let's strings the file to find any clue.
4. Actually i got no clue.
5. Before decompile the binary, let's try with hexedit.
6. Well something caught my attention.

![image](https://user-images.githubusercontent.com/70703371/209169096-044b646b-a597-427b-a406-f33aafc662bf.png)


7. Could be the password is -> Itz_0nLy_UD2 (?) 
8. Try to run it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209169347-d6aac69a-18e8-44d3-bdb9-5a8edec51411.png)


9. Hmm, let's check by run with another string.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209169486-5ceebfc7-1355-46e6-9863-b35f83066734.png)


10. Yep, we got the correct flag then.

## FLAG

```
HTB{Itz_0nLy_UD2}
```

