# Regularity
> Write-up author: jon-brandy

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/d20d1e54-c9f0-4e60-8820-70dea1f1090c)


## Lessons Learned:
- Ret2reg using call rsi; gadget.

## DESCRIPTION:

<p align="justify">Nothing much changes from day to day. Famine, conflict, hatred - it's all part and parcel of the lives we live now. We've grown used to the animosity that we experience every day, and that's why it's so nice to have a useful program that asks how I'm doing. It's not the most talkative, though, but it's the highest level of tech most of us will ever see...</p>

## STEPS:
1. In this challenge, we're given a 64 bit binary, statically linked, and not stripped.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/9b195474-0e37-4725-bf60-798139df026b)


> BINARY PROTECTIONS

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/bf714acb-c3d3-48f2-a180-944cd07db6a3)


2. Interesting, no protections are applied to the binary.
3. Upon reviewing the decompiled code, seems the binary using write() instead of printf() as stdout.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/b297ed28-a23f-4f83-8ec9-755a2f5258a9)

4
