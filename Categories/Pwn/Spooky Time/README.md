# Spooky Time
> Write-up author: jon-brandy
## DESCRIPTION:
Everyone loves a good jumpscare, especially kids or the person who does it.. Try to scare them all!
## HINT:
- NONE
## STEPS:
1. First, unzip the `.zip` file given, then jump to the extracted directory.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210698087-4d63d665-fb25-48f7-a475-80942d0b7044.png)


2. Check the file type.

> RESULT - 64 BIT BINARY FILE , NOT STRIPPED

![image](https://user-images.githubusercontent.com/70703371/210698241-0878bd4e-09de-4771-821e-9dc3b324aa20.png)


3. Now check the binary's protection.

> RESULT - NO RELRO

![image](https://user-images.githubusercontent.com/70703371/210698319-59563128-bbe4-4e1e-b737-b65fa1126d91.png)


4. Let's run the binary.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210698789-43aa5b50-42a2-42cf-aca3-51d0435208f4.png)


![image](https://user-images.githubusercontent.com/70703371/210698819-342f0f12-33e0-4f96-8689-b1b3c9a814bf.png)


5. Hmm.. the next input suddenly skipped, how about we input less strings.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/210698880-12cc361b-1e1c-4c58-9d06-e9da61baea72.png)


6. Let's decompile it with ghidra.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/210699065-0fe491f8-8f69-4304-b4c5-e1d5255cd7bc.png)


7. 
