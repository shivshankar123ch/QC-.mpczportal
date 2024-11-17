from django.contrib import admin
from django.urls import path
from nabl import views

urlpatterns = [
    path('nabl_base', views.nabl_base, name='nabl_base'),
    path('testNabl', views.testNabl, name='testNabl'),

    path('nabl_reg7', views.nabl_reg7, name='nabl_reg7'),
    path('nabl_reg8', views.nabl_reg8, name='nabl_reg8'),
    path('nabl_reg9', views.nabl_reg9, name='nabl_reg9'),
    path('add_material', views.add_material, name='add_material'),

    path('nabl_reg10', views.nabl_reg10, name='nabl_reg10'),
    path('nabl_reg11', views.nabl_reg11, name='nabl_reg11'),
    path('nabl_reg12', views.nabl_reg12, name='nabl_reg12'),
    path('nabl_reg13', views.nabl_reg13, name='nabl_reg13'),
    path('nabl_reg14', views.nabl_reg14, name='nabl_reg14'),
    path('nabl_reg15', views.nabl_reg15, name='nabl_reg15'),
    path('nabl_reg16', views.nabl_reg16, name='nabl_reg16'),
    path('basic', views.basic, name='basic'),
    path('rejected_doc', views.rejected_doc, name='rejected_doc'),
    path('rejected_doc_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),
    path('rejected_doc_cgm_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),
    path('specification/<int:id>', views.specification, name='specification'),
    path('test1/<int:id>', views.test, name='test'),
    path('product', views.product, name='product'),
    path('nabl_profile',views.nabl_profile,name='nabl_profile'),
    path('Test2', views.Test2, name='Test2'),
    path('AddProduct', views.AddProduct, name='AddProduct'),
    path('userlist', views.userlist, name='userlist'),
    path('UpdateNablProfile',views.Nabl_Profile,name='Nabl_Profile'),
    path('vendor_otp_verify', views.vendor_otp_verify, name='vendor_otp_verify'),
    path('profile_status', views.profile_status, name="profile_status"),
    
    path('nabl_trf', views.nabl_trf, name="nabl_trf"),
    path('nabl_trf_view/<int:user_id>', views.nabl_trf_view, name="nabl_trf_view"),
    path('nabl_sample_recv/<int:user_id>/<int:TRF_Id>', views.nabl_sample_recv, name="nabl_sample_recv"),
    path('nabl_sample_recv2/<str:material_serial_number>/<int:ro_id>/<int:gp_id>', views.nabl_sample_recv2, name="nabl_sample_recv2"),
    path('nabl_sample_reject/<str:xmr_number>/<int:ro_id>/<int:gp_id>', views.nabl_sample_reject, name="nabl_sample_reject"),
    path('nabl_sample_reject2/<str:xmr_number>', views.nabl_sample_reject, name="nabl_sample_reject"),
    path('nabl_out_physical', views.nabl_out_physical, name='nabl_out_physical'),
    path('nabl_out_physical_view', views.nabl_out_physical_view, name='nabl_out_physical_view'),
    path('nabl_out_physical_view_gatepass/<int:GatepassOutward_id>', views.nabl_out_physical_view_gatepass, name='nabl_out_physical_view_gatepass'),

    path('nabl_sample_recv/<int:gatepass_id>', views.nabl_sample_recv, name="nabl_sample_recv"),
    # path('Gatepass_save_nabl/<int:ro_id>/<int:gp_id>', views.Gatepass_save_nabl, name="Gatepass_save_nabl"),
    path('Gatepass_save_nabl', views.Gatepass_save_nabl, name="Gatepass_save_nabl"),
    path('uplaod_Outwardgatepass/<str:gatepass_id>', views.uplaod_Outwardgatepass, name="uplaod_Outwardgatepass"),

    path('fqp_material_report', views.fqp_material_report, name="fqp_material_report"),

    path('Offer_Item_Code/<int:id>', views.Offer_Item_Code, name="Offer_Item_Code"),
    ##############################  PO Sampling Anil######################################################
    
    path('cp_nabl_trf', views.cp_nabl_trf, name="cp_nabl_trf"),
    path('cp_nabl_trf_view/<int:id>', views.cp_nabl_trf_view, name="cp_nabl_trf_view"),
    path('cp_nabl_trf_view2/<int:gp_id>/<int:trf_id>/<str:mat_sr>', views.cp_nabl_trf_view2, name="cp_nabl_trf_view2"),
    path('cp_nabl_sample_reject/<int:gp_id>/<int:trf_id>/<str:mat_sr>', views.cp_nabl_sample_reject, name="cp_nabl_sample_reject"),
    path('cp_nabl_out_physical', views.cp_nabl_out_physical, name="cp_nabl_out_physical"),
    path('cp_Gatepass_save_nabl/<int:trf_id>/<int:gp_id>', views.cp_Gatepass_save_nabl, name="cp_Gatepass_save_nabl"),
    path('cp_uplaod_Outwardgatepass/<int:gatepass_id>', views.cp_uplaod_Outwardgatepass, name="cp_uplaod_Outwardgatepass"),
    path('cp_nabl_out_physical_view', views.cp_nabl_out_physical_view, name="cp_nabl_out_physical_view"),
    
    path('cp_nabl_result_sampling/<int:id>', views.cp_nabl_result_sampling, name="cp_nabl_result_sampling"),
    
    path('cp_nabl_result_resampling/<int:id>', views.cp_nabl_result_resampling, name="cp_nabl_result_resampling"),
    
    path('cp_nabl_trf_view_resampling/<int:id>', views.cp_nabl_trf_view_resampling, name="cp_nabl_trf_view_resampling"),
    
    path('cp_nabl_trf_view2_resampling/<int:gp_id>/<int:trf_id>/<str:mat_sr>', views.cp_nabl_trf_view2_resampling, name="cp_nabl_trf_view2_resampling"),
    
    path('cp_nabl_sample_reject_resampling/<int:gp_id>/<int:trf_id>/<str:mat_sr>', views.cp_nabl_sample_reject_resampling, name="cp_nabl_sample_reject_resampling"),


#----------------pd mishra code start form here -------------------
    path('tkc_nabl_sampling_wo', views.tkc_nabl_sampling_wo, name="tkc_nabl_sampling_wo"),
    path('nabl_sampling_offerlist/<int:wo_id>', views.nabl_sampling_offerlist, name="nabl_sampling_offerlist"),
    path('nabl_sampling_details/<str:offer_no>/<int:tkc_di_id>/<str:item_code>', views.nabl_sampling_details, name="nabl_sampling_details"),
    path('nabl_sampling_receiving/<int:id>', views.nabl_sampling_receiving, name="nabl_sampling_receiving"),
    path('nabl_accept/<int:id>', views.nabl_accept, name="nabl_accept"),
    path('show_site_store_gate_pass/<str:offer_no>/<int:tkc_di_id>', views.show_site_store_gate_pass, name="show_site_store_gate_pass"),
    path('show_tkc_trf/<str:offer_no>/<int:tkc_di_id>', views.show_tkc_trf, name="show_tkc_trf"),
    path('tkc_nabl_item_details/<str:offer_no>/<int:tkc_di_id>', views.tkc_nabl_item_details, name="tkc_nabl_item_details"),
    path('tkc_nabl_gate_pass/<int:gate_pass_id>/<str:offer_no>', views.tkc_nabl_gate_pass, name="tkc_nabl_gate_pass"),
    path('tkc_nabl_gatepass_letter/<int:gate_pass_id>/<int:nabl_gatepass_id>', views.tkc_nabl_gatepass_letter, name="tkc_nabl_gatepass_letter"),
    path('gatepass/<nabl_gatepass_data>/<int:gate_pass_id>/', views.GatepassLetterView, name='GatepassLetterView'),


    
]
