from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(OwnerShip_Type_Table_Master)
class UserRegistration(admin.ModelAdmin):
    list_display = ['User_Id','Authorised_person_E','ContactNo','CompanyName_E', 'User_type','User_zone','cgm_approval' ]
    search_fields = ('Authorised_person_E','CompanyName_E', 'User_Id','ContactNo')
admin.site.register(UserCompanyDataMain)
admin.site.register(AuthorisedPerson)
admin.site.register(BankDetails)
admin.site.register(Role_Master)
class OfficerData(admin.ModelAdmin):
    list_display = ['employ_id','employ_name','employ_login_id', 'role','mobile','Discom','Region','Circle',]
    list_filter = ['role','Discom','Circle']
    search_fields = ('employ_login_id','employ_name','mobile')
admin.site.register(PO_Type_Table_Master)
admin.site.register(User_Registration,UserRegistration)
admin.site.register(Officer,OfficerData)
admin.site.register(PO_Clause_Master)
admin.site.register(PO_Type_Clause)
admin.site.register(VendorDispatchInfo)
admin.site.register(InspectingOfficerInfo)
admin.site.register(LocalStoreInventory)
admin.site.register(VendorDispatchItemInfo)
admin.site.register(FI_Officer)
admin.site.register(Payudata_main)
admin.site.register(Sampling_Info)
admin.site.register(product_sampling)

####Anupam....

admin.site.register(Factory_Inspection_Info)
admin.site.register(RCA_Factory_Inspection_Info)
admin.site.register(sample_code_table)
admin.site.register(teachincal_officer_table)


admin.site.register(User_Registration_Check_Status)
admin.site.register(Store_Info)
admin.site.register(Material_Inspection_Info)

class GatepassRoIdUser(admin.ModelAdmin):
    list_display = ('roid', 'User', 'Zone',)
    search_fields = ('roid',)
    list_filter = ('TRF_Id','roid',)

admin.site.register(Add_material_nabl, GatepassRoIdUser)
#admin.site.register(Add_material_nabl)

admin.site.register(Add_material_rca)
admin.site.register(teachincal_officer_table_rca)
admin.site.register(sample_code_table_rca)

admin.site.register(certificate_details)
admin.site.register(Sample_Document)
admin.site.register(Field_Inspection_Info)

admin.site.register(blacklistedSaved)



# TTTTTTTTTTT
admin.site.register(Exam_Data)


admin.site.register(RCA_Cell)

# Location Master
admin.site.register(Discom_Master)
admin.site.register(Region_Master)
admin.site.register(Circle_Master)
admin.site.register(Division_Master)
admin.site.register(Sub_Division_Master)
admin.site.register(DC_Master)



admin.site.register(Vendor_Material_Master)
admin.site.register(Vendor_Material_Specification_Master)
admin.site.register(Nabl_Is_Master)
admin.site.register(Nabl_Acceptance_Test_Master)
admin.site.register(AreaStore_Officer)
admin.site.register(PDI_Inspection_Info)

admin.site.register(Add_material_nabl_outward)


admin.site.register(message_template_log)

# Neha
admin.site.register(UOM_Master)
admin.site.register(reject_and_approve_summary)


#---------shubham tripathi code start here
admin.site.register(InvoiceType)
admin.site.register(Invoice)
admin.site.register(InvoiceHistory)
admin.site.register(Pdi_Inspection_Representive_data)

# -----add by shubham tripathi for fqp intimation at 8 march 2022------
admin.site.register(Milestone_Main)
admin.site.register(Milestone_Main_Category)
admin.site.register(Milestone_Main_SubCategory)
admin.site.register(Milestone_Main_SubCategory_Data)
#---add by PDMishra for Factory inspection----
admin.site.register(Factory_Inspection_Info_history) 

