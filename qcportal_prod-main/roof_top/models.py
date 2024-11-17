from atexit import register
from re import T
from django.db import models

# Create your models here.

# Create your models here.
class roof_top_first(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=85, null=True, blank=True)
    agency_name = models.CharField(max_length=100, null=True, blank=True)
    name_of_auth = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    gst = models.CharField(max_length=15, null=True, blank=True)
    dist = models.CharField(max_length=15, null=True, blank=True)
    pan_card = models.CharField(max_length=30, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    reg_date = models.DateField(default=None, null=True)
    created_by = models.CharField(max_length=15, null=True, blank=True)
    otp = models.CharField(max_length=15, null=True, blank=True)
    profile_complete = models.IntegerField(blank=True, default=0, null=True)
    viewer_officer = models.IntegerField(blank=True, default=0, null=True)
    approver_officer = models.IntegerField(blank=True, default=0, null=True)
    final_rejection = models.IntegerField(blank=True, default=0, null=True)
    payment = models.IntegerField(blank=True, default=0, null=True)
    basic_details = models.IntegerField(blank=True, default=0, null=True)
    imageCert = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    loa = models.IntegerField(blank=True, default=0, null=True)
    registration_no = models.CharField(max_length=200, default="") 
    user_zone = models.CharField(max_length=200, default="") 
    # doc for approval in work use 1 and finance use 2


class roof_top_sec(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=35, null=True, blank=True)
    Types_of_Docs = models.CharField(max_length=100, null=True, blank=True)
    Issued_office_Name = models.CharField(max_length=50, null=True, blank=True)
    Document_Number = models.CharField(max_length=15, null=True, blank=True)
    Name_on_Document = models.CharField(max_length=50, null=True, blank=True)
    Ddocfile = models.FileField(upload_to='documents/vendor/work_data', null=True, blank=True,default='')
    Doc_issue_date = models.DateField(default=None, null=True)
    Doc_expiry_date = models.DateField(default=None, null=True)
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_verification_Status_approver = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    DGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    DGM_remark = models.CharField(max_length=100, null=True, blank=True)
    DGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    DGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True, null=True)
    Status = models.IntegerField(blank=True, default=0, null=True)
    Status_approver = models.IntegerField(blank=True, default=0, null=True)
    Doc_type = models.CharField(max_length=50, null=True, blank=True)
    Po_file = models.FileField(upload_to='po')
    CGM_remark = models.CharField(max_length=100, null=True, blank=True)
    
    # doc for approval in work use 1 and finance use 2

class root_top_cert_details(models.Model):
    cert_id = models.AutoField(primary_key=True)
    User_Id = models.CharField(max_length=200, default="")
    agency_name = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=500, default="")
    registration_no = models.CharField(max_length=200, default="") # Registration number
    User_type = models.CharField(max_length=200, default="") #roof top vendor
    current_date = models.DateTimeField(null=True, blank=True)
    current_time = models.CharField(max_length=200, default="")
    valid_upto = models.DateTimeField(null=True, blank=True)
    Officer_name = models.CharField(max_length=200, default="") #Officer_name
    Officer_designation = models.CharField(max_length=200, default="") #Officer Designation
    User_Zone = models.CharField(max_length=200, default="") # CZ, WZ, EZ
    otp = models.IntegerField(blank=True, default=0, null=True)
    image = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')



class payment_roof_top(models.Model):
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


class roof_top_loa(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=35, null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    loa_file = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    viewer = models.IntegerField(blank=True, default=0, null=True)
    approver = models.IntegerField(blank=True, default=0, null=True)
    Primary_verification_Status_approver = models.IntegerField(blank=True, default=0, null=True)
    remark = models.CharField(max_length=35, null=True, blank=True)
    signed_loa_file = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    annexure = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    vendor_document = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    bg_status = models.IntegerField(blank=True, default=0, null=True)
    Doc_issue_date = models.DateField(default=None, null=True)


class solar_sd(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=35, null=True, blank=True)
    agency_name = models.CharField(max_length=100, null=True, blank=True)
    bg_name = models.CharField(max_length=200, null=True, blank=True)
    bg_no = models.CharField(max_length=30, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    valid_date = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    bg_document = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    bank_order = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)



# ***************************************************EZ

    
    # doc for approval in work use 1 and finance use 2

class root_top_cert_details_ez(models.Model):
    cert_id = models.AutoField(primary_key=True)
    User_Id = models.CharField(max_length=200, default="")
    agency_name = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=500, default="")
    registration_no = models.CharField(max_length=200, default="") # Registration number
    User_type = models.CharField(max_length=200, default="") #roof top vendor
    current_date = models.DateTimeField(null=True, blank=True)
    current_time = models.CharField(max_length=200, default="")
    valid_upto = models.DateTimeField(null=True, blank=True)
    Officer_name = models.CharField(max_length=200, default="") #Officer_name
    Officer_designation = models.CharField(max_length=200, default="") #Officer Designation
    User_Zone = models.CharField(max_length=200, default="") # CZ, WZ, EZ
    otp = models.IntegerField(blank=True, default=0, null=True)
    image = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')



class payment_roof_top_ez(models.Model):
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



class roof_top_loa_ez(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=35, null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    loa_file = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    viewer = models.IntegerField(blank=True, default=0, null=True)
    approver = models.IntegerField(blank=True, default=0, null=True)
    Primary_verification_Status_approver = models.IntegerField(blank=True, default=0, null=True)
    remark = models.CharField(max_length=35, null=True, blank=True)
    signed_loa_file = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    annexure = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    vendor_document = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    bg_status = models.IntegerField(blank=True, default=0, null=True)
    Doc_issue_date = models.DateField(default=None, null=True)


class solar_sd_ez(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=35, null=True, blank=True)
    agency_name = models.CharField(max_length=100, null=True, blank=True)
    bg_name = models.CharField(max_length=200, null=True, blank=True)
    bg_no = models.CharField(max_length=30, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    valid_date = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    bg_document = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    bank_order = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)

# *********************************************************WZ


    
    # doc for approval in work use 1 and finance use 2

class root_top_cert_details_wz(models.Model):
    cert_id = models.AutoField(primary_key=True)
    User_Id = models.CharField(max_length=200, default="")
    agency_name = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=500, default="")
    registration_no = models.CharField(max_length=200, default="") # Registration number
    User_type = models.CharField(max_length=200, default="") #roof top vendor
    current_date = models.DateTimeField(null=True, blank=True)
    current_time = models.CharField(max_length=200, default="")
    valid_upto = models.DateTimeField(null=True, blank=True)
    Officer_name = models.CharField(max_length=200, default="") #Officer_name
    Officer_designation = models.CharField(max_length=200, default="") #Officer Designation
    User_Zone = models.CharField(max_length=200, default="") # CZ, WZ, EZ
    otp = models.IntegerField(blank=True, default=0, null=True)
    image = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')



class payment_roof_top_wz(models.Model):
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



class roof_top_loa_wz(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=35, null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    loa_file = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    viewer = models.IntegerField(blank=True, default=0, null=True)
    approver = models.IntegerField(blank=True, default=0, null=True)
    Primary_verification_Status_approver = models.IntegerField(blank=True, default=0, null=True)
    remark = models.CharField(max_length=35, null=True, blank=True)
    signed_loa_file = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    annexure = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    vendor_document = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    bg_status = models.IntegerField(blank=True, default=0, null=True)


class solar_sd_wz(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=35, null=True, blank=True)
    agency_name = models.CharField(max_length=100, null=True, blank=True)
    bg_name = models.CharField(max_length=200, null=True, blank=True)
    bg_no = models.CharField(max_length=30, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    valid_date = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    bg_document = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    bank_order = models.FileField(upload_to='roofTopCertificate/', null=True, blank=True, default='')
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    Doc_issue_date = models.DateField(default=None, null=True)
