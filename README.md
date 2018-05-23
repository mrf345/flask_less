<h1 align='center'> flask_less </h1>
<h3 align='center'>A Flask extension for lesscpy python less compiler.</h3>

## Install:
#### - With pip
> - `pip install Flask-Less` <br />

#### - From the source:
> - `git clone https://github.com/mrf345/flask_less.git`<br />
> - `cd flask_less` <br />
> - `python setup.py install`

## Setup:
#### - Inside Flask app:
```python
from flask import Flask, render_template
from flask_less import lessc

app = Flask(__name__)
lessc(app)
```

#### - Inside jinja template:
```jinja
{% block head %}
  {{ cssify('static/main.less') }}
{% endblock %}
```
> results in:
```html
<link ref="stylesheet" href="static/main.css" />
```

## Options:
> The accepted arguments to be passed to the `lessc.cssify()` function are as follow:
```python
def __init__(self,
  app=None, # Flask app instance
  minify=True, # To minify the css file
  spaces=True, # To remove spaces from the css file
  tabs=False, # to remove tabs from the css file
  inTag=True # to return the css file link in link html tag
):
```

## Credit:
> - [lesscpy][1322353e]: Awesome Python less compiler.

  [1322353e]: https://github.com/lesscpy/lesscpy "lesscpy repo"
