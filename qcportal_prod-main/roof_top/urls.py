from django.contrib import admin
from django.urls import path
from roof_top import views

urlpatterns = [

    
    path('login_reg', views.login_reg, name="login_reg"),
    path('roof_top_one', views.roof_top_one, name="roof_top_one"),
    path('check_otp', views.check_otp, name="check_otp"),
    path('profile', views.profile, name="profile"),
    path('update_profile', views.update_profile, name="update_profile"),
    path('agent_basic', views.agent_basic, name="agent_basic"),
    path('roof_top_upload', views.roof_top_upload, name="roof_top_upload"),
    path('view_document', views.view_document, name="view_document"),
    path('roof_top_payment', views.roof_top_payment, name="roof_top_payment"),
    path('rejected_doc', views.rejected_doc, name='rejected_doc'),
    path('rejected_doc_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),  


    path('rejected_doc_save_approver/<int:id>', views.rejected_doc_save_approver, name='rejected_doc_save_approver'),  
    path('payu_success_registration', views.payu_success_registration, name="payu_success_registration"),
    path('payment_fail', views.payu_failure1, name="payu_failure1"),

    path('payment_fail', views.payu_failure1, name="payu_failure1"),

    path('payu/success/', views.payu_success_registration, name="payu/success"),

    path('payu/failure/', views.payu_failure1, name="payu/failure/"),

    path('payu/failure/', views.payu_failure1, name="payu/failure/"),

    path('transaction_history_solar', views.transaction_history_solar, name="transaction_history_solar"),

    path('view_loa', views.view_loa, name="view_loa"),

    path('solar_vendor_all_approved_list/', views.solar_vendor_all_list, name="solar_vendor_all_approved_list"),
    path('get_data_from_registration_no/', views.get_data_from_registration_no, name="get_data_from_registration_no"),

    path('zone_wise', views.zone_wise, name="zone_wise"),

    
    

    



    
    
    


]
