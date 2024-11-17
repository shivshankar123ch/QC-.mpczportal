from django import forms
from po.models import Purchase_Order
from po.models import *
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class WorkForm(forms.ModelForm):
    work_order = RichTextField()
    copy_to = RichTextField()

    class Meta:
        model = Purchase_Order
        # fields = 'term_and_condition'
        fields = ('term_and_condition',)
        
        
class WorkFormData(forms.ModelForm):
    work_order = RichTextField()
    copy_to = RichTextField()

    class Meta:
        model = DI_Master
        # fields = 'term_and_condition'
        # fields = ('term_and_condition',)
        fields = ['term_and_condition']
