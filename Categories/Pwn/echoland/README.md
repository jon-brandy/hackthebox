# echoland

> Write-up author: jon-brandy

## Lessons Learned:
- Pwning blind PWN.
- Exploiting Format Strings Bug (leaking PIE and LIBC runtime).
- Binary dumping.

## DESCRIPTION:

<p align="justify">
It is heavily raining. You run to the cave in order to find shelter, but a heavy boulder falls and shuts your exit. Darkness everywhere, you cannot see a thing. You and your friend get separated. You need your friend to help you move the boulder! You shout, and shout for dear life, but there's dead silence and your friend is nowhere to be found. Are you really both going to be stuck in this cave forever, or are you going to do something to get a response back?
</p>


## HINT: 
- NONE

## STEPS:
1. In this challenge we're not given any binary or source code. It's a blind pwn challenge.
2. Knowing this is a blind pwn challenge, most likely there is FSB and the program flow shall be simple.

> Identifying FSB

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/f65eeeb2-b606-4644-a678-80ddadf9984f)


3. We're given 2 menu options, but the FSB is found at the menu option prompt. The second menu seems should not be our interest.
4. Upon checking whether there is canary by simply sending 1024 cyclic pattern, got segfault but no **stack smashing**. This indicates that there is no canary.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/7082c50e-36e0-45e7-b6f8-6a26c4a3c6e8)


5. Further checking, by leaking addresses, found that PIE is enabled.

![image](https://github.com/jon-brandy/hackthebox/assets/70703371/dd484e18-f08c-4e6f-ad76-204490012529)


6. In a blind pwn challenge, the objective is to dump the binary. The first approach is to identify potential main() function.
7. At this state we're lacking of visibility, index 12, 17, or 20 can be used to dump the binary.
8. Let's try to use index 12.



