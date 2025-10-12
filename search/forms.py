from django import forms

class SearchRequest(forms.Form):


    request_field = forms.CharField(max_length=255, label="",
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Search',
                        'class': 'search-field'
                    }))
