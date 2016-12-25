from django import forms

class module_nameForm(forms.Form):
    """Module_Name configuration form."""
    enabled = forms.BooleanField(
        label='Enable module_name',
        required=False)