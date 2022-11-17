from django import forms
from django.forms import ModelForm
from .models import Distance

class DistanceForm(ModelForm):
    class Meta:
        model = Distance
        fields = ('source_url','destination')