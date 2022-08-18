# import the standard Django Forms
# from built-in library
from django import forms


# creating a form
class InputForm(forms.Form):
    treść_artykułu = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':'30', 'cols':'40', 'class': 'special'}))


GEEKS_CHOICES =(
    ("0", "-"),
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
)
class Results(forms.Form):
    propozycja_1 = forms.ChoiceField(choices=GEEKS_CHOICES, required=True)
    propozycja_2 = forms.ChoiceField(choices=GEEKS_CHOICES, required=True)
    propozycja_3 = forms.ChoiceField(choices=GEEKS_CHOICES, required=True)


