from django import forms
from .models import EnergyData

class EnergyDataForm(forms.ModelForm):
    class Meta:
        model = EnergyData
        fields = ['steps']  # user inputs steps only
