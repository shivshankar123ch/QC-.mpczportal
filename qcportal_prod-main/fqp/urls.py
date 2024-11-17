from django.contrib import admin
from django.urls import path,include
from fqp import views

urlpatterns = [

    #Added By Aayush Joshi for API:Integration
    path('fetch_gbpa_order_view', views.fetch_gbpa_order_view, name='fetch_gbpa_order_view'),
    path('gbpa_api_call', views.gbpa_api_call, name='gbpa_api_call'),
    path('check_gbpa', views.gbpa_api_call, name='gbpa_api_call'),
    path('wo_view_gbpa/<int:id>', views.wo_view_created_by_gbpa, name='wo_view_created_by_gbpa'),
    path('view_workorder/<int:v_id>', views.view_workorder, name='view_workorder'),


###########################################################################################

    path('project_base', views.project_base, name="project_base"),
    path('approver_base', views.approver_base, name="approver_base"),
    path('search_wo',  views.search_wo, name="search_wo"),
    path('generate_wo',  views.generate_wo, name="generate_wo"),
    path('generate_wo1',  views.generate_wo1, name="generate_wo1"),
    path('generate_wo2/<int:PO_id>',  views.generate_wo2, name="generate_wo2"),
    path('generate_wo3/<int:PO_id>',  views.generate_wo3, name="generate_wo3"),
    path('view_wo/<int:PO_id>',  views.view_wo, name="view_wo"),
    path('all_wo',  views.all_wo, name="all_wo"),
    path('approve_all_wo',  views.approve_all_wo, name="approve_all_wo"),
    path('upload_agreement/<int:PO_id>',  views.upload_agreement, name="upload_agreement"),
    path('upload_agreement_save/<int:PO_id>',  views.upload_agreement_save, name="upload_agreement_save"),
    path('upload_loa/<int:PO_id>',  views.upload_loa, name="upload_loa"),
    path('upload_loa_save/<int:PO_id>',  views.upload_loa_save, name="upload_loa_save"),
    path('wo_approval/<int:PO_id>',  views.wo_approval, name="wo_approval"),
    # path('wo_delete/<int:PO_id>',  views.wo_delete, name="wo_delete"),
    # path('wo_approved/<int:PO_id>',  views.wo_approved, name="wo_approved"),
    path('wo_approved_save/<int:PO_id>',  views.wo_approved_save, name="wo_approved_save"),
    path('wo_rejected/<int:PO_id>',  views.wo_rejected, name="wo_rejected"),
    path('wo_rejected_save/<int:PO_id>',  views.wo_rejected_save, name="wo_rejected_save"),
    path('bg_review/<int:PO_id>', views.bg_review, name="bg_review"),
    path('bank_review/<int:PO_id>', views.bank_review, name="bank_review"),
    # path('bg_approval/<int:PO_id>',  views.bg_approval, name="bg_approval"),
    # path('bg_view/<int:PO_id>',  views.bg_view, name="bg_view"),
    path('bg_approval_save/<int:PO_id>',  views.bg_approval_save, name="bg_approval_save"),
    path('all_bg',  views.all_bg, name="all_bg"),
    path('all_pert',  views.all_pert, name="all_pert"),
    path('all_bg_approval',  views.all_bg_approval, name="all_bg_approval"),
    path('bg_view_approved/<int:PO_id>',  views.bg_view_approved, name="bg_view_approved"),
    # path('bg_approval/<int:PO_id>', views.bg_approval, name="bg_approval"),
    # path('bank_approval/<int:PO_id>', views.bank_approval, name="bank_approval"),
    path('all_pert_approval',  views.all_pert_approval, name="all_pert_approval"),
    # path('pert_approval/<int:PO_id>', views.pert_approval, name="pert_approval"),
    path('pert_review/<int:PO_id>', views.pert_review, name="pert_review"),
    path('vendor_ins_approval/', views.vendor_ins_approval, name="vendor_ins_approval"),
    path('vendor_ins_approved/<int:WO_id>',  views.vendor_ins_approved, name="vendor_ins_approved"),
    path('all_material_offer',  views.all_material_offer, name="all_material_offer"),
    path('material_offer/<int:PO_id>',  views.material_offer, name="material_offer"),
    path('material_offer_approval_save/<int:PO_id>', views.material_offer_approval_save, name="material_offer_approval_save"),

    
    path('officersop',views.officersop,name="officersop"),

    path('pdi_schedule',  views.pdi_schedule, name="pdi_schedule"),
    path('pdi_schedule_set/<int:PO_id>',  views.pdi_schedule_set, name="pdi_schedule_set"),

    path('upload_schedule',  views.upload_schedule, name="upload_schedule"),
    path('tkc_all_purchase', views.tkc_all_purchase, name="tkc_all_purchase"),
    path('tkc_tier1_inspection', views.tkc_tier1_inspection, name="tkc_tier1_inspection"),
    path('tkc_tier2_inspection', views.tkc_tier2_inspection, name="tkc_tier2_inspection"),
    path('vendor_ins_approval_save/<int:v_id>', views.vendor_ins_approval_save, name="vendor_ins_approval_save"),

    #  jeevan New code
    # creater
    path('logout', views.logout, name='logout'),
    path('procurement_generate_wo', views.procurement_Generate_WO, name='procurement_generate_wo'),
    path('procurement_generate_wo1/<int:id>', views.procurement_Generate_WO1, name='procurement_generate_wo1'),
    path('procurement_generate_wo2/<int:id>', views.procurement_Generate_WO2, name='procurement_Generate_wo2'),
    path('procurement_generate_wo3/<int:id>', views.procurement_Generate_WO3, name='procurement_Generate_wo3'),
    path('procurement_generate_wo4/<int:id>', views.procurement_Generate_WO4, name='procurement_Generate_wo4'),
    path('procurement_generate_wo5/<int:id>', views.procurement_Generate_WO5, name='procurement_Generate_wo5'),
    path('procurement_generate_wo6/<int:id>', views.procurement_Generate_WO6, name='procurement_Generate_wo6'),
    path('procurement_generate_wo7/<int:id>', views.procurement_Generate_WO7, name='procurement_Generate_wo7'),
    path('procurement_generate_wo8/<int:id>', views.procurement_Generate_WO8, name='procurement_Generate_wo8'),
    path('procurement_generate_wo9/<int:id>', views.procurement_Generate_WO9, name='procurement_Generate_wo9'),
    # path('procurement_generate_wo10/<int:id>', views.procurement_Generate_WO10, name='procurement_Generate_wo10'),
    # path('procurement_generate_wo11/<int:id>', views.procurement_Generate_WO11, name='procurement_Generate_wo11'),

    #Updated URL Added by Aayush For Manual and Automated Process
    path('procurement_generate_wo10/<int:id>/<str:message_rendered>', views.procurement_Generate_WO10, name='procurement_Generate_wo10'),
    path('procurement_generate_wo11/<int:id>/<str:message_rendered>', views.procurement_Generate_WO11, name='procurement_Generate_wo11'),

    path('wo_view/<int:id>', views.wo_view, name='wo_view'),
    path('send_to_approval/<int:id>', views.send_to_approval, name='send_to_approval'),
    path('delete_amount/<int:id>/<int:amount_id>', views.delete_amount, name='delete_amount'),
    path('delete_advance/<int:id>/<int:amount_id>', views.delete_advance, name='delete_advance'),
    path('delete_time/<int:id>/<int:time_id>', views.delete_time, name='delete_time'),
    path('delete_schedule_supply/<int:id>/<int:schedule_supply_id>', views.delete_schedule_supply, name='delete_schedule_supply'),
    path('delete_schedule_install/<int:id>/<int:schedule_install_id>', views.delete_schedule_install, name='delete_schedule_install'),
    path('delete_schedule_supply_item/<int:id>/<int:schedule_install_id>', views.delete_schedule_supply_item,
         name='delete_schedule_supply_item'),
    path('delete_schedule_install_item/<int:id>/<int:schedule_install_id>', views.delete_schedule_install_item,
         name='delete_schedule_install_item'),
    path('delete_major_item/<int:id>/<int:schedule_install_id>', views.delete_major_item,name='delete_major_item'),
    path('delete_variable_item/<int:id>/<int:schedule_install_id>', views.delete_variable_item,name='delete_variable_item'),
    path('delete_copy_to/<int:id>/<int:schedule_install_id>', views.delete_copy_to,name='delete_copy_to'),
    path('procurement_previous_wo', views.procurement_previous_wo, name="procurement_previous_wo"),
    path('wo_delete/<int:id>', views.wo_delete, name="wo_delete"),
    path('wo_upload_agreement_copy/<int:id>', views.wo_upload_agreement_copy, name='wo_upload_agreement_copy'),
    path('bank_approval/<int:wo_id>', views.bank_approval, name="bank_approval"),
    path('bg_approval/<int:wo_id>', views.bg_approval, name="bg_approval"),
    path('loc_approval/<int:wo_id>', views.loc_approval, name="loc_approval"),
    path('pert_approval/<int:wo_id>', views.pert_approval, name="pert_approval"),
    path('otherdoc_approval/<int:wo_id>', views.otherdoc_approval, name="otherdoc_approval"),
    path('mqpdoc_approval/<int:wo_id>', views.mqpdoc_approval, name="mqpdoc_approval"),
    path('fqpdoc_approval/<int:wo_id>', views.fqpdoc_approval, name="fqpdoc_approval"),
    path('vendor_approval/<int:wo_id>/<int:tkc_vendor_id>', views.vendor_approval, name="vendor_approval"),
    path('material_offer_approval_offer_data/<int:id>/<int:wo_id>', views.material_offer_approval_offer_data, name="material_offer_approval_offer_data"),
    path('material_offer_approval/<int:wo_id>/<str:offer_no>/<int:wo_material_boq_id>', views.material_offer_approval, name="material_offer_approval"),
    path('view_offered_material_details/<int:wo_id>/<str:offer_no>/<int:wo_material_boq_id>', views.view_offered_material_details, name="view_offered_material_details"),

    
#     path('create_di/<int:wo_id>/<int:create_Di_id>', views.create_di, name="create_di"),
#     path('Create-Dispatch-Instruction/<int:wo_id>/<int:material_id>/<int:create_Di_id>', views.CreateDispatchInstruction, name="CreateDispatchInstruction"),
    
    #TKC DI urls
    path('di_offers_list/<int:wo_id>', views.di_offers_list, name="di_offers_list"),
    path('view_offer_approved_material/<int:wo_id>/<str:offer_no>', views.view_offer_approved_material, name="view_offer_approved_material"),
    path('create_tkc_di_step1/<int:wo_id>/<str:offer_no>', views.create_tkc_di_step1, name="create_tkc_di_step1"),
    path('Tkc-Di-Terms/<int:wo_id>/<int:create_Di_id>/<str:offer_no>/<str:di_ref_no>',views.TkcDiTerms,name="TkcDiTerms"),
    path('create_di_step2/<int:wo_id>/<int:create_Di_id>/<str:offer_no>/<str:di_ref_no>', views.create_di_step2, name="create_di_step2"),
    # path('wo_di_view/<int:wo_id>', views.wo_di_view, name="wo_di_view"),
    # path('Send-Wo-Di-For-Approval/<int:wo_id>',views.SendWoDiForApproval,name="SendWoDiForApproval"),
    path('Work-Order-DI',views.WorkOrderDI,name="WorkOrderDI"),
    path('all_wo_di',views.all_wo_di,name="all_wo_di"),
    path('created_di_view/<int:wo_id>/<int:create_Di_id>/<str:offer_no>', views.created_di_view, name="created_di_view"),
    path('Send-pending-Wo-Di-For-Approval/<int:di_id>',views.SendPendingWoDiForApproval,name="SendPendingWoDiForApproval"),
    path('delete_di_data/<int:di_id>',views.delete_di_data,name="delete_di_data"),
    path('approver_delete_di_data/<int:di_id>/<int:wo_id>',views.approver_delete_di_data,name="approver_delete_di_data"),
    path('all_rejected_wo_di',views.all_rejected_wo_di,name="all_rejected_wo_di"),
    path('view_site_store_serial_no/<int:offer_id>',views.view_site_store_serial_no,name="view_site_store_serial_no"),
    
    
    path('approver_view_work_order_di/<int:di_id>/<int:wo_id>',views.approver_view_work_order_di,name="approver_view_work_order_di"),
    path('Wo-Di-Approval/<int:di_id>/<int:wo_id>',views.WoDiApproval,name="WoDiApproval"),
    path('upload_digital_work_order_di/<int:di_id>/<int:wo_id>',views.upload_digital_work_order_di,name="upload_digital_work_order_di"),
    
    #New Url Added for Verify DI info using DI API .(Added By Aayush) 
    path('verify_and_create_di/<int:wo_id>/<str:offer_no>', views.verify_and_create_di, name="verify_and_create_di"),
    path('view_and_create_multiple_DI/<int:wo_id>/<str:offer_no>', views.view_and_create_multiple_DI, name="view_and_create_multiple_DI"),
    path('create_erp_di_entry/<int:wo_id>/D/<str:di_no>/<str:offer_no>', views.create_erp_di_entry, name="create_erp_di_entry"),
    path('create_erp_di_step2/<int:wo_id>/<int:create_Di_id>/<str:offer_no>/D/<int:di_no>', views.create_erp_di_step2, name="create_erp_di_step2"),
    path('erp-tkc-Di-Terms/<int:wo_id>/<int:create_Di_id>/<str:offer_no>/D/<int:erp_di_no>',views.erp_tkc_DiTerms,name="erp_tkc_DiTerms"),
    path('erp_approver_view_work_order_di/<int:di_id>/<int:wo_id>',views.erp_approver_view_work_order_di,name="erp_approver_view_work_order_di"),
    path('ERP-Work-Order-DI',views.ERPWorkOrderDI,name="ERPWorkOrderDI"),
    path('erp_di_offers_list/<int:wo_id>', views.erp_di_offers_list, name="erp_di_offers_list"),
    path('view_erp_offered_approved_material/<int:wo_id>/<str:offer_no>', views.view_erp_offered_approved_material, name="view_erp_offered_approved_material"),
    path('view_receiving_details/<int:wo_id>/D/<int:di_no>/<str:offer_no>', views.view_receiving_details, name="view_receiving_details"),
    path('erp_work_order_dispatch_instruction_list/<int:wo_id>', views.erp_work_order_dispatch_instruction_list, name="erp_work_order_dispatch_instruction_list"),
    path('Upload-erp-Di-Copy/<str:offer_no>/D/<str:erp_di_no>/<int:wo_id>',views.upload_erp_di_copy,name="upload_erp_di_copy"),
    path('delete-non-approved-di/D/<int:di_id>',views.delete_non_approved_di,name="delete_non_approved_di"),
    # approver
    path('work_order', views.work_order, name="work_order"),
    path('approver_view_work_order/<int:id>', views.approver_view_work_order,name="approver_view_work_order"),
    path('wo_approved/<int:id>', views.wo_approved, name='wo_approved'),
    path('wo_reject/<int:id>', views.wo_reject, name='wo_reject'),
    path('wo_upload_digital_copy/<int:id>', views.wo_upload_digital_copy, name='wo_upload_digital_copy'),
    path('bank_view/<int:wo_id>', views.bank_view, name="bank_view"),
    path('bg_view/<int:wo_id>', views.bg_view, name="bg_view"),
    path('loc_view/<int:wo_id>', views.loc_view, name="loc_view"),
    path('pert_view/<int:wo_id>', views.pert_view, name="pert_view"),
    path('otherdoc_view/<int:wo_id>', views.otherdoc_view, name="otherdoc_view"),
    path('mqpdoc_view/<int:wo_id>', views.mqpdoc_view, name="mqpdoc_view"),
    path('fqpdoc_view/<int:wo_id>', views.fqpdoc_view, name="fqpdoc_view"),
    path('vendor_view/<int:wo_id>', views.vendor_view, name="vendor_view"),
    path('material_offer_approved/<int:id>/<int:wo_id>', views.material_offer_approved, name="material_offer_approved"),
    
    # Nodal officer
    path('view_item/', views.view_item, name="view_item"),
    path('item_received/<int:item_id>', views.item_received, name="item_received"),
    
    
    
    path('wo_pdi_material_view/<int:id>', views.wo_pdi_material_view, name='wo_pdi_material_view'),
    path('fqp_di_status/<int:id>', views.FqpDiStatus, name='fqp_di_status'),
    path('fqp_reject_di', views.fqp_reject_di, name="fqp_reject_di"),
    path('fqp_reject_di_material_view/<int:id>', views.fqp_reject_di_material_view, name='fqp_reject_di_material_view'),
    path('fqp_select_material_for_getpass/<int:id>', views.fqp_select_material_for_getpass, name='fqp_select_material_for_getpass'),
    path('fqp_create_po_gatepass/<int:id>', views.fqp_create_po_gatepass, name='fqp_create_po_gatepass'),
    path('fqp_gatepass', views.fqp_gatepass, name='fqp_gatepass'),
    path('fqp_gatepass_history/<int:id>', views.fqp_gatepass_history, name='fqp_gatepass_history'),
    path('fqp_di_send_to_cgm/<int:id>', views.fqp_di_send_to_cgm, name='fqp_di_send_to_cgm'),
    path('fqp_wo_sample_list', views.fqp_wo_sample_list, name='fqp_wo_sample_list'),
    path('fqp_sample_select/<int:id>', views.fqp_sample_select, name='fqp_sample_select'),
    path('fqp_select_testing_nabl/<int:id>', views.fqp_select_testing_nabl, name='fqp_select_testing_nabl'),
    path('fqp_view_samled_material/<int:id>', views.fqp_view_samled_material, name='fqp_view_samled_material'),
    path('fqp_wo_trf_create', views.fqp_wo_trf_create, name='fqp_wo_trf_create'),
    path('fqp_wo_di_sampled_item/<int:id>', views.fqp_wo_di_sampled_item, name='fqp_wo_di_sampled_item'),
    path('fqp_wo_nabl_gatepass/<int:id>', views.fqp_wo_nabl_gatepass_new, name='fqp_wo_nabl_gatepass'),
    path('fqp_wo_test_request_form_submit/<int:id>', views.fqp_test_request_form_submit, name='fqp_test_request_form_submit'),
    
    # boq urls 
    path('all_discom', views.all_discom, name='all_discom'),
    path('tag_circle', views.tag_circle, name='tag_circle'),
    path('wo_boq_list',views.wo_boq_list, name = "wo_boq_list"),
    path('update_boq/<int:wo_id>', views.update_boq, name="update_boq"),
    path('update_boq_info',views.update_boq_info, name = "update_boq_info"),
    path('circle_master/<int:discom_id>', views.circle_master, name='circle_master'),
    path('tag_circle_by_wo/<int:wo_no>/<int:region_id>',views.tag_circle_by_wo, name = "tag_circle_by_wo"),
    path('wo_region_save',views.wo_region_save,name = "wo_region_save"),
    path('save_boq/<int:wo_id>/<int:identifier>',views.save_boq,name = "save_boq"),
    path('update_boq_edit/<int:wo_id>',views.update_boq_edit,name = "update_boq_edit"),
    path('save_boq_info/<int:wo_id>/<int:identifier>',views.save_boq_info, name = "save_boq_info"),    
    
    path('proj_verify_boq_list',views.proj_verify_boq_list, name = "proj_verify_boq_list"),
    path('proj_verify_boq_info/<int:wo_id>',views.proj_verify_boq_info, name = "proj_verify_boq_info"),
    path('proj_accept_boq/<int:wo_id>',views.proj_accept_boq, name = "proj_accept_boq"),
    path('proj_reject_boq/<int:wo_id>',views.proj_reject_boq, name = "proj_reject_boq"),
    path('proj_view_boq/<int:wo_id>',views.proj_view_boq, name = "proj_view_boq"),
    
    path('fake_call', views.fake_call, name='fake_call'),
    path('pdi_against_wo/<str:offer_no>',views.pdi_against_wo,name='pdi_against_wocreator'),
    path('pdi_inspection_data_wo/<str:item_code>/<str:offer_no>', views.pdi_inspection_data_wo, name='pdi_inspection_data_wo'),
    path('all_fake_called_data/<str:offer_no>',views.all_fake_called_data,name='all_fake_called_data'),
    


# ----------- shubham tripathi ---------fqp intimatin inspection  for officer ----16-03-2023---------------------
    path('officer_fqpintimation',views.officer_fqpintimation, name = "officer_fqpintimation"),
    path('officer_fqpintimation_list',views.officer_fqpintimation_list, name = "officer_fqpintimation_list"),
    path('officer_fqpintimation_observation_detail',views.officer_fqpintimation_observation_detail, name = "officer_fqpintimation_observation_detail"),

# ------------------fqp intimation code end here -----------------------------------------
        # -------------------shubham tripathi------------------
    path('wo_officer_invoice_list/', views.wo_officer_invoice_list, name="wo_officer_invoice_list"),
    path('wo_approver_invoice/', views.wo_approver_invoice, name="wo_approver_invoice"),
    path('wo_approver_invoice_list/', views.wo_approver_invoice_list, name="wo_approver_invoice_list"),
    path('wo_creator_invoice_list/', views.wo_creator_invoice_list, name="wo_creator_invoice_list"),


    path('wo_cfo_invoice_list/', views.wo_cfo_invoice_list, name="wo_cfo_invoice_list"),
    path('wo_dgmcbpu_invoice_list/', views.wo_dgmcbpu_invoice_list, name="wo_dgmcbpu_invoice_list"),
    path('wo_aubills_invoice_list/', views.wo_aubills_invoice_list, name="wo_aubills_invoice_list"),
    path('wo_dgmem_invoice_list/', views.wo_dgmem_invoice_list, name="wo_dgmem_invoice_list"),	

            # -------------------shubham tripathi code ene here------------------

# <---------------------- Lokesh Kauraik -------------------> 24-Aug-2023
    path('tkc_show_current_invoice_list/',views.tkc_show_current_invoice_list,name="tkc_show_current_invoice_list"),
    path('tkc_gm_circle_current_invoice_list/',views.tkc_gm_circle_current_invoice_list,name="tkc_gm_circle_current_invoice_list"),
    path('tkc_dgm_circle_current_invoice_list/',views.tkc_dgm_circle_current_invoice_list,name="tkc_dgm_circle_current_invoice_list"),
    path('tkc_cgmproject_current_invoice_list/',views.tkc_cgmproject_current_invoice_list,name="tkc_cgmproject_current_invoice_list"),
    path('tkc_dgmproject_current_invoice_list/',views.tkc_dgmproject_current_invoice_list,name="tkc_dgmproject_current_invoice_list"),
    path('tkc_cfoproject_current_invoice_list/',views.tkc_cfoproject_current_invoice_list,name="tkc_cfoproject_current_invoice_list"),
    path('tkc_dgmcbpu_current_invoice_list/',views.tkc_dgmcbpu_current_invoice_list,name="tkc_dgmcbpu_current_invoice_list"),
    path('tkc_aocbpu_current_invoice_list/',views.tkc_aocbpu_current_invoice_list,name="tkc_aocbpu_current_invoice_list"),
    path('tkc_dgmem_current_invoice_list/',views.tkc_dgmem_current_invoice_list,name="tkc_dgmem_current_invoice_list"),
    
            
            
            
    # Code for PS dashboard
    path('Ps-Dashboard',views.ps_dashboard,name="ps_dashboard"),
    path('All-Discom-Work-Orders',views.all_discom_work_orders,name="all_discon_work_orders"),
    path('Wo-Discom-Data/<str:discom>',views.wo_discom_data,name="wo_discom_data"),
    path('Work-Order-Offer-Data/<int:wo_id>',views.work_order_offer_data,name="work_order_offer_data"),
    path('Offer-Data-Details/<str:offer_no>/<int:wo_id>',views.offer_data_details,name="offer_data_details"), 
    path('All-Discom-DIs',views.all_discom_dispatch_instruction,name="all_discom_dispatch_instruction"),
    path('Dispatch-Instruction-Discom-Data/<str:discom>',views.di_discom_data,name="di_discom_data"),
    path('All-Discom-Material-Offers',views.all_discom_material_offer,name="all_discom_material_offer"),
    path('Material-Offers--Discom-Data/<str:discom>',views.material_offer_discom_data,name="material_offer_discom_data"),
    path('PS-Logout',views.ps_logout,name="ps_logout"),
    path('Package-Wo-Data/<int:package_id>',views.package_wo_Data,name="package_wo_Data"),
    path('Package-Discom-Wo-Data/<int:package_id>/<str:discom>',views.package_discom_wo_Data,name="package_discom_wo_Data"),
    path('Work-Order-Offer-Details/<str:wo_no>/<int:package_id>',views.work_order_offer_details,name="work_order_offer_details"),
    path('Work-Order-pdi-Details/<str:wo_no>/<int:package_id>',views.work_order_pdi_details,name="work_order_pdi_details"),
    path('Work-Order-Offer-Materials-Details/<str:offer_no>/<int:package_id>',views.work_order_offer_material_details,name="work_order_offer_material_details"),
    path('Work-Order-di-Details/<str:offer_no>/<int:package_id>',views.work_order_dispatch_instruction,name="work_order_dispatch_instruction"),
    # url FOR PDI details to PS Sir
    path('all_discom_pdi',views.all_discom_pdi,name="all_discom_pdi"),
    path('all_assigned_pdi_ps/<str:zone>',views.all_assigned_pdi_ps,name="all_assigned_pdi_ps"),
    path('pdi_against_wo_ps/<str:offer_no>',views.pdi_against_wo_ps,name="pdi_against_wo_ps"),
    path('all_approved_pdi_ps/<str:zone>',views.all_approved_pdi_ps,name="all_approved_pdi_ps"),
    path('all_pending_ins_pdi_ps/<str:zone>',views.all_pending_ins_pdi_ps,name="all_pending_ins_pdi_ps"),
    path('all_pending_pdi_appr_ps/<str:zone>',views.all_pending_pdi_appr_ps,name="all_pending_pdi_appr_ps"),
    path('all_rejected_pdi_ps/<str:zone>',views.all_rejected_pdi_ps,name="all_rejected_pdi_ps"),
    path('pdi_pending_assign_ps/<str:zone>',views.pdi_pending_assign_ps,name="pdi_pending_assign_ps"),
    path('view_offer_ps/<str:offer_no>',views.view_offer_ps,name="view_offer_ps"),
    
    
    # fqp new added url
    path('created_di_list/<int:wo_id>', views.created_di_list, name="created_di_list"),
    path('Upload-Di-Copy/<str:offer_no>/<str:erp_di_no>/<int:wo_id>',views.upload_di_copy,name="Upload-Di-Copy"),
    path('work_order_dispatch_instruction_list/<int:wo_id>', views.work_order_dispatch_instruction_list, name="work_order_dispatch_instruction_list"),
    
    
    
    # url added pd mishra
    
    # path('view_offer_wo/<str:offer_no>',views.view_offer_wo,name='view_offer_wo'),
    # path('bypass_pdi_offer', views.bypass_pdi_offer, name='bypass_pdi_offer'),
    
    
    path('contractor_details_ps', views.new_dashboard_ps, name='contractor_details_ps'),
    path('contractor_history_ps/<str:name>', views.new_dashboard_history_ps, name='ncontractor_history_ps'),
    path('active_inactive_contractor_list_ps', views.active_inactive_contractor_list_ps, name='active_inactive_contractor_list_ps'),
    path('contractor_details_view_ps/<int:id>', views.contractor_view_details_ps, name='contractor_details_view_ps'),
    path('day_wise_count_vendor_ps', views.day_wise_count_tkc_ps, name="day_wise_count_vendor_ps"),
    path('day_wise_count_vendor_view_ps/<str:name>',views.new_dashboard_history, name="day_wise_count_vendor_view_ps"),
    path('gtp_drawing_dashboard_ps', views.gtp_drawing_auditor_dashboard_ps, name="gtp_drawing_dashboard_ps"),
    path('view_gtp_wo_wise_ps/<int:id>',views.view_gtp_wo_wise_ps, name="view_gtp_wo_wise_ps"),
    
#---------------------- shubham tripathi new fqpintimation code ----------

     # -----------------new -fqp intimation code end here -- added by shubham tripathi---------------------------------------
    path('officer_new_fqpintimation_wo',views.officer_new_fqpintimation_wo, name = "officer_new_fqpintimation_wo"),
    path('officer_new_fqpintimation_list',views.officer_new_fqpintimation_list, name = "officer_new_fqpintimation_list"),
    path('officer_new_fqpintimation_observation_detail',views.officer_new_fqpintimation_observation_detail, name = "officer_new_fqpintimation_observation_detail"),

    path('officer_new_fqpintimation_task_create/',views.officer_new_fqpintimation_task_create, name = "officer_new_fqpintimation_task_create"),
    path('officer_new_fqpintimation_addmilestone/',views.officer_new_fqpintimation_addmilestone, name = "officer_new_fqpintimation_addmilestone"),
    path('officer_new_fqpintimation_tasklist/',views.officer_new_fqpintimation_tasklist, name = "officer_new_fqpintimation_tasklist"),
    path('officer_new_fqpintimation_list/',views.officer_new_fqpintimation_list, name = "officer_new_fqpintimation_list"),

    path('officer_new_fqpintimation_resurvey_observation/',views.officer_new_fqpintimation_resurvey_observation, name = "officer_new_fqpintimation_resurvey_observation"),
    
    #to do list
    path('to_do_list', views.to_do_list, name = "to_do_list"),
    path('bg_approval_list', views.bg_approval_list, name ="bg_approval_list"),
    path('bg_approval_data/<int:wo_id>', views.bg_approval_data, name ="bg_approval_data"),
    path('submit_bg_approval/<int:wo_id>', views.submit_bg_approval, name ="submit_bg_approval"),
    
    path('pending_gtp_approval', views.pending_gtp_approval, name ="pending_gtp_approval"),
    path('pending_gtp/<int:wo_id>', views.pending_gtp, name ="pending_gtp"),
    path('submit_vendor_approval/<int:wo_id>/<int:tkc_vendor_id>', views.submit_vendor_approval, name="submit_vendor_approval"),
    
    path('material_offer_approval_list', views.material_offer_approval_list, name = "material_offer_approval_list"),
    path('pending_material_offer_approval/<int:wo_id>', views.pending_material_offer_approval, name = "pending_material_offer_approval"),
    
    path('pending_di_list', views.pending_di_list, name = "pending_di_list"),
    path('pending_di/<int:wo_id>', views.pending_di, name = "pending_di"),
    
    # path('fqp_intimation', views.fqp_intimation, name = "fqp_intimation"),
    
    path('approver_todo_list', views.approver_todo_list, name = "approver_todo_list"),    
    path('pending_wo_approval', views.pending_wo_approval, name = "pending_wo_approval"),
    path('pending_di_list_data', views.pending_di_list_data, name = "pending_di_list_data"),
    path('pending_di_approval/<int:wo_id>', views.pending_di_approval, name = "pending_di_approval"),
    path('wo_di_approval/<int:di_id>/<int:wo_id>', views.wo_di_approval, name = "wo_di_approval"),    
    path('officer_invoice_list', views.officer_invoice_list, name = "officer_invoice_list"),

    # path('sampling_pro',views.sampling_pro, name = "sampling_pro"),
    # path('view_offer_sampling/<str:offer_no>',views.view_offer_sampling, name = "view_offer_sampling"),
    # path('sampling_pro/<str:offer_no>/<str:item_code>/<str:quantity>',views.sampling_pro, name = "sampling_pro"),

    path('fqp_intimation_data',views.fqp_intimation_data, name = "fqp_intimation_data"),    
    path('officer_fqpintimation_data',views.officer_fqpintimation_data, name = "officer_fqpintimation_data"),
    path('fqp_fqpintimation_list',views.fqp_fqpintimation_list, name = "fqp_fqpintimation_list"),
    path('new_fqpintimation_data',views.new_fqpintimation_data, name = "new_fqpintimation_data"),
    path('officer_fqp_intimation',views.officer_fqp_intimation, name = "officer_fqp_intimation"),



    path('officer_sampling_wo',views.officer_sampling_wo, name = "officer_sampling_wo"),
    path('officer_sampling_offerlist',views.officer_sampling_offerlist, name = "officer_sampling_offerlist"),
    path('view_offer_sampling',views.view_offer_sampling, name = "view_offer_sampling"),
    path('officer_sampling_details/<str:offer_no>/<str:item_code>',views.officer_sampling_details, name = "officer_sampling_details"),
    path('officer_sampling_details_di/<str:offer_no>',views.officer_sampling_details_di, name = "officer_sampling_details_di"),
    path('officer_di_sampling/<str:offer_no>/<int:tkc_di_id>',views.officer_di_sampling, name = "officer_di_sampling"),
    

    path('officer_gatepass_trf_wo',views.officer_gatepass_trf_wo, name = "officer_gatepass_trf_wo"),
    path('officer_gatepass_trf_offerlist/<int:woid>',views.officer_gatepass_trf_offerlist, name = "officer_gatepass_trf_offerlist"),
    path('officer_create_wo_offer_trf/<int:tkc_di_id>/<int:site_store_gatepass_id>/<str:offer_no>', views.officer_create_wo_offer_trf, name='officer_create_wo_offer_trf'),
    path('officer_view_gatepasslist/<int:tkc_di_id>/<int:wo_id>/<str:offer_no>', views.officer_view_gatepasslist, name='officer_view_gatepasslist'),
    
    # path('officer_wo_view_gatepass/<int:tkc_di_id>/<str:offer_no>', views.officer_wo_view_gatepass, name='officer_wo_view_gatepass'),
    
    ]
