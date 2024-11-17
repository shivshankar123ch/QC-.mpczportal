from CA.models import CA_Bank_Update_Req  
from django import forms

  
  
class CABankImageForm(forms.ModelForm):

    class Meta:  
        model = CA_Bank_Update_Req  
        fields = ['bank_name', 'account_Holder_Name', 'account_Number', 'ifsc','passbook_image'] 

        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_Holder_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_Number': forms.NumberInput(attrs={'class': 'form-control'}),
            'ifsc': forms.TextInput(attrs={'class': 'form-control'}),
            'passbook_image': forms.FileInput(attrs={'class': 'form-control'}),

        }