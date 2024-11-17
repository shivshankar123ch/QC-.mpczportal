from django.contrib import admin
from django.urls import path
from po import views

urlpatterns = [

    path('vendor_purchase', views.vendor_purchase, name="vendor_purchase"),
    path('vendor_purchase_b/', views.vendor_purchase_B, name="vendor_purchase_B"),
    path('vendor_dispatch_open/', views.vendor_dispatch_Open, name="vendor_dispatch_Open"),
    path('vendor_dispatch_b/<int:po_id>', views.vendor_dispatch_B, name="vendor_dispatch_B"),
    path('vendor_dispatch_b_gtp/<int:po_id>', views.vendor_dispatch_GTP, name="vendor_dispatch_gtp"),
    path('vendor_dispatch_b_sd/<int:po_id>', views.vendor_dispatch_SD, name="vendor_dispatch_sd"),
    path('vendor_dispatch_b2/<int:po_id>', views.vendor_dispatch_B2, name="vendor_dispatch_B2"),
    path('vendor_dispatch_b2/<int:po_id>/<int:quantity>', views.vendor_dispatch_B3, name="vendor_dispatch_B2"),

    path('vendor_gtp_approval/', views.vendor_gtp_approval, name="vendor_gtp_approval"),
    path('vendor_gtp_approved/<int:po_id>', views.vendor_gtp_approved, name="vendor_gtp_approved"),
    path('vendor_bg_approval/', views.vendor_bg_approval, name="vendor_bg_approval"),
    path('vendor_bg_approved/<int:po_id>', views.vendor_bg_approved, name="vendor_bg_approved"),
    path('vendor_bg_rejected/<int:po_id>', views.vendor_bg_rejected, name="vendor_bg_rejected"),
    path('vendor_ins_approved/<int:po_id>/<int:po_material_id>', views.vendor_ins_approved, name="vendor_ins_approved"),
    path('vendor_ins_reject/<int:po_id>/<int:po_material_id>', views.vendor_ins_reject, name="vendor_ins_reject"),
    path('vendor_procurement_status/<int:po_id>', views.vendor_procurement_status, name="vendor_procurement_status"),

    path('nabl_Registration_sixteen', views.nabl_Registration_Sixteen, name='nabl_Registration_sixteen'),
    path('nabl_Registration_sixteen1', views.nabl_Registration_Sixteen1, name='nabl_Registration_Sixteen1'),
    path('dispatch_for_nabl/<int:po_id>', views.dispatch_for_nabl, name='dispatch_for_nabl'),
    path('nabl_upload/<int:po_id>', views.nabl_Upload, name='nabl_upload'),
    path('nabl_report/<int:po_id>', views.nabl_Report, name='nabl_Report'),

    path('procurement_dashboard', views.procurement_Dashboard, name='procurement_dashboard'),
    path('procurement_di_list', views.procurement_Di_List, name='procurement_di_list'),
    path('procurement_Di_Issue/<int:po_id>', views.procurement_Di_Issue, name='procurement_Di_Issue'),
    path('procurement_Di_Issued/<int:po_id>', views.procurement_Di_Issued, name='procurement_Di_Issued'),
    path('procurement_Dispatch/<int:po_id>', views.procurement_Dispatch, name='procurement_Dispatch'),

    path('area_base', views.area_base, name="area_base"),
    path('area_dashboard', views.area_dashboard, name="area_dashboard"),
    path('area_process', views.area_process, name="area_process"),
    path('area_stock', views.area_stock, name="area_stock"),
    path('offer_receive/<int:po_id>', views.offer_receive, name="offer_receive"),
    path('vendor_view_di/<int:po_id>', views.vendor_view_di, name="vendor_view_di"),
    path('area_store_view/<int:po_id>', views.area_store_view, name="area_store_view"),

    path('nabl_Registration_sixteen1', views.nabl_Registration_Sixteen1, name='nabl_Registration_Sixteen1'),

    path('tkc_purchase', views.tkc_purchase, name="tkc_purchase"),
    path('tkc_po_view/<int:id>', views.tkc_po_view, name="tkc_po_view"),
    path('tkc_purchase1', views.tkc_purchase1, name="tkc_purchase1"),
    path('tkc_purchase2/<int:PO_id>', views.tkc_purchase2, name="tkc_purchase2"),
    path('tkc_all_purchase', views.tkc_all_purchase, name="tkc_all_purchase"),
    path('tkc_tier1_inspection', views.tkc_tier1_inspection, name="tkc_tier1_inspection"),
    path('tkc_tier2_inspection', views.tkc_tier2_inspection, name="tkc_tier2_inspection"),



    path('tkc_reg_fourteen', views.tkc_reg14, name="tkc_reg14"),
    path('tkc_reg_fifteen', views.tkc_reg15, name="tkc_reg15"),
    path('tkc_reg_sixteen', views.tkc_reg16, name="tkc_reg16"),
    path('tkc_reg_seventeen', views.tkc_reg17, name="tkc_reg17"),
    path('tkc_view/<int:id>', views.tkc_view, name="tkc_view"),
    path('offer_inspection/<int:id>', views.offer_inspection, name="offer_inspection"),
    path('view_schedule/<int:id>', views.view_schedule, name="view_schedule"),
    path('tkc_view_schedule/<int:id>', views.tkc_view_schedule, name="tkc_view_schedule"),

    path('procurement_generate_po', views.procurement_Generate_PO, name='procurement_generate_po'),
    #path('procurement_generate_po2/<int:po_id>', views.procurement_Generate_PO2, name='procurement_generate_po2'),

    # path('procurement_add_test', views.procurement_Add_Test, name='procurement_add_test'),
    # path('procurement_test_list', views.procurement_Test_List, name='procurement_test_list'),
    # path('procurement_add_di', views.procurement_Add_Di, name='procurement_add_di'),
    path('procurement_status/<int:po_id>', views.procurement_status, name="procurement_status"),
    path('procurement_delete/<int:po_id>', views.procurement_delete, name="procurement_delete"),
    path('User_section_dashboard', views.User_section_dashboard, name="User_section_dashboard"),

    path('po_base', views.po_base, name='po_base'),
    path('procurement_dashboard', views.procurement_dashboard, name='procurement_dashboard'),
    # path('vendor_gtp_approval/', views.vendor_gtp_approval, name="vendor_gtp_approval"),
    path('vendor_bg_approval/', views.vendor_bg_approval, name="vendor_bg_approval"),
    path('vendor_bg_view/<int:po_id>', views.vendor_bg_view, name="vendor_bg_view"),
    path('vendor_ins_approval/', views.vendor_ins_approval, name="vendor_ins_approval"),
    path('tkc_purchase', views.tkc_purchase, name="tkc_purchase"),
    path('tkc_all_purchase', views.tkc_all_purchase, name="tkc_all_purchase"),
    path('tkc_tier1_inspection', views.tkc_tier1_inspection, name="tkc_tier1_inspection"),
    path('tkc_tier2_inspection', views.tkc_tier2_inspection, name="tkc_tier2_inspection"),
    path('po_gen', views.po_gen, name="po_gen"),



    # ********************* New Code Jeevan *******************

    path('procurement_previous_po', views.procurement_Previous_PO, name='procurement_previous_po'),

    # ********************* Cgm procurement url *******************
    path('cgm_approved_po', views.cgm_approved_po, name='cgm_approved_po'),
    path('cgm_pending_po', views.cgm_pending_po, name='cgm_pending_po'),
    path('cgm_rejected_po', views.cgm_rejected_po, name='cgm_rejected_po'),
    path('cgm_total_po', views.cgm_total_po, name='cgm_total_po'),
    path('cgm_procurement_approved/<int:id>', views.cgm_procurement_approved, name='cgm_procurement_approved'),
    path('cgm_procurement_rejected/<int:id>', views.cgm_procurement_rejected, name='cgm_procurement_rejected'),
    path('po_gen', views.po_gen, name="po_gen"),

    path('po_gen1', views.po_gen1, name="po_gen1"),

    path('po_gen2', views.po_gen2, name="po_gen2"),
    path('vendor_offer_view/<int:po_id>/<int:po_material_id>', views.vendor_offer_view, name="vendor_offer_view"),



    ###Anupam..

    path('test_request_form/<int:user_id>/<int:ro_id>/<int:id>/<str:discom_name_radio>/<str:nabl_name_sub_radio>', views.test_request_form, name="test_request_form"),
    path('test_request_form_submit/<int:user_id>/<int:ro_id>/<int:id>/<str:discom_name_radio>/<str:nabl_name_sub_radio>', views.test_request_form_submit, name="test_request_form_submit"),
    # path('test_request_view/<int:user_id>/<int:ro_id>/<int:id>/<str:discom_name_radio>/<str:nabl_name_sub_radio>', views.test_request_view, name="test_request_view"),
#-----------------lokendra
    path('all_rca_wo', views.all_rca_wo, name="all_rca_wo"),
    path('rca_order_view/<int:id>', views.rca_order_view, name="rca_order_view"),
    path('all_rca_ro', views.all_rca_ro, name="all_rca_ro"),
    path('rca_ro_view/<int:id>', views.rca_ro_view, name="rca_ro_view"),
    path('create_rca_di', views.create_rca_di, name="create_rca_di"),
    path('as_issue_mat_gp_add/<int:id>', views.as_issue_mat_gp_add, name="as_issue_mat_gp_add"),
    path('as_issue_mat_gp/<int:id>', views.as_issue_mat_gp, name="as_issue_mat_gp"),
    path('create_rca_di_add_material/<int:id>', views.create_rca_di_add_material, name="create_rca_di_add_material"),
    path('all_rca_di', views.all_rca_di, name="all_rca_di"),
    path('rca_di_view/<int:id>', views.rca_di_view, name="rca_di_view"),
    path('all_oil_request', views.all_oil_request, name="all_oil_request"),
    path('oil_request_forward/<int:id>', views.oil_request_forward, name="oil_request_forward"),
    # path('rca_as_vn_info', views.rca_as_vn_info, name="rca_as_vn_info"),
    # path('rca_search_xmr1/<int:id>',views.rca_search_xmr, name="rca_search_xmr"),
    # path('rca_di_issue',views.rca_di_issue,name="rca_di_issue"),


    
    path('rca_as_repaired_inward_list',views.rca_as_repaired_inward_list,name="rca_as_repaired_inward_list"),
    path('rca_as_repaired_inward/<int:id>',views.rca_as_repaired_inward,name="rca_as_repaired_inward"),
    path('rca_as_repaired_inward_accepted/<int:id>',views.rca_as_repaired_inward_accepted,name="rca_as_repaired_inward_accepted"),



    path('power_analyser',views.power_analyser,name="power_analyser"),
    path('power_analyser_inward/<int:id>',views.power_analyser_inward,name="power_analyser_inward"),
    path('power_analyser_inward_accepted/<int:id>',views.power_analyser_inward_accepted,name="power_analyser_inward_accepted"),


    
    path('drr_rel_details/<int:id>',views.drr_rel_details,name="drr_rel_details"),
    path('drr_details/<int:id>',views.drr_details,name="drr_details"),


    path('rca_gatepass_order_list',views.rca_gatepass_order_list,name="rca_gatepass_order_list"),
    path('rca_as_gatepass_details/<int:id>',views.rca_as_gatepass_details,name="rca_as_gatepass_details"),
    path('rca_as_gatepass_add/<int:id>',views.rca_as_gatepass_add,name="rca_as_gatepass_add"),
    path('rca_as_rejected_dispatch/<int:id>',views.rca_as_rejected_dispatch,name="rca_as_rejected_dispatch"),
    path('rca_as_rejected_dispatch_accept/<int:id>',views.rca_as_rejected_dispatch_accept,name="rca_as_rejected_dispatch_accept"),
    path('rca_as_gen_gatepass/<int:id>',views.rca_as_gen_gatepass,name="rca_as_gen_gatepass"),

    
    path('test_request_form_rca/<int:id>', views.test_request_form_rca, name="test_request_form_rca"),
    path('test_request_form_submit_rca/<int:id>', views.test_request_form_submit_rca, name="test_request_form_submit_rca"),

    path('rca_to_nabl_list',views.rca_to_nabl_list,name="rca_to_nabl_list"),
    path('rca_to_nabl/<int:id>',views.rca_to_nabl,name="rca_to_nabl"),
    path('rca_cgm_all_work_order/',views.rca_cgm_all_work_order,name="rca_cgm_all_work_order"),
    path('rca_cgm_order_view/<int:id>', views.rca_cgm_order_view, name="rca_cgm_order_view"),
    path('upload_digi/<int:id>',views.upload_digi,name="upload_digi"),
    path('rca_cgm_all_release_order/',views.rca_cgm_all_release_order,name="rca_cgm_all_release_order"),

    path('rca_cgm_release_view/<int:id>', views.rca_cgm_release_view, name="rca_cgm_release_view"),

    path('upload_digi_ro/<int:id>',views.upload_digi_ro,name="upload_digi_ro"),
    path('delete/<int:id>/<int:ro_id>',views.delete,name="delete"),
    path('rca_di_view_accepted/<int:id>',views.rca_di_view_accepted,name="rca_di_view_accepted"),
    
    
    #  jeevan New code
    # creater
    path('procurement_generate_po', views.procurement_Generate_PO, name='procurement_generate_po'),
    path('procurement_generate_po1/<int:id>', views.procurement_Generate_PO1, name='procurement_generate_po1'),
    path('procurement_generate_po2/<int:id>', views.procurement_Generate_PO2, name='procurement_Generate_PO2'),
    path('procurement_generate_po3/<int:id>', views.procurement_Generate_PO3, name='procurement_Generate_PO3'),
    path('procurement_generate_po4/<int:id>', views.procurement_Generate_PO4, name='procurement_Generate_PO4'),
    path('po_view/<int:id>', views.po_view, name='po_view'),
    path('send_to_approval/<int:id>', views.send_to_approval, name='send_to_approval'),

    #----------------------delete function in po at creator----------------------------------------------
    path('material_delete/<int:id>/<int:po_id>', views.material_delete, name='material_delete'),
    path('po_delete/<int:id>', views.po_delete, name="po_delete"),
    path('di_delete/<int:id>', views.di_delete, name="di_delete"),
    #--------------------------end------------------------------------------------------------------------


    # approver
    path('purchase_order', views.purchase_order, name="purchase_order"),
    #--------------------------soft delete function in PO at approver----------------------------------------------
    path('po_delete_approver/<int:id>',views.po_delete_approver,name="po_delete_approver"),
    path('di_delete_approver/<int:di_id>/<str:erp_di_no>',views.di_delete_approver, name="di_delete_approver"),
    #-----------------------------------------end-------------------------------------------------------------
    path('approver_view_purchase_order/<int:id>', views.approver_view_purchase_order, name="approver_view_purchase_order"),
    path('po_approved/<int:id>', views.po_approved, name='po_approved'),

    path('vendor_purchase_order', views.vendor_purchase_order, name="vendor_purchase_order"),
    path('view_po_details/<int:id>', views.view_po_details, name="view_po_details"),
    path('po_sd_detail/<int:id>', views.vender_sd_detail, name="vender_sd_detail"),

    path('vender_bank_detail_view/<int:id>', views.vender_bank_detail_view, name="vender_bank_detail_view"),
    
    path('vendor_bank_details_approval/', views.vendor_bank_details_approval, name="vendor_bank_details_approval"),
    path('vendor_bank_details_approved/<int:po_id>', views.vendor_bank_details_approved, name="vendor_bank_details_approved"),
    path('po_upload_digital_copy/<int:id>', views.po_upload_digital_copy, name='po_upload_digital_copy'),
    path('vendor_bank_details/', views.vendor_bank_details_approval, name="vendor_bank_details/"),
    path('vendor_gtp_rejected/<int:po_id>', views.vendor_gtp_rejected, name="vendor_gtp_rejected"),
    path('vendor_bank_details_rejected/<int:po_id>', views.vendor_bank_details_rejected, name="vendor_bank_details_rejected"),
    
    #********************************************************************************
    #------------------------------------------approver View Documnet details in CPO---------------------------------
    path('approver_view_po_details/<int:id>',views.approver_view_po_details, name='approver_view_po_details'),
    #--------------------------------------------------------end-----------------------------------------------------
    path('po_creater_DI_list', views.po_creater_DI_list, name="po_creater_DI_list"),
    path('create_dispatch_instruction/<int:id>', views.create_dispatch_instruction, name="create_dispatch_instruction"),
    path('po_approval_offered_material_view', views.po_approval_offered_material_view, name="po_approval_offered_material_view"),
    path('approver_offer_view/<int:po_id>/<int:po_material_id>', views.approver_offer_view, name="approver_offer_view"),
    path('create_di_checked_material', views.create_di_checked_material, name="create_di_checked_material"),
    path('create_di_areastores/<int:offer_material_id>/<int:po_id>/<int:po_material_id>', views.create_di_areastores, name="create_di_areastores"),
    path('create_di_step/<int:po_id>',views.create_di_step, name="create_di_step"),
    path('create_di_step1/<int:po_id>/<str:erp_di_no>',views.create_di_step1, name="create_di_step1"),
    path('send_to_approval_di/<int:id>/<str:erp_di_no>', views.send_to_approval_di, name='send_to_approval_di'),
    path('di_view_approver', views.di_view_approver, name='di_view_approver'),
    path('approver_view_di/<int:po_id>/<str:erp_di_no>',views.approver_view_di, name="approver_view_di"),
    path('di_approved/<int:id>/<str:erp_di_no>', views.di_approved, name='di_approved'),
    path('di_upload_digital_copy/<int:id>', views.di_upload_digital_copy, name='di_upload_digital_copy'),

    #-------------------------Multiple areastore---------------------------------------------------
    path('po_di_view', views.po_di_view, name='po_di_view'),
    path('check_pending_areastore/<int:id>', views.check_pending_areastore, name='check_pending_areastore'),
    path('po_di_material_view/<int:id>', views.po_di_material_view, name='po_di_material_view'),
    path('PoDiStatus/<int:id>/<str:erp_di_no>', views.PoDiStatus, name='PoDiStatus'),
    path('po_di_material_view/<int:id>', views.po_di_material_view, name='po_di_material_view'),
    path('PoDiStatus/<int:id>', views.PoDiStatus, name='PoDiStatus'),
    path('disendtogm/<int:id>',views.di_send_to_gm,name="di_send_to_gm"),
    path('disendtocgm/<int:id>',views.di_send_to_cgm,name="di_send_to_cgm"),
    path('reject_di', views.reject_di, name='reject_di'),
    path('reject_di_material_view/<int:id>',views.reject_di_material_view,name="reject_di_material_view"),
    path('create_po_gatepass/<int:id>/<str:erp_di_no>',views.create_po_gatepass,name="create_po_gatepass"),
    #-----------------------------------------end-----------------------------------------------------------

    #---------------------------------------drr and gatepass details-----------------------------------------
    path('gatepass', views.gatepass, name='gatepass'),
    path('gatepass_history/<int:id>', views.gatepass_history, name='gatepass_history'),
    path('po_receiving_material', views.po_receiving_material, name="po_receiving_material"),
    path('drr_info_history/<int:id>',views.drr_info_history, name="drr_info_history"),
    #-----------------------------------------end-----------------------------------------------------------

    # path('invert_gatepass_details/<int:id>', views.invert_gatepass_details, name='invert_gatepass_details'),

    #  po sampling Anil ================
    
    path('sample_select/<int:id>', views.sample_select, name='sample_select'),
    path('sample_select_submit/<int:id>/<str:final_random_sample_mat>', views.sample_select_submit, name='sample_select_submit'),
    
    path('select_testing_nabl/<int:id>', views.select_testing_nabl, name='select_testing_nabl'),
    path('view_sampled_material/<int:id>', views.view_sampled_material, name='view_sampled_material'),
    path('po_nabl_gatepass/<int:id>', views.po_nabl_gatepass_details, name='po_nabl_gatepass'),
    path('po_nabl_gatepass_print/<int:id>', views.po_nabl_gatepass_print, name='po_nabl_gatepass_print'),
    path('po_nabl_gatepass_upload/<int:id>', views.po_nabl_gatepass_upload, name='po_nabl_gatepass_upload'),
    path('po_nabl_update/<int:id>', views.po_nabl_update, name='po_nabl_update'),
    path('po_sample_list', views.po_sample_list, name='po_sample_list'),
    # path('disendtocgm/<int:id>',views.di_send_to_cgm,name="di_send_to_cgm"),
    path('po_logout',views.po_logout,name="po_logout"),
    path('po_trf_create', views.po_trf_create, name='po_trf_create'),
    
    path('po_nabl_result', views.po_nabl_result, name="po_nabl_result"),
    path('po_nabl_items_result/<int:id>', views.po_nabl_items_result, name="po_nabl_items_result"),
    
    
    path('po_di_sampled_item/<int:id>', views.po_di_sampled_item, name='po_di_sampled_item'),

    path('po_test_request_form_submit/<int:id>', views.po_test_request_form_submit, name='po_test_request_form_submit'),

    ######################  PO Sampling End ##############

    ######################       PO  Resampling Anil       ####################
    
    
    path('po_resampling_submit/<int:id>/<str:final_random_sample_mat>', views.po_resampling_submit, name='po_resampling_submit'),
    path('po_resampling_nabl_update/<int:id>', views.po_resampling_nabl_update, name='po_resampling_nabl_update'),
    path('po_resampling/<int:id>', views.po_resampling, name='po_resampling'),
    path('po_resampling_test_request_form_submit/<int:id>', views.po_resampling_test_request_form_submit, name='po_resampling_test_request_form_submit'),
    path('po_nabl_resampling_trf_upload/<int:id>', views.po_nabl_resampling_trf_upload, name='po_nabl_resampling_trf_upload'),
    path('po_nabl_gatepass_resampling/<int:id>', views.po_nabl_gatepass_resampling, name='po_nabl_gatepass_resampling'),
    path('po_nabl_gatepass_print_resampling/<int:id>', views.po_nabl_gatepass_print_resampling, name='po_nabl_gatepass_print_resampling'),
    path('view_Resamled_material/<int:id>', views.view_Resamled_material, name='view_Resamled_material'),
    path('po_nabl_items_resampling_result/<int:id>', views.po_nabl_items_resampling_result, name="po_nabl_items_resampling_result"),
    
       #######################  End ####################

    path('select_received_material/<int:id>/<str:erp_di_no>', views.select_received_material, name='select_received_material'),
    path('select_material_for_getpass/<int:id>/<str:erp_di_no>', views.select_material_for_getpass, name='select_material_for_getpass'),
    path('forward_nabl_order',views.forward_nabl_order,name="forward_nabl_order"),
    path('forward_nabl_order2/<int:id>',views.forward_nabl_order2,name="forward_nabl_order2"),
    path('forward_nabl_submit/<int:id>',views.forward_nabl_submit, name="forward_nabl_submit"),
    path('forward_nabl/<int:id>',views.forward_nabl, name="forward_nabl"),
    path('ro_for_trf', views.ro_for_trf, name="ro_for_trf"),
    path('ro_for_trf2/<int:id>', views.ro_for_trf2, name="ro_for_trf2"),
    
    path('uplaod_gatepass/<int:user_id>/<int:ro_id>/<int:id>', views.uplaod_gatepass, name="uplaod_gatepass"),
    
    
    path('Gatepass_areastore/<int:ro_id>', views.Gatepass_areastore, name="Gatepass_areastore"),
    path('Gatepass_areastore2/<int:gatepass_id>', views.Gatepass_areastore2, name="Gatepass_areastore2"),
    path('uplaod_gatepass/<int:user_id>/<int:ro_id>/<int:id>', views.uplaod_gatepass, name="uplaod_gatepass"),
    path('sampling_details', views.sampling_details, name="sampling_details"),
    path('sampling_details2/<int:id>', views.sampling_details2, name="sampling_details2"),
    path('sampling_nabl_details/<int:id>',views.sampling_nabl_details, name="sampling_nabl_details"),
    path('sampling_details_store', views.sampling_details_store, name="sampling_details_store"),
    path('sampling_details2_store/<int:id>', views.sampling_details2_store, name="sampling_details2_store"),
    path('sampling_nabl_details_store/<int:id>/<int:vd>',views.sampling_nabl_details_store, name="sampling_nabl_details_store"),
    
    path('rca_nabl_mat_rec_list',views.rca_nabl_mat_rec_list,name="rca_nabl_mat_rec_list"),
    path('rca_nabl_aprov_mat_list/<int:id>',views.rca_nabl_aprov_mat_list,name="rca_nabl_aprov_mat_list"),
    path('rca_nabl_aprov_gatepass_details/<int:id>',views.rca_nabl_aprov_gatepass_details,name="rca_nabl_aprov_gatepass_details"),
    path('rca_nabl_aprov_gatepass/<int:id>',views.rca_nabl_aprov_gatepass,name="rca_nabl_aprov_gatepass"),   
    path('rca_nabl_gp_xmr/<int:id>',views.rca_nabl_gp_xmr,name="rca_nabl_gp_xmr"),
    path('rca_nabl_gp_xmr_add/<int:id>',views.rca_nabl_gp_xmr_add,name="rca_nabl_gp_xmr_add"),

	path('rca_mrc_order_list',views.rca_mrc_order_list,name="rca_mrc_order_list"),
    path('rca_mrc_aprov_mat_list/<int:id>',views.rca_mrc_aprov_mat_list,name="rca_mrc_aprov_mat_list"),
    path('rca_mrc_add_release/<int:id>',views.rca_mrc_add_release,name="rca_mrc_add_release"),
    path('rca_mrc_add_copy/<int:id>',views.rca_mrc_add_copy,name="rca_mrc_add_copy"),
    path('rca_mrc_add_comment/<int:id>',views.rca_mrc_add_comment,name="rca_mrc_add_copy"),
    path('rca_mrc_view/<int:id>',views.rca_mrc_view,name="rca_mrc_view"),
    path('upload_digi_mr/<int:id>',views.upload_digi_mr,name="upload_digi_mr"),

    path('cgm_all_mrc',views.cgm_all_mrc,name="cgm_all_mrc"),

	path('rca_mrc_release_list',views.rca_mrc_release_list,name="rca_mrc_release_list"),
    
    path('po_view_DI_list', views.po_view_DI_list, name="po_view_DI_list"),
    path('send_di_for_approval/<int:di_id>/<str:erp_di_no>', views.send_di_for_approval, name="send_di_for_approval"),
    path('creater_view_di/<int:po_id>/<str:erp_di_no>', views.creater_view_di, name="creater_view_di"),
    
    
    path('select_nabl/<int:ro_id>/<str:final_mat_lst>', views.select_nabl, name="select_nabl"),
    path('select_nabl2/<int:ro_id>/<str:final_mat_lst>/<str:user_zone>', views.select_nabl2, name="select_nabl2"),
    path('TRF_generate', views.TRF_generate, name="TRF_generate"),
    
    path('Gatepass_save/<str:usr_obj2>/<str:roid>', views.Gatepass_save, name="Gatepass_save"),
    path('uplaod_gatepass/<int:gatepass_id>', views.uplaod_gatepass, name="uplaod_gatepass"),
    path('test_request_form/<int:gatepass_id>', views.test_request_form, name="test_request_form"),
    path('test_request_form_submit/<int:gatepass_id>', views.test_request_form_submit, name="test_request_form_submit"),
    path('test_request_view/<int:gatepass_id>', views.test_request_view, name="test_request_view"),
    
    path('SendMatToNabl/<int:gatepass_id>/<int:TRF_Id>/<int:roid>', views.SendMatToNabl, name="SendMatToNabl"),
    path('select_testing_nabl/<int:id>', views.select_testing_nabl, name='select_testing_nabl'),
    path('NABL_Report', views.NABL_Report, name="NABL_Report"),
    path('NABL_Report2/<str:ro_id>', views.NABL_Report2, name="NABL_Report2"),
    path('power_analyzer_api_report/<int:id>/<int:ro>',views.power_analyzer_api_report,name="power_analyzer_api_report"),
    path('po_vendor_list', views.po_vendor_list, name="po_vendor_list"),
    path('vendor_material_po_creater/<int:id>', views.vendor_check_material_po_creater, name='vendor_check_material_po_creater'),
    path('po_approver_vendor_list', views.po_approver_vendor_list, name="po_approver_vendor_list"),
    path('vendor_material_po_approver/<int:id>', views.vendor_check_material_po_approver, name='vendor_check_material_po_approver'),



        # -------------------shubham tripathi------------------
    path('po_approver_invoice_list/', views.po_approver_invoice_list, name="po_approver_invoice_list"),
    path('po_approver_invoice/', views.po_approver_invoice, name="po_approver_invoice"),
    path('po_creator_invoice_list/', views.po_creator_invoice_list, name="po_creator_invoice_list"),
    path('po_officer_invoice_list/', views.po_officer_invoice_list, name="po_officer_invoice_list"),

    path('po_cfo_invoice_list/', views.po_cfo_invoice_list, name="po_cfo_invoice_list"),
    path('po_dgmcbpu_invoice_list/', views.po_dgmcbpu_invoice_list, name="po_dgmcbpu_invoice_list"),
    path('po_aubills_invoice_list/', views.po_aubills_invoice_list, name="po_aubills_invoice_list"),
    path('po_dgmem_invoice_list/', views.po_dgmem_invoice_list, name="po_dgmem_invoice_list"),	
            # -------------------shubham tripathi code ene here------------------
    
    #******************************lokendra partial mrc*********************************
        
    path('partial_mrc_order_list',views.partial_mrc_order_list,name="partial_mrc_order_list"),
    path('partial_mrc_add_release/<int:id>',views.partial_mrc_add_release,name="partial_mrc_add_release"),
    path('partial_mrc_add_copy/<int:id>',views.partial_mrc_add_copy,name="partial_mrc_add_copy"),
    path('partial_mrc_add_comment/<int:id>',views.partial_mrc_add_comment,name="partial_mrc_add_comment"),
    path('partial_mrc_add_xmr/<int:id>',views.partial_mrc_add_xmr,name="partial_mrc_add_xmr"),
    path('partial_mrc_xmr_accepted/<int:id>',views.partial_mrc_xmr_accepted,name="partial_mrc_xmr_accepted"),
    path('partial_mrc_view/<int:id>',views.partial_mrc_view,name="partial_mrc_view"),
    
    path('partial_mrc_sign_list',views.partial_mrc_sign_list,name="partial_mrc_sign_list"),
    path('upload_digi_partial_mrc/<int:id>',views.upload_digi_partial_mrc,name="upload_digi_partial_mrc"),
    

    #------------------------------PO MRC create-----------------------------------------
    path('po_mrc_order_list',views.po_mrc_order_list,name="po_mrc_order_list"),
    path('view_test_result/<int:id>',views.view_test_result,name="view_test_result"),
    path('po_mrc_add_release/<int:id>',views.po_mrc_add_release,name="po_mrc_add_release"),
    path('po_mrc_add_copy/<int:id>',views.po_mrc_add_copy,name="po_mrc_add_copy"),
    path('po_mrc_add_comment/<int:id>',views.po_mrc_add_comment,name="po_mrc_add_comment"),
    path('po_view_mrc/<int:id>',views.po_view_mrc,name="po_view_mrc"),
    path('po_mrc_release_list',views.po_mrc_release_list,name="po_mrc_release_list"),
    path('upload_digital_po_mrc/<int:id>',views.upload_digital_po_mrc,name="upload_digital_po_mrc"),
    #----------------------------------------------end------------------------------------

    #----------------------------------view PO MRC----------------------------------------------
    path('las_view_mrc/<int:id>',views.las_view_mrc,name="las_view_mrc"),
    path('view_mrc_creator/<str:erp_di_no>',views.view_mrc_creator,name="view_mrc_creator"),
    path('view_mrc_approver/<str:erp_di_no>',views.view_mrc_approver,name="view_mrc_approver"),
    # #---------------------------------end---------------------------------------------------

    #---------------------------------------PO NABL Approved Items----------------------------------------------
    path('nabl_approved_di_items',views.nabl_approved_di_items,name="nabl_approved_di_items"),
    path('nabl_approve_di_material_view/<int:id>',views.nabl_approve_di_material_view,name="nabl_approve_di_material_view"),
    # ---------------------------------------end---------------------------------------------------------------

    #---------------------------------------PO_NABL_REJECTED_AT_LAS-------------------------------------------
    path('nabl_check_di_status',views.nabl_check_di_status,name="nabl_check_di_status"),
    path('nabl_reject_di',views.nabl_reject_di,name="nabl_reject_di"),
    path('nabl_reject_di_material_view/<int:id>',views.nabl_reject_di_material_view,name="nabl_reject_di_material_view"),
    path('create_nabl_reject_di_gatepass/<int:id>/<str:erp_di_no>',views.create_nabl_reject_di_gatepass,name="create_nabl_reject_di_gatepass"),
    path('rejected_di_send_to_Vendor/<int:id>',views.rejected_di_send_to_Vendor,name="rejected_di_send_to_Vendor"),
    #----------------------------------------------end----------------------------------------------------------

    path('po_pending_sample_list', views.po_pending_sample_list, name='po_pending_sample_list'),
    
    ##### handle logout lok#######
    path('logout',views.handle_logout,name="handle_logout"),

]
