from django.http import HttpResponse

def home_page(request):

    response = "Hi i am luke!"

    return HttpResponse(response)

def elenca_params(request):
    response = ""
    
    for k in request.GET:
        response += request.GET[k] + " "

    return HttpResponse(response)