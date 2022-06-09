# import the standard Django Forms
# from built-in library
from django import forms


# creating a form
class InputForm(forms.Form):
    article_content = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':'40', 'cols':'50'}))

