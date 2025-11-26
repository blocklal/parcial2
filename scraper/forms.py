from django import forms

class ScraperForm(forms.Form):
    keyword = forms.CharField(label='Palabra clave', max_length=100)
