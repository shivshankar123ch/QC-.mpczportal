from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('type', views.user_type, name='type'),
    path('type_of_user', views.type_of_user, name='type_of_user'),
    path('otp_verify', views.otp_verify, name='otp_verify'),
    path('reg', views.reg, name='reg'),
    path('thanks', views.thanks, name='thanks'),
    path('test', views.test, name='test'),
    path('user_data_show', views.user_data_show, name='user_data_show'),
    path('reg_first', views.reg_first, name='reg_first'),
    path('reg_second', views.reg_second, name='reg_second'),
    path('reg_third', views.reg_third, name='reg_third'),
    path('reg_fourth', views.reg_fourth, name='reg_fourth'),
    path('reg_fifth', views.reg_fifth, name='reg_fifth'),
    path('reg_sixth', views.reg_sixth, name='reg_sixth'),
    path('finance_login', views.Finance_login, name='finance'),
    path('wokring_login', views.wokring_login, name="wokring_login"),
    path('user_finance_base', views.user_finance_base, name="user_finance_base"),
    path('mpeb_login', views.mpeb_login, name="mpeb_login"),
    path('mpeb_base', views.mpeb_base, name="mpeb_base"),
    path('works_base', views.works_base, name="works_base"),
    path('finance_base', views.finance_base, name="finance_base"),
    path('cgm_base', views.cgm_base, name="cgm_base"),
    path('work_pending_vendor', views.work_pending_vendor, name="work_pending_vendor"),
    path('vendor_wnp_evaluate/<int:id>', views.vendor_wnp_evaluate, name="vendor_wnp_evaluate"),
    path('vendor_wnp_evaluate_save/<int:id>', views.vendor_wnp_evaluate_save, name="vendor_wnp_evaluate_save"),
    path('cgm_pending_vendor', views.cgm_pending_vendor, name="cgm_pending_vendor"),
    path('cgm_complete_vendor', views.cgm_complete_vendor, name="cgm_complete_vendor"),
    path('vendor_cgm_evaluate/<int:id>', views.vendor_cgm_evaluate, name="vendor_cgm_evaluate"),
    path('vendor_cgm_evaluate_save/<int:id>', views.vendor_cgm_evaluate_save, name="vendor_cgm_evaluate_save"),
    path('tkc_cgm_evaluate/<int:id>', views.tkc_cgm_evaluate, name="tkc_cgm_evaluate"),
    path('tkc_cgm_evaluate_save/<int:id>', views.tkc_cgm_evaluate_save, name="tkc_cgm_evaluate_save"),
    path('vendor_cgm_evaluate_save1/<int:id>', views.vendor_cgm_evaluate_save1, name="vendor_cgm_evaluate_save1"),
    path('mpeb_verify_otp', views.mpeb_verify_otp, name="mpeb_verify_otp"),
    # Dgm work
    path('dgm_work_pending', views.dgm_work_pending, name="dgm_work_pending"),
    path('vendor_dgm_work_pending', views.vendor_dgm_work_pending, name="vendor_dgm_work_pending"),
    path('vendor_dgm_work_complete', views.vendor_dgm_work_complete, name="vendor_dgm_work_complete"),
    path('vendor_dgm_work_pending_resubmit', views.vendor_dgm_work_pending_resubmit, name="vendor_dgm_work_pending_resubmit"),
    path('tkc_dgm_work_complete', views.tkc_dgm_work_complete, name="tkc_dgm_work_complete"),
    path('tkc_dgm_work_pending_resubmit', views.tkc_dgm_work_pending_resubmit, name="tkc_dgm_work_pending_resubmit"),
    path('dgm_work_evaluate/<int:id>', views.dgm_work_evaluate, name="dgm_work_evaluate"),

    path('resubmit_view/<int:id>', views.resubmit_view, name="resubmit_view"),
    path('dgm_work_evaluate_save/<int:id>', views.dgm_work_evaluate_save, name="dgm_work_evaluate_save"),
    path('factory_inspection_initiate', views.factory_inspection_initiate, name="factory_inspection_initiate"),
    path('factory_initiate', views.factory_initiate, name="factory_initiate"),
    path('factory_inspection_initiate/<int:id>', views.factory_inspection_initiate, name="factory_inspection_initiate"),
    path('factory_assigned', views.factory_assigned, name='factory_assigned'),
    #url for reassign and mentain history of inspectinng ofiicer for factory inspection by PD MISHRA
    path('update_FI/<int:id>', views.update_FI, name='update_FI'),
    path('Update_factory_inspection_initiate/<int:id>', views.Update_factory_inspection_initiate, name='Update_factory_inspection_initiate'),
    path('reassign_history/<int:id>', views.reassign_history, name='reassign_history'),



    # Dgm Finance
    
    path('dgm_finance_pending', views.dgm_finance_pending, name="dgm_finance_pending"),
    path('vendor_dgm_finance_pending', views.vendor_dgm_finance_pending, name="vendor_dgm_finance_pending"),
    path('vendor_dgm_finance_total_approved', views.vendor_dgm_finance_total_approved, name="vendor_dgm_finance_total_approved"),
    path('dgm_finance_complete_tkc', views.dgm_finance_complete_tkc, name="dgm_finance_complete_tkc"),
    path('vendor_dgm_finance_pending_rejection_tkc', views.vendor_dgm_finance_pending_rejection_tkc, name="vendor_dgm_finance_pending_rejection_tkc"),
    path('vendor_dgm_finance_pending_rejection_vendor', views.vendor_dgm_finance_pending_rejection_vendor, name="vendor_dgm_finance_pending_rejection_vendor"),
    path('dgm_finance_all_tkc', views.dgm_finance_all_tkc, name="vendor_dgm_finance_pending_rejection_vendor"),

    
    
    path('vendor_dgm_finance_pending_rejection', views.vendor_dgm_finance_pending_rejection, name="vendor_dgm_finance_pending_rejection"),
    path('vendor_dgm_finance_complate', views.vendor_dgm_finance_complate, name="vendor_dgm_finance_complate"),
    path('vendor_dgm_finance_all', views.vendor_dgm_finance_all, name="vendor_dgm_finance_all"),

    path('dgm_finance_evaluate/<int:id>', views.dgm_finance_evaluate, name="dgm_finance_evaluate"),
    path('dgm_finance_view/<int:id>', views.dgm_finance_view, name="dgm_finance_view"),
    # path('vendor_dgm_finance_all', views.vendor_dgm_finance_all, name="vendor_dgm_finance_all"),

    path('resubmit_finance_evaluate/<int:id>', views.resubmit_finance_evaluate, name="resubmit_finance_evaluate"),
    path('dgm_finance_evaluate_save/<int:id>', views.dgm_finance_evaluate_save, name="dgm_finance_evaluate_save"),
    # Dgm qc
    #path('dgm_qc_pending', views.dgm_qc_pending, name="dgm_qc_pending"),
    path('vendor_dgm_qc_pending', views.vendor_dgm_qc_pending, name="vendor_dgm_qc_pending"),
    path('dgm_qc_evaluate/<int:id>', views.dgm_qc_evaluate, name="dgm_qc_evaluate"),


    #path('dgm_qc_evaluate_save/<int:id>', views.dgm_qc_evaluate_save, name="dgm_qc_evaluate_save"),

    path('index', views.index, name="index"),
    path('index_login', views.index_login, name="index_login"),

    path('test1', views.test1, name="test1"),
    path('success_reg', views.success_reg, name='success_reg'),
    path('mail_sent',views.msgsent),
    path('forgot_password',views.PasswordForgetView.as_view(),name="passwordforget1"),
    path("password-reset/<email>/<token>/",views.PasswordResetView.as_view(), name="passwordreset"),
    # path('', home, name='home'),


    # path('payu_demo',views.payu_demo,name="payu_demo"),
    # path(mt-md-n8 mt-n8 
    
    path('cgm_pending_tkc', views.cgm_pending_tkc, name='cgm_pending_tkc'),
    path('cgm_complete_tkc', views.cgm_complete_tkc, name='cgm_complete_tkc'),
    path('inactive_tkc', views.Inactive_tkc, name='Inactive_tkc'),
    path('active_tkc', views.Active_tkc, name='Active_tkc'),
    path('cgm_rejected_tkc', views.cgm_rejected_tkc, name='cgm_rejected_tkc'),
    path('vendor_cgm_evaluate_view/<int:id>', views.vendor_cgm_evaluate_view, name="vendor_cgm_evaluate_view"),
    path('tkc_total', views.tkc_total, name='tkc_total'),
    path('search_contractor/', views.search_contractor, name='search_contractor'),
    path('nabl_dgm_qc_pending',views.nabl_dgm_qc_pending,name='nabl_dgm_qc_pending'),
    path('nabl_dgm_qc_evaluate/<int:id>', views.nabl_dgm_qc_evaluate, name="nabl_dgm_qc_evaluate"),
    path('nabl_dgm_qc_evaluate_save/<int:id>', views.nabl_dgm_qc_evaluate_save, name="nabl_dgm_qc_evaluate_save"),
    path("cgm_pending_nabl",views.cgm_pending_nabl,name="cgm_pending_nabl"),
    path('nabl_cgm_evaluate/<int:id>', views.nabl_cgm_evaluate, name="nabl_cgm_evaluate"),
    path('nabl_cgm_evaluate_save/<int:id>', views.nabl_cgm_evaluate_save, name="nabl_cgm_evaluate_save"),
    path('cgm_approved_nabl',views.cgm_approved_nabl,name='cgm_approved_nabl'),
    # path('vendor_cgm_evaluate',views.vendor_cgm_evaluate,name='vendor_cgm_evaluate'),
    path('vendor_cgm_evaluate2/<int:id>', views.vendor_cgm_evaluate2, name="vendor_cgm_evaluate2"),
    # path(mt-md-n8 mt-n8 'success',views.success_payu,name='success_payu'),


    ########

    # path('payu_demo',views.payu_demo,name="payu_demo"),
    # path('payu/success',views.payu_success,name='payu_success'),
    # path(mt-md-n8 mt-n8 p_view/<int:trf_id>', views.gp_view, name='gp_view'),
    path('new2/<int:trf_id>', views.employees_list2, name='employees-list2'),
    path('create2/<int:trf_id>', views.create_employee2, name='create-employee2'),
    path('two2/<int:trf_id>', views.two2, name='two2'),

    path('tmqm_sample_reject/<int:trf_id>', views.tmqm_sample_reject, name='tmqm_sample_reject'),

    path('tmqm_sample_recv', views.tmqm_sample_recv, name='tmqm_sample_recv'),

    path('tmqm_sample_recv2/<int:trf_id>', views.tmqm_sample_recv2, name='tmqm_sample_recv2'),
    path('tmqm_job_order', views.tmqm_job_order, name='tmqm_job_order'),
    path('tmqm_job_order2/<int:trf_id>', views.tmqm_job_order2, name='tmqm_job_order2'),
    path('tmqm_job_order3/<int:trf_id>', views.tmqm_job_order3, name='tmqm_job_order3'),
    path('ta_base', views.ta_base, name='ta_base'),
    path('ta_joborder', views.ta_joborder, name='ta_joborder'),
    


    path('nabl_dgm_qc_total', views.nabl_dgm_qc_total, name="nabl_dgm_qc_total"),
    path('tkc_dgm_work_total', views.tkc_dgm_work_total, name="tkc_dgm_work_total"),
    path('vendor_dgm_work_total', views.vendor_dgm_work_total, name="vendor_dgm_work_total"),
    path('vendor_dgm_finance_total', views.vendor_dgm_finance_total, name="vendor_dgm_finance_total"),
    path('cgm_total_vendor', views.cgm_total_vendor,name='cgm_total_vendor'),

    path('cgm_total_nabl', views.cgm_total_nabl,name='cgm_total_nabl'),
    path('nabl_cgm_evaluate_test/<int:id>', views.nabl_cgm_evaluate_test, name="nabl_cgm_evaluate_test"),


    path('', views.user, name='user'),
######lok####
    path('payment/request',views.payu_demo_registration,name="payu_demo_registration"),
    path('payment/success',views.payu_success_registration,name='payu_success_registration'),
    path('payment/failure',views.payu_failure,name='payu_failure'),
    path('gen_invoice_registration', views.gen_invoice_registration, name='gen_invoice_registration'),

    path('nabl_dgm_work_pending_resubmit', views.nabl_dgm_work_pending_resubmit, name='nabl_dgm_work_pending_resubmit'),

    path('nabl_dgm_qc_approve', views.nabl_dgm_qc_approve, name="nabl_dgm_qc_approves"),

    path('officer_otp/<int:id>/<int:otp>', views.officer_otp, name="officer_otp"),
    path('gp_inward', views.gp_inward, name='gp_inward'),
    path('gp_inward_rca', views.gp_inward_rca, name='gp_inward_rca'),
    path('create2_rca/<int:trf_id>', views.create_employee2_rca, name='create-employee2_rca'),
    path('new2_rca/<int:trf_id>', views.employees_list2_rca, name='employees-list2_rca'),
    path('two2_rca/<int:trf_id>', views.two2_rca, name='two2_rca'),
    path('gp_view/<int:trf_id>', views.gp_view, name='gp_view'),
    path('gp_view_rca/<int:trf_id>', views.gp_view_rca, name='gp_view_rca'),
    path('gp_outward_rca/<int:trf_id>', views.gp_outward_rca, name='gp_outward_rca'),
    path('gp_outward_view_rca/<int:trf_id>', views.gp_outward_view_rca, name='gp_outward_view_rca'),
    path('tmqm_sample_reject_rca/<int:trf_id>', views.tmqm_sample_reject_rca, name='tmqm_sample_reject_rca'),
    path('tmqm_sample_recv_rca', views.tmqm_sample_recv_rca, name='tmqm_sample_recv_rca'),
    path('tmqm_sample_recv2_rca/<int:trf_id>', views.tmqm_sample_recv2_rca, name='tmqm_sample_recv2_rca'),
    path('tmqm_job_order_rca', views.tmqm_job_order_rca, name='tmqm_job_order_rca'),
    path('tmqm_job_order2_rca/<int:trf_id>', views.tmqm_job_order2_rca, name='tmqm_job_order2_rca'),
    path('tmqm_job_order3_rca/<int:trf_id>', views.tmqm_job_order3_rca, name='tmqm_job_order3_rca'),
    path('ta_uploadReport/<int:trf_id>', views.ta_uploadReport, name='ta_uploadReport'),
    # path('Report_success_rca', views.Report_success_rca, name='Report_success_rca'),
    path('Report_success', views.Report_success, name='Report_success'),
    # path('Report_success_view_rca/<str:sc>', views.Report_success_view_rca, name='Report_success_view_rca'),
    path('Report_success_view/<str:sc>', views.Report_success_view, name='Report_success_view'),

    path('gp_outward_base', views.gp_outward_base, name='gp_outward_base'),

    path('gp_outward/<int:trf_id>', views.gp_outward, name='gp_outward'),

    path('gp_outward_view/<int:trf_id>', views.gp_outward_view, name='gp_outward_view'),

    path('nabl_dgm_nabl_evaluate/<int:id>',views.nabl_dgm_nabl_evaluate, name="nabl_dgm_nabl_evaluate"),



#----------poornima
    path('dgm_work_evaluate2/<int:id>', views.dgm_work_evaluate2, name="dgm_work_evaluate2"),
    path('nabl_dgm_qc_evaluate_pending/<int:id>', views.nabl_dgm_qc_evaluate_pending, name="nabl_dgm_qc_evaluate_pending"),
    path('resubmit_cgm/<int:id>', views.resubmit_cgm, name="resubmit_cgm"),



#----- Upload data
    path('upload_basic_details',views.upload_basic_details, name="upload_basic_details"),
    path('cert_all/<str:reg_id>',views.cert_all, name="cert_all"),
    
	path('uplaod_cert/<str:no>',views.uplaod_cert, name="uplaod_cert"),
    path('certificate_submit/<str:User_type>',views.certificate_submit, name="certificate_submit"),
    path('digital_sign_cert/<str:user_type>',views.digital_sign_cert, name="digital_sign_cert"),
    path('cert_upload_download/<int:id>',views.cert_upload_download, name="cert_upload_download"),
    path('show_cert/<str:Authentication_id>',views.show_cert, name="show_cert"),
    path('show_digital_sign_cert_cgm/<str:User_type>',views.show_digital_sign_cert_cgm, name="show_digital_sign_cert_cgm"),


    path('payment', views.payment, name="payment"),
    path('exam_data', views.Exam, name="Exam"),

    path('databaseDB', views.databaseDB, name="databaseDB"),
    path('databaseView', views.databaseView, name="databaseView"),
    path('databaseView2/<str:User_Id>', views.databaseView2, name="databaseView2"),
    
    #Jeevan ERP Integration Code
    path('ErpPushViewId', views.ErpPushViewId, name="ErpPushViewId"),
    # path('ErpPush/<int:id>', views.ErpPush, name="ErpPush"),
    path('ErpPush/<int:id>/<str:discom_name>', views.ErpPush, name="ErpPush"),
	path('roof_top_discom', views.roof_top_discom, name="roof_top_discom"),

    path('roof_top_upload_discom', views.roof_top_upload_discom, name="roof_top_upload_discom"),
    path('roof_top_filling_pending_list', views.roof_top_filling_pending_list, name="roof_top_filling_pending_list"),

    

    path('roof_toop_officer_dashboard', views.roof_toop_officer_dashboard, name="roof_toop_officer_dashboard"),

    path('roof_toop_officer_pending', views.roof_toop_officer_pending, name="roof_toop_officer_pending"),


    path('roof_toop_officer_evaluate/<int:id>', views.roof_toop_officer_evaluate, name="roof_toop_officer_evaluate"),

    path('roof_toop_officer_evaluate_save/<int:id>', views.roof_toop_officer_evaluate_save, name="roof_toop_officer_evaluate_save"),


    path('roof_toop_officer_complete_list', views.roof_toop_officer_complete_list, name="roof_toop_officer_complete_list"),

    path('roof_toop_officer_complete_view/<int:id>', views.roof_toop_officer_complete_view, name="roof_toop_officer_complete_view"),
    

    path('roof_toop_approver_officer_pending', views.roof_toop_approver_officer_pending, name="roof_toop_approver_officer_pending"),

    path('roof_toop_approver_officer_evaluate/<int:id>', views.roof_toop_approver_officer_evaluate, name="roof_toop_approver_officer_evaluate"),



    path('roof_toop_approver_officer_evaluate_save/<int:id>', views.roof_toop_approver_officer_evaluate_save, name="roof_toop_approver_officer_evaluate_save"),
    
    path('root_top_otp/<int:id>', views.root_top_otp, name="root_top_otp"),

    path('root_top_otp2/<int:id>', views.root_top_otp2, name="root_top_otp2"),

    path('root_top_otp3/<str:registration_no>', views.root_top_otp3, name="root_top_otp3"),

    path('roof_top_cert_show/<str:registration_no>', views.roof_top_cert_show, name="roof_top_cert_show"),



    path('roof_toop_approver_complete_list', views.roof_toop_approver_complete_list, name="roof_toop_approver_complete_list"),

    path('roof_toop_approver_complete_view/<int:id>', views.roof_toop_approver_complete_view, name="roof_toop_approver_complete_view"),
    
    path('transaction_history_solar_viewer', views.transaction_history_solar_viewer, name='transaction_history_solar_viewer'),
    path('transaction_history_solar_Approver', views.transaction_history_solar_Approver, name='transaction_history_solar_Approver'),

    path('all_tkc_field_officer', views.all_tkc_field_officer, name="all_tkc_field_officer"),
    path('all_tkc_field_officer_document/<int:id>', views.all_tkc_field_officer_document, name="all_tkc_field_officer_document"),


    path('all_vendor_field_officer', views.all_vendor_field_officer, name="all_vendor_field_officer"),
    path('all_vendor_field_officer_document/<int:id>', views.all_vendor_field_officer_document, name="all_vendor_field_officer_document"),

    path('all_nabl_field_officer', views.all_nabl_field_officer, name="all_nabl_field_officer"),    
    path('all_nabl_field_officer_document/<int:id>', views.all_nabl_field_officer_document, name="all_nabl_field_officer_document"),

    path('demo_test', views.demo_test, name="demo_test"),
    
    path('discom', views.discom, name="discom"),
    path('discom_reg1', views.discom_reg1, name="discom_reg1"),
    path('roof_top_discom', views.roof_top_discom, name="roof_top_discom"),
    path('roof_top_upload_discom', views.roof_top_upload_discom, name="roof_top_upload_discom"),
    path('roof_top_filling_pending_list', views.roof_top_filling_pending_list, name="roof_top_filling_pending_list"),
    path('roof_top_filling_pending_form/<int:id>', views.roof_top_filling_pending_form, name="roof_top_filling_pending_form"),
    path('discom_approved_vendor', views.discom_approved_vendor, name='discom_approved_vendor'),
    path('all_pending_loa_for_approvel_evaluate/<int:id>', views.all_pending_loa_for_approvel_evaluate, name="all_pending_loa_for_approvel_evaluate"),

    path('all_pending_loa_for_approvel_evaluate_save/<int:id>', views.all_pending_loa_for_approvel_evaluate_save, name="all_pending_loa_for_approvel_evaluate_save"),

    
    path('roof_toop_officer_loa', views.roof_toop_officer_loa, name="roof_toop_officer_loa"),
    path('uploaded_loa', views.uploaded_loa, name="uploaded_loa"),


    path('all_loa_viewer_view', views.all_loa_viewer_view, name="all_loa_viewer_view"),
    path('all_pending_loa_for_approvel', views.all_pending_loa_for_approvel, name="all_pending_loa_for_approvel"),

    path('all_approved_loa_approvel_officer', views.all_approved_loa_approvel_officer, name="all_approved_loa_approvel_officer"),
    path('loa_resubmit/<int:id>',views.loa_resubmit,name="loa_resubmit"),
    path('non_loa_vendors',views.non_loa_vendors,name="non_loa_vendors"),
    path('solar_vendor_bg/<int:id>',views.solar_vendor_bg,name="solar_vendor_bg"),

    path('bg_expiry_status',views.bg_expiry_status,name="bg_expiry_status"),
    path('bg_expiry_status_approver',views.bg_expiry_status_approver,name="bg_expiry_status_approver"),
    path('tkc_cert_gen', views.tkc_cert_gen, name="tkc_cert_gen"),
    path('tkc_cert_gen2', views.tkc_cert_gen2, name="tkc_cert_gen2"),
    path('tkc_cert_gen3/<int:User_Id>', views.tkc_cert_gen3, name="tkc_cert_gen3"),
    path('discom_approved_vendor', views.discom_approved_vendor, name='discom_approved_vendor'),

    path('all_vendor_dicome_document/<int:id>', views.all_vendor_dicome_document, name="all_vendor_dicome_document"),
    
    #***********************rohit rca***************************
    path('rca_pending_cgm',views.rca_pending_cgm,name="rca_pending_cgm"),
    
    path('rca_pending_cgm_regular',views.rca_pending_cgm_regular,name="rca_pending_cgm_regular"),
    path('rca_cgm_evaluate/<int:id>',views.rca_cgm_evaluate,name="rca_cgm_evaluate"),
    path('rca_cgm_evaluate_save/<int:id>',views.rca_cgm_evaluate_save,name="rca_cgm_evaluate_save"),
    path('rca_certificate/<int:id>/<int:otp>',views.rca_certificate,name="rca_certificate"),

    path('factory_initiate_rca', views.factory_initiate_rca, name="factory_initiate_rca"),
    path('factory_inspection_initiate_rca/<int:id>', views.factory_inspection_initiate_rca, name="factory_inspection_initiate_rca"),
    path('factory_assigned_rca', views.factory_assigned_rca, name='factory_assigned_rca'),
    path('cgm_complete_vendor_rca', views.cgm_complete_vendor_rca, name="cgm_complete_vendor_rca"),

    path('cgm_complete_vendor_rca_regular', views.cgm_complete_vendor_rca_regular, name="cgm_complete_vendor_rca_regular"),

    path('rca_cgm_evaluate_regular/<int:id>',views.rca_cgm_evaluate_regular,name="rca_cgm_evaluate_regular"),


    path('rca_cgm_evaluate_save/<int:id>',views.rca_cgm_evaluate_save,name="rca_cgm_evaluate_save"),

    path('rca_certificate_regular/<int:id>/<int:otp>',views.rca_certificate_regular,name="rca_certificate_regular"),

    path('rca_regular_cgm_evaluate_save/<int:id>',views.rca_regular_cgm_evaluate_save,name="rca_regular_cgm_evaluate_save"),
    path('digital_sign_cert_rca/<str:user_type>/<str:User_Zone>',views.digital_sign_cert_rca, name="digital_sign_cert_rca"),
    path('cert_upload_download_rca/<int:id>',views.cert_upload_download_rca,name="cert_upload_download_rca"),
    path('uplaod_cert_rca/<str:no>',views.uplaod_cert_rca, name="uplaod_cert_rca"),
    path('certificate_submit_rca/<str:User_type>',views.certificate_submit_rca, name="certificate_submit_rca"),
    path('factory_assigned_rca_view/<int:id>',views.factory_assigned_rca_view,name="factory_assigned_rca_view"),
    path('all_rca_vendor_approved_list', views.all_rca_vendor_approved_list, name="all_rca_vendor_approved_list"),

    path('all_vendor_approved_list', views.all_vendor_approved_list, name="all_vendor_approved_list"),

    path('all_vendor_approved_list_documents/<int:id>',views.all_vendor_approved_list_documents,name="all_vendor_approved_list_documents"),
    path('Add_Factory_Officer', views.Add_Factory_Officer, name="Add_Factory_Officer"),
    path('Anubhand_Entry', views.Anubhand_Entry, name='Anubhand_Entry'),
    path('new_status', views.new_status, name="new_status"),
    path('export_users_csv', views.export_users_csv, name="export_users_csv"),
    path('gm_search_by_id', views.gm_search_by_id, name="gm_search_by_id"),
    path('dgm_complete_tkc', views.dgm_complete_tkc, name="dgm_complete_tkc"),

    path('factory_payment_details', views.factory_payment_details, name="factory_payment_details"),
    path('all_factory_payment_details_save/<int:id>',views.all_factory_payment_details_save,name="all_factory_payment_details_save"),

    path('all_factory_payment_material/<int:id>',views.all_factory_payment_material,name="all_factory_payment_material"),
    path('new_material_vendor_dgm', views.new_material_vendor_dgm, name="new_material_vendor_dgm"),

    path('new_material_vendor_dgm_evaluate/<int:id>',views.new_material_vendor_dgm_evaluate,name="new_material_vendor_dgm_evaluate"),

    path('new_material_vendor_cgm', views.new_material_vendor_cgm, name="new_material_vendor_cgm"),

    path('new_material_vendor_cgm_evaluate/<int:id>',views.new_material_vendor_cgm_evaluate,name="new_material_vendor_cgm_evaluate"),
    path('cgm_pending_vendor_new', views.cgm_pending_vendor_new, name="cgm_pending_vendor_new"),
    path('vendor_cgm_evaluate_new/<int:id>',views.vendor_cgm_evaluate_new,name="vendor_cgm_evaluate_new"),
    path('RCA_ErpPushViewId', views.RCA_ErpPushViewId, name="RCA_ErpPushViewId"),
    path('RCA_ErpPush/<int:id>', views.RCA_ErpPush, name="RCA_ErpPush"),
    path('dgm_finance_complete_status', views.dgm_finance_complete_status, name="dgm_finance_complete_status"),

    path('cgm_all_complete_status', views.cgm_qc_complete_status, name="cgm_all_complete_status"),
    path('contractor_status_check', views.contractor_status_check, name="contractor_status_check"),
    path('authZoneUpdate', views.authZoneUpdate, name="authZoneUpdate"),
    path('rca_cgm_view_complete_vendor/<int:id>', views.rca_cgm_view_complete_vendor, name="rca_cgm_view_complete_vendor"),
    path('contractor_deregistered_cgm', views.contractor_deregistered_cgm, name="contractor_deregistered_cgm"),
    path('deregister_tkc_dgm_work', views.deregister_tkc_dgm_work, name="deregister_tkc_dgm_work"),
    path('deregister_tkc_dgm_finance', views.deregister_tkc_dgm_finance, name="deregister_tkc_dgm_finance"),
    path('pending_contractor_filed_officer', views.pending_contractor_filed_officer, name="pending_contractor_filed_officer"),
    
    path('vendor_factory_status_view_dgm_work', views.vendor_factory_status_view_dgm_work, name="vendor_factory_status_view_dgm_work"),
    
    path('contractor_certificate_dgm_work_view', views.contractor_certificate_dgm_work_view, name="contractor_certificate_dgm_work_view"),
    
    
    
    #urls code for pdi inspection
    # path('pdi_initiate/<int:id>', views.pdi_initiate, name="pdi_initiate"),
    path('all_wo', views.all_wo, name="all_wo"),
    # path('pdi_inspection_initiate/<int:id>', views.pdi_inspection_initiate, name="pdi_inspection_initiate"),
    path('pdi_assigned', views.pdi_assigned, name='pdi_assigned'),
    path('pdi_view/<int:id>', views.pdi_view, name="pdi_view"),
    
    path('vendor_status_check', views.vendor_status_check, name="vendor_status_check"),
    
    path('vendor_check_material/<int:id>', views.vendor_check_material, name="vendor_check_material"),
    
    path('blacklisted', views.blacklisted, name="blacklisted"),
    path('blacklisted_save', views.blacklisted_save, name="blacklisted_save"),
    path('blacklisted_gm', views.blacklisted_gm, name="blacklisted_gm"),
    path('blacklisted_vendor', views.blacklisted_vendor, name="blacklisted_vendor"),
    path('blacklisted_gm_evaluate/<int:id>', views.blacklisted_gm_evaluate, name="blacklisted_gm_evaluate"),
    path('blacklisted_gm_evaluate_save/<int:id>', views.blacklisted_gm_evaluate_save, name="blacklisted_gm_evaluate_save"),
    path('blacklisted_gm_all', views.blacklisted_gm_all, name="blacklisted_gm_all"),
    path('blacklisted_gm_view/<int:id>', views.blacklisted_gm_view, name="blacklisted_gm_view"),
    path('blacklisted_gm_work_all', views.blacklisted_gm_work_all, name="blacklisted_gm_work_all"),
    path('blacklisted_cgm_vendor', views.blacklisted_cgm_vendor, name="blacklisted_cgm_vendor"),
    path('blacklisted_cgm_vendor_evaluate/<int:id>', views.blacklisted_cgm_vendor_evaluate, name="blacklisted_cgm_vendor_evaluate"),
    path('blacklisted_cgm_evaluate_vendor_save/<int:id>', views.blacklisted_cgm_evaluate_vendor_save, name="blacklisted_cgm_evaluate_vendor_save"),
    path('cgm_qc_complete_status_nabl', views.cgm_qc_complete_status_nabl, name="cgm_qc_complete_status_nabl"),
    path('blacklisted_cgm_all', views.blacklisted_cgm_all, name="blacklisted_cgm_all"),
	
    path('sopinfo',views.sopinfo,name="sopinfo"), 
    path('officersop',views.officersop,name="officersop"),
    path('remove_vendor_material/<int:id>', views.remove_vendor_material, name="remove_vendor_material"),
    
    
    path('work_order', views.work_order, name='work_order'),  
    path('get_bank/<int:user_id>', views.get_bank, name='get_bank'),
    path('get_bg/<int:wo_id>', views.get_bg, name='get_bg'),
    path('get_pert/<int:wo_id>', views.get_pert, name='get_pert'),
    path('get_vendor/<int:wo_id>', views.get_vendor, name='get_vendor'),
    path('get_loc/<int:wo_id>', views.get_loc, name='get_loc'),
    path('nabl_status_check',views.nabl_status_check,name="nabl_status_check"),
    path('nabl_check_material/<int:id>', views.nabl_check_material, name="nabl_check_material"),
    path('remove_vendor_material_new/<int:id>', views.remove_vendor_material_new, name="remove_vendor_material_new"),
    path('approved_vendor_list_discom', views.approved_vendor_list_discom, name="approved_vendor_list_discom"),
    path('vendor_material_details_view_discom/<int:id>', views.vendor_check_material_discom, name='vendor_check_material_discom'),
    path('vendor_basic_details_discom/<int:id>', views.vendor_basic_details_discom, name='vendor_basic_details_discom'),
    path('active_inactive_contractor_works', views.active_inactive_contractor_list_dgm_work, name='active_inactive_contractor_list_dgm_work'),
    path('active_inactive_contractor_finance', views.active_inactive_contractor_list_dgm_finance, name='active_inactive_contractor_list_dgm_finance'),
    path('new_dashboard', views.new_dashboard, name='new_dashboard'),
    path('new_dashboard_history/<str:name>', views.new_dashboard_history, name='new_dashboard_history'),	
    path('active_inactive_contractor_list', views.active_inactive_contractor_list_auditor, name='active_inactive_contractor_list_auditor'),
    path('contractor_details_view/<int:id>', views.contractor_view_details_auditor, name='contractor_view_details_auditor'),
	
    path('all_vendor_wo_creater', views.all_vendor_wo_creater, name="all_vendor_wo_creater"),
    path('all_vendor_wo_creater_document/<int:id>',views.all_vendor_wo_creater_document, name="all_vendor_wo_creater_document"),
    path('all_contractor_wo_creater', views.all_contractor_wo_creater, name="all_contractor_wo_creater"),

    path('all_vendor_wo_approver', views.all_vendor_wo_approver, name="all_vendor_wo_approver"),
    path('all_vendor_wo_approver_document/<int:id>',views.all_vendor_wo_approver_document, name="all_vendor_wo_approver_document"),
    path('all_contractor_wo_approver', views.all_contractor_wo_approver, name="all_contractor_wo_approver"),
    path('contractor_document_view_wo_approver/<int:id>',views.contractor_document_view_wo_approver, name="contractor_document_view_wo_approver"),
    path('contractor_document_view_wo_creater/<int:id>',views.contractor_document_view_wo_creater, name="contractor_document_view_wo_creater"),
    path('wo_creater_view_reject_summary', views.wo_creater_view_reject_summary, name="wo_creater_view_reject_summary"),
    path('wo_creater_view_reject_summary_history/<str:name>',views.wo_creater_view_reject_summary_history, name="wo_creater_view_reject_summary_history"),
    path('wo_approver_view_reject_summary', views.wo_approver_view_reject_summary, name="wo_approver_view_reject_summary"),
    path('wo_approver_view_reject_summary_history/<str:name>',views.wo_approver_view_reject_summary_history, name="wo_approver_view_reject_summary_history"),
    path('blacklisted_contractor_view_wo_creater', views.blacklisted_contractor_wo_creater, name="blacklisted_contractor_wo_creater"),
    path('blacklisted_contractor_view_wo_approver', views.blacklisted_contractor_wo_approver, name="blacklisted_contractor_wo_approver"),


    
       
# PDI new code according to offer

    path('pdi_pending_assign', views.pdi_pending_assign, name='pdi_pending_assign'),
    path('view_offer/<str:offer_no>', views.view_offer, name='view_offer'),
    path('new_pdi_assign/<str:offer_no>', views.new_pdi_assign, name='new_pdi_assign'),
    path('pdi_add_data/<str:offer_no>', views.pdi_add_data, name='pdi_add_data'),
    path('all_pdi_assigned/<str:offer_no>', views.all_pdi_assigned, name='all_pdi_assigned'),
    path('pdi_inspection_data/<str:item_code>/<str:offer_no>', views.pdi_inspection_data, name='pdi_inspection_data'),
    path('pdi_against_wo/<str:offer_no>', views.pdi_against_wo, name='pdi_against_wo'),
    # path('pdi_accept/<str:offer_no>/<str:item_code>', views.pdi_accept, name="pdi_accept"),
    # path('pdi_reject/<str:offer_no>/<str:item_code>', views.pdi_reject, name="pdi_reject"),
    path('pdi/<str:offer_no>', views.pdi, name='pdi'),
    path('all_pdi_assigned_data/<str:offer_no>', views.all_pdi_assigned_data, name='all_pdi_assigned_data'),
    path('all_pdi_assigned_data_cgm', views.all_pdi_assigned_data_cgm, name='all_pdi_assigned_data_cgm'),
    path('officer_view_inspection/<str:offer_no>', views.officer_view_inspection, name='officer_view_inspection'),
    path('inspection_data/<str:offer_no>/<str:item_code>', views.inspection_data, name='inspection_data'),
    path('submit_button/<str:offer_no>', views.submit_button, name='submit_button'),
    # path('fake_call/<str:offer_no>/<str:item_code>', views.fake_call, name="fake_call"),
    path('pdi_officers_add/<str:offer_no>', views.pdi_officers_add, name="pdi_officers_add"),
    path('assigned_officer_pdi', views.assigned_officer_pdi, name="assigned_officer_pdi"),
    path('update_pdi_assign/<str:offer_no>',views.update_pdi_assign,name="update_pdi_assign"),
    path('pdi_update_data/<str:offer_no>',views.pdi_update_data,name="pdi_update_data"),
    path('pending_pdi_acceptance',views.pending_pdi_acceptance,name="pending_pdi_acceptance"),
    path('rejected_pdi',views.rejected_pdi,name="rejected_pdi"),
    path('fake_call_pdi',views.fake_call_pdi,name="fake_call_pdi"),
    path('fake_call/<str:offer_no>', views.fake_call, name="fake_call"),
    path('pdi_reject/<str:offer_no>/', views.pdi_reject, name="pdi_reject"),
    path('pdi_accept/<str:offer_no>/', views.pdi_accept, name="pdi_accept"),
    path('wo_view_cgm/<int:id>', views.wo_view_cgm, name='wo_view_cgm'),
    #PDI reject code before PDI assign in CGM QC side
    path('pending_pdi_reject/<str:offer_no>', views.pending_pdi_reject, name="pending_pdi_reject"),
    # code for add remove and update inspecting officer by PDM
    path('inspecting_off_info',views.inspecting_off_info,name="inspecting_off_info"),
    path('add_inspecting_off_info',views.add_inspecting_off_info,name="add_inspecting_off_info"),
    path('update_inspecting_off_info',views.update_inspecting_off_info,name="update_inspecting_off_info"),
    path('del_ins_officer/<int:pk>', views.del_ins_officer, name='del_ins_officer'),
    
    

    

    
# BOQ Urls

    path('pma_verify_boq_list', views.pma_verify_boq_list, name='pma_verify_boq_list'),
    path('pma_verify_boq/<int:wo_id>', views.pma_verify_boq, name='pma_verify_boq'),
    path('pma_save_boq/<int:wo_id>', views.pma_save_boq, name='pma_save_boq'),
    path('pma_reject_boq/<int:wo_id>', views.pma_reject_boq, name='pma_reject_boq'),
    path('pma_accept_boq/<int:wo_id>', views.pma_accept_boq, name='pma_accept_boq'),
    path('gm_save_remarks/<int:wo_id>', views.gm_save_remarks, name='gm_save_remarks'),
	
    path('gm_save_boq/<int:wo_id>', views.gm_save_boq, name='gm_save_boq'),
    path('gm_verify_boq_list', views.gm_verify_boq_list, name="gm_verify_boq_list"),
    path('gm_verify_boq/<int:wo_id>', views.gm_verify_boq, name="gm_verify_boq"),   
    path('gm_reject_boq/<int:wo_id>', views.gm_reject_boq, name="gm_reject_boq"),    
    path('gm_verified_boq_data/<int:wo_id>', views.gm_verified_boq_data, name="gm_verified_boq_data"),
    path('gm_save_new_data/<int:wo_id>', views.gm_save_new_data, name='gm_save_new_data'),

	
    path('tkc_registration', views.tkc_registration, name="tkc_registration"),
    path('tkc_registration_view', views.tkc_registration_view, name="tkc_registration_view"),
    path('tkc_registration_pending', views.tkc_registration_pending_approver, name="tkc_registration_pending_approver"),
    path('tkc_registration_approve/<int:id>', views.tkc_registration_approver_evaluate, name="tkc_registration_approver_evaluate"),  
    path('officer_otp_tkc/<int:id>/<int:otp>', views.officer_otp_tkc, name="officer_otp_tkc"),
    path('uplaod_cert_new_tkc/<str:no>',views.uplaod_cert_new_tkc, name="uplaod_cert_new_tkc"),
    path('digital_sign_cert_new_tkc/<str:user_type>',views.digital_sign_cert_new_tkc, name="digital_sign_cert_new_tkc"),
    path('cert_upload_download_new_tkc/<int:id>',views.cert_upload_download_new_tkc, name="cert_upload_download_new_tkc"),
    path('tkc_registration_view_approver', views.tkc_registration_view_approver, name="tkc_registration_view_approver"),
    path('contractor_approvel_history_gm_works', views.contractor_approvel_history_gm_works, name="contractor_approvel_history_gm_works"),
    path('contractor_approvel_history_gm_works_check/<str:name>',views.contractor_approvel_history_gm_works_check, name="contractor_approvel_history_gm_works_check"),
    path('gm_works_vendor_complete_status', views.gm_works_vendor_complete_status, name="gm_works_vendor_complete_status"),
	
    path('day_wise_count_tkc', views.day_wise_count_tkc, name="day_wise_count_tkc"),
    path('new_dashboard_history_vendor/<str:name>', views.new_dashboard_history_vendor, name='new_dashboard_history_vendor'),
    path('gtp_drawing_auditor_dashboard', views.gtp_drawing_auditor_dashboard, name="gtp_drawing_auditor_dashboard"),
    path('view_gtp_wo_wise/<int:id>',views.view_gtp_wo_wise, name="view_gtp_wo_wise"),
    path('deregister_cgm_all', views.deregister_cgm_all, name="deregister_cgm_all"),

    path('to_do', views.to_do, name="to_do"),
    path('pending_pdi_acceptance_data',views.pending_pdi_acceptance_data,name="pending_pdi_acceptance_data"),
    path('cgm_pending_vendor_data',views.cgm_pending_vendor_data,name="cgm_pending_vendor_data"),

]
