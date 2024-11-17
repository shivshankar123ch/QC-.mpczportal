from rest_framework import serializers
from tkc.models import *
from main.models import *

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



#--------------------------------SERIALIZERS BY RAVINDRA & GAURAV---------------------------------------# 
        
# class ConsumerSerializer_1(serializers.ModelSerializer):
    
#     class Meta:
#         model = TKC_Consumer
#         fields = "__all__"
        
class ConsumerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TKC_Consumer
        fields = ['id','consumerApplicationNo']
                      
class UserSerializer(serializers.ModelSerializer):  
      
    class Meta:
        model = User_Registration
        fields = ["User_Id","Authorised_person_E","CompanyName_E", "User_type","Authentication_id","Oyt"]

class tkc_paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TKC_Payment
        fields = ['Name']

class Consumer_bidSerializer2(serializers.ModelSerializer):    
   
    class Meta:
        model = TKC_Consumer_bid
        fields = ["contractor_category"]
                
class UserCompanyDataMainSerializer(serializers.ModelSerializer):
    
    user_id_id = UserSerializer()
    
    class Meta:
        model = UserCompanyDataMain     
        fields = ['user_id_id','Company_Id','CompanyName_E','Company_add_1','Company_add_2','Company_pin_code','Company_dist','Company_city','Company_state']

class CompanyDataMainSerializer(serializers.ModelSerializer):
    user_id_id = UserSerializer()
    
    class Meta:
        model = UserCompanyDataMain 
        fields = ['user_id_id','Company_Id','Company_add_1','CompanyName_E','Company_add_2','Company_pin_code','Company_dist','Company_city','Company_state']

class UserCompanyDataSerializer(serializers.ModelSerializer):    
    
    user_company_data = CompanyDataMainSerializer(many=True, read_only=True)
    
    class Meta:
        model = User_Registration
        fields = ["User_Id","Authorised_person_E","CompanyName_E","User_type","Authentication_id","user_company_data","Oyt"]

class Consumer_bidSerializer2(serializers.ModelSerializer):    
    class Meta:
        model = TKC_Consumer_bid
        fields = ["bid_order_at","contractor_category","bid_amount"]
           
class Consumer_bidSerializer(serializers.ModelSerializer):    
    User_Id = UserCompanyDataSerializer()
    consumers = ConsumerSerializer()
    class Meta:
        model = TKC_Consumer_bid
        fields = ["User_Id","bid_order_at","contractor_category", "bid_amount","consumers"]

class Contractor_selectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TKC_ContractorSelections
        fields = ['User_Id','consumers']
        
class Contractor_selectionSerializerGet(serializers.ModelSerializer):
    User_Id = UserCompanyDataSerializer()
    consumers = ConsumerSerializer()
    
    class Meta:
        model = TKC_ContractorSelections
        fields = ['consumers','User_Id']
 
#---------------------------SERIALIZERS BY RAVINDRA & GAURAV--------------------------#