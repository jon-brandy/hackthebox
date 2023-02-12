# Diagnostic
> Write-up author: jon-brandy
## DESCRIPTION:
Our SOC has identified numerous phishing emails coming in claiming to have a document about an upcoming round of layoffs in the company. 
The emails all contain a link to diagnostic.htb/layoffs.doc. 
The DNS for that domain has since stopped resolving, but the server is still hosting the malicious document (your docker). 
Take a look and figure out what's going on.
## HINT:
- NONE
## STEPS:
1. First, spawn the docker, then run `wget http://134.122.103.40:32730/layoffs.doc`, to download the file.
2. 
