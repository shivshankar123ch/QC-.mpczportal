from django import forms
from fqp.models import TKCWoInfo
from fqp.models import *
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class WorkForm(forms.ModelForm):
    work_order = RichTextField()
    copy_to = RichTextField()

    class Meta:
        model = TKCWoInfo
        fields = ('work_order', 'copy_to')


class Term_And_Condition(forms.ModelForm):
    Work_Order_Term_And_Condition = RichTextField()

    class Meta:
        model = TKCWoInfo
        fields = ('Work_Order_Term_And_Condition',)


class Major_Item(forms.ModelForm):
    class Meta:
        model = TKCWoInfo_Major_Item
        fields = ['Item_Description', 'Item_Code', 'Unit', 'Quantity', 'Unit_Price_With_Tax']
        widgets = {
            'Item_Description': forms.TextInput(attrs={'class': 'form-form-control ed-textbox'}),
            'Item_Code': forms.TextInput(attrs={'class': 'form-control ed-textbox'}),
            'Unit': forms.TextInput(attrs={'class': 'form-control ed-textbox'}),
            'Quantity': forms.TextInput(attrs={'class': 'form-control ed-textbox'}),
            'Unit_Price_With_Tax': forms.TextInput(attrs={'class': 'form-control ed-textbox'}),
        }


class TKC_T_C_WorkFormData(forms.ModelForm):
    term_and_condition = RichTextField()

    class Meta:
        model = tkc_di_master
        fields = ('term_and_condition',)
        
        
class TKCCopyWorkFormData(forms.ModelForm):
    copy_to = RichTextField()

    class Meta:
        model = tkc_di_master
        fields = ('copy_to',)