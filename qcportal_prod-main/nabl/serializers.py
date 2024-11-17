from rest_framework import serializers
from nabl.models import Product_Specification
from main.models import User_Registration;


class Specification_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Specification
        fields = ['id','Product_Specification']


class User_RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Registration
        fields = ['User_Id','Type_of_business']
