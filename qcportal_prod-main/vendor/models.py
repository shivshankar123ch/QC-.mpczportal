from django.db import models
import uuid

from main.models import *
# Create your models here.
class Vendor_Document(models.Model):
    Vendor_Document_Id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Types_of_Docs = models.CharField(max_length=100, null=True, blank=True)
    Issued_office_Name = models.CharField(max_length=50, null=True, blank=True)
    Document_Number = models.CharField(max_length=15, null=True, blank=True)
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


class Vendor_Factory_Details(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Documnet_id = models.CharField(max_length=15, null=True, blank=True)
    Factory_License = models.CharField(max_length=15, null=True, blank=True)
    Area_of_land = models.IntegerField(blank=True, null=True, default=0)
    Area_built_up = models.IntegerField(blank=True, null=True, default=0)
    No_of_Shifts = models.IntegerField(blank=True, null=True, default=0)
    Yearly_Production = models.IntegerField(blank=True, null=True, default=0)
    Outsourced_person = models.IntegerField(blank=True, null=True, default=0)
    Production_Capacity = models.IntegerField(blank=True, null=True, default=0)
    lat = models.CharField(max_length=15, null=True, blank=True)
    log = models.CharField(max_length=15, null=True, blank=True)
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    DGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    DGM_remark = models.CharField(max_length=100, null=True, blank=True)
    DGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    DGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)
    Ddocfile = models.FileField(upload_to='documents/vendor/work_data', default=0, null=True)
    No_of_employee = models.IntegerField(blank=True, default=0)


class Vendor_Factory_image(models.Model):
    Factory = models.ForeignKey(Vendor_Factory_Details, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Image = models.FileField(upload_to='documents/vendor/Factory')


class Vendor_Turnover(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Financial_year = models.CharField(max_length=15, null=True, blank=True)
    Amount = models.IntegerField(blank=True, null=True, default=0)
    # Type use key Turnover 1 And for return 2
    Status = models.IntegerField(blank=True, default=0)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)


class Vendor_BalanceSheet(models.Model):
    Vendor_Document_Id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    document_name = models.CharField(max_length=50, null=True, blank=True)
    Financial_year = models.CharField(max_length=15, null=True, blank=True)
    Balance_Sheet = models.FileField(upload_to='documents/vendor/Balance_Sheet',null=True, blank=True,default='documents/No_Preview.pdf')
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    DGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    DGM_remark = models.CharField(max_length=100, null=True, blank=True)
    DGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    DGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    # Type use key Balance_Sheet 1 And for Loss_Sheet 2
    Status = models.IntegerField(blank=True, default=0)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)

class Vendor_Material_Details(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Material_Name = models.CharField(max_length=100, null=True, blank=True)
    Material_Specification = models.CharField(max_length=200, null=True, blank=True)
    Material_Test_Doc = models.FileField(upload_to='documents/vendor/material')
    Material_GTP_Doc = models.FileField(upload_to='documents/vendor/material')
    Material_Other_Doc = models.FileField(upload_to='documents/vendor/material')
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    DGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    DGM_remark = models.CharField(max_length=100, null=True, blank=True)
    DGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    DGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(default=0)
    item_code = models.CharField(max_length=100, null=True, blank=True)
    new_material = models.IntegerField(blank=True, default=0)
    item_code_ez = models.CharField(max_length=50, null=True, blank=True)
    item_code_wz = models.CharField(max_length=50, null=True, blank=True)
    new_status = models.IntegerField(blank=True, default=0)
    per_month_capacity = models.FloatField(null=True, blank=True, default=None)
    material_unit = models.CharField(max_length=50, null=True, blank=True)
    response_submitted = models.IntegerField(blank=True, default=0)


class Vendor_Technical_Details(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Types_of_Docs = models.CharField(max_length=100, null=True, blank=True)
    Issued_office_Name = models.CharField(max_length=150, null=True, blank=True)
    Document_Number = models.CharField(max_length=150, null=True, blank=True)
    Document_Doc = models.FileField(upload_to='documents/vendor/Technical')
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    DGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    DGM_remark = models.CharField(max_length=100, null=True, blank=True)
    DCM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    DCM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)
    complete_data = models.IntegerField(blank=True, default=0)
    response_submitted = models.IntegerField(blank=True, default=0)


class Vendor_Financial_Details(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=80, null=True, blank=True)
    Docs_Name = models.CharField(max_length=80, null=True, blank=True)
    Docs_Holder_Name = models.CharField(max_length=80, null=True, blank=True)
    Issued_office_Name = models.CharField(max_length=80, null=True, blank=True)
    Document_Number = models.CharField(max_length=80, null=True, blank=True)
    Doc_File = models.FileField(upload_to='documents/vendor/Finance')
    Doc_issue_date = models.DateField(default=None, null=True)
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    DGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    DGM_remark = models.CharField(max_length=100, null=True, blank=True)
    DGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    DGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)
    complete_data = models.IntegerField(blank=True, default=0)
    all_complete_data = models.IntegerField(blank=True, default=0)


class Vendor_fiance_officer(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=80, null=True, blank=True)
    fiance_approve = models.IntegerField(blank=True, default=0)
    remark = models.CharField(max_length=80, null=True, blank=True)


class Add_material(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    select_material = models.CharField(max_length=200, default="")
    select_specification = models.CharField(max_length=200, default="")
    type_test_report = models.ImageField(blank=True, upload_to='Type_Test_Report')
    gtp_and_drawing = models.ImageField(blank=True, upload_to='GTP_and_Drawing')
    others = models.ImageField(blank=True, upload_to='Others')

    emp_name = models.CharField(max_length=200)

    def __str__(self):
        return self.emp_name

    @property
    def type_test_reportURL(self):
        try:
            url = self.type_test_report.url
        except:
            url = ''

        return url

    def gtp_and_drawingURL(self):
        try:
            url = self.gtp_and_drawing.url
        except:
            url = ''

        return url

    def othersURL(self):
        try:
            url = self.others.url
        except:
            url = ''

        return url



class Material_Master(models.Model):
    Material_Id = models.AutoField(primary_key=True)
    Material_Name = models.CharField(max_length=200)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200,null=True)
    Is_Active = models.IntegerField(blank=True, default=0, null=True)
    Material_Type = models.CharField(max_length=200)



class Material_Acceptance_Test_Master(models.Model):
    Acceptance_Test_Id = models.AutoField(primary_key=True)
    Acceptance_Test_Name = models.CharField(max_length=200)
    Is_Active = models.IntegerField(blank=True, default=0, null=True)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200,null=True)

class Material_Specification(models.Model):
    Material_Specification_Id = models.AutoField(primary_key=True)
    Material_Id = models.ForeignKey(Material_Master, on_delete=models.PROTECT)
    Material_Code = models.CharField(max_length=200)
    Material_Specification = models.CharField(max_length=200)
    Unit = models.CharField(max_length=200)
    Is_Active = models.IntegerField(blank=True, default=0, null=True)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200,null=True)

class area_store_officer(models.Model):
    user_name = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=20, null=True, blank=True)



class LeasingPerson(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_id = models.CharField(max_length=200)
    name = models.CharField(max_length=20, null=True, blank=True)
    designation = models.CharField(max_length=20, null=True, blank=True)
    dob = models.DateField(default=None, null=True)
    firm  = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    photo = models.FileField(upload_to='documents/vendor/work_data', default=0, null=True)
    # Created_Date = models.DateField(default=None, null=True)
    # Updated_By = models.CharField(max_length=200)
    # Updated_Date = models.DateField(default=None, null=True)
    # Created_By = models.CharField(max_length=200,null=True)



class Factory_Technical_Details(models.Model):
    vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    consumer_no = models.CharField(max_length=500, null=True, blank=True)
    section_id = models.CharField(max_length=500, null=True, blank=True)
    work_load = models.CharField(max_length=500, null=True, blank=True)
    load_shading = models.CharField(max_length=500, null=True, blank=True)
    dg_rating = models.CharField(max_length=500, null=True, blank=True)
    power_backup = models.CharField(max_length=500, null=True, blank=True)
    power_remark = models.CharField(max_length=500, null=True, blank=True)
    plant_machinery = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    latest_machinery = models.CharField(max_length=500, null=True, blank=True)
    latest_remark = models.CharField(max_length=500, null=True, blank=True)
    manufacturing = models.CharField(max_length=500, null=True, blank=True)
    manufacturing_remark = models.CharField(max_length=500, null=True, blank=True)
    inspection = models.CharField(max_length=500, null=True, blank=True)
    inspection_remark = models.CharField(max_length=500, null=True, blank=True)
    sub_stand = models.CharField(max_length=500, null=True, blank=True)
    sub_stand_remark = models.CharField(max_length=500, null=True, blank=True)
    assistance = models.CharField(max_length=500, null=True, blank=True)
    assistance_remark = models.CharField(max_length=500, null=True, blank=True)
    internal_testing = models.CharField(max_length=500, null=True, blank=True)
    internal_testing_remark = models.CharField(max_length=500, null=True, blank=True)
    details_testing = models.CharField(max_length=500, null=True, blank=True)
    details_testing_remark = models.CharField(max_length=500, null=True, blank=True)


class FI_Appraisal_Details(models.Model):
    vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    experience = models.CharField(max_length=500, null=True, blank=True)
    availability = models.CharField(max_length=500, null=True, blank=True)
    calibration = models.CharField(max_length=500, null=True, blank=True)
    bought = models.CharField(max_length=500, null=True, blank=True)
    inprocess = models.CharField(max_length=500, null=True, blank=True)
    dispatch = models.CharField(max_length=500, null=True, blank=True)
    overall = models.CharField(max_length=500, null=True, blank=True)
    control = models.CharField(max_length=500, null=True, blank=True)
    iso = models.CharField(max_length=500, null=True, blank=True)
    material = models.CharField(max_length=500, null=True, blank=True)
    general = models.CharField(max_length=500, null=True, blank=True)
    packing = models.CharField(max_length=500, null=True, blank=True)
    incharge = models.CharField(max_length=500, null=True, blank=True)
    supervisor = models.CharField(max_length=500, null=True, blank=True)
    controlsystem = models.CharField(max_length=500, null=True, blank=True)
    qualityofplant = models.CharField(max_length=500, null=True, blank=True)
    workshoap = models.CharField(max_length=500, null=True, blank=True)
    sefty = models.CharField(max_length=500, null=True, blank=True)
    store = models.CharField(max_length=500, null=True, blank=True)
    faciality = models.CharField(max_length=500, null=True, blank=True)
    progress = models.CharField(max_length=500, null=True, blank=True)
    overallp = models.CharField(max_length=500, null=True, blank=True)


class Factory_Form_Details(models.Model):
    vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=None, null=True)
    report = models.FileField(upload_to='documents/vendor/work_data', default=0, null=True)
    status = models.IntegerField(blank=True, default=0, null=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    
   
