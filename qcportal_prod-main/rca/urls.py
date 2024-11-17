from django.contrib import admin
from django.urls import path
from rca import views

urlpatterns = [

path('create_wo', views.create_wo, name="create_wo"),
path('rca_base', views.rca_base, name="rca_base"),
path('rca_order', views.rca_order,name="rca_order"),
path('rca_order_add_schedule/<int:id>', views.rca_order_add_schedule, name="rca_order_add_schedule"),
path('rca_order_add_copy_to/<int:id>', views.rca_order_add_copy_to, name="rca_order_add_copy_to"),
path('rca_order_view/<int:id>', views.rca_order_view, name="rca_order_view"),
path('rca_all_work_order',views.rca_all_work_order,name="rca_all_work_order"),
path('rca_ro_create',views.rca_ro_create,name="rca_ro_create"),
path('rca_ro_add_material',views.rca_ro_add_material,name="rca_ro_add_material"),
path('rca_ro_add_rating/<int:id>',views.rca_ro_add_rating,name="rca_ro_add_rating"),
path('rca_ro_order_add_schedule/<int:id>', views.rca_ro_order_add_schedule, name="rca_ro_order_add_schedule"),
path('rca_ro_order_add_copy_to/<int:id>', views.rca_ro_order_add_copy_to, name="rca_ro_order_add_copy_to"),
path('rca_ro_view/<int:id>', views.rca_ro_view, name="rca_ro_view"),
path('rca_all_release_order',views.rca_all_release_order,name="rca_all_release_order"),
path('all_oil_request', views.all_oil_request, name="all_oil_request"),
path('oil_request_forward/<int:id>', views.oil_request_forward, name="oil_request_forward"),
path('oil_request_forward_vendor/<int:id>', views.oil_request_forward_vendor, name="oil_request_forward_vendor"),
path('RCA_dtr_issued',views.RCA_dtr_issued,name="RCA_dtr_issued"),
path('rca_di_view/<int:id>',views.rca_di_view,name="rca_di_view"),
path('rca_as_oil_confirmed',views.rca_as_oil_confirmed,name="rca_as_oil_confirmed"),
path('rca_oilconfir_for_ven/<int:id>',views.rca_oilconfir_for_ven,name="rca_oilconfir_for_ven"),








path('rca_allotment', views.rca_allotment, name="rca_allotment"),
path('rca_as', views.rca_as, name="rca_as"),
path('rca_di', views.rca_di, name="rca_di"),

path('rca_inspection_officer_base', views.rca_inspection_officer_base, name="rca_inspection_officer_base"),
path('rca_inspection_pending', views.rca_inspection_pending, name="rca_inspection_pending"),
path('rca_inspection_pending2', views.rca_inspection_pending2, name="rca_inspection_pending2"),
path('rca_inspection_complete', views.rca_inspection_complete, name="rca_inspection_complete"),

path('rca_vendor_base', views.rca_vendor_base, name="rca_vendor_base"),
path('rca_acceptance', views.rca_acceptance, name="rca_acceptance"),
path('rca_release_ack', views.rca_release_ack, name="rca_release_ack"),
path('rca_repair_ue', views.rca_repair_ue, name="rca_repair_ue"),
path('rca_to_as', views.rca_to_as, name="rca_to_as"),
path('RCA_di_issue',views.RCA_di_issue,name="RCA_di_issue"),
path('RCA_di_issue_view/<int:id>',views.RCA_di_issue_view,name="RCA_di_issue_view"),
path('RCA_di_issue_accept/<int:id>',views.RCA_di_issue_accept,name="RCA_di_issue_accept"),


###### as_circle_officer #######

path('rca_as_circle_wo',views.rca_as_circle_wo,name="rca_as_circle_wo"),
path('rca_as_circle_ro',views.rca_as_circle_ro,name='rca_as_circle_ro'),
path('rca_as_circle_issue',views.rca_as_circle_issue,name='rca_as_circle_issue'),
path('rca_as_circle_inward/<int:id>',views.rca_as_circle_inward,name='rca_as_circle_inward'),

# rohit*********************************

path('rca_login', views.rca_login, name="rca_login"),
path('check_otp', views.check_otp, name="check_otp"),
path('upload_docs', views.upload_docs, name="upload_docs"),
path('view_document', views.view_document, name="view_document"),

path('rca_payment', views.rca_payment, name="rca_payment"),

path('payu_success_registration', views.payu_success_registration, name="payu_success_registration"),

path('update_profile', views.update_profile, name="update_profile"),

path('rca_basic', views.rca_basic, name="rca_basic"),

path('payment_dis', views.payment_dis, name="payment_dis"),
path('certificate_details', views.certificate_details, name="certificate_details"),
path('rca_ven_bg_order_list/',views.rca_ven_bg_order_list,name="rca_ven_bg_order_list"),
path('rca_ven_bg_confirm/<int:id>',views.rca_ven_bg_confirm,name="rca_ven_bg_confirm"),
path('rca_ven_dtr_dis_order_list',views.rca_ven_dtr_dis_order_list,name="rca_ven_dtr_dis_order_list"),
path('rca_ven_dtr_dis/<int:id>',views.rca_ven_dtr_dis,name="rca_ven_dtr_dis"),
path('vednor_approved_list_rca_cell',views.approved_vendor_list_rca_cell,name="approved_vendor_list_rca_cell"),
path('vendor_material_rca_cell/<int:id>',views.vendor_check_material_rca_cell,name="vendor_check_material_rca_cell"),
path('vendor_basic_details_rca_cell/<int:id>',views.vendor_basic_details_rca_cell,name="vendor_basic_details_rca_cell"),



# lok...............................additional bg

path('add_bg_order_list',views.add_bg_order_list,name='add_bg_order_list'),
path('additional_bg_confirm/<int:id>',views.additional_bg_confirm,name='additional_bg_confirm'),





]
