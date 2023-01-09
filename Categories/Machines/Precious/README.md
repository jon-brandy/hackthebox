# Precious
> Write-up author: jon-brandy
## DESCRIPTION:
- NONE
## HINT:
- NONE
## STEPS:
1. First, scan all open ports and it's services from the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211276690-4fe354b9-3638-442c-9480-5805e5c76317.png)


2. Notice the machines seems running a web application, let's open the host on the web browser.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211276928-1b29c212-2439-47e0-bb58-720df75f81ff.png)


3. Let's enter `http://google.com`.

> RESULT


![image](https://user-images.githubusercontent.com/70703371/211277475-e4846599-d902-479b-b914-f14759cebfd4.png)


4. Already tried to enter my own ip but didn't get any pdf.
5. Let's serve http on port 8000 first.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211278408-539b23c8-4444-4b66-b25c-523dbc65ae6c.png)


![image](https://user-images.githubusercontent.com/70703371/211278442-8bd11666-3bf6-4d31-9e18-6631343ef3ca.png)


6. Great! We got it.
7. Check the meta data, to see if we can grab any clue.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/211278752-fed9eaf3-6a3e-4eba-9701-42d0d4a7db02.png)


8. Notice the version of pdfkit is outdated and it's vulnerable.

> WRITTEN IN CVE MITRE

```
https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-25765
```

9. Hence i did a small outsource about the approach they used for this vuln, found this link.

```
https://security.snyk.io/vuln/SNYK-RUBY-PDFKIT-2869795
```

10. 
