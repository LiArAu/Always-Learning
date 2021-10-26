from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class DateInput(forms.DateInput):
    input_type = 'date'

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label = 'Search')

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject','title','description','due','is_finished']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','due','is_finished']

class ConversionForm(forms.Form):
    CHOICES = [('length', 'Length'),('mass', 'Mass'), ('temperature','Temperature')]
    measurement = forms.ChoiceField(choices = CHOICES, widget = forms.RadioSelect)

# Widgets should not be confused with the form fields.
# Form fields deal with the logic of input validation and are used directly in templates.
# Widgets deal with rendering of HTML form input elements on the web page and extraction of raw submitted data.
# However, widgets do need to be assigned to form fields.
# For example, different of forms.RadioSelect and forms.Select.

class ConversionLengthForm(forms.Form):
    CHOICES = [('inch','Inch'),('centimeter','Centimeter')]
    input = forms.CharField(required = False, label = False,
            widget = forms.TextInput(attrs={'type':'number','placeholder':'Enter the Number'}))
    measure1 = forms.CharField(label = "", widget = forms.Select(choices = CHOICES))
    measure2 = forms.CharField(label = "", widget = forms.Select(choices = CHOICES))

class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'),('kilogram', 'Kilogram')]
    input = forms.CharField(required=False,label=False,
            widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter the Number'}))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))

class ConversionTempForm(forms.Form):
    CHOICES = [('c', 'C'),('f', 'F')]
    input = forms.CharField(required=False,label=False,
            widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter the Number'}))
    measure1 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    measure2 = forms.CharField(label='', widget=forms.Select(choices=CHOICES))
