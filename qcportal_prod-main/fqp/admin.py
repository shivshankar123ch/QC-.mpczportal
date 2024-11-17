from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TKCScheduleInfo)
admin.site.register(FQP_Test)
admin.site.register(FQP_Test_Attributes)

admin.site.register(FQP_Material)
admin.site.register(FQP_Officers)
# admin.site.register(FQP_Officer_Task)
admin.site.register(FQP_Test_Data)
admin.site.register(tkc_di_master)


#
admin.site.register(TKCWoInfo)
admin.site.register(TKCWoInfo_Header)
admin.site.register(TKCWoInfo_Contract_Price)
admin.site.register(TKCWoInfo_Advance)
admin.site.register(TKCWoInfo_Advance_Type)

admin.site.register(TKCWoInfo_Time_Schedule)
admin.site.register(TKCWoInfo_Schedule_Supply)
admin.site.register(TKCWoInfo_Schedule_Installation)
admin.site.register(TKCWoInfo_Schedule_Supply_Item)
admin.site.register(TKCWoInfo_Schedule_Installation_Item)
admin.site.register(TKCWoInfo_Variable_Item)
admin.site.register(TKCWoInfo_Major_Item)
admin.site.register(TKCWoInfo_Copy_To)
# new
admin.site.register(TKCWoInfo_Bg_Type)
admin.site.register(TKCWoInfo_Pert)

admin.site.register(TKCOtherDocuments)

admin.site.register(TKC_MqpPlanDocuments)
admin.site.register(TKC_FqpPlanDocuments)

admin.site.register(TKCWoInfo_Bg)
admin.site.register(TKCWoInfo_LOC)

admin.site.register(TKCVendor)
# admin.site.register(TKCVendorMaterial)
admin.site.register(Offer_Material)
admin.site.register(PDI_Factory_image)
admin.site.register(Offer_Material_Item_Code)


admin.site.register(Tier_1_Test_Item)
admin.site.register(Tier_1_Test_Item_Type)
admin.site.register(Tier_1_Test_Item_Type_Inspection_List)

admin.site.register(Fqp_Work_Order_Trf_Details)
admin.site.register(fqp_wo_nabl_gatepass)
admin.site.register(offer_material_divisions_data)
admin.site.register(tkc_wo_items_boq)

admin.site.register(tkc_update_boq)
admin.site.register(Tag_Circle)
admin.site.register(tkc_requested_boq_item)


#  add by shubham tripathi
admin.site.register(FqpIntimation)
admin.site.register(FqpIntimation_Observation_Info)
admin.site.register(FqpIntimation_Officer_Info)
admin.site.register(FqpIntimation_Observation_Close)

admin.site.register(Wo_Order_Task)
admin.site.register(Wo_Task_Milestone)
admin.site.register(New_FqpIntimation)
admin.site.register(New_FqpIntimation_milestone_category)
admin.site.register(New_FqpIntimation_Observation)
admin.site.register(New_FqpIntimation_Observation_data)
admin.site.register(New_FqpIntimation_Officer_Info)
admin.site.register(New_FqpIntimation_Observation_Close)
# ----------------end here----------------------------------


admin.site.register(fqp_check_status) #by ravindra
admin.site.register(fqp_check_status_save) #by ravindra

