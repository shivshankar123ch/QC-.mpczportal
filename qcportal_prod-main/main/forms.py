from django import forms
from .models import *

class PasswordForgotForm(forms.Form):
    email =forms.CharField(widget=forms.EmailInput(attrs={
		"class":"form-control",
		"placeholder":"enter the email"
	}))
    def clean_email(self):
        e = self.cleaned_data.get("email")
        if User_Registration.objects.filter(Email_Id=e).exists():
            pass
        else:
            raise forms.ValidationError("User with this account does not exist")
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'New Mobile Number',
        'placeholder': 'Enter New Mobile Number',
    }), label="New Contact Number")
    confirm_new_password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'New-Contact-Number',
        'placeholder': 'Confirm New Contact Number',
    }), label="Confirm new mobile number")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New mobile number did not match!")
        return confirm_new_password