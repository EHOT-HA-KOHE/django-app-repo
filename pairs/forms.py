from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=True, label="Search query")
