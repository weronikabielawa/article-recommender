# import the standard Django Forms
# from built-in library
from django import forms


# creating a form
class InputForm(forms.Form):
    treść_artykułu = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':'30', 'cols':'40', 'class': 'special'}))

