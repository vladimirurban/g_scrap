from cProfile import label

from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label='Hledat', max_length=100)