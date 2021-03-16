# Herokuapp

A step-by-step guide to creating a simple web application that shows the number of page views in _Python_ and _Django_ using _Redis_. It also shows how to roll out the application to _Heroku_ hosting using _Git_.


## Dependencies

First of all, let's see what dependencies we need to develop and deploy the application. We will place them in `requirements.txt`, which will make it possible to put them in one command locally in _Python's virtual environment_.
```
pip install -r requirements.txt
```

This file will also be used when installing dependencies on the hosting during the deployment of the application.
```
# requirements.txt

django
redis
gunicorn
django-heroku
```

Details for each dependency:
- `django` &ndash; The app is created using Django.
- `redis` &ndash; Package for linking _Redis_ to _Python_. We need it because we store a page view counter in _Redis_.
- `gunicorn` &ndash; Needed to run _Django_ in production. Locally, _Django_ runs through the `runserver`. To run on _Heroku_, you need `gunicorn` or another web server. Note that this is not specific to _Heroku_, but rather specific to production.
- `django-heroku` &ndash; Module from _Heroku_ itself, it is not required. But it helps to configure _Django_ settings for working with _Heroku_, which makes our life easier. And then, in the file `settings.py` it will show how it is applied.


## Development

We will start development by creating the basic project structure using _Django_ tools. And inside the project, we will create a counter application.
```
$ django-admin startproject herokuapp
$ cd herokuapp
$ python manage.py startapp counter
```

The app will contain one page in the root of the site. We will specify this in the file `urls.py`.
```
# herokuapp/urls.py

from django.contrib import admin
from django.urls import path
from counter.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
]
```

The handler will be class-based view. It will use the template `index.html` and access the object `counter` to save the number of page views.
```
# counter/view.py

from django.views.generic import TemplateView
from counter.storage import counter

class IndexView(TemplateView):
    template_name = 'counter/index.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['counter'] = counter.inc()
        return data
```

The object `counter` will save the number of views in the _Redis_ database if there is an access url. Otherwise, the data will be stored in memory.
```
# counter/storage.py

import redis
from django.conf import settings


class Counter:
    redis = None
    key = "counter_key"

    def __init__(self):
        if settings.REDIS_URL:
            self.redis = redis.from_url(settings.REDIS_URL)
        else:
            self.x = 0

    def inc(self):
        if settings.REDIS_URL:
            return self.redis.incr(self.key)
        else:
            self.x += 1
            return self.x


counter = Counter()
```

Template is a simple page with a basic layout and a single variable.
```
# counter/templates/counter/index.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello, world!</title>
</head>
<body>
    <h1>Hello, world!</h1>
    <p>This page was viewed {{ counter }} times.</p>
</body>
</html>
```

In the `settings.py` we will add the definition of the necessary constants, and also use the `django-heroku` module to facilitate the deployment of the application to the hosting.
```
# herokuapp/settings.py

import os
import django_heroku
...
SECRET_KEY = os.getenv('SECRET_KEY')
...
DEBUG = bool(os.getenv('DEBUG', True))
...
INSTALLED_APPS = [
    ...
    'counter',
]
...
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')

django_heroku.settings(locals())
```


## Deployment

To run Django on Heroku, we will use the _Gunicorn_ web-server. We will specify this in the file `Procfile`.
```
# Procfile

web: gunicorn herokuapp.wsgi --log-file -
```

In the `.gitignore` we specify which files will not be tracked by _Git_.
```
# .gitignore

*.py[co]
__pycache__
db.sqlite3
.*
!.gitignore
```

We will look deploy using _Heroku Git_. You must install the following applications on local machine, if they are not already installed: [_Git_](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and
[_Heroku CLI_](https://devcenter.heroku.com/articles/heroku-command-line). 

In this case, the deployment process will occur when sending a commit of changes to _Heroku_ server.
```
$ heroku login

$ git init

$ heroku git:remote -a herokuapp

$ git add .
$ git commit -m "Initial commit"

$ git push heroku master
```
