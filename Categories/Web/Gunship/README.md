# Gunship
> Write-up author: jon-brandy
## DESCRIPTION:
A city of lights, with retrofuturistic 80s peoples, and coffee, and drinks from another world... 
all the wooing in the world to make you feel more lonely... this ride ends here, with a tribute page of the British synthwave band called Gunship. 🎶
## HINT:
- NONE
## STEPS:
1. First, open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441576-cfe4ab52-5d0d-43cf-b5db-b34ce018ee4c.png)

2. Now let's unzip the `.zip` file given and jump to the extracted directory.
3. Go to **challenge** directory to see the source code.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209441642-37e44dfb-37a5-4c9e-b9de-e446961670ab.png)


4. When i traverse to **routes** directory and check the `.js` script. Found a clue.

> index.js

```js
const path              = require('path');
const express           = require('express');
const pug        		= require('pug');
const { unflatten }     = require('flat');
const router            = express.Router();

router.get('/', (req, res) => {
    return res.sendFile(path.resolve('views/index.html'));
});

router.post('/api/submit', (req, res) => {
    const { artist } = unflatten(req.body);

	if (artist.name.includes('Haigh') || artist.name.includes('Westaway') || artist.name.includes('Gingell')) {
		return res.json({
			'response': pug.compile('span Hello #{user}, thank you for letting us know!')({ user: 'guest' })
		});
	} else {
		return res.json({
			'response': 'Please provide us with the full name of an existing member.'
		});
	}
});

module.exports = router;
```

5. It is known that `unflatten()` is outdated and vulnerable to prototype pollution.



## LEARNING REFERENCES:

```
https://security.snyk.io/vuln/SNYK-JS-ARRFLATTENUNFLATTEN-598396
https://blog.p6.is/AST-Injection/#Exploit
```
