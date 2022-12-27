# baby interdimensional internet
> Write-up author: jon-brandy
## DESCRIPTION:
aw man, aw geez, my grandpa rick is passed out from all the drinking again, where is a calculator when you need one, aw geez
## HINT:
- NONE
## STEPS:
1. First open the host given.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209678509-c2065897-5b59-4982-890a-9b844c591c93.png)


2. Let's try to add `?='` at the url.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209678593-9cce6de9-f264-4b30-b78a-24be585eb7e4.png)


3. The number changed, hmm.. try to refresh the page now.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209678648-49e4db67-dfcd-4fea-bea1-8f73a01e2df4.png)


4. The number changed again. Let's analyze the source code then.
5. Got a hint here, there should be a directory named `debug`.

![image](https://user-images.githubusercontent.com/70703371/209679126-67078665-2044-416a-8ee0-795889779c44.png)


6. Try to traverse there.

> RESULT

![image](https://user-images.githubusercontent.com/70703371/209679190-f2d0555c-36b1-4e1a-8625-b82dc0b3f6aa.png)


```py
from flask import Flask, Response, request, render_template, request
from random import choice, randint
from string import lowercase
from functools import wraps

app = Flask(__name__)

def calc(recipe):
	global garage
	garage = {}
	try: exec(recipe, garage)
	except: pass

def GCR(func): # Great Calculator of the observable universe and it's infinite timelines
	@wraps(func)
	def federation(*args, **kwargs):
		ingredient = ''.join(choice(lowercase) for _ in range(10))
		recipe = '%s = %s' % (ingredient, ''.join(map(str, [randint(1, 69), choice(['+', '-', '*']), randint(1,69)])))

		if request.method == 'POST':
			ingredient = request.form.get('ingredient', '')
			recipe = '%s = %s' % (ingredient, request.form.get('measurements', ''))

		calc(recipe)

		if garage.get(ingredient, ''):
			return render_template('index.html', calculations=garage[ingredient])

		return func(*args, **kwargs)
	return federation

@app.route('/', methods=['GET', 'POST'])
@GCR
def index():
	return render_template('index.html')

@app.route('/debug')
def debug():
	return Response(open(__file__).read(), mimetype='text/plain')

if __name__ == '__main__':
	app.run('0.0.0.0', port=1337)

```
