# Guida passo per passo per la realizzazione del sito 🇮🇹


## Step1 - init 

```bash

pipenv install django
pipenv shell
django-admin startproject <Project_name>
python manage.py startapp <App_name>

```

## Step2

### Creation of *views.py*

```python

from django.http import HttpResponse

def home_page(request):
    response = "Hi i am luke!"
    return HttpResponse(response)

def elenca_params(request):
    response = ""
    for k in request.GET:
        response += request.GET[k] + " "
    return HttpResponse(response)

```

### Add path on *urls.py*

```python

from .views import home_page,elenca_params

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/' , home_page , name="homepage"),
    path("", home_page,name="homepage"),
    path("elenca/", elenca_params ,name="elenca")
]

```

