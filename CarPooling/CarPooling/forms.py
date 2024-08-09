from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

class CreateUserPassenger(UserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit)  # Get user reference
        g = Group.objects.get(name="Passenger")       # Searching for the group
        g.user_set.add(user) # Add user to the specific group
        return user 


"""
class CreaUtenteBibliotecario(UserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit) 
        g = Group.objects.get(name="Bibliotecari") 
        g.user_set.add(user) 
        return user
""" 