from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *


class CreateVehicleForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addcar_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Add vehicle"))
    
    # Improve form front-end
    last_inspection_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    # Makes "inspection_date" optional
    def __init__(self, *args, **kwargs):     
        super(CreateVehicleForm, self).__init__(*args, **kwargs)   
        self.fields['last_inspection_date'].required = False

        

    class Meta:
        model = Car
        fields = ["model", "license_plate", "km" , "last_inspection_date"]