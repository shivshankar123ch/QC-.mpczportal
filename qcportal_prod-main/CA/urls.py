from django.contrib import admin
from django.urls import path
from CA import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('otp_verify', views.otp_verify, name="otp_verify"),
    path('regca', views.regca, name="regca"),
    path('all_commerical_pending', views.all_commerical_pending, name="all_commerical_pending"),
    path('commercial', views.commercial, name="commercial"),
    path('finance', views.finance, name="finance"),
    path('ae_dashboard', views.ae_dashboard, name="ae_dashboard"),
    path('uploaded_data',views.uploaded_data,name="uploaded_data"),
    path('agent_search',views.agent_search,name="agent_search"),
    path('commerical_invoice_ca_otp',views.commerical_invoice_ca_otp,name="commerical_invoice_ca_otp"),
    path('commerical_invoice_ca',views.commerical_invoice_ca,name='commerical_invoice_ca'),
    path('Cash_Voucher/<int:id>',views.Cash_Voucher,name='Cash_Voucher'),
    path('Cash_Voucher_list',views.Cash_Voucher_list,name='Cash_Voucher_list'),
    path('ca_invoice',views.ca_invoice,name='ca_invoice.html'),
    path('ca_invoice/<str:title>',views.ca_invoice_details,name='ca_invoice_details'),
    path('fi_Cash_Voucher/<int:id>',views.fi_Cash_Voucher,name='fi_Cash_Voucher'),
    path('agents_details_otp',views.agents_details_otp,name="agents_details_otp"),
    path('agents_details', views.agents_details, name="agents_details"),
    path('agents_all_details/<int:id>', views.agents_all_details, name='agents_all_details'),
    path('agents_details_ae', views.agents_details_ae, name="agents_details_ae"),
    path('agents_all_details_ae/<int:id>', views.agents_all_details_ae, name='agents_all_details_ae'),
    path('reject_agents_details_ae', views.reject_agents_details_ae, name="reject_agents_details_ae"),
    path('approved_agents_details_ae', views.approved_agents_details_ae, name="approved_agents_details_ae"),
    path('agents_upload_detail', views.agents_upload_detail, name="agents_upload_detail"),
    path('payment', views.payment, name="payment"),
    path('payment/success',views.payu_success_registration,name="payu_success_registration"),
    path('payment/failure',views.payu_failure1,name="payu_failure1"),
    path('payment_invoice',views.payment_invoice,name="payment_invoice"),
    path('all_collectionagent', views.all_collectionagent, name="all_collectionagent"),
    path('detail_by_pincode/<int:pincode_number>', views.detail_by_pincode, name='detail_by_pincode'),


    
    path('transaction_upload', views.transaction_upload, name="transaction_upload"),
    path('transaction_viewdata', views.all_collection_agentdata, name="transaction_viewdata"),       
    path('all_collection_agentdata', views.all_collection_agentdata, name="all_collection_agentdata"),
    path('agents_details_ce', views.agents_details_ce, name="agents_details_ce"),
    path('agents_details_ce_pending', views.agents_details_ce_pending, name="agents_details_ce_pending"),
    path('agents_details_ce_approved', views.agents_details_ce_approved, name="agents_details_ce_approved"),


    path('all_commercial', views.all_commercial, name="all_commercial"),
    path('all_commercial_save/<int:id>', views.all_commercial_save, name="all_commercial_save"),
    path('agents_details_ce_pending_save/<int:id>', views.agents_details_ce_pending_save, name='agents_details_ce_pending_save'),

    path('finance_details', views.finance_details, name="finance_details"),
    path('finance_details_fi', views.finance_details_fi, name="finance_details_fi"),
    path('finance_details_pending', views.finance_details_pending, name="finance_details_pending"),

    path('finance_details_save/<int:id>', views.finance_details_save, name='finance_details_save'),

    path('logout', views.logout, name="logout"),




    path('basic', views.basic, name="basic"),


    path('gen_invoice_ca', views.gen_invoice_ca, name="gen_invoice_ca"),
  

    path('commerical_ce_pending', views.commerical_ce_pending, name="commerical_ce_pendings"),
    path('commerical_pending', views.commerical_pending, name="commerical_pending"),

    path('commerical_invoice/<int:id>', views.commerical_invoice, name="commerical_invoice"),
    path('commerical_approve_save/<int:id>', views.commerical_approve_save, name="commerical_approve_save"),

    path('invoice_otp', views.invoice_otp, name="invoice_otp"),


    path('finance_invoice/<str:title>', views.finance_invoice, name="finance_invoice"),
    path('finance_approve_save/<int:id>', views.finance_approve_save, name="finance_approve_save"),
    path('finance_invoice_otp', views.finance_invoice_otp, name="finance_invoice_otp"),


    path('pcv_invoice', views.pcv_invoice, name="pcv_invoice"),
    path('commerical_approved', views.commerical_approved, name="commerical_approved"),

    path('commerical_invoice2/<str:title>', views.commerical_invoice2, name="commerical_invoice2"),

    #URL for deregistration of CA
    path('ca_deregistered', views.ca_deregistered, name="ca_deregistered"),
    path('ca_deregistered_req', views.ca_deregistered_request, name="ca_deregistered_req"),
    path('deregistration_requests', views.deregistration_requests, name = "deregistration_requests"),
    path('view_deregistered_data/<int:id>', views.view_deregistered_data, name = "view_deregistered_data"),
    path('ca_deregister_rq_approve', views.ca_deregister_rq_approve, name = "ca_deregister_rq_approve"),
    path('deregistration_cash_voucher', views.deregistration_cash_voucher, name = "deregistration_cash_voucher"),
    path('deregistration_receipt', views.deregistration_receipt, name = "deregistration_receipt"),
    path('deregister_cash_voucher_list', views.deregister_cash_voucher_list, name = "deregister_cash_voucher_list"),
    path('deregister_cash_Voucher/<int:id>',views.deregister_cash_Voucher,name='deregister_cash_Voucher'),
    path('finance_cash_voucher_list',views.finance_cash_voucher_list,name='finance_cash_voucher_list'),
    path('finance_deregister_cash_Voucher/<int:id>',views.finance_deregister_cash_Voucher,name='finance_deregister_cash_Voucher'),

    #URL for security refund of CA
    path('ca_security_refund', views.ca_security_refund, name="ca_security_refund"),
    path('ca_security_refund_req', views.ca_security_refund_req, name="ca_security_refund_req"),
    path('security_refund_requests', views.security_refund_requests, name = "security_refund_requests"),
    path('view_security_refund_data/<str:data_id>', views.view_security_refund_data, name = "view_security_refund_data"),
    path('ca_security_refund_rq_approve', views.ca_security_refund_rq_approve, name = "ca_security_refund_rq_approve"),
    path('security_refund_cash_voucher', views.security_refund_cash_voucher, name = "security_refund_cash_voucher"),
    path('security_refund_receipt', views.security_refund_receipt, name = "security_refund_receipt"),
    path('security_refund_cash_Voucher/<int:id>', views.security_refund_cash_Voucher, name = "security_refund_cash_Voucher"),
    path('security_refund_cash_voucher_list',views.security_refund_cash_voucher_list,name='security_refund_cash_voucher_list'),
    path('finance_security_refund_cash_Voucher/<int:id>',views.finance_security_refund_cash_Voucher,name='finance_security_refund_cash_Voucher'),

    #URL for Collection agent Reports 
    

    #URLs for Reports Section
    path('ca_reports', views.ca_report, name="ca_reports"),
    path('ca_txn_report', views.ca_txn_report, name="ca_txn_report"),
    # path('ca_monthly_transaction_report', views.ca_monthly_transaction_report, name="ca_monthly_transaction_report"),
    path('ca_bank_update', views.ca_bank_update, name="ca_bank_update"),
    path('bank_change_requests', views.bank_change_requests, name="bank_change_requests"),
    path('view_bank_passbook_data/<int:id>/<int:agent_id>', views.view_bank_passbook_data, name="view_bank_passbook_data"),
    path('ca_bank_approved/<int:agent_id>/<int:new_data_id>', views.ca_bank_approved, name="ca_bank_approved"),
    path('ca_bank_reject/<int:agent_id>/<int:new_data_id>', views.ca_bank_reject, name="ca_bank_reject"),
    path('all_ca_list', views.all_ca_list, name="all_ca_list"),
    path('ca_total_deregister', views.ca_total_deregister, name="ca_total_deregister"),
    path('ca_total_security_refund', views.ca_total_security_refund, name="ca_total_security_refund"),
    path('bank_change_requests_IT', views.bank_change_requests_IT, name="bank_change_requests_IT"),
    path('view_bank_passbook_data_IT/<int:id>/<int:agent_id>', views.view_bank_passbook_data_IT, name="view_bank_passbook_data_IT"),
    path('commercial_ca_reports', views.commercial_ca_reports, name="commercial_ca_reports"),
    path('commercial_ca_txn_report', views.commercial_ca_txn_report, name="commercial_ca_txn_report"),
    path('commercial_all_ca_list', views.commercial_all_ca_list, name="commercial_all_ca_list"),
    path('commercial_ca_total_deregister', views.commercial_ca_total_deregister, name="commercial_ca_total_deregister"),
    path('commercial_ca_total_security_refund', views.commercial_ca_total_security_refund, name="commercial_ca_total_security_refund"),
    path('commercial_bank_change_requests_IT', views.commercial_bank_change_requests_IT, name="commercial_bank_change_requests_IT"),
    path('commercial_view_bank_passbook_data_IT/<int:id>/<int:agent_id>', views.commercial_view_bank_passbook_data_IT, name="commercial_view_bank_passbook_data_IT"),
    path('detail_by_pincode/<int:pincode_number>', views.detail_by_pincode, name='detail_by_pincode'),

    
    
    
    ]
