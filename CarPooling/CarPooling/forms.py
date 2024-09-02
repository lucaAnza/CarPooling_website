from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class CreateUserPassenger(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit)  # Get user reference
        g = Group.objects.get(name="Passenger")       # Searching for the group
        g.user_set.add(user) # Add user to the specific group
        return user 


class CreateUserDriver(UserCreationForm):
    
    def save(self, commit=True):
        user = super().save(commit) 
        g = Group.objects.get(name="Driver") 
        g.user_set.add(user) 
        return user
