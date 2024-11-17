from django.db import models


# # Create your models here.
# class FQP_Material(models.Model):
#     FQP_Material = models.AutoField(primary_key=True)
#     Material_Name = models.CharField(max_length=200, null=True, blank=True)
#     def __str__(self):
#        return self.Material_Name


# class FQP_Test(models.Model):
#     FQP_Test_Id = models.AutoField(primary_key=True)
#     FQP_Material = models.ForeignKey(FQP_Material, on_delete=models.PROTECT)
#     FQP_Test = models.CharField(max_length=200, null=True, blank=True)
#     # Image = models.ImageField(upload_to='api/image', null=True, blank=True)
#     # Status = models.BooleanField()
#     # Observation = models.CharField(max_length=200, null=True, blank=True)
#     # Latitude = models.CharField(max_length=30, null=True, blank=True)
#     # Longitude = models.CharField(max_length=30, null=True, blank=True)


# class FQP_Data(models.Model):
#     id = models.AutoField(primary_key=True)
#     FQP_Test_Id = models.ForeignKey(FQP_Test, on_delete=models.PROTECT,default='0')
#     # FQP_Material_Id = models.ForeignKey(FQP_Material, on_delete=models.PROTECT)
#     Image = models.ImageField(upload_to='api/image', null=True, blank=True)
#     Status = models.BooleanField()
#     Observation = models.CharField(max_length=200, null=True, blank=True)
#     Latitude = models.CharField(max_length=30, null=True, blank=True)
#     Longitude = models.CharField(max_length=30, null=True, blank=True)
#     # def __str__(self):
#     #        return self.Observation


class AppraisalReport(models.Model):
    v_experience = models.IntegerField(blank=True, null=True)
    v_availability = models.IntegerField(blank=True, null=True, default=0)
    v_calibration = models.IntegerField(blank=True, null=True, default=0)
    v_bought_out_items = models.IntegerField(blank=True, null=True, default=0)
    v_inprocess_inspection = models.IntegerField(blank=True, null=True, default=0)
    v_dispatch = models.IntegerField(blank=True, null=True, default=0)
    v_overall_record = models.IntegerField(blank=True, null=True, default=0)
    v_area_instruction = models.IntegerField(blank=True, null=True, default=0)
    v_isobis_certification = models.IntegerField(blank=True, null=True, default=0)
    v_material_handling = models.IntegerField(blank=True, null=True, default=0)
    v_general_observation = models.IntegerField(blank=True, null=True, default=0)
    v_packing_product = models.IntegerField(blank=True, null=True, default=0)

    p_experience_of_production = models.IntegerField(blank=True, null=True, default=0)
    p_experience_of_supervisor = models.IntegerField(blank=True, null=True, default=0)
    p_effectiveness = models.IntegerField(blank=True, null=True, default=0)
    p_quality = models.IntegerField(blank=True, null=True, default=0)
    p_cleanliness = models.IntegerField(blank=True, null=True, default=0)
    p_safety_equipment = models.IntegerField(blank=True, null=True, default=0)
    p_condition_of_stores = models.IntegerField(blank=True, null=True, default=0)
    p_back_uppower_facility = models.IntegerField(blank=True, null=True, default=0)
    p_adequate_progress = models.IntegerField(blank=True, null=True, default=0)
    p_overall_view = models.IntegerField(blank=True, null=True, default=0)


class Login(models.Model):
    username = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=15, null=True, blank=True)


class VendorDetail(models.Model):
    user_id = models.CharField(max_length=15, null=True, blank=True)
    E_Sanctioned = models.IntegerField(blank=True, null=True)
    E_Working_Load = models.IntegerField(blank=True, null=True)
    E_Data = models.CharField(max_length=10, blank=True, null=True)
    E_Details_of_electric_power = models.IntegerField(blank=True, null=True)

    P_Quantity = models.IntegerField(blank=True, null=True)
    P_Testing = models.BooleanField()

    T_Details = models.CharField(max_length=10, blank=True, null=True)
    T_Desription = models.CharField(max_length=10, blank=True, null=True)
    T_Equipments = models.BooleanField()
    T_Manufacturing = models.BooleanField()
    T_Inspection = models.BooleanField()
    T_Substandard = models.BooleanField()
    T_Assistance = models.BooleanField()
    T_Accreditation = models.BooleanField()
    T_Testing_carried = models.BooleanField()
    T_Certification = models.BooleanField()



class MaterialVerification(models.Model):
    Material_Name = models.CharField(max_length=30, null=True, blank=True)
    Material_Specification = models.CharField(max_length=50, null=True, blank=True)
    Material_Test_Doc = models.BooleanField()
    Remark_Test = models.CharField(max_length=100, blank=True, null=True)
    Material_GTP_Doc = models.BooleanField()
    Remark_GTP = models.CharField(max_length=100, blank=True, null=True)
    Material_Other_Doc = models.BooleanField()
    Remark_Other = models.CharField(max_length=100, blank=True, null=True)
    sufficient_capacity = models.BooleanField()  # api
    sufficient_capacity_remark = models.CharField(max_length=100, blank=True, null=True)  # api
    Verify = models.BooleanField()  # api



class Erp_Data(models.Model):
    vendor_name = models.CharField(max_length=300, null=True, blank=True)
    vendor_type = models.CharField(max_length=300, null=True, blank=True)
    vendor_number = models.CharField(max_length=300, null=True, blank=True)
    pan_no = models.CharField(max_length=300, null=True, blank=True)
    vendor_site_code = models.CharField(max_length=300, null=True, blank=True)
    email_address = models.CharField(max_length=300, null=True, blank=True)
    address_1 = models.CharField(max_length=300, null=True, blank=True)
    address_2 = models.CharField(max_length=300, null=True, blank=True)
    address_3 = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    pin = models.CharField(max_length=20, null=True, blank=True)
    bank = models.CharField(max_length=500, null=True, blank=True)
    branch = models.CharField(max_length=500, null=True, blank=True)
    ifsc = models.CharField(max_length=50, null=True, blank=True)
    branch_address = models.CharField(max_length=500, null=True, blank=True)
    account_no = models.CharField(max_length=50, null=True, blank=True)
    gst_no = models.CharField(max_length=50, null=True, blank=True)
    status = models.IntegerField(default='0', null=True, blank=True)
    Is_Admin = models.IntegerField(null=True, blank=True, default=0)
    Is_Active = models.IntegerField(null=True, blank=True, default=0)
    Created_At = models.DateTimeField(auto_now_add=True, null=True)
    Updated_At = models.DateTimeField(auto_now_add=True, null=True)


class NablDTRReport(models.Model):
    trf_id = models.CharField(blank=True, null=True,max_length=100)
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
    
    discom = models.CharField(max_length=300, blank=True, null=True) #CZ<WZ<EZ
    nabl_id = models.CharField(max_length=300, blank=True, null=True)
    nabl_name = models.CharField( max_length=300, blank=True, null=True)
    xmr_id = models.CharField(max_length=300, blank=True, null=True)
    result_pass_fail = models.CharField(max_length=10, blank=True, null=True)
    remark = models.CharField(max_length=300, blank=True, null=True)
    report_file = models.FileField(upload_to='NABLReport/', blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    rating = models.CharField(max_length=300, blank=True, null=True)

    location = models.CharField(max_length=1000, blank=True, null=True)



class NablDTRReport(models.Model):
    # trf_id = models.IntegerField(blank=True, null=True)
    trf_id = models.CharField(max_length=100, blank=True, null=True)
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
    
    
    discom = models.CharField(max_length=300, blank=True, null=True) #CZ<WZ<EZ
    nabl_id = models.CharField(max_length=300, blank=True, null=True)
    nabl_name = models.CharField( max_length=300, blank=True, null=True)
    xmr_id = models.CharField(max_length=300, blank=True, null=True)
	
    result_pass_fail = models.CharField(max_length=10, blank=True, null=True)
    remark = models.CharField(max_length=300, blank=True, null=True)
    report_file = models.FileField(upload_to='NABLReport/', blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True, default=0)
    rating = models.CharField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=1000, blank=True, null=True)