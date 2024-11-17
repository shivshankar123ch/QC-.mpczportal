from rest_framework import serializers
from tkc.models import *


class BalanceSheet_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TKC_BalanceSheet
        fields = "__all__"

class TKC_Document_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TKC_Document
        fields = "__all__"


class TKC_Turnover_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TKC_Turnover
        fields = "__all__"

        
