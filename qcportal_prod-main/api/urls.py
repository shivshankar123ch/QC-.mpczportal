from django.contrib import admin
from django.urls import path

from api import views

from .views import *

# from .views import GeneratePdf

urlpatterns = [
    path('getInspectingData/<int:pk>', views.getInspectingData.as_view(), name="getInspectingData"), # by PD MISHRA
    path('get_vendor/', views.get_vendor, name="get_vendor"),#by ravindra
    path('get_vendor_material/<int:id>', views.get_vendor_material, name="get_vendor_material"),#by ravindra
    path('get_vendor_material_2/<int:id>', views.get_vendor_material_2, name="get_vendor_material_2"),#by ravindra

    path('material_specification', views.material_specification, name="material_specification"),
    path('material_master/', views.material_master, name="material_master"),
    path('material_specification_master/<int:id>', views.material_specification_master, name="material_specification_master"),
    path('material_is_master/<int:id>', views.material_is_master, name="material_is_master"),
    path('material_test_master/<int:id>', views.material_test_master, name="material_test_master"),
    path('material_fetch/<int:id>', views.material_featch, name="material_fetch"),
    path('material_test_fetch/<int:id>', views.material_test_fetch, name="material_test_fetch"),

    # -----------jeevan---------------------------
    path('no_verification', views.no_verification, name="no_verification"),
    path('otp_generate', views.otp_generate, name="otp_generate"),
    path('fi_login', views.FI_Login, name="FI_Login"),
    path('fi_inspection_list', views.FI_Inspection_List, name="FI_Inspection_List"),
    path('fi_inspection_record', views.FI_Inspection_Record, name="FI_Inspection_Record"),
    path('fi_inspection_deny', views.FI_Inspection_Deny, name="FI_Inspection_Deny"),
    path('fi_document_list', views.FI_Document_List, name="FI_Document_List"),
    path('fi_document_verify', views.FI_Document_Verify, name="FI_Document_Verify"),
    path('fi_technical_detail', views.FI_Technical_Details, name="FI_Technical_Details"),
    path('fi_material_list', views.FI_Material_List, name="FI_Material_List"),
    path('fi_material_verify', views.FI_Material_Verify, name="FI_Material_Verify"),
    path('fi_appraisal_detail', views.FI_Appraisal, name="FI_Appraisal"),
    path('fi_image', views.FI_Factory_Data, name="FI_Factory_Data"),
    path('rca_fi_document_response', views.RCA_FI_Document_Response, name="RCA_FI_Document_Response"),
    # -----------jeevan--------FQP ---------------------------
    path('fqp_login', views.FQP_Login, name="FQP_Login"),
    path('fqp_inspection_list', views.FQP_Inspection_List, name="FQP_Inspection_List"),
    path('fqp_inspection_record', views.FQP_Inspection_Record, name="FQP_Inspection_Record"),
    path('fqp_inspection_deny', views.FQP_Inspection_Deny, name="FQP_Inspection_Deny"),
    path('fqp_test_list', views.FQP_Test_List, name="FQP_Test_List"),
    path('fqp_test_parameter', views.FQP_Test_Parameter, name="FQP_Test_Parameter"),
    path('fqp_test_result', views.FQP_Test_Result, name="FQP_Test_Result"),
    path('fqp_inspection_end', views.FQP_Inspection_End, name="FQP_Inspection_End"),
    # -----------jeevan--------MQP ---------------------------
    path('mqp_login', views.MQP_Login, name="MQP_Login"),
    path('mqp_inspection_list', views.MQP_Inspection_List, name="MQP_Inspection_List"),
    path('mqp_material_list', views.MQP_Material_List, name="MQP_Material_List"),
    path('mqp_material_verify', views.MQP_Material_Verify, name="MQP_Material_Verify"),
    path('mqp_inspection_deny', views.MQP_Inspection_Deny, name="MQP_Inspection_Deny"),
    path('mqp_inspection_submit', views.MQP_Inspection_Submit, name="MQP_Inspection_Submit"),


    path('erp_test', views.Erp_Test, name="Erp_Test"),


        # -----------jeevan--------erp ---------------------------
    path('PO_info', views.PO_info, name="PO_info"),
    path('PO_info1', views.PO_info1, name="PO_info1"),


    #------------jeevan--------- Location Master ---------------------
    path('discom_master/', views.discom_master, name="discom_master"),
    path('region/<int:id>', views.region, name="region"),
    path('circle/<int:id>', views.circle, name="circle"),
    path('division/<int:id>', views.division, name="division"),
    path('sub_division/<int:id>', views.sub_division, name="sub_division"),
    path('dc/<int:id>', views.dc, name="dc"),
    path('pdi_login', views.PDI_Login, name="PDI_Login"),
    path('pdi_inspection_list', views.PDI_Inspection_List, name="PDI_Inspection_List"),
    path('pdi_material_list', views.PDI_Material_List, name="PDI_Material_List"),
    path('pdi_item_serial', views.PDI_Item_Serial, name="PDI_Item_Serial"),
    path('pdi_user_address', views.PDI_User_Address, name="PDI_User_Address"),
    path('pdi_inspection_record', views.PDI_Inspection_Record, name="PDI_Inspection_Record"),
    path('pdi_inspection_deny', views.PDI_Inspection_Deny, name="PDI_Inspection_Deny"),
    path('pdi_response', views.PDI_Response, name="PDI_Response"),
    
    path('tier1_inspection_response', views.Tier1_Inspection_Response, name="Tier1_Inspection_Response"),
    path('NablReportData', views.NablReportData, name="NablReportData"),
    # created by shubham tripathi 25/11/2022 for jabalpur discome suggest by yashwant sir 
    path('Emb_Measurement_Detail', views.Emb_Measurement_Detail, name="Emb_Measurement_Detail"),

    #  ----------created by nikhil karole-   1/12/2022-----------------------------------------    
    path('pdi_inspection_representative', views.pdi_inspection_representative, name="pdi_inspection_representative"),
    path('close_pdi_inspection', views.close_pdi_inspection, name="close_pdi_inspection"),
    path('pdi_inspection_representative_list', views.pdi_inspection_representative_list, name="pdi_inspection_representative_list"),
    
    #shubham tripathi
    path('tier1_inspection_representative', views.tier1_inspection_representative, name="tier1_inspection_representative"),
    path('tier1_inspection_record', views.tier1_inspection_record, name="tier1_inspection_record"),


# created by shubham tripathi 8/3/2023  suggest by yashwant sir 
    path('api_workorder_list', views.api_workorder_list, name="api_workorder_list"),
    path('api_tkcintimation_list', views.api_tkcintimation_list, name="api_tkcintimation_list"),
    path('api_tkcintimation_detail', views.api_tkcintimation_detail, name="api_tkcintimation_detail"),
    path('api_fqpmilestone_list', views.api_fqpmilestone_list, name="api_fqpmilestone_list"),
    path('api_fqpmilestone_category_list', views.api_fqpmilestone_category_list, name="api_fqpmilestone_category_list"),
    path('api_fqpmilestone_subcategory_list', views.api_fqpmilestone_subcategory_list, name="api_fqpmilestone_subcategory_list"),
    path('api_fqpmilestone_subcategory_data_list', views.api_fqpmilestone_subcategory_data_list, name="api_fqpmilestone_subcategory_data_list"),
    path('api_fqpintimation_observation_info_detail', views.api_fqpintimation_observation_info_detail, name="api_fqpintimation_observation_info_detail"),
    path('api_fqpintimation_observation_officer_detail', views.api_fqpintimation_observation_officer_detail, name="api_fqpintimation_observation_officer_detail"),
    path('api_fqpintimation_observation_create_data', views.api_fqpintimation_observation_create_data, name="api_fqpintimation_observation_create_data"),
    path('api_fqpintimation_officer_list', views.api_fqpintimation_officer_list, name="api_fqpintimation_officer_list"),
# ------------------------shubham tripathi code end here-----------------------

     #--nikhil
    path('vendor_materials/<str:item_code>',views.vendor_materials, name ="vendor_materials"),


    #------Lokendra----------#
    path('power_analyzer', views.Power_Analyzer, name="Power_Analyzer"),


    #--nikhil
    path('list_support',ListSupport.as_view()),
    
    #----------------------------------start of fqp api url by ravindra------------------------------------#
   
    
    path('api_check_fqpintimation_status_post', views.api_check_fqpintimation_status_post.as_view()), #post_api_url
    # path('api_check_fqpintimation_status_01', views.api_check_fqpintimation_status_01, name="api_check_fqpintimation_status_01"),#by ravindra
    path('api_check_fqpintimation_status_get', views.api_check_fqpintimation_status_get.as_view()), #get_api_url
    
    
    #----------------------------------end of fqp api url by ravindra------------------------------------#
    
    path('package-master-data', views.package_master_data, name="package_master_data"),
    path('contractors-data', views.all_contractors_data, name="UserCompanyDataMain"),
    path('works-master-data', views.work_order_data, name="work_order_data"),
    path('material-supply-data', views.supply_testing_data, name="supply_testing_data"),
    path('invoice-data', views.invoice_data, name="invoice_data"),



#S----------- created by shubham tripathi 8/3/2023  suggest by yashwant sir 
    path('api_otp_generate_officer', views.api_otp_generate_officer, name="api_otp_generate_officer"),
    path('api_officer_login', views.api_officer_login, name="api_officer_login"),

    path('api_new_fqpintimation_wo_list', views.api_new_fqpintimation_wo_list, name="api_new_fqpintimation_wo_list"),
    path('api_new_fqpintimation_task_list', views.api_new_fqpintimation_task_list, name="api_new_fqpintimation_task_list"),
    path('api_new_fqpintimation_list', views.api_new_fqpintimation_list, name="api_new_fqpintimation_list"),

    path('api_newfqpintimation_milestone_category_list', views.api_newfqpintimation_milestone_category_list, name="api_newfqpintimation_milestone_category_list"),
    path('api_newfqpintimation_milestone_subcategory_list', views.api_newfqpintimation_milestone_subcategory_list, name="api_newfqpintimation_milestone_subcategory_list"),
    path('api_newfqpintimation_milestone_subcategory_data_list', views.api_newfqpintimation_milestone_subcategory_data_list, name="api_newfqpintimation_milestone_subcategory_data_list"),
    path('api_newfqpintimation_observation_info_detail_saved', views.api_newfqpintimation_observation_info_detail_saved, name="api_newfqpintimation_observation_info_detail_saved"),
    path('api_new_fqpintimation_observation_close_data', views.api_new_fqpintimation_observation_close_data, name="api_new_fqpintimation_observation_close_data"),
    path('api_new_fqpintimation_observation_officer_detail', views.api_new_fqpintimation_observation_officer_detail, name="api_new_fqpintimation_observation_officer_detail"),    
    path('api_newfqpintimation_emb_measurment_status', views.api_newfqpintimation_emb_measurment_status, name="api_newfqpintimation_emb_measurment_status"),
    path('api_new_fqpintimation_officer_list', views.api_new_fqpintimation_officer_list, name="api_new_fqpintimation_officer_list"),
    


    
]

