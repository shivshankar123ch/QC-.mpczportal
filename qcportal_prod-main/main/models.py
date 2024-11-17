from django.db import models
from datetime import datetime
from po.models import *


# Create your models here.

class OwnerShip_Type_Table_Master(models.Model):
    OwnerShip_type_Id = models.AutoField(primary_key=True)
    OwnerShip_type_Name_E = models.CharField(max_length=100, null=True, blank=True)
    OwnerShip_type_Name_H = models.CharField(max_length=100, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.IntegerField(blank=True, null=True, default=0)
    From_Date = models.IntegerField(blank=True, null=True, default=0)
    Till_Date = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.OwnerShip_type_Name_E


# Discom Master
class Discom_Master(models.Model):
    Discom_Code = models.CharField(max_length=300, null=True, blank=True)
    Discom_Name_E = models.CharField(max_length=300, null=True, blank=True)
    Discom_Name_H = models.CharField(max_length=300, null=True, blank=True)
    Discom_Short_Name = models.CharField(max_length=300, null=True, blank=True)
    Discom_location = models.CharField(max_length=300, null=True, blank=True)
    Discom_Address = models.CharField(max_length=300, null=True, blank=True)
    Discom_Contact_Number = models.CharField(max_length=300, null=True, blank=True)
    Discom_CIN_Number = models.CharField(max_length=300, null=True, blank=True)
    Discom_GST_Number = models.CharField(max_length=300, null=True, blank=True)
    Discom_Logo_Doc = models.FileField(upload_to='logo', null=True, blank=True)
    Discom_Header = models.FileField(upload_to='logo', null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Updated_By = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Updated_At = models.DateTimeField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=1)
    Po_Main_Sign = models.CharField(max_length=50, null=True, blank=True)
    Po_Copy_To_Sign = models.CharField(max_length=50, null=True, blank=True)
    TKC_Main_Sign = models.CharField(max_length=50, null=True, blank=True)
    TKC_Copy_To_Sign = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Discom_Name_E


class Region_Master(models.Model):
    Region_Code = models.CharField(max_length=300, null=True, blank=True)
    Region_Name_E = models.CharField(max_length=300, null=True, blank=True)
    Region_Name_H = models.CharField(max_length=300, null=True, blank=True)
    region_discom_name = models.CharField(max_length=300, null=True, blank=True)
    Discom = models.ForeignKey(Discom_Master, on_delete=models.CASCADE, null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Updated_By = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Updated_At = models.DateTimeField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=1)
    Po_Main_Sign = models.CharField(max_length=50, null=True, blank=True)
    Po_Copy_To_Sign = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Region_Name_E


class Circle_Master(models.Model):
    Region = models.ForeignKey(Region_Master, on_delete=models.CASCADE, null=True, blank=True)
    Circle_Code = models.CharField(max_length=300, null=True, blank=True)
    Circle_Name_E = models.CharField(max_length=300, null=True, blank=True)
    Circle_Name_H = models.CharField(max_length=300, null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Updated_By = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Updated_At = models.DateTimeField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.Circle_Name_E


class Division_Master(models.Model):
    Circle = models.ForeignKey(Circle_Master, on_delete=models.CASCADE, null=True, blank=True)
    Division_Code = models.CharField(max_length=300, null=True, blank=True)
    Division_Name_E = models.CharField(max_length=300, null=True, blank=True)
    Division_Name_H = models.CharField(max_length=300, null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Updated_By = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Updated_At = models.DateTimeField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.Division_Name_E


class Sub_Division_Master(models.Model):
    Division = models.ForeignKey(Division_Master, on_delete=models.CASCADE, null=True, blank=True)
    Sub_Division_Code = models.CharField(max_length=300, null=True, blank=True)
    Sub_Division_Name_E = models.CharField(max_length=300, null=True, blank=True)
    Sub_Division_Name_H = models.CharField(max_length=300, null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Updated_By = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Updated_At = models.DateTimeField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.Sub_Division_Name_E

class DC_Master(models.Model):
    Sub_Division = models.ForeignKey(Sub_Division_Master, on_delete=models.CASCADE, null=True, blank=True)
    DC_Code = models.CharField(max_length=300, null=True, blank=True)
    DC_Name_E = models.CharField(max_length=300, null=True, blank=True)
    DC_Name_H = models.CharField(max_length=300, null=True, blank=True)
    DC_Short_Name = models.CharField(max_length=300, null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Updated_By = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Updated_At = models.DateTimeField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return self.DC_Name_E




class PO_Type_Table_Master(models.Model):
    PO_type_Id = models.AutoField(primary_key=True)
    PO_type_Name = models.CharField(max_length=100, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.IntegerField(blank=True, null=True, default=0)
    From_Date = models.IntegerField(blank=True, null=True, default=0)
    Till_Date = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.PO_type_Name


class PO_Clause_Master(models.Model):
    PO_Clause_Id = models.AutoField(primary_key=True)
    PO_Clause_Name = models.CharField(max_length=200, null=True, blank=True)
    PO_Clause_Description = models.TextField(default="", null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.IntegerField(blank=True, null=True, default=0)
    From_Date = models.IntegerField(blank=True, null=True, default=0)
    Till_Date = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.PO_Clause_Name


class PO_Type_Clause(models.Model):
    PO_type_Id = models.ForeignKey(PO_Type_Table_Master, on_delete=models.CASCADE, null=True, blank=True)
    PO_Clause_Id = models.ForeignKey(PO_Clause_Master, on_delete=models.CASCADE, null=True, blank=True)


class User_login_table(models.Model):
    User_Id = models.AutoField(primary_key=True)
    User_Password = models.CharField(max_length=20, null=True, blank=True)
    User_type_Id = models.CharField(max_length=20, null=True, blank=True)
    OTP_No = models.CharField(max_length=10, null=True, blank=True)
    Verify_Status = models.IntegerField(blank=True, null=True, default=0)
    Last_Login = models.DateTimeField(null=True, blank=True)
    Is_Deleted = models.BooleanField()
    In_Between_Date = models.DateField(null=True, blank=True)
    Out_Between_Date = models.DateField(null=True, blank=True)
    Contact_No = models.CharField(max_length=15, null=True, blank=True)


class Bank_Master_Table(models.Model):
    Bank_id = models.AutoField(primary_key=True)
    Bank_Name = models.CharField(max_length=40, null=True, blank=True)
    Bank_Code = models.CharField(max_length=20, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Created_Date = models.DateField(null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)


class State_Master_Table(models.Model):
    State_Id = models.AutoField(primary_key=True)
    State_Code = models.CharField(max_length=20, null=True, blank=True)
    State_Name_E = models.CharField(max_length=20, null=True, blank=True)
    State_Name_H = models.CharField(max_length=20, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Created_Date = models.DateField(null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.BooleanField()


class District_Master_Table(models.Model):
    District_Id = models.AutoField(primary_key=True)
    District_Name_E = models.CharField(max_length=20, null=True, blank=True)
    District_Name_H = models.CharField(max_length=20, null=True, blank=True)
    Distict_Code = models.CharField(max_length=10, null=True, blank=True)
    State_Id = models.CharField(max_length=10, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Created_Date = models.DateField(null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.BooleanField()


class City_Table_Master(models.Model):
    City_Id = models.AutoField(primary_key=True)
    City_name_E = models.CharField(max_length=20, null=True, blank=True)
    City_name_H = models.CharField(max_length=20, null=True, blank=True)
    State_id = models.CharField(max_length=20, null=True, blank=True)
    District_id = models.CharField(max_length=20, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Created_Date = models.DateField(null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.BooleanField()


class Pin_Code_Table_Master(models.Model):
    pincode_Id = models.AutoField(primary_key=True)
    Pincode_number = models.IntegerField(blank=True, null=True, default=0)
    State = models.CharField(max_length=100, null=True, blank=True)
    District = models.CharField(max_length=100, null=True, blank=True)
    City = models.CharField(max_length=100, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Created_Date = models.DateField(null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)


class User_Registration(models.Model):
    User_Id = models.AutoField(primary_key=True)
    Type_of_business = models.CharField(max_length=20, null=True, blank=True)
    Authorised_person_E = models.CharField(max_length=100, null=True, blank=True)
    Authorised_person_H = models.CharField(max_length=100, null=True, blank=True)
    CompanyName_E = models.CharField(max_length=100, null=True, blank=True)
    CompanyName_H = models.CharField(max_length=100, null=True, blank=True)
    ContactNo = models.CharField(max_length=20, null=True, blank=True)
    Email_Id = models.EmailField(max_length=50, null=True, blank=True)
    User_code = models.CharField(max_length=16, null=True, blank=True)
    # use value for Central Zone  = CZ  West Zone = WZ East Zone = EZ
    User_zone = models.CharField(max_length=10, null=True, blank=True)
    # use value for vendor = 1 nabl = 2 tkc = 3
    User_type = models.CharField(max_length=12, null=True, blank=True)
    Basic_Details = models.IntegerField(blank=True, null=True, default=0)
    Complete_Details = models.IntegerField(blank=True, null=True, default=0)
    Experience = models.IntegerField(blank=True, null=True, default=0)
    Turnover = models.FloatField(blank=True, null=True, default=0)
    Vendor_type = models.CharField(max_length=3, null=True, blank=True)
    Oyt = models.CharField(max_length=3, null=True, blank=True)
    Upgrade_Oyt = models.CharField(max_length=3, null=True, blank=True)
    New_Oyt = models.CharField(max_length=3, null=True, blank=True)
    Pancard = models.CharField(max_length=12, null=True, blank=True)
    Aadhar = models.CharField(max_length=15, null=True, blank=True)
    Otp = models.CharField(max_length=6, null=True, blank=True)
    payment = models.IntegerField(blank=True, default=0)
    complete_data = models.IntegerField(blank=True, default=0)
    work_approval = models.IntegerField(blank=True, null=True, default=0)
    work_rejection = models.IntegerField(blank=True, null=True, default=0)
    finance_approval = models.IntegerField(blank=True, null=True, default=0)
    finance_rejection = models.IntegerField(blank=True, null=True, default=0)
    factory_approval_status = models.IntegerField(blank=True, null=True, default=0)
    factory_approval_payment = models.IntegerField(blank=True, null=True, default=0)
    factory_approval = models.IntegerField(blank=True, null=True, default=0)
    factory_rejection = models.IntegerField(blank=True, null=True, default=0)
    cgm_approval = models.IntegerField(blank=True, null=True, default=0)
    final_rejection = models.IntegerField(blank=True, null=True, default=0)
    Authentication_id = models.CharField(max_length=20, null=True, blank=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True, null=True)
    Updated_Date = models.DateTimeField(auto_now=True, null=True)
    add_material = models.IntegerField(blank=True, null=True, default=0)
    qc_approval = models.IntegerField(blank=True, null=True, default=0)
    qc_rejection = models.IntegerField(blank=True, null=True, default=0)
    profile_update_fee = models.IntegerField(blank=True, null=True, default=0)
    activation = models.IntegerField(blank=True, null=True, default=0)
    activation_payment = models.IntegerField(blank=True, null=True, default=0)
    upgrade = models.IntegerField(blank=True, null=True, default=0)
    upgrade_payment = models.IntegerField(blank=True, null=True, default=0)
    rca_vendor = models.IntegerField(blank=True, null=True, default=0)  # lokendra21-03
    tkc_payment = models.IntegerField(blank=True, null=True, default=0)
    activation_before_expired = models.IntegerField(blank=True, null=True, default=0)
    activation_after_expired = models.IntegerField(blank=True, null=True, default=0)
    status = models.IntegerField(blank=True, null=True, default=0)
    cert_image = models.FileField(upload_to='certificate/', blank=True, null=True)
    digital_cert_upload = models.IntegerField(blank=True, null=True, default=0)
    blacklisted = models.IntegerField(blank=True, null=True, default=0)
    erp_cz_id = models.CharField(max_length=50,  blank=True, null=True)
    erp_wz_id = models.CharField(max_length=50, blank=True, null=True)
    erp_ez_id = models.CharField(max_length=50, blank=True, null=True)
    by_discom = models.IntegerField(blank=True, null=True, default=0)
    rca_and_vendor = models.IntegerField(blank=True, null=True, default=0)
    #date_of_approved = models.DateTimeField()
    date_of_approved = models.DateTimeField(null=True,blank=True)
    reg_date = models.DateField(null=True, blank=True)
    is_cpri_user = models.BooleanField(default = False)
    factory_waiver = models.IntegerField(blank=True, null=True, default=0)
    deregister = models.IntegerField(blank=True, null=True, default=0)
    dgm_work_reject_date = models.DateTimeField(blank=True, null=True)
    dgm_work_approved_date = models.DateTimeField(blank=True, null=True)
    dgm_finance_reject_date = models.DateTimeField(blank=True, null=True)
    dgm_finance_approved_date = models.DateTimeField(blank=True, null=True)
    gm_work_reject_date = models.DateTimeField(blank=True, null=True)
    gm_work_approved_date = models.DateTimeField(blank=True, null=True)
    document_resubmit_date = models.DateTimeField(blank=True, null=True)
    officer_create = models.IntegerField(blank=True, null=True, default=0)
    cert_image_tkc = models.FileField(upload_to='certificate_tkc/', blank=True, null=True)
    Authentication_id_new = models.CharField(max_length=20, null=True, blank=True)
    is_erp_pushed = models.BooleanField(default=False)
    otp_not_change = models.IntegerField(blank=True, null=True, default=0)
    def __str__(self):
        return self.CompanyName_E


class UserCompanyData(models.Model):
    Company_Id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    CompanyName_E = models.CharField(max_length=100, null=True, blank=True)
    CompanyName_H = models.CharField(max_length=100, null=True, blank=True)
    Company_Contact_No = models.CharField(max_length=15, null=True, blank=True)
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


class UserCompanyDataMain(models.Model):
    Company_Id = models.AutoField(primary_key=True)
    user_id_id = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    CompanyName_E = models.CharField(max_length=100, null=True, blank=True)
    CompanyName_H = models.CharField(max_length=100, null=True, blank=True)
    Company_Contact_No = models.CharField(max_length=15, null=True, blank=True)
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
    Company_city = models.CharField(max_length=50, null=True, blank=True)
    Company_t_add_1 = models.CharField(max_length=100, null=True, blank=True)
    Company_t_add_2 = models.CharField(max_length=100, null=True, blank=True)
    Company_t_pin_code = models.IntegerField(blank=True, null=True, default=0)
    Company_t_dist = models.CharField(max_length=30, null=True, blank=True)
    Company_t_state = models.CharField(max_length=30, null=True, blank=True)
    Company_t_city = models.CharField(max_length=50, null=True, blank=True)
    Reg_No = models.CharField(max_length=10, blank=True, null=True)  # add new for api

    Mi_Type_of_Inspection = models.CharField(max_length=100, blank=True, null=True)  # add new api
    # Letter_No = models.CharField( max_length=10, blank=True,null=True)#add new for(PO number rhega)
    Mi_Remark = models.CharField(max_length=10, blank=True, null=True)  # add new


class AuthorisedPerson(models.Model):
    AuthorisedPerson_id = models.AutoField(primary_key=True)
    user_id_id = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    Authorised_P_Name_E = models.CharField(max_length=100, null=True, blank=True)
    Authorised_P_Name_H = models.CharField(max_length=100, null=True, blank=True)
    Authorised_P_DOB = models.DateField(null=True, blank=True)
    Authorised_P_Number = models.CharField(max_length=15, null=True, blank=True)
    Authorised_P_Email = models.CharField(max_length=15, null=True, blank=True)
    Authorised_P_Aadhar_No = models.CharField(max_length=15, null=True, blank=True)
    Authorised_P_add_1 = models.CharField(max_length=100, null=True, blank=True)
    Authorised_P_add_2 = models.CharField(max_length=100, null=True, blank=True)
    Authorised_P_pin_code = models.IntegerField(blank=True, null=True, default=0)
    Authorised_P_state = models.CharField(max_length=50, null=True, blank=True)
    Authorised_P_District = models.CharField(max_length=50, null=True, blank=True)
    Authorised_P_City = models.CharField(max_length=50, null=True, blank=True)
    Director_P_Name_E = models.CharField(max_length=50, null=True, blank=True)
    Director_P_Name_H = models.CharField(max_length=50, null=True, blank=True)
    Director_P_DOB = models.DateField(null=True, blank=True)
    Director_P_Number = models.CharField(max_length=15, null=True, blank=True)
    Director_P_Email = models.CharField(max_length=50, null=True, blank=True)
    Director_P_Aadhar_No = models.CharField(max_length=15, null=True, blank=True)
    Director_P_add_1 = models.CharField(max_length=100, null=True, blank=True)
    Director_P_add_2 = models.CharField(max_length=100, null=True, blank=True)
    Director_P_pin_code = models.IntegerField(blank=True, null=True, default=0)
    Director_P_state = models.CharField(max_length=50, null=True, blank=True)
    Director_P_District = models.CharField(max_length=50, null=True, blank=True)
    Director_P_City = models.CharField(max_length=50, null=True, blank=True)
    Status = models.IntegerField(blank=True, default=0)


class BankDetails(models.Model):
    Bank_Id = models.AutoField(primary_key=True)
    po_no = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Bank_name = models.CharField(max_length=100, null=True, blank=True)
    Account_Holder_Name = models.CharField(max_length=100, null=True, blank=True)
    Account_Number = models.CharField(max_length=25, null=True, blank=True)
    IFSC = models.CharField(max_length=15, null=True, blank=True)
    Status = models.IntegerField(blank=True, default=0)
    new_data = models.IntegerField(blank=True, default=0, null=True)
    file = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    cancel_check = models.FileField(upload_to='user/main/cancel_check/', null=True, blank=True)
    bank_submit = models.IntegerField(null=True, blank=True, default=0)
    bank_review = models.IntegerField(null=True, blank=True, default=0)
    bank_approved = models.IntegerField(null=True, blank=True, default=0)
    submit_at = models.DateTimeField(null=True, blank=True)
    review_remark = models.CharField(max_length=300, null=True, blank=True)
    review_by = models.CharField(max_length=300, null=True, blank=True)
    review_at = models.DateTimeField(null=True, blank=True)
    approved_remark = models.CharField(max_length=300, null=True, blank=True)
    approved_by = models.CharField(max_length=300, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

class PaymentDetails(models.Model):
    payment_Id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    Payment_mode = models.CharField(max_length=15, null=True, blank=True)
    Transaction_id = models.CharField(max_length=15, null=True, blank=True)
    Status = models.IntegerField(blank=True, default=0)


class Role_Master(models.Model):
    Role_Id = models.AutoField(primary_key=True)
    Role_Name = models.CharField(max_length=100, null=True, blank=True)
    Role_Description = models.CharField(max_length=200, null=True, blank=True)
    Role_Priority = models.CharField(max_length=15, null=True, blank=True)
    Is_Admin = models.IntegerField(null=True, blank=True)
    Is_Active = models.IntegerField(null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    user_zone = models.CharField(max_length=15, null=True, blank=True)
    #Discom = models.ForeignKey(Discom_Master, on_delete=models.CASCADE, null=True, blank=True)
    #Region = models.ForeignKey(Region_Master, on_delete=models.CASCADE, null=True, blank=True)
    #Circle = models.ForeignKey(Circle_Master, on_delete=models.CASCADE, null=True, blank=True)
    #Division = models.ForeignKey(Division_Master, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Role_Name


class RCA_Cell(models.Model):
    Name=  models.CharField(max_length=100, null=True, blank=True)
    user_zone = models.CharField(max_length=10, null=True, blank=True)
    Discom = models.ForeignKey(Discom_Master, on_delete=models.CASCADE, null=True, blank=True)
    Region = models.ForeignKey(Region_Master, on_delete=models.CASCADE, null=True, blank=True)

class Store_Info(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Town = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=200, null=True, blank=True)
    lat = models.CharField(max_length=200, null=True, blank=True)
    lon = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    Is_Admin = models.IntegerField(null=True, blank=True)
    Is_Active = models.IntegerField(null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    Discom = models.ForeignKey(Discom_Master, on_delete=models.CASCADE, null=True, blank=True)
    Region = models.ForeignKey(Region_Master, on_delete=models.CASCADE, null=True, blank=True)
    Circle = models.ForeignKey(Circle_Master, on_delete=models.CASCADE, null=True, blank=True)
    Division = models.ForeignKey(Division_Master, on_delete=models.CASCADE, null=True, blank=True)
    Rca_cell= models.ForeignKey(RCA_Cell, on_delete=models.CASCADE, null=True, blank=True)

class Officer(models.Model):
    POSTED = (
        ("0", "ADMIN"),
        ("1", "DIS COM"),
        ("2", "REGION"),
        ("3", "DIVISION"),
        ("4", "SUB DIVISION"),
        ("5", "DC"),
        ("6", "RCA CELL"),
        ("7", "AREA STORE"))
    employ_id = models.AutoField(primary_key=True)
    rank = models.CharField(max_length=50, null=True, blank=True)
    employ_login_id = models.CharField(max_length=100, null=True, blank=True)
    employ_name = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(Role_Master, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='officer/image', null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    user_zone = models.CharField(max_length=15, null=True, blank=True)
    Discom = models.ForeignKey(Discom_Master, on_delete=models.CASCADE, null=True, blank=True)
    Region = models.ForeignKey(Region_Master, on_delete=models.CASCADE, null=True, blank=True)
    Circle = models.ForeignKey(Circle_Master, on_delete=models.CASCADE, null=True, blank=True)
    Division = models.ForeignKey(Division_Master, on_delete=models.CASCADE, null=True, blank=True)
    Posted = models.CharField(max_length=100,choices=POSTED, null=True, blank=True)
    DC_Zone = models.ForeignKey(DC_Master, on_delete=models.CASCADE, null=True, blank=True)# add by shubham tripathi for je location
    is_active = models.BooleanField(default=True,blank=True,null=True)# add by shubham tripathi suggenst by rustam sir and yashwant sir

    def __str__(self):
        return self.employ_login_id

class AreaStore_Officer(models.Model):
    Officer = models.ForeignKey(Officer, on_delete=models.CASCADE, null=True, blank=True)
    AreaStore = models.ForeignKey(Store_Info, on_delete=models.CASCADE, null=True, blank=True)

class VendorDispatchInfo(models.Model):
    po_id = models.ForeignKey(ProcurementInfo, on_delete=models.CASCADE, null=True, blank=True)
    item_quantity = models.IntegerField(blank=True)
    inspecting_officer_id = models.CharField(max_length=10, null=True, blank=True)
    lab_name = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    test_status = models.IntegerField(blank=True, default=0)

    def _str_(self):
        return self.VendorDispatchInfo_id


WORK = (
    ("MQP", "Material Inspection"),
    ("FQP", "Field Inspection "),
    ("FI", "Factory Inspection"),
    ("RFI", "RCA Factory Inspection"))


class InspectingOfficerInfo(models.Model):
    officer_name = models.CharField(max_length=100, null=True, blank=True)
    contact_no = models.CharField(max_length=100, null=True, blank=True)
    officer_email = models.CharField(max_length=100, null=True, blank=True)
    officer_employ_id = models.CharField(max_length=100, null=True, blank=True)
    officer_designation = models.CharField(max_length=100, null=True, blank=True)
    officer_password = models.CharField(max_length=100, null=True, blank=True)
    officer_work = models.CharField(max_length=100, choices=WORK, null=True, blank=True)
    user_zone = models.CharField(max_length=15, null=True, blank=True)
    officer_address = models.CharField(max_length=50, null=True, blank=True)
    officer_region = models.CharField(max_length=50, null=True, blank=True)
    Otp = models.CharField(max_length=50, null=True, blank=True)

    def _str_(self):
        return self.officer_name


class VendorDispatchItemInfo(models.Model):
    dispatch_d = models.IntegerField(blank=True)
    serial_number = models.CharField(max_length=30, null=True, blank=True)
    status = models.IntegerField(blank=True, default=0)
    remark = models.CharField(max_length=200, null=True, blank=True)

    def str(self):
        return self.serial_number


class TestReport(models.Model):
    VendorDispatchInfo = models.IntegerField(blank=True)
    item_serial_no = models.IntegerField(blank=True)
    item_name = models.CharField(max_length=30, null=True, blank=True)
    test_applied = models.CharField(max_length=30, null=True, blank=True)
    test_result = models.IntegerField(blank=True)
    status = models.IntegerField(blank=True, default=0)


class LocalStore(models.Model):
    store_name = models.CharField(max_length=30, null=True, blank=True)
    add_store_address = models.CharField(max_length=30, null=True, blank=True)
    store_latitude = models.CharField(max_length=30, null=True, blank=True)
    store_longitude = models.CharField(max_length=30, null=True, blank=True)
    store_officer_id = models.CharField(max_length=30, null=True, blank=True)
    store_officer_contact_no = models.CharField(max_length=30, null=True, blank=True)

    def _str_(self):
        return self.add_store_name


class LocalStoreInventory(models.Model):
    store_name = models.CharField(max_length=30, null=True, blank=True)
    po_id = models.IntegerField(blank=True)
    Di_Id = models.IntegerField(blank=True)
    quantity = models.IntegerField(blank=True)

    def _str_(self):
        return self.store_name


class LabInfo(models.Model):
    select_product = models.CharField(max_length=30, null=True, blank=True)
    name_of_material_for_testing = models.CharField(max_length=30, null=True, blank=True)
    is_as_per_tender = models.CharField(max_length=30, null=True, blank=True)
    select_testing = models.CharField(max_length=30, null=True, blank=True)


class PO_Type_Table_Master(models.Model):
    PO_type_Id = models.AutoField(primary_key=True)
    PO_type_Name = models.CharField(max_length=100, null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.IntegerField(blank=True, null=True, default=0)
    From_Date = models.IntegerField(blank=True, null=True, default=0)
    Till_Date = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.PO_type_Name


from tinymce import models as tinymce_models


class PO_Clause_Master(models.Model):
    PO_Clause_Id = models.AutoField(primary_key=True)
    PO_Clause_Name = models.CharField(max_length=200, null=True, blank=True)
    PO_Clause_Description = tinymce_models.HTMLField(null=True, blank=True)
    # PO_Clause_Description = models.TextField(default="", null=True, blank=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_Date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.IntegerField(blank=True, null=True, default=0)
    From_Date = models.IntegerField(blank=True, null=True, default=0)
    Till_Date = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.PO_Clause_Name


class PO_Type_Clause(models.Model):
    PO_type_Id = models.ForeignKey(PO_Type_Table_Master, on_delete=models.CASCADE, null=True, blank=True)
    PO_Clause_Id = models.ForeignKey(PO_Clause_Master, on_delete=models.CASCADE, null=True, blank=True)


class FI_Officer(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Contact_Number = models.CharField(max_length=20, null=True, blank=True)


# lokendra...............................................

class Payudata_main(models.Model):
    User_Id = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
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
    Error = models.CharField(max_length=500, null=True, blank=True)
    user_zone = models.CharField(max_length=5, null=True, blank=True)


class Add_material_nabl(models.Model):
    TRF_Id = models.CharField(max_length=15, null=True, blank=True)
    Submitted_by = models.CharField(max_length=200, null=True, blank=True)
    Test_Request_Form_by = models.CharField(max_length=200, null=True, blank=True)
    select_material = models.CharField(max_length=200, null=True, blank=True)
    select_specification = models.CharField(max_length=200, null=True, blank=True)
    material_number_list = models.CharField(max_length=200, null=True, blank=True)
    Allot_no = models.CharField(max_length=200, null=True, blank=True)
    Material_id = models.CharField(max_length=200, null=True, blank=True)
    Start_date = models.CharField(max_length=200, null=True, blank=True)
    End_Date = models.CharField(max_length=200, null=True, blank=True)
    sample_received = models.IntegerField(blank=True, null=True, default=0)
    job_order_complete = models.IntegerField(blank=True, null=True, default=0)
    emp_name = models.CharField(max_length=200, null=True, blank=True)
    Reject = models.IntegerField(blank=True, null=True, default=0)
    Reject_Remark = models.CharField(max_length=200, null=True, blank=True)
    # user_id = models.CharField(max_length=15, null=True, blank=True)
    driver_name = models.CharField(max_length=200, null=True, blank=True)
    vehicle_number = models.CharField(max_length=200, null=True, blank=True)
    out_date = models.CharField(max_length=200, null=True, blank=True)
    ro_id = models.CharField(max_length=15, null=True, blank=True)
    driver_mobile = models.CharField(max_length=200, null=True, blank=True)
    receiver_name = models.CharField(max_length=200, null=True, blank=True)
    Material_name = models.CharField(max_length=200, null=True, blank=True)
    trnsfrmr_type = models.CharField(max_length=200, null=True, blank=True)
    manufacturer_name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.CharField(max_length=200, null=True, blank=True)
    order_number = models.CharField(max_length=200, null=True, blank=True)
    order_date = models.CharField(max_length=200, null=True, blank=True)
    di_number = models.CharField(max_length=200, null=True, blank=True)
    di_date = models.CharField(max_length=200, null=True, blank=True)
    xmr_snos = models.CharField(max_length=200, null=True, blank=True)
    send_to_lab = models.CharField(max_length=200, null=True, blank=True)
    letter_no = models.CharField(max_length=200, null=True, blank=True)
    date_within = models.CharField(max_length=200, null=True, blank=True)
    issue_auth = models.CharField(max_length=200, null=True, blank=True)
    inspectioner_sign = models.CharField(max_length=200, null=True, blank=True)
    receiver_sign = models.CharField(max_length=200, null=True, blank=True) 
    gatekeeper_sign = models.CharField(max_length=200, null=True, blank=True)
    trf_generated = models.IntegerField(blank=True, null=True, default=0)
    discom_name_radio = models.CharField(max_length=200, null=True, blank=True)
    nabl_name_sub_radio = models.CharField(max_length=200, null=True, blank=True)
    gatepassAreaStore_file = models.FileField(upload_to='Gatepass/AreaStore/', blank=True, null=True)
    gatepass_generated = models.IntegerField(blank=True, null=True, default=0)
    DispatcherNameOfEntity = models.CharField(max_length=500, null=True, blank=True)
    LoaOrderNo = models.CharField(max_length=500, null=True, blank=True)
    NameOfItem = models.CharField(max_length=500, null=True, blank=True)
    LoaOrderDate = models.DateField(null=True, blank=True)
    DescriptionOfItem = models.CharField(max_length=500, null=True, blank=True)
    ManufacturerName = models.CharField(max_length=500, null=True, blank=True)
    VehicleNumber = models.CharField(max_length=500, null=True, blank=True)
    DINoDate =  models.CharField(max_length=500, null=True, blank=True)
    DriverName =  models.CharField(max_length=500, null=True, blank=True)
    DriverContactNo = models.CharField(max_length=500, null=True, blank=True)
    IssueDate = models.DateField(null=True, blank=True)
    IssuedTo = models.CharField(max_length=500, null=True, blank=True)
    VerifiedBy = models.CharField(max_length=500, null=True, blank=True)
    Gatekeeper = models.CharField(max_length=500, null=True, blank=True)
    IssuingAuthority = models.CharField(max_length=500, null=True, blank=True)
    VerifiedByDesignation = models.CharField(max_length=500, null=True, blank=True)
    GatekeeperDesignation = models.CharField(max_length=500, null=True, blank=True)
    IssuingAuthorityDesignation = models.CharField(max_length=500, null=True, blank=True)
    ReceiverNameOfEntity = models.CharField(max_length=500, null=True, blank=True)
    ReceiverContactPerson = models.CharField(max_length=500, null=True, blank=True)
    ReceiverDetails = models.CharField(max_length=500, null=True, blank=True)
    ReceiverContact = models.CharField(max_length=500, null=True, blank=True)
    User = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Zone = models.CharField(max_length=500, null=True, blank=True)
    roid = models.IntegerField(blank=True, null=True, default=0)
    login_number = models.CharField(max_length=500, null=True, blank=True)
    AllSampleReportSubmited = models.IntegerField(blank=True, null=True, default=0)
    SomeSamplePhyRejected = models.IntegerField(blank=True, null=True, default=0)
    SendMatToNabl = models.IntegerField(blank=True, null=True, default=0)
    def __int__(self):
        return self.id


class Add_material_nabl_outward(models.Model):
    DispatcherNameOfEntity = models.CharField(max_length=500, null=True, blank=True)
    LoaOrderNo = models.CharField(max_length=500, null=True, blank=True)
    NameOfItem = models.CharField(max_length=500, null=True, blank=True)
    LoaOrderDate = models.DateField(null=True, blank=True)
    DescriptionOfItem = models.CharField(max_length=500, null=True, blank=True)
    ManufacturerName = models.CharField(max_length=500, null=True, blank=True)
    VehicleNumber = models.CharField(max_length=500, null=True, blank=True)
    DINoDate =  models.CharField(max_length=500, null=True, blank=True)
    DriverName =  models.CharField(max_length=500, null=True, blank=True)
    DriverContactNo = models.CharField(max_length=500, null=True, blank=True)
    IssueDate = models.DateField(null=True, blank=True)
    IssuedTo = models.CharField(max_length=500, null=True, blank=True)
    VerifiedBy = models.CharField(max_length=500, null=True, blank=True)
    Gatekeeper = models.CharField(max_length=500, null=True, blank=True)
    IssuingAuthority = models.CharField(max_length=500, null=True, blank=True)
    VerifiedByDesignation = models.CharField(max_length=500, null=True, blank=True)
    GatekeeperDesignation = models.CharField(max_length=500, null=True, blank=True)
    IssuingAuthorityDesignation = models.CharField(max_length=500, null=True, blank=True)
    ReceiverNameOfEntity = models.CharField(max_length=500, null=True, blank=True)
    ReceiverContactPerson = models.CharField(max_length=500, null=True, blank=True)
    ReceiverDetails = models.CharField(max_length=500, null=True, blank=True)
    ReceiverContact = models.CharField(max_length=500, null=True, blank=True)
    UserOutward = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Zone = models.CharField(max_length=500, null=True, blank=True)
    roid = models.IntegerField(blank=True, null=True, default=0)
    login_number = models.CharField(max_length=500, null=True, blank=True)
    gatepassAreaStoreOutward_file = models.FileField(upload_to='Gatepass/NABL/', blank=True, null=True)
    gatepassOutward_generated = models.IntegerField(blank=True, null=True, default=0)


class teachincal_officer_table(models.Model):
    officer_id = models.AutoField(primary_key=True)
    officer_name = models.CharField(max_length=200, default="")


class sample_code_table(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    TRF_Id = models.CharField(max_length=15, null=True, blank=True)
    ro_id = models.IntegerField(blank=True, default=0)
    # gatepass_id = models.IntegerField(blank=True, default=0)
    outward_gatepass_id = models.IntegerField(blank=True, default=0)
    material_serial_number = models.CharField(max_length=200, null=True, blank=True)
    sample_code = models.CharField(max_length=200, null=True, default="", blank=True )
    officer_id = models.CharField(max_length=200, null=True, default="", blank=True)
    date = models.CharField(max_length=200, null=True, default="", blank=True)
    rejected_sample_code = models.CharField(max_length=200, null=True, default="", blank=True)
    rejection_yes_no = models.CharField(max_length=200, null=True, default="", blank=True)
    rejected_by_officer = models.ForeignKey(teachincal_officer_table, on_delete=models.CASCADE, null=True, blank=True)
    rejection_remark = models.CharField(max_length=200, null=True, default="", blank=True)
    rejected_date = models.CharField(max_length=200, null=True, default="", blank=True)
    rejected_vehicle_number = models.CharField(max_length=200, null=True, default="", blank=True)
    is_rejected = models.IntegerField(blank=True, null=True, default=0)
    phy_rejected = models.IntegerField(blank=True, null=True, default=0)
    sent_to_phy_replaced = models.IntegerField(blank=True, null=True, default=0)
    outward_pass = models.IntegerField(blank=True, null=True, default=0)
    outward_driver_name = models.CharField(max_length=200, null=True, default="", blank=True)
    outward_vehicle_number = models.CharField(max_length=200, null=True, default="", blank=True)
    outward_driver_mobile = models.CharField(max_length=15, null=True, blank=True)
    outward_date = models.DateField(null=True, blank=True)
    result_pass = models.IntegerField(blank=True, null=True)
    phy_accepted = models.IntegerField(blank=True, null=True, default=0)
    material_name = models.CharField(max_length=200, null=True, blank=True)
    material_rating = models.CharField(max_length=200, null=True, default="", blank=True)
    company_name = models.CharField(max_length=200, null=True, default="", blank=True)
    gatepass_Submitted_by = models.CharField(max_length=200, null=True, default="", blank=True)
    Test_Request_Form_submitted_by = models.CharField(max_length=200, null=True, default="", blank=True)
    XMRList = models.CharField(max_length=200, null=True, blank=True)
    CapacityList = models.CharField(max_length=200, null=True, blank=True)
    TypeList = models.CharField(max_length=200, null=True, blank=True)
    RemarkList = models.CharField(max_length=200, null=True, blank=True)
    Gatepass = models.ForeignKey(Add_material_nabl, on_delete=models.CASCADE, null=True, blank=True)
    sampleCode_report = models.FileField(upload_to='NABL_Report/', blank=True, null=True)
    outward_generated = models.IntegerField(null=True, blank=True, default=0)
    GatepassOutward = models.ForeignKey(Add_material_nabl_outward, on_delete=models.CASCADE, null=True, blank=True)
    FinalRemark = models.CharField(max_length=500, null=True, blank=True)


class Factory_Inspection_Info(models.Model):
    vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    counter = models.IntegerField(blank=True, default=0)
    assign_date = models.DateField(null=True, blank=True)
    execution_date = models.DateField(null=True, blank=True)
    perform_date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    deny_reason = models.CharField(max_length=500, blank=True, default="")
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    user_zone = models.CharField(max_length=15, null=True, blank=True)
    lattitude = models.CharField(max_length=15, null=True, blank=True)
    longtitude = models.CharField(max_length=15, null=True, blank=True)
    assigned_by =  models.CharField(max_length=50, null=True, blank=True)


# class RCA_Factory_Inspection_Info(models.Model):
    # vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    # officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    # counter = models.IntegerField(blank=True, default=0)
    # assign_date = models.DateField(null=True, blank=True)
    # execution_date = models.DateField(null=True, blank=True)
    # perform_date = models.DateField(null=True, blank=True)
    # Status = models.IntegerField(blank=True, null=True, default=0)
    # deny_reason = models.CharField(max_length=500, blank=True, default="")
    # Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    # Is_Active = models.IntegerField(null=True, blank=True, default=0)
    # Created_At = models.DateTimeField(auto_now_add=True, null=True)
    # Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    # user_zone = models.CharField(max_length=15, null=True, blank=True)


class User_Registration_Check_Status(models.Model):
    id = models.AutoField(primary_key=True)
    User = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    page_1 = models.IntegerField(blank=True, null=True, default=0)
    page_2 = models.IntegerField(blank=True, null=True, default=0)
    page_3 = models.IntegerField(blank=True, null=True, default=0)
    page_4 = models.IntegerField(blank=True, null=True, default=0)
    page_5 = models.IntegerField(blank=True, null=True, default=0)
    page_6 = models.IntegerField(blank=True, null=True, default=0)
    page_7 = models.IntegerField(blank=True, null=True, default=0)
    page_8 = models.IntegerField(blank=True, null=True, default=0)
    page_9 = models.IntegerField(blank=True, null=True, default=0)
    page_10 = models.IntegerField(blank=True, null=True, default=0)
    page_11 = models.IntegerField(blank=True, null=True, default=0)
    page_12 = models.IntegerField(blank=True, null=True, default=0)
    page_13 = models.IntegerField(blank=True, null=True, default=0)
    page_14 = models.IntegerField(blank=True, null=True, default=0)
    page_15 = models.IntegerField(blank=True, null=True, default=0)
    page_16 = models.IntegerField(blank=True, null=True, default=0)


# ----------lokendra


class Material_Inspection_Info(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    di = models.ForeignKey(VendorDispatchInfo, on_delete=models.CASCADE, null=True, blank=True)
    counter = models.IntegerField(blank=True, default=0)
    assign_date = models.DateField(null=True, blank=True)
    execution_date = models.DateField(null=True, blank=True)
    perform_date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    deny_reason = models.CharField(max_length=500, blank=True, default="")
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)


class Add_material_rca(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    TRF_Id = models.CharField(max_length=15, null=True, blank=True)
    Vehicle_number = models.CharField(max_length=200, null=True, blank=True)
    Driver_name = models.CharField(max_length=200, null=True, blank=True)
    Date = models.CharField(max_length=200, null=True, blank=True)
    Submitted_by = models.CharField(max_length=200, null=True, blank=True)
    Test_Request_Form_by = models.CharField(max_length=200, null=True, blank=True)
    select_material = models.CharField(max_length=200, null=True, blank=True)
    select_specification = models.CharField(max_length=200, null=True, blank=True)
    material_number_list = models.CharField(max_length=200, null=True, blank=True)
    Allot_no = models.CharField(max_length=200, null=True, blank=True)
    Material_id = models.CharField(max_length=200, null=True, blank=True)
    Start_date = models.CharField(max_length=200, null=True, blank=True)
    End_Date = models.CharField(max_length=200, null=True, blank=True)
    sample_received = models.IntegerField(blank=True, null=True, default=0)
    job_order_complete = models.IntegerField(blank=True, null=True, default=0)
    emp_name = models.CharField(max_length=200, null=True, blank=True)
    Reject = models.IntegerField(blank=True, null=True, default=0)
    Reject_Remark = models.CharField(max_length=200, null=True, blank=True)
    outpass_date = models.CharField(max_length=200, null=True, blank=True)
    outpass_driver_name = models.CharField(max_length=200, null=True, blank=True)
    outpass_generate_complete = models.IntegerField(blank=True, null=True, default=0)
    outpass_Vehicle_number = models.CharField(max_length=200, null=True, blank=True)

    def _str_(self):
        return self.TRF_Id


class teachincal_officer_table_rca(models.Model):
    officer_id = models.AutoField(primary_key=True)
    officer_name = models.CharField(max_length=200, default="")


class sample_code_table_rca(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    TRF_Id = models.CharField(max_length=15, null=True, blank=True)
    material_serial_number = models.CharField(max_length=200, default="")
    sample_code = models.CharField(max_length=200, default="")
    officer_id = models.CharField(max_length=200, default="")
    date = models.CharField(max_length=200, default="")
    rejected_sample_code = models.CharField(max_length=200, default="")
    rejection_yes_no = models.CharField(max_length=200, default="")
    # rejected_by_officer = models.CharField(max_length=200, default="")
    rejected_by_officer = models.ForeignKey(teachincal_officer_table, on_delete=models.CASCADE, null=True, blank=True)
    rejection_remark = models.CharField(max_length=200, default="")
    rejected_date = models.CharField(max_length=200, default="")
    rejected_vehicle_number = models.CharField(max_length=200, default="")
    is_rejected = models.IntegerField(blank=True, null=True, default=0)


class certificate_details(models.Model):
    cert_id = models.AutoField(primary_key=True)
    User_Id = models.CharField(max_length=500, default="")
    Authorised_person_E = models.CharField(max_length=200, null=True, blank=True, default="")
    company_name = models.CharField(max_length=200, default="")
    Company_add_1 = models.CharField(max_length=200, default="")
    Company_add_2 = models.CharField(max_length=200, default="")
    Company_dist = models.CharField(max_length=200, default="")
    Company_state = models.CharField(max_length=200, default="")
    Company_pin_code = models.CharField(max_length=200, default="")
    no = models.CharField(max_length=200, default="") # Registration number
    User_type = models.CharField(max_length=200, default="") #vendor, nabl, tkc
    vmaterial = models.CharField(max_length=15000, default="", null=True, blank=True) # materials
    day = models.CharField(max_length=100, null=True, blank=True)
    valid_upto = models.CharField(max_length=100, null=True, blank=True)
    employ_name = models.CharField(max_length=200, default="", null=True, blank=True) #Officer_name
    designation = models.CharField(max_length=200, default="", null=True, blank=True) #Officer Designation
    current_time = models.CharField(max_length=200, default="", null=True, blank=True)
    tkc_class_contractor = models.CharField(max_length=200, default="", null=True, blank=True)
    electic_liecense_date = models.CharField(max_length=200, default="", null=True, blank=True)
    User_Zone = models.CharField(max_length=200, default="", null=True, blank=True) # CZ, WZ, EZ
    nabl_cert_exp = models.CharField(max_length=100, null=True, blank=True)
    nabl_cert_number = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='certificate/', blank=True, null=True)
    nabl_accredited_issue = models.DateField(null=True, blank=True)
    nabl_accredited_expiry = models.DateField(null=True, blank=True)


class Sample_Document(models.Model):
    file_name = models.CharField(max_length=400, null=True, blank=True)
    image = models.FileField(upload_to='sample', null=True, blank=True)


class Field_Inspection_Info(models.Model):
    contractor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    counter = models.IntegerField(blank=True, default=0)
    assign_date = models.DateField(null=True, blank=True)
    execution_date = models.DateField(null=True, blank=True)
    perform_date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    deny_reason = models.CharField(max_length=500, blank=True, default="")
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)




class Exam_Data(models.Model):
    user = models.CharField(max_length=500, blank=True, default="")
    score = models.CharField(max_length=500, blank=True, default="")
    gender = models.CharField(max_length=500, blank=True, default="")
    category = models.CharField(max_length=500, blank=True, default="")
    age = models.CharField(max_length=500, blank=True, default="")
    marks = models.CharField(max_length=500, blank=True, default="")
    select = models.CharField(max_length=500, blank=True, default="")
    select_category = models.CharField(max_length=500, blank=True, default="")



class Sampling_Info(models.Model):
    # use for percentage = 1 and number 0
    # Type = (
    #     ("O", "Number"),
    #     ("1", "Percentage"))
    sample_type = models.IntegerField(null=True, blank=True, default=0)
    lot_size_min = models.IntegerField(null=True, blank=True, default=0)
    lot_size_max = models.IntegerField(null=True, blank=True, default=0)
    sample_unit = models.IntegerField(null=True, blank=True, default=0)
    sample_percentage = models.IntegerField(null=True, blank=True, default=0)
    acceptable_unit = models.IntegerField(null=True, blank=True, default=0)
    acceptable_percentage = models.IntegerField(null=True, blank=True, default=0)
    permissible_unit = models.IntegerField(null=True, blank=True, default=0)
    permissible_percentage = models.IntegerField(null=True, blank=True, default=0)
    rejection_unit = models.IntegerField(null=True, blank=True, default=0)
    rejection_percentage = models.IntegerField(null=True, blank=True, default=0)
    # for failure re sampling
    resampling_acceptable_unit = models.IntegerField(null=True, blank=True, default=0)
    resampling_acceptable_percentage = models.IntegerField(null=True, blank=True, default=0)
    resampling_rejection_unit = models.IntegerField(null=True, blank=True, default=0)
    resampling_rejection_percentage = models.IntegerField(null=True, blank=True, default=0)
    status = models.IntegerField(null=True, blank=True, default=0)
    created_by = models.CharField(max_length=300, null=True, blank=True)
    name_of_material = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=300, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)


class product_sampling(models.Model):
    item_code = models.CharField(max_length=500, blank=True, default="")
    sampling = models.ForeignKey(Sampling_Info, on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=0)
    created_by = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.CharField(max_length=300, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    item_code_description = models.CharField(max_length=2500, blank=True, default="")
    item_code_ez = models.CharField(max_length=500, blank=True, default="")
    item_code_wz = models.CharField(max_length=500, blank=True, default="")
    
class Factory_Inspection_Info_history(models.Model):
    vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    assign_date = models.DateField(null=True, blank=True)
    execution_date = models.DateField(null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    user_zone = models.CharField(max_length=15, null=True, blank=True)
    assigned_by =  models.CharField(max_length=50, null=True, blank=True)
    cancel_remark=models.CharField(max_length=500,null=True,blank=True) 







class Vendor_Material_Master(models.Model):
    Material_Id = models.AutoField(primary_key=True)
    Material_Name = models.CharField(max_length=200)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200, null=True)
    Status = models.IntegerField(blank=True, default=0, null=True)


class Nabl_Is_Master(models.Model):
    Is_Id = models.AutoField(primary_key=True)
    Material = models.ForeignKey(Vendor_Material_Master, on_delete=models.PROTECT)
    Material_Name = models.CharField(max_length=200)
    IS_Name = models.CharField(max_length=200)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200, null=True)
    Status = models.IntegerField(blank=True, default=0, null=True)


class Vendor_Material_Specification_Master(models.Model):
    Material_Specification_Id = models.AutoField(primary_key=True)
    Material = models.ForeignKey(Vendor_Material_Master, on_delete=models.PROTECT)
    Is = models.ForeignKey(Nabl_Is_Master, on_delete=models.PROTECT)
    Material_Item_Code = models.CharField(max_length=200)
    Material_Specification_Name = models.CharField(max_length=200)
    Material_Specification_Certificate_Name = models.CharField(max_length=200)
    Material_Unit_Name= models.CharField(max_length=200)
    Test = models.IntegerField(blank=True, default=0, null=True)
    Status = models.IntegerField(blank=True, default=0, null=True)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200, null=True)
    Material_Type = models.CharField(max_length=200)
    Material_Item_Code_WZ = models.CharField(max_length=30, null=True)
    Material_Item_Code_EZ = models.CharField(max_length=30, null=True)


class Nabl_Acceptance_Test_Master(models.Model):
    Acceptance_Test_Id = models.AutoField(primary_key=True)
    Name_Of_Acceptance_Test = models.CharField(max_length=200)
    IS_Name =  models.CharField(max_length=200)
    Is = models.ForeignKey(Nabl_Is_Master, on_delete=models.PROTECT)
    Status = models.IntegerField(blank=True, default=0, null=True)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200, null=True)


class Material_Specification(models.Model):
    Material_Specification_Id = models.AutoField(primary_key=True)
    # Material_Id = models.ForeignKey(Material_Master, on_delete=models.PROTECT)
    Material_Code = models.CharField(max_length=200)
    Material_Specification = models.CharField(max_length=200)
    Unit = models.CharField(max_length=200)
    Test = models.IntegerField(blank=True, default=0, null=True)
    Status = models.IntegerField(blank=True, default=0, null=True)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200, null=True)
    Material_Type = models.CharField(max_length=200)
    
from rca.models import *
from rca.models import Rca_User_Registration

class RCA_Factory_Inspection_Info(models.Model):
    vendor = models.ForeignKey(Rca_User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    counter = models.IntegerField(blank=True, default=0)
    assign_date = models.DateField(null=True, blank=True)
    execution_date = models.DateField(null=True, blank=True)
    perform_date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    deny_reason = models.CharField(max_length=500, blank=True, default="")
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)

# class PDI_Inspection_Info(models.Model):
#     officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
#     Material = models.ForeignKey('fqp.Offer_Material', on_delete=models.CASCADE, null=True, blank=True)
#     counter = models.IntegerField(blank=True, default=0)
#     assign_date = models.DateField(null=True, blank=True)
#     execution_date = models.DateField(null=True, blank=True)
#     perform_date = models.DateField(null=True, blank=True)
#     Status = models.IntegerField(blank=True, null=True, default=0)
#     deny_reason = models.CharField(max_length=500, blank=True, default="")
#     Is_Admin = models.IntegerField(null=True, blank=True, default=0)
#     Is_Active = models.IntegerField(null=True, blank=True, default=0)
#     Created_At = models.DateTimeField(auto_now_add=True, null=True)
#     Updated_At = models.DateTimeField(auto_now_add=True, null=True)
#     user_zone = models.CharField(max_length=15, null=True, blank=True)
    
class Payment_Mode_Master(models.Model):
    Payment_Mode = models.CharField(max_length=100, null=True, blank=True)
    Payment_Mode_Description = models.CharField(max_length=200, null=True, blank=True)
    Payment_Mode_Priority = models.IntegerField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)

    def _str_(self):
        return self.Payment_Mode    
    
    

class UOM_Master(models.Model):
    UOM = models.CharField(max_length=100, null=True, blank=True)
    UOM_Description = models.CharField(max_length=200, null=True, blank=True)
    UOM_Priority = models.IntegerField(null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)

    def _str_(self):
        return self.UOM    
        
        
class message_template_log(models.Model):
    template_id = models.CharField(max_length=500, blank=True, default="")
    date = models.DateTimeField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True, default="")
    message = models.CharField(max_length=500, blank=True, default="")

class PDI_Inspection_Info(models.Model):
    officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    Material = models.ForeignKey('tkc.offer_material_site_stores', on_delete=models.CASCADE, null=True, blank=True)
    wo=models.ForeignKey('fqp.TKCWoInfo', on_delete=models.CASCADE, null=True, blank=True)
    subject=models.CharField(max_length=500, blank=True, default="", null=True)
    material_name=models.CharField(max_length=500, blank=True, default="", null=True)
    item_code=models.CharField(max_length=500, blank=True, default="", null=True)    
    offer_no=models.CharField(max_length=500, blank=True, default="")
    offer_date=models.CharField(null=True, blank=True, max_length=500)
    tkc_name=models.CharField(max_length=500, blank=True, default="", null=True)
    tkc_address=models.CharField(max_length=500, blank=True, default="", null=True)
    vendor_name=models.CharField(max_length=500, blank=True, default="", null=True)
    vendor_address=models.CharField(max_length=500, blank=True, default="", null=True)
    counter = models.IntegerField(blank=True, default=0, null=True)
    assign_date = models.DateField(null=True, blank=True)
    execution_date = models.DateField(null=True, blank=True)
    perform_date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    deny_reason = models.CharField(max_length=500, blank=True, default="", null=True)
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    user_zone = models.CharField(max_length=15, null=True, blank=True)
    inspection_date = models.CharField(max_length=150, null=True, blank=True)  
    another_officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True,related_name = 'another_officer')  
    pdi_report=models.FileField(upload_to='TKC/FQP/tkc_offer_material_docs/', null=True, blank=True)
    letter_report=models.FileField(upload_to='TKC/FQP/tkc_offer_material_docs/', null=True, blank=True)
    quantity=models.FloatField(blank=True, default=0)
    pdi_report_url=models.CharField(max_length=500, blank=True, default="", null=True)
    propose_fakecall=models.BooleanField(blank=True,default=False)
    fake_call_remark=models.TextField(blank=True, default="", null=True)
    fake_call_letter=models.FileField(upload_to='TKC/FQP/tkc_offer_material_docs/', null=True, blank=True)


class pdi_other_officer(models.Model):
    offer_no=models.CharField(max_length=500, blank=True, default="")
    officer_name=models.CharField(max_length=500, blank=True, default="")
    officer_contact=models.CharField(max_length=500, blank=True, default="")
    officer_from=models.CharField(max_length=500, blank=True, default="")
    officer_designation=models.CharField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    
class Tier1_Inspection_Info(models.Model):
    officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    Estimate = models.ForeignKey('fqp.TKCWoInfo_Estimate', on_delete=models.CASCADE, null=True, blank=True)
    counter = models.IntegerField(blank=True, default=0)
    assign_date = models.DateField(null=True, blank=True)
    execution_date = models.DateField(null=True, blank=True)
    perform_date = models.DateField(null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    deny_reason = models.CharField(max_length=500, blank=True, default="")
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    user_zone = models.CharField(max_length=15, null=True, blank=True)

class Tier_1_Inspection_Representive_data(models.Model):
    task = models.ForeignKey(Tier1_Inspection_Info, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=150)
    image_1 = models.ImageField(upload_to='main/tier1_inpection/representative')
    representative_from = models.CharField(max_length=200)
    remark = models.CharField(max_length=5000,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name


class Pdi_Inspection_Representive_data(models.Model):
    task = models.ForeignKey(PDI_Inspection_Info, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=15)
    designation = models.CharField(max_length=150)
    image_1 = models.ImageField(upload_to='main/pdi_inpection/representative')
    representative_from = models.CharField(max_length=200)
    remark = models.CharField(max_length=5000,blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
    
    
class blacklistedSaved(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    CompanyName_E = models.CharField(max_length=100, null=True, blank=True)
    blacklisted_type = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField(max_length=15, null=True, blank=True)
    recommended_by = models.CharField(max_length=100, null=True, blank=True)
    recommended_order = models.FileField(upload_to='officer/image', null=True, blank=True)
    user_type = models.CharField(max_length=10, null=True, blank=True)


# ------------------ shubham code end here ------------------------
class reject_and_approve_summary(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField(max_length=15, null=True, blank=True)
    officer = models.CharField(max_length=50, null=True, blank=True)
    officer_designation = models.CharField(max_length=50, null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    document = models.FileField(upload_to='documents/tkc', null=True, blank=True)
    document_name = models.CharField(max_length=200, null=True, blank=True)





# ------------------ shubham tripathi code start from here  ------------------------
class InvoiceType(models.Model):
    invoice_type = models.CharField(max_length=250, null=True, blank=True)
    status = models.IntegerField(blank=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.invoice_type

class Invoice(models.Model):
    invoicetype = models.ForeignKey(InvoiceType,on_delete=models.SET_NULL,null=True, blank=True,related_name="invoicetype_data")
    purchase_order = models.ForeignKey('po.Purchase_Order',on_delete=models.SET_NULL,null=True, blank=True,related_name="purchase_order_data")
    assign_officer = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True,related_name="officer_data")
    user = models.ForeignKey(User_Registration,on_delete=models.SET_NULL,null=True, blank=True,related_name="user_data")
    work_order = models.ForeignKey('fqp.TKCWoInfo',on_delete=models.SET_NULL,null=True, blank=True,related_name="work_order_data")

    invoice_number = models.CharField(max_length=50, blank=False, null=False)
    invoice_amount_withought_taxes = models.FloatField(blank=True, default=0, null=True)
    invoice_amount_sgst = models.FloatField(blank=True, default=0, null=True)
    invoice_amount_cgst = models.FloatField(blank=True, default=0, null=True)
    total_invoice_amount = models.FloatField(blank=True, default=0, null=True)
    invoice_deducted_amount = models.FloatField(blank=True, default=0, null=True)
    invoice_approved_amount = models.FloatField(blank=True, default=0, null=True)
    bg_document = models.FileField(upload_to="po_invoice/bg_document", null=True, blank=True)
    bg_acceptance_letter = models.FileField(upload_to="po_invoice/bg_acceptance",blank=True, null=True)
    invoice_submission_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    supporting_document_name = models.CharField(max_length=250, blank=True, null=True)
    supporting_document = models.FileField(upload_to="po_invoice/supporting_doc",blank=True, null=True)
    order_type = models.CharField(max_length=50, blank=False, null=False,default="PurchaseOrder")
    invoice_pdf = models.FileField(upload_to="po_invoice/document", blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    
    cgm_remark = models.TextField(blank=True, null=True)
    cgm_document = models.FileField(upload_to="invoice/cgm", blank=True, null=True)
    cgm_status = models.IntegerField(blank=True, null=True, default=0)
    cgm_action_date = models.DateTimeField(auto_now_add=True, null=True)

    gm_remark = models.TextField(blank=True, null=True)
    gm_document = models.FileField(upload_to="invoice/gm", blank=True, null=True)
    gm_status = models.IntegerField(blank=True, null=True, default=0)
    gm_action_date = models.DateTimeField(auto_now_add=True, null=True)

    cfo_remark = models.TextField(blank=True, null=True)
    cfo_document = models.FileField(upload_to="invoice/cfo", blank=True, null=True)
    cfo_status = models.IntegerField(blank=True, null=True, default=0)
    cfo_action_date = models.DateTimeField(auto_now_add=True, null=True)

    dgm_cbpu_remark = models.TextField(blank=True, null=True)
    dgm_cbpu_document = models.FileField(upload_to="invoice/dgm_cbpu", blank=True, null=True)
    dgm_cbpu_status = models.IntegerField(blank=True, null=True, default=0)
    dgm_action_date = models.DateTimeField(auto_now_add=True, null=True)

    ao_bills_remark = models.TextField(blank=True, null=True)
    ao_bills_document = models.FileField(upload_to="invoice/ao_bills", blank=True, null=True)
    ao_bills_status = models.IntegerField(blank=True, null=True, default=0)
    ao_bills_action_date = models.DateTimeField(auto_now_add=True, null=True)

    dgm_em_remark = models.TextField(blank=True, null=True)
    dgm_em_document = models.FileField(upload_to="invoice/dgm_em", blank=True, null=True)
    dgm_em_status = models.IntegerField(blank=True, null=True, default=0)
    dgm_em_action_date = models.DateTimeField(auto_now_add=True, null=True)

    rejected_by_officer = models.CharField(max_length=50, blank=True, null=True)
    rejected_by_role = models.CharField(max_length=50, blank=True, null=True)
    rejected_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    # <--------------- Lokesh --------------> live date 24-Aug-2023
    #### gm dashboard fields
    gm_select_officer = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True,related_name='circle_officer_invoice')
    gm_comment = models.TextField(blank=True, null=True)
    gm_file_select =  models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True)
    gm_doc_name = models.TextField(blank=True, null=True)

    ##dgm data to be submitted to GM
    deduct_ld_amount = models.IntegerField(blank=True, null=True, default=0) #done
    deduct_penalty = models.IntegerField(blank=True, null=True, default=0) #done
    deduct_mob_adv = models.IntegerField(blank=True, null=True, default=0) #done
    inv_pass_wto_tax = models.IntegerField(blank=True, null=True, default=0)
    inv_cgst = models.IntegerField(blank=True, null=True, default=0)
    inv_sgst = models.IntegerField(blank=True, null=True, default=0)
    inv_igst = models.IntegerField(blank=True, null=True, default=0)
    inv_total_pass_amt = models.IntegerField(blank=True, null=True, default=0)
    upload_inv_pass_order_amt = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True) #done
    supp_doc_by_dgmtogm = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True)
    dgm_remark = models.TextField(blank=True, null=True)
    dgm_submit_to_gm = models.IntegerField(blank=True, null=True, default=0)
    #july 18
    gm_remark_second = models.TextField(blank=True, null=True)
    gm_select_second_officer = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True)
    gm_file_second_select = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True)
    gm_doc_second_name = models.TextField(blank=True, null=True)
    
    ##gm cirlce #Aug 12, 2023
    gm_circle_remark = models.TextField(blank=True, null=True)
    gm_circle_action = models.DateTimeField(null=True, blank=True) 
    doc_by_gm_circle = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True) 
    doc_name_gm_circle = models.TextField(blank=True, null=True) 
    officer_select_by_gm_circle = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True,related_name ="officer_select_by_gm_circle") 
    gm_circle_submit_name = models.TextField(blank=True, null=True)
    gm_circle_action_sec = models.DateTimeField(null=True, blank=True) 
    doc_by_gm_circle_sec = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True) 
    doc_name_gm_circle_sec = models.TextField(blank=True, null=True)
    gm_circle_remark_sec = models.TextField(blank=True, null=True)
    ##dgm cirlce #Aug 12, 2023 
    dgm_circle_remark = models.TextField(blank=True, null=True)
    doc_by_dgm_circle = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True) 
    doc_name_dgm_circle = models.TextField(blank=True, null=True)
    dgm_circle_action = models.DateTimeField(null=True, blank=True)
    # dgm_circle_submit_name = models.TextField(blank=True, null=True)    #ppp
    officer_select_by_dgm_circle = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True,related_name ="officer_select_by_dgm_circle") #right now not in use, may be useful in future
    ##cgm project dashboard   #July 28,2023 
    cgmproject_remark = models.TextField(blank=True, null=True)
    doc_by_cgmproject = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True)
    doc_name_cgmproject = models.TextField(blank=True, null=True)
    officer_select_by_cgmproject = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True,related_name ="officer_select_by_cgmproject")
    ##dgm project dashboard   #Aug 02,2023
    dgmproject_remark = models.TextField(blank=True, null=True)
    doc_by_dgmproject = models.FileField(upload_to="po_invoice/bg_document", blank=True, null=True)
    doc_name_dgmproject = models.TextField(blank=True, null=True)
    ##cfo project dashboard   #Aug 02,2023
    cfoproject_remark = models.TextField(blank=True, null=True)
    cfoproject_action = models.DateTimeField(null=True, blank=True)
    cfoproject_submit_name = models.TextField(blank=True, null=True)
    officer_select_by_cfoproject = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True,related_name ="officer_select_by_cfoproject")
    # tkc_dgmcbpu_current_invoice_list dashboard #Aug 03,2023 
    dgmcbpu_remark = models.TextField(blank=True, null=True)
    dgmcbpu_action = models.DateTimeField(null=True, blank=True)
    # dgmcbpu_submit_name = models.TextField(blank=True, null=True)         #ppp
    officer_select_by_dgmcbpu = models.ForeignKey(Officer,on_delete=models.SET_NULL,null=True, blank=True,related_name ="officer_select_by_dgmcbpu")    
    # tkc_aocbpu_current_invoice_list dashboard #Aug 03,2023 
    aocbpu_erp_voucher_number = models.CharField(max_length=50, blank = True, null = True)
    aocbpu_invoice_verfiy_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_invoice_cgst_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_invoice_sgst_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_invoice_igst_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_labour_welfare_cess = models.FloatField(blank=True, null=True, default=0)
    aocbpu_liquidity_damage_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_mob_adv_recovery_amount= models.FloatField(blank=True, null=True, default=0)
    aocbpu_material_adv_recovery_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_recovery_of_intrest_on_advanced = models.FloatField(blank=True, null=True, default=0)
    aocbpu_retention_amount  = models.FloatField(blank=True, null=True, default=0)
    aocbpu_other_recovery_amount  = models.FloatField(blank=True, null=True, default=0)
    aocbpu_miscelleneous_recovery_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_final_net_payable_amount = models.FloatField(blank=True, null=True, default=0)
    aocbpu_remark = models.TextField(blank=True, null=True)
    aocbpu_action = models.DateTimeField(null=True, blank=True)
    # aocbpu_submit_name = models.TextField(blank=True, null=True)      #pppending 
    # tkc_dgmem_current_invoice_list dashboard #Aug 03,2023 
    dgmem_erp_payment_voucher_no = models.CharField(max_length=50, blank = True, null = True)
    dgmem_pfms_no = models.CharField(max_length=50, blank = True, null = True)
    dgmem_utr_no = models.CharField(max_length=50, blank = True, null = True)
    dgmem_remark = models.TextField(blank=True, null=True)
    dgmem_action = models.DateTimeField(null=True, blank=True)
    dgmem_submit_name = models.TextField(blank=True, null=True)
    
        

    #flage for submission # Aug 20,2023
    gm_circle_submit_status = models.IntegerField(blank=True, null=True, default=0)
    dgm_circle_submit_status = models.IntegerField(blank=True, null=True, default=0)
    cgmproject_submit_status =  models.IntegerField(blank=True, null=True, default=0)
    dgmproject_submit_status =  models.IntegerField(blank=True, null=True, default=0)
    cfoproject_submit_status =  models.IntegerField(blank=True, null=True, default=0)
    dgmcbpu_submit_status =  models.IntegerField(blank=True, null=True, default=0)
    aocbpu_submit_status =  models.IntegerField(blank=True, null=True, default=0)
    dgmem_submit_status =  models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.invoice_number



class InvoiceHistory(models.Model):
    invoice = models.ForeignKey(Invoice,on_delete=models.SET_NULL,null=True, blank=True,related_name="invoice_history")
    officer = models.ForeignKey(Officer,on_delete=models.CASCADE,null=True, blank=True)
    role = models.CharField(max_length=50, blank=False, null=False)
    invoice_document = models.FileField(upload_to="po_invoice/history", null=True, blank=True)
    invoice_remark = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=20,blank=True, null=True)
    status = models.IntegerField(blank=True, default=1, null=True)
    action_time = models.DateTimeField(auto_now_add=True, null=True)


# ---------------fqp inspection code start from here--------------------------


class Milestone_Main(models.Model):
    milestone_name= models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    status = models.IntegerField(null=True, blank=True, default=1)
    def __str__(self):
        return self.milestone_name


class Milestone_Main_Category(models.Model):
    milestone_main = models.ForeignKey(Milestone_Main, on_delete=models.CASCADE, null=True, blank=True)
    milestone_category_name= models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    status = models.IntegerField(null=True, blank=True, default=1)
    def __str__(self):
        return self.milestone_category_name


class Milestone_Main_SubCategory(models.Model):
    milestone_main_category = models.ForeignKey(Milestone_Main_Category, on_delete=models.CASCADE, null=True, blank=True)
    milestone_subcategory_name= models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    status = models.IntegerField(null=True, blank=True, default=1)
    def __str__(self):
        return self.milestone_subcategory_name

class Milestone_Main_SubCategory_Data(models.Model):
    milestone_main_subcategory = models.ForeignKey(Milestone_Main_SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    activity_and_operation = models.CharField(max_length=500, null=True, blank=True)
    characteristics = models.CharField(max_length=300, null=True, blank=True)
    class_of_check = models.CharField(max_length=200, null=True, blank=True)
    type_of_check = models.CharField(max_length=200, null=True, blank=True)
    quantum_of_check_contractor = models.CharField(max_length=800, null=True, blank=True)
    quantum_of_check_tpqma = models.CharField(max_length=500, null=True, blank=True)
    reference_document = models.CharField(max_length=500, null=True, blank=True)
    acceptance_norms = models.CharField(max_length=800, null=True, blank=True)
    format_of_record = models.CharField(max_length=800, null=True, blank=True)
    remark = models.CharField(max_length=800, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=1)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    def __str__(self):
        if self.activity_and_operation:
            return self.activity_and_operation
        else:
            return "Activity and operation"

# ------------------ shubham tripati code end here ------------------------


class sitestore_pi_verification(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    zone = models.CharField(max_length=5, null=True, blank=True)

    
class tkc_certificate_details(models.Model):
    cert_id = models.AutoField(primary_key=True)
    User_Id = models.CharField(max_length=500, default="")
    Authorised_person_E = models.CharField(max_length=200, null=True, blank=True, default="")
    company_name = models.CharField(max_length=200, default="")
    Company_add_1 = models.CharField(max_length=200, default="")
    Company_add_2 = models.CharField(max_length=200, default="")
    Company_dist = models.CharField(max_length=200, default="")
    Company_state = models.CharField(max_length=200, default="")
    Company_pin_code = models.CharField(max_length=200, default="")
    no = models.CharField(max_length=200, default="") # Registration number
    User_type = models.CharField(max_length=200, default="") #vendor, nabl, tkc
    vmaterial = models.CharField(max_length=15000, default="", null=True, blank=True) # materials
    day = models.CharField(max_length=100, null=True, blank=True)
    valid_upto = models.CharField(max_length=100, null=True, blank=True)
    employ_name = models.CharField(max_length=200, default="", null=True, blank=True) #Officer_name
    designation = models.CharField(max_length=200, default="", null=True, blank=True) #Officer Designation
    current_time = models.CharField(max_length=200, default="", null=True, blank=True)
    tkc_class_contractor = models.CharField(max_length=200, default="", null=True, blank=True)
    electic_liecense_date = models.CharField(max_length=200, default="", null=True, blank=True)
    User_Zone = models.CharField(max_length=200, default="", null=True, blank=True) # CZ, WZ, EZ
    nabl_cert_exp = models.CharField(max_length=100, null=True, blank=True)
    nabl_cert_number = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='certificate/', blank=True, null=True)
    nabl_accredited_issue = models.DateField(null=True, blank=True)
    nabl_accredited_expiry = models.DateField(null=True, blank=True)
    new_tkc = models.IntegerField(blank=True, default=0)    
    
    
class nistha_nabl_lab_test_material_master(models.Model):
    Material = models.CharField(max_length=500, null=True, blank=True)
    Material_code = models.CharField(max_length=50, null=True, blank=True)

