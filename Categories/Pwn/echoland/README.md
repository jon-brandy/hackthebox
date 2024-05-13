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

