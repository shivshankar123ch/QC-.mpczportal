from django.db import models

# Create your models here.
from django.db import models
from main.models import *

# Create your models here.


from django.db import models
from main.models import *


# Create your models here.
class Rca_User_Registration(models.Model):
    User_Id = models.AutoField(primary_key=True)
    Type_of_business = models.CharField(max_length=20, null=True, blank=True)
    Authorised_person_E = models.CharField(max_length=100, null=True, blank=True)
    CompanyName_E = models.CharField(max_length=100, null=True, blank=True)
    ContactNo = models.CharField(max_length=20, null=True, blank=True)
    Email_Id = models.EmailField(max_length=50, null=True, blank=True)
    User_code = models.CharField(max_length=16, null=True, blank=True)
    # use value for Central Zone  = CZ  West Zone = WZ East Zone = EZ
    User_zone = models.CharField(max_length=10, null=True, blank=True)
    # use value for vendor = 1 nabl = 2 tkc = 3
    User_type = models.CharField(max_length=12, null=True, blank=True)
    Basic_Details = models.IntegerField(blank=True, null=True, default=0)
    Aadhar = models.CharField(max_length=15, null=True, blank=True)
    Otp = models.CharField(max_length=6, null=True, blank=True)
    payment = models.IntegerField(blank=True, default=0)
    factory_approval = models.IntegerField(blank=True, null=True, default=0)
    Authentication_id = models.CharField(max_length=20, null=True, blank=True)
    Company_Fax = models.CharField(max_length=20, null=True, blank=True)
    Company_Pan_No = models.CharField(max_length=15, null=True, blank=True)
    Company_Gumastha_No = models.CharField(max_length=25, null=True, blank=True)
    Company_Gst_No = models.CharField(max_length=25, null=True, blank=True)
    Registration_Date = models.DateField(null=True, blank=True)
    Company_add_1 = models.CharField(max_length=100, null=True, blank=True)
    Company_add_2 = models.CharField(max_length=100, null=True, blank=True)
    Company_pin_code = models.IntegerField(blank=True, null=True, default=0)
    Company_dist = models.CharField(max_length=30, null=True, blank=True)
    Company_state = models.CharField(max_length=30, null=True, blank=True)
    Company_t_add_1 = models.CharField(max_length=100, null=True, blank=True)
    Company_t_add_2 = models.CharField(max_length=100, null=True, blank=True)
    Company_t_pin_code = models.IntegerField(blank=True, null=True, default=0)
    Company_t_dist = models.CharField(max_length=30, null=True, blank=True)
    Company_t_state = models.CharField(max_length=30, null=True, blank=True)
    cgm_approval = models.IntegerField(blank=True, null=True, default=0)
    Company_city = models.CharField(max_length=50, null=True, blank=True)
    Company_t_add_1 = models.CharField(max_length=100, null=True, blank=True)
    Company_t_city = models.CharField(max_length=50, null=True, blank=True)
    profile_complete = models.IntegerField(blank=True, default=0, null=True)
    provision_fi = models.IntegerField(blank=True, default=0, null=True)
    factory_approval_payment = models.IntegerField(blank=True, null=True, default=0)
    factory_approval_status = models.IntegerField(blank=True, null=True, default=0)
    lat = models.CharField(max_length=15, null=True, blank=True)
    log = models.CharField(max_length=15, null=True, blank=True)
    digital_cert_upload = models.IntegerField(blank=True, null=True, default=0)
    cert = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    erp_cz_id = models.IntegerField(blank=True, default=0, null=True)
    erp_cz_number = models.IntegerField(blank=True, default=0, null=True)
    erp_ez_id = models.IntegerField(blank=True, default=0, null=True)
    erp_ez_number = models.IntegerField(blank=True, default=0, null=True)
    erp_wz_id = models.IntegerField(blank=True, default=0, null=True)
    erp_wz_number = models.IntegerField(blank=True, default=0, null=True)

    def _str_(self):
        return self.CompanyName_E

class Rca_Vendor_Document(models.Model):
    Vendor_Document_Id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Types_of_Docs = models.CharField(max_length=100, null=True, blank=True)
    Issued_office_Name = models.CharField(max_length=50, null=True, blank=True)
    Document_Number = models.CharField(max_length=50, null=True, blank=True)
    Name_on_Document = models.CharField(max_length=50, null=True, blank=True)
    Ddocfile = models.FileField(upload_to='documents/vendor/work_data', null=True, blank=True,default='documents/No_Preview.pdf')
    Doc_issue_date = models.DateField(default=None, null=True)
    Doc_expiry_date = models.DateField(default=None, null=True)
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    DGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    DGM_remark = models.CharField(max_length=100, null=True, blank=True)
    DGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    DGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True, null=True)
    Status = models.IntegerField(blank=True, default=0, null=True)
    Doc_type = models.CharField(max_length=50, null=True, blank=True)
    Po_file = models.FileField(upload_to='po')
    CGM_remark = models.CharField(max_length=100, null=True, blank=True)


class payment_rca(models.Model):
	user =  models.CharField(max_length=100,null=True,blank=True)
	Payment_For = models.CharField(max_length=100, null=True, blank=True)
	Hash_Id = models.CharField(max_length=255, null=True, blank=True)
	date = models.DateField(null=True, blank=True)
	Payu_Status = models.CharField(max_length=50, null=True, blank=True)
	Txdid = models.CharField(max_length=50, null=True, blank=True)
	Productinfo = models.CharField(max_length=100, null=True, blank=True)
	Firstname = models.CharField(max_length=100, null=True, blank=True)
	Lastname = models.CharField(max_length=100, null=True, blank=True)
	Contact_No = models.CharField(max_length=15, null=True, blank=True)
	Email_Id = models.EmailField(max_length=50, null=True, blank=True)
	Paymentgateway_Type = models.CharField(max_length=50, null=True, blank=True)
	Encrypted_PaymentId = models.CharField(max_length=100, null=True, blank=True)
	Bank_Ref_Num = models.CharField(max_length=150, null=True, blank=True)
	Bankcode = models.CharField(max_length=50, null=True, blank=True)
	Name_On_Card = models.CharField(max_length=50, null=True, blank=True)
	Cardnum = models.CharField(max_length=50, null=True, blank=True)
	Payu_Moneyid = models.CharField(max_length=50, null=True, blank=True)
	Netamount_Debited = models.CharField(max_length=50, null=True, blank=True)
	invoice = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
	company_name = models.CharField(max_length=100, null=True, blank=True)
    
class RCA_Vendor_Factory_image(models.Model):
    Vendor = models.ForeignKey(Rca_User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Image = models.FileField(upload_to='documents/rca_vendor/Factory')

class certificate_details_cra(models.Model):
    cert_id = models.AutoField(primary_key=True)
    User_Id = models.CharField(max_length=200, default="")
    company_name = models.CharField(max_length=200, default="")
    Company_add_1 = models.CharField(max_length=200, default="")
    Company_add_2 = models.CharField(max_length=200, default="")
    Company_dist = models.CharField(max_length=200, default="")
    Company_state = models.CharField(max_length=200, default="")
    Company_pin_code = models.CharField(max_length=200, default="")
    no = models.CharField(max_length=200, default="") # Registration number
    User_type = models.CharField(max_length=200, default="") #vendor, nabl, tkc
    vmaterial = models.CharField(max_length=200, default="") # materials
    day = models.CharField(max_length=100, null=True, blank=True)
    valid_upto = models.CharField(max_length=100, null=True, blank=True)
    employ_name = models.CharField(max_length=200, default="") #Officer_name
    designation = models.CharField(max_length=200, default="") #Officer Designation
    current_time = models.CharField(max_length=200, default="")
    tkc_class_contractor = models.CharField(max_length=200, default="")
    electic_liecense_date = models.CharField(max_length=200, default="")
    User_Zone = models.CharField(max_length=200, default="") # CZ, WZ, EZ
    nabl_cert_exp = models.CharField(max_length=100, null=True, blank=True)
    nabl_cert_number = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')    


class WO_Info(models.Model):
    rca_cell = models.ForeignKey(RCA_Cell, on_delete=models.CASCADE, null=True, blank=True)
    vendor_id = models.ForeignKey(Rca_User_Registration,on_delete=models.CASCADE, null=True, blank=True)
    tendor_no = models.CharField(max_length=100, null=True, blank=True)
    bid_open_date = models.DateField(null=True, blank=True)
    sub = models.CharField(max_length=1000, null=True, blank=True)
    work_order = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    wo_ack = models.IntegerField(blank=True, default=0)
    dispatch_no = models.CharField(max_length=100, null=True, blank=True)
    ordr_date = models.DateField(null=True, blank=True)
    wo_specification = models.CharField(max_length=100, null=True, blank=True)
    digi_sign_doc=models.FileField(upload_to='documents/rca/digital_sign_doc', null=True, blank=True)
    digi_flag=models.IntegerField(blank=True, default=0)
    bg_bank = models.CharField(max_length=200, null=True, blank=True)
    bg_no = models.CharField(max_length=30, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    valid_date = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    ac_number = models.CharField(max_length=25, null=True, blank=True)
    ifsc=models.CharField(max_length=15, null=True, blank=True)
    rca_bg_status=models.IntegerField(blank=True, default=0)
    rca_bg_accept=models.IntegerField(blank=True, default=0)
    rca_bg_submitted=models.IntegerField(blank=True, default=0)
    rca_bg_remark=models.CharField(max_length=100, null=True, blank=True)
    rca_bg_remark_flag=models.IntegerField(blank=True, default=0)    
    Account_Holder_Name = models.CharField(max_length=100, null=True, blank=True)
    rca_bg_upload=models.FileField(upload_to='documents/rca/rca_bg_upload', null=True, blank=True)
    bg_acceptance_letter=models.FileField(upload_to='documents/rca/rca_bg_upload', null=True, blank=True)
    claim_date=models.DateField(null=True, blank=True)
    # digi_sign_doc_ro=models.FileField(upload_to='documents/rca/digital_sign_doc_ro', null=True, blank=True)
    # digi_flag_ro=models.IntegerField(blank=True, default=0)

    def str(self):
        return self.WO_Info


class WO_Schedule_Info(models.Model):
    schedule_id = models.ForeignKey(WO_Info, on_delete=models.CASCADE, null=True, blank=True)
    schedule_name = models.CharField(max_length=100, null=True, blank=True)
    description_name = models.CharField(max_length=1000, null=True, blank=True)

    def _str_(self):
        return self.WO_Schedule_Info


class WO_Copy_Info(models.Model):
    wo = models.ForeignKey(WO_Info, on_delete=models.CASCADE, null=True, blank=True)
    copy_name = models.CharField(max_length=100, null=True, blank=True)

    def _str_(self):
        return self.WO_Copy_Info
    
    
    
    


class Multiple_Bg(models.Model):
    wo= models.ForeignKey(WO_Info, on_delete=models.CASCADE, null=True, blank=True)
    add_bg_bank = models.CharField(max_length=200, null=True, blank=True)
    add_bg_no = models.CharField(max_length=30, null=True, blank=True)
    add_amount = models.CharField(max_length=20, null=True, blank=True)
    add_ac_number = models.CharField(max_length=25, null=True, blank=True)
    add_ifsc=models.CharField(max_length=15, null=True, blank=True)
    add_bg_status=models.IntegerField(blank=True, default=0)
    add_bg_accept=models.IntegerField(blank=True, default=0)
    add_bg_submitted=models.IntegerField(blank=True, default=0)
    add_bg_remark=models.CharField(max_length=100, null=True, blank=True)
    add_bg_remark_flag=models.IntegerField(blank=True, default=0)
    add_Account_Holder_Name = models.CharField(max_length=100, null=True, blank=True)
    add_bg_upload=models.FileField(upload_to='documents/rca/additional_bg', null=True, blank=True)
    add_bg_acceptance_letter=models.FileField(upload_to='documents/rca/additional_bg_accept', null=True, blank=True)
    add_claim_date=models.DateField(null=True, blank=True)
    add_issue_date = models.DateField(null=True, blank=True)
    add_valid_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
         return self.Multiple_Bg



# class RO_Info(models.Model):
#     rca_cell = models.ForeignKey(RCA_Cell, on_delete=models.CASCADE, null=True, blank=True)
#     wo = models.ForeignKey(WO_Info, on_delete=models.CASCADE, null=True, blank=True)
#     store = models.ForeignKey(Store_Info, on_delete=models.CASCADE, null=True, blank=True)
#     digi_sign_doc_ro=models.FileField(upload_to='documents/rca/digital_sign_doc_ro', null=True, blank=True)
#     digi_flag_ro=models.IntegerField(blank=True, default=0)
#     mrc_flag=models.IntegerField(blank=True, default=0)
#     random_flag=models.IntegerField(blank=True, default=0)
#     dispatch_for_nabl = models.IntegerField(blank=True, default=0)
#     test_request_form = models.IntegerField(blank=True, default=0)
#     TRF_Id = models.IntegerField(blank=True, default=0)
#     nabl_manual_rej_flag=models.IntegerField(blank=True, default=0)
#     ro_nabl_lot_reject = models.IntegerField(blank=True, default=0)
#     ro_order_date = models.DateField(null=True, blank=True)
#     any_release_sampled = models.IntegerField(blank=True, default=0)
#     ro_as_nabl_receive_flag = models.IntegerField(blank=True, default=0)
#     complete_sampled_by_cgm = models.IntegerField(blank=True, default=0)
#     ro_sampling_date=models.DateField(null=True, blank=True)
#     ro_nabl_sin_rej=models.IntegerField(blank=True, default=0)
#     ro_nabl_mac_rej=models.IntegerField(blank=True, default=0)
#     ro_nabl_comp_rej=models.IntegerField(blank=True, default=0)
#     final_ro_mrc=models.IntegerField(blank=True, default=0)
#     ro_resampling_date=models.DateField(null=True, blank=True)
	

    

#     def str(self):
#         return self.RO_Info



class RO_Info(models.Model):
    rca_cell = models.ForeignKey(RCA_Cell, on_delete=models.CASCADE, null=True, blank=True)
    wo = models.ForeignKey(WO_Info, on_delete=models.CASCADE, null=True, blank=True)
    store = models.ForeignKey(Store_Info, on_delete=models.CASCADE, null=True, blank=True)
    digi_sign_doc_ro=models.FileField(upload_to='documents/rca/digital_sign_doc_ro', null=True, blank=True)
    digi_flag_ro=models.IntegerField(blank=True, default=0)
    mrc_flag=models.IntegerField(blank=True, default=0)
    random_flag=models.IntegerField(blank=True, default=0)
    dispatch_for_nabl = models.IntegerField(blank=True, default=0)
    test_request_form = models.IntegerField(blank=True, default=0)
    TRF_Id = models.IntegerField(blank=True, default=0)
    nabl_manual_rej_flag=models.IntegerField(blank=True, default=0)
    ro_nabl_lot_reject = models.IntegerField(blank=True, default=0)
    ro_order_date = models.DateField(null=True, blank=True)
    any_release_sampled = models.IntegerField(blank=True, default=0)
    ro_as_nabl_receive_flag = models.IntegerField(blank=True, default=0)
    complete_sampled_by_cgm = models.IntegerField(blank=True, default=0)
    ro_sampling_date=models.DateField(null=True, blank=True)
    ro_nabl_sin_rej=models.IntegerField(blank=True, default=0)
    ro_nabl_mac_rej=models.IntegerField(blank=True, default=0)
    ro_nabl_comp_rej=models.IntegerField(blank=True, default=0)
    final_ro_mrc=models.IntegerField(blank=True, default=0)
    ro_resampling_date=models.DateField(null=True, blank=True)
    ro_mrc_initiate=models.IntegerField(blank=True,default=0)
    partial_mrc_initiate=models.IntegerField(blank=True,default=0)
    mrc_flag_copy=models.IntegerField(blank=True, default=0)
    ro_ven_dis_flag = models.IntegerField(blank=True, default=0)
    ro_ven_dis_date=models.DateField(null=True, blank=True)
    

	

    def str(self):
        return self.RO_Info



class Pa_report(models.Model):
    rel = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    power_report_flag=models.FileField(upload_to='documents/rca/rel_pa_report', null=True, blank=True)
    power_report_date=models.DateField(null=True, blank=True)


# class rca_gatepass(models.Model):
    # gate_no = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    # gatepass_num=models.CharField(max_length=200, null=True, blank=True)
    # gatekeeper_name=models.CharField(max_length=200, null=True, blank=True)
    # vehicle_no=models.CharField(max_length=200, null=True, blank=True)
    # driver_name=models.CharField(max_length=200, null=True, blank=True)
    # driver_phone=models.CharField(max_length=15, null=True, blank=True)
    # gatepass_date=models.DateField(null=True, blank=True)
    # material_rec_by=models.CharField(max_length=200, null=True, blank=True)
    # outward_quantity=models.IntegerField(blank=True, default=0)
    # gatepass_flag=models.IntegerField(blank=True, default=0)
    # driver_aadhar=models.FileField(upload_to='documents/rca/all_xmr_report', null=True, blank=True)


    # def _str_(self):
        # return self.rca_gatepass
        

class rca_gatepass(models.Model):
    gate_no = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    gatepass_num=models.CharField(max_length=200, null=True, blank=True)
    gatekeeper_name=models.CharField(max_length=200, null=True, blank=True)
    vehicle_no=models.CharField(max_length=200, null=True, blank=True)
    driver_name=models.CharField(max_length=200, null=True, blank=True)
    driver_phone=models.CharField(max_length=15, null=True, blank=True)
    gatepass_date=models.DateField(null=True, blank=True)
    material_rec_by=models.CharField(max_length=200, null=True, blank=True)
    outward_quantity=models.IntegerField(blank=True, default=0)
    gatepass_flag=models.IntegerField(blank=True, default=0)
    driver_aadhar=models.FileField(upload_to='documents/rca/all_xmr_report', null=True, blank=True)


    def _str_(self):
        return self.rca_gatepass






class power_analyser_newdesign(models.Model):
    rating= models.CharField(max_length=200, null=True, blank=True)
    no_load_loss= models.IntegerField(blank=True, default=0)
    no_load_redstrip= models.IntegerField(blank=True, default=0)
    max_load_loss= models.IntegerField(blank=True, default=0)
    tolerance= models.IntegerField(blank=True, default=0)
    


class power_analyser_level1(models.Model):
    rating= models.CharField(max_length=200, null=True, blank=True)
    impedance= models.FloatField(blank=True, default=0)
    total_loss_50= models.IntegerField(blank=True, default=0)
    total_loss_100= models.IntegerField(blank=True, default=0)
    tolerance= models.IntegerField(blank=True, default=0)



class power_analyser_level2(models.Model):
    rating= models.CharField(max_length=200, null=True, blank=True)
    impedance=models.FloatField(blank=True, default=0)
    total_loss_50= models.IntegerField(blank=True, default=0)
    total_loss_100= models.IntegerField(blank=True, default=0)
    tolerance= models.IntegerField(blank=True, default=0)


class power_analyser_nonstar_newdesign(models.Model):
    rating= models.CharField(max_length=200, null=True, blank=True)
    no_load_loss= models.IntegerField(blank=True, default=0)
    no_load_redstrip= models.IntegerField(blank=True, default=0)
    max_load_loss= models.IntegerField(blank=True, default=0)
    tolerance= models.IntegerField(blank=True, default=0)
        

# class RO_Material_Info(models.Model):
    # ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    # rate = models.IntegerField(blank=True, default=0)
    # specification = models.CharField(max_length=100, null=True, blank=True)
    # rating = models.CharField(max_length=100, null=True, blank=True)
    # description = models.CharField(max_length=200, null=True, blank=True)
    # total_rate = models.IntegerField(blank=True, default=0)
    # quantity = models.IntegerField(blank=True, default=0)
    # digi_sign_doc_ro=models.FileField(upload_to='documents/rca/digital_sign_doc_ro', null=True, blank=True)
    # digi_flag_ro=models.IntegerField(blank=True, default=0)
    # nabl_lot_reject = models.IntegerField(blank=True, default=0)
    # mat_nabl_lot_reject = models.IntegerField(blank=True, default=0)
    # forward_for_sampling = models.IntegerField(blank=True, default=0)
    # forward_mat_to_cgm = models.IntegerField(blank=True, default=0)
    # def str(self):
        # return self.RO_Info


class RO_Material_Info(models.Model):
    ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.IntegerField(blank=True, default=0)
    specification = models.CharField(max_length=100, null=True, blank=True)
    rating = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    total_rate = models.IntegerField(blank=True, default=0)
    quantity = models.IntegerField(blank=True, default=0)
    digi_sign_doc_ro=models.FileField(upload_to='documents/rca/digital_sign_doc_ro', null=True, blank=True)
    digi_flag_ro=models.IntegerField(blank=True, default=0)
    nabl_lot_reject = models.IntegerField(blank=True, default=0)
    mat_nabl_lot_reject = models.IntegerField(blank=True, default=0)
    forward_for_sampling = models.IntegerField(blank=True, default=0)
    forward_mat_to_cgm = models.IntegerField(blank=True, default=0)
    mat_sampled_flag= models.IntegerField(blank=True, default=0)
    finally_sampled= models.IntegerField(blank=True, default=0)
    nabl_mat_lot_reject = models.IntegerField(blank=True, default=0)
    nabl_mat_lot_submit = models.IntegerField(blank=True, default=0)
    mat_rejection_flag=models.IntegerField(blank=True, default=0)
    flag_25_sampled=models.IntegerField(blank=True, default=0)
    flag_63_sampled=models.IntegerField(blank=True, default=0)
    flag_100_sampled=models.IntegerField(blank=True, default=0)
    flag_200_sampled=models.IntegerField(blank=True, default=0)
    nabl_mat_lot_reject = models.IntegerField(blank=True, default=0)
    nabl_mat_lot_submit = models.IntegerField(blank=True, default=0)
    nabl_as_lot_receive = models.IntegerField(blank=True, default=0)
    final_mrc_creation = models.IntegerField(blank=True, default=0)
    def str(self):
        return self.RO_Info

class RO_Schedule_Info(models.Model):
    ro_id = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    schedule_name = models.CharField(max_length=100, null=True, blank=True)
    description_name = models.CharField(max_length=1000, null=True, blank=True)

    def _str_(self):
        return self.RO_Schedule_Info


class RO_Copy(models.Model):
    ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    copy_name = models.CharField(max_length=100, null=True, blank=True)

    def _str_(self):
        return self.RO_Copy

# class as_issue_gatepass(models.Model):
    # ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    # as_issue_gp_num=models.CharField(max_length=200, null=True, blank=True)
    # as_issue_gp_date=models.DateField(null=True, blank=True)
    # as_issue_pr_name=models.CharField(max_length=200, null=True, blank=True)


class as_issue_gatepass(models.Model):
    ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    as_issue_gp_num=models.CharField(max_length=200, null=True, blank=True)
    as_issue_gp_date=models.DateField(null=True, blank=True)
    as_issue_pr_name=models.CharField(max_length=200, null=True, blank=True)


class Fault_DTR(models.Model):
    xmr_code = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=100, null=True, blank=True)

    def str(self):
        return self.Fault_DTR

class drr_info(models.Model):
    drr_no=models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    drr_date=models.DateField(null=True, blank=True)
    drr_vehicle=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_no=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_date=models.DateField(null=True, blank=True)
    drr_quantity=models.IntegerField(blank=True, default=0)

    def _str_(self):
        return self.drr_info


class as_nablpass_gatepass(models.Model):
    # inward_no = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    inward_mat= models.ForeignKey(RO_Material_Info, on_delete=models.CASCADE, null=True, blank=True)
    gp_in_num=models.CharField(max_length=200, null=True, blank=True)
    gp_in_gk_name=models.CharField(max_length=200, null=True, blank=True)
    gp_in_vehicle_no=models.CharField(max_length=200, null=True, blank=True)
    gp_in_driver_name=models.CharField(max_length=200, null=True, blank=True)
    gp_in_driver_phone=models.CharField(max_length=15, null=True, blank=True)
    gp_in_date=models.DateField(null=True, blank=True)
    gp_in_rec_by=models.CharField(max_length=200, null=True, blank=True)
    gp_in_quantity=models.IntegerField(blank=True, default=0)
    gp_in_flag=models.IntegerField(blank=True, default=0)
    gp_id_proof=models.FileField(upload_to='documents/rca/all_xmr_report', null=True, blank=True)


    def str(self):
        return self.as_nablpass_gatepass

class as_nabllotpass_gp(models.Model):
    lotp_inward_no = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    lotp_in_num=models.CharField(max_length=200, null=True, blank=True)
    lotp_in_gk_name=models.CharField(max_length=200, null=True, blank=True)
    lotp_in_vehicle_no=models.CharField(max_length=200, null=True, blank=True)
    lotp_in_driver_name=models.CharField(max_length=200, null=True, blank=True)
    lotp_in_driver_phone=models.CharField(max_length=15, null=True, blank=True)
    lotp_in_date=models.DateField(null=True, blank=True)
    lotp_in_rec_by=models.CharField(max_length=200, null=True, blank=True)
    lotp_in_quantity=models.IntegerField(blank=True, default=0)
    lotp_in_flag=models.IntegerField(blank=True, default=0)
    lotp_id_proof=models.FileField(upload_to='documents/rca/lotpass_gatepass', null=True, blank=True)

    def str(self):
        return self.as_nabllotpass_gp
        
        
class rca_mrc_details(models.Model):
    ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    ro_mat_id = models.ForeignKey(RO_Material_Info, on_delete=models.CASCADE, null=True, blank=True)
    mrc_date=models.DateField(null=True, blank=True)
    digi_sign_mr=models.FileField(upload_to='documents/rca/digital_sign_doc_mrc', null=True, blank=True)
    digi_flag_mr=models.IntegerField(blank=True, default=0)

    def str(self):
        return self.rca_mrc_details
  
class rca_mrc_copy(models.Model):
    mr = models.ForeignKey(rca_mrc_details, on_delete=models.CASCADE, null=True, blank=True)
    copy_name = models.CharField(max_length=100, null=True, blank=True)

    def str(self):
        return self.rca_mrc_copy

class rca_mrc_comment(models.Model):
    mr_no = models.ForeignKey(rca_mrc_details, on_delete=models.CASCADE, null=True, blank=True)
    add_comment = models.CharField(max_length=1000, null=True, blank=True)

    def str(self):
        return self.rca_mrc_comment
    
    
class partial_mrc_details(models.Model):
    ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    partial_date=models.DateField(null=True, blank=True)
    digi_sign_pr=models.FileField(upload_to='documents/rca/digital_sign_partial_mrc', null=True, blank=True)
    digi_flag_pr=models.IntegerField(blank=True, default=0)

    def str(self):
        return self.partial_mrc_details

  
class partial_mrc_copy(models.Model):
    ro = models.ForeignKey(partial_mrc_details, on_delete=models.CASCADE, null=True, blank=True)
    copy_name = models.CharField(max_length=100, null=True, blank=True)

    def _str_(self):
        return self.partial_mrc_copy

class partial_mrc_comment(models.Model):
    ro = models.ForeignKey(partial_mrc_details, on_delete=models.CASCADE, null=True, blank=True)
    add_comment = models.CharField(max_length=1000, null=True, blank=True)

    def _str_(self):
        return self.partial_mrc_comment
            

class rca_test_rept_power_analyzer(models.Model):
    
    pa_test_areastore = models.CharField(max_length=200, null=True, blank=True)
    xmr = models.CharField(max_length=200, null=True, blank=True)
    ptcode = models.CharField(max_length=200, null=True, blank=True)
    serial = models.CharField(max_length=200, null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    nlil1 = models.FloatField(null=True, blank=True)
    nlil2 = models.FloatField(null=True, blank=True)
    nlil3 = models.FloatField(null=True, blank=True)
    nlvoltage = models.FloatField(null=True, blank=True)
    nlfreq = models.FloatField(null=True, blank=True)
    flil1 = models.FloatField(null=True, blank=True)
    flil2 = models.FloatField(null=True, blank=True)
    flil3 = models.FloatField(null=True, blank=True)
    FLfreq = models.FloatField(null=True, blank=True)
    FLpower = models.FloatField(null=True, blank=True)
    hvAmp = models.FloatField(null=True, blank=True)
    FLvoltage = models.FloatField(null=True, blank=True)
    Rating = models.FloatField(null=True, blank=True)
    Type = models.CharField(max_length=200, null=True, blank=True)
    NlHvVolts = models.IntegerField(blank=True, null=True, default=0)
    NlLvVolts = models.IntegerField(blank=True, null=True, default=0)
    LVamp = models.FloatField(null=True, blank=True)
    Phase = models.IntegerField(blank=True, null=True, default=0)
    VectorGroup = models.CharField(max_length=200, null=True, blank=True)
    Freq = models.IntegerField(blank=True, null=True, default=0)
    ImpedenceVolts = models.FloatField(null=True, blank=True)
    CoolingType = models.CharField(max_length=200, null=True, blank=True)
    TempRise = models.FloatField(null=True, blank=True)
    OilVolume = models.FloatField(null=True, blank=True)
    OilMass = models.FloatField(null=True, blank=True)
    CoreWeight = models.FloatField(null=True, blank=True)
    TotalWeight = models.FloatField(null=True, blank=True)
    MfgYear = models.CharField(max_length=200, null=True, blank=True)
    WindMaterial = models.CharField(max_length=200, null=True, blank=True)
    RefStd = models.CharField(max_length=200, null=True, blank=True)
    OilTest = models.CharField(max_length=200, null=True, blank=True)
    LoadLoss50 = models.FloatField(null=True, blank=True)
    LoadLoss100 = models.FloatField(null=True, blank=True)
    MaxHVR = models.FloatField(null=True, blank=True)
    MaxLVR = models.FloatField(null=True, blank=True)
    FreqTest = models.CharField(max_length=200, null=True, blank=True)
    OverVoltageTest = models.CharField(max_length=200, null=True, blank=True)
    Ambient = models.FloatField(null=True, blank=True)
    HvRes1 = models.FloatField(null=True, blank=True)
    HvRes2 = models.FloatField(null=True, blank=True)
    HvRes3 = models.FloatField(null=True, blank=True)
    LvRes1 = models.FloatField(null=True, blank=True)
    LvRes2 = models.FloatField(null=True, blank=True)
    LvRes3 = models.FloatField(null=True, blank=True)
    VoltRatio1 = models.FloatField(null=True, blank=True)
    VoltRatio2 = models.FloatField(null=True, blank=True)
    VoltRatio3 = models.FloatField(null=True, blank=True)
    Polarity = models.CharField(max_length=200, null=True, blank=True)
    IR1 = models.FloatField(null=True, blank=True)
    IR2 = models.FloatField(null=True, blank=True)
    IR3 = models.FloatField(null=True, blank=True)
    NLpower = models.FloatField(null=True, blank=True)
    TestDate = models.DateTimeField(null=True, blank=True)
    Customer = models.CharField(max_length=200, null=True, blank=True)
    Transerial = models.CharField(max_length=200, null=True, blank=True)
    AmbFact = models.FloatField(null=True, blank=True)
    Zat75 = models.FloatField(null=True, blank=True)
    Zatamb = models.FloatField(null=True, blank=True)
    RatAmb = models.FloatField(null=True, blank=True)
    XatAnl = models.FloatField(null=True, blank=True)
    ZatRoom = models.FloatField(null=True, blank=True)
    HvperPhaseAtAmb = models.FloatField(null=True, blank=True)
    LVperPhaseAtAmb = models.FloatField(null=True, blank=True)
    HVRperphaseat75 = models.FloatField(null=True, blank=True)
    LVRperphaseat75 = models.FloatField(null=True, blank=True)
    TotalIsqRatAmb = models.FloatField(null=True, blank=True)
    StrayLossatAmb = models.FloatField(null=True, blank=True)
    StrayLossat75 = models.FloatField(null=True, blank=True)
    IsqRat75 = models.FloatField(null=True, blank=True)
    TotalLossat75 = models.FloatField(null=True, blank=True)
    guarantee50 = models.FloatField(null=True, blank=True)
    guarantee100 = models.FloatField(null=True, blank=True)
    OrderInfo = models.CharField(max_length=200, null=True, blank=True)
    OrderDate = models.DateTimeField(null=True, blank=True)



class RO_Material_XMR_Info(models.Model):
    ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    material = models.ForeignKey(RO_Material_Info, on_delete=models.CASCADE, null=True, blank=True)
    xmr = models.CharField(max_length=200, null=True, blank=True)
    vendor_send = models.IntegerField(blank=True, default=0)
    vendor_submitted = models.IntegerField(blank=True, default=0)
    physical_status = models.IntegerField(blank=True, default=0)
    as_remark = models.CharField(max_length=10, null=True, blank=True)
    acceptted_date = models.DateField(null=True, blank=True)
    as_accepted = models.IntegerField(blank=True, default=0)
    as_xmr_rej_resubmit= models.IntegerField(blank=True, default=0)
    as_xmr_rej_resubmit_date=models.DateField(null=True, blank=True)
    Is_Admin = models.IntegerField(null=True, blank=True)
    Is_Active = models.IntegerField(null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    pa_no_loss = models.FloatField(blank=True,null=True, default=0)
    pa_no_loss_per = models.FloatField(blank=True,null=True, default=0)
    pa_max_loss = models.FloatField(blank=True,null=True, default=0)
    pa_max_loss_per = models.FloatField(blank=True,null=True, default=0)
    pa_remark = models.CharField(max_length=10, null=True, blank=True)
    analyser_rprt=models.FileField(upload_to='documents/rca/power_test', null=True, blank=True)
    pa_result= models.IntegerField(blank=True, default=0)
    pa_report_flag=models.IntegerField(blank=True,default=0)
    pa_result_date= models.DateField(null=True, blank=True)
    pa_result_submitted= models.IntegerField(blank=True, default=0)
    pa_rej_resubmit= models.IntegerField(blank=True, default=0)
    pa_rej_resubmit_date= models.DateField(null=True, blank=True)
    uneco_status=models.IntegerField(blank=True, default=0)
    new_design=models.IntegerField(blank=True,default=0)
    old_l1=models.IntegerField(blank=True,default=0)
    old_l2=models.IntegerField(blank=True,default=0)
    xmr_type_submitted=models.IntegerField(blank=True,default=0)
    load_per=models.IntegerField(blank=True, default=0)
    drr_details=models.ForeignKey(drr_info, on_delete=models.CASCADE, null=True, blank=True)
    xmr_sampled_flag=models.IntegerField(blank=True, default=0)
    xmr_rej_gp_flag=models.IntegerField(blank=True, default=0)
    xmr_rej_gp_remark = models.CharField(max_length=100, null=True, blank=True)
    xmr_rej_gp_date = models.DateField(null=True, blank=True)
    xmr_rej_gp_submitted = models.IntegerField(blank=True, default=0)
    gatepass_details=models.ForeignKey(rca_gatepass, on_delete=models.CASCADE, null=True, blank=True)
    as_issue_mat=models.IntegerField(blank=True, default=0)
    nabl_lot_rej=models.IntegerField(blank=True, default=0)
    nabl_single_rej=models.IntegerField(blank=True, default=0)
    ##physical reject nabl
    ph_reject_by_nabl=models.IntegerField(blank=True, default=0)
    ph_reject_by_submit=models.IntegerField(blank=True, default=0)
    ####lot reject
    machine_reject_by_nabl=models.IntegerField(blank=True, default=0)
    nachine_reject_nabl_submit=models.IntegerField(blank=True, default=0)
    ##nabl machine single reject
    single_reject_by_nabl=models.IntegerField(blank=True, default=0)
    single_reject_nabl_submit=models.IntegerField(blank=True, default=0)
    xmr_replaced=models.IntegerField(blank=True, default=0)
    return_intent_mrc=models.IntegerField(blank=True, default=0)
    forward_to_mrc=models.IntegerField(blank=True, default=0)
    forward_for_sampling=models.IntegerField(blank=True, default=0)
    as_issue_gp=models.ForeignKey(as_issue_gatepass, on_delete=models.CASCADE, null=True, blank=True)
    as_nabl_approve = models.ForeignKey(as_nablpass_gatepass, on_delete=models.CASCADE, null=True, blank=True)
    as_nabl_approve_flag = models.IntegerField(blank=True, default=0)
    as_nabl_approve_submitted = models.IntegerField(blank=True, default=0)
    as_nabl_approve_date = models.DateField(null=True, blank=True)
    as_issue_xmr_date=models.DateField(null=True, blank=True)
    xmr_ven_dispatch_date=models.DateField(null=True, blank=True)
    pa_api=models.ForeignKey(rca_test_rept_power_analyzer,on_delete=models.CASCADE, null=True, blank=True)
    xmr_initial_sampled_flag=models.IntegerField(blank=True)
    xmr_second_sampled_flag=models.IntegerField(blank=True)
    design_non_star=models.IntegerField(blank=True, default=0)
    as_nabl_lotgp = models.ForeignKey(as_nabllotpass_gp, on_delete=models.CASCADE, null=True, blank=True)
    partial_mrc_det = models.ForeignKey(partial_mrc_details, on_delete=models.CASCADE, null=True, blank=True)
    partial_mrc_xmr_submit = models.IntegerField(blank=True, default=0)

    def _str_(self):
        return self.RO_Material_XMR_Info


# class Request_Of_Oil(models.Model):
    # ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    # v_request_quantity = models.IntegerField(blank=True, default=0)
    # available_quantity = models.IntegerField(blank=True, default=0)
    # rca_forward_to_as = models.IntegerField(blank=True, default=0)
    # as_forward_to_rca = models.IntegerField(blank=True, default=0)
    # vendor_receive = models.IntegerField(blank=True, default=0)

    # def _str_(self):
        # return self.Request_Of_Oil


# class Oil_Request(models.Model):
    # ro = models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    # v_request_quantity = models.IntegerField(blank=True, null=True, default=0)
    #v_request_quantity_date=models.DateField(null=True, blank=True)
    # available_quantity = models.IntegerField(blank=True, null=True, default=0)
    #available_quantity_date=models.DateField(null=True, blank=True)
    # rca_forward_to_as = models.IntegerField(blank=True,  null=True,default=0)
    # as_forward_to_rca = models.IntegerField(blank=True, null=True, default=0)
    # rca_forward_to_vendor = models.IntegerField(blank=True, null=True, default=0)
    # vendor_receive = models.IntegerField(blank=True,  null=True,default=0)

    # def _str_(self):
        # return self.Oil_Request


# class di_dtr(models.Model):
    # ro=models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    # v_material_offer=models.IntegerField(blank=True, null=True, default=0)
    # r_di_inst=models.IntegerField(blank=True, null=True, default=0)
   
    # def _str_(self):
        # return self.di_dtr

class material_offer(models.Model):
    ro=models.ForeignKey(RO_Info, on_delete=models.CASCADE, null=True, blank=True)
    quanity_offered=models.CharField(max_length=100, null=True, blank=True)
    mo_capacity=models.ForeignKey(RO_Material_Info,on_delete=models.CASCADE,null=True, blank=True)
    material_status=models.IntegerField(blank=True, null=True, default=0)
    issue_di=models.IntegerField(blank=True, null=True, default=0)
    all_xmr_rprt=models.FileField(upload_to='documents/rca/all_xmr_report', null=True, blank=True)


    def _str_(self):
        return self.material_offer

class RcaProcurementInfo(models.Model):
    rcaPo_id = models.CharField(max_length=200, null=True, blank=True)
    dispatch_for_nabl = models.IntegerField(blank=True, default=0)
    test_request_form = models.IntegerField(blank=True, default=0)
    TRF_Id = models.IntegerField(blank=True, default=0)

    def _str_(self):
        return self.TRF_Id

class Rcatrf_Details(models.Model):
    TRF_Id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    racPo_id = models.IntegerField(blank=True, default=0)
    customer_Organization_name = models.CharField(max_length=200, null=True, blank=True)
    customer_Organization_address = models.CharField(max_length=200, null=True, blank=True)
    contact_person_name = models.CharField(max_length=200, null=True, blank=True)
    mobile_no = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    name_of_sample_product = models.CharField(max_length=200, null=True, blank=True)
    customer_ref_gatepass_no = models.CharField(max_length=200, null=True, blank=True)
    dated = models.DateField(null=True, blank=True)
    sample_description_condition = models.CharField(max_length=200, null=True, blank=True)
    test_spec = models.CharField(max_length=200, null=True, blank=True)
    drawings_catalogs_operating_manual = models.CharField(max_length=200, null=True, blank=True)
    sample_identification_no = models.CharField(max_length=200, null=True, blank=True)
    decision_on_compliance = models.CharField(max_length=200, null=True, blank=True)
    for_tolerance = models.CharField(max_length=200, null=True, blank=True)
    mu_status = models.CharField(max_length=200, null=True, blank=True)
    sign = models.CharField(max_length=200, null=True, blank=True)
    gatepass_gen = models.IntegerField(blank=True, default=0)
    outpass_gen = models.IntegerField(blank=True, default=0)

class Rca_TRF_Test_Details(models.Model):
    TRF_Test_Id = models.IntegerField(blank=True, null=True, default=0)
    TRF_Id = models.IntegerField(blank=True, default=0)
    TRF_Test_Name = models.CharField(max_length=100, null=True, blank=True)    
