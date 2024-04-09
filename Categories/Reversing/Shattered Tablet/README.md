# Shattered Tablet
> Write-up author: jon-brandy

## Lessons Learned:
- Code Review.

## DESCRIPTION:

Deep in an ancient tomb, you've discovered a stone tablet with secret information on the locations of other relics. 
However, while dodging a poison dart, it slipped from your hands and shattered into hundreds of pieces. Can you reassemble it and read the clues?

## HINT:
- NONE

## STEPS:
1. In this challenge we're given a binary which accepts one user input only. The binary is 64 bit, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/85a1e94c-92d6-4723-9fe4-23aafae4d23c)


> User Input Testing

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/18df2efd-1e0f-4c2a-8a05-97f1142b57a9)


2. Seems this binary checks whether our input is the same as what it's compare (flag checker).
3. Upon decompiling the binary in ghidra, found that it compares every chars in user input.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d3f2cab5-ecc9-40c7-bb49-90e99c3a9591)


4. Upon reviewing the main() function, we can identified the correct chars that are need to send.
5. Follow chars based from the order of these stack var declaration:

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/31d63bea-64bb-4fe9-80e9-fd8ed31e229e)


6. Noticed only variables `local_48` to `local_28` are used.

### THE FLOW

```
local_48 --> chr(local_48) + local_48._1_1_ + local_48._2_1_ + etc.
| | |
| | |
v v v
local_28 --> chr(local_28) + local_28._1_1_ + local_28._2_1_ + etc.
```

> RESULT

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/1df0ed47-61a3-48cd-a7df-250e054c91be)


## FLAG

```
HTB{br0k3n_4p4rt...n3ver_t0_b3_r3p41r3d}
```
