from django.contrib.auth import authenticate
from django import forms


attrs_dict = {'class':'required'}


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,
        maxlength=75)),
        label="Username",
        required=True)

    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                               label="Password")

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            if not authenticate(username = self.cleaned_data['username'],
                                password = self.cleaned_data['password']):
                raise forms.ValidationError("Wrong username or password")
        return self.cleaned_data
