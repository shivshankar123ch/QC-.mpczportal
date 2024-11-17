from django.db import models


class NABL_Document(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Types_of_Docs = models.CharField(max_length=100, null=True, blank=True)
    Issued_office_Name = models.CharField(max_length=50, null=True, blank=True)
    Document_Name = models.CharField(max_length=50, null=True, blank=True)
    Doc_issue_date = models.DateField(default=None, null=True)
    Doc_expiry_date = models.DateField(default=None, null=True)
    Ddocfile = models.FileField(upload_to='documents/vendor/work_data', null=True, blank=True,default='documents/No_Preview.pdf')
    Primary_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    Primary_remark = models.CharField(max_length=100, null=True, blank=True)
    Primary_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    Primary_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    CGM_verification_Date = models.DateTimeField(auto_now_add=True, null=True)
    CGM_remark = models.CharField(max_length=100, null=True, blank=True)
    CGM_verification_Status = models.IntegerField(blank=True, default=0, null=True)
    CGM_remark_rejection_counter = models.IntegerField(blank=True, default=0, null=True)
    Status = models.IntegerField(blank=True, default=0, null=True)
    Uploaded_Date = models.DateTimeField(auto_now_add=True)
    Updated_Date = models.DateTimeField(auto_now=True, null=True)



class NABL_Registration_Test(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Material_Name = models.CharField(max_length=1000, null=True, blank=True)
    Material_Specification_Name = models.CharField(max_length=1000, null=True, blank=True)
    Material_Item_Code = models.CharField(max_length=100, null=True, blank=True)
    Material_IS = models.CharField(max_length=100, null=True, blank=True)
    Material_Certificate_Name = models.CharField(max_length=500, null=True, blank=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Created_by = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)
    material_code_ez = models.CharField(max_length=50, null=True, blank=True)
    material_code_wz = models.CharField(max_length=50, null=True, blank=True)


class NABL_Perform_Test(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    Material = models.CharField(max_length=200, null=True, blank=True)
    Test_Id = models.CharField(max_length=1000, null=True, blank=True)
    Test_Name = models.CharField(max_length=1000, null=True, blank=True)
    Created_by = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)
    test = models.CharField(max_length=50, null=True, blank=True)


class Product(models.Model):
    Product_id = models.AutoField(primary_key=True)
    IST_name = models.CharField(max_length=200, null=True, blank=True)
    Product_Name = models.CharField(max_length=200, null=True, blank=True)
    Created_date = models.CharField(max_length=50, null=True, blank=True)
    Created_by = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)


class Product_Specification(models.Model):
    Product_id = models.CharField(max_length=10, null=True, blank=True)
    Product_Code = models.CharField(max_length=50, null=True, blank=True)
    Product_Specification = models.CharField(max_length=500, null=True, blank=True)
    Product_Unit = models.CharField(max_length=100, null=True, blank=True)
    Product_GST = models.CharField(max_length=100, null=True, blank=True)
    Product_Price = models.CharField(max_length=100, null=True, blank=True)
    Created_date = models.CharField(max_length=50, null=True, blank=True)
    Created_by = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)


class List_Of_Test(models.Model):
    Product_Id = models.CharField(max_length=10, null=True, blank=True)
    Test_Name = models.CharField(max_length=500, null=True, blank=True)
    Created_date = models.CharField(max_length=50, null=True, blank=True)
    Created_by = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)


class Product_List_Of_Test(models.Model):
    Product_id = models.CharField(max_length=10, null=True, blank=True)
    Test_id = models.CharField(max_length=15, null=True, blank=True)
    Created_date = models.CharField(max_length=50, null=True, blank=True)
    Created_by = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)


class Perform_Test_By_NABL(models.Model):
    NABL_User_Id = models.CharField(max_length=15, null=True, blank=True)
    Product_Specification_id = models.CharField(max_length=15, null=True, blank=True)
    Test_id = models.CharField(max_length=15, null=True, blank=True)
    Created_date = models.CharField(max_length=50, null=True, blank=True)
    Created_by = models.CharField(max_length=50, null=True, blank=True)
    Status = models.CharField(max_length=50, null=True, blank=True)


class Nabl_Test_Report(models.Model):
    TRF_Id = models.CharField(max_length=15, null=True, blank=True)
    ReportFile = models.FileField(upload_to='documents/vendor/work_data', null=True, blank=True, default='documents/No_Preview.pdf')



class nabl_report_data(models.Model):
    trf_id = models.IntegerField(blank=True, null=True)
    reportno = models.CharField(db_column='ReportNo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ulrno = models.CharField(db_column='ULRNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    manufacturer_wopo = models.CharField(db_column='Manufacturer_WOPO', max_length=500, blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=500, blank=True, null=True)  # Field name made lowercase.
    wo_po = models.CharField(db_column='WO_PO', max_length=500, blank=True, null=True)  # Field name made lowercase.
    srno = models.CharField(max_length=100)
    lot = models.CharField(max_length=50, blank=True, null=True)
    mainid = models.IntegerField(db_column='MainID', blank=True, null=True)  # Field name made lowercase.
    maindetid = models.IntegerField(db_column='MainDETID', blank=True, null=True)  # Field name made lowercase.
    bulkmain_tfcondition = models.CharField(db_column='BulkMain_TfCondition', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_phase = models.CharField(db_column='BulkMain_Phase', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_windingtype = models.CharField(db_column='BulkMain_WindingType', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_vector = models.CharField(db_column='BulkMain_Vector', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_win_descg1 = models.CharField(db_column='BulkMain_win_descg1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_win_descg2 = models.CharField(db_column='BulkMain_win_descg2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_cooling = models.CharField(db_column='BulkMain_Cooling', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_mva = models.FloatField(db_column='BulkMain_Prim_MVA', blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_mva = models.FloatField(db_column='BulkMain_Sec_MVA', blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_ratedvol = models.FloatField(db_column='BulkMain_Prim_RatedVol', blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_ratedvol = models.FloatField(db_column='BulkMain_Sec_RatedVol', blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_ratedcur = models.FloatField(db_column='BulkMain_Prim_RatedCur', blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_ratedcur = models.FloatField(db_column='BulkMain_Sec_RatedCur', blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_conn = models.CharField(db_column='BulkMain_Prim_Conn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_conn = models.CharField(db_column='BulkMain_Sec_Conn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not1 = models.CharField(db_column='BulkMain_Prim_not1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not2 = models.CharField(db_column='BulkMain_Prim_not2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not3 = models.CharField(db_column='BulkMain_Prim_not3', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not4 = models.CharField(db_column='BulkMain_Prim_not4', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not1 = models.CharField(db_column='BulkMain_Sec_not1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not2 = models.CharField(db_column='BulkMain_Sec_not2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not3 = models.CharField(db_column='BulkMain_Sec_not3', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not4 = models.CharField(db_column='BulkMain_Sec_not4', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_temp_oil = models.FloatField(db_column='BulkMain_Temp_Oil', blank=True, null=True)  # Field name made lowercase.
    bulkmain_temp_wind = models.FloatField(db_column='BulkMain_Temp_Wind', blank=True, null=True)  # Field name made lowercase.
    bulkmain_windingmaterial = models.CharField(db_column='BulkMain_WindingMaterial', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_metalval = models.IntegerField(db_column='BulkMain_MetalVal', blank=True, null=True)  # Field name made lowercase.
    bulkmain_refstd = models.CharField(db_column='BulkMain_refstd', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bulkmain_jobrating = models.CharField(db_column='BulkMain_jobrating', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bulkmain_reftemp = models.FloatField(db_column='BulkMain_RefTemp', blank=True, null=True)  # Field name made lowercase.
    bulkmain_freq = models.FloatField(db_column='BulkMain_freq', blank=True, null=True)  # Field name made lowercase.
    bulkmain_oilleakage = models.BooleanField(db_column='BulkMain_oilleakage', blank=True, null=True)  # Field name made lowercase.
    bulkmain_oilquantity = models.CharField(db_column='BulkMain_OilQuantity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_total_loss = models.BooleanField(db_column='BulkMain_total_loss', blank=True, null=True)  # Field name made lowercase.
    bulkmain_tap_changer = models.CharField(db_column='BulkMain_tap_changer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_tapon = models.CharField(db_column='BulkMain_tapon', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bulkmain_variation = models.CharField(db_column='BulkMain_variation', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bulkmain_volts1 = models.FloatField(db_column='BulkMain_volts1', blank=True, null=True)  # Field name made lowercase.
    bulkmain_volts2 = models.FloatField(db_column='BulkMain_volts2', blank=True, null=True)  # Field name made lowercase.
    bulkmain_persteps = models.FloatField(db_column='BulkMain_persteps', blank=True, null=True)  # Field name made lowercase.
    bulkmain_steps = models.FloatField(db_column='BulkMain_steps', blank=True, null=True)  # Field name made lowercase.
    torder_scheduleoftest = models.CharField(db_column='TOrder_ScheduleOfTest', max_length=250, blank=True, null=True)  # Field name made lowercase.
    torder_dateofreceipt = models.DateTimeField(db_column='TOrder_DateOfReceipt', blank=True, null=True)  # Field name made lowercase.
    torder_dateoftestingfrom = models.DateTimeField(db_column='TOrder_DateOfTestingFrom', blank=True, null=True)  # Field name made lowercase.
    torder_dateoftestingto = models.DateTimeField(db_column='TOrder_DateOfTestingTo', blank=True, null=True)  # Field name made lowercase.
    torder_dateofissue = models.DateTimeField(db_column='TOrder_DateOfIssue', blank=True, null=True)  # Field name made lowercase.
    torder_samplecode = models.CharField(db_column='TOrder_SampleCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_customernameaddress = models.CharField(db_column='TOrder_CustomerNameAddress', max_length=250, blank=True, null=True)  # Field name made lowercase.
    torder_note1 = models.CharField(db_column='TOrder_Note1', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    torder_note2 = models.CharField(db_column='TOrder_Note2', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    torder_note3 = models.CharField(db_column='TOrder_Note3', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    torder_note4 = models.CharField(db_column='TOrder_Note4', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    tfooter_1testedbylabel = models.CharField(db_column='TFooter_1TestedByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_1testedbyname = models.CharField(db_column='TOrder_1TestedByName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_1testedbydesign = models.CharField(db_column='TOrder_1TestedByDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_2checkedbylabel = models.CharField(db_column='TFooter_2CheckedByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_2checkedbyname = models.CharField(db_column='TOrder_2CheckedByName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_2checkedbydesign = models.CharField(db_column='TOrder_2CheckedByDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_3approvedbylabel = models.CharField(db_column='TFooter_3ApprovedByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_3approvedbyname = models.CharField(db_column='TOrder_3ApprovedByName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_3approvedbydesign = models.CharField(db_column='TOrder_3ApprovedByDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_4hodlabel = models.CharField(db_column='TFooter_4HODLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_4hodname = models.CharField(db_column='TOrder_4HODName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_4hoddesign = models.CharField(db_column='TOrder_4HODDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_witnessbylabel = models.CharField(db_column='TFooter_WitnessByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname1 = models.CharField(db_column='TOrder_WitnessByName1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign1 = models.CharField(db_column='TOrder_WitnessByDesign1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname2 = models.CharField(db_column='TOrder_WitnessByName2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign2 = models.CharField(db_column='TOrder_WitnessByDesign2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname3 = models.CharField(db_column='TOrder_WitnessByName3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign3 = models.CharField(db_column='TOrder_WitnessByDesign3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname4 = models.CharField(db_column='TOrder_WitnessByName4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign4 = models.CharField(db_column='TOrder_WitnessByDesign4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    normaltapno = models.IntegerField(db_column='NormalTapNo', blank=True, null=True)  # Field name made lowercase.
    totaltapqty = models.IntegerField(db_column='TotalTapQty', blank=True, null=True)  # Field name made lowercase.
    wr_lot = models.CharField(db_column='WR_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wr_testdate = models.DateTimeField(db_column='WR_testdate', blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_mwrwindphconn = models.CharField(db_column='WR_BulkMain_MWRwindphconn', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_mwrwindtol = models.FloatField(db_column='WR_BulkMain_MWRWindTol', blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_hvunit = models.CharField(db_column='WR_BulkMain_HVUnit', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputhvu = models.CharField(db_column='WR_MWRInputHVU', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputhvv = models.CharField(db_column='WR_MWRInputHVV', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputhvw = models.CharField(db_column='WR_MWRInputHVW', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvtemp = models.FloatField(db_column='WR_NormalTap_ResHVTemp', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvu = models.FloatField(db_column='WR_NormalTap_ResHVU', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvv = models.FloatField(db_column='WR_NormalTap_ResHVV', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvw = models.FloatField(db_column='WR_NormalTap_ResHVW', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvavg = models.FloatField(db_column='WR_NormalTap_ResHVavg', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshv75 = models.FloatField(db_column='WR_NormalTap_ResHV75', blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_lvunit = models.CharField(db_column='WR_BulkMain_LVUnit', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputlvu = models.CharField(db_column='WR_MWRInputLVU', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputlvv = models.CharField(db_column='WR_MWRInputLVV', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputlvw = models.CharField(db_column='WR_MWRInputLVW', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvtemp = models.FloatField(db_column='WR_NormalTap_ResLVTemp', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvu = models.FloatField(db_column='WR_NormalTap_ResLVU', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvv = models.FloatField(db_column='WR_NormalTap_ResLVV', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvw = models.FloatField(db_column='WR_NormalTap_ResLVW', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvavg = models.FloatField(db_column='WR_NormalTap_ResLVavg', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslv75 = models.FloatField(db_column='WR_NormalTap_ResLV75', blank=True, null=True)  # Field name made lowercase.
    wr_result = models.CharField(db_column='WR_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vr_lot = models.CharField(db_column='VR_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vr_testdate = models.DateTimeField(db_column='VR_Testdate', blank=True, null=True)  # Field name made lowercase.
    vr_mratioinputu = models.CharField(db_column='VR_MRatioInputU', max_length=200, blank=True, null=True)  # Field name made lowercase.
    vr_mratioinputv = models.CharField(db_column='VR_MRatioInputV', max_length=200, blank=True, null=True)  # Field name made lowercase.
    vr_mratioinputw = models.CharField(db_column='VR_MRatioInputW', max_length=200, blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_hvrated = models.FloatField(db_column='VR_NormalTap_HVRated', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_lvrated = models.FloatField(db_column='VR_NormalTap_LVRated', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_calratio = models.FloatField(db_column='VR_NormalTap_CalRatio', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_ratiou = models.FloatField(db_column='VR_NormalTap_RatioU', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_ratiov = models.FloatField(db_column='VR_NormalTap_RatioV', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_ratiow = models.FloatField(db_column='VR_NormalTap_RatioW', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_acccritdata = models.CharField(db_column='VR_NormalTap_AccCritData', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vr_vectordetected = models.CharField(db_column='VR_VectorDetected', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vr_result = models.CharField(db_column='VR_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ir_lot = models.CharField(db_column='IR_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ir_testdate = models.DateTimeField(db_column='IR_Testdate', blank=True, null=True)  # Field name made lowercase.
    ir_time = models.FloatField(db_column='IR_Time', blank=True, null=True)  # Field name made lowercase.
    ir_temp = models.FloatField(db_column='IR_Temp', blank=True, null=True)  # Field name made lowercase.
    ir_reshve = models.FloatField(db_column='IR_Reshve', blank=True, null=True)  # Field name made lowercase.
    ir_reslve = models.FloatField(db_column='IR_Reslve', blank=True, null=True)  # Field name made lowercase.
    ir_reshvlv = models.FloatField(db_column='IR_Reshvlv', blank=True, null=True)  # Field name made lowercase.
    ir_hve_volt = models.FloatField(db_column='IR_HVE_Volt', blank=True, null=True)  # Field name made lowercase.
    ir_lve_volt = models.FloatField(db_column='IR_LVE_Volt', blank=True, null=True)  # Field name made lowercase.
    ir_hvlv_volt = models.FloatField(db_column='IR_HVLV_Volt', blank=True, null=True)  # Field name made lowercase.
    ir_result = models.CharField(db_column='IR_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nll_lot = models.CharField(db_column='NLL_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nll_testdate = models.DateTimeField(db_column='NLL_Testdate', blank=True, null=True)  # Field name made lowercase.
    nll_bulkmain_nllguar = models.FloatField(db_column='NLL_BulkMain_Nllguar', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_ptr = models.CharField(db_column='NLL_NormalTap_ptr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_ctr = models.CharField(db_column='NLL_NormalTap_ctr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_frq = models.FloatField(db_column='NLL_NormalTap_frq', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_vrms = models.FloatField(db_column='NLL_NormalTap_Vrms', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_vmean = models.FloatField(db_column='NLL_NormalTap_Vmean', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_i1 = models.FloatField(db_column='NLL_NormalTap_I1', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_i2 = models.FloatField(db_column='NLL_NormalTap_I2', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_i3 = models.FloatField(db_column='NLL_NormalTap_I3', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_iavg = models.FloatField(db_column='NLL_NormalTap_Iavg', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_w1 = models.FloatField(db_column='NLL_NormalTap_W1', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_w2 = models.FloatField(db_column='NLL_NormalTap_W2', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_w3 = models.FloatField(db_column='NLL_NormalTap_W3', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_pmeasured = models.FloatField(db_column='NLL_NormalTap_Pmeasured', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_pcorrected = models.FloatField(db_column='NLL_NormalTap_Pcorrected', blank=True, null=True)  # Field name made lowercase.
    nll_result = models.CharField(db_column='NLL_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_lot = models.CharField(db_column='LL_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ll_testdate = models.DateTimeField(db_column='LL_Testdate', blank=True, null=True)  # Field name made lowercase.
    ll_bulkmain_llguar50 = models.FloatField(db_column='LL_BulkMain_llguar50', blank=True, null=True)  # Field name made lowercase.
    ll_bulkmain_llguar100 = models.FloatField(db_column='LL_BulkMain_llguar100', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_ptr = models.CharField(db_column='LL_NormalTap_ptr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_ctr = models.CharField(db_column='LL_NormalTap_ctr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_temp = models.FloatField(db_column='LL_NormalTap_50per_Temp', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_frq = models.FloatField(db_column='LL_NormalTap_50per_frq', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_vmeas = models.FloatField(db_column='LL_NormalTap_50per_Vmeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_i1 = models.FloatField(db_column='LL_NormalTap_50per_I1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_i2 = models.FloatField(db_column='LL_NormalTap_50per_I2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_i3 = models.FloatField(db_column='LL_NormalTap_50per_I3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_imeas = models.FloatField(db_column='LL_NormalTap_50per_Imeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_w1 = models.FloatField(db_column='LL_NormalTap_50per_W1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_w2 = models.FloatField(db_column='LL_NormalTap_50per_W2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_w3 = models.FloatField(db_column='LL_NormalTap_50per_W3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_pmeasured = models.FloatField(db_column='LL_NormalTap_50per_Pmeasured', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_llat75 = models.FloatField(db_column='LL_NormalTap_50per_LLat75', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_zat75 = models.FloatField(db_column='LL_NormalTap_50per_Zat75', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_temp = models.FloatField(db_column='LL_NormalTap_100per_Temp', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_frq = models.FloatField(db_column='LL_NormalTap_100per_frq', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_vmeas = models.FloatField(db_column='LL_NormalTap_100per_Vmeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_i1 = models.FloatField(db_column='LL_NormalTap_100per_I1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_i2 = models.FloatField(db_column='LL_NormalTap_100per_I2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_i3 = models.FloatField(db_column='LL_NormalTap_100per_I3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_imeas = models.FloatField(db_column='LL_NormalTap_100per_Imeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_w1 = models.FloatField(db_column='LL_NormalTap_100per_W1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_w2 = models.FloatField(db_column='LL_NormalTap_100per_W2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_w3 = models.FloatField(db_column='LL_NormalTap_100per_W3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_pmeasured = models.FloatField(db_column='LL_NormalTap_100per_Pmeasured', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_llat75 = models.FloatField(db_column='LL_NormalTap_100per_LLat75', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_zat75 = models.FloatField(db_column='LL_NormalTap_100per_Zat75', blank=True, null=True)  # Field name made lowercase.
    ll_percimpedancevoltreq = models.CharField(db_column='LL_PercImpedanceVoltReq', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_percimpedancevoltobtained = models.CharField(db_column='LL_PercImpedanceVoltObtained', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_percimpedancevoltremark = models.CharField(db_column='LL_PercImpedanceVoltRemark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss50perreq = models.CharField(db_column='LL_TotalLoss50PerReq', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss50perobtained = models.CharField(db_column='LL_TotalLoss50PerObtained', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss50perremark = models.CharField(db_column='LL_TotalLoss50PerRemark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss100perreq = models.CharField(db_column='LL_TotalLoss100PerReq', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss100perobtained = models.CharField(db_column='LL_TotalLoss100PerObtained', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss100perremark = models.CharField(db_column='LL_TotalLoss100PerRemark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_iovt_lot = models.CharField(db_column='HVT_IOVT_lot', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_iovt_testdate = models.DateTimeField(db_column='HVT_IOVT_Testdate', blank=True, null=True)  # Field name made lowercase.
    hvt_iovt_ptr = models.CharField(db_column='HVT_IOVT_ptr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_iovtctr = models.CharField(db_column='HVT_IOVTctr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_hvdetail = models.TextField(db_column='HVT_HVDetail', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hvt_lvdetail = models.TextField(db_column='HVT_LVDetail', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hvt_result = models.CharField(db_column='HVT_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iovt_hvdetail = models.TextField(db_column='IOVT_HVDetail', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    iovt_result = models.CharField(db_column='IOVT_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.





class nabl_report_data_rca(models.Model):
    trf_id = models.IntegerField(blank=True, null=True)
    reportno = models.CharField(db_column='ReportNo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ulrno = models.CharField(db_column='ULRNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    manufacturer_wopo = models.CharField(db_column='Manufacturer_WOPO', max_length=500, blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=500, blank=True, null=True)  # Field name made lowercase.
    wo_po = models.CharField(db_column='WO_PO', max_length=500, blank=True, null=True)  # Field name made lowercase.
    srno = models.CharField(max_length=100)
    lot = models.CharField(max_length=50, blank=True, null=True)
    mainid = models.IntegerField(db_column='MainID', blank=True, null=True)  # Field name made lowercase.
    maindetid = models.IntegerField(db_column='MainDETID', blank=True, null=True)  # Field name made lowercase.
    bulkmain_tfcondition = models.CharField(db_column='BulkMain_TfCondition', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_phase = models.CharField(db_column='BulkMain_Phase', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_windingtype = models.CharField(db_column='BulkMain_WindingType', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_vector = models.CharField(db_column='BulkMain_Vector', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_win_descg1 = models.CharField(db_column='BulkMain_win_descg1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_win_descg2 = models.CharField(db_column='BulkMain_win_descg2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_cooling = models.CharField(db_column='BulkMain_Cooling', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_mva = models.FloatField(db_column='BulkMain_Prim_MVA', blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_mva = models.FloatField(db_column='BulkMain_Sec_MVA', blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_ratedvol = models.FloatField(db_column='BulkMain_Prim_RatedVol', blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_ratedvol = models.FloatField(db_column='BulkMain_Sec_RatedVol', blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_ratedcur = models.FloatField(db_column='BulkMain_Prim_RatedCur', blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_ratedcur = models.FloatField(db_column='BulkMain_Sec_RatedCur', blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_conn = models.CharField(db_column='BulkMain_Prim_Conn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_conn = models.CharField(db_column='BulkMain_Sec_Conn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not1 = models.CharField(db_column='BulkMain_Prim_not1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not2 = models.CharField(db_column='BulkMain_Prim_not2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not3 = models.CharField(db_column='BulkMain_Prim_not3', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_prim_not4 = models.CharField(db_column='BulkMain_Prim_not4', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not1 = models.CharField(db_column='BulkMain_Sec_not1', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not2 = models.CharField(db_column='BulkMain_Sec_not2', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not3 = models.CharField(db_column='BulkMain_Sec_not3', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_sec_not4 = models.CharField(db_column='BulkMain_Sec_not4', max_length=200, blank=True, null=True)  # Field name made lowercase.
    bulkmain_temp_oil = models.FloatField(db_column='BulkMain_Temp_Oil', blank=True, null=True)  # Field name made lowercase.
    bulkmain_temp_wind = models.FloatField(db_column='BulkMain_Temp_Wind', blank=True, null=True)  # Field name made lowercase.
    bulkmain_windingmaterial = models.CharField(db_column='BulkMain_WindingMaterial', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_metalval = models.IntegerField(db_column='BulkMain_MetalVal', blank=True, null=True)  # Field name made lowercase.
    bulkmain_refstd = models.CharField(db_column='BulkMain_refstd', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bulkmain_jobrating = models.CharField(db_column='BulkMain_jobrating', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bulkmain_reftemp = models.FloatField(db_column='BulkMain_RefTemp', blank=True, null=True)  # Field name made lowercase.
    bulkmain_freq = models.FloatField(db_column='BulkMain_freq', blank=True, null=True)  # Field name made lowercase.
    bulkmain_oilleakage = models.BooleanField(db_column='BulkMain_oilleakage', blank=True, null=True)  # Field name made lowercase.
    bulkmain_oilquantity = models.CharField(db_column='BulkMain_OilQuantity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_total_loss = models.BooleanField(db_column='BulkMain_total_loss', blank=True, null=True)  # Field name made lowercase.
    bulkmain_tap_changer = models.CharField(db_column='BulkMain_tap_changer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    bulkmain_tapon = models.CharField(db_column='BulkMain_tapon', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bulkmain_variation = models.CharField(db_column='BulkMain_variation', max_length=10, blank=True, null=True)  # Field name made lowercase.
    bulkmain_volts1 = models.FloatField(db_column='BulkMain_volts1', blank=True, null=True)  # Field name made lowercase.
    bulkmain_volts2 = models.FloatField(db_column='BulkMain_volts2', blank=True, null=True)  # Field name made lowercase.
    bulkmain_persteps = models.FloatField(db_column='BulkMain_persteps', blank=True, null=True)  # Field name made lowercase.
    bulkmain_steps = models.FloatField(db_column='BulkMain_steps', blank=True, null=True)  # Field name made lowercase.
    torder_scheduleoftest = models.CharField(db_column='TOrder_ScheduleOfTest', max_length=250, blank=True, null=True)  # Field name made lowercase.
    torder_dateofreceipt = models.DateTimeField(db_column='TOrder_DateOfReceipt', blank=True, null=True)  # Field name made lowercase.
    torder_dateoftestingfrom = models.DateTimeField(db_column='TOrder_DateOfTestingFrom', blank=True, null=True)  # Field name made lowercase.
    torder_dateoftestingto = models.DateTimeField(db_column='TOrder_DateOfTestingTo', blank=True, null=True)  # Field name made lowercase.
    torder_dateofissue = models.DateTimeField(db_column='TOrder_DateOfIssue', blank=True, null=True)  # Field name made lowercase.
    torder_samplecode = models.CharField(db_column='TOrder_SampleCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_customernameaddress = models.CharField(db_column='TOrder_CustomerNameAddress', max_length=250, blank=True, null=True)  # Field name made lowercase.
    torder_note1 = models.CharField(db_column='TOrder_Note1', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    torder_note2 = models.CharField(db_column='TOrder_Note2', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    torder_note3 = models.CharField(db_column='TOrder_Note3', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    torder_note4 = models.CharField(db_column='TOrder_Note4', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    tfooter_1testedbylabel = models.CharField(db_column='TFooter_1TestedByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_1testedbyname = models.CharField(db_column='TOrder_1TestedByName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_1testedbydesign = models.CharField(db_column='TOrder_1TestedByDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_2checkedbylabel = models.CharField(db_column='TFooter_2CheckedByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_2checkedbyname = models.CharField(db_column='TOrder_2CheckedByName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_2checkedbydesign = models.CharField(db_column='TOrder_2CheckedByDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_3approvedbylabel = models.CharField(db_column='TFooter_3ApprovedByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_3approvedbyname = models.CharField(db_column='TOrder_3ApprovedByName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_3approvedbydesign = models.CharField(db_column='TOrder_3ApprovedByDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_4hodlabel = models.CharField(db_column='TFooter_4HODLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_4hodname = models.CharField(db_column='TOrder_4HODName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_4hoddesign = models.CharField(db_column='TOrder_4HODDesign', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tfooter_witnessbylabel = models.CharField(db_column='TFooter_WitnessByLabel', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname1 = models.CharField(db_column='TOrder_WitnessByName1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign1 = models.CharField(db_column='TOrder_WitnessByDesign1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname2 = models.CharField(db_column='TOrder_WitnessByName2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign2 = models.CharField(db_column='TOrder_WitnessByDesign2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname3 = models.CharField(db_column='TOrder_WitnessByName3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign3 = models.CharField(db_column='TOrder_WitnessByDesign3', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbyname4 = models.CharField(db_column='TOrder_WitnessByName4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    torder_witnessbydesign4 = models.CharField(db_column='TOrder_WitnessByDesign4', max_length=50, blank=True, null=True)  # Field name made lowercase.
    normaltapno = models.IntegerField(db_column='NormalTapNo', blank=True, null=True)  # Field name made lowercase.
    totaltapqty = models.IntegerField(db_column='TotalTapQty', blank=True, null=True)  # Field name made lowercase.
    wr_lot = models.CharField(db_column='WR_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    wr_testdate = models.DateTimeField(db_column='WR_testdate', blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_mwrwindphconn = models.CharField(db_column='WR_BulkMain_MWRwindphconn', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_mwrwindtol = models.FloatField(db_column='WR_BulkMain_MWRWindTol', blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_hvunit = models.CharField(db_column='WR_BulkMain_HVUnit', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputhvu = models.CharField(db_column='WR_MWRInputHVU', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputhvv = models.CharField(db_column='WR_MWRInputHVV', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputhvw = models.CharField(db_column='WR_MWRInputHVW', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvtemp = models.FloatField(db_column='WR_NormalTap_ResHVTemp', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvu = models.FloatField(db_column='WR_NormalTap_ResHVU', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvv = models.FloatField(db_column='WR_NormalTap_ResHVV', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvw = models.FloatField(db_column='WR_NormalTap_ResHVW', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshvavg = models.FloatField(db_column='WR_NormalTap_ResHVavg', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reshv75 = models.FloatField(db_column='WR_NormalTap_ResHV75', blank=True, null=True)  # Field name made lowercase.
    wr_bulkmain_lvunit = models.CharField(db_column='WR_BulkMain_LVUnit', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputlvu = models.CharField(db_column='WR_MWRInputLVU', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputlvv = models.CharField(db_column='WR_MWRInputLVV', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_mwrinputlvw = models.CharField(db_column='WR_MWRInputLVW', max_length=200, blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvtemp = models.FloatField(db_column='WR_NormalTap_ResLVTemp', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvu = models.FloatField(db_column='WR_NormalTap_ResLVU', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvv = models.FloatField(db_column='WR_NormalTap_ResLVV', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvw = models.FloatField(db_column='WR_NormalTap_ResLVW', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslvavg = models.FloatField(db_column='WR_NormalTap_ResLVavg', blank=True, null=True)  # Field name made lowercase.
    wr_normaltap_reslv75 = models.FloatField(db_column='WR_NormalTap_ResLV75', blank=True, null=True)  # Field name made lowercase.
    wr_result = models.CharField(db_column='WR_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vr_lot = models.CharField(db_column='VR_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vr_testdate = models.DateTimeField(db_column='VR_Testdate', blank=True, null=True)  # Field name made lowercase.
    vr_mratioinputu = models.CharField(db_column='VR_MRatioInputU', max_length=200, blank=True, null=True)  # Field name made lowercase.
    vr_mratioinputv = models.CharField(db_column='VR_MRatioInputV', max_length=200, blank=True, null=True)  # Field name made lowercase.
    vr_mratioinputw = models.CharField(db_column='VR_MRatioInputW', max_length=200, blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_hvrated = models.FloatField(db_column='VR_NormalTap_HVRated', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_lvrated = models.FloatField(db_column='VR_NormalTap_LVRated', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_calratio = models.FloatField(db_column='VR_NormalTap_CalRatio', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_ratiou = models.FloatField(db_column='VR_NormalTap_RatioU', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_ratiov = models.FloatField(db_column='VR_NormalTap_RatioV', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_ratiow = models.FloatField(db_column='VR_NormalTap_RatioW', blank=True, null=True)  # Field name made lowercase.
    vr_normaltap_acccritdata = models.CharField(db_column='VR_NormalTap_AccCritData', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vr_vectordetected = models.CharField(db_column='VR_VectorDetected', max_length=100, blank=True, null=True)  # Field name made lowercase.
    vr_result = models.CharField(db_column='VR_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ir_lot = models.CharField(db_column='IR_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ir_testdate = models.DateTimeField(db_column='IR_Testdate', blank=True, null=True)  # Field name made lowercase.
    ir_time = models.FloatField(db_column='IR_Time', blank=True, null=True)  # Field name made lowercase.
    ir_temp = models.FloatField(db_column='IR_Temp', blank=True, null=True)  # Field name made lowercase.
    ir_reshve = models.FloatField(db_column='IR_Reshve', blank=True, null=True)  # Field name made lowercase.
    ir_reslve = models.FloatField(db_column='IR_Reslve', blank=True, null=True)  # Field name made lowercase.
    ir_reshvlv = models.FloatField(db_column='IR_Reshvlv', blank=True, null=True)  # Field name made lowercase.
    ir_hve_volt = models.FloatField(db_column='IR_HVE_Volt', blank=True, null=True)  # Field name made lowercase.
    ir_lve_volt = models.FloatField(db_column='IR_LVE_Volt', blank=True, null=True)  # Field name made lowercase.
    ir_hvlv_volt = models.FloatField(db_column='IR_HVLV_Volt', blank=True, null=True)  # Field name made lowercase.
    ir_result = models.CharField(db_column='IR_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nll_lot = models.CharField(db_column='NLL_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nll_testdate = models.DateTimeField(db_column='NLL_Testdate', blank=True, null=True)  # Field name made lowercase.
    nll_bulkmain_nllguar = models.FloatField(db_column='NLL_BulkMain_Nllguar', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_ptr = models.CharField(db_column='NLL_NormalTap_ptr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_ctr = models.CharField(db_column='NLL_NormalTap_ctr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_frq = models.FloatField(db_column='NLL_NormalTap_frq', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_vrms = models.FloatField(db_column='NLL_NormalTap_Vrms', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_vmean = models.FloatField(db_column='NLL_NormalTap_Vmean', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_i1 = models.FloatField(db_column='NLL_NormalTap_I1', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_i2 = models.FloatField(db_column='NLL_NormalTap_I2', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_i3 = models.FloatField(db_column='NLL_NormalTap_I3', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_iavg = models.FloatField(db_column='NLL_NormalTap_Iavg', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_w1 = models.FloatField(db_column='NLL_NormalTap_W1', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_w2 = models.FloatField(db_column='NLL_NormalTap_W2', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_w3 = models.FloatField(db_column='NLL_NormalTap_W3', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_pmeasured = models.FloatField(db_column='NLL_NormalTap_Pmeasured', blank=True, null=True)  # Field name made lowercase.
    nll_normaltap_pcorrected = models.FloatField(db_column='NLL_NormalTap_Pcorrected', blank=True, null=True)  # Field name made lowercase.
    nll_result = models.CharField(db_column='NLL_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_lot = models.CharField(db_column='LL_lot', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ll_testdate = models.DateTimeField(db_column='LL_Testdate', blank=True, null=True)  # Field name made lowercase.
    ll_bulkmain_llguar50 = models.FloatField(db_column='LL_BulkMain_llguar50', blank=True, null=True)  # Field name made lowercase.
    ll_bulkmain_llguar100 = models.FloatField(db_column='LL_BulkMain_llguar100', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_ptr = models.CharField(db_column='LL_NormalTap_ptr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_ctr = models.CharField(db_column='LL_NormalTap_ctr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_temp = models.FloatField(db_column='LL_NormalTap_50per_Temp', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_frq = models.FloatField(db_column='LL_NormalTap_50per_frq', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_vmeas = models.FloatField(db_column='LL_NormalTap_50per_Vmeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_i1 = models.FloatField(db_column='LL_NormalTap_50per_I1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_i2 = models.FloatField(db_column='LL_NormalTap_50per_I2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_i3 = models.FloatField(db_column='LL_NormalTap_50per_I3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_imeas = models.FloatField(db_column='LL_NormalTap_50per_Imeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_w1 = models.FloatField(db_column='LL_NormalTap_50per_W1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_w2 = models.FloatField(db_column='LL_NormalTap_50per_W2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_w3 = models.FloatField(db_column='LL_NormalTap_50per_W3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_pmeasured = models.FloatField(db_column='LL_NormalTap_50per_Pmeasured', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_llat75 = models.FloatField(db_column='LL_NormalTap_50per_LLat75', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_50per_zat75 = models.FloatField(db_column='LL_NormalTap_50per_Zat75', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_temp = models.FloatField(db_column='LL_NormalTap_100per_Temp', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_frq = models.FloatField(db_column='LL_NormalTap_100per_frq', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_vmeas = models.FloatField(db_column='LL_NormalTap_100per_Vmeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_i1 = models.FloatField(db_column='LL_NormalTap_100per_I1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_i2 = models.FloatField(db_column='LL_NormalTap_100per_I2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_i3 = models.FloatField(db_column='LL_NormalTap_100per_I3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_imeas = models.FloatField(db_column='LL_NormalTap_100per_Imeas', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_w1 = models.FloatField(db_column='LL_NormalTap_100per_W1', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_w2 = models.FloatField(db_column='LL_NormalTap_100per_W2', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_w3 = models.FloatField(db_column='LL_NormalTap_100per_W3', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_pmeasured = models.FloatField(db_column='LL_NormalTap_100per_Pmeasured', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_llat75 = models.FloatField(db_column='LL_NormalTap_100per_LLat75', blank=True, null=True)  # Field name made lowercase.
    ll_normaltap_100per_zat75 = models.FloatField(db_column='LL_NormalTap_100per_Zat75', blank=True, null=True)  # Field name made lowercase.
    ll_percimpedancevoltreq = models.CharField(db_column='LL_PercImpedanceVoltReq', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_percimpedancevoltobtained = models.CharField(db_column='LL_PercImpedanceVoltObtained', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_percimpedancevoltremark = models.CharField(db_column='LL_PercImpedanceVoltRemark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss50perreq = models.CharField(db_column='LL_TotalLoss50PerReq', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss50perobtained = models.CharField(db_column='LL_TotalLoss50PerObtained', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss50perremark = models.CharField(db_column='LL_TotalLoss50PerRemark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss100perreq = models.CharField(db_column='LL_TotalLoss100PerReq', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss100perobtained = models.CharField(db_column='LL_TotalLoss100PerObtained', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ll_totalloss100perremark = models.CharField(db_column='LL_TotalLoss100PerRemark', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_iovt_lot = models.CharField(db_column='HVT_IOVT_lot', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_iovt_testdate = models.DateTimeField(db_column='HVT_IOVT_Testdate', blank=True, null=True)  # Field name made lowercase.
    hvt_iovt_ptr = models.CharField(db_column='HVT_IOVT_ptr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_iovtctr = models.CharField(db_column='HVT_IOVTctr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hvt_hvdetail = models.TextField(db_column='HVT_HVDetail', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hvt_lvdetail = models.TextField(db_column='HVT_LVDetail', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    hvt_result = models.CharField(db_column='HVT_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iovt_hvdetail = models.TextField(db_column='IOVT_HVDetail', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    iovt_result = models.CharField(db_column='IOVT_Result', max_length=50, blank=True, null=True)  # Field name made lowercase.   

class sample_test(models.Model):
    #id = models.IntegerField(blank=True, null=True)
    name_of_material = models.CharField(max_length=500, null=True, blank=True)
    lot_size_min = models.CharField(max_length=500, null=True, blank=True)
    lot_size_max = models.CharField(max_length=500, null=True, blank=True)
    sample_size_in_nos = models.CharField(max_length=500, null=True, blank=True)
    unit = models.CharField(max_length=500, null=True, blank=True)
    sample_size_in_percent = models.CharField(max_length=500, null=True, blank=True)
    unit_1 = models.CharField(max_length=500, null=True, blank=True)
    acceptable_limit = models.CharField(max_length=500, null=True, blank=True)
    permissible_limit = models.CharField(max_length=500, null=True, blank=True)
    unit_3 = models.CharField(max_length=500, null=True, blank=True)
    rejection_criteria_of_lot_or_di_qty = models.CharField(max_length=500, null=True, blank=True)
    unit_4 = models.CharField(max_length=500, null=True, blank=True)
    resample_acceptable_limit = models.CharField(max_length=500, null=True, blank=True)
    resample_rejection_criteria_lot_or_di_qty = models.CharField(max_length=500, null=True, blank=True)
    unit_5 = models.CharField(max_length=500, null=True, blank=True)



