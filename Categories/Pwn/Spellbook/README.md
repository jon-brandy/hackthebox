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

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/2362b950-13e0-4c8a-a3ef-68c5025f11f3)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/903afd72-3c9b-49b1-8ebe-31f124d66587)


2. Upon reviewing the main() functions, we found 4 function call that seems to be our interest. Those are **add()**, **delete()**, **edit()**, and **show()**.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/3dd271bb-f89a-4e64-bdf3-57a392a7be7b)


3. Great! Let's review the **add()** function first.



