# Oxidized ROP

> Write-up author: jon-brandy


## Lessons Learned:
- RUST code review.
- Local Variable Overwrite using unicode characters.

## DESCRIPTION:

Our workshop is rapidly oxidizing and we want a statement on its state from every member of the team! > flag in `/challenge/flag.txt`

## HINT:
- NONE

## STEPS:
1. In this challenge, we're given a 64 bit binary, dynamically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/ab601b6c-8a5f-44ac-8f83-d71adeb32830)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/5753d15e-03a9-4c69-8e98-78da40535ba0)


2. Noticed, the challenge author disclosed the source code. Hence no need to decompile the binary **for now**.
3. Upon reviewing the **rust** code, found a potential overflow at the `save_data()` function.
