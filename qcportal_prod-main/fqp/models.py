from django.db import models
from main.models import *
from vendor.models import Vendor_Material_Details
from main.models import User_Registration, BankDetails
from ckeditor.fields import RichTextField
from tkc.models import works_master


# Create your models here.

class TKCWoInfo(models.Model):
    supplier = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Contract_Number = models.CharField(max_length=300, null=True, blank=True)
    # new
    Supplier_Erp_no = models.IntegerField(null=True, blank=True, default=0)
    Contract_Date = models.DateField(null=True, blank=True)
    Contract_Effective_Date = models.DateField(null=True, blank=True)
    Header = models.ForeignKey('TKCWoInfo_Header', on_delete=models.SET_NULL, null=True, blank=True)
    Discom = models.ForeignKey(Discom_Master, on_delete=models.SET_NULL, null=True, blank=True)
    zone = models.CharField(max_length=30, null=True, blank=True)
    Work_Order_Term_And_Condition = RichTextField(null=True, blank=True)
    Bank = models.ForeignKey('BankDetails', on_delete=models.SET_NULL, null=True, blank=True)
    # Pert = models.ForeignKey('TKCWoInfo_Pert', on_delete=models.SET_NULL, null=True, blank=True)
    # commented
    nit_no = models.CharField(max_length=30, null=True, blank=True)
    milestone = models.IntegerField(null=True, blank=True, default=0)
    price = models.IntegerField(null=True, blank=True, default=0)
    wo_no = models.CharField(max_length=30, null=True, blank=True)
    Loa = models.FileField(upload_to='TKC/FQP/LOA/', null=True, blank=True)

    # loc = models.FileField(upload_to='TKC/FQP/loc/', null=True, blank=True)
    Loa_doc = models.CharField(max_length=30, null=True, blank=True)
    copy_to = RichTextField(null=True, blank=True)
    work_order = RichTextField(null=True, blank=True)
    # Bg = models.ForeignKey('TKCWoInfo_Bg', on_delete=models.SET_NULL, null=True, blank=True)
    Bank = models.ForeignKey(BankDetails, on_delete=models.SET_NULL, null=True, blank=True)
    erp_po_id = models.IntegerField(null=True, blank=True, default=0)
    supplier_pan = models.CharField(max_length=30, null=True, blank=True)
    create_status = models.IntegerField(null=True, blank=True, default=0)
    approve_status = models.IntegerField(null=True, blank=True, default=0)
    approve_remark = models.CharField(max_length=300, null=True, blank=True)
    # comment

    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Wo_Send_To_Approval_Status = models.IntegerField(default=0, blank=True)
    Wo_Send_To_Approval_At = models.DateTimeField(null=True, blank=True)
    Wo_Send_To_Approval_By = models.CharField(max_length=300, null=True, blank=True)
    Wo_Approved_Status = models.IntegerField(default=0, blank=True)
    Wo_Approved_At = models.DateField(null=True, blank=True)
    Wo_Approved_By = models.CharField(max_length=300, null=True, blank=True)
    Wo_Digital = models.FileField(upload_to='Contractor/WO/Digital/', null=True, blank=True)
    Wo_Digital_Upload_Status = models.IntegerField(default=0, blank=True)
    Wo_Digital_Upload_At = models.DateField(null=True, blank=True)
    Wo_Digital_Upload_By = models.CharField(max_length=300, null=True, blank=True)
    # new
    Wo_Agreement = models.FileField(upload_to='TKC/FQP/Agreement/', null=True, blank=True)
    Wo_Agreement_Upload_Status = models.IntegerField(default=0, blank=True)
    Wo_Agreement_Upload_At = models.DateField(null=True, blank=True)
    Wo_Agreement_Upload_By = models.CharField(max_length=300, null=True, blank=True)
    Deleted_At = models.DateField(null=True, blank=True)
    Deleted_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)
   # offer_material_docs = models.FileField(upload_to='TKC/FQP/tkc_offer_material_docs/', null=True, blank=True)
    discrepancies_found_in_Survey_docs = models.FileField(upload_to='TKC/FQP/discrepancies_found_in_Survey/', null=True, blank=True)
    is_boq_added = models.IntegerField(null=True, blank=True, default=0)
    pma_status = models.IntegerField(null=True, blank=True, default=0)     
    approver_status = models.IntegerField(null=True, blank=True, default=0)
    is_verified_boq_added = models.IntegerField(null=True, blank=True, default=0)
    cz_circle_added = models.IntegerField(null=True, blank=True, default=0)
    wz_circle_added = models.IntegerField(null=True, blank=True, default=0)
    ez_circle_added = models.IntegerField(null=True, blank=True, default=0)
    pakage = models.ForeignKey(works_master, on_delete=models.SET_NULL, null=True, blank=True)
    loa_amount = models.FloatField(null=True, blank=True)
    erp_wo_no = models.CharField(max_length=300, null=True, blank=True)
    #Added by Aayush as per API Integration req.
    revision = models.IntegerField(null=True, blank=True) 
    is_gbpa_order = models.IntegerField(null=True, blank=True,default=0) 
    
    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Header(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Scheme_code = models.CharField(max_length=300, null=True, blank=True)
    Scheme_Name = models.CharField(max_length=300, null=True, blank=True)
    Payment_Mode = models.CharField(max_length=300, null=True, blank=True)
    Payment_Term = models.CharField(max_length=300, null=True, blank=True)
    Quotation_No = models.CharField(max_length=300, null=True, blank=True)
    Contract_Offer_No = models.CharField(max_length=300, null=True, blank=True)
    Contract_Offer_Date = models.DateField(null=True, blank=True)
    Contract_Description = models.CharField(max_length=3000, null=True, blank=True)
    Document_Sale_Open_Date = models.DateField(null=True, blank=True)
    Document_Sale_Closed_Date = models.DateField(null=True, blank=True)
    Bid_Submission_Date = models.DateField(null=True, blank=True)
    Bid_Opening_Date = models.DateField(null=True, blank=True)
    Tender_Date = models.DateField(null=True, blank=True)
    Nit_No = models.CharField(max_length=300, null=True, blank=True)
    Nit_Date = models.DateField(null=True, blank=True)
    WO_Prefix = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    VENDOR_NAME = models.CharField(max_length=300, null=True, blank=True)
    VENDOR_SITE_CODE = models.CharField(max_length=300, null=True, blank=True)
    VENDOR_ADDRESS = models.CharField(max_length=300, null=True, blank=True)
    VENDOR_COMMUNICATION = models.CharField(max_length=300, null=True, blank=True)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Contract_Price(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Item_Name = models.CharField(max_length=3000, null=True, blank=True)
    Amount = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Advance_Type(models.Model):
    Name = models.CharField(max_length=300, null=True, blank=True)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Name


class TKCWoInfo_Advance(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=3000, null=True, blank=True)
    Amount_Percentage = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Time_Schedule(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Stage = models.IntegerField(null=True, blank=True, default=0)
    Month = models.IntegerField(null=True, blank=True, default=0)
    Days = models.IntegerField(null=True, blank=True, default=0)
    Completion_date = models.DateField(null=True, blank=True)
    Contract_Amount_Percentage = models.FloatField(null=True, blank=True, default=0)
    Stage_Amount = models.FloatField(null=True, blank=True, default=0)
    Remarks = models.CharField(max_length=3000, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Schedule_Supply(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Schedule_No = models.CharField(max_length=300, null=True, blank=True)
    Schedule_Description = models.CharField(max_length=3000, null=True, blank=True)
    Unit = models.CharField(max_length=300, null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True, default=0)
    Unit_Price_With_Tax = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Schedule_Installation(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Schedule_No = models.CharField(max_length=300, null=True, blank=True)
    Schedule_Description = models.CharField(max_length=3000, null=True, blank=True)
    Unit = models.CharField(max_length=300, null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True, default=0)
    Unit_Price_With_Tax = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Schedule_Supply_Item(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Schedule_Supply = models.ForeignKey(TKCWoInfo_Schedule_Supply, on_delete=models.CASCADE, null=True, blank=True)
    Item_Description = models.CharField(max_length=3000, null=True, blank=True)
    Item_Code = models.CharField(max_length=300, null=True, blank=True)
    Unit = models.CharField(max_length=300, null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True, default=0)
    Unit_Price_With_Tax = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Schedule_Installation_Item(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Schedule_Installation = models.ForeignKey(TKCWoInfo_Schedule_Installation, on_delete=models.CASCADE, null=True,
                                              blank=True)
    Item_Description = models.CharField(max_length=3000, null=True, blank=True)
    Item_Code = models.CharField(max_length=300, null=True, blank=True)
    Unit = models.CharField(max_length=300, null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True, default=0)
    Unit_Price_With_Tax = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Major_Item(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Item_Description = models.CharField(max_length=3000, null=True, blank=True)
    Item_Code = models.CharField(max_length=300, null=True, blank=True)
    Unit = models.CharField(max_length=300, null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True, default=0)
    Unit_Price_With_Tax = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Variable_Item(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Item_Description = models.CharField(max_length=3000, null=True, blank=True)
    Item_Code = models.CharField(max_length=300, null=True, blank=True)
    Unit = models.CharField(max_length=300, null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True, default=0)
    Unit_Price_With_Tax = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Copy_To(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Copy_To = models.CharField(max_length=300, null=True, blank=True)
    Copy_To_URL = models.CharField(max_length=300, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Bg_Type(models.Model):
    Name = models.CharField(max_length=300, null=True, blank=True)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Name


class TKCWoInfo_Bg(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    BG_Copy = models.FileField(upload_to='TKC/FQP/bg/', null=True, blank=True)
    BG_Approved_copy = models.FileField(upload_to='TKC/FQP/bg/', null=True, blank=True)
    BG_Type = models.CharField(max_length=300, null=True, blank=True)
    BG_Bank_name = models.CharField(max_length=300, null=True, blank=True)
    BG_Guarantee_no = models.CharField(max_length=30, null=True, blank=True)
    BG_Issue_Date = models.DateField(null=True, blank=True)
    BG_Valid_Date = models.DateField(null=True, blank=True)
    BG_Amount = models.CharField(max_length=30, null=True, blank=True)
    BG_Submit = models.IntegerField(default=0, blank=True)
    BG_Submit_At = models.DateField(null=True, blank=True)
    BG_Approved_Remark = models.CharField(max_length=300, null=True, blank=True)
    BG_Approved_Status = models.IntegerField(default=0, blank=True)
    BG_Approved_At = models.DateTimeField(null=True, blank=True)
    BG_Approved_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCWoInfo_Pert(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Pert = models.FileField(upload_to='TKC/FQP/Pert/', null=True, blank=True)
    Pert_Submit = models.IntegerField(default=0, blank=True)
    Pert_Submit_At = models.DateTimeField(null=True, blank=True)
    Pert_Approved_Remark = models.CharField(max_length=300, null=True, blank=True)
    Pert_Approved_Status = models.IntegerField(default=0, blank=True)
    Pert_Approved_At = models.DateTimeField(null=True, blank=True)
    Pert_Approved_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo
    

class TKC_MqpPlanDocuments(models.Model):
    
    tkcwoinfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    mqpdoc = models.FileField(upload_to='TKC/FQP/Mqp Document/', null=True, blank=True)
    mqpdoc_submit = models.IntegerField(default=0, blank=True)
    mqpdoc_at = models.DateTimeField(null=True, blank=True)
    mqpdoc_approved_remark = models.CharField(max_length=300, null=True, blank=True)
    mqpdoc_approved_status = models.IntegerField(default=0, blank=True)
    mqpdoc_approved_at = models.DateTimeField(null=True, blank=True)
    mqpdoc_approved_by = models.CharField(max_length=300, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.tkcwoinfo
    
class TKC_FqpPlanDocuments(models.Model):
    tkcwoinfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    fqpdoc = models.FileField(upload_to='TKC/FQP/Fqp Documents/', null=True, blank=True)
    fqpdoc_submit = models.IntegerField(default=0, blank=True)
    fqpdoc_at = models.DateTimeField(null=True, blank=True)
    fqpdoc_approved_remark = models.CharField(max_length=300, null=True, blank=True)
    fqpdoc_approved_status = models.IntegerField(default=0, blank=True)
    fqpdoc_approved_at = models.DateTimeField(null=True, blank=True)
    fqpdoc_approved_by = models.CharField(max_length=300, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.tkcwoinfo

class TKCOtherDocuments(models.Model):
    
    tkcwoinfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    otherdoc = models.FileField(upload_to='TKC/FQP/Other Documents/', null=True, blank=True)
    otherdoc_submit = models.IntegerField(default=0, blank=True)
    otherdoc_at = models.DateTimeField(null=True, blank=True)
    otherdoc_approved_remark = models.CharField(max_length=300, null=True, blank=True)
    otherdoc_approved_status = models.IntegerField(default=0, blank=True)
    otherdoc_approved_at = models.DateTimeField(null=True, blank=True)
    otherdoc_approved_by = models.CharField(max_length=300, null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.tkcwoinfo


class TKCWoInfo_LOC(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    LOC = models.FileField(upload_to='TKC/FQP/LOC/', null=True, blank=True)
    LOC_No = models.IntegerField(default=0, blank=True)
    LOC_Amount = models.CharField(max_length=30, null=True, blank=True)
    LOC_Issue_Date = models.DateField(null=True, blank=True)
    LOC_Valid_Date = models.DateField(null=True, blank=True)
    LOC_Submit = models.IntegerField(default=0, blank=True)
    LOC_Submit_At = models.DateTimeField(null=True, blank=True)
    LOC_Approved_Remark = models.CharField(max_length=300, null=True, blank=True)
    LOC_Approved_Status = models.IntegerField(default=0, blank=True)
    LOC_Approved_At = models.DateTimeField(null=True, blank=True)
    LOC_Approved_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.TKCWoInfo


class TKCVendor(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Vendor = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    Material_id = models.ForeignKey('vendor.Vendor_Material_Details', to_field='id', on_delete=models.CASCADE,
                                    null=True, blank=True)
    TKCVendor_Submit = models.IntegerField(default=0, blank=True)
    TKCVendor_Submit_At = models.DateTimeField(null=True, blank=True)
    TKCVendor_Approved_Remark = models.CharField(max_length=300, null=True, blank=True)
    TKCVendor_Approved_Status = models.IntegerField(default=0, blank=True)
    TKCVendor_Approved_At = models.DateTimeField(null=True, blank=True)
    TKCVendor_Approved_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)
    vendor_gtp_file = models.FileField(upload_to='TKC/FQP/vendor_gtp_drawings/', null=True, blank=True)
    vendor_other_docs = models.FileField(upload_to='TKC/FQP/vendor_other_docs/', null=True, blank=True)
    vendor_gtp_approval = models.IntegerField(default=0, blank=True)
    other_acceptance_rejection_doc = models.FileField(upload_to='TKC/FQP/other_acceptance_rejection_doc/', null=True, blank=True)

    def _str_(self):
        return self.TKCWoInfo


# class TKCVendorMaterial(models.Model):
    # TKCVendor = models.ForeignKey(TKCVendor, on_delete=models.CASCADE, null=True, blank=True)
    # Vendor_Material_Details = models.ForeignKey('vendor.Vendor_Material_Details', on_delete=models.CASCADE, null=True, blank=True)
    # item_code = models.CharField(max_length=200, null=True, blank=True)
    # Unit = models.CharField(max_length=200, null=True, blank=True)
    # Quantity = models.IntegerField(null=True, blank=True)
    # Status = models.IntegerField(null=True, blank=True, default=0)

    # def _str_(self):
        # return self.TKCVendor

class Offer_Material(models.Model):
    TKCVendor = models.ForeignKey(TKCVendor, on_delete=models.CASCADE, null=True, blank=True)
    Quantity = models.IntegerField(null=True, blank=True)
    Calibration_Certificate = models.FileField(upload_to='TKC/FQP/Test/', null=True, blank=True)
    Material_Offer_Submit = models.IntegerField(default=0, blank=True)
    Material_Offer_Submit_Submit_At = models.DateTimeField(null=True, blank=True)
    Material_Offer_Submit_Approved_Remark = models.CharField(max_length=300, null=True, blank=True)
    Material_Offer_Submit_Approved_Status = models.IntegerField(default=0, blank=True)
    Material_Offer_Submit_Approved_At = models.DateTimeField(null=True, blank=True)
    Material_Offer_Submit_Approved_By = models.CharField(max_length=300, null=True, blank=True)
    Quantity_Inspected = models.IntegerField(null=True, blank=True)
    Document_Referred = models.CharField(max_length=300, null=True, blank=True)
    Test_Witnessed = models.CharField(max_length=500, null=True, blank=True)
    Raw_material = models.CharField(max_length=500, null=True, blank=True)
    Remark = models.CharField(max_length=500, null=True, blank=True)
    Observations = models.CharField(max_length=500, null=True, blank=True)
    Lat = models.CharField(max_length=50, null=True, blank=True)
    Log = models.CharField(max_length=50, null=True, blank=True)
    PDI = models.ForeignKey("main.PDI_Inspection_Info", on_delete=models.CASCADE, null=True, blank=True)
    PDI_Assign = models.IntegerField(default=0, blank=True)
    PDI_Assign_At = models.DateTimeField(null=True, blank=True)
    PDI_Assign_By = models.CharField(max_length=300, null=True, blank=True)
    PDI_Complete = models.IntegerField(default=0, blank=True)
    PDI_Approved_Remark = models.CharField(max_length=300, null=True, blank=True)
    PDI_Approved_Status = models.IntegerField(default=0, blank=True)
    PDI_Approved_At = models.DateTimeField(null=True, blank=True)
    PDI_Approved_By = models. CharField(max_length=300, null=True, blank=True)
    DI_Created_Status = models.IntegerField(default=0, blank=True)
    DI_Created_At = models.DateTimeField(null=True, blank=True)
    DI_Created_By = models.CharField(max_length=300, null=True, blank=True)
    Dispatch_Status = models.IntegerField(default=0, blank=True)
    Dispatch_At = models.DateTimeField(null=True, blank=True)
    Dispatch_Address = models.CharField(max_length=3000, null=True, blank=True)
    Received_Remark = models.CharField(max_length=3000, null=True, blank=True)
    Received_Status = models.IntegerField(default=0, blank=True)
    Received_At = models.DateTimeField(null=True, blank=True)
    Received_By = models.CharField(max_length=300, null=True, blank=True)
    Physical_Remark = models.CharField(max_length=3000, null=True, blank=True)
    Physical_Status = models.IntegerField(default=0, blank=True)
    Physical_At = models.DateTimeField(null=True, blank=True)
    Physical_By = models.CharField(max_length=300, null=True, blank=True)
    DI_Division = models.ForeignKey("main.Division_Master", on_delete=models.CASCADE, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)
    nabl_status = models.IntegerField(null=True, blank=True, default=0)
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_number = models.CharField(max_length=15, null=True, blank=True)
    nabl_gatepass = models.IntegerField(null=True, blank=True, default=0)
    send_to_nabl = models.IntegerField(null=True, blank=True, default=0)
    send_to_cgm = models.IntegerField(null=True, blank=True, default=0) 
    Signed_Remark = models.CharField(max_length=500, null=True, blank=True)  # add for data forund or not found mobile side that remark----> add by shubham tripathi 
    Signed_Status = models.IntegerField(null=True, blank=True, default=0)  # if data found in mobile app side then status 1 and else not 0  ----> add by shubham tripathi 
    pdi_report = models.FileField(upload_to='main/pdi_inpection/representative')
    readiness_date = models.DateField(null=True, blank=True)
    def str(self):
        return self.TKCVendor

    
    
    def str(self):
        return self.Offer_Material

class PDI_Factory_image(models.Model):
    Offer_Material = models.ForeignKey('tkc.offer_material_site_stores', on_delete=models.CASCADE, null=True, blank=True)
    Image = models.FileField(upload_to='FQP/PDI/Factory')



class Offer_Material_Item_Code(models.Model):
    Offer_Material= models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True, blank=True)
    Item_Serial_No = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)
    Physical_Status = models.IntegerField(default=0, blank=True)
    Physical_At = models.DateTimeField(null=True, blank=True)
    Physical_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)
    gatepass = models.IntegerField(null=True, blank=True, default=0)
    is_sampled = models.IntegerField(null=True, blank=True, default=0)
    
    nabl_result = models.IntegerField(null=True, blank=True, default=0)
    nabl_report = models.FileField(upload_to='documents/wo/nabl_report', null=True, blank=True)
    nabl_result_percentage = models.CharField(max_length=5, null=True, blank=True)
    Division = models.ForeignKey("main.Division_Master", on_delete=models.CASCADE, null=True, blank=True)
    Store_Address = models.CharField(max_length=150, null=True, blank=True)

    def _str_(self):
        return self.Offer_Material

class Tier_1_Test_Item(models.Model):
    Name = models.CharField(max_length=300, null=True, blank=True)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Name


class Tier_1_Test_Item_Type(models.Model):
    Item = models.ForeignKey(Tier_1_Test_Item, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=300, null=True, blank=True)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Name


class TKCWoInfo_Estimate(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Estimate_No = models.CharField(max_length=3000, null=True, blank=True)
    Estimate_Name = models.CharField(max_length=5000, null=True, blank=True)
    Erp_no = models.IntegerField(null=True, blank=True, default=0)
    Creation_Date = models.DateField(auto_now_add=True, null=True)
    Legacy_No = models.CharField(max_length=300, null=True, blank=True)
    Organisation_Name = models.CharField(max_length=500, null=True, blank=True)
    Sub_Division = models.CharField(max_length=500, null=True, blank=True)
    DC = models.CharField(max_length=500, null=True, blank=True)
    Scheme_Name = models.CharField(max_length=500, null=True, blank=True)
    ERP_Status = models.CharField(max_length=50, null=True, blank=True)
    ERP_Status_Date = models.DateField(auto_now_add=True, null=True)
    Funding_Agency_Percentage = models.CharField(max_length=500, null=True, blank=True)
    Amount = models.IntegerField(null=True, blank=True, default=0)
    DOP_Admin = models.CharField(max_length=500, null=True, blank=True)
    DOP_Admin_Code = models.CharField(max_length=500, null=True, blank=True)
    DOP_Work = models.CharField(max_length=500, null=True, blank=True)
    DOP_Work_Code = models.CharField(max_length=500, null=True, blank=True)
    Project_Creater = models.CharField(max_length=500, null=True, blank=True)
    Project_Manager = models.CharField(max_length=500, null=True, blank=True)
    Description = models.CharField(max_length=500, null=True, blank=True)
    History_Scope = models.CharField(max_length=10000, null=True, blank=True)
    Attachments = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Estimate_Name


class Estimate_Task(models.Model):
    Estimate = models.ForeignKey(TKCWoInfo_Estimate, on_delete=models.CASCADE, null=True, blank=True)
    Task_Name = models.CharField(max_length=500, null=True, blank=True)
    Task_No = models.IntegerField(null=True, blank=True, default=0)
    UOM = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Estimate


class Estimate_Sub_Task(models.Model):
    Estimate_Task = models.ForeignKey(Estimate_Task, on_delete=models.CASCADE, null=True, blank=True)
    Tier_1_Test = models.ForeignKey("Tier_1_Test_Item", on_delete=models.CASCADE, null=True, blank=True)
    SubTask_No = models.CharField(max_length=500, null=True, blank=True)
    Task_Name = models.CharField(max_length=500, null=True, blank=True)
    UOM = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Estimate


class Sub_Task_Item(models.Model):
    Sub_Task = models.ForeignKey(Estimate_Sub_Task, on_delete=models.CASCADE, null=True, blank=True)
    Item_Code = models.CharField(max_length=500, null=True, blank=True)
    Item_Description = models.CharField(max_length=1000, null=True, blank=True)
    UOM = models.CharField(max_length=500, null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True, default=0)
    Rate = models.FloatField(null=True, blank=True, default=0)
    Amount = models.FloatField(null=True, blank=True, default=0)
    Erection_Cost = models.FloatField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Estimate


class TKCWoInfo_Estimate_Schedule(models.Model):
    Estimate = models.ForeignKey(TKCWoInfo_Estimate, on_delete=models.CASCADE, null=True, blank=True)
    Schedule = models.ForeignKey(TKCWoInfo_Schedule_Installation, on_delete=models.CASCADE, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Estimate



class Tier_1_Test_Item_Type_Inspection_List(models.Model):
    Item_Type = models.ForeignKey(Tier_1_Test_Item_Type, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=300, null=True, blank=True)
    Description = models.CharField(max_length=500, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.Name


class Tier_1_Inspection_Result(models.Model):
    Inspection_Info = models.ForeignKey(Tier1_Inspection_Info, on_delete=models.CASCADE, null=True, blank=True)
    Sub_Task = models.ForeignKey(Estimate_Sub_Task, on_delete=models.CASCADE, null=True, blank=True)
    Inspection = models.ForeignKey(Tier_1_Test_Item_Type_Inspection_List, on_delete=models.CASCADE, null=True, blank=True)
    Image = models.FileField(upload_to='FQP/Tier1/Inspection')
    Remark = models.CharField(max_length=500, null=True, blank=True)
    Lat = models.CharField(max_length=50, null=True, blank=True)
    Log = models.CharField(max_length=50, null=True, blank=True)
    Submitted_At = models.DateTimeField(auto_now_add=True, null=True)
    Submitted_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)
    Short_Coming_Remark = models.CharField(max_length=500, null=True, blank=True)# add for save  mobile side data ----> add by shubham tripathi 1/12/2022

    def _str_(self):
        return self.Name

class TKCScheduleInfo(models.Model):
    TKCWoInfo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    phase = models.IntegerField(null=True, blank=True)
    task = models.CharField(max_length=1000, null=True, blank=True)
    percentage = models.IntegerField(null=True, blank=True)
    tkc_offer_date = models.DateField(null=True, blank=True)
    inspecting_officer_id = models.CharField(max_length=10, null=True, blank=True)
    inspecting_date = models.DateField(null=True, blank=True)
    inspecting_status = models.IntegerField(blank=True, default=0)
    offer_status = models.IntegerField(blank=True, default=0)
    Result = models.IntegerField(blank=True, default=0)
    comment = models.CharField(max_length=1000, null=True, blank=True)

    def _str_(self):
        return self.TKCScheduleInfo

        


class FQP_Test(models.Model):
    test_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.IntegerField(blank=True, null=True, default=0)
    From_Date = models.IntegerField(blank=True, null=True, default=0)
    Till_Date = models.IntegerField(blank=True, null=True, default=0)

    def _str_(self):
        return self.test_name


class FQP_Test_Attributes(models.Model):
    FQP_Test = models.ForeignKey(FQP_Test, on_delete=models.CASCADE, null=True, blank=True)
    Test_Attributes = models.CharField(max_length=1000, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    Created_By = models.CharField(max_length=20, null=True, blank=True)
    Updated_By = models.CharField(max_length=20, null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Is_Deleted = models.IntegerField(blank=True, null=True, default=0)
    From_Date = models.IntegerField(blank=True, null=True, default=0)
    Till_Date = models.IntegerField(blank=True, null=True, default=0)

    def _str_(self):
        return self.Test_Attributes


# ------------------POORNIMA

class FQP_Officers(models.Model):
    # Use =1 for Tier 1 officer and 2 for tier2  officer and 3 for tier 3 officer
    officer_Tier = models.IntegerField(blank=True, default=0, null=True)
    FQP_Officer = models.CharField(max_length=200, null=True)
    FQP_Officer_Id = models.AutoField(primary_key=True)
    FQP_Officer_Name = models.CharField(max_length=200, null=True)
    FQP_Password = models.CharField(max_length=200, null=True)
    FQP_Mobile_No = models.CharField(max_length=200, null=True, unique=True)
    Is_Active = models.IntegerField(blank=True, default=0, null=True)
    Created_Date = models.DateField(default=None, null=True)
    Updated_By = models.CharField(max_length=200)
    Updated_Date = models.DateField(default=None, null=True)
    Created_By = models.CharField(max_length=200, null=True)


# Create your models here.
class FQP_Material(models.Model):
    officer_id = models.ForeignKey(FQP_Officers, on_delete=models.PROTECT)
    FQP_Material = models.AutoField(primary_key=True)
    Material_Name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.Material_Name


# class FQP_Test(models.Model):
#     officer_id = models.ForeignKey(FQP_Officers, on_delete=models.PROTECT)
#
#     FQP_Test_Id = models.AutoField(primary_key=True)
#     FQP_Material = models.ForeignKey(FQP_Material, on_delete=models.PROTECT)
#     FQP_Test = models.CharField(max_length=200, null=True, blank=True)

#
# class FQP_Officer_Task(models.Model):
#     FQP_Officer_Id = models.AutoField(primary_key=True)
#     Schedule_id = models.ForeignKey(TKCScheduleInfo, on_delete=models.CASCADE, null=True, blank=True)
#     FQP_material_id = models.ForeignKey(FQP_Material, on_delete=models.CASCADE, null=True, blank=True)
#     # FQP_test_id = models.ForeignKey(FQP_Test, on_delete=models.CASCADE, null=True, blank=True)
#     Is_Active = models.IntegerField(blank=True, default=0, null=True)
#     Created_Date = models.DateField(default=None, null=True)
#     Updated_By = models.CharField(max_length=200, null=True)
#     Updated_Date = models.DateField(default=None, null=True)
#     Created_By = models.CharField(max_length=200, null=True)

#
class FQP_Test_Data(models.Model):
    Officer = models.ForeignKey(InspectingOfficerInfo, on_delete=models.CASCADE, null=True, blank=True)
    Test = models.ForeignKey(FQP_Test_Attributes, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    work_order = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    Image = models.ImageField(upload_to='fqp/image', null=True, blank=True)
    Status = models.IntegerField(blank=True, null=True, default=0)
    Observation = models.CharField(max_length=200, null=True, blank=True)
    Latitude = models.CharField(max_length=30, null=True, blank=True)
    Longitude = models.CharField(max_length=30, null=True, blank=True)
    Is_Active = models.IntegerField(blank=True, default=0, null=True)
    Updated_By = models.CharField(max_length=200, null=True, blank=True)
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Created_By = models.CharField(max_length=200, null=True, blank=True)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)
    
    
class tkc_di_master(models.Model):
    id = models.AutoField(primary_key=True)
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    # wo_material = models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True, blank=True)
    offer_no = models.CharField(max_length=200, null=True, blank=True)
    tkc_di_doc = models.FileField(upload_to='TKC_DI_documents', null=True, blank=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    wo_no = models.CharField(max_length=200, null=True, blank=True)
    di_send_to_approval_status = models.BooleanField(default=False, blank=True)
    di_send_by_approval_by = models.CharField(max_length=300, null=True, blank=True)
    di_approved_status = models.IntegerField(default=0, blank=True)
    di_approved_by = models.CharField(max_length=300, null=True, blank=True)
    di_approved_date = models.DateTimeField(auto_now=True,null=True)
    di_digital_upload_status = models.IntegerField(default=0, blank=True)
    di_digital_upload_by = models.CharField(max_length=300, null=True, blank=True)
    supplier_deliverable_status = models.BooleanField(default=False, blank=True)
    status = models.IntegerField(default=0, blank=True)
    di_subject = models.CharField(max_length=1000, null=True, blank=True)
    erp_di_number  = models.CharField(max_length=200, null=True, blank=True)
    prefix = models.CharField(max_length=700, null=True, blank=True)
    term_and_condition = RichTextField(null=True, blank=True)
    copy_to = RichTextField(null=True, blank=True)
    send_to_cgm = models.IntegerField(default=0, blank=True)
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_status = models.IntegerField(default=0, blank=True)
    nabl_number = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True,null=True)
    Physical_Status = models.IntegerField(default=0, blank=True)
    final_di_submit = models.BooleanField(default=False, blank=True)
    created_di_doc = models.FileField(upload_to='created_di_documents', null=True, blank=True)
    lr_copy_or_rr_and_delivery_challan = models.FileField(upload_to='lr_copy_or_rr_and_delivery_challan', null=True, blank=True)
    packing_list_of_materials = models.FileField(upload_to='packing_list_of_materials', null=True, blank=True)
    insurance_policy_certificate = models.FileField(upload_to='insurance_policy_certificate', null=True, blank=True)
    material_guarantee_certificate = models.FileField(upload_to='material_guarantee_certificate', null=True, blank=True)
    di_site_store_location=models.CharField(max_length=100, null=True, blank=True)
    # approver_di_rejected = models.BooleanField(default=False, blank=True)
    
    

    
class fqp_drr_info(models.Model):
    area_store = models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True, blank=True)
    drr_date=models.DateField(null=True, blank=True)
    drr_vehicle=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_no=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_date=models.DateField(null=True, blank=True)
    drr_quantity=models.IntegerField(blank=True, default=0)

   
class fqp_wo_gatepass(models.Model):
    area_store = models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True, blank=True)
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
    aname = models.CharField(max_length=15, null=True, blank=True)

 
class fqp_wo_nabl_gatepass(models.Model):
    area_store = models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True, blank=True)
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
    aname = models.CharField(max_length=15, null=True, blank=True)
    Division = models.ForeignKey("main.Division_Master", on_delete=models.CASCADE, null=True, blank=True)
    Store_Address = models.CharField(max_length=150, null=True, blank=True)
    gate_pass = models.FileField(upload_to='documents/rca/all_xmr_report', null=True, blank=True)

 
   


class Fqp_Work_Order_Trf_Details(models.Model):
    TRF_Id = models.AutoField(primary_key=True)
    area_store_id = models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True, blank=True)
    areastore = models.CharField(max_length=200, null=True, blank=True)
    user_id = models.IntegerField(blank=True, default=0)
    ro_id = models.IntegerField(blank=True, default=0)
    gatepass_id = models.IntegerField(blank=True, default=0)
    outward_gatepass_id = models.IntegerField(blank=True, default=0)
    po_id = models.CharField(max_length=200, null=True, blank=True)
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
    sign = models.CharField(max_length=200, null=True, blank=True)
    gatepass_gen = models.IntegerField(blank=True, default=0)
    outpass_gen = models.IntegerField(blank=True, default=0)
    #######################################
    contact_person_designation = models.CharField(max_length=200, null=True, blank=True)
    decision_yes_no = models.CharField(max_length=200, null=True, blank=True)
    decision_option = models.CharField(max_length=200, null=True, blank=True)
    onbehalf = models.CharField(max_length=200, null=True, blank=True)
    sign2 = models.CharField(max_length=200, null=True, blank=True) 
    Organization = models.CharField(max_length=200, null=True, blank=True) 
    email_address = models.CharField(max_length=200, null=True, blank=True)
    phy_cond = models.CharField(max_length=200, null=True, blank=True) 
    as_per_trf = models.CharField(max_length=200, null=True, blank=True) 
    dec_rule_app = models.CharField(max_length=200, null=True, blank=True) 
    scope = models.CharField(max_length=200, null=True, blank=True) 
    sample_status = models.CharField(max_length=200, null=True, blank=True) 
    recv_incharge = models.CharField(max_length=200, null=True, blank=True) 
    tech_manager = models.CharField(max_length=200, null=True, blank=True)
    tender_generated = models.IntegerField(blank=True, default=0)
    TRFAreastore_file = models.FileField(upload_to='TRFForms/', null=True, blank=True)
    trf_generated = models.IntegerField(blank=True, default=0)
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_number = models.CharField(max_length=15, null=True, blank=True)
    

# created by shubham tripathi 25/11/2022 for jabalpur discome suggest by yashwant sir 
#  pdi inspection application 
class Emb_Measurement(models.Model):
    Feeder_id = models.IntegerField(null=True, blank=True, default=0)
    Estimate_id = models.IntegerField(null=True, blank=True, default=0)
    Contractor = models.ForeignKey("main.User_Registration", on_delete=models.CASCADE, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=1)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)


class offer_material_divisions_data(models.Model):
    tkc_di = models.ForeignKey(tkc_di_master,on_delete=models.CASCADE, null=True, blank=True)
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    wo_material = models.ForeignKey(Offer_Material, on_delete=models.CASCADE, null=True, blank=True) 
    quantity = models.IntegerField(blank=True, default=0)
    Division = models.ForeignKey("main.Division_Master", on_delete=models.CASCADE)
    supplier = models.ForeignKey("main.User_Registration",on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
class tkc_wo_items_boq(models.Model):
    id = models.AutoField(primary_key=True)
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    material_name  = models.CharField(max_length=200, null=True, blank=True)
    item_code  = models.CharField(max_length=200, null=True, blank=True)
    total_order_qty  = models.FloatField(default=0, blank=True)
    dispatch_qty = models.FloatField(default=0, blank=True)
    balance_qty = models.FloatField(default=0, blank=True)
    old_loa_qty = models.FloatField(default=0, blank=True)
    is_offered = models.BooleanField(default=False, blank = True)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(null=True, blank = True)
    uom = models.CharField(max_length=500, null=True, blank=True)
    balance_di_qty = models.FloatField(null=True, blank=True)
    
class Tag_Circle(models.Model):
    
    wo_no = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)    
    discom=models.ForeignKey(Discom_Master, on_delete=models.CASCADE, null=True, blank=True)
    circle_name = models.CharField(max_length=100, null=True, blank=True)
    circle = models.ForeignKey(Circle_Master, on_delete=models.CASCADE, null=True, blank=True)
    Created_At = models.DateTimeField(null=True, blank=True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)

    def _str_(self):
        return self.wo_no 
    
    
class tkc_update_boq(models.Model):
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    boq_item = models.ForeignKey(tkc_wo_items_boq, on_delete=models.CASCADE, null=True, blank=True)
    item_code  = models.CharField(max_length=200, null=True, blank=True)
    material_name  = models.CharField(max_length=200, null=True, blank=True)
    total_order_qty  = models.IntegerField(default=0, blank=True)
    circles_name = models.CharField(max_length=200, null=True, blank=True)
    circle_quantity = models.FloatField(default=0, blank=True, null=True)
    verified_circle_qty = models.FloatField(default=0, blank=True, null=True)
    gm_verified_circle_qty = models.FloatField(default=0, blank=True, null=True)
    gm_status = models.IntegerField(null=True, blank=True, default=0)    
    total_qty = models.FloatField(default=0, blank=True, null=True)
    gm_boq_recommendation  = models.CharField(max_length=1000, null=True, blank=True) 
    pma_boq_recommendation  = models.CharField(max_length=1000, null=True, blank=True)         
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(null=True, blank = True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Officer_name = models.CharField(max_length=200, default="")
    

    
class tkc_requested_boq_item(models.Model):
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    boq_item = models.ForeignKey(tkc_wo_items_boq, on_delete=models.CASCADE, null=True, blank=True)
    item_code  = models.CharField(max_length=200, null=True, blank=True)
    material_name  = models.CharField(max_length=200, null=True, blank=True)
    circles_name = models.CharField(max_length=200, null=True, blank=True)
    circle_qty = models.FloatField(default=0, blank=True, null=True)
    gm_verified_circle_qty = models.FloatField(default=0, blank=True, null=True) 
    gm_status = models.IntegerField(null=True, blank=True, default=0) 
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(null=True, blank = True)
    Created_By = models.CharField(max_length=300, null=True, blank=True)
    Officer_name = models.CharField(max_length=200, default="")




# #  8/3/2023------fqp intimation model by shubham tripahti-----guide by yashwant sir and rustam sir---------

class FqpIntimation(models.Model):
    user = models.ForeignKey(User_Registration,on_delete=models.CASCADE,blank=True,null=True)
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True,related_name="intimation_workorder_data")
    officer = models.ForeignKey('main.officer', on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey('main.Region_Master', on_delete=models.CASCADE, null=True, blank=True)
    circle = models.ForeignKey('main.Circle_Master', on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey('main.Division_Master', on_delete=models.CASCADE, null=True, blank=True)
    work_execution_detail = models.CharField(max_length=500,blank=True,null=True)
    brief_description_of_work = models.CharField(max_length=500,blank=True,null=True)
    work_execution_milestone_pdf = models.FileField(upload_to='fqp_intimation/work_execution/',blank=True,null=True)
    layout_sld_of_work_execution = models.FileField(upload_to='fqp_intimation/sld_work_pdf/',blank=True,null=True)
    tentative_date_of_execution = models.DateField(blank=True,null=True)
    remark = models.CharField(max_length=500,blank=True,null=True)
    intimation_status = models.IntegerField(blank=True,null=True,default=0)
    status = models.IntegerField(blank=True,null=True,default=0)
    created_at = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    def __str__(self):
        return self.work_execution_detail

class FqpIntimation_Observation_Info(models.Model):
    milestone_subcategory_data = models.ForeignKey("main.Milestone_Main_SubCategory_Data", on_delete=models.CASCADE,related_name="milestones_data",null=True, blank=True)
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE,null=True, blank=True)
    fqpintimation = models.ForeignKey(FqpIntimation, on_delete=models.CASCADE, related_name="fqpintimationdata",null=True, blank=True)
    observation_image = models.FileField(upload_to='fqp_intimation/image/',null=True, blank=True)
    observation_date = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    observation_remark = models.CharField(max_length=500,null=True, blank=True)
    observation_location = models.CharField(max_length=800,null=True, blank=True)
    observation_lat = models.CharField(max_length=100,null=True, blank=True)
    observation_long = models.CharField(max_length=100,null=True, blank=True)
    observation_status = models.IntegerField(default=0,null=True, blank=True)
    status = models.IntegerField(default=0,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.observation_remark:
            return self.observation_remark
        else:
            return "Observation Info"

class FqpIntimation_Officer_Info(models.Model):
    fqpintimation = models.ForeignKey(FqpIntimation, on_delete=models.CASCADE,null=True, blank=True)
    # fqpintimation_observation_info = models.ForeignKey(FqpIntimation_Observation_Info, on_delete=models.CASCADE,related_name="fqpIntimation_observation_info_data",null=True, blank=True)
    officer_fullname = models.CharField(max_length=500,null=True, blank=True)
    # officer_image = models.FileField(upload_to='fqp_intimation/officer_image/',null=True, blank=True)
    officer_designation = models.CharField(max_length=200,null=True, blank=True)
    representative_from = models.CharField(max_length=200,null=True, blank=True)
    officer_mobile = models.CharField(max_length=15,null=True, blank=True)
    status = models.IntegerField(default=1,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.officer_fullname:
            return self.officer_fullname
        else:
            return "Officer fullname"

class FqpIntimation_Observation_Close(models.Model):
    fqpintimation = models.ForeignKey(FqpIntimation, on_delete=models.CASCADE,null=True, blank=True)
    image_1 = models.FileField(upload_to='fqp_intimation/observation_close/',null=True, blank=True)
    image_2 = models.FileField(upload_to='fqp_intimation/observation_close/',null=True, blank=True)
    image_3 = models.FileField(upload_to='fqp_intimation/observation_close/',null=True, blank=True)
    close_remark = models.CharField(max_length=500,null=True, blank=True)
    close_lat = models.CharField(max_length=100,null=True, blank=True)
    close_long = models.CharField(max_length=100,null=True, blank=True)
    status = models.IntegerField(default=0,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.close_remark:
            return self.close_remark
        else:
            return "close remark"


# -----------------------------------------start by ravindra------------------------------------------#
        
class fqp_check_status(models.Model):
    feeder_id = models.CharField(max_length=30,blank=True,primary_key=True)
    FQP_response = models.CharField(max_length=30,default='Not Ok', blank = True)
    
class fqp_check_status_save(models.Model):  
    feeder_id = models.CharField(max_length=30, blank=True,primary_key=True)
    FQP_response = models.CharField(max_length=30,default='Not Ok', blank = True)
    
    
#-------------------------------------------------- end by ravindra-------------------------------------#        


#----------------new fqpintimation code added by shubham tripathi-----

# ---------------new fqp intmaiton code added by shubahm tripathi ---20-jun-2023-------------
class Wo_Order_Task(models.Model):
    officer = models.ForeignKey('main.officer', on_delete=models.CASCADE, null=True, blank=True,related_name="task_created_by_officer")
    wo = models.ForeignKey('TKCWoInfo', on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey('main.Region_Master', on_delete=models.SET_NULL, null=True, blank=True)
    circle = models.ForeignKey('main.Circle_Master', on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey('main.Division_Master', on_delete=models.SET_NULL, null=True, blank=True)
    distribution_center= models.ForeignKey('main.DC_Master', on_delete=models.SET_NULL, null=True, blank=True)
    gis_feeder_id = models.CharField(max_length=30, null=True, blank=True)
    erp_estimate_no = models.CharField(max_length=30, null=True, blank=True)
    erp_gbpa_no = models.CharField(max_length=30, null=True, blank=True)
    package_name_and_no = models.CharField(max_length=150, null=True, blank=True)
    description_of_work = models.CharField(max_length=900, null=True, blank=True)
    feeder_name_on_which_work_proposed = models.CharField(max_length=150, null=True, blank=True)
    substation_name_on_which_work_proposed = models.CharField(max_length=150, null=True, blank=True)
    emb_measurement_send_status = models.IntegerField(default=0,null=True, blank=True)
    status = models.IntegerField(default=0,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.description_of_work:
            return self.description_of_work
        else:
            return "Description of work"

class Wo_Task_Milestone(models.Model):
    wo_task = models.ForeignKey(Wo_Order_Task, on_delete=models.SET_NULL, null=True, blank=True)
    milestone = models.ForeignKey(Milestone_Main, on_delete=models.SET_NULL, null=True, blank=True)
    task_milestone_status = models.IntegerField(default=0,null=True, blank=True)
    def __str__(self):
        if self.milestone.milestone_name:
            return self.milestone.milestone_name
        else:
            return "Milestone Name"


class New_FqpIntimation(models.Model):
    user = models.ForeignKey(User_Registration,on_delete=models.CASCADE,blank=True,null=True,related_name="intimated_by_contractor")
    intimation_unique_no = models.CharField(max_length=50,blank=True,null=True)
    # wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True,related_name="new_intimation_workorder_data")
    wo_task = models.ForeignKey(Wo_Order_Task, on_delete=models.CASCADE, null=True, blank=True,related_name="newfqp_intimation_data")
    wotask_milestone = models.ForeignKey(Wo_Task_Milestone, on_delete=models.CASCADE, null=True, blank=True,related_name="new_intimation_task_milestone_data")
    # officer = models.ForeignKey('main.officer', on_delete=models.CASCADE, null=True, blank=True)
    work_execution_detail = models.CharField(max_length=500,blank=True,null=True)
    brief_description_of_work = models.CharField(max_length=500,blank=True,null=True)
    work_execution_milestone_image1 = models.FileField(upload_to='new_fqp_intimation/execution_image1',blank=True,null=True)
    work_execution_milestone_image2 = models.FileField(upload_to='new_fqp_intimation/execution_image2',blank=True,null=True)
    date_of_execution = models.DateField(blank=True,null=True)
    date_of_readines = models.DateField(blank=True,null=True)
    date_of_completion = models.DateField(blank=True,null=True)
    intimation_status = models.IntegerField(blank=True,null=True,default=0)
    intimation_remark = models.CharField(max_length=500,blank=True,null=True)
    emb_send_status = models.IntegerField(default=0,null=True, blank=True)
    status = models.IntegerField(blank=True,null=True,default=0)
    created_at = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    def __str__(self):
        return self.work_execution_detail

# intimation_milestone_main_category
class New_FqpIntimation_milestone_category(models.Model):
    fqpintimation = models.ForeignKey(New_FqpIntimation,on_delete=models.CASCADE,blank=True,null=True,related_name="newfqp_milestone_category")
    milestone_category = models.ForeignKey(Milestone_Main_Category, on_delete=models.CASCADE, null=True, blank=True,related_name="new_intimation_wo_milestone_category_data")
    milestone_category_status = models.IntegerField(blank=True,null=True,default=1)

class New_FqpIntimation_Observation(models.Model):
    officer = models.ForeignKey('main.officer', on_delete=models.CASCADE, null=True, blank=True,related_name="new_inspecting_officer_data")
    fqpintimation = models.ForeignKey(New_FqpIntimation, on_delete=models.CASCADE, related_name="new_fqp_observation_detail",null=True, blank=True)
    new_fqpintimation_milestone_category = models.ForeignKey(New_FqpIntimation_milestone_category, on_delete=models.CASCADE,related_name="new_milestones_category_data",null=True, blank=True)
    milestone_main_category = models.ForeignKey(Milestone_Main_Category, on_delete=models.CASCADE, null=True, blank=True)
    milestone_subcategory_data = models.ForeignKey("main.Milestone_Main_SubCategory_Data", on_delete=models.CASCADE,related_name="new_milestones_observation_data",null=True, blank=True)
    # tkc_review_remark = models.CharField(max_length=500,null=True, blank=True)
    # tkc_review_status = models.IntegerField(default=0,null=True, blank=True) #  0 for pending and 1 for read by officer
    observation_count = models.IntegerField(default=0,null=True, blank=True)
    observation_image = models.FileField(upload_to='new_fqp_intimation/observation/',null=True, blank=True)
    observation_date = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    observation_remark = models.CharField(max_length=500,null=True, blank=True)
    observation_location = models.CharField(max_length=800,null=True, blank=True)
    observation_lat = models.CharField(max_length=100,null=True, blank=True)
    observation_long = models.CharField(max_length=100,null=True, blank=True)
    observation_status = models.IntegerField(default=0,null=True, blank=True)
    # status = models.IntegerField(default=0,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.observation_remark:
            return self.observation_remark
        else:
            return "Observation remark"


class New_FqpIntimation_Observation_data(models.Model):
    # user = models.ForeignKey(User_Registration,on_delete=models.CASCADE,blank=True,null=True)
    officer = models.ForeignKey('main.officer', on_delete=models.CASCADE, null=True, blank=True,related_name="re_survey_officer_data")
    observation = models.ForeignKey(New_FqpIntimation_Observation, on_delete=models.CASCADE, null=True, blank=True,related_name="observation_data")
    # milestone_subcategory_data = models.ForeignKey("main.Milestone_Main_SubCategory_Data", on_delete=models.CASCADE,related_name="new_milestones_data",null=True, blank=True)
    tkc_review_remark = models.CharField(max_length=500,null=True, blank=True)
    tkc_review_image = models.FileField(upload_to='new_fqp_intimation/observation/',null=True, blank=True)
    tkc_review_date = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    tkc_review_status = models.IntegerField(default=0,null=True, blank=True) #  0 for pending and 1 for accept and 2 for reject
    re_survey_remark = models.CharField(max_length=500,null=True, blank=True)
    re_survey_image = models.FileField(upload_to='new_fqp_intimation/observation/',null=True, blank=True)
    re_survey_date = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    re_survey_status = models.IntegerField(default=0,null=True, blank=True) #  0 for pending and 1 for accept and 2 for reject
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.tkc_review_remark:
            return self.tkc_review_remark
        else:
            return "Tkc review remark"



class New_FqpIntimation_Officer_Info(models.Model):
    officer = models.ForeignKey('main.officer', on_delete=models.CASCADE,null=True, blank=True)
    fqpintimation = models.ForeignKey(New_FqpIntimation, on_delete=models.CASCADE,null=True, blank=True)
    officer_fullname = models.CharField(max_length=500,null=True, blank=True)
    officer_designation = models.CharField(max_length=200,null=True, blank=True)
    representative_from = models.CharField(max_length=200,null=True, blank=True)
    officer_mobile = models.CharField(max_length=15,null=True, blank=True)
    status = models.IntegerField(default=1,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.officer_fullname:
            return self.officer_fullname
        else:
            return "Officer fullname"

class New_FqpIntimation_Observation_Close(models.Model):
    officer = models.ForeignKey('main.officer', on_delete=models.CASCADE,null=True, blank=True)
    fqpintimation = models.ForeignKey(New_FqpIntimation, on_delete=models.CASCADE,null=True, blank=True)
    image_1 = models.FileField(upload_to='new_fqp_intimation/observation_close/',null=True, blank=True)
    image_2 = models.FileField(upload_to='new_fqp_intimation/observation_close/',null=True, blank=True)
    image_3 = models.FileField(upload_to='new_fqp_intimation/observation_close/',null=True, blank=True)
    close_remark = models.CharField(max_length=500,null=True, blank=True)
    close_lat = models.CharField(max_length=100,null=True, blank=True)
    close_long = models.CharField(max_length=100,null=True, blank=True)
    status = models.IntegerField(default=0,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    def __str__(self):
        if self.close_remark:
            return self.close_remark
        else:
            return "close remark"


# --------------------new fqp intimation end here----------------------------------



class tkc_di_master_deleted_history(models.Model):
    id = models.AutoField(primary_key=True)
    wo = models.ForeignKey(TKCWoInfo, on_delete=models.CASCADE, null=True, blank=True)
    offer_no = models.CharField(max_length=200, null=True, blank=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    di_send_to_approval_status = models.BooleanField(default=False, blank=True)
    di_send_by_approval_by = models.CharField(max_length=300, null=True, blank=True)
    di_approved_status = models.IntegerField(default=0, blank=True)
    di_approved_by = models.CharField(max_length=300, null=True, blank=True)
    di_subject = models.CharField(max_length=1000, null=True, blank=True)
    erp_di_number  = models.CharField(max_length=200, null=True, blank=True)
    prefix = models.CharField(max_length=700, null=True, blank=True)
    term_and_condition = RichTextField(null=True, blank=True)
    copy_to = RichTextField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True,null=True)
    created_di_doc = models.FileField(upload_to='created_di_documents', null=True, blank=True)
    revised_di_created = models.BooleanField(default=False, blank=True,null = True)
