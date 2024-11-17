from django.contrib import admin
from django.urls import path
from tkc import views

urlpatterns = [
    path('login', views.Logout, name='Logout'),
    path('tkc_reg_seven', views.tkc_reg_seven, name='tkc_reg_seven'),
    path('tkc_reg_eight', views.tkc_reg_eight, name='tkc_reg_eight'),

    path('tkc_reg_nine', views.tkc_reg_nine, name='tkc_reg_nine'),

    path('tkc_reg_ten', views.tkc_reg_ten, name='tkc_reg_ten'),
    path('tkc_reg_eleven', views.tkc_reg_eleven, name='tkc_reg_eleven'),
    path('tkc_reg_twelve', views.tkc_reg_twelve, name='tkc_reg_twelve'),

    path('base', views.base, name='base'),
    path('updatedata', views.updatedata, name='updatedata'),
    path('basic', views.basic, name='basic'),
    path('complete', views.complete, name='complete'),
    path('activation', views.activation, name='activation'),
    path('tkc_update', views.tkc_update, name='tkc_update'),
    path('rejected_doc', views.rejected_doc, name='rejected_doc'),
    path('rejected_doc_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),
    path('rejected_doc_finance_save/<int:id>', views.rejected_doc_finance_save, name='rejected_doc_finance_save'),
    path('rejected_doc_cgm_save/<int:id>', views.rejected_doc_save, name='rejected_doc_save'),
    path('message', views.message, name='message'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('activation_after_expired', views.activation_after_expired, name='activation_after_expired'),
    path('activation_before_expired', views.activation_before_expired, name='activation_before_expired'),

    #####
    # path('payu_demo1',views.payu_demo1,name="payu_demo1"),
    # path('success',views.payu_success1,name='payu_success1'),
    # path('payu/failure',views.payu_failure,name='payu_failure'),




    path('payu_demo_tkc',views.payu_demo_tkc,name="payu_demo_tkc"),
    path('payu/success',views.payu_success_tkc,name='payu_success_tkc'),
    path('payu/failure',views.payu_failure,name='payu_failure'),
    path('payu/gen_invoice_first_tkc', views.gen_invoice_first_tkc, name='gen_invoice_first_tkc'),
    path('tkc_view_profile',views.tkc_view_profile,name='tkc_view_profile'),
    path('transaction_history', views.transaction_history, name='transaction_history'),


]
