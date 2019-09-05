from django import forms
from core.models import URL

class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ['path', 'timeshift_in_seconds', 'timeshift_in_minutes',]
