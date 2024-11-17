from django.db import models


# Create your models here.
class TKC_Document(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Types_of_Docs = models.CharField(max_length=100, null=True, blank=True)
    Issued_office_Name = models.CharField(max_length=15, null=True, blank=True)
    Document_Number = models.CharField(max_length=15, null=True, blank=True)
    Ddocfile = models.FileField(upload_to='documents/tkc/work_data')
    Doc_issue_date = models.DateTimeField(null=True, blank=True)
    Doc_expiry_date = models.DateField(null=True, blank=True)
    # doc for approval in work use 1 and finance use 2
    Approval_doc = models.IntegerField(blank=True, default=0, null=True)
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    CGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    CGM_remark = models.CharField(max_length=100, null=True, blank=True)
    CGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    CGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(null=True, blank=True)
    Updated_Date = models.DateTimeField(null=True, blank=True)
    Status = models.IntegerField(blank=True, default=0, null=True)
    complete_data = models.IntegerField(blank=True, default=0, null=True)
    new_data = models.IntegerField(blank=True, default=0, null=True)


class TKC_Factory_Details(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Documnet_id = models.CharField(max_length=15, null=True, blank=True)
    Factory_License = models.CharField(max_length=15, null=True, blank=True)
    Area_of_land = models.IntegerField(blank=True, null=True, default=0)
    Area_built_up = models.IntegerField(blank=True, null=True, default=0)
    No_of_Shifts = models.IntegerField(blank=True, null=True, default=0)
    Yearly_Production = models.IntegerField(blank=True, null=True, default=0)
    Outsourced_person = models.IntegerField(blank=True, null=True, default=0)
    Production_Capacity = models.IntegerField(blank=True, null=True, default=0)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)


class TKC_Turnover(models.Model):
    user_id = models.CharField(max_length=45, null=True, blank=True)
    Financial_year = models.CharField(max_length=45, null=True, blank=True)
    Amount = models.CharField(max_length=55, null=True, blank=True)
    # Type use key Turnover 1 And for return 2
    Status = models.IntegerField(blank=True, default=0)
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    CGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    CGM_remark = models.CharField(max_length=100, null=True, blank=True)
    CGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    CGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)
    complete_data = models.IntegerField(blank=True, default=0, null=True)


class TKC_BalanceSheet(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Financial_year = models.CharField(max_length=15, null=True, blank=True)
    Amount = models.CharField(max_length=15, null=True, blank=True)
    Balance_Sheet = models.FileField(upload_to='documents/vendor/Balance_Sheet')
    # Type use key Balance_Sheet 1 And for Loss_Sheet 2
    Status = models.IntegerField(blank=True, default=0)
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    CGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    CGM_remark = models.CharField(max_length=100, null=True, blank=True)
    CGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    CGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(blank=True, default=0)
    complete_data = models.IntegerField(blank=True, default=0, null=True)
    final_complete_data = models.IntegerField(blank=True, default=0, null=True)


class TKC_Payment(models.Model):
    Name = models.CharField(max_length=15, null=True, blank=True)
    code = models.IntegerField(blank=True, default=0)
    payment = models.IntegerField(blank=True, default=0)
