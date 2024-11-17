from django import forms
from django.forms import ModelForm
from .models import Add_material

SELECT_MATERIALS= [
    ('Power Transformer', 'Power Transformer'),
    ('Distribution Transformer', 'Distribution Transformer'),
    ('Three Phase LT Energy Meter', 'Three Phase LT Energy Meter'),
   
    
    ]

SELECT_SPECIFICATIONS= [
    ('33/11 KV Power transformer , OFTC Type , 1600 KVA', '33/11 KV Power transformer , OFTC Type , 1600 KVA'),
    ('33/11 KV Power transformer , OFTC Type , 3150 KVA  (Loss 3+15 KW)', '33/11 KV Power transformer , OFTC Type , 3150 KVA  (Loss 3+15 KW)'),
    ('33/11 KV Power transformer , OFTC Type , 8000 KVA  (Loss 6.5+46 KW)', '33/11 KV Power transformer , OFTC Type , 8000 KVA  (Loss 6.5+46 KW)'),
    ('DTR 11/0.4 KV  Conventional Star Rating  5 KVA (Copper wound)','DTR 11/0.4 KV  Conventional Star Rating  5 KVA (Copper wound)'),
    ('11/0.4 KV Distribution transformer  16 KVA (Conventional) (Copper wound)','11/0.4 KV Distribution transformer  16 KVA (Conventional) (Copper wound)'),

    ('11/0.4 KV Distribution transformer  100 KVA (Conventional)','11/0.4 KV Distribution transformer  100 KVA (Conventional)')]

class EmployeeForm(ModelForm):
    class Meta:
        model = Add_material
        
        fields = ('select_material', 'select_specification', 'type_test_report', 'gtp_and_drawing', 'others', )

        widgets = {
            # 'user_id': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'user_id'}),
            # 'emp_name': forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'select_material': forms.Select(attrs={'class': 'select'}, choices=SELECT_MATERIALS),
            'select_specification': forms.Select(attrs={'class': 'select'}, choices=SELECT_SPECIFICATIONS),          
            
        }