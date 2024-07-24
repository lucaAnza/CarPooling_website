# Guida passo per passo per la realizzazione del sito 🇮🇹


## Step1 - init 

```bash

pipenv install django
pipenv shell
django-admin startproject <Project_name>

#If you want to create a sub-application
python manage.py startapp <App_name>

```

## Step2

### Creation of *views.py*

```python

from django.http import HttpResponse

def home_page(request):
    response = "Hi i am luke!"
    return HttpResponse(response)

# Parametri passati con ?
def elenca_params(request):
    response = ""
    for k in request.GET:
        response += request.GET[k] + " "
    return HttpResponse(response)
# Parametri passati con /
def two_params(request , nome , eta):
    response = nome + " " + str(eta)
    return HttpResponse(response)

```

### Add path on *urls.py*

```python

from .views import home_page,elenca_params

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/' , home_page , name="homepage"),
    path("", home_page,name="homepage"),
    path("elenca/", elenca_params ,name="elenca") # Parametri passati con ?
    path('parametri/<str:nome>/<int:eta>/', view_func, name=’alias’)  # Parametri passati con /
]

```

## Step3 - Aggiunta template

Consigli:

- Fare `{% extends "base.html" %}` o `{% include "base.html" %}` son 2 cose diverse.

1. Creazione /templates nella root del progetto.
2. Aggiungi in *urls.py* `'DIRS': [os.path.join(BASE_DIR, "templates")],`
3. Aggiunti *base.html*, *base_extended.html* on /templates.
    Base:

    ```html
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">

        {% block head %} {% endblock %}

        <title> {% block title %}{% endblock %}</title>
    </head>
    <body>
        {% block content %}

        {% endblock %}
    </body>
    </html>
    ```

    Extended:

    ```html
    {% extends "base.html" %}

    {% block title %} {{title}} {% endblock %}

    {% block content %}
        <h1>
            {% if user.is_authenticated %}
                Ciao, {{user.name}}
            {% else %}
                Ciao, guest!
            {% endif %}
        </h1>

        {% for i in lista %}
            <p> {{i}} </p>
        {% end for %}
    {% endblock %}
    ```
4. Add this on *views.py*

    ```python
    def hello_template(request):
            ctx= { "title" : "Hello Template",
                   "lista" : [datetime.now() , datetime.today().strftim('%A') , datetime.today().strftime('%B')]}
        return render(request, template_name = 'base_extended.html' , context = ctx)
    ```

5. Change *urls.py*

    ```python
    from .views import home_page,elenca_params,hello_template,two_params

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('home/' , home_page , name="homepage"),
        path("", home_page,name="homepage"),
        path("elenca/", elenca_params ,name="elenca"), # Parametri passati con ?
        path('parametri/<str:nome>/<int:eta>/', two_params, name='alias'),  # Parametri passati con /
        path('template/', hello_template, name='template')  
    ]
    ```

## Step4 - Risorse statiche

1. Crea directory */static*.
2. Add info on *settings.py*.

    ```python
    #remember to import os
    STATICFILES_DIRS = [os.path.join(BASE_DIR , "static")]
    ```

3. Add `{% load static %}` on block head of the extended html.
4. Add `<img src="{% static 'img/test.png' %}" alt="Mia immagine">`.


## Step5 - Creazione sub-application

1. `python3 manage.py startapp gestione`
   
2. Changes on *settings.py*

    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'gestione'       # <----------------- 
    ]
    ```

3. Changes on *urls.py*

    ```python
    from django.urls import path,include
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('gestione/' , include('gestione.urls'))  # <----- Move old urls on Gestione/urls.py
    ]
    ```

4. Move old *views.py* on *Gestione/views.py*
   

## Step5 - Il mio primo database

//TODO - Insert img

1. Create `models.py` on /<Application_Name>

2. `models.py` : 

```python
# TODO
```

3. Make migrations : 

```bash
cd <Project_Name_Dir>
python manage.py makemigrations gestione # gestione is <Application_Name>
python manage.py migrate
```