from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import *


# Function Based View (FBV)
def home_page(request):
    return render(request, template_name="home.html")


class UserCreateView(CreateView):
    form_class = CreateUserPassenger
    template_name = "user_create.html"
    success_url = reverse_lazy("login")


"""

class BiblioCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = CreaUtenteBibliotecario
"""