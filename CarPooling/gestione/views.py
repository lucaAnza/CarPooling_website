from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Car
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

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


    # Get element example
    ctx = { "title":"Lista di Macchine", "carlist": Car.objects.all()}

    # Filtering Example
    km_threshold = 10000
    lista_filtrata = Car.objects.filter(km__gte=km_threshold)
    lista_filtrata = Car.objects.exclude(km__lt=km_threshold)
    lista_filtrata = Car.objects.filter(model="Ford") #Case insensitive
    # for l in Car.objects.raw("SELECT * FROM gestione_car WHERE km >= %s", [km_threshold]):  ## RAW QUERY

    # Add entry
    """c = Car()
    c.model = "Mustang"
    c.license_plate = "NY244DC"
    c.km = 3002
    c.last_inspection_date = timezone.now()
    try:
        c.save()
        print("Salvataggio riuscito!")
    except:
        print("Errore! Salvataggio non riuscito!")"""

    # Modify Entry
    #car_to_modify = get_object_or_404(Car, model="Model2")
    #car_to_modify.model = "Lamborghini"
    #car_to_modify.save()

    # Delete element
    #car_to_modify.delete()

    return render(request,template_name=templ,context=ctx)


class CarsListView(ListView):
    model = Car
    template_name = "garage.html"

    def get_queryset(self):
        return Car.objects.filter(user_id=self.request.user)