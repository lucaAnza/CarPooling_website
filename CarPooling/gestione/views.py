from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Car

def home_page(request):

    response = "Hi i am luke!"

    return HttpResponse(response)

def elenca_params(request):
    response = ""
    
    for k in request.GET:
        response += request.GET[k] + " "

    return HttpResponse(response)

def two_params(request , nome , eta):
    response = nome + " " + str(eta)
    return HttpResponse(response)

def hello_template(request):
    ctx= { "title" : "Hello Template",
           "lista" : [datetime.now() , datetime.today().strftime('%A') , datetime.today().strftime('%B')]}
    return render(request, template_name = 'base_extended.html' , context = ctx)

def play_with_database(request):

    templ = "play_with_database.html"

    ctx = { "title":"Lista di Macchine", "carlist": Car.objects.all()}

    #TODO -> Finish to implement 1. Changes of a Database entry 2. Filtering of a entry 3. Add of a Database entry 

    return render(request,template_name=templ,context=ctx)
