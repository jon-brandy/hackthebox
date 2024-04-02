# Spellbook
> Write-up author: jon-brandy

## Lessons Learned:
- Leak main arena address by freeing a chunk to unsorted bin.
- Utilizing OOB for fastbin attack lead to RCE.

## DESCRIPTION:
In this magic school, there are some spellbound books given to young wizards where they can create and store the spells they 
learn throughout the years. There are some forbidden spells that can cause serious damage to other wizards and are not allowed. 
Beware what you write inside this book. Have fun, if you are a true wizard after all..

## HINT:
- NONE

## STEPS:
1. In this challenge we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/079264de-f052-44f2-bbc2-994e89cc9ae8)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ac148f78-c617-47bd-bc9c-dbd02fe1facd)


2. Upon reviewing the main() functions, we found 4 function call that seems to be our interest. Those are **add()**, **delete()**, **edit()**, and **show()**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3dd271bb-f89a-4e64-bdf3-57a392a7be7b)


3. Great! Let's review the **add()** function first.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/58851af2-e2d8-42e6-992a-b16cff1399f7)


4. Based from the code above, everytime we allocate a chunk and it's size, a new chunk with 0x30 sized field is also created. Let's prove that by allocate a small size of chunk.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/911fbc71-1d53-49dd-9d58-d338f3e91caa)


5. Now let's review the **delete()** function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bf0bd5df-e0ce-45da-b923-29c49a2f351c)


6. Noticed the **__ptr** and **__ptr->sp** is freed but is not set to NULL afterwards. Hence we can still use the chunk later, it's introduce **Use After Free** vuln.
7. Remembering at the **add()** function, we can allocate up to 1000 bytes and there is Use After Free vuln at the **delete()** function. We can leak main arena libc address by freeing size above a fastbin range, so it shall fell to the unsorted bin. Using UAF, we might could obtain RCE.
8. Now let's review the **show()** function.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1d269956-3cca-4a3b-893b-f56bcd0600ef)


9. Nothing interesting here, it just prints all the data we sent before.
10. BUT, it introduces another vuln. A Format Strings Bug (FSB).
11. We can use an alternate way to leak libc address, by using this vuln.
12. Now let's analyze the **edit()** function.

