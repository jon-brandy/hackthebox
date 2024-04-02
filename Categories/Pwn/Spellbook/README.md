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




