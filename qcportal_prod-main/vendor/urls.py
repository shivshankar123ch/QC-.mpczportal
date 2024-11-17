from django.contrib import admin
from django.urls import path
from vendor import views

urlpatterns = [
    path('vendor_view_profile',views.vendor_view_profile, name='vendor_view_profile'),
    path('base', views.base, name='base'),
    path('updatedata', views.updatedata, name='updatedata'),
    path('basic', views.basic, name='basic'),
    path('message', views.message, name='message'),
    path('vendor_reg_seven', views.vendor_reg_seven, name='vendor_reg_seven'),
    path('vendor_reg_eight', views.vendor_reg_eight, name='vendor_reg_eight'),
    path('vendor_reg_nine', views.vendor_reg_nine, name='vendor_reg_nine'),
    path('vendor_reg_ten', views.vendor_reg_ten, name='vendor_reg_ten'),
    path('vendor_reg_eleven', views.vendor_reg_eleven, name='vendor_reg_eleven'),
    path('vendor_reg_twelve', views.vendor_reg_twelve, name='vendor_reg_twelve'),
    path('vendor_reg_thirteen', views.vendor_reg_thirteen, name='vendor_reg_thirteen'),
    path('vendor_reg_fourteen', views.vendor_reg_fourteen, name='vendor_reg_fourteen'),
    path('vendor_reg_fifteen', views.vendor_reg_fifteen, name='vendor_reg_fifteen'),
    path('vendor_reg_sixteen', views.vendor_reg_sixteen, name='vendor_reg_sixteen'),
    path('liaison', views.LeasingPerson, name='liaison'),
    path('vendor_otp_verify', views.vendor_otp_verify, name='vendor_otp_verify'),    
    path('snipped', views.snipped, name='snipped'),
    # **********************Vendor Purchase********************
    path('vendor_purchase', views.vendor_purchase, name="vendor_purchase"),
    path('vendor_purchase_b/', views.vendor_purchase_B, name="vendor_purchase_B"),
    path('vendor_dispatch_open/', views.vendor_dispatch_Open, name="vendor_dispatch_Open"),
    path('vendor_dispatch_b/<int:po_id>', views.vendor_dispatch_B2, name="vendor_dispatch_B"),
    path('vendor_dispatch_b_gtp/<int:po_id>', views.vendor_dispatch_GTP, name="vendor_dispatch_gtp"),
    path('vendor_dispatch_b_gtp_save/<int:po_id>', views.vendor_dispatch_GTP_Save, name="vendor_dispatch_GTP_Save"),
    path('vendor_dispatch_b_sd/<int:po_id>', views.vendor_dispatch_SD, name="vendor_dispatch_sd"),
    path('vendor_dispatch_b_sd_save/<int:po_id>', views.vendor_dispatch_SD_Save, name="vendor_dispatch_sd_Save"),
    path('vendor_dispatch_b2/<int:po_id>', views.vendor_dispatch_B2, name="vendor_dispatch_B2"),
    path('vendor_dispatch_b2/<int:po_id>/<int:quantity>', views.vendor_dispatch_B3, name="vendor_dispatch_B2"),
    path('vendor_view_di/<int:po_id>', views.vendor_view_di, name="vendor_view_di"),
    path('procurement_Dispatch/<int:po_id>', views.procurement_Dispatch, name="procurement_Dispatch"),
    path('vendor_gtp_approval/', views.vendor_gtp_approval, name="vendor_gtp_approval"),
    path('vendor_gtp_approved/<int:po_id>', views.vendor_gtp_approved, name="vendor_gtp_approved"),
    path('vendor_bg_approval/', views.vendor_bg_approval, name="vendor_bg_approval"),
    path('vendor_bg_approved/<int:po_id>', views.vendor_bg_approved, name="vendor_bg_approved"),
    path('vendor_ins_approval/', views.vendor_ins_approval, name="vendor_ins_approval"),
    path('vendor_ins_approved/<int:po_id>', views.vendor_ins_approved, name="vendor_ins_approved"),
    path('vendor_procurement_status/<int:po_id>', views.vendor_procurement_status, name="vendor_procurement_status"),


    # **********************working officer********************
    path('vendor_wnp_base', views.vendor_wnp_base, name='vendor_wnp_base'),
    path('Working_data', views.Working_data, name='Working_data'),
    path('vendor_wnp_evaluate', views.vendor_wnp_evaluate, name="vendor_wnp_evaluate"),
    path('vendor_wnp_approval/<int:V_id>', views.vendor_wnp_approval, name="vendor_wnp_approval"),
    path('main', views.test, name='main'),

    path('changepwd', views.changepwd, name='changepwd'),

    path('two', views.two, name='two'),

    path('new', views.employees_list, name='employees-list'),
    path('create/', views.create_employee, name='create-employee'),
    path('edit/<str:pk>/', views.edit_employee, name='edit-employee'),
    path('delete/<str:pk>/', views.delete_employee, name='delete-employee'),
    # path('procurement_Dispatch/<int:po_id>', views.procurement_Dispatch, name='procurement_Dispatch'),
    # path('procurement_preview/<int:po_id>', views.procurement_preview, name='procurement_preview'),
    #**************** work Rejected**************
    path('rejected_doc', views.rejected_doc, name='rejected_doc'),
    path('rejected_doc_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),
    path('vendor_factory_pay/<int:id>', views.vendor_factory_pay, name='vendor_factory_pay'),
    path('vendor_factory_payment/<int:id>', views.vendor_factory_payment, name='vendor_factory_payment'),

    # path('payu_demo_one',views.payu_demo_one,name="payu_demo_one"),
    # path('success_fi',views.payu_success,name='payu_success'),
    # path('payu/failure',views.payu_failure,name='payu_failure'),

    # path('success_reg_new', views.success_reg_new, name='success_reg_new'),
    # path('gen_invoice_fi', views.gen_invoice_fi, name='gen_invoice_fi'),
    path('add_material', views.add_material, name='add_material'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('transaction_history', views.transaction_history, name='transaction_history'),
    


    path('payu_demo_factoryinspection',views.payu_demo_factoryinspection,name="payu_demo_factoryinspection"),
    path('vendorfact/payu/success',views.payu_success_factoryinspection,name='payu_success_factoryinspection'),
    path('payu/failure',views.payu_failure,name='payu_failure'),
    path('gen_invoice_factoryinspection', views.gen_invoice_factoryinspection, name='gen_invoice_factoryinspection'),

    # path('success_reg_new', views.success_reg_new, name='success_reg_new'),
    # path('gen_invoice_fi', views.gen_invoice_fi, name='gen_invoice_fi'),
    # path('add_material', views.add_material, name='add_material'),
    # path('update_profile', views.update_profile, name='update_profile'),

    

    path('payu_demo_vendormaterial',views.payu_demo_vendormaterial,name="payu_demo_vendormaterial"),
    path('addmaterial/payu/success',views.payu_success_vendormaterial,name='payu_success_vendormaterial'),
    path('payu/failure',views.payu_failure,name='payu_failure'),
    path('gen_invoice_vendormaterial', views.gen_invoice_vendormaterial, name='gen_invoice_vendormaterial'),
    
    
    path('payu_demo_vendorprofile',views.payu_demo_vendorprofile,name="payu_demo_vendorprofile"),
    path('updateprofile/payu/success',views.payu_success_vendorprofile,name='payu_success_vendorprofile'),
    path('payu/failure',views.payu_failure,name='payu_failure'),
    path('gen_invoice_vendorprofile', views.gen_invoice_vendorprofile, name='gen_invoice_vendorprofile'),
      
#--------------loke21-03

    path('RCA_vendor_order/',views.RCA_vendor_order,name='RCA_vendor_order'),
    path('rca_order_view/<int:id>',views.rca_order_view,name="rca_order_view"),
    path('RCA_vendor_order_submit/<int:id>',views.RCA_vendor_order_submit,name='RCA_vendorRCA_vendor_order_submit_order'),
    path('RCA_vendor_release_order/',views.RCA_vendor_release_order,name='RCA_vendor_release_order'),
    path('RCA_release_order_submit/<int:id>',views.RCA_release_order_submit,name='RCA_release_order_submit'),
    path('rca_release_order_view/<int:id>',views.rca_release_order_view,name="rca_release_order_view"),
    path('oil_request', views.oil_request, name='oil_request'),
    path('oil_request1/<int:id>', views.oil_request1, name='oil_request1'),
    path('RCA_vendor_dtr_list/<int:id>',views.RCA_vendor_dtr_list,name='RCA_vendor_dtr_list'),
    path('rca_di_view/<int:id>',views.rca_di_view,name="rca_di_view"),
    path('rca_oil_confirmed/',views.rca_oil_confirmed,name="rca_oil_confirmed"),
    path('repaired_dtr_by_vendor/',views.repaired_dtr_by_vendor,name="repaired_dtr_by_vendor"),
    path('repaired_dtr_by_vendor_view/<int:id>',views.repaired_dtr_by_vendor_view,name="repaired_dtr_by_vendor_view"),
    path('rca_all_dispatch_instruction',views.rca_all_dispatch_instruction,name="rca_all_dispatch_instruction"),
    # path('rca_repaired_capacity_view/<int:id>',views.rca_repaired_capacity_view,name='rca_repaired_capacity_view')
    path('rca_di_issue',views.rca_di_issue,name="rca_di_issue"),
    path('rca_ven_di_issue_view/<int:id>',views.rca_ven_di_issue_view,name="rca_ven_di_issue_view"),
    path('vendor_matria_view', views.vendor_matria_view, name='vendor_matria_view'),
    path('transaction_history_copy/<int:id>',views.transaction_history_copy,name="transaction_history_copy"),
    path('Material_Delete/<int:id>',views.Material_Delete,name="Material_Delete"),
    path('rca_bg_order_list/',views.rca_bg_order_list,name="rca_bg_order_list"),
    path('rca_ven_bg_save/<int:id>',views.rca_ven_bg_save,name="rca_ven_bg_save"),
    path('rca_vendor_bg_accept_list/',views.rca_vendor_bg_accept_list,name="rca_vendor_bg_accept_list"),
    path('rca_ven_bg_acceptance_details/<int:id>',views.rca_ven_bg_acceptance_details,name="rca_ven_bg_acceptance_details"),
    path('RCA_vendor_release_list/<int:id>',views.RCA_vendor_release_list,name="RCA_vendor_release_list"),
    path('RCA_vendor_dtr_order_list/',views.RCA_vendor_dtr_order_list,name="RCA_vendor_dtr_order_list"),
    path('repaired_dtr_by_vendor_release_list/<int:id>',views.repaired_dtr_by_vendor_release_list,name="repaired_dtr_by_vendor_release_list"),
    path('view_po_details/<int:id>', views.view_po_details, name="view_po_details"),
    path('vendor_dispatch_b_bd/<int:po_id>', views.vendor_dispatch_BD, name="vendor_dispatch_bd"),
    path('vendor_dispatch_b_bd_save/<int:po_id>', views.vendor_dispatch_BD_Save, name="vendor_dispatch_bd_Save"),
    
    #########
    path('rca_ven_pass_order_list/',views.rca_ven_pass_order_list,name="rca_ven_pass_order_list"),
    path('rca_ven_pass_release_list/<int:id>',views.rca_ven_pass_release_list,name="rca_ven_pass_release_list"),
    path('rca_ven_pass_dtr_list/<int:id>',views.rca_ven_pass_dtr_list,name="rca_ven_pass_dtr_list"),

    # Meeting Code
    path('vendor_matria_view', views.vendor_matria_view, name='vendor_matria_view'),
    path('PO_Material_View', views.PO_Material_View, name="PO_Material_View"),
    path('view_po_material/<int:id>', views.view_po_material, name="view_po_material"),
    path('single_material_offer/<int:id>', views.single_material_offer, name="single_material_offer"),
    path('vendor_offer_xmr_save/<int:po_id>', views.vendor_offer_xmr_save, name="vendor_offer_xmr_save"),
    path('dispatch_item', views.Dispatch_item, name='dispatch_item'),
    path('view_di_material/<int:id>/<str:erp_di_no>', views.view_di_material, name='view_di_material'),
    path('enter/serial/<int:id>',views.Enter_serial,name="Enter_serial"),
    path('vendor_dispatch_di_new/<int:id>',views.vendor_dispatch_di_new,name="vendor_dispatch_di_new"),
    path('vendor_offer_di_save/<int:id>',views.vendor_offer_di_save,name="vendor_offer_di_save"),
    
    #------------------------------------------po resubmit item at areastore------------------------------------
    path('reject_di_item', views.view_di_material_reject, name='view_di_material_reject'),
    path('view_di_material_resubmit/<int:id>',views.view_di_material_resubmit,name="view_di_material_resubmit"),
    path('view_di_material_resubmit_save/<int:id>/<str:erp_di_no>',views.view_di_material_resubmit_save,name="view_di_material_resubmit_save"),
    #----------------------------------------------end--------------------------------------------------------------------

    #-----------------------------------------PO-view offered material-----------------------------------------
    path('po_view_offered',views.po_view_offered, name="po_view_offered"),
    path('po_view_offered_material/<int:id>',views.po_view_offered_material, name="po_view_offered_material"),
    path('view_offered_details/<int:id>',views.view_offered_details, name="view_offered_details"),
    #---------------------------------------------end----------------------------------------------------------

    #------------------------------------------PO NABL Rejected Items-------------------------------------------
    path('nabl_di_material_reject', views.nabl_di_material_reject, name="nabl_di_material_reject"),
    path('nabl_di_material_reject_view/<int:id>', views.nabl_di_material_reject_view, name="nabl_di_material_reject_view"),
    path('nabl_reject_di_areastore/<int:id>',views.nabl_reject_di_areastore,name="nabl_reject_di_areastore"),
    path('lot_rejected_gatepass_info/<int:id>',views.lot_rejected_gatepass_info, name = "lot_rejected_gatepass_info"),
    #--------------------------------------end------------------------------------------------------------



    path('profile_status',views.profile_status,name="profile_status"),

    path('factory_payment_form',views.factory_payment_form,name="factory_payment_form"),
    path('vednor_new_material', views.vednor_new_material, name="vednor_new_material"),
    path('new_material_data', views.new_material_data, name="new_material_data"),
    path('material-submit',views.material_submit,name="material_submit"),
    path('download_demo_excel', views.download_demo_excel, name="download_demo_excel"),
    path('rejected_new_material', views.rejected_new_material, name="rejected_new_material"),

    path('rejected_new_material_save/<int:id>',views.rejected_new_material_save,name="rejected_new_material_save"),


     # ------------shubham tripathi code start from here
    path('vendor_po_invoice_list/', views.vendor_po_invoice_list, name="vendor_po_invoice_list"),
    path('vendor_invoice_list/', views.vendor_invoice_list, name="vendor_invoice_list"),
    path('vendor_invoice_generate/', views.vendor_invoice_generate, name="vendor_invoice_generate"),
    path('delete_reject_material_delete/<int:id>',views.delete_reject_material_delete,name="delete_reject_material_delete"),
    
    
    
     
    #................ additional bg rca lok.....................
    
    path('add_bg/',views.add_bg,name="add_bg"),
    path('add_bg_save/<int:id>',views.add_bg_save,name='add_bg_save'),
    path('add_bg_accept_list',views.add_bg_accept_list,name='add_bg_accept_list'),
    path('add_bg_acceptance_details/<int:id>',views.add_bg_acceptance_details,name='add_bg_acceptance_details'),
    path('add_bg_resubmit_save/<int:id>',views.add_bg_resubmit_save,name="add_bg_resubmit_save"),
    
    
]
