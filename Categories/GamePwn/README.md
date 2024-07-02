# GamePwn
> Write-up author: jon-brandy

## Lessons Learned:
1. Utilizing cheat engine to manipulate values in game's memory at runtime.

## DESCRIPTION:
Gotta collect them all.

## STEPS:
1. In this challenge we're given few dll files and 2 exe files.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/152a2f9f-6f58-4630-9fd0-a08c128fb3e8)


2. Running the game, seems our objective is to collect 20 cubes but somehow there are only 6 cubes available and no re-spawn.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/0ba25bde-a1b2-4cad-b48c-1f5e788d20b8)


3. Interesting. Actually we can use cheat engine to manipulate the cube collected values.
4. BUT, we need to identify which memory holds our cube value.
5. Now let's reopen the exe then attach the process to cheat engine.

> attach process

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58684ff9-82b4-46ac-9883-8599cfadc55a)


6. At the attached process page, type value 0 then click enter. This to trigger memory page, so then it rendered to us.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/cbf95534-f7e0-41d8-8bc2-46e0ad1e1db5)


> RESUT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/22efc0c7-6eef-48eb-91a0-dc090b00a92b)


7. Based from the result above, there are around 40 million values of 0s.
8. Let's grab one cube, then change the value to 1.

> RESULT


