from django.db import models
from main.models import User_Registration


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
    Primary_verification_Status_approver = models.IntegerField(blank=True, default=0, null=True)
    Approver_Status = models.IntegerField(blank=True, default=0, null=True)


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
    

class SiteStore_Master(models.Model):
    Division = models.ForeignKey("main.Division_Master", on_delete=models.CASCADE)
    Store_Address = models.CharField(max_length=150, null=True, blank=True)
    supplier = models.ForeignKey("main.User_Registration",on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    rent_agreement_copy = models.FileField(upload_to='tkc/Site Store Data/Site Store Rent Agreement')
    electricity_bill = models.FileField(upload_to='tkc/Site Store Data/Site Store Electricity')
    consumer_no = models.CharField(max_length=100)
    contact_no = models.IntegerField()
    autherised_person = models.CharField(max_length=100)
    man_power = models.IntegerField()
    otp = models.IntegerField(null=True, blank=True)

class sitestore_circle(models.Model):
    tkc_sitestore = models.ForeignKey(SiteStore_Master, on_delete=models.CASCADE, null=True, blank=True)
    circle = models.ForeignKey("main.Circle_Master", on_delete=models.CASCADE, null=True, blank=True)
    circle_name = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)




# class Wo_Material_Dispatch_details(models.Model):
#     tkc_di = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)
#     wo = models.ForeignKey("fqp.TKCWoInfo", on_delete=models.CASCADE, null=True, blank=True)
#     wo_material = models.ForeignKey("fqp.Offer_Material", on_delete=models.CASCADE, null=True, blank=True) 
#     quantity = models.IntegerField(blank=True, default=0)
#     Division = models.ForeignKey("main.Division_Master", on_delete=models.CASCADE)
#     supplier = models.ForeignKey("main.User_Registration",on_delete=models.CASCADE, null=True, blank=True)
    # Store_Address = models.CharField(max_length=150, null=True, blank=True)
#     created_at = models.DateField(auto_now_add=True)
#     delivery_status = models.IntegerField(blank=True, default=0, null=True)
    # nabl_status = models.IntegerField(blank=True, default=0, null=True)




class offer_material_site_stores(models.Model):
    wo = models.ForeignKey("fqp.TKCWoInfo", on_delete=models.CASCADE, null=True, blank=True)
    wo_material = models.ForeignKey("fqp.tkc_wo_items_boq", on_delete=models.CASCADE, null=True, blank=True)
    tkc_di = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.FloatField(blank=True, default=0)
    site_store = models.CharField(max_length=150, null=True, blank=True)
    supplier = models.ForeignKey("main.User_Registration",on_delete=models.CASCADE, null=True, blank=True)
    is_serial_excel_uploaded = models.BooleanField(default=False)
    is_di_created = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now_add=True, null=True, blank=True)
    TKCVendor = models.ForeignKey("fqp.TKCVendor", on_delete=models.CASCADE, null=True, blank=True)
    Calibration_Certificate = models.FileField(upload_to='TKC/FQP/Test/', null=True, blank=True)
    Material_Offer_Submit = models.IntegerField(default=0, blank=True)
    Material_Offer_Submit_Submit_At = models.DateTimeField(null=True, blank=True)
    Material_Offer_Submit_Approved_Remark = models.CharField(max_length=300, null=True, blank=True)
    Material_Offer_Submit_Approved_Status = models.IntegerField(default=0, blank=True)
    Material_Offer_Submit_Approved_At = models.DateTimeField(null=True, blank=True)
    Material_Offer_Submit_Approved_By = models.CharField(max_length=300, null=True, blank=True)
    Quantity_Inspected = models.FloatField(null=True, blank=True)
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
    PDI_Approved_Status = models.IntegerField(default=0,null=True, blank=True)
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
    Status = models.IntegerField(null=True, blank=True, default=0)
    nabl_status = models.IntegerField(null=True, blank=True, default=0)
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_number = models.CharField(max_length=15, null=True, blank=True)
    nabl_gatepass = models.IntegerField(null=True, blank=True, default=0)
    send_to_nabl = models.IntegerField(null=True, blank=True, default=0)
    send_to_cgm = models.IntegerField(null=True, blank=True, default=0) 
    Signed_Remark = models.CharField(max_length=500, null=True, blank=True)  # add for data forund or not found mobile side that remark----> add by shubham tripathi 
    Signed_Status = models.IntegerField(null=True, blank=True, default=0)  # if data found in mobile app side then status 1 and else not 0  ----> add by shubham tripathi 
    phy_reject_nabl = models.IntegerField(null=True, blank=True, default=0)
    is_offered = models.BooleanField(default=False)
    offer_no = models.CharField(max_length=500, null=True, blank=True)
    offer_material_docs = models.FileField(upload_to='TKC/FQP/tkc_offer_material_docs/', null=True, blank=True)
    input_serial_number = models.CharField(max_length=500, null=True, blank=True)
    sampling = models.IntegerField(null=True, blank=True, default=0)
    nabl_gatepass_status = models.IntegerField(blank=True, default=0, null=True)
    trf_status = models.IntegerField(blank=True, default=0, null=True) # when trf is generated
    gatepass = models.IntegerField(blank=True, default=0)
    site_store_fk = models.ForeignKey(SiteStore_Master, on_delete=models.CASCADE, null=True, blank=True)
    officer_checked = models.IntegerField(blank=True, default=0)
    report=models.FileField(upload_to='TRFForms/reports/', null=True, blank=True)
    readiness_date = models.DateField(null=True, blank=True)
    ready_quantity=models.FloatField(blank=True, default=0, null=True)
    passed_quantity=models.FloatField(blank=True, default=0, null=True)
    failed_quantity=models.FloatField(blank=True, default=0, null=True)
    circle = models.ForeignKey("main.Circle_Master", on_delete=models.CASCADE, null=True, blank=True)
    Physical_Status_officer = models.IntegerField(default=0, blank=True)
    officer_assined = models.IntegerField(default=0, blank=True)
    final_check = models.IntegerField(default=0, blank=True)
    accept_from_nabl = models.IntegerField(default=0, blank=True)
    resampled_requred = models.IntegerField(default=0, blank=True)
    received_from_nabl = models.IntegerField(default=0, blank=True)
    tkc_mrc_initiate=models.IntegerField(blank=True,default=0)
    balance_quantity = models.FloatField(null=True, blank=True, default=0)
    already_dispatch_qty = models.FloatField(null=True, blank=True, default=0)
    excel_type = models.BooleanField(null=True, blank=True)
    is_di_required = models.BooleanField(null=True, blank=True)
    is_pdi_required = models.BooleanField(null=True, blank=True) 
    is_sampling_required = models.BooleanField(null=True, blank=True)
    material_category = models.CharField(max_length=500, null=True, blank=True)
    tkc_mrc = models.ForeignKey("tkc.create_mrc", on_delete=models.CASCADE, null=True, blank=True)
    di_offer_ref_no = models.CharField(max_length=500, null=True, blank=True)
    vendor_factory_address = models.CharField(max_length=500, null=True, blank=True)
    site_store_gatepass = models.IntegerField(null=True, blank=True, default=0)# status 1 created 0 not created shubham tripatii
    nabl_user = models.ForeignKey("main.User_Registration", on_delete=models.CASCADE, null=True,blank=True,related_name="nabl_company_data" )

class nabl_wo_outward_gatepass(models.Model):
    gatepass_num=models.CharField(max_length=200, null=True, blank=True)
    gatekeeper_name=models.CharField(max_length=200, null=True, blank=True)
    vehicle_no=models.CharField(max_length=200, null=True, blank=True)
    driver_name=models.CharField(max_length=200, null=True, blank=True)
    driver_phone=models.CharField(max_length=15, null=True, blank=True)
    gatepass_date=models.DateField(null=True, blank=True)
    material_rec_by=models.CharField(max_length=200, null=True, blank=True)
    driver_aadhar=models.FileField(upload_to='documents/rca/all_xmr_report', null=True, blank=True)
    offer_no=models.CharField(max_length=500, null=True, blank=True)
    gatepass_letter=models.FileField(upload_to='documents/nabl/gatepass', null=True, blank=True)  
    site_store = models.ForeignKey(SiteStore_Master, on_delete=models.CASCADE, null=True, blank=True)
    nabl_user = models.ForeignKey("main.User_Registration", on_delete=models.CASCADE, null=True,blank=True)
    tkc_di = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)




class wo_outward_gatepass(models.Model):
    offer = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)
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
    

class tkc_site_store_drr_info(models.Model):
    area_store = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)
    drr_date=models.DateField(null=True, blank=True)
    drr_vehicle=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_no=models.CharField(max_length=100, null=True, blank=True)
    drr_challan_date=models.DateField(null=True, blank=True)
    drr_quantity=models.IntegerField(blank=True, default=0)
   

class tkc_wo_nabl_gatepass(models.Model):
    offer_number = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)    
    gatepass_num=models.CharField(max_length=200, null=True, blank=True)
    gatekeeper_name=models.CharField(max_length=200, null=True, blank=True)
    vehicle_no=models.CharField(max_length=200, null=True, blank=True)
    driver_name=models.CharField(max_length=200, null=True, blank=True)
    driver_phone=models.CharField(max_length=100, null=True, blank=True)
    gatepass_date=models.DateField(null=True, blank=True)
    material_rec_by=models.CharField(max_length=200, null=True, blank=True)
    outward_quantity=models.IntegerField(blank=True, default=0)
    gatepass_flag=models.IntegerField(blank=True, default=0)
    Division = models.ForeignKey("main.Division_Master", on_delete=models.CASCADE, null=True, blank=True)
    aname = models.CharField(max_length=50, null=True, blank=True)
    Store_Address = models.CharField(max_length=150, null=True, blank=True)#add by shubham tripathi 
    driver_aadhar=models.FileField(upload_to='documents/tkc_gatepass/aadhar_card', null=True, blank=True)
    gate_pass = models.FileField(upload_to='documents/tkc_gatepass/gatepass', null=True, blank=True)

    offer_no=models.CharField(max_length=500, null=True, blank=True) #add by shubham tripahti
    site_store = models.ForeignKey(SiteStore_Master, on_delete=models.CASCADE, null=True, blank=True)
    nabl_user = models.ForeignKey("main.User_Registration", on_delete=models.CASCADE, null=True,blank=True)
    tkc_di = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)
    nabl_gatepass=models.BooleanField(null=True,blank=True)




class Tkc_Work_Order_Trf_Details(models.Model):
    TRF_Id = models.AutoField(primary_key=True)

    user_id = models.IntegerField(blank=True, default=0)
    ro_id = models.IntegerField(blank=True, default=0)
    outward_gatepass_id = models.IntegerField(blank=True, default=0)
    po_id = models.CharField(max_length=200, null=True, blank=True)
    gatepass_id = models.IntegerField(blank=True, null=True,default=0)
    customer_Organization_name = models.CharField(max_length=200, null=True, blank=True)
    customer_Organization_address = models.CharField(max_length=200, null=True, blank=True)
    contact_person_name = models.CharField(max_length=200, null=True, blank=True)
    mobile_no = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    name_of_sample_product = models.CharField(max_length=200, null=True, blank=True)
    customer_ref_gatepass_no = models.CharField(max_length=200, null=True, blank=True)
    dated = models.CharField(max_length=50, null=True, blank=True)
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
    nabl_name = models.CharField(max_length=100, null=True, blank=True)
    nabl_number = models.CharField(max_length=15, null=True, blank=True)   
    offer_number = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)# it is for old pattern 

    recv_incharge = models.CharField(max_length=200, null=True, blank=True) 
    tech_manager = models.CharField(max_length=200, null=True, blank=True)
    tender_generated = models.IntegerField(blank=True, default=0)
    TRFAreastore_file = models.FileField(upload_to='TRFForms/', null=True, blank=True)    
    offer_no = models.CharField(max_length=200, null=True, blank=True) # offer no add by shubham tripathi gate data offerwise and tkc_di_id  
    tkc_di = models.ForeignKey("fqp.tkc_di_master", on_delete=models.CASCADE, null=True, blank=True) # offer no add by shubham tripathi gate data offerwise and tkc_di_id  
    nabl_user = models.ForeignKey("main.User_Registration", on_delete=models.CASCADE, null=True, blank=True) # offer no add by shubham tripathi gate data offerwise and tkc_di_id  
    site_store_gatepass = models.ForeignKey(tkc_wo_nabl_gatepass, on_delete=models.CASCADE, null=True, blank=True) # offer no add by shubham tripathi gate data offerwise and tkc_di_id  
    trf_generated = models.IntegerField(blank=True, default=0)
    areastore = models.CharField(max_length=200, null=True, blank=True)
    


class offer_material_serial_number(models.Model):
    offer = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)
    wo = models.ForeignKey("fqp.TKCWoInfo", on_delete=models.CASCADE, null=True, blank=True)
    wo_material = models.ForeignKey("fqp.tkc_wo_items_boq", on_delete=models.CASCADE, null=True, blank=True)
    tkc_di = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)
    site_store = models.CharField(max_length=150, null=True, blank=True)
    serial_no = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    is_di_created = models.BooleanField(default=False, null=True, blank=True)
    Physical_Status = models.IntegerField(default=0, blank=True)
    Status = models.IntegerField(null=True, blank=True, default=0)
    remark = models.CharField(max_length=150, null=True, blank=True)
    is_sampled = models.IntegerField(null=True, blank=True, default=0)
    accepted = models.IntegerField(blank=True, default=0)
    gatepass = models.IntegerField(blank=True, default=0)
    gatepass_number = models.ForeignKey("tkc.wo_outward_gatepass", on_delete=models.CASCADE, null=True, blank=True)
    offer_no = models.CharField(max_length=500, null=True, blank=True)
    batch_no = models.CharField(max_length=100, null=True, blank=True)
    batch_qty = models.FloatField(null=True, blank=True)
    Physical_Status_officer_check = models.IntegerField(default=0, blank=True)
    nabl_report = models.FileField(upload_to='documents/nabl_report', null=True, blank=True)
    result = models.IntegerField(blank=True, default=0)
    Physical_Status_Nabl = models.IntegerField(blank=True, default=0)
    sampled_by=models.ForeignKey("main.officer", on_delete=models.CASCADE, null=True, blank=True)
    sampled_date=models.DateField(null=True, blank=True)
# -----------------
    # gatepass_created_status = models.BooleanField(blank=True, default=False)
    nabl_date=models.DateField(null=True, blank=True)
    nabl_remark=models.CharField(max_length=500,blank=True,null=True)
    nabl_status=models.BooleanField(null=True,blank=True, default=False)
    site_store_gatepass = models.ForeignKey(tkc_wo_nabl_gatepass, on_delete=models.CASCADE, null=True, blank=True)
    site_store_trf = models.ForeignKey(Tkc_Work_Order_Trf_Details, on_delete=models.CASCADE, null=True, blank=True)
    nabl_outward_gatepass=models.ForeignKey(nabl_wo_outward_gatepass,on_delete=models.CASCADE,null=True,blank=True)
#-----------------------------------------
    # nabl_selection_status=models.BooleanField(null=True,blank=True, default=False)
    
    


class tkc_wo_nabl_gatepass_detail(models.Model):# add by shubham tripati we use this table for store gatepass and trf data
    wo_trf = models.ForeignKey(Tkc_Work_Order_Trf_Details, on_delete=models.CASCADE, null=True, blank=True, related_name="trf_data")
    gatepass = models.ForeignKey(tkc_wo_nabl_gatepass, on_delete=models.CASCADE, null=True, blank=True)
    wo_material = models.ForeignKey("fqp.tkc_wo_items_boq", on_delete=models.CASCADE, null=True, blank=True)
    serial_no = models.ForeignKey(offer_material_serial_number, on_delete=models.CASCADE, null=True, blank=True)
    outward_quantity=models.IntegerField(blank=True, default=0)
    delete_status=models.IntegerField(null=True, blank=True,default=1)
    tkc_di = models.ForeignKey("fqp.tkc_di_master", on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)
 



class pi_verification_offier(models.Model):
    site_store = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    designation=models.CharField(max_length=50, null=True, blank=True)
    officer_from=models.CharField(max_length=50, null=True, blank=True)
    mobile=models.CharField(max_length=15, null=True, blank=True)
    report=models.FileField(upload_to='TRFForms/', null=True, blank=True)


#------------------------------------- START OF MODELS BY RAVINDRA & GAURAV------------------------------------------#

class TKC_Consumer(models.Model):
    estimate_name = models.CharField(max_length=500,default=0,null=True, blank=True)
    kwload = models.CharField(max_length=100, null=True, blank=True) 
    consumer_mobile_no = models.CharField(max_length=30, null=True, blank=True) 
    sgst = models.CharField(max_length=30, null=True, blank=True) 
    consumerApplicationNo = models.CharField(max_length=100, null=True, blank=True)
    cgst = models.CharField(max_length=30, null=True, blank=True) 
    consumer_email_id = models.CharField(max_length=100, null=True, blank=True) 
    approved_by = models.CharField(max_length=100, null=True, blank=True) 
    to_char = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True) 
    schema = models.CharField(max_length=100, null=True, blank=True) 
    kvaload = models.CharField(max_length=50, null=True, blank=True) 
    deposit_amount = models.CharField(max_length=100, null=True, blank=True) 
    shortDescriptionOfWork = models.TextField(max_length=100, null=True, blank=True) 
    erp_no = models.CharField(max_length=100, null=True, blank=True) 
    supervision_amount = models.CharField(max_length=100, null=True, blank=True) 
    consumerName = models.CharField(max_length=100, null=True, blank=True) 
    bid_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    bid_modified = models.DateTimeField(auto_now=True,null=True, blank=True)
    bid_expiry = models.DateTimeField(editable=True,null=True, blank=True)
    is_bid_submitted = models.BooleanField(default=False)

class TKC_Consumer_bid(models.Model):
    consumers = models.ForeignKey(TKC_Consumer, on_delete=models.CASCADE)
    User_Id = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    bid_amount = models.FloatField(max_length=100, null=True, blank=True, default = 0)
    bid_order_at = models.DateTimeField(auto_now_add=True)
    contractor_category = models.CharField(max_length=15,null=True, blank=True,default=0)
    
class TKC_ContractorSelections(models.Model):
    User_Id = models.ForeignKey(User_Registration, on_delete=models.CASCADE)
    consumers = models.ForeignKey(TKC_Consumer, on_delete=models.CASCADE)
    contractor_category = models.ForeignKey(TKC_Payment, on_delete=models.CASCADE, null=True, blank=True,default="")
    is_participated = models.BooleanField(default=None,null=True,blank=True)
    
class TKC_bid_not_participated(models.Model):
    User_Id = models.ForeignKey(User_Registration, on_delete=models.CASCADE)
    consumers = models.ForeignKey(TKC_Consumer, on_delete=models.CASCADE,blank=True, null=True)
    is_rejected = models.BooleanField(default=None,null=True,blank=True)
    consumer_application_no = models.CharField(max_length=100, blank=True, null=True)
    consumerName = models.CharField(max_length=100, null=True, blank=True) 
    shortDescriptionOfWork = models.TextField(max_length=100, null=True, blank=True) 
    
class TKC_contractor_work(models.Model):
    User_Id = models.ForeignKey(User_Registration, on_delete=models.CASCADE, null=True, blank=True)
    consumers = models.ForeignKey(TKC_Consumer, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.CharField(max_length= 200,blank=True,null=True)
    vendor_material_specification = models.CharField(max_length= 500,blank=True,null=True)
    transformer_serial_no = models.CharField(max_length= 200,blank=True,null=True)
    documents_for_material = models.FileField(upload_to='documents/material_testing_report',null=True, blank=True)
    contractor_work_started = models.CharField(max_length=100, blank=True,editable=True)
    material_handover_site = models.CharField(max_length=100, blank=True,editable=True)
    material_installation_start = models.CharField(max_length=100, blank=True,editable=True)
    material_installation_finished = models.CharField(max_length=100, blank=True,editable=True)
    contractor_work_completed = models.CharField(max_length=100, blank=True,editable=True)
    ptr = models.BooleanField(default=False)
    dtr = models.BooleanField(default=False)
    lt = models.BooleanField(default=False)
    ht_11kv = models.BooleanField(default=False)
    ht_33kv = models.BooleanField(default=False)
    ht_132kv = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=None,null=True, blank=True)
    
#-----------------------------------END OF MODELS BY RAVINDRA---------------------------------------------------#

#--------- Models by Gaurav Pathak

class create_mrc(models.Model):
    offer = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null = True, blank= True)
    date = models.DateField(null=True, blank=True)
    digi_sign = models.FileField(upload_to='documents/fqp_sign/tkc_mrc_sign',null=True, blank=True)
    digi_signflag = models.IntegerField(blank=True, default=0)
    remark = models.CharField(max_length=2000, null=True, blank=True)
    tkc_di = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)
    circle = models.ForeignKey("main.Circle_Master", on_delete=models.CASCADE, null=True, blank=True)
    
    
#---------- end of models by Gaurav Pathak


class  works_master(models.Model):
    package_name = models.CharField(max_length=200,null=True, blank=True)



#Added By Aayush For DI api Integration.
class Offered_Item_Remaining_Quantity(models.Model):
    offer_no = models.CharField(max_length=100, null=True, blank=True)
    item_code  = models.CharField(max_length=200, null=True, blank=True)
    remaining_quantity  =  models.FloatField(default=0, blank=True)
    total_quantity  =  models.FloatField(default=0, blank=True)
    already_di_issued_quantity  =  models.FloatField(default=0, blank=True)

class di_receiving_details_data(models.Model):
    wo = models.ForeignKey("fqp.TKCWoInfo", on_delete=models.CASCADE, null=True, blank=True)
    di_obj = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)
    offer_obj = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)
    receiving_ref_number=models.CharField(max_length=100, null=True, blank=True)
    di_receiver_name=models.CharField(max_length=500, null=True, blank=True)
    erp_di_number=models.CharField(max_length=100, null=True, blank=True)
    rec_delievery_date= models.DateTimeField(auto_now_add=True,null=True, blank=True)
    receiving_location=models.CharField(max_length=100, null=True, blank=True)
    inspection_number=models.CharField(max_length=100, null=True, blank=True)
    inspection_date=models.DateTimeField(auto_now_add=True,null=True, blank=True)
    receiving_item_code=models.CharField(max_length=100, null=True, blank=True)
    receiving_item_code_desc=models.CharField(max_length=100, null=True, blank=True)
    receiving_quantity=models.FloatField(default=0, blank=True)
    receiving_remarks=models.CharField(max_length=100, null=True, blank=True)

class di_mapping(models.Model):
    wo = models.ForeignKey("fqp.TKCWoInfo", on_delete=models.CASCADE, null=True, blank=True)
    di_quantity  =  models.FloatField(default=0, blank=True)
    di_obj = models.ForeignKey("fqp.tkc_di_master",on_delete=models.CASCADE, null=True, blank=True)
    offer_obj = models.ForeignKey(offer_material_site_stores, on_delete=models.CASCADE, null=True, blank=True)
    erp_di_number=models.CharField(max_length=100, null=True, blank=True)
    uom = models.CharField(max_length=500, null=True, blank=True)
    di_receiver_name=models.CharField(max_length=500, null=True, blank=True)
    # discom = models.CharField(max_length=100, null=True, blank=True)



