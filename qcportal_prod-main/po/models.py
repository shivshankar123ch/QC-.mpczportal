from django.db import models
from django.utils import timezone


# Create your models here.
class ProcurementInfo(models.Model):
    User_code = models.CharField(max_length=200, null=True, blank=True)
    user_name = models.CharField(max_length=200, null=True, blank=True)
    item_class = models.CharField(max_length=5, null=True, blank=True)
    item_category = models.CharField(max_length=200, null=True, blank=True)
    item_name = models.CharField(max_length=200, null=True, blank=True)
    item_quantity = models.IntegerField(blank=True)
    item_price = models.IntegerField(blank=True)
    specification = models.CharField(max_length=200, null=True, blank=True)
    tendor_no = models.CharField(max_length=50, null=True, blank=True)
    nit_no = models.CharField(max_length=50, null=True, blank=True)

    # Po_doc = models.FileField(null=True, blank=True)

    Po_doc = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    Po_GTP = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    Po_SD = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    Po_Material_Offer = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    Po_DI = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    Po_MRC = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    po_viewer = models.IntegerField(blank=True, default=0)
    # use value for approve 1 and rejected -1
    po_approver = models.IntegerField(blank=True, default=0)
    gtp_status = models.IntegerField(blank=True, default=0)
    gtp_approved = models.IntegerField(blank=True, default=0)
    bg_status = models.IntegerField(blank=True, default=0)
    bg_approved = models.IntegerField(blank=True, default=0)
    vendor_offer = models.IntegerField(blank=True, default=0)
    offer_approved = models.IntegerField(blank=True, default=0)
    # flag for po section approval
    di_status = models.IntegerField(blank=True, default=0)
    # flag for vendor section approval
    dispatch_status = models.IntegerField(blank=True, default=0)
    local_store_status = models.IntegerField(blank=True, default=0)
    dispatch_for_nabl = models.IntegerField(blank=True, default=0)
    po_test = models.IntegerField(blank=True, default=0)
    po_dispatch = models.IntegerField(blank=True, default=0)
    po_store = models.IntegerField(blank=True, default=0)
    temporary_rejection = models.IntegerField(blank=True, default=0)
    test_request_form = models.IntegerField(blank=True, default=0)
    TRF_Id = models.IntegerField(blank=True, default=0)

    def _str_(self):
        return self.ProcurementInfo_id



from ckeditor.fields import RichTextField


class Purchase_Order(models.Model):
    vendor = models.ForeignKey('main.User_Registration', on_delete=models.CASCADE, null=True, blank=True)
    discom = models.ForeignKey('main.Discom_Master', on_delete=models.CASCADE, null=True, blank=True)
    region_discom = models.ForeignKey('main.Region_Master', on_delete=models.CASCADE, null=True, blank=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    po_no = models.CharField(max_length=200, null=True, blank=True)
    po_prefix = models.CharField(max_length=300, null=True, blank=True)
    po_subject = models.CharField(max_length=500, null=True, blank=True)
    erp_created_date = models.DateField(null=True, blank=True)
    header = models.CharField(max_length=300, null=True, blank=True)
    header_creation_date = models.DateField(null=True, blank=True)
    header_created_by = models.CharField(max_length=300, null=True, blank=True)
    term_and_condition = RichTextField(null=True, blank=True)
    po_send_to_approval_status = models.IntegerField(default=0, blank=True)
    po_send_to_approval_at = models.DateField(null=True, blank=True)
    po_send_by_approval_by = models.CharField(max_length=300, null=True, blank=True)
    is_po_deleted = models.BooleanField(blank=True, default=False)
    po_deleted_date = models.DateField(null=True, blank=True)
    po_deleted_by = models.CharField(max_length=300, null=True, blank=True)
    po_approved_status = models.IntegerField(default=0, blank=True)
    po_approved_at = models.DateField(null=True, blank=True)
    po_approved_by = models.CharField(max_length=300, null=True, blank=True)
    po_digital_upload_status = models.IntegerField(default=0, blank=True)
    po_digital_upload_at = models.DateField(null=True, blank=True)
    po_digital_upload_by = models.CharField(max_length=300, null=True, blank=True)
    status = models.IntegerField(default=0, blank=True)

    Po_doc = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)
    po_approver = models.IntegerField(blank=True, default=0, null=True)
    gtp_status = models.IntegerField(blank=True, default=0, null=True)
    gtp_approved = models.IntegerField(blank=True, default=0)
    bg_status = models.IntegerField(blank=True, default=0)
    bg_approved = models.IntegerField(blank=True, default=0)
    vendor_offer = models.IntegerField(blank=True, default=0)
    offer_approved = models.IntegerField(blank=True, default=0)
    # po_date = models.DateField(null=True, blank=True)
    User_code = models.CharField(max_length=200, blank=True,null=True)
    item_category = models.CharField(max_length=200, null=True, blank=True)
    item_name = models.CharField(max_length=200, blank=True,null=True)
    item_quantity = models.IntegerField(blank=True, null=True)
    Po_GTP = models.FileField(upload_to='vendor/po/document/',null=True, blank=True)
    bank_details = models.IntegerField(blank=True, default=0)
    bank_details_approved = models.IntegerField(blank=True, default=0)
   
    vendor_offer = models.IntegerField(blank=True, default=0)
    offer_approved = models.IntegerField(blank=True, default=0)
    # flag for po section approval
    di_status = models.IntegerField(blank=True, default=0)
    # flag for vendor section approval
    dispatch_status = models.IntegerField(blank=True, default=0)
    temporary_rejection = models.IntegerField(blank=True, default=0)
    po_item_approved = models.BooleanField(blank=True, default=False)





class PO_SD(models.Model):
    po_no = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    bg_name = models.CharField(max_length=200, null=True, blank=True)
    bg_no = models.CharField(max_length=30, null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    valid_date = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    file = models.FileField(upload_to='vendor/po/document/', null=True, blank=True)







from tinymce import models as tinymce_models

class PO_Temp_Table(models.Model):
    PO_Temp_Table_Id = models.AutoField(primary_key=True)
    PO_type_Name = models.CharField(max_length=100, null=True, blank=True)
    PO_Clause_Name = models.CharField(max_length=200, null=True, blank=True)
    PO_Clause_Description = tinymce_models.HTMLField()
    PO_type_Id = models.IntegerField(blank=True, null=True, default=0)
    PO_Clause_Id = models.IntegerField(blank=True, null=True, default=0)

class TRF_Details(models.Model):
    TRF_Id = models.AutoField(primary_key=True)
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
    discom_name_radio = models.CharField(max_length=200, null=True, blank=True)
    nabl_name_sub_radio = models.CharField(max_length=200, null=True, blank=True)
    #############################################################################
    TRFAreastore_file = models.FileField(upload_to='TRFForms/', null=True, blank=True)
    trf_generated = models.IntegerField(blank=True, default=0)
    #****************************************************************************
    Gatepass = models.ForeignKey('main.Add_material_nabl', on_delete=models.CASCADE, null=True, blank=True)
    Test_name1 = models.IntegerField(blank=True, null=True, default=0)
    Test_name2 = models.IntegerField(blank=True, null=True, default=0)
    Test_name3 = models.IntegerField(blank=True, null=True, default=0)
    Test_name4 = models.IntegerField(blank=True, null=True, default=0)
    Test_name5 = models.IntegerField(blank=True, null=True, default=0)
    Test_name6 = models.IntegerField(blank=True, null=True, default=0)
    Test_name7 = models.IntegerField(blank=True, null=True, default=0)
    Test_name8 = models.IntegerField(blank=True, null=True, default=0)
    Test_name9 = models.IntegerField(blank=True, null=True, default=0)
    Test_name10 = models.IntegerField(blank=True, null=True, default=0)
  

class TRF_Test_Details(models.Model):
    TRF_Test_Id = models.IntegerField(blank=True, null=True, default=0)
    user_id = models.IntegerField(blank=True, default=0)
    ro_id = models.IntegerField(blank=True, default=0)
    gatepass_id = models.IntegerField(blank=True, default=0)
    po_id = models.CharField(max_length=200, null=True, blank=True)
    TRF_Id = models.IntegerField(blank=True, default=0)
    TRF_Test_Name = models.CharField(max_length=100, null=True, blank=True)
    TRF_Details = models.ForeignKey(TRF_Details, on_delete=models.CASCADE, null=True, blank=True)


class InspectingOfficerInfo(models.Model):
    officer_name = models.CharField(max_length=30, null=True, blank=True)
    contact_no = models.CharField(max_length=30, null=True, blank=True)
    officer_email = models.CharField(max_length=30, null=True, blank=True)
    officer_employ_id = models.CharField(max_length=30, null=True, blank=True)



class PO_Material(models.Model):
    po = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    specification = models.CharField(max_length=500, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    Quantity = models.FloatField(blank=True, default=0)
    Amount = models.FloatField(blank=True, default=0)
    total_amount = models.FloatField(blank=True, default=0)
    tax = models.FloatField(blank=True, default=0)
    status = models.IntegerField(blank=True, default=0)
    Offer = models.IntegerField(blank=True, default=0)
    item_code = models.CharField(max_length=50, null=True, blank=True)
    dispatch_qty = models.FloatField(blank=True, default=0)
    remaining_qty = models.FloatField(blank=True, default=0)




class PO_Copy(models.Model):
    po = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    copy = models.CharField(max_length=500, null=True, blank=True)


class PO_Schedule(models.Model):
    po = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    schedule_name = models.CharField(max_length=100, null=True, blank=True)
    schedule_description = models.CharField(max_length=1000, null=True, blank=True)

    def str(self):
        return self.PO_Schedule
        
    
    
#***********************************************************************************

class DI_Master(models.Model):
    po = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey('main.User_Registration', on_delete=models.CASCADE, null=True, blank=True)
    di_doc = models.FileField(upload_to='DI_documents', null=True, blank=True)
    zone = models.CharField(max_length=200, null=True, blank=True)
    po_no = models.CharField(max_length=200, null=True, blank=True)
    di_send_to_approval_status = models.BooleanField(default=False, blank=True)
    di_create_date = models.DateField(null=True, blank=True)
    di_send_by_approval_by = models.CharField(max_length=300, null=True, blank=True)
    is_di_deleted = models.BooleanField(blank=True, default=False)
    di_deleted_date = models.DateField(null=True, blank=True)
    di_deleted_by = models.CharField(max_length=300, null=True, blank=True)
    di_approved_status = models.IntegerField(default=0, blank=True)
    di_approved_date = models.DateField(null=True, blank=True)
    di_approved_by = models.CharField(max_length=300, null=True, blank=True)
    di_digital_upload_status = models.IntegerField(default=0, blank=True)
    di_digital_upload_date = models.DateField(null=True, blank=True)
    di_digital_upload_by = models.CharField(max_length=300, null=True, blank=True)
    vendor_deliverable_status = models.BooleanField(default=False, blank=True)
    status = models.IntegerField(default=0, blank=True)
    di_subject = models.CharField(max_length=200, null=True, blank=True)
    erp_di_number  = models.CharField(max_length=200, null=True, blank=True)
    prefix = models.CharField(max_length=200, null=True, blank=True)
    scheme_name = models.CharField(max_length=100, null=True, blank=True)
    scheme_code = models.IntegerField(blank=True, default=0)
    term_and_condition = RichTextField(null=True, blank=True)
    send_to_cgm = models.IntegerField(default=0, blank=True)
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_status = models.IntegerField(default=0, blank=True)
    nabl_number = models.CharField(max_length=100, null=True, blank=True)
    mrc_status = models.BooleanField(default=False, blank=True)


class PO_Material_Offer(models.Model):
    po = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    material = models.ForeignKey(PO_Material, on_delete=models.CASCADE, null=True, blank=True)
    Offer_Quantity = models.FloatField(blank=True, default=0)
    date = models.DateField(null=True, blank=True)
    status = models.IntegerField(blank=True, default=0)
    Offer = models.IntegerField(blank=True, default=0)
    total_quantity = models.FloatField(blank=True, default=0)
    item_name = models.CharField(max_length=500, null=True, blank=True)
    is_di_created = models.BooleanField(blank=True, default=False)
    dispatch_qty = models.FloatField(blank=True, default=0)
    remaining_qty = models.FloatField(blank=True, default=0)
    input_serial_no= models.CharField(max_length=100, null=True, blank=True)
    readiness_date = models.DateField(null=True, blank=True)
    item_code = models.CharField(max_length=50, null=True, blank=True,default=0)
    routine_report_file = models.ImageField(upload_to='Material_routine_test', null=True, blank=True)
    di_master = models.ForeignKey(DI_Master, on_delete=models.CASCADE, null=True, blank=True)  


class PO_Material_Offer_Serial_No(models.Model):
    offer = models.ForeignKey(PO_Material_Offer, on_delete=models.CASCADE, null=True, blank=True)
    serial_no = models.CharField(max_length=100, null=True, blank=True)
    Offer = models.IntegerField(blank=True, default=0)
    date = models.DateField(null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(blank=True, default=0)

class DI_Areastores(models.Model):
    po = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    offer_item = models.ForeignKey(PO_Material_Offer, on_delete=models.CASCADE, null=True, blank=True)
    # di_master = models.ForeignKey(DI_Master, on_delete=models.CASCADE, null=True, blank=True)
    areastore = models.CharField(max_length=300, null=True, blank=True)
    deliverable_qty = models.FloatField(blank=True, default=0)
    delivered_status = models.BooleanField(default=False, blank=True)
    status = models.BooleanField(default=False, blank=True)
    p_varification = models.BooleanField(default=False, blank=True)
    send_to_gm = models.IntegerField(blank=True, default=0)
    di_master = models.ForeignKey(DI_Master, on_delete=models.CASCADE, null=True, blank=True)
    gatepass = models.IntegerField(blank=True, default=0)
    material_sample_code = models.CharField(max_length=300, null=True, blank=True)
    zone = models.CharField(max_length=300, null=True, blank=True)
    send_to_nabl = models.IntegerField(default = 0, blank = True)
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_status = models.IntegerField(default = 0, blank = True)
    nabl_gatepass = models.IntegerField(default = 0, blank = True)
    nabl_number = models.CharField(max_length=15, null=True, blank=True)
    nabl_trf = models.IntegerField(default = 0, blank = True)
    sampling_flag = models.IntegerField(default = 0, blank = True)  
    samp_accepted_flag = models.IntegerField(default = 0, blank = True)
    samp_rejected_flag = models.IntegerField(default = 0, blank = True)
    resampling_flag = models.IntegerField(default = 0, blank = True)
    mrc_create_flag =models.BooleanField(blank=True, default=False)

 
class DI_copy(models.Model):
    di = models.IntegerField(default = 0, blank = True)
    copy_to = models.CharField(max_length=200, null=True, blank=True)


class DI_Material_Offer_Serial_No(models.Model):
    po = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(PO_Material_Offer, on_delete=models.CASCADE, null=True, blank=True)
    area_store = models.CharField(max_length=100, null=True, blank=True)
    serial_no = models.CharField(max_length=100, null=True, blank=True)
    Offer_status = models.IntegerField(blank=True, default=0)
    date = models.DateField(null=True, blank=True)
    material = models.CharField(max_length=1000, null=True, blank=True)
    status = models.IntegerField(blank=True, default=0)
    accepted = models.IntegerField(blank=True, default=0)
    p_status = models.IntegerField(blank=True, default=0)
    remark = models.CharField(max_length=100, null=True, blank=True)
    as_accepted = models.IntegerField(blank=True, default=0)
    nabl_reject_status = models.BooleanField(default=False, blank=True)
    batch_no = models.CharField(max_length=100, null=True, blank=True)
    batch_qty = models.FloatField(null=True, blank=True)

    date = models.DateField(null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(blank=True, default=0)
    area_store_id = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True)
    received_material = models.IntegerField(blank=True, default=0,null=True)


class po_gatepass(models.Model):
    area_store = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True)
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
    aname = models.CharField(max_length=200, null=True, blank=True)

class DI_nabl_rejected_gatepass(models.Model):
    area_store = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True)
    gatepass_num=models.CharField(max_length=200, null=True, blank=True)
    gatekeeper_name=models.CharField(max_length=200, null=True, blank=True)
    vehicle_no=models.CharField(max_length=200, null=True, blank=True)
    driver_name=models.CharField(max_length=200, null=True, blank=True)
    driver_phone=models.CharField(max_length=50, null=True, blank=True)
    gatepass_date=models.DateField(null=True, blank=True)
    material_rec_by=models.CharField(max_length=200, null=True, blank=True)
    outward_quantity=models.IntegerField(blank=True, default=0)
    gatepass_flag=models.IntegerField(blank=True, default=0)
    driver_aadhar=models.FileField(upload_to='documents/rca/all_xmr_report', null=True, blank=True)
    aname = models.CharField(max_length=50, null=True, blank=True)

class po_nabl_gatepass(models.Model):
    id = models.AutoField(primary_key=True)
    area_store = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True, related_name="ar_store")
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
    aname = models.CharField(max_length=150, null=True, blank=True)
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_number = models.CharField(max_length=15, null=True, blank=True)
    gatepass=models.FileField(upload_to='documents/po/gatepasses', null=True, blank=True)

class PO_TRF_Details(models.Model):
    TRF_Id = models.AutoField(primary_key=True)
    area_store_id = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True)
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
    #######################################
    discom_name_radio = models.CharField(max_length=200, null=True, blank=True)
    nabl_name_sub_radio = models.CharField(max_length=200, null=True, blank=True)
    gatepass_doc = models.ForeignKey('po_nabl_gatepass', on_delete=models.CASCADE, null=True, blank=True)
    trf_file = models.FileField(upload_to='TRFForms/', null=True, blank=True)    


class po_drr_info(models.Model):
    area_store = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True)
    drr_date=models.DateField(null=True, blank=True)
    drr_vehicle=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_no=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_date=models.DateField(null=True, blank=True)
    drr_quantity=models.FloatField(blank=True, default=0)
    # drr_DI_quantity=models.IntegerField(blank=True, default=0)
    
    
class po_nabl_gatepass_outward(models.Model):
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
    UserOutward = models.ForeignKey('main.User_Registration', on_delete=models.CASCADE, null=True, blank=True)
    Zone = models.CharField(max_length=500, null=True, blank=True)
    trfid = models.IntegerField(blank=True, null=True, default=0)
    login_number = models.CharField(max_length=500, null=True, blank=True)
    gatepassAreaStoreOutward_file = models.FileField(upload_to='Gatepass/NABL/CP/', blank=True, null=True)
    gatepassOutward_generated = models.IntegerField(blank=True, null=True, default=0)
    nabl_outward_count_id = models.IntegerField(blank=True, null=True, default=0)


class sample_code_table_cp(models.Model):
    di_area_store = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.CharField(max_length=1500, null=True, blank=True)
    TRF_Id = models.CharField(max_length=1500, null=True, blank=True)
    material_serial_number = models.CharField(max_length=2000, null=True, blank=True)
    material_name = models.CharField(max_length=2000, null=True, blank=True)
    company_name = models.CharField(max_length=2000, null=True, default="", blank=True)
    Gatepass = models.ForeignKey(po_nabl_gatepass, on_delete=models.CASCADE, null=True, blank=True)
    officer_id = models.CharField(max_length=200, null=True, default="", blank=True)
    rejection_yes_no = models.CharField(max_length=200, null=True, default="", blank=True)
    rejection_remark = models.CharField(max_length=200, null=True, default="", blank=True)
    rejected_date = models.CharField(max_length=200, null=True, default="", blank=True)
    phy_accepted = models.IntegerField(blank=True, null=True, default=0)
    phy_rejected = models.IntegerField(blank=True, null=True, default=0)
    result_pass = models.IntegerField(blank=True, null=True)
    sampleCode_report = models.FileField(upload_to='NABL_Report/', blank=True, null=True)
    FinalRemark = models.CharField(max_length=500, null=True, blank=True)           
    report_date = models.DateTimeField(null=True, blank=True)
    outward_generated = models.IntegerField(null=True, blank=True, default=0)
    GatepassOutward = models.ForeignKey(po_nabl_gatepass_outward, on_delete=models.CASCADE, null=True, blank=True)
    #######################################################################################
    ro_id = models.IntegerField(blank=True, default=0)
    outward_gatepass_id = models.IntegerField(blank=True, default=0)
    sample_code = models.CharField(max_length=200, null=True, default="", blank=True )
    date = models.CharField(max_length=200, null=True, default="", blank=True)
    rejected_sample_code = models.CharField(max_length=200, null=True, default="", blank=True)
    rejected_vehicle_number = models.CharField(max_length=200, null=True, default="", blank=True)
    is_rejected = models.IntegerField(blank=True, null=True, default=0)
    sent_to_phy_replaced = models.IntegerField(blank=True, null=True, default=0)
    outward_pass = models.IntegerField(blank=True, null=True, default=0)
    outward_driver_name = models.CharField(max_length=200, null=True, default="", blank=True)
    outward_vehicle_number = models.CharField(max_length=200, null=True, default="", blank=True)
    outward_driver_mobile = models.CharField(max_length=15, null=True, blank=True)
    outward_date = models.DateField(null=True, blank=True)
    material_rating = models.CharField(max_length=200, null=True, default="", blank=True)
    gatepass_Submitted_by = models.CharField(max_length=200, null=True, default="", blank=True)
    Test_Request_Form_submitted_by = models.CharField(max_length=200, null=True, default="", blank=True)
    XMRList = models.CharField(max_length=200, null=True, blank=True)
    CapacityList = models.CharField(max_length=200, null=True, blank=True)
    TypeList = models.CharField(max_length=200, null=True, blank=True)
    RemarkList = models.CharField(max_length=200, null=True, blank=True)
    machine_tested = models.IntegerField(null=True, blank=True, default=0)

class purchase_mrc_details(models.Model):
    ro = models.ForeignKey(DI_Areastores, on_delete=models.CASCADE, null=True, blank=True)
    mrc_date=models.DateField(null=True, blank=True)
    digi_sign_pr=models.FileField(upload_to='media/documents/po/po_mrc', null=True, blank=True)
    digi_flag_pr=models.IntegerField(blank=True, default=0)

    def str(self):
        return self.purchase_mrc_details

class purchase_mrc_copy(models.Model):
    ro = models.ForeignKey(purchase_mrc_details, on_delete=models.CASCADE, null=True, blank=True)
    copy_name = models.CharField(max_length=100, null=True, blank=True)

    def str(self):
        return self.purchase_mrc_copy

class purchase_mrc_comment(models.Model):
    ro = models.ForeignKey(purchase_mrc_details, on_delete=models.CASCADE, null=True, blank=True)
    add_comment = models.CharField(max_length=1000, null=True, blank=True)

    def str(self):
        return self.purchase_mrc_comment