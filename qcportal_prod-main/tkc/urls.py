from django.contrib import admin
from django.urls import path
from tkc import views

urlpatterns = [
    path('login', views.Logout, name='Logout'),
    path('tkc_reg_seven', views.tkc_reg_seven, name='tkc_reg_seven'),
    path('tkc_reg_eight', views.tkc_reg_eight, name='tkc_reg_eight'),

    path('tkc_reg_nine', views.tkc_reg_nine, name='tkc_reg_nine'),

    path('tkc_reg_ten', views.tkc_reg_ten, name='tkc_reg_ten'),
    # path('tkc_reg_declare', views.tkc_reg_declare, name='tkc_reg_declare'),
    path('tkc_reg_eleven', views.tkc_reg_eleven, name='tkc_reg_eleven'),
    path('tkc_reg_twelve', views.tkc_reg_twelve, name='tkc_reg_twelve'),

    path('base', views.base, name='base'),
    path('updatedata', views.updatedata, name='updatedata'),
    path('basic', views.basic, name='basic'),
    path('complete', views.complete, name='complete'),
    path('activation', views.activation, name='activation'),
    path('upgrade', views.upgrade, name='upgrade'),
    path('tkc_update', views.tkc_update, name='tkc_update'),
    path('tkc_sd_payment', views.tkc_sd_payment, name='tkc_sd_payment'),
    path('rejected_doc', views.rejected_doc, name='rejected_doc'),
    path('rejected_doc_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),
    path('rejected_doc_finance_save/<int:id>', views.rejected_doc_finance_save, name='rejected_doc_finance_save'),
    path('rejected_doc_cgm_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),
    path('message', views.message, name='message'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('activation_after_expired', views.activation_after_expired, name='activation_after_expired'),
    path('activation_before_expired', views.activation_before_expired, name='activation_before_expired'),
    path('vendor_otp_verify', views.vendor_otp_verify, name='vendor_otp_verify'),
    
    path('fake_called', views.Fake_called, name='fake_called'),
    path('rejected_offer', views.rejected_offer, name='rejected_offer'),
    path('pdi_details/<str:offer_no>', views.pdi_details, name='pdi_details'),

    #####
    # path('payu_demo1',views.payu_demo1,name="payu_demo1"),
    # path('success',views.payu_success1,name='payu_success1'),
    # path('payu/failure',views.payu_failure,name='payu_failure'),
    path('all_active_contractors_list/', views.active_contractors_new, name="all_active_contractors_list"),




    path('payu_demo_tkc',views.payu_demo_tkc,name="payu_demo_tkc"),
    path('payu/success',views.payu_success_tkc,name='payu_success_tkc'),
    path('payu/failure',views.payu_failure,name='payu_failure'),
    path('payu/gen_invoice_first_tkc', views.gen_invoice_first_tkc, name='gen_invoice_first_tkc'),
    path('tkc_view_profile',views.tkc_view_profile,name='tkc_view_profile'),
    path('transaction_history', views.transaction_history, name='transaction_history'),
    path('payu_demo_tkc',views.payu_demo_tkc,name="payu_demo_tkc"),
    # upgrade Url
    path('upgrade_tkc_one', views.upgrade_tkc_one, name="upgrade_tkc_one"),
    path('upgrade_tkc_two', views.upgrade_tkc_two, name="upgrade_tkc_two"),
    path('upgrade_tkc_three', views.upgrade_tkc_three, name="upgrade_tkc_three"),
    path('upgrade_tkc_four', views.upgrade_tkc_four, name="upgrade_tkc_four"),
    path('activation_payment_check', views.activation_payment_check, name="activation_payment_check"),
    path('activation_tkc_three', views.activation_tkc_three, name="activation_tkc_three"),

    path('wo', views.wo, name='wo'),
    path('all_wo', views.all_wo, name='all_wo'),
    path('upload_bg_loc', views.upload_bg_loc, name='upload_bg_loc'),
    # path('upload_bg/<int:PO_id>', views.upload_bg, name="upload_bg"),
    path('view_wo/<int:PO_id>', views.view_wo, name="view_wo"),
    # path('upload_loc/<int:PO_id>', views.upload_loc, name="upload_loc"),
    path('upload_bg_save/<int:PO_id>', views.upload_bg_save, name="upload_bg_save"),
    path('upload_loc_save/<int:PO_id>', views.upload_loc_save, name="upload_loc_save"),
    path('upload/<int:PO_id>', views.upload_loc_save, name="upload_loc_save"),
    path('upload_vendor', views.upload_vendor, name="upload_vendor"),
    path('add_vendor', views.add_vendor, name="add_vendor"),
    path('rejected_doc_GM_save/<int:id>', views.rejected_doc_GM_save, name='rejected_doc_GM_save'),
    path('profile_status', views.profile_status, name="profile_status"),
    path('active_contractors_list/', views.active_contractors, name="active_contractors_list"),
    
    


    path('wo', views.wo, name='wo'),
    path('upload_bank/<int:wo_id>', views.upload_Bank, name="upload_Bank"),
    path('upload_bg/<int:wo_id>', views.upload_bg, name="upload_bg"),
    path('bg_sumit_for_approval/<int:wo_id>/<int:bg_id>', views.bg_sumit_for_approval, name="bg_sumit_for_approval"),
    path('upload_bg/<int:wo_id>', views.upload_bg, name="upload_bg"),
    path('bg_sumit_for_approval/<int:wo_id>/<int:bg_id>', views.bg_sumit_for_approval, name="bg_sumit_for_approval"),
    path('bg_delete/<int:wo_id>/<int:bg_id>', views.bg_delete, name="bg_delete"),
    path('upload_loc/<int:wo_id>', views.upload_loc, name="upload_loc"),
    path('loc_sumit_for_approval/<int:wo_id>/<int:bg_id>', views.loc_sumit_for_approval, name="loc_sumit_for_approval"),
    path('loc_delete/<int:wo_id>/<int:bg_id>', views.loc_delete, name="loc_delete"),
    path('upload_pert/<int:wo_id>', views.upload_pert, name="upload_pert"),
    path('pert_sumit_for_approval/<int:wo_id>/<int:bg_id>', views.pert_sumit_for_approval, name="pert_sumit_for_approval"),
    path('pert_delete/<int:wo_id>/<int:bg_id>', views.pert_delete, name="pert_delete"),
    path('upload_mqpdoc/<int:wo_id>', views.upload_mqpdoc, name="upload_mqpdoc"),
    path('upload_fqpdoc/<int:wo_id>', views.upload_fqpdoc, name="upload_fqpdoc"),
    path('mqpdoc_sumit_for_approval/<int:wo_id>/<int:bg_id>', views.mqpdoc_sumit_for_approval, name="mqpdoc_sumit_for_approval"),
    path('fqpdoc_sumit_for_approval/<int:wo_id>/<int:bg_id>', views.fqpdoc_sumit_for_approval, name="fqpdoc_sumit_for_approval"),
    path('mqpdoc_delete/<int:wo_id>/<int:bg_id>', views.mqpdoc_delete, name="mqpdoc_delete"),
    path('fqpdoc_delete/<int:wo_id>/<int:bg_id>', views.fqpdoc_delete, name="fqpdoc_delete"),
    path('upload_otherdoc/<int:wo_id>', views.upload_otherdoc, name="upload_otherdoc"),
    path('otherdoc_sumit_for_approval/<int:wo_id>/<int:bg_id>', views.otherdoc_sumit_for_approval, name="otherdoc_sumit_for_approval"),
    path('otherdoc_delete/<int:wo_id>/<int:bg_id>', views.otherdoc_delete, name="otherdoc_delete"),
    path('tkc_vendor_approval/<int:wo_id>/<int:bg_id>', views.tkc_vendor_approval, name="tkc_vendor_approval"),
    path('tkc_vendor_delete/<int:wo_id>/<int:bg_id>', views.tkc_vendor_delete, name="tkc_vendor_delete"),


    path('upload_bg_loc', views.upload_bg_loc, name='upload_bg_loc'),
    path('material_offer/<int:v_id>', views.material_offer, name='material_offer'),
    path('material_offer_delete/<int:v_id>/<int:offer_id>', views.material_offer_delete, name='material_offer_delete'),
    path('material_offer_submit/<int:v_id>/<int:offer_id>', views.material_offer_submit, name='material_offer_submit'),
    path('upload_item/<int:offer_id>', views.upload_item, name='upload_item'),
    path('item_delete/<int:offer_id>/<int:item_id>', views.item_delete, name='item_delete'),

    path('upload_bg_save/<int:wo_id>', views.upload_bg_save, name="upload_bg_save"),
    path('upload_loc_save/<int:wo_id>', views.upload_loc_save, name="upload_loc_save"),
    path('upload/<int:wo_id>', views.upload_loc_save, name="upload_loc_save"),
    path('upload_vendor', views.upload_vendor, name="upload_vendor"),
    path('add_vendor/<int:wo_id>', views.add_vendor, name="add_vendor"),
    path('invoicing', views.invoicing, name='invoicing'),
    # path('add_vendor', views.add_vendor, name="add_vendor"),
    # path('view_wo/<int:PO_id>', views.view_wo, name="view_wo"),
    path('api_response_data', views.api_response_data, name="api_response_data"),  
    path('transaction_history_copy_tkc/<int:id>', views.transaction_history_copy_tkc, name='transaction_history_copy_tkc'),
    path('tkc_reg_declare', views.tkc_reg_declare, name='tkc_reg_declare'),

    
    path('add-site-store', views.addsitestore, name='addsitestore'),
    path('save_tks_site_store', views.save_tks_site_store, name='save_tks_site_store'),
    path('all_di', views.all_di, name="all_di"),
    path('view_di_material/<int:di_id>', views.view_di_material, name='view_di_material'),
    path('dispatch_all_di_items/<int:di_id>',views.dispatch_all_di_items,name='dispatch_all_di_items'),
    # path('select_material_sitestore/<int:offer_id>/<int:di_id>/<int:division_id>', views.select_material_sitestore, name='select_material_sitestore'),
    # path('create_di_for_sitestore/<int:offer_id>/<int:di_id>/<int:division_id>', views.create_di_for_sitestore, name='create_di_for_sitestore'),
    
    
    # add on docs for wo
    path('approved_vendor_list', views.approved_vendor_list, name="approved_vendor_list"),
    path('vendor_material_details_view/<int:id>', views.vendor_check_material_tkc, name='vendor_check_material_tkc'),
    path('receving_wo_material', views.receving_wo_material, name="receving_wo_material"),
    path('site_store_item_received/<int:tkc_di_id>/<str:offer>', views.site_store_item_received, name="site_store_item_received"),
    path('site_store_wo_pdi_material_view/<int:tkc_di_id>/<str:id>', views.site_store_wo_pdi_material_view, name='site_store_wo_pdi_material_view'),
    path('tkc_site_store_material_drr/<int:tkc_di_id>/<str:offer>', views.tkc_site_store_material_drr, name='tkc_site_store_material_drr'),
    path('tkc_wo_send_to_cgm/<int:tkc_di_id>/<int:id>', views.tkc_wo_send_to_cgm, name='tkc_wo_send_to_cgm'),
    path('tkc_wo_sample_list', views.tkc_wo_sample_list, name="tkc_wo_sample_list"),
    path('tkc_wo_sample_sampling/<str:offer>', views.tkc_wo_sample_sampling, name='tkc_wo_sample_sampling'),
    path('tkc_view_samled_material/<str:offer>', views.tkc_view_samled_material, name='tkc_view_samled_material'),

    
# ------modified by shubham tripathi and akash change flow di wise----------------
    
    
    path('outward_gatepass', views.outward_gatepass, name="outward_gatepass"),
    path('tkc_reject_di_material_view/<int:id>', views.tkc_reject_di_material_view, name='tkc_reject_di_material_view'),
    path('select_material_for_getpass/<int:id>', views.select_material_for_getpass, name='select_material_for_getpass'),
    path('create_wo_gatepass_outward/<int:id>', views.create_wo_gatepass_outward, name='create_wo_gatepass_outward'),
    path('outward_gatepass_history', views.outward_gatepass_history, name="outward_gatepass_history"),
    path('outward_gatepass_view/<int:id>', views.outward_gatepass_view, name='outward_gatepass_view'),
    path('add_officer_details/<int:tkc_di_id>/<str:offer>', views.add_officer_details, name='add_officer_details'),
    path('site_store_item_received_from_nabl/<str:offer>', views.site_store_item_received_from_nabl, name='site_store_item_received_from_nabl'),
    path('tkc_wo_receive_from_nabl', views.tkc_wo_receive_from_nabl, name="tkc_wo_receive_from_nabl"),

    
    path('receving_wo_material_circle/<str:offer>', views.receving_wo_material_circle, name="receving_wo_material_circle"),
    path('site_store_item_received_officer/<int:tkc_di_id>/<str:offer>', views.site_store_item_received_officer, name="site_store_item_received_officer"),
    path('site_store_wo_pdi_material_view_officer/<int:tkc_di_id>/<str:offer>', views.site_store_wo_pdi_material_view_officer, name='site_store_wo_pdi_material_view_officer'),
    path('tkc_site_store_material_received_officer/<int:tkc_di_id>/<str:offer>', views.tkc_site_store_material_received_officer, name='tkc_site_store_material_received_officer'),
    path('gm_circle_view_wo', views.gm_circle_view_wo, name="gm_circle_view_wo"),
    path('gm_circle_assine_officer/<int:id>', views.gm_circle_assine_officer, name='gm_circle_assine_officer'),
    path('gm_circle_assined_officer_details', views.gm_circle_assined_officer_details, name="gm_circle_assined_officer_details"),
    
    



    # new offer multiple material url's
    path('all_vendor', views.all_vendor, name='all_vendor'),
    path('wo_approve_vendor_list/<int:wo_id>',views.wo_approve_vendor_list,name = 'wo_approve_vendor_list'),
    path('wo_approve_vendor_material_list/<int:wo_id>/<int:vendor_id>',views.wo_approve_vendor_material_list,name = "wo_approve_vendor_material_list"),
    path('wo_material_offer_step1/<int:wo_id>/<str:itemcode>/<int:vendor_id>',views.wo_material_offer_step1,name = "wo_material_offer_step1"),
    path('save_material_offer_store/<int:wo_id>/<str:itemcode>/<int:vendor_id>',views.save_material_offer_store,name= "save_material_offer_store"),
    path('delete_material_offer_store/<int:wo_id>/<str:itemcode>/<int:id>/<int:vendor_id>',views.delete_material_offer_store,name= "delete_material_offer_store"),
    path('upload_wo_material_serial_no_excel/<int:wo_id>/<str:itemcode>/<int:id>/<int:vendor_id>',views.upload_wo_material_serial_no_excel,name= "upload_wo_material_serial_no_excel"),
    path('offer_material/<int:wo_id>/<int:vendor_id>',views.offer_material,name = 'offer_material'),
    path('upload_excel_options/<int:wo_id>/<str:itemcode>/<int:id>/<int:vendor_id>',views.upload_excel_options,name= "upload_excel_options"),
    path('download_batch_demo_excel', views.download_batch_demo_excel, name="download_batch_demo_excel"),
    path('tkc_wo_offred_material_data', views.tkc_wo_offred_material_data, name="tkc_wo_offred_material_data"),
    path('tkc_offered_materials/<int:wo_id>', views.tkc_offered_materials, name="tkc_offered_materials"),
    path('remove_added_offer_material/<int:wo_id>/<str:itemcode>/<int:vendor_id>/<int:offer_id>', views.remove_added_offer_material, name="remove_added_offer_material"),
    
    
    
    


    # urls for circle mapping with sitestore and offer
    path('view-site-store', views.viewsitestore, name='viewsitestore'),
    path('tag_sitestore_circle/<int:store_id>', views.tag_sitestore_circle, name='tag_sitestore_circle'),
    path('save_sitestore_circle/<int:store_id>', views.save_sitestore_circle, name='tag_sitestore_circle'),
    path('sitestore_circles/<int:store_id>', views.sitestore_circles, name='sitestore_circles'),

       


    # add on docs for wo
    path('Discrepancies_found_in_Survey/<int:wo_id>', views.Discrepancies_found_in_Survey, name="Discrepancies_found_in_Survey"),
    path('wo_approve_vendor_material_list_test/<int:wo_id>/<int:vendor_id>/<int:boq_id>/<int:supplier_id>',views.wo_approve_vendor_material_list_test,name = "wo_approve_vendor_material_list_test"),

# BOQ urls        
    path('verify_boq_list', views.verify_boq_list, name="verify_boq_list"),
    path('verify_boq/<int:wo_id>', views.verify_boq, name="verify_boq"),
    path('save_verified_boq_data/<int:wo_id>', views.save_verified_boq_data, name="save_verified_boq_data"),
    path('save_boq_data/<int:wo_id>', views.save_boq_data, name="save_boq_data"),
    path('verify_boq_edit/<int:wo_id>', views.verify_boq_edit, name="verify_boq_edit"),    
    path('save_boq_info/<int:wo_id>/<int:identifier>', views.save_boq_info, name="save_boq_info"), 

# --------------------shubham tripathi fqp intimation inspection 9 march code -------------------
    path('tkc_circle_list/', views.tkc_circle_list, name="tkc_circle_list"),
    path('tkc_division_list/', views.tkc_division_list, name="tkc_division_list"),
    path('tkc_sub_division_list/', views.tkc_sub_division_list, name="tkc_sub_division_list"),
    path('tkc_division_circle_list/', views.tkc_division_circle_list, name="tkc_division_circle_list"),

    path('tkc_fqpintimation/', views.tkc_fqpintimation, name="tkc_fqpintimation"),
    path('tkc_fqpintimation_list/', views.tkc_fqpintimation_list, name="tkc_fqpintimation_list"),
    path('tkc_fqpintimation_create/', views.tkc_fqpintimation_create, name="tkc_fqpintimation_create"),
    path('tkc_fqpintimation_observation_detail/', views.tkc_fqpintimation_observation_detail, name="tkc_fqpintimation_observation_detail"),
   
      # ------------------start of urls by ravindra and gaurav for consumerbid-------------------------#
     
    path('consumer-estimation', views.consumer_estimation, name='consumer-estimation'),
    path('place_bid_data', views.place_bid_data, name='place_bid_data'),
    path('contractor-details/<str:id>', views.contractor_details, name='contractor-details'),
    path('contractor-display', views.contractor_display, name='contractor-display'),
    path('consumer-estimation-offline', views.consumer_estimation_offline, name='consumer-estimation-offline'),
    path('consumerbid/', views.ConsumerbidView.as_view()), #get_api_url
    path('contractor_selection_papi', views.contractorSelectionView.as_view()), #post_api_url
    # path('consumer_estimation', views.TKC_ConsumerCreateAPIView.as_view()), #post_api_url
    path('bid-accept/<int:id>',views.bid_accept,name="bid-accept"),
    path('bid-reject/<int:id>',views.bid_reject,name="bid_reject"),
    path('view_work/<int:id>',views.view_work,name="view_work"),
    path('contractor_selectiondisplay/<int:uid>',views.Contractor_selectionview2,name="contractor_selectiondisplay"),
    path('interested/<int:id>',views.interested,name="interested"),
    path('not_interested/<int:id>',views.not_interested,name="not_interested"), 
    path('requested_bid_data',views.requested_bid_data,name="requested_bid_data"), 
    path('contractor_work_started/<str:CAN>',views.contractor_work_started,name="contractor_work_started"), 
    path('contractor_selectiondisplay',views.contractor_status,name="contractor_status"),
    path('contractor_bid_details',views.contractor_bid_details,name="contractor_bid_details"),
    path('contractor_bid_details1',views.all_contractors,name="all_contractors"),
    path("update_contractor_work/<int:pk>",views.update_contractor_work, name="update_contractor_work"),
    path("update_contractor_page/<int:pk>",views.update_contractor_page, name="update_contractor_page"),
    
    #-------------------end of urls by ravindra and gaurav for consumerbid-------------------------------#
    
    
    
    
    
# ----------tkc invoice------------------------
     # ------------shubham tripathi code start from here
    path('tkc_wo_invoice_list/', views.tkc_wo_invoice_list, name="tkc_wo_invoice_list"),
    path('tkc_invoice_list/', views.tkc_invoice_list, name="tkc_invoice_list"),
    path('tkc_invoice_generate/', views.tkc_invoice_generate, name="tkc_invoice_generate"),
    
    
    #-----------------------------------TKC MRC add by Gaurav Pathak------------------------------
    #-----------------------TKC MRC GM Circle------------------
    path('tkc_mrc_offer_list/', views.tkc_mrc_offer_list, name="tkc_mrc_offer_list"),
    path('create_mrcview/', views.create_mrcview, name="create-mrcview"),
    
    path('format_tk_create/<int:id>', views.format_tk_create, name="format_tk_create"),
    
    
    path('tkc_mrc_sign_list/<int:id>',views.tkc_mrc_sign_list,name="tkc_mrc_sign_list"),
    path('upload_digi_tkc_mrc/<int:id>',views.upload_digi_tkc_mrc,name="upload_digi_tkc_mrc"),
    
    
    #-----------------------TKC MRC STC------------------
    
    path('tkc_mrc_offer_list_stc/', views.tkc_mrc_offer_list_stc, name="tkc_mrc_offer_list_stc"),
    path('create_mrcview_stc/', views.create_mrcview_stc, name="create-mrcview_stc"),
    path('tkc_mrc_add_offer_stc/<int:id>', views.tkc_mrc_add_offer_stc, name="tkc_mrc_add_offer_stc"),
    
    path('format_tk_stc/<int:id>', views.format_tk_stc, name="format_tk_stc"),
    path('format_tk_create_stc/<int:id>', views.format_tk_create_stc, name="format_tk_create_stc"),
    
    
    path('tkc_mrc_sign_list_stc/<int:id>',views.tkc_mrc_sign_list_stc,name="tkc_mrc_sign_list_stc"),
    path('upload_digi_tkc_mrc_stc/<int:id>',views.upload_digi_tkc_mrc_stc,name="upload_digi_tkc_mrc_stc"),
    
    path('tkc_mrc_nabl_report_stc/<int:id>', views.tkc_mrc_nabl_report_stc, name="tkc_mrc_nabl_report_stc"),
    
    
    #-----------------------TKC MRC ONM------------------
    
    path('tkc_mrc_offer_list_onm/', views.tkc_mrc_offer_list_onm, name="tkc_mrc_offer_list_onm"),
    path('create_mrcview_onm/', views.create_mrcview_onm, name="create-mrcview_onm"),
    
    path('format_tk_create_onm/<int:id>', views.format_tk_create_onm, name="format_tk_create_onm"),
    
    
    path('tkc_mrc_sign_list_onm/<int:id>',views.tkc_mrc_sign_list_onm,name="tkc_mrc_sign_list_onm"),
    path('upload_digi_tkc_mrc_onm/<int:id>',views.upload_digi_tkc_mrc_onm,name="upload_digi_tkc_mrc_onm"),
    
    path('tkc_mrc_nabl_report_onm/<int:id>', views.tkc_mrc_nabl_report_onm, name="tkc_mrc_nabl_report_onm"),
    
    #----------------------TKC MRC TKC Dashboard-------------------
     
    path('tkc_mrc_offer_list_tkc/', views.tkc_mrc_offer_list_tkc, name="tkc_mrc_offer_list_tkc"),
    path('tkc_mrc_sign_list_tkc/<int:id>',views.tkc_mrc_sign_list_tkc,name="tkc_mrc_sign_list_tkc"),

    #----------------------TKC MRC wo creator Dashboard-------------------
    
    path('tkc_mrc_offer_list_wo_creator/', views.tkc_mrc_offer_list_wo_creator, name="tkc_mrc_offer_list_wo_creator"),
    path('tkc_mrc_sign_list_wo_creator/<int:id>',views.tkc_mrc_sign_list_wo_creator,name="tkc_mrc_sign_list_wo_creator"),
    
    #----------------------TKC MRC wo approver Dashboard-------------------
    
    path('tkc_mrc_offer_list_wo_approver/', views.tkc_mrc_offer_list_wo_approver, name="tkc_mrc_offer_list_wo_approver"),
    path('tkc_mrc_sign_list_wo_approver/<int:id>',views.tkc_mrc_sign_list_wo_approver,name="tkc_mrc_sign_list_wo_approver"),

    #----------------------TKC MRC sitestore Dashboard-------------------
    
    path('tkc_mrc_offer_list_sitestore/', views.tkc_mrc_offer_list_sitestore, name="tkc_mrc_offer_list_sitestore"),
    path('tkc_mrc_sign_list_sitestore/<int:id>',views.tkc_mrc_sign_list_sitestore,name="tkc_mrc_sign_list_sitestore"),

    #-----------------------TKC MRC DGM STC DI-----------------------
    
    path('tkc_mrc_offer_list_stc_di/', views.tkc_mrc_offer_list_stc_di, name="tkc_mrc_offer_list_stc_di"),
    
    path('tkc_mrc_all_di_stc_di/<int:id>',views.tkc_mrc_all_di_stc_di,name="tkc_mrc_all_di_stc_di"),
    
    # path('format_tk_create_stc_di/<int:di_id>', views.format_tk_create_stc_di, name="format_tk_create_stc_di"),
    path('format_tk_create_stc_di/<int:id>', views.format_tk_create_stc_di, name="format_tk_create_stc_di"),
    
    path('tkc_mrc_sign_list_stc_di/<int:id>',views.tkc_mrc_sign_list_stc_di,name="tkc_mrc_sign_list_stc_di"),
    
    path('upload_digi_tkc_mrc_stc_di/<int:id>',views.upload_digi_tkc_mrc_stc_di,name="upload_digi_tkc_mrc_stc_di"),
    
    path('tkc_mrc_nabl_report_stc_di/<int:id>', views.tkc_mrc_nabl_report_stc_di, name="tkc_mrc_nabl_report_stc_di"),
    

    #-----------------------TKC MRC DGM ONM DI------------------------
    
    path('tkc_mrc_offer_list_onm_di/', views.tkc_mrc_offer_list_onm_di, name="tkc_mrc_offer_list_onm_di"),
    
    path('tkc_mrc_all_di_onm_di/<int:id>',views.tkc_mrc_all_di_onm_di,name="tkc_mrc_all_di_onm_di"),
    
    path('format_tk_create_onm_di/<int:id>', views.format_tk_create_onm_di, name="format_tk_create_onm_di"),
    
    path('tkc_mrc_sign_list_onm_di/<int:id>',views.tkc_mrc_sign_list_onm_di,name="tkc_mrc_sign_list_onm_di"),
    
    path('upload_digi_tkc_mrc_onm_di/<int:id>',views.upload_digi_tkc_mrc_onm_di,name="upload_digi_tkc_mrc_onm_di"),
        
    path('tkc_mrc_nabl_report_onm_di/<int:id>', views.tkc_mrc_nabl_report_onm_di, name="tkc_mrc_nabl_report_onm_di"),


    #-------------------------TKC MRC GM circle DI---------------------
    
    path('tkc_mrc_offer_list_gm_di/', views.tkc_mrc_offer_list_gm_di, name="tkc_mrc_offer_list_gm_di"),
    
    path('tkc_mrc_all_di_gm_di/<int:id>',views.tkc_mrc_all_di_gm_di,name="tkc_mrc_all_di_gm_di"),
    
    path('tkc_mrc_sign_list_gm_di/<int:id>',views.tkc_mrc_sign_list_gm_di,name="tkc_mrc_sign_list_gm_di"),
    
    
    #-------------------------TKC MRC TKC DI---------------------
    
    path('tkc_mrc_offer_list_tkc_di/', views.tkc_mrc_offer_list_tkc_di, name="tkc_mrc_offer_list_tkc_di"),
    
    path('tkc_mrc_all_di_tkc_di/<int:id>',views.tkc_mrc_all_di_tkc_di,name="tkc_mrc_all_di_tkc_di"),
    
    path('tkc_mrc_sign_list_tkc_di/<int:id>',views.tkc_mrc_sign_list_tkc_di,name="tkc_mrc_sign_list_tkc_di"),
    
    
    #-------------------------TKC MRC WO CREATOR DI---------------------
    
    path('tkc_mrc_offer_list_wo_creator_di/', views.tkc_mrc_offer_list_wo_creator_di, name="tkc_mrc_offer_list_wo_creator_di"),
    
    path('tkc_mrc_all_di_wo_creator_di/<int:id>',views.tkc_mrc_all_di_wo_creator_di,name="tkc_mrc_all_di_wo_creator_di"),
    
    path('tkc_mrc_sign_list_wo_creator_di/<int:id>',views.tkc_mrc_sign_list_wo_creator_di,name="tkc_mrc_sign_list_wo_creator_di"),


    #-------------------------TKC MRC WO APPROVER DI---------------------
    
    path('tkc_mrc_offer_list_wo_approver_di/', views.tkc_mrc_offer_list_wo_approver_di, name="tkc_mrc_offer_list_wo_approver_di"),
    
    path('tkc_mrc_all_di_wo_approver_di/<int:id>',views.tkc_mrc_all_di_wo_approver_di,name="tkc_mrc_all_di_wo_approver_di"),
    
    path('tkc_mrc_sign_list_wo_approver_di/<int:id>',views.tkc_mrc_sign_list_wo_approver_di,name="tkc_mrc_sign_list_wo_approver_di"),

    #-------------------------TKC MRC Site Store DI---------------------
    
    path('tkc_mrc_offer_list_sitestore_di/', views.tkc_mrc_offer_list_sitestore_di, name="tkc_mrc_offer_list_sitestore_di"),
    
    path('tkc_mrc_all_di_sitestore_di/<int:id>',views.tkc_mrc_all_di_sitestore_di,name="tkc_mrc_all_di_sitestore_di"),
    
    path('tkc_mrc_sign_list_sitestore_di/<int:id>',views.tkc_mrc_sign_list_sitestore_di,name="tkc_mrc_sign_list_sitestore_di"),

    #-------------------------TKC MRC PMA DI---------------------
    
    path('tkc_mrc_offer_list_pma_di/', views.tkc_mrc_offer_list_pma_di, name="tkc_mrc_offer_list_pma_di"),
    
    path('tkc_mrc_all_di_pma_di/<int:id>',views.tkc_mrc_all_di_pma_di,name="tkc_mrc_all_di_pma_di"),
    
    path('tkc_mrc_sign_list_pma_di/<int:id>',views.tkc_mrc_sign_list_pma_di,name="tkc_mrc_sign_list_pma_di"),


    #----------------------------------TKC MRC by Gaurav Pathak end here--------------------------------




# ---------------- new fqp intimantion list-- added by shubham tripathi 21 june 2023--------------------
    path('tkc_new_fqpintimation_wo/', views.tkc_new_fqpintimation_wo, name="tkc_new_fqpintimation_wo"),
    path('tkc_new_fqpintimation_tasklist/', views.tkc_new_fqpintimation_tasklist, name="tkc_new_fqpintimation_tasklist"),
    path('tkc_new_fqpintimation_list/', views.tkc_new_fqpintimation_list, name="tkc_new_fqpintimation_list"),
    path('tkc_new_fqpintimation_create/', views.tkc_new_fqpintimation_create, name="tkc_new_fqpintimation_create"),
    path('tkc_new_fqpintimation_observation_detail/', views.tkc_new_fqpintimation_observation_detail, name="tkc_new_fqpintimation_observation_detail"),
    path('tkc_new_fqpintimation_observation_review/', views.tkc_new_fqpintimation_observation_review, name="tkc_new_fqpintimation_observation_review"),
    path('tkc_fqpintimation_milestone_category_list/', views.tkc_fqpintimation_milestone_category_list, name="tkc_fqpintimation_milestone_category_list"),
    path('tkc_new_fqpintimation_addmilestone_category/', views.tkc_new_fqpintimation_addmilestone_category, name="tkc_new_fqpintimation_addmilestone_category"),
# ---------------- new fqp intimantion list-- added by shubham tripathi 21 june 2023- end here-------------------
    

    path('mrc_offer_list/', views.mrc_offer_list, name="mrc_offer_list"),
    path('tkc_mrc_all_di/<int:id>', views.tkc_mrc_all_di, name="tkc_mrc_all_di"),
    path('tkc_mrc_sign_list/<int:id>', views.tkc_mrc_sign_list, name="tkc_mrc_sign_list"),

    path('mrc_offer_list_approver/', views.mrc_offer_list_approver, name="mrc_offer_list_approver"),
    path('tkc_mrc_all_di_approver/<int:id>', views.tkc_mrc_all_di_approver, name="tkc_mrc_all_di_approver"),
    path('tkc_mrc_sign_list_approver/<int:id>', views.tkc_mrc_sign_list_approver, name="tkc_mrc_sign_list_approver"),


    # url for to-do list
    
    path('tkc_todo_list', views.tkc_todo_list, name="tkc_todo_list"),
    path('all_pending_di', views.all_pending_di, name="all_pending_di"),
    
    # path('tkc_invoice_data/', views.tkc_invoice_data, name="tkc_invoice_data"),
    path('pending_invoice_wo_list', views.pending_invoice_wo_list, name="pending_invoice_wo_list"),
    path('pending_invoice_list/', views.pending_invoice_list, name="pending_invoice_list"),

    path('pending_upload_bg/', views.pending_upload_bg, name="pending_upload_bg"),
    path('pending_upload_loc/', views.pending_upload_loc, name="pending_upload_loc"),
    path('pending_upload_pert/', views.pending_upload_pert, name="pending_upload_pert"),
    path('pending_mqpdoc/', views.pending_mqpdoc, name="pending_mqpdoc"),
    path('pending_upload_fqpdoc/', views.pending_upload_fqpdoc, name="pending_upload_fqpdoc"),
    path('pending_otherdoc/', views.pending_otherdoc, name="pending_otherdoc"),
    
    path('new_fqpintimation/', views.new_fqpintimation, name="new_fqpintimation"),
    path('new_fqpintimation_tasklist/', views.new_fqpintimation_tasklist, name="new_fqpintimation_tasklist"),
    path('new_fqpintimation_list/', views.new_fqpintimation_list, name="new_fqpintimation_list"),
   

    path('nabl_selection', views.nabl_selection, name="nabl_selection"),
    path('tkc_nabl_selection_new', views.tkc_nabl_selection_new, name="tkc_nabl_selection_new"),
    
    path('tkc_wo_select_testing_nabl/<str:offer>', views.tkc_wo_select_testing_nabl, name='tkc_wo_select_testing_nabl'),
    path('tkc_wo_select_testing_nabl_new/<int:tkc_di_id>/<str:offer>', views.tkc_wo_select_testing_nabl_new, name='tkc_wo_select_testing_nabl_new'),
    
    path('tkc_wo_trf_create', views.tkc_wo_trf_create, name="tkc_wo_trf_create"),
    path('tkc_wo_trf_create_new', views.tkc_wo_trf_create_new, name="tkc_wo_trf_create_new"),

    path('tkc_wo_nabl_gatepass_new/<str:offer>', views.tkc_wo_nabl_gatepass_new, name='tkc_wo_nabl_gatepass_new'),
    path('tkc_wo_nabl_gatepass_new_new/<int:nabl_user_id>/<int:tkc_di_id>/<str:offer_no>', views.tkc_wo_nabl_gatepass_new_new, name='tkc_wo_nabl_gatepass_new_new'),

   path('tkc_site_store_view_samled_material/<str:offer>', views.tkc_site_store_view_samled_material, name='tkc_site_store_view_samled_material'),
   path('tkc_site_store_view_samled_material_new/<int:tkc_di_id>/<str:offer>', views.tkc_site_store_view_samled_material_new, name='tkc_site_store_view_samled_material_new'),


    path('tkc_wo_sampled_item/<str:offer>', views.tkc_wo_sampled_item, name='tkc_wo_sampled_item'),
    path('tkc_wo_sampled_item_new/<int:nabl_user_id>/<int:tkc_di_id>/<str:offer>', views.tkc_wo_sampled_item_new, name='tkc_wo_sampled_item_new'),

    path('show_sitestore_gatepass/<int:tkc_di_id>/<str:offer_no>', views.show_sitestore_gatepass, name="show_sitestore_gatepass"),
    path('tkc_wo_test_request_form_submit/<str:offer>', views.tkc_wo_test_request_form_submit, name='tkc_wo_test_request_form_submit'),
    # path('gatepass/<int:nabl_user_id>/<int:tkc_di_id>/<int:offer_1id>/<int:gate_pass_id>/', views.GatepassLetterTKCView, name='GatepassLetterTKCView'),
    path('tkc_site_store_gatepass_letter_print', views.tkc_site_store_gatepass_letter_print, name='tkc_site_store_gatepass_letter_print'),



]
