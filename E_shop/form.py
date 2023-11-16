from django import forms
#from .models import Ticket
from store_app.models import Ticket
from .views import *

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','description','contacts','Bag','Battery','Charger']


class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','description','contacts','Bag','Battery','Charger']
