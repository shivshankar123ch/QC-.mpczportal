from csv import field_size_limit
# from dataclasses import field
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from main.models import *
from rest_framework import serializers
from vendor.models import *
from api.models import *
from fqp.models import *
from tkc.models import *
from nabl.models import *
#from rca.models import rca_test_rept_power_analyzer
from rca.models import Rca_User_Registration, Rca_Vendor_Document                        
from rca.models import rca_test_rept_power_analyzer

# 1st api loginview--------------------------------

# INSPECTIONLIST 2nd api---------------------------------------------

class UserCompanyDataMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompanyDataMain
        fields = (
            'user_id', 'Mi_Type_of_Inspection', 'CompanyName_E', 'Reg_No', 'Registration_Date', 'Company_pin_code',
            'Company_add_1', 'Company_add_2', 'Company_dist', 'Company_state', 'Company_city', 'Mi_Remark')


# vendordetail 3rd api---------------------------------------------

class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetail
        # fields = ('E_Sanctioned','E_Working_Load','E_Data','E_Details_of_electric_power','P_Quantity','P_Testing','T_Details','T_Desription','T_Equipments','T_Manufacturing','T_Inspection','T_Substandard','T_Assistance','T_Accreditation','T_Testing_carried','T_Certification')
        fields = (
            'user_id', 'E_Sanctioned', 'E_Working_Load', 'E_Data', 'E_Details_of_electric_power', 'P_Quantity',
            'P_Testing',
            'T_Details', 'T_Desription', 'T_Equipments', 'T_Manufacturing', 'T_Inspection', 'T_Substandard',
            'T_Assistance',
            'T_Accreditation', 'T_Testing_carried', 'T_Certification')


# AppraisalReport 4th api---------------------------------------------

class AppraisalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalReport
        fields = (
            'v_experience', 'v_availability', 'v_calibration', 'v_bought_out_items', 'v_inprocess_inspection',
            'v_dispatch',
            'v_overall_record', 'v_area_instruction', 'v_isobis_certification', 'v_material_handling',
            'v_general_observation', 'v_packing_product', 'p_experience_of_production', 'p_experience_of_supervisor',
            'p_effectiveness', 'p_quality', 'p_cleanliness', 'p_safety_equipment', 'p_condition_of_stores',
            'p_back_uppower_facility', 'p_adequate_progress', 'p_overall_view')


class Vendor_Material_DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Details
        fields = ['user_id', 'Material_Name']


class VendorMaterialDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Details
        fields = ['user_id', 'Material_Specification']


class VendorMaterialDetailsSerializerS(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Details
        fields = ('user_id', 'Material_Name')


class VendorMaterialDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Details
        fields = ('user_id', 'Material_Name', 'Material_Specification', 'Material_Test_Doc', 'Material_GTP_Doc',
                  'Material_Other_Doc')


class MaterialVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialVerification
        fields = (
            'Material_Name', 'Material_Specification', 'Material_Test_Doc', 'Remark_Test', 'Material_GTP_Doc',
            'Remark_GTP',
            'Material_Other_Doc', 'Remark_Other', 'sufficient_capacity', 'sufficient_capacity_remark', 'Verify')


class Add_materialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add_material
        fields = (
            'id', 'user_id', 'select_material', 'select_specification', 'type_test_report', 'gtp_and_drawing', 'others',
            'emp_name')


class Vendor_Technical_DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Technical_Details
        fields = ('user_id', 'Plant_View', 'Machinery_View')


# ------fqp---------------------------------------------------------------------

# class FQP_MaterialSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FQP_Material
#         fields = ('FQP_Material','Material_Name')


class FQP_TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FQP_Test
        fields = ('officer_id', 'FQP_Test_Id', 'FQP_Material', 'FQP_Test')


# class FQP_DataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FQP_Data
#         fields = ('FQP_Test_Id','Status','Observation','Latitude','Longitude')


# ----quality liat------------------------1st api


class FQP_MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = FQP_Material
        fields = '__all__'


class FQP_Test_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FQP_Test_Data
        fields = ('Test_id', 'FQP_Officer_Id', 'Status', 'Observation', 'Latitude', 'Longitude')


class FQP_OfficerSerializer(serializers.ModelSerializer):
    FQP_Officer_Id = serializers.EmailField(max_length=255, min_length=6, read_only=True)
    FQP_Officer_Name = serializers.CharField(max_length=555)
    FQP_Password = serializers.CharField(max_length=68, min_length=5, required=True)

    class Meta:
        model = FQP_Officers
        fields = ["FQP_Officer_Id", "FQP_Officer_Name", "FQP_Password"]


class InspectingOfficerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectingOfficerInfo
        fields = ('id', 'officer_name', 'officer_password')


class Material_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Master
        fields = ('Material_Id', 'Material_Name')


class Material_SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Specification_Master
        fields = ('Material_Specification_Id', 'Material_Item_Code', 'Material_Specification_Name',
                  'Material_Specification_Certificate_Name', 'Material_Unit_Name')


class IS_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Nabl_Is_Master
        fields = ('Is_Id', 'IS_Name', 'Material_Name')


class Material_Test(serializers.ModelSerializer):
    class Meta:
        model = Nabl_Acceptance_Test_Master
        fields = ('Acceptance_Test_Id', 'Name_Of_Acceptance_Test')


# ---------------------jeevan ------------------->
class InspectingOfficerInfoSerializer(serializers.ModelSerializer):
    # = serializers.IntegerField(source='category_id')
    class Meta:
        model = InspectingOfficerInfo
        fields = "__all__"


class User_RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Registration
        fields = ['User_Id', 'Type_of_business']


class MQP_Inspecting_Officer_Serializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDispatchInfo
        fields = "__all__"


class User_RegistrationSerializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(source='User_Id')
    Authorised_person = serializers.CharField(source='Authorised_person_E')
    CompanyName = serializers.CharField(source='CompanyName_E')

    class Meta:
        model = User_Registration
        fields = ["vendor_id", "Authorised_person", "CompanyName", "ContactNo", "Email_Id", "add_material","cgm_approval"]


class Factory_Inspection_InfoSerializer(serializers.ModelSerializer):
    vendor = User_RegistrationSerializer()
    task_id = serializers.IntegerField(source='id')
    status = serializers.IntegerField(source='Status')

    class Meta:
        model = Factory_Inspection_Info
        fields = ["task_id", "assign_date", "execution_date", "status", "vendor"]


class RCA_User_RegistrationSerializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(source='User_Id')
    Authorised_person = serializers.CharField(source='Authorised_person_E')
    CompanyName = serializers.CharField(source='CompanyName_E')
    Authorised_Person_Aadhar = serializers.CharField(source='Aadhar')
    Address_1 = serializers.CharField(source='Company_add_1')
    Address_2 = serializers.CharField(source='Company_add_2')
    Pin_code = serializers.IntegerField(source='Company_pin_code')
    District = serializers.CharField(source='Company_dist')
    State = serializers.CharField(source='Company_state')

    class Meta:
        model = Rca_User_Registration
        fields = ["vendor_id", "Authorised_person", "CompanyName", "ContactNo", "Email_Id",
                  "Authorised_Person_Aadhar", "Company_Pan_No", "Company_Gst_No", "Address_1",
                  "Address_2", "Pin_code", "District", "State"]


class RCA_Factory_Inspection_InfoSerializer(serializers.ModelSerializer):
    vendor = RCA_User_RegistrationSerializer()
    task_id = serializers.IntegerField(source='id')
    status = serializers.IntegerField(source='Status')

    class Meta:
        model = RCA_Factory_Inspection_Info
        fields = ["task_id", "assign_date", "execution_date","perform_date" ,"status", "vendor"]


class ProcurementInfoSerializer(serializers.ModelSerializer):
    # vendor = User_RegistrationSerializer()
    # task_id = serializers.IntegerField(source='id')
    # status = serializers.IntegerField(source='Status')

    class Meta:
        model = ProcurementInfo
        fields = ["item_class", "item_category", "item_name", "specification"]


class VendorDispatchInfoSerializer(serializers.ModelSerializer):
    lab_name = User_RegistrationSerializer()
    po_id = ProcurementInfoSerializer()

    class Meta:
        model = VendorDispatchInfo
        fields = ["po_id", "item_quantity", "lab_name"]


class Material_Inspection_InfoSerializer(serializers.ModelSerializer):
    vendor = User_RegistrationSerializer()
    di = VendorDispatchInfoSerializer()
    task_id = serializers.IntegerField(source='id')
    status = serializers.IntegerField(source='Status')

    class Meta:
        model = Material_Inspection_Info
        fields = ["task_id", "assign_date", "execution_date", "status", "vendor", "di"]


class Vendor_Material_Details_Serializer(serializers.ModelSerializer):
    status = serializers.IntegerField(source='Primary_verification_Status')

    class Meta:
        model = Vendor_Material_Details
        fields = ["id", "Material_Name", "Material_Specification", "Material_Test_Doc", "Material_GTP_Doc",
                  "Material_Other_Doc", "status","response_submitted"]


class Vendor_Technical_Document_Serializer(serializers.ModelSerializer):
    status = serializers.IntegerField(source='Primary_verification_Status')

    class Meta:
        model = Vendor_Technical_Details
        fields = ['id', 'Types_of_Docs', 'Document_Doc', 'status','response_submitted']


class RCA_Vendor_Technical_Document_Serializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='Vendor_Document_Id')
    doc = serializers.CharField(source='Ddocfile')

    class Meta:
        model = Rca_Vendor_Document
        fields = ['id', 'Types_of_Docs', 'Document_Number', 'doc']


class VendorDispatchItemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDispatchItemInfo
        fields = ['id', 'serial_number', 'status']


class Field_Inspection_InfoSerializer(serializers.ModelSerializer):
    contractor = User_RegistrationSerializer()
    task_id = serializers.IntegerField(source='id')
    status = serializers.IntegerField(source='Status')

    class Meta:
        model = Field_Inspection_Info
        fields = ["task_id", "assign_date", "execution_date", "status", "contractor"]


class FQP_Test_Serializer(serializers.ModelSerializer):
    test_id = serializers.IntegerField(source='id')

    class Meta:
        model = FQP_Test
        fields = ["test_id", "test_name"]


class FQP_Test_Attributes_Serializer(serializers.ModelSerializer):
    test_parameter = serializers.CharField(source='Test_Attributes')
    parameter_id = serializers.IntegerField(source='id')

    class Meta:
        model = FQP_Test
        fields = ["parameter_id", "test_parameter"]


# for erp
class Erp_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Erp_Data
        fields = ["vendor_name", "vendor_type", "vendor_number", "pan_no", "vendor_site_code",
                  "email_address", "address_1", "address_2", "address_3", "city",
                  "state", "state", "pin", "bank", "branch", "ifsc", "branch_address", "account_no", "gst_no"]


class AreaStoreSerializer(serializers.ModelSerializer):
    store_id = serializers.IntegerField(source='id')

    class Meta:
        model = Store_Info
        fields = "__all__"



# created by shubham tripathi 25/11/2022 for jabalpur discome suggest by yashwant sir 
#  pdi inspection application 
class User_Registration_PdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Registration
        fields = ['Authorised_person_E','ContactNo','Email_Id']

class Emb_MeasurementSerializer(serializers.ModelSerializer):
    Contractor=User_Registration_PdiSerializer(read_only=True) # add by shubham tripathi 24/12/2022 for get officer name and contact number for mobile application 
    class Meta:
        model = Emb_Measurement
        fields = ['id','Feeder_id','Estimate_id','Contractor']



# -------created by shubham tripathi---------------------
class Tier_1_Inspection_RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier_1_Inspection_Representive_data
        fields = '__all__'


class Pdi_Inspection_RepresentativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdi_Inspection_Representive_data
        fields ='__all__'

class UserRegistration_Inspection_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Registration
        fields = ['Authorised_person_E','ContactNo','Email_Id']
class TKCWoInfo_Inspection_Serializer(serializers.ModelSerializer):
    supplier=UserRegistration_Inspection_Serializer()
    class Meta:
        model = TKCWoInfo
        fields = ["supplier","Loa","work_order","wo_no"]    
class Estimate_Serializer(serializers.ModelSerializer):
    TKCWoInfo=TKCWoInfo_Inspection_Serializer()
    class Meta:
        model = TKCWoInfo_Estimate
        fields = ["id","Estimate_No", "Estimate_Name", "Organisation_Name", "Sub_Division", "DC", "Scheme_Name","ERP_Status","Project_Creater","Project_Manager","DOP_Admin","DOP_Admin_Code","DOP_Work","DOP_Work_Code","TKCWoInfo"]
       
class Tier1_Inspection_InfoSerializer(serializers.ModelSerializer):
    # officer=InspectingOfficerInfo_Serializer() # add by shubham tripathi 24/12/2022 for get officer name and contact number for mobile application 
    Estimate = Estimate_Serializer()
    task_id = serializers.IntegerField(source='id')
    status = serializers.IntegerField(source='Status')
    class Meta:
        model = Tier1_Inspection_Info
        fields = ["task_id", "assign_date", "execution_date", "Estimate", "status"]





class PowerAnalyzerSerializer(serializers.Serializer):
    
    pa_test_areastore = serializers.CharField(max_length=500)
    xmr = serializers.CharField(max_length=500)
    ptcode = serializers.CharField(max_length=500, allow_blank=True)
    serial = serializers.CharField(max_length=500, allow_blank=True)
    remark = serializers.CharField(max_length=500, allow_blank=True)
    nlil1 = serializers.FloatField()
    nlil2 = serializers.FloatField()
    nlil3 = serializers.FloatField()
    nlvoltage = serializers.FloatField()

    nlfreq = serializers.FloatField()
    flil1 = serializers.FloatField()
    flil2 = serializers.FloatField()
    flil3 = serializers.FloatField()
    FLfreq = serializers.FloatField()
    FLpower = serializers.FloatField()
    hvAmp = serializers.FloatField()
    FLvoltage = serializers.FloatField()
    Rating = serializers.FloatField()
    Type = serializers.CharField(max_length=500, allow_blank=True)
    NlHvVolts = serializers.FloatField()
    NlLvVolts = serializers.FloatField()
    LVamp = serializers.FloatField()
    Phase = serializers.FloatField()
    VectorGroup = serializers.CharField(max_length=100, allow_blank=True)
    Freq = serializers.IntegerField()
    ImpedenceVolts = serializers.FloatField()
    CoolingType = serializers.CharField(max_length=100, allow_blank=True)
    TempRise = serializers.FloatField()
    OilVolume = serializers.FloatField()
    OilMass = serializers.FloatField()
    CoreWeight = serializers.FloatField()
    TotalWeight = serializers.FloatField()
    MfgYear = serializers.CharField(max_length=500, allow_blank=True)
    WindMaterial = serializers.CharField(max_length=500, allow_blank=True)
    RefStd = serializers.CharField(max_length=500, allow_blank=True)
    OilTest = serializers.CharField(max_length=500, allow_blank=True)
    LoadLoss50 = serializers.FloatField()
    LoadLoss100 = serializers.FloatField()
    MaxHVR = serializers.FloatField()
    MaxLVR = serializers.FloatField()
    FreqTest = serializers.CharField(max_length=500, allow_blank=True)
    OverVoltageTest = serializers.CharField(max_length=500, allow_blank=True)
    Ambient = serializers.FloatField()
    HvRes1 = serializers.FloatField()
    HvRes2 = serializers.FloatField()
    HvRes3 = serializers.FloatField()
    LvRes1 = serializers.FloatField()
    LvRes2 = serializers.FloatField()
    LvRes3 = serializers.FloatField()
    VoltRatio1 = serializers.FloatField()
    VoltRatio2 = serializers.FloatField()
    VoltRatio3 = serializers.FloatField()
    Polarity = serializers.CharField(max_length=500, allow_blank=True)
    IR1 = serializers.FloatField()
    IR2 = serializers.FloatField()
    IR3 = serializers.FloatField()
    NLpower = serializers.FloatField()
    TestDate = serializers.DateTimeField()
    Customer = serializers.CharField(max_length=500, allow_blank=True)
    Transerial = serializers.CharField(max_length=500, allow_blank=True)
    AmbFact = serializers.FloatField()
    Zat75 = serializers.FloatField()
    Zatamb = serializers.FloatField()
    RatAmb = serializers.FloatField()
    XatAnl = serializers.FloatField()
    ZatRoom = serializers.FloatField()
    HvperPhaseAtAmb = serializers.FloatField()
    LVperPhaseAtAmb = serializers.FloatField()
    HVRperphaseat75 = serializers.FloatField()
    LVRperphaseat75 = serializers.FloatField()
    TotalIsqRatAmb = serializers.FloatField()
    StrayLossatAmb = serializers.FloatField()
    StrayLossat75 = serializers.FloatField()
    IsqRat75 = serializers.FloatField()
    TotalLossat75 = serializers.FloatField()
    guarantee50 = serializers.FloatField()
    guarantee100 = serializers.FloatField()
    OrderInfo = serializers.CharField(max_length=500, allow_blank=True)
    OrderDate = serializers.DateTimeField()


    def create(self, validated_data):
        return rca_test_rept_power_analyzer.objects.create(**validated_data)


#  Location Master Serializer
class Discom_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discom_Master
        fields = "__all__"


class Region_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region_Master
        fields = "__all__"


class Circle_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle_Master
        fields = "__all__"


class Division_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division_Master
        fields = "__all__"


class Sub_Division_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Division_Master
        fields = "__all__"


class DC_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DC_Master
        fields = "__all__"
        
class PDI_User_AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='Company_Id')
    CompanyName = serializers.CharField(source='CompanyName_E')

    class Meta:
        model = UserCompanyDataMain
        fields = ["id", "CompanyName", "Company_Contact_No", "Company_Pan_No", "Company_Gst_No", "Company_add_1", "Company_add_2", "Company_pin_code","Company_city",
                  "Company_dist","Company_state", "Company_t_add_1", "Company_t_add_2", "Company_t_pin_code", "Company_t_city",
                  "Company_t_dist","Company_t_state"]
                  
class PDI_User_RegistrationSerializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(source='User_Id')
    Authorised_person = serializers.CharField(source='Authorised_person_E')
    CompanyName = serializers.CharField(source='CompanyName_E')

    class Meta:
        model = User_Registration
        fields = ["vendor_id", "Authorised_person", "CompanyName", "ContactNo", "Email_Id"]

class TKCWoInfo_Serializer(serializers.ModelSerializer):
    supplier = PDI_User_RegistrationSerializer()

    class Meta:
        model = TKCWoInfo
        fields = ["id", "Contract_Number", "supplier"]


class Material_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Details
        fields = ["Material_Name", "Material_Specification"]



class TKC_Vendor_Serializer(serializers.ModelSerializer):
    Vendor = PDI_User_RegistrationSerializer()
    TKCWoInfo = TKCWoInfo_Serializer()
    Material_id = Material_Serializer()

    class Meta:
        model = TKCVendor
        fields = ["id", "Vendor","TKCWoInfo","Material_id","vendor_gtp_file"]

class Material_Offer_Serializer(serializers.ModelSerializer):
    offer_id = serializers.IntegerField(source='id')
    Item_Quantity = serializers.IntegerField(source='Quantity')
    TKCVendor = TKC_Vendor_Serializer()
    class Meta:
        model = Offer_Material
        fields = ["offer_id", "TKCVendor", "Item_Quantity","Calibration_Certificate"]

# class PDI_Inspection_InfoSerializer(serializers.ModelSerializer):
#     Material = Material_Offer_Serializer()
#     task_id = serializers.IntegerField(source='id')
#     status = serializers.IntegerField(source='Status')

#     class Meta:
#         model = PDI_Inspection_Info
#         fields = ["task_id", "assign_date", "execution_date", "Material", "status"]
        




class PDI_Item_InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer_Material_Item_Code
        fields = ["id", "Item_Serial_No"]


class NablDTRReportSerializers(serializers.Serializer):
    # trf_id = serializers.IntegerField(required=False, allow_null=True)
    trf_id =  serializers.CharField(max_length=200, allow_blank=True)
    reportno = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    ulrno = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    manufacturer_wopo = serializers.CharField(max_length=500, allow_blank=True)  # Field name made lowercase.
    manufacturer = serializers.CharField(max_length=500, allow_blank=True)  # Field name made lowercase.
    wo_po = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    srno = serializers.CharField(max_length=200, allow_blank=True)
    lot = serializers.CharField(max_length=200, allow_blank=True)
    mainid = serializers.IntegerField(required=False, allow_null=True)  # Field name made lowercase.
    maindetid = serializers.IntegerField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_tfcondition = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_phase = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_windingtype = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_vector = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_win_descg1 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_win_descg2 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_cooling = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_prim_mva = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_sec_mva = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_prim_ratedvol = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_sec_ratedvol = serializers.FloatField(required=False, allow_null=True) # Field name made lowercase.
    bulkmain_prim_ratedcur = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_sec_ratedcur = serializers.FloatField(required=False, allow_null=True) # Field name made lowercase.
    bulkmain_prim_conn = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_sec_conn = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_prim_not1 = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_prim_not2 = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_prim_not3 = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_prim_not4 = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_sec_not1 = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_sec_not2 = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_sec_not3 = serializers.CharField(max_length=200, allow_blank=True)   # Field name made lowercase.
    bulkmain_sec_not4 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_temp_oil = serializers.FloatField(required=False, allow_null=True) # Field name made lowercase.
    bulkmain_temp_wind = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_windingmaterial = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_metalval = serializers.IntegerField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_refstd = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_jobrating = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_reftemp = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_freq = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_oilleakage = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_oilquantity = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_total_loss = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_tap_changer = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_tapon = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_variation = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    bulkmain_volts1 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_volts2 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_persteps = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    bulkmain_steps = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    torder_scheduleoftest = serializers.CharField(max_length=250, allow_blank=True)  # Field name made lowercase.
    torder_dateofreceipt = serializers.DateTimeField(required=False, allow_null=True)  # Field name made lowercase.
    torder_dateoftestingfrom = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    torder_dateoftestingto = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    torder_dateofissue = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    torder_samplecode = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    torder_customernameaddress = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    torder_note1 = serializers.CharField(max_length=4000, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_note2 = serializers.CharField(max_length=4000, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_note3 = serializers.CharField(max_length=4000, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_note4 = serializers.CharField(max_length=4000, allow_blank=True,allow_null=True)  # Field name made lowercase.
    tfooter_1testedbylabel = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_1testedbyname = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_1testedbydesign = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    tfooter_2checkedbylabel = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_2checkedbyname = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_2checkedbydesign = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    tfooter_3approvedbylabel = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_3approvedbyname = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_3approvedbydesign = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    tfooter_4hodlabel = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_4hodname = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_4hoddesign = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    tfooter_witnessbylabel = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_witnessbyname1 = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_witnessbydesign1 = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    torder_witnessbyname2 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    torder_witnessbydesign2 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    torder_witnessbyname3 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    torder_witnessbydesign3 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    torder_witnessbyname4 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    torder_witnessbydesign4 = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    normaltapno = serializers.IntegerField(required=False, allow_null=True)  # Field name made lowercase.
    totaltapqty = serializers.IntegerField(required=False, allow_null=True)  # Field name made lowercase.
    wr_lot = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_testdate = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    wr_bulkmain_mwrwindphconn = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_bulkmain_mwrwindtol = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_bulkmain_hvunit = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_mwrinputhvu = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_mwrinputhvv = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_mwrinputhvw = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_normaltap_reshvtemp = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reshvu = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reshvv = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reshvw = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reshvavg = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reshv75 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_bulkmain_lvunit = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_mwrinputlvu = serializers.CharField(max_length=200, allow_blank=True) # Field name made lowercase.
    wr_mwrinputlvv = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_mwrinputlvw = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    wr_normaltap_reslvtemp = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reslvu = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reslvv = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reslvw = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reslvavg = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_normaltap_reslv75 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    wr_result = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    vr_lot = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    vr_testdate = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    vr_mratioinputu = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    vr_mratioinputv = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    vr_mratioinputw = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    vr_normaltap_hvrated = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    vr_normaltap_lvrated = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    vr_normaltap_calratio = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    vr_normaltap_ratiou = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    vr_normaltap_ratiov = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    vr_normaltap_ratiow = serializers.FloatField(required=False, allow_null=True) # Field name made lowercase.
    vr_normaltap_acccritdata = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    vr_vectordetected = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    vr_result = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    ir_lot = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    ir_testdate = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    ir_time = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_temp = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_reshve = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_reslve = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_reshvlv = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_hve_volt = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_lve_volt = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_hvlv_volt = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ir_result = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    nll_lot = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    nll_testdate = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    nll_bulkmain_nllguar = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_ptr = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    nll_normaltap_ctr = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    nll_normaltap_frq = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_vrms = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_vmean = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_i1 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_i2 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_i3 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_iavg = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_w1 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_w2 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_w3 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_pmeasured = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_normaltap_pcorrected = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    nll_result = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    ll_lot = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    ll_testdate = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    ll_bulkmain_llguar50 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_bulkmain_llguar100 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_ptr = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    ll_normaltap_ctr = serializers.CharField(max_length=200, allow_blank=True)  # Field name made lowercase.
    ll_normaltap_50per_temp = serializers.FloatField(required=False, allow_null=True) # Field name made lowercase.
    ll_normaltap_50per_frq = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_vmeas = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_i1 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_i2 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_i3 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_imeas = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_w1 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_w2 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_w3 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_pmeasured = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_llat75 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_50per_zat75 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_temp = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_frq = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_vmeas = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_i1 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_i2 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_i3 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_imeas = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_w1 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_w2 = serializers.FloatField(required=False, allow_null=True) # Field name made lowercase.
    ll_normaltap_100per_w3 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_pmeasured = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_llat75 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_normaltap_100per_zat75 = serializers.FloatField(required=False, allow_null=True)  # Field name made lowercase.
    ll_percimpedancevoltreq = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_percimpedancevoltobtained = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_percimpedancevoltremark = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_totalloss50perreq = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_totalloss50perobtained = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_totalloss50perremark = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_totalloss100perreq = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_totalloss100perobtained = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    ll_totalloss100perremark = serializers.CharField(max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    hvt_iovt_lot = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    hvt_iovt_testdate = serializers.DateTimeField(required=False, allow_null=True)   # Field name made lowercase.
    hvt_iovt_ptr = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    hvt_iovtctr = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    hvt_hvdetail = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase. This field type is a guess.
    hvt_lvdetail = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase. This field type is a guess.
    hvt_result = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    iovt_hvdetail = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase. This field type is a guess.
    iovt_result = serializers.CharField(required=False, max_length=200, allow_blank=True,allow_null=True)  # Field name made lowercase.
    
    discom = serializers.CharField(required=False, max_length=200, allow_blank=True) #CZ<WZ<EZ
    nabl_id = serializers.CharField(required=False, max_length=200, allow_blank=True)
    nabl_name = serializers.CharField(required=False, max_length=200, allow_blank=True)
    xmr_id = serializers.CharField(required=False, max_length=200, allow_blank=True)

    
    result_pass_fail = serializers.CharField(required=False, max_length=10, allow_blank=True)
    remark = serializers.CharField(required=False, max_length=5000, allow_blank=True)
    report_file = serializers.CharField(required=False, max_length=200, allow_blank=True)
    user_id = serializers.IntegerField(required=False, allow_null=True, default=0)
    rating = serializers.CharField(required=False, max_length=200, allow_blank=True)
    location = serializers.CharField(required=False, max_length=200, allow_blank=True)

    def create(self, validated_data):
        return NablDTRReport.objects.create(**validated_data)


class Vendor_Material_Details_Serializer_shubham(serializers.ModelSerializer):
    user_id = User_RegistrationSerializer()

    class Meta:
        model = Vendor_Material_Details
        fields = ["id","user_id", "Material_Name", "Material_Specification", "Status"]





class PDI_RegistrationSerializer(serializers.ModelSerializer):
    vendor_id = serializers.IntegerField(source='User_Id')
    Authorised_person_E = serializers.CharField()
    CompanyName = serializers.CharField(source='CompanyName_E')

    class Meta:
        model = User_Registration
        fields = ["vendor_id", "Authorised_person_E", "CompanyName", "ContactNo", "Email_Id"]


class Multiple_Material_Offer_Serializer(serializers.ModelSerializer):
    supplier=PDI_RegistrationSerializer()
    offer_id = serializers.IntegerField(source='id')
    
    TKCVendor = TKC_Vendor_Serializer()
    class Meta:
        model = offer_material_site_stores
        fields = ["offer_id", "TKCVendor", "supplier", "Calibration_Certificate"]
        

class PDI_Inspection_InfoSerializer(serializers.ModelSerializer):
    Material = Multiple_Material_Offer_Serializer()
    task_id = serializers.IntegerField(source='id')
    status = serializers.IntegerField(source='Status')

    class Meta:
        model = PDI_Inspection_Info
        fields = ["task_id", "Material", "assign_date", "execution_date", "status","offer_no","offer_date","vendor_name","vendor_address","inspection_date","tkc_name","letter_report"]


class PDI_Material_Serializer(serializers.ModelSerializer):
    Status = serializers.IntegerField(source='PDI_Complete')
    class Meta:
        model = offer_material_site_stores
        fields = ["Status"]

class PDI_Material_InfoSerializer(serializers.ModelSerializer):
    Material = PDI_Material_Serializer()
    material_name = serializers.CharField()
    item_code = serializers.CharField()

    class Meta:
        model = PDI_Inspection_Info
        fields = ["material_name", "item_code","Material"]



# ----- shubham tripathi work started from 9 march fqp intimation data---------------------------

# class FqpIntimation_WorkOrder_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = TKCWoInfo
#         fields = ["id","wo_no","Contract_Number","Contract_Date"]

class Fqp_Region_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region_Master
        fields = ["id","Region_Code","Region_Name_E"]

class Fqp_Circle_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle_Master
        fields = ["id","Circle_Code","Circle_Name_E"]

class Fqp_Division_MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division_Master
        fields = ["id","Division_Code","Division_Name_E"]


class FqpIntimation_TkcHeader_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TKCWoInfo_Header
        fields = ["id","Contract_Description"]

# class FqpIntimation_TkcHeader_Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = FqpIntimation
#         fields = ["id","Contract_Description"]

# class TKCWoInfo_Intimation_Serializer(serializers.ModelSerializer):
#     work_order_description = serializers.CharField(source='Header.Contract_Description')
#     supplier=UserRegistration_Inspection_Serializer()
#     # Region=Fqp_Region_MasterSerializer(read_only=True)
#     # Circle=Fqp_Circle_MasterSerializer(read_only=True)
#     # division=Fqp_Division_MasterSerializer(read_only=True)
#     class Meta:
#         model = TKCWoInfo
#         fields = ["id","wo_no",'supplier',"Contract_Number","Region","Circle","Contract_Date","work_order","work_order_description"]    

class FqpIntimation_UserCompanyDataMain_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompanyDataMain
        fields = ['CompanyName_E']

class FqpIntimation_UserRegistration_Inspection_Serializer(serializers.ModelSerializer):
    user_id_id = FqpIntimation_UserCompanyDataMain_Serializer(many=True,read_only=True)
    class Meta:
        model = User_Registration
        fields = ['Authorised_person_E','ContactNo','User_Id','user_id_id','CompanyName_E']

class TKCWoInfo_fqpintimation_Serializer(serializers.ModelSerializer):
    work_order_description = serializers.CharField(source='Header.Contract_Description')
    supplier=FqpIntimation_UserRegistration_Inspection_Serializer()
    # Region=Fqp_Region_MasterSerializer(read_only=True)
    # Circle=Fqp_Circle_MasterSerializer(read_only=True)
    class Meta:
        model = TKCWoInfo
        fields = ["id","wo_no",'supplier',"Contract_Number","work_order","work_order_description"]    


class FqpIntimation_Serializer(serializers.ModelSerializer):
    wo=TKCWoInfo_fqpintimation_Serializer(read_only=True)
    region=Fqp_Region_MasterSerializer(read_only=True)
    circle=Fqp_Circle_MasterSerializer(read_only=True)
    division=Fqp_Division_MasterSerializer(read_only=True)
    class Meta:
        model=FqpIntimation
        fields=["id", "wo", "region", "circle", "division", "work_execution_detail",  "brief_description_of_work",  "work_execution_milestone_pdf", "layout_sld_of_work_execution",  "tentative_date_of_execution", 'intimation_status',"remark"]

class MilestoneMain_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Milestone_Main
        fields=['id','milestone_name']

class MilestoneMainCategory_Serializer(serializers.ModelSerializer):
    milestone_main=MilestoneMain_Serializer(read_only=True)
    class Meta:
        model=Milestone_Main_Category
        fields=["id","milestone_main",'milestone_category_name']

class MilestoneMainSubcategory_Serializer(serializers.ModelSerializer):
    milestone_main_category = MilestoneMainCategory_Serializer(read_only=True)
    class Meta:
        model=Milestone_Main_SubCategory
        fields=["id", "milestone_main_category","milestone_subcategory_name"]


class MilestoneMainSubcategory_Data_Serializer(serializers.ModelSerializer):
    milestone_main_subcategory = MilestoneMainSubcategory_Serializer(read_only=True)
    class Meta:
        model=Milestone_Main_SubCategory_Data
        fields='__all__'

class FqpIntimation_Observation_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FqpIntimation_Observation_Info
        fields =['fqpintimation', 'wo', 'milestone_subcategory_data', 'observation_remark', 'observation_image','observation_location','observation_lat','observation_long','observation_status']

    def validate(self, data):

        required_fields = ['fqpintimation', 'wo', 'milestone_subcategory_data', 'observation_remark', 'observation_image','observation_location','observation_lat','observation_long','observation_status'] # replace with your own required fields
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required.")
        return data

class FqpIntimation_Officer_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FqpIntimation_Officer_Info
        fields = ['fqpintimation', 'officer_fullname', 'officer_mobile' ,'officer_designation','representative_from']

    def validate(self, data):
        required_fields = ['fqpintimation', 'officer_fullname','officer_mobile' ,'officer_designation','representative_from'] # replace with your own required fields
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required.")
        return data

class FqpIntimation_Observation_Close_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FqpIntimation_Observation_Close
        fields = ['fqpintimation','close_remark', 'image_1', 'image_2', 'image_3','close_lat','close_long']

    def validate(self, data):
        required_fields = ['fqpintimation','close_remark', 'image_1', 'image_2', 'image_3','close_lat','close_long']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required.")
        return data

class FqpIntimation_Officer_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model=FqpIntimation_Officer_Info
        fields='__all__'


#-----------------START OF SERIALIZER BY RAVINDRA----------------------------------------------#

class vendor_master_serial(serializers.ModelSerializer):
    class Meta:
        model = User_Registration
        fields = ('User_Id', 'CompanyName_E')


class vendor_material_serial(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Details
        fields = ('id','user_id', 'Material_Specification','item_code')
        
class vendor_material_serial_2(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Material_Details
        fields = ('id','item_code')
        
        
        
#-----------------END OF SERIALIZER BY RAVINDRA----------------------------------------------#  

#-----------------START OF FQP SERIALIZER BY RAVINDRA----------------------------------------------#  


class fqp_check_status_serializer(serializers.ModelSerializer):
    class Meta:
        model=fqp_check_status
        fields=['feeder_id','FQP_response']
        
class fqp_check_status_save_serializer(serializers.ModelSerializer):
    class Meta:
        model=fqp_check_status_save
        fields=['feeder_id']

        
        
#-----------------END OF FQP SERIALIZER BY RAVINDRA----------------------------------------------#  


class works_master_serializer(serializers.ModelSerializer):
    class Meta:
        model= works_master
        fields = '__all__'
        
        

        
class User_Registration_serializer(serializers.ModelSerializer):
    
    class Meta:
        model= User_Registration
        fields = ('User_Id','Authorised_person_E', 'CompanyName_E', 'ContactNo')
        
class UserCompanyDataMain_serializer(serializers.ModelSerializer):
    user_id_id = User_Registration_serializer()
    class Meta:
        model= UserCompanyDataMain
        fields = ('user_id_id', 'Company_add_1', 'Company_add_2')
        
        
        
        
class User_Registration_serializer_2(serializers.ModelSerializer):
    
    class Meta:
        model= User_Registration
        fields = ['CompanyName_E']
        
        
class TKCWoInfo_Header_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TKCWoInfo_Header
        fields = ['Contract_Description']
        

class package_serializer(serializers.ModelSerializer):
    class Meta:
        model = works_master
        fields = ['package_name']       

          
        

class work_order_Serializer(serializers.ModelSerializer):
    Header = TKCWoInfo_Header_Serializer(many=False)
    supplier = User_Registration_serializer_2()    
    package = package_serializer(many=False, source='pakage')
    loa_date = serializers.DateField(source='Contract_Date')   
    class Meta:
        model=TKCWoInfo   
        fields = ['Header', 'supplier', 'loa_amount', 'Contract_Number', 'zone', 'loa_date', 'package']
        # fields = '__all__' 

        
class work_order_Serializer_2(serializers.ModelSerializer):
    Header = TKCWoInfo_Header_Serializer(many=False)
    supplier = User_Registration_serializer_2()    
    package = package_serializer(many=False, source='pakage')      
    class Meta:
        model=TKCWoInfo   
        fields = ['Header', 'supplier', 'Contract_Number', 'zone', 'package']
        # fields = '__all__' 


# ---------shubham trippatin new fqpintimation code staryt from here -----date 11/7/2023------


# ----- shubham tripathi work started from 9 march fqp intimation data---------------------------


class UserCompanyDataMain_New_FqpIntimation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompanyDataMain
        fields = ['CompanyName_E']

class UserRegistration_Inspection_New_FqpIntimation_Serializer(serializers.ModelSerializer):
    user_id_id = UserCompanyDataMain_New_FqpIntimation_Serializer(many=True,read_only=True)
    class Meta:
        model = User_Registration
        fields = ['Authorised_person_E','ContactNo','User_Id','user_id_id','CompanyName_E']

class TKCWoInfo_New_Fqpintimation_Serializer(serializers.ModelSerializer):
    work_order_description = serializers.CharField(source='Header.Contract_Description',allow_null=True)
    supplier=UserRegistration_Inspection_New_FqpIntimation_Serializer()
    class Meta:
        model = TKCWoInfo
        fields = ["id","wo_no",'supplier',"Contract_Number","work_order","work_order_description"]    


class TKCWoInfo_Workorder_List_New_Fqpintimation_Serializer(serializers.ModelSerializer):
    work_order_description = serializers.CharField(source='Header.Contract_Description',allow_null=True)
    supplier_Authorised_person_E = serializers.CharField(source='supplier.Authorised_person_E',allow_null=True)
    supplier_ContactNo = serializers.CharField(source='supplier.ContactNo',allow_null=True)
    supplier_User_Id = serializers.CharField(source='supplier.User_Id',allow_null=True)
    supplier_CompanyName_E = serializers.CharField(source='supplier.CompanyName_E',allow_null=True)
    # supplier=UserRegistration_Inspection_New_FqpIntimation_Serializer()
    class Meta:
        model = TKCWoInfo
        fields = ['id',"wo_no","Contract_Number",'supplier_Authorised_person_E','supplier_ContactNo','supplier_User_Id','supplier_CompanyName_E',"work_order","work_order_description"]    


class Work_Order_Task_Workorder_List_New_FqpIntimation_Serializer(serializers.ModelSerializer):
    wo=TKCWoInfo_Workorder_List_New_Fqpintimation_Serializer(read_only=True)
    region_name = serializers.CharField(source='region.Region_Name_E',allow_null=True)
    circle_name = serializers.CharField(source='circle.Circle_Name_E',allow_null=True)
    division_name = serializers.CharField(source='division.Division_Name_E',allow_null=True)
    distribution_center_name = serializers.CharField(source='distribution_center.DC_Name_E',allow_null=True)
    class Meta:
        model=Wo_Order_Task
        fields=["wo","region_name","circle_name","division_name","distribution_center_name"]

class New_FqpIntimation_Workorder_List_Serializer(serializers.ModelSerializer):# for getting work-order list page data
    wo_task = Work_Order_Task_Workorder_List_New_FqpIntimation_Serializer(read_only =True)
    # wo = TKCWoInfo_Workorder_List_New_Fqpintimation_Serializer(read_only =True)
    class Meta:
        model=New_FqpIntimation
        fields=["wo_task"]

class Work_Order_Task_List_New_FqpIntimation_Serializer(serializers.ModelSerializer):
    wo=TKCWoInfo_Workorder_List_New_Fqpintimation_Serializer(read_only=True)
    region_name = serializers.CharField(source='region.Region_Name_E',allow_null=True)
    circle_name = serializers.CharField(source='circle.Circle_Name_E',allow_null=True)
    division_name = serializers.CharField(source='division.Division_Name_E',allow_null=True)
    distribution_center_name = serializers.CharField(source='distribution_center.DC_Name_E',allow_null=True)
    class Meta:
        model=Wo_Order_Task
        fields=fields=["id","region_name","circle_name","division_name","distribution_center_name",  "gis_feeder_id", "erp_estimate_no",  "erp_gbpa_no", "package_name_and_no",  "feeder_name_on_which_work_proposed", 'substation_name_on_which_work_proposed', "wo"]


#  for getting task list page data
class New_FqpIntimation_Task_List_Serializer(serializers.ModelSerializer): # for getting task list page data
    wo_task = Work_Order_Task_List_New_FqpIntimation_Serializer(read_only =True)
    # wo = TKCWoInfo_Workorder_List_New_Fqpintimation_Serializer(read_only =True)
    class Meta:
        model=New_FqpIntimation
        fields=["wo_task"]

# intimation all milestone category list intimation wise
class New_FqpIntimation_Milestone_Category_Serializer(serializers.ModelSerializer):  # for getting intimation list page data
    # fqpintimation_id = serializers.CharField(source='fqpintimation.id',allow_null=True)
    milestone_id = serializers.CharField(source='fqpintimation.wotask_milestone.milestone.id',allow_null=True)
    milestone_category_id = serializers.CharField(source='milestone_category.id',allow_null=True)
    milestone_category_name = serializers.CharField(source='milestone_category.milestone_category_name',allow_null=True)
    class Meta:
        model=New_FqpIntimation_milestone_category
        fields=["id","milestone_id","milestone_category_id", "milestone_category_name"]

# for getting intimation list page data
class New_FqpIntimation_List_Serializer(serializers.ModelSerializer):  
    wo_task = Work_Order_Task_List_New_FqpIntimation_Serializer(read_only =True)
    wotask_milestone_id = serializers.CharField(source='wotask_milestone.milestone.id',allow_null=True)
    wotask_milestone_name = serializers.CharField(source='wotask_milestone.milestone.milestone_name',allow_null=True)
    # newfqp_milestone_category=New_FqpIntimation_Milestone_Category_Serializer(many=True,read_only=True)
    class Meta:
        model=New_FqpIntimation
        fields=["id","intimation_unique_no","wotask_milestone_id","wotask_milestone_name", "work_execution_detail",  "brief_description_of_work",  "work_execution_milestone_image1", "work_execution_milestone_image2", "date_of_execution", "date_of_readines", "date_of_completion", "intimation_status","wo_task"]



#   new fqp intimation ----- milestone subcategory list
class New_FqpIntimation_MilestoneMainSubcategory_Serializer(serializers.ModelSerializer):
    milestone_id = serializers.CharField(source='milestone_main_category.milestone_main.id',allow_null=True)
    class Meta:
        model=Milestone_Main_SubCategory
        fields=["id","milestone_id", "milestone_main_category_id", "milestone_subcategory_name"]

#   new fqp intimation ----- milestone subcategory data list
class New_FqpIntimation_MilestoneMainSubcategory_Data_Serializer(serializers.ModelSerializer):
    milestone_id = serializers.CharField(source='milestone_main_subcategory.milestone_main_category.milestone_main.id',allow_null=True)
    milestone_main_category_id = serializers.CharField(source='milestone_main_subcategory.milestone_main_category.id',allow_null=True)
    class Meta:
        model=Milestone_Main_SubCategory_Data
        fields='__all__'


#  for save new fqp intimation observation info detail
class New_FqpIntimation_Observation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = New_FqpIntimation_Observation
        fields =['officer','fqpintimation',"milestone_main_category",'milestone_subcategory_data', 'observation_remark', 'observation_image','observation_location','observation_lat','observation_long','observation_status','new_fqpintimation_milestone_category']

    def validate(self, data):

        required_fields = ['officer','fqpintimation',"milestone_main_category", 'milestone_subcategory_data', 'observation_remark', 'observation_image','observation_location','observation_lat','observation_long','observation_status','new_fqpintimation_milestone_category'] # replace with your own required fields
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required.")
        return data

#  serial_izer task wise for ankit sir api 
class EMB_New_FqpIntimation_Observation_List_Serializer(serializers.ModelSerializer):
    milestone_name = serializers.CharField(source='milestone_subcategory_data.milestone_main_subcategory.milestone_main_category.milestone_main.milestone_name',allow_null=True)
    milestone_main_category_name = serializers.CharField(source='milestone_subcategory_data.milestone_main_subcategory.milestone_main_category.milestone_category_name',allow_null=True)
    milestone_subcategory_name = serializers.CharField(source='milestone_subcategory_data.milestone_main_subcategory.milestone_subcategory_name',allow_null=True)
    milestone_subcategory_data = serializers.CharField(source='milestone_subcategory_data.activity_and_operation',allow_null=True)
    class Meta:
        model = New_FqpIntimation_Observation
        fields =["id","milestone_name",'milestone_main_category_name', "milestone_subcategory_name",'milestone_subcategory_data', 'observation_remark', 'observation_image','observation_location','observation_lat','observation_long','observation_status']

class EMB_New_FqpIntimation_Intimation_List_Serializer(serializers.ModelSerializer):
    new_fqp_observation_detail=EMB_New_FqpIntimation_Observation_List_Serializer(many=True,read_only=True)
    newfqp_milestone_category=New_FqpIntimation_Milestone_Category_Serializer(many=True,read_only=True)
    wotask_milestone_name = serializers.CharField(source='wotask_milestone.milestone.milestone_name',allow_null=True)
    class Meta:
        model = New_FqpIntimation
        fields =["id","intimation_unique_no","wotask_milestone_name", "work_execution_detail",  "brief_description_of_work",  "work_execution_milestone_image1", "work_execution_milestone_image2", "date_of_execution", "date_of_readines", "date_of_completion", "intimation_status","wo_task","newfqp_milestone_category","new_fqp_observation_detail"]

class Emb_Measurement_New_Fqpintimation_Serializer(serializers.ModelSerializer):
    wo=TKCWoInfo_Workorder_List_New_Fqpintimation_Serializer(read_only=True)
    newfqp_intimation_data=EMB_New_FqpIntimation_Intimation_List_Serializer(many=True,read_only=True)
    class Meta:
        model=Wo_Order_Task
        fields=fields=["id", "gis_feeder_id", "erp_estimate_no",  "erp_gbpa_no", "package_name_and_no",  "feeder_name_on_which_work_proposed", 'substation_name_on_which_work_proposed', "wo","newfqp_intimation_data"]


class OfficerMainSerializer(serializers.ModelSerializer):  #officer login id  for new fqpintimation 
    class Meta:
        model=Officer
        fields="__all__"


class New_FqpIntimation_Observation_Close_Serializer(serializers.ModelSerializer):
    class Meta:
        model = New_FqpIntimation_Observation_Close
        fields = ['officer','fqpintimation','close_remark', 'image_1', 'image_2', 'image_3','close_lat','close_long']
    def validate(self, data):
        required_fields = ['officer','fqpintimation','close_remark', 'image_1', 'image_2', 'image_3','close_lat','close_long']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required.")
        return data

class New_FqpIntimation_Officer_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = New_FqpIntimation_Officer_Info
        fields = ['officer','fqpintimation', 'officer_fullname', 'officer_mobile' ,'officer_designation','representative_from']

    def validate(self, data):
        required_fields = ['officer','fqpintimation', 'officer_fullname','officer_mobile' ,'officer_designation','representative_from'] # replace with your own required fields
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required.")
        return data


class Officer_Main_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Officer
        fields = ['employ_id','employ_name', 'designation', 'role' ,'mobile','user_zone','Discom','rank','Posted']

class New_FqpIntimation_Officer_Info_List_Serializer(serializers.ModelSerializer):
    officer=Officer_Main_List_Serializer(read_only=True)
    class Meta:
        model = FqpIntimation_Officer_Info
        fields = ['officer','fqpintimation', 'officer_fullname', 'officer_mobile' ,'officer_designation','representative_from']




# ---------------end here------------------------------------------------------------
# ---------created by pd mishra -------------------------------------------
class Inspecting_officer(serializers.ModelSerializer):
    class Meta:
        model = InspectingOfficerInfo
        fields = ['id','officer_name','contact_no','officer_email','officer_employ_id','officer_designation','officer_password','officer_address','officer_region']
