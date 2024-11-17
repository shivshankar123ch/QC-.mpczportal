from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from vendor.models import *
from main.models import *
from django.conf import settings
from django.core.mail import send_mail
from vendor.models import *
from django.core.mail import EmailMessage
from rca.models import *
import psycopg2
import psycopg2
from django.shortcuts import render
from django.http import HttpResponse
from .resources import PersonResource
from tablib import Dataset
from rca.models import RO_Material_XMR_Info
from django.db.models import Q
from api.models import NablDTRReport
from nabl.models import *

from itertools import chain
from datetime import datetime as dtm
from nabl.models import *
from django.db.models import Sum

# ************ 28/01/2022 Jeevan *************
def procurement_dashboard(request):
    return render(request, 'po/procurement_dashboard.html')


def cgm_total_po(request):
    data = ProcurementInfo.objects.all()
    return render(request, 'po/cgm/cgm_total_po.html', {"data": data})


def cgm_pending_po(request):
    data = ProcurementInfo.objects.filter(po_viewer=1, po_approver=0)

    return render(request, 'po/cgm/cgm_pending_po.html', {"data": data})


def cgm_rejected_po(request):
    data = ProcurementInfo.objects.filter(po_viewer=1, po_approver=-1)
    return render(request, 'po/cgm/cgm_rejected_po.html', {"data": data})


def cgm_approved_po(request):
    data = ProcurementInfo.objects.filter(po_viewer=1, po_approver=1)
    return render(request, 'po/cgm/cgm_approved_po.html', {"data": data})


def cgm_procurement_approved(request, id):
    data = ProcurementInfo.objects.get(id=id)
    data.po_approver = 1
    data.save()
    data = ProcurementInfo.objects.filter(po_viewer=1, po_approver=0)

    return render(request, 'po/cgm/cgm_pending_po.html', {"data": data})


def cgm_procurement_rejected(request, id):
    data = ProcurementInfo.objects.get(id=id)
    data.po_approver = -1
    data.save()
    data = ProcurementInfo.objects.filter(po_viewer=1, po_approver=0)
    return render(request, 'po/cgm/cgm_pending_po.html', {"data": data})


# Create your views here.
def po_base(request):
    return HttpResponse("PO BASE")


def area_base(request):
    return render(request, 'po/area_store/areastore_base.html', {})


def nabl_base(request):
    return render(request, 'po/nabl/nabl_base.html', {})


def vendor_view_di(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    vd = VendorDispatchInfo.objects.filter(po_id=po_id)
    store = LocalStoreInventory.objects.filter(po_id=po_id)
    return render(request, 'vendor/vendor_view_di.html', {"data": data[0], 'offer': vd, 'store': store})


def area_dashboard(request):
    return render(request, 'po/area_store/areastore_dashboard.html')


def nabl_dashboard(request):
    return render(request, 'po/nabl/dasbordbase.html')


def area_process(request):
    data = ProcurementInfo.objects.filter(dispatch_status=1)
    return render(request, 'po/area_store/area_process_inventory.html', {"data": data})


def offer_receive(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(local_store_status=1)
    data = ProcurementInfo.objects.filter(local_store_status=1)
    return render(request, 'po/area_store/area_stock_inventory.html', {"data": data})


def area_stock(request):
    data = ProcurementInfo.objects.filter(dispatch_status=1)
    return render(request, 'po/area_store/area_stock_inventory.html', {"data": data})


def dispatch_for_nabl(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(dispatch_for_nabl=1)
    data = ProcurementInfo.objects.filter(local_store_status=1)
    return render(request, 'po/area_store/area_stock_inventory.html', {"data": data})


def nabl_Registration_Sixteen(request, po_id):
    if request.method == 'POST':
        data = ProcurementInfo.objects.filter(po_id=po_id)
        data.update(po_test=1)
        return render(request, 'po/nabl/nabl_reg16.html', {"data": data})


def nabl_Registration_Sixteen1(request):
    data = ProcurementInfo.objects.filter(dispatch_status=1)
    return render(request, 'po/nabl/nabl_reg16.html', {"data": data})


import math


def nabl_Upload(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    dispatch_info = VendorDispatchInfo.objects.filter(po_id=po_id)
    quantity = math.ceil(data[0].item_quantity * .2)
    item = VendorDispatchItemInfo.objects.filter(dispatch_d=dispatch_info[0].id).order_by('?')[:quantity]
    data.update(po_store=1)
    if data[0].item_class == 'A':
        return render(request, 'po/nabl/nabl_reg15.html',
                      {"data": data[0], "dispatch_info": dispatch_info, "item": item})
    elif data[0].item_class == 'B':
        return render(request, 'po/nabl/nabl_reg13.html',
                      {"data": data[0], "dispatch_info": dispatch_info, "item": item})
    else:
        return render(request, 'po/nabl/nabl_reg14.html',
                      {"data": data[0], "dispatch_info": dispatch_info, "item": item})
    return render(request, 'po/nabl/nabl_reg16.html', {"data": data[0], "dispatch_info": dispatch_info, "item": item})


def nabl_Report(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(po_test=1)
    data = ProcurementInfo.objects.filter(vendor_offer=1)
    return render(request, 'po/nabl/nabl_reg16.html', {"data": data})


# ************ OLD code Jeevan *************

def procurement_Previous_PO(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    data = Purchase_Order.objects.filter(zone=officer.user_zone).order_by("-id")
    return render(request, 'po/procurement_di_list.html', {"data": data, "officer":officer})



def vendor_bg_view(request, po_id):
    data = ProcurementInfo.objects.get(id=po_id)
    sd = PO_SD.objects.get(po_no=data)
    return render(request, 'po/procurement_bg_view.html', {"data": data, 'sd': sd})


def vendor_offer_view(request, po_id,po_material_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    data = Purchase_Order.objects.filter(id=po_id)
    vd = PO_Material_Offer.objects.get(po_id=po_id, id = po_material_id)
    material_data = PO_Material.objects.get(id = vd.material.id)
    dispatch_info = PO_Material_Offer_Serial_No.objects.filter(offer=vd.id)
    return render(request, 'po/vendor_offer_new.html', {"data": data[0],
                                                        "dispatch_info": dispatch_info, 'offer': vd, 'material_data': material_data})


def area_store_view(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    vd = VendorDispatchInfo.objects.get(po_id=po_id)
    dispatch_info = VendorDispatchItemInfo.objects.filter(dispatch_d=vd.id)
    return render(request, 'po/area_store/view_di.html', {"data": data[0],
                                                          "dispatch_info": dispatch_info, 'offer': vd})


def procurement_Di_List(request):
    data = ProcurementInfo.objects.filter(offer_approved=1)
    return render(request, 'po/procurement_di_list1.html', {"data": data})


def tkc_purchase(request):
    data = TkcLogin.objects.all()
    return render(request, 'po/procurement_tkc_po.html', {"data": data})


def tkc_all_purchase(request):
    return render(request, 'po/procurement_tkc_po1.html')


def tkc_tier1_inspection(request):
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'po/tkc_tier1_Inspectin.html', {"officer": officer})


def tkc_tier2_inspection(request):
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'po/tkc_tier2_inpection.html', {"officer": officer})


# def po_gen1(request):
#     accept = request.POST.getlist("clause_name")
#     value = PO_Type_Clause.objects.filter(PO_type_Id=1)
#     lst_clause_name = []
#     for i in value:
#         clause_name = i.PO_Clause_Id
#         lst_clause_name.append(clause_name)
#         clause_id = i.PO_type_Id

#     return render(request, 'po/po_gen1.html', {'value': lst_clause_name})


# def po_gen2(request):
#     accept = request.POST.getlist("clause_name")
#     lst_clause_detail = []
#     for key in accept:
#         value = PO_Clause_Master.objects.filter(PO_Clause_Name=key)
#         for i in value:
#             lst_clause_detail.append(i.PO_Clause_Description)

#     data = zip(accept, lst_clause_detail)

#     return render(request, 'po/po_gen2.html', {'data_po': data})




def procurement_Dashboard(request):
    return render(request, 'po/procurement_dashboard.html')


def procurement_Di_Issue(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    vd = VendorDispatchInfo.objects.filter(po_id=po_id)
    # dispatch_info = VendorDispatchItemInfo.objects.filter(dispatch_d=vd.id)
    return render(request, 'po/procurement_generate_di.html',
                  {"data": data[0], 'offer': vd})


def procurement_Di_Issued(request, po_id):
    if request.method == 'POST':
        data = ProcurementInfo.objects.filter(id=po_id)
        vd = VendorDispatchInfo.objects.filter(po_id=po_id)
        name1 = request.POST.get('name1')
        if name1 is not None:
            inventry = LocalStoreInventory(store_name='Bhopal', po_id=po_id, Di_Id=vd[0].id, quantity=name1)
            inventry.save()
        name2 = request.POST.get('name2')
        if name2 is not None:
            inventry = LocalStoreInventory(store_name='Guna', po_id=po_id, Di_Id=vd[0].id, quantity=name2)
            inventry.save()
        name3 = request.POST.get('name3')
        if name3 is not None:
            inventry = LocalStoreInventory(store_name='Gwalior', po_id=po_id, Di_Id=vd[0].id, quantity=name3)
            inventry.save()
        data.update(di_status=1)
        data = ProcurementInfo.objects.filter(di_status=1)
        return render(request, 'po/procurement_previous_po.html', {"data": data})
    data = ProcurementInfo.objects.filter(di_status=1)
    return render(request, 'po/procurement_previous_po.html', {"data": data})


def procurement_Generate_DI(request):
    if request.method == "POST":
        vendor_id = request.POST.get('vendor')
        item_class = request.POST.get('class')
        item_category = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        name = request.POST.get('name')
        procurement = ProcurementInfo(vendor_email=vendor_id, item_class=item_class,
                                      item_category=item_category, item_name=name, item_quantity=quantity,
                                      item_price=price)
        procurement.save()
        vd = ProcurementInfo.objects.latest('id')
        vendor = VendorRegistration.objects.all()
        return render(request, 'po/procurement_generate_po1.html', {'vendor': vendor[0]})
    vendor = VendorRegistration.objects.all()
    return render(request, 'po/procurement_generate_po.html', {'vendor': vendor})


def vendor_purchase(request):
    data = ProcurementInfo.objects.filter(di_status=1)
    return render(request, 'vendor/vendor_purchase_order.html', {"data": data})


def procurement_Dispatch(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(dispatch_status=1)
    return render(request, 'vendor/vendor_purchase_order.html', {"data": data})


def vendor_purchase_B(request):
    if request.method == 'POST':
        data = ProcurementInfo.objects.filter(bg_status=1)
        return render(request, 'vendor/vendor_purchase_order_list.html', {"data": data})

    data = ProcurementInfo.objects.all()
    return render(request, 'vendor/vendor_purchase_order_list.html', {"data": data})

#--------------------------------Documents approval in PO-----------------------------------------------
def vendor_gtp_approval(request):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone, is_po_deleted = False, po_approved_status = 1).order_by("-id")
    return render(request, 'po/procurement_gtp_approval.html', {"data": data})


def vendor_gtp_approved(request, po_id):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(id=po_id,zone = officer_data.user_zone)
    data.update(gtp_approved=1)
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone, is_po_deleted = False, po_approved_status = 1).order_by("-id")
    return render(request, 'po/procurement_gtp_approval.html', {"data": data})


def vendor_bank_details_approval(request): 
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone, is_po_deleted = False, po_approved_status = 1).order_by("-id")
    return render(request, 'po/bankdetails.html', {"data": data})

def vender_bank_detail_view(request,id):
    sd = BankDetails.objects.filter(po_no=id).last()

    return render(request,'po/procurement_bank_details_view.html',{'sd':sd})

def vendor_bank_details_approved(request, po_id):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(id=po_id)
    data1 = Purchase_Order.objects.filter(id=po_id)
    data.update(bank_details_approved=1)
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone, is_po_deleted = False, po_approved_status = 1).order_by("-id")
    return render(request, 'po/bankdetails.html', {"data": data})


def vendor_bg_approval(request):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone, is_po_deleted = False, po_approved_status = 1).order_by("-id")
    return render(request,'po/po_creater/bankguarantee.html', {"data": data})


def vender_sd_detail(request,id):
    sd = PO_SD.objects.filter(po_no=id).last()

    return render(request,'po/procurement_bg_view.html',{'sd':sd})

def vendor_bg_approved(request, po_id):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(id=po_id)
    data.update(bg_approved=1)
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone, is_po_deleted = False, po_approved_status = 1).order_by("-id")
    return render(request, 'po/po_creater/bankguarantee.html', {"data": data})
#-----------------------------------------------------------end-------------------------------------------------------------

#---------------------------------------------------Material offer in PO---------------------------------------------------------------------
def vendor_ins_approval(request):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = PO_Material_Offer.objects.filter(po__zone =officer_data.user_zone).order_by("-id")
    return render(request, 'po/procurement_ins_approval.html', {"data": data})


def vendor_ins_approved(request, po_id, po_material_id):
    po_master_data = Purchase_Order.objects.get(id = po_id)
    po_master_data.po_item_approved = True
    po_master_data.save()
    po_data = PO_Material_Offer.objects.get(po = po_id, id = po_material_id)
    po_data.Offer=1
    po_data.save()
    data = PO_Material_Offer.objects.filter(po = po_id, Offer = 0,is_di_created = False)
    return render(request, 'po/procurement_ins_approval.html', {"data": data,"msg":"Purchase order approved successfully"})


def vendor_ins_reject(request, po_id, po_material_id):
    po_master_data = Purchase_Order.objects.get(id = po_id)
    po_master_data.po_item_approved = False
    po_master_data.save()
    po_data = PO_Material_Offer.objects.get(po = po_id, id = po_material_id)
    po_data.Offer=-1
    po_data.status=0
    po_data.save()
    update_material=PO_Material.objects.get(po_id=po_data.po.id, item_code=po_data.item_code, specification= po_data.item_name )
    update_material.remaining_qty=(float(update_material.remaining_qty) + float(po_data.Offer_Quantity))
    update_material.dispatch_qty= (float(update_material.dispatch_qty) - float(po_data.Offer_Quantity))
    if update_material.remaining_qty != 0:
        update_material.Offer=0
        update_material.save()
    po_exist_data = PO_Material_Offer.objects.filter(po = update_material.po, material =update_material , item_code = update_material.item_code, status=1)
    if len(po_exist_data) >= 1:
        i = po_exist_data.last()
        i.remaining_qty= update_material.remaining_qty
        i.dispatch_qty= update_material.dispatch_qty
        i.save()
    data = PO_Material_Offer.objects.filter(po = po_id, Offer = 0,is_di_created = False)
    return render(request, 'po/procurement_ins_approval.html', {"data": data})
#--------------------------------------------------end-------------------------------------------------------------------

def vendor_dispatch_GTP(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    return render(request, 'vendor/vendor_gtp.html', {"data": data[0]})


def vendor_dispatch_SD(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(gtp_status=1, bg_status=1)
    return render(request, 'vendor/vendor_sd.html', {"data": data[0]})


def vendor_dispatch_Open(request):
    data = ProcurementInfo.objects.filter(bg_status=1)
    return render(request, 'vendor/vendor_generate_di1.html', {"data": data})


def vendor_dispatch_B(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(bg_status=1)
    return render(request, 'vendor/vendor_generate_di.html', {"data": data[0]})


def vendor_dispatch_B2(request, po_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        data = ProcurementInfo.objects.filter(id=po_id)
        return render(request, 'vendor/vendor_generate_di2.html',
                      {"data": data[0], "quantity": range(quantity), "quantity1": quantity})
    data = ProcurementInfo.objects.filter(id=po_id)
    return render(request, 'vendor/vendor_generate_di.html', {"data": data[0]})


def vendor_dispatch_B3(request, po_id, quantity):
    print('ttttttttttttttttttt')
    if request.method == "POST":
        officer = InspectingOfficerInfo.objects.all().order_by('?')[:1]
        print('ttttttttttttttttttt',officer)
        lab = NablRegistration.objects.all().order_by('?')[:1]
        vdi = VendorDispatchInfo(po_id=po_id, item_quantity=quantity,
                                 inspecting_officer_id=officer[0].officer_employ_id,
                                 lab_name=lab[0].n_company_name)
        vdi.save()
        vd = VendorDispatchInfo.objects.latest('id')
        for data in range(quantity):
            serial_no = request.POST.get(str(data))
            vdi = VendorDispatchItemInfo(dispatch_d=vd.id, serial_number=serial_no)
            vdi.save()
        data = ProcurementInfo.objects.filter(id=po_id)
        data.update(vendor_offer=1)
        dispatch_info = VendorDispatchItemInfo.objects.filter(dispatch_d=vd.id)
        return render(request, 'vendor/vendor_generate_di3.html',
                      {"data": data[0], "quantity": range(quantity), "quantity1": quantity,
                       "dispatch_info": dispatch_info, 'offer': vd})
    data = ProcurementInfo.objects.filter(id=po_id)
    return render(request, 'vendor/vendor_generate_di.html', {"data": data[0]})


def tkc_purchase(request):
    data = TkcLogin.objects.all()
    return render(request, 'po/procurement_tkc_po.html', {"data": data})


def tkc_purchase1(request):
    if request.method == "POST":
        tkc_id = request.POST.get('vendor')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        tendor = request.POST.get('tendor')
        nit = request.POST.get('nit')
        procurement = TKCProcurementInfo(tkc_id=tkc_id, item_quantity=quantity,
                                         item_price=price, nit_no=nit, tendor_no=tendor)
        procurement.save()
        vd = TKCProcurementInfo.objects.latest('id')
        tkc = TkcLogin.objects.filter(v_id=tkc_id)
        procurement = TKCProcurementInfo.objects.filter(id=vd.id)
        cdatetime = datetime.datetime.now().date()
        return render(request, 'po/procurement_tkc_po1.html',
                      {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                       'quantity': range(int(quantity))})


def tkc_purchase2(request, PO_id):
    if request.method == "POST":
        price_variable = request.POST.get('price_variable')
        price_date = request.POST.get('price_date')
        gst_percent = request.POST.get('gst_percent')
        payment_submitted_to = request.POST.get('payment_submitted_to')
        payment_upto = request.POST.get('payment_upto')
        payment_above = request.POST.get('payment_above')
        delivery_fromDATE = request.POST.get('delivery_fromDATE')
        delivery_withinDATE = request.POST.get('delivery_withinDATE')
        delivery_Sno1 = request.POST.get('delivery_Sno1')
        delivery_itemDetails1 = request.POST.get('delivery_itemDetails1')
        delivery_quantity1 = request.POST.get('delivery_quantity1')
        delivery_date1 = request.POST.get('delivery_date1')
        securityDeposite_amount = request.POST.get('securityDeposite_amount')
        securityDeposite_percent = request.POST.get('securityDeposite_percent')
        securityDeposite_SDpercent = request.POST.get('securityDeposite_SDpercent')
        securityDeposite_SD = request.POST.get('securityDeposite_SD')
        penalty_sumEqualPercent = request.POST.get('penalty_sumEqualPercent')
        penalty_restrictedPercent = request.POST.get('penalty_restrictedPercent')
        scheme_Sno = request.POST.get('scheme_Sno')
        scheme_Item = request.POST.get('scheme_Item')
        scheme_RRTD = request.POST.get('scheme_RRTD')
        scheme_Total = request.POST.get('scheme_Total')
        performance_months = request.POST.get('performance_months')
        performance_days = request.POST.get('performance_days')
        performance_freight = request.POST.get('performance_freight')
        performance_days2 = request.POST.get('performance_days2')
        drawing_submitted = request.POST.get('drawing_submitted')
        drawing_conveyed = request.POST.get('drawing_conveyed')
        fake_amountGST = request.POST.get('fake_amountGST')
        acceptanceMaterial_days = request.POST.get('acceptanceMaterial_days')
        acceptanceMaterial_percent = request.POST.get('acceptanceMaterial_percent')
        acceptanceMaterial_percentPerWeek = request.POST.get('acceptanceMaterial_percentPerWeek')
        acceptanceMaterial_percentMax = request.POST.get('acceptanceMaterial_percentMax')
        extension_quantity = request.POST.get('extension_quantity')
        extension_months = request.POST.get('extension_months')
        settlement_court = request.POST.get('settlement_court')
        settlement_email = request.POST.get('settlement_email')
        schedule_Sno = request.POST.get('schedule_Sno')
        schedule_item = request.POST.get('schedule_item')
        schedule_itemCode = request.POST.get('schedule_itemCode')
        schedule_Qty = request.POST.get('schedule_Qty')
        schedule_price = request.POST.get('schedule_price')
        schedule_freight = request.POST.get('schedule_freight')
        schedule_freightGST = request.POST.get('schedule_freightGST')
        schedule_total1 = request.POST.get('schedule_total1')
        schedule_total2 = request.POST.get('schedule_total2')
        schedule_total3 = request.POST.get('schedule_total3')
        procurement = TKCProcurementInfo.objects.filter(id=PO_id)
        procurement.update(price_variable=price_variable, price_date=price_date, gst_percent=gst_percent,
                           payment_submitted_to=payment_submitted_to,
                           payment_upto=payment_upto, payment_above=payment_above,
                           delivery_fromDATE=delivery_fromDATE, delivery_withinDATE=delivery_withinDATE,
                           delivery_Sno1=delivery_Sno1, delivery_itemDetails1=delivery_itemDetails1,
                           delivery_quantity1=delivery_quantity1, delivery_date1=delivery_date1,
                           securityDeposite_amount=securityDeposite_amount,
                           securityDeposite_percent=securityDeposite_percent,
                           securityDeposite_SDpercent=securityDeposite_SDpercent,
                           securityDeposite_SD=securityDeposite_SD,
                           penalty_sumEqualPercent=penalty_sumEqualPercent,
                           penalty_restrictedPercent=penalty_restrictedPercent,
                           scheme_Sno=scheme_Sno, scheme_Item=scheme_Item, scheme_RRTD=scheme_RRTD,
                           scheme_Total=scheme_Total, performance_months=performance_months,
                           performance_days=performance_days, performance_freight=performance_freight,
                           performance_days2=performance_days2, drawing_submitted=drawing_submitted,
                           drawing_conveyed=drawing_conveyed, fake_amountGST=fake_amountGST,
                           acceptanceMaterial_days=acceptanceMaterial_days,
                           acceptanceMaterial_percent=acceptanceMaterial_percent,
                           acceptanceMaterial_percentPerWeek=acceptanceMaterial_percentPerWeek,
                           acceptanceMaterial_percentMax=acceptanceMaterial_percentMax,
                           extension_quantity=extension_quantity,
                           extension_months=extension_months, settlement_court=settlement_court,
                           settlement_email=settlement_email, schedule_Sno=schedule_Sno,
                           schedule_item=schedule_item,
                           schedule_itemCode=schedule_itemCode, schedule_Qty=schedule_Qty,
                           schedule_price=schedule_price, schedule_freight=schedule_freight,
                           schedule_freightGST=schedule_freightGST,
                           schedule_total1=schedule_total1, schedule_total2=schedule_total2,
                           schedule_total3=schedule_total3)
        counter = 100
        for data in range(int(procurement[0].item_quantity)):
            task = request.POST.get(str(data))
            percentage = request.POST.get(str(counter))
            tkc = TKCScheduleInfo(TKCProcurementInfo_id=procurement[0].id, phase=data + 1, percentage=percentage,
                                  task=task)
            tkc.save()
            counter = counter + 1
        tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
        cdatetime = datetime.datetime.now().date()
        data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id)
        return render(request, 'po/procurement_tkc_po_view.html',
                      {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                       'data': data})


def tkc_all_purchase(request):
    tkc = TKCProcurementInfo.objects.all()
    return render(request, 'po/procurement_tkc_po1.html', {'tkc': tkc})


def tkc_tier1_inspection(request):
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'TKC/tkc_tier1_Inspectin.html', {"officer": officer})


def tkc_tier2_inspection(request):
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'po/tkc_tier2_inpection.html', {"officer": officer})


def procurement_status(request, po_id):
    data = Purchase_Order.objects.filter(id=po_id)
    return render(request, 'po/procurement_po_status.html', {"data": data[0]})


def procurement_delete(request, po_id):
    data = Purchase_Order.objects.filter(id=po_id)
    data.delete()
    return render(request, 'po/procurement_di_list.html', {"data": data})


import datetime;


def vendor_procurement_status(request, po_id):
    data = Purchase_Order.objects.filter(id=po_id)
    cdatetime = dtm.now().date()
    return render(request, 'vendor/vendor_po_status.html', {"data": data[0], "date": cdatetime})

def tkc_reg13(request):
    return render(request, 'tkc/tkc_reg13.html')


def tkc_reg14(request):
    return render(request, 'tkc/tkc_reg14.html')


def tkc_reg15(request):
    return render(request, 'tkc/tkc_reg15.html')


def tkc_reg17(request):
    return render(request, 'tkc/tkc_reg17.html')


def User_section_dashboard(request):
    return render(request, 'po/User_section_dashboard.html')


def cgm_signup(request):
    return render(request, 'vendor/cgm_signup.html')


def cgm_login(request):
    return render(request, 'vendor/cgm_login.html')


def cgm_home(request):
    data = ProcurementInfo.objects.all().order_by('-id')[:1]
    return render(request, 'vendor/cgm_dashboard.html', {"data": data})


# def procurement_Generate_PO2(request, po_id):
    # if request.method == "POST":
        # price_variable = request.POST.get('price_variable')
        # price_date = request.POST.get('price_date')
        # gst_percent = request.POST.get('gst_percent')
        # payment_submitted_to = request.POST.get('payment_submitted_to')
        # payment_upto = request.POST.get('payment_upto')
        # payment_above = request.POST.get('payment_above')
        # delivery_fromDATE = request.POST.get('delivery_fromDATE')
        # delivery_withinDATE = request.POST.get('delivery_withinDATE')
        # delivery_Sno1 = request.POST.get('delivery_Sno1')
        # delivery_itemDetails1 = request.POST.get('delivery_itemDetails1')
        # delivery_quantity1 = request.POST.get('delivery_quantity1')
        # delivery_date1 = request.POST.get('delivery_date1')
        # securityDeposite_amount = request.POST.get('securityDeposite_amount')
        # securityDeposite_percent = request.POST.get('securityDeposite_percent')
        # securityDeposite_SDpercent = request.POST.get('securityDeposite_SDpercent')
        # securityDeposite_SD = request.POST.get('securityDeposite_SD')
        # penalty_sumEqualPercent = request.POST.get('penalty_sumEqualPercent')
        # penalty_restrictedPercent = request.POST.get('penalty_restrictedPercent')
        # scheme_Sno = request.POST.get('scheme_Sno')
        # scheme_Item = request.POST.get('scheme_Item')
        # scheme_RRTD = request.POST.get('scheme_RRTD')
        # scheme_Total = request.POST.get('scheme_Total')
        # performance_months = request.POST.get('performance_months')
        # performance_days = request.POST.get('performance_days')
        # performance_freight = request.POST.get('performance_freight')
        # performance_days2 = request.POST.get('performance_days2')
        # drawing_submitted = request.POST.get('drawing_submitted')
        # drawing_conveyed = request.POST.get('drawing_conveyed')
        # fake_amountGST = request.POST.get('fake_amountGST')
        # acceptanceMaterial_days = request.POST.get('acceptanceMaterial_days')
        # acceptanceMaterial_percent = request.POST.get('acceptanceMaterial_percent')
        # acceptanceMaterial_percentPerWeek = request.POST.get('acceptanceMaterial_percentPerWeek')
        # acceptanceMaterial_percentMax = request.POST.get('acceptanceMaterial_percentMax')
        # extension_quantity = request.POST.get('extension_quantity')
        # extension_months = request.POST.get('extension_months')
        # settlement_court = request.POST.get('settlement_court')
        # settlement_email = request.POST.get('settlement_email')
        # schedule_Sno = request.POST.get('schedule_Sno')
        # schedule_item = request.POST.get('schedule_item')
        # schedule_itemCode = request.POST.get('schedule_itemCode')
        # schedule_Qty = request.POST.get('schedule_Qty')
        # schedule_price = request.POST.get('schedule_price')
        # schedule_freight = request.POST.get('schedule_freight')
        # schedule_freightGST = request.POST.get('schedule_freightGST')
        # schedule_total1 = request.POST.get('schedule_total1')
        # schedule_total2 = request.POST.get('schedule_total2')
        # schedule_total3 = request.POST.get('schedule_total3')
        # procurement = ProcurementInfo.objects.filter(id=po_id)
        # procurement.update(price_variable=price_variable, price_date=price_date, gst_percent=gst_percent,
                           # payment_submitted_to=payment_submitted_to,
                           # payment_upto=payment_upto, payment_above=payment_above, delivery_fromDATE=delivery_fromDATE,
                           # delivery_withinDATE=delivery_withinDATE,
                           # delivery_Sno1=delivery_Sno1, delivery_itemDetails1=delivery_itemDetails1,
                           # delivery_quantity1=delivery_quantity1, delivery_date1=delivery_date1,
                           # securityDeposite_amount=securityDeposite_amount,
                           # securityDeposite_percent=securityDeposite_percent,
                           # securityDeposite_SDpercent=securityDeposite_SDpercent,
                           # securityDeposite_SD=securityDeposite_SD, penalty_sumEqualPercent=penalty_sumEqualPercent,
                           # penalty_restrictedPercent=penalty_restrictedPercent,
                           # scheme_Sno=scheme_Sno, scheme_Item=scheme_Item, scheme_RRTD=scheme_RRTD,
                           # scheme_Total=scheme_Total, performance_months=performance_months,
                           # performance_days=performance_days, performance_freight=performance_freight,
                           # performance_days2=performance_days2, drawing_submitted=drawing_submitted,
                           # drawing_conveyed=drawing_conveyed, fake_amountGST=fake_amountGST,
                           # acceptanceMaterial_days=acceptanceMaterial_days,
                           # acceptanceMaterial_percent=acceptanceMaterial_percent,
                           # acceptanceMaterial_percentPerWeek=acceptanceMaterial_percentPerWeek,
                           # acceptanceMaterial_percentMax=acceptanceMaterial_percentMax,
                           # extension_quantity=extension_quantity,
                           # extension_months=extension_months, settlement_court=settlement_court,
                           # settlement_email=settlement_email, schedule_Sno=schedule_Sno, schedule_item=schedule_item,
                           # schedule_itemCode=schedule_itemCode, schedule_Qty=schedule_Qty,
                           # schedule_price=schedule_price, schedule_freight=schedule_freight,
                           # schedule_freightGST=schedule_freightGST,
                           # schedule_total1=schedule_total1, schedule_total2=schedule_total2,
                           # schedule_total3=schedule_total3)

    # procurement = ProcurementInfo.objects.filter(id=po_id)
    # vendor = VendorRegistration.objects.filter(v_email=procurement[0].vendor_email)
    # date = datetime.datetime.now()
    # return render(request, 'po/procurement_preview.html',
                  # {'vendor': vendor[0], "procurement": procurement[0], "date": date})


def tkc_reg16(request):
    tkc = TKCProcurementInfo.objects.all()
    return render(request, 'tkc/tkc_reg16.html', {"data": tkc})


def tkc_view(request, id):
    procurement = TKCProcurementInfo.objects.filter(id=id)
    tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id)
    return render(request, 'tkc/tkc_view.html', {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                                                 'data': data})


def tkc_po_view(request, id):
    procurement = TKCProcurementInfo.objects.filter(id=id)
    tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id)
    return render(request, 'po/procurement_tkc_po_view.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                   'data': data})


def offer_inspection(request, id):
    procurement = TKCProcurementInfo.objects.filter(id=id)
    tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    officer = InspectingOfficerInfo.objects.all()
    data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, offer_status=0)
    return render(request, 'tkc/tkc_offer_inspection.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                   "officer": officer, 'data': data[0]})


def view_schedule(request, id):
    procurement = TKCProcurementInfo.objects.filter(id=id)
    tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id)
    return render(request, 'tkc/tkc_view_schedule.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                   'data': data})


def tkc_view_schedule(request, id):
    procurement = TKCProcurementInfo.objects.filter(id=id)
    tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id)
    return render(request, 'po/tkc_view_schedule.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                   'data': data})


def tkc_dash(request):
    return render(request, 'tkc/dashboardbase.html')


def tkc_all_purchase(request):
    tkc = TKCProcurementInfo.objects.all()
    return render(request, 'po/procurement_tkc_all_po.html', {"data": tkc})


def tkc_tier1_inspection(request):
    tkc = TKCProcurementInfo.objects.all()
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'po/tkc_tier1_Inspectin.html', {"officer": officer, "data": tkc})


def tkc_tier2_inspection(request):
    tkc = TKCProcurementInfo.objects.all()
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'po/tkc_tier2_inpection.html', {"officer": officer, "data": tkc})


def tkc_inspecting_offer(request, id, phase):
    if request.method == "POST":
        date = request.POST.get('date')
        procurement = TKCProcurementInfo.objects.filter(id=id)
        data1 = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, phase=phase)
        data1.update(tkc_offer_date=date, offer_status=1)
        tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
        cdatetime = datetime.datetime.now().date()
        data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, offer_status=0)
        return render(request, 'tkc/tkc_offer_inspection.html',
                      {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                       'data': data[0]})


def inspecting_schedule_set(request, id):
    procurement = TKCProcurementInfo.objects.filter(id=id)
    tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    officer = InspectingOfficerInfo.objects.all()
    data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, offer_status=1)
    return render(request, 'po/tkc_tier1_Inspection1.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime, "officer": officer,
                   'data': data[0]})


def tkc_inspecting_offer_approved(request, id, phase):
    if request.method == "POST":
        date = request.POST.get('date')
        officer = request.POST.get('officer')
        procurement = TKCProcurementInfo.objects.filter(id=id)
        data1 = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, phase=phase)
        data1.update(inspecting_officer_id=officer, inspecting_date=date, inspecting_status=1)
        tkc = TKCProcurementInfo.objects.all()
        return render(request, 'po/procurement_tkc_all_po.html',
                      {"data": tkc})


def tkc_officer_preview(request):
    tkc = TKCProcurementInfo.objects.all()
    return render(request, 'po/procurement_tkc_officer_all_po.html', {"data": tkc})


def tkc_officer_view_detail(request, id):
    procurement = TKCProcurementInfo.objects.filter(id=id)
    tkc = TkcLogin.objects.filter(v_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    officer = InspectingOfficerInfo.objects.all()
    data = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, inspecting_status=1)
    return render(request, 'po/tkc_officer_view_detail.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime, "officer": officer,
                   'data': data[0]})


def tkc_inspecting_officer_result(request, id, phase):
    if request.method == "POST":
        result = request.POST.get('result')
        if result == 'pass':
            procurement = TKCProcurementInfo.objects.filter(id=id)
            data1 = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, phase=phase)
            data1.update(Result=1)
        else:
            procurement = TKCProcurementInfo.objects.filter(id=id)
            data1 = TKCScheduleInfo.objects.filter(TKCProcurementInfo_id=procurement[0].id, phase=phase)
            data1.update(offer_status=0, inspecting_status=0)
        tkc = TKCProcurementInfo.objects.all()
        return render(request, 'po/procurement_tkc_all_po.html',
                      {"data": tkc})

    if request.method == "POST":
        result = request.POST.get('result')

        tkc = TKCProcurementInfo.objects.all()
        return render(request, 'po/procurement_tkc_all_po.html',
                      {"data": tkc})


def po_gen(request):
    text = """ 
     Considering your offer against the tender under subject and subsequent correspondence, we have pleasure in placing this detailed order for supply of 11KV CT:PT Unit ratio
     300-150/5A & 33KV CT:PT unit ratio 10/5A on <b>own quoted rates as detailed in Schedule-I; Price & Quantity of this order. This order is subject to the terms and conditions 
     as stipulated in detail in Annexure-I enclosed with this order except the terms and condition as modified / laid down hereunder. 
     These shall be binding on you in respect of this contract and no conditions or stipulations to be contrary or which are inconsistent will be applicable / acceptable. 
     This order is also subject to the technical specifications as contained in Annexure-II """
    return render(request, 'po/po_gen.html', {'text': text})


def po_gen1(request):
    value = PO_Type_Clause.objects.filter(PO_type_Id=1)
    lst_clause_name = []
    for i in value:
        clause_name = i.PO_Clause_Id
        lst_clause_name.append(clause_name)
        clause_id = i.PO_type_Id

    value2 = PO_Type_Clause.objects.filter(PO_type_Id=2)
    lst_clause_name2 = []
    for i in value2:
        clause_name2 = i.PO_Clause_Id
        lst_clause_name2.append(clause_name2)
        clause_id2 = i.PO_type_Id

    value3 = PO_Type_Clause.objects.filter(PO_type_Id=3)
    lst_clause_name3 = []
    for i in value3:
        clause_name3 = i.PO_Clause_Id
        lst_clause_name3.append(clause_name3)
        clause_id3 = i.PO_type_Id

    return render(request, 'po/po_gen1.html',
                  {'value': lst_clause_name, 'value2': lst_clause_name2, 'value3': lst_clause_name3})


from fpdf import FPDF
import os
from datetime import datetime


def po_gen2(request):
    lst_clause_detail = []
    if request.method == "POST":
        Radio = request.POST.get('colorRadio')
        clause_list = request.POST.getlist("clause_name")

        clause_detail_list = []
        for clause_name in clause_list:
            value = PO_Clause_Master.objects.filter(PO_Clause_Name=clause_name)
            for i in value:
                clause_detail_list.append(i.PO_Clause_Description)

        data_value = zip(clause_list, clause_detail_list)
        data_value2 = zip(clause_list, clause_detail_list)
        data_zip_cl_cld = zip(clause_list, clause_detail_list)

        c = 0
        if Radio == "GOODS":
            for cl, cdl in data_zip_cl_cld:
                obj_po = PO_Temp_Table(PO_type_Name="GOODS", PO_Clause_Name=cl, PO_Clause_Description=cdl, PO_type_Id=1,
                                       PO_Clause_Id=1)
                c = c + 1
                obj_po.save()
        elif Radio == "WORKS":
            for cl, cdl in data_zip_cl_cld:
                obj_po1 = PO_Temp_Table(PO_type_Name="GOODS", PO_Clause_Name=cl, PO_Clause_Description=cdl,
                                        PO_type_Id=2, PO_Clause_Id=2)
                c = c + 1
                obj_po1.save()
        elif Radio == "SERVICES":
            for cl, cdl in data_zip_cl_cld:
                obj_po2 = PO_Temp_Table(PO_type_Name="GOODS", PO_Clause_Name=cl, PO_Clause_Description=cdl,
                                        PO_type_Id=2, PO_Clause_Id=2)
                c = c + 1
                obj_po2.save()
        else:
            pass

        procurement = ProcurementInfo.objects.get(id=request.session['dddddd'])
        tendor_number = procurement.tendor_no
        iddd = procurement.User_code

        vendor = User_Registration.objects.get(User_Id=iddd)
        company_name = vendor.CompanyName_E
        user_id = vendor.User_Id
        vendor_email = vendor.Email_Id
        vendor_phone = vendor.ContactNo

        address = UserCompanyDataMain.objects.get(user_id_id=vendor)
        company_add_1 = address.Company_add_1
        company_add_2 = address.Company_add_2
        company_dist = address.Company_dist
        company_state = address.Company_state
        company_pincode = address.Company_pin_code

        item = procurement.item_name

        cdatetime = str(datetime.now().date())

        pdf = FPDF()
        pdf.add_page()
        path = os.getcwd() + "/static/assets/images/header.png"
        pdf.image(path, -10, 0, 225, 50)

        sub_text = str(
            "Order for supply of ") + item + " against Tender Specification No. MD/MK/" + tendor_number + " (Opened on " + cdatetime + ")."
        sub_text2 = sub_text.encode('latin-1', 'replace').decode('latin-1')

        ref_text = """Your offer submitted against TS. No. MD/MK/04/710 (Opened on 27.08.2021)."""

        accept = "ACCEPTANCE : "

        accept_text = """Considering your above offer against the tender under subject, we have pleasure in placing this detailed order for supply of 11 KV Dry Type CT ratio 300-150/5-5A on your own quoted rate indicated as detailed in Schedule-I; Price & Quantity of this order.

        This order is subject to the terms and conditions as stipulated in detail in Annexure-I enclosed with this order except the terms and conditions as modified / laid down hereunder. These shall be binding on you in respect of this contract and no conditions or stipulations to the contrary or which are inconsistent will be applicable/ acceptable.

        This order is also subject to the Technical Specifications as contained in Annexure-II."""

        accept_text2 = accept_text.encode('latin-1', 'replace').decode('latin-1')

        pdf.ln(38)

        pdf.set_font('Times', '', 12.0)
        pdf.cell(100, 10, f'No. MD/MK/{tendor_number}', 0, 0)
        pdf.cell(20)
        pdf.cell(80, 10, f'Bhopal, dated:- {cdatetime}', 0, 1)

        pdf.ln(5)
        pdf.cell(80, 5, f'To,', 0, 0)
        pdf.ln(5)

        pdf.cell(10)
        pdf.cell(50, 5, f'', 0, 1)
        pdf.set_font('Times', 'B', 12.0)
        pdf.cell(50, 2, f'{company_name}', 0, 0)
        pdf.cell(10)
        pdf.set_font('Times', '', 12.0)
        pdf.cell(50, 2, f'', 0, 1)
        pdf.cell(10)
        pdf.cell(50, 2, f'', 0, 1)
        pdf.cell(100, 2, f'{company_add_1}', 0, 0)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 12.0)
        pdf.cell(50, 2, f'Email:- agarwal.industries@ymail.com', 0, 1)
        pdf.cell(10)
        pdf.cell(50, 2, f'', 0, 1)
        pdf.set_font('Times', '', 12.0)
        pdf.cell(100, 2, f'{company_add_2},{company_dist}, {company_state}, {company_pincode}', 0, 0)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 12.0)
        pdf.cell(50, 2, f'{vendor_email}', 0, 1)

        pdf.ln(5)
        pdf.cell(30)
        pdf.cell(50, 5, f'', 0, 1)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(5, 5, f'Sub : ', 0, 0)

        pdf.cell(10)
        pdf.set_font('Times', 'B', 12.0)
        pdf.multi_cell(h=5.0, align='J', w=0, txt=sub_text2, border=0)

        pdf.ln(2)

        pdf.cell(30)
        pdf.cell(50, 5, f'', 0, 1)
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(5, 10, f'Ref : ', 0, 0)

        pdf.cell(10)
        pdf.set_font('Times', '', 12.0)
        pdf.cell(50, 10, f'{ref_text}', 0, 1)

        pdf.cell(30)
        pdf.cell(50, 5, f'', 0, 1)
        pdf.set_font('Times', '', 14.0)
        pdf.cell(5, 10, f'Dear Sirs, ', 0, 0)

        pdf.ln(5)

        for cl, cld in data_value:
            pdf.cell(10)
            pdf.cell(50, 5, f'', 0, 1)
            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(5, 5, f'{cl} ', 0, 1)
            pdf.set_font('Times', '', 12.0)
            cld2 = cld.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(h=5.0, align='J', w=0, txt=cld2, border=0)

        now_mirco = datetime.now()
        now_mirco1 = str(now_mirco)
        final_path = "/media/" + company_name + "_" + cdatetime + "_" + now_mirco1
        # v_obj = Vendor_Document(Po_file=final_path)
        # v_obj.save()

        pdf.output(final_path, 'F')

        final_path2 = os.getcwd() + "/po/" + company_name + "_" + cdatetime + "_" + now_mirco1

        v_obj = ProcurementInfo.objects.get(id=request.session['dddddd'])
        v_obj.Po_doc = final_path2
        v_obj.po_viewer = 1
        v_obj.user_name = company_name
        v_obj.save()

        message = EmailMessage(
            "Subject",
            "Some body."
            "rohitpatel1790@gmail.com",
            ['rohitpatel.mpcz@gmail.com'],
        )
        message.attach("document.pdf", final_path2)
        message.send(fail_silently=False)
        td = datetime.now()
        return render(request, 'po/po_gen2.html',
                      {'td':td,'data_po': data_value2, 'vendor': vendor, "date": cdatetime, 'procurement': procurement,
                       'address': address})

    return render(request, 'po/po_gen2.html')

    
def test_request_form(request, gatepass_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    areastore = AreaStore_Officer.objects.get(Officer=officer)
    store_name = areastore.AreaStore.Name
    store_name = store_name.strip()
    zone_name = areastore.AreaStore.Discom.Discom_Name_E
    zone_name = zone_name.strip()
    amn_obj = Add_material_nabl.objects.get(id = gatepass_id)
    lab_name = str(amn_obj.User)
    lab_name = lab_name.strip()
    return render(request, 'po/area_store/test_request_form.html', {'amn_obj':amn_obj, 'store_name':store_name,
                                                                    'zone_name':zone_name, 'lab_name':lab_name})

def test_request_form_submit(request, gatepass_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    areastore = AreaStore_Officer.objects.get(Officer=officer)
    store_name = areastore.AreaStore.Name
    store_name = store_name.strip()
    zone_name = areastore.AreaStore.Discom.Discom_Name_E
    zone_name = zone_name.strip()
    amn_obj = Add_material_nabl.objects.get(id = gatepass_id)
    lab_name = str(amn_obj.User)
    lab_name = lab_name.strip()
    if request.method == "POST":
        customer_Organization_name = request.POST.get('customer_Organization_name')
        customer_Organization_address = request.POST.get('customer_Organization_address')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_designation = request.POST.get('contact_person_designation')
        mobile_no = request.POST.get('mobile_no')
        email_id = request.POST.get('email_id')
        name_of_sample_product = request.POST.get('name_of_sample_product')
        customer_ref_gatepass_no = request.POST.get('customer_ref_gatepass_no')
        dated = request.POST.get('dated')
        sample_description_condition = request.POST.get('sample_description_condition')
        test_spec = request.POST.get('test_spec')
        drawings_catalogs_operating_manual = request.POST.get('drawings_catalogs_operating_manual')

        test_name = request.POST.getlist('Test_name[]')

        decision_yes_no = request.POST.get('decision_yes_no')
        if decision_yes_no == "Yes":
            decision_option = request.POST.get('decision_option')
        elif decision_yes_no == "No":
            decision_option = ""
           
        sign = request.POST.get('sign')
        onbehalf = request.POST.get('onbehalf')
        sign2 = request.POST.get('sign2')
        Organization = request.POST.get('Organization')
        email_address = request.POST.get('email_address')

        Test_name1 = request.POST.get('Test_name1')
        Test_name2 = request.POST.get('Test_name2')
        Test_name3 = request.POST.get('Test_name3')
        Test_name4 = request.POST.get('Test_name4')
        Test_name5 = request.POST.get('Test_name5')
        Test_name6 = request.POST.get('Test_name6')
        Test_name7 = request.POST.get('Test_name7')
        Test_name8 = request.POST.get('Test_name8')
        Test_name9 = request.POST.get('Test_name9')
        Test_name10 = request.POST.get('Test_name10')

        amn_obj = Add_material_nabl.objects.get(id = gatepass_id)
        if TRF_Details.objects.filter(Gatepass=amn_obj).exists():
            pass
        else:
            trf_obj = TRF_Details(ro_id = amn_obj.roid,gatepass_id=gatepass_id, 
                                customer_Organization_name=customer_Organization_name, 
                                customer_Organization_address=customer_Organization_address,
                                contact_person_name=contact_person_name,
                                contact_person_designation=contact_person_designation, 
                                mobile_no=mobile_no, email_id=email_id, 
                                name_of_sample_product=name_of_sample_product, 
                                customer_ref_gatepass_no=customer_ref_gatepass_no, 
                                dated=dated, sample_description_condition=sample_description_condition, 
                                test_spec=test_spec, drawings_catalogs_operating_manual=drawings_catalogs_operating_manual,
                                decision_yes_no=decision_yes_no, decision_option=decision_option, 
                                sign=sign, onbehalf=onbehalf, sign2=sign2, Organization=Organization, 
                                email_address=email_address, trf_generated = 1, Gatepass = amn_obj,
                                Test_name1=Test_name1, Test_name2=Test_name2, Test_name3=Test_name3,
                                Test_name4=Test_name4, Test_name5=Test_name5, Test_name6=Test_name6,
                                Test_name7=Test_name7, Test_name8=Test_name8, Test_name9=Test_name9,
                                Test_name10=Test_name10)
            trf_obj.save()
        
        # trf_id = TRF_Details.objects.latest('TRF_Id')
        trf_obj = TRF_Details.objects.get(gatepass_id=gatepass_id)
        data2=RO_Info.objects.filter(id = amn_obj.roid)
        data2.update(dispatch_for_nabl=1)

        for data in test_name:
            test_details = TRF_Test_Details(gatepass_id=gatepass_id, TRF_Test_Id=trf_obj.TRF_Id, 
                                            TRF_Test_Name=data, TRF_Details = trf_obj)
            test_details.save()

        data = ProcurementInfo.objects.filter(User_code=gatepass_id)
        data.update(dispatch_for_nabl=1)
        data.update(test_request_form=1)
        data.update(TRF_Id=trf_obj.TRF_Id)

        data1=RO_Info.objects.filter(id=amn_obj.roid,dispatch_for_nabl=1)
        for i in data1:
            material1=RO_Material_Info.objects.filter(ro=i.id)
            for j in material1:
                if j.flag_25_sampled == 1:
                    j.mat_sampled_flag = 0
                    j.finally_sampled=1
                    j.save()

                elif j.flag_63_sampled == 1:
                    j.mat_sampled_flag = 0
                    j.finally_sampled=1
                    j.save()
 
                elif j.flag_100_sampled == 1:
                    j.mat_sampled_flag = 0
                    j.finally_sampled=1
                    j.save()

                elif j.flag_200_sampled == 1:
                    j.mat_sampled_flag = 0
                    j.finally_sampled=1
                    j.save()   

        amn_obj = Add_material_nabl.objects.get(id = gatepass_id)
        amn_obj.trf_generated=1
        amn_obj.TRF_Id=trf_obj.TRF_Id
        amn_obj.save()

        ri_obj = RO_Info.objects.get(id = amn_obj.roid)
        ri_obj.store_to_nabl_complete = 1
        ri_obj.save()

        data = TRF_Details.objects.get(Gatepass=amn_obj)
        data2 = TRF_Test_Details.objects.filter(TRF_Details=data)
        var_show = 1
        return render(request, 'po/area_store/test_request_view.html', {'data': data, 'data2': data2,
                                                                    'id':id, 'var_show':var_show,
                                                                    'amn_obj':amn_obj, 'store_name':store_name,
                                                                    'zone_name':zone_name, 'lab_name':lab_name})
    amn_obj = Add_material_nabl.objects.all()
    return render(request, 'po/area_store/test_request_view.html', {'amn_obj':amn_obj, 'store_name':store_name,
                                                                    'zone_name':zone_name, 'lab_name':lab_name})


def test_request_view(request, gatepass_id):
    var_show = 0
    if request.method == "POST":
        if request.FILES['digitalCert']:
            filename = request.FILES['digitalCert']  
            amn_obj = Add_material_nabl.objects.get(id = gatepass_id)
            trf_obj = TRF_Details.objects.get(Gatepass = amn_obj)
            trf_obj.TRFAreastore_file = filename
            trf_obj.save()
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    areastore = AreaStore_Officer.objects.get(Officer=officer)
    store_name = areastore.AreaStore.Name
    store_name = store_name.strip()
    zone_name = areastore.AreaStore.Discom.Discom_Name_E
    zone_name = zone_name.strip()
    amn_obj = Add_material_nabl.objects.get(id = gatepass_id)
    lab_name = str(amn_obj.User)
    lab_name = lab_name.strip()
    amn_obj = Add_material_nabl.objects.get(id = gatepass_id)
    data = TRF_Details.objects.get(Gatepass=amn_obj)
    data2 = TRF_Test_Details.objects.filter(TRF_Details=data)
    return render(request, 'po/area_store/test_request_view.html', {'data': data, 'data2': data2,
                                                                    'id':id, 'var_show':var_show,
                                                                    'amn_obj':amn_obj,'store_name':store_name,
                                                                    'zone_name':zone_name, 'lab_name':lab_name})


def all_rca_wo(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id

    cell =RCA_Cell.objects.get(Region = officer.Region)
    data = WO_Info.objects.filter(rca_cell=cell).order_by('-id')


    return render(request, 'po/area_store/all_rca_wo.html', {'data': data})


from datetime import date
from fpdf import FPDF
import os


def rca_order_view(request, id):
    vd = WO_Info.objects.get(id=id)
    schedule = WO_Schedule_Info.objects.filter(schedule_id=vd)
    copy = WO_Copy_Info.objects.filter(wo=vd)
    
    # add = UserCompanyDataMain.objects.get(user_id=vd.vendor_id.ContactNo)
    return render(request, 'po/area_store/rca_wo_view.html',
                  {'vd': vd, 'copy': copy, 'schedule': schedule})


def all_rca_ro(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id

    areastore=AreaStore_Officer.objects.get(Officer=officer)

    data=RO_Info.objects.filter(store=areastore.AreaStore.id,digi_flag_ro=1).order_by('-id')
    
    
    return render(request, 'po/area_store/all_rca_ro.html', {'data': data})


# def rca_ro_view(request, id):
#     vd = RO_Info.objects.get(id=id)
#     schedule = RO_Schedule_Info.objects.filter(ro_id=vd)
#     copy = RO_Copy.objects.filter(ro=vd)
#     ro_m = RO_Material_Info.objects.filter(ro=vd)
#     today = date.today()
#     return render(request, 'po/area_store/RCA_ro_view.html',
#                   {'vd': vd, 'copy': copy, 'date': today, 'schedule': schedule, 'material': ro_m})


def rca_ro_view(request, id):
    vd = RO_Info.objects.get(id=id)
    schedule = RO_Schedule_Info.objects.get(ro_id=vd)
    schedule_ro = RO_Schedule_Info.objects.get(ro_id=vd)

    copy = RO_Copy.objects.filter(ro=vd)
    ro_m = RO_Material_Info.objects.filter(ro=vd)

    # add = UserCompanyDataMain.objects.get(user_id=vd.wo.vendor_id.ContactNo)
    return render(request, 'po/area_store/RCA_ro_view.html',
                  {'vd': vd, 'copy': copy, 'schedule': schedule, 'material': ro_m, 'schedule_ro': schedule_ro})


def create_rca_di(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)    

    data=RO_Info.objects.filter(store=areastore.AreaStore.id,digi_flag_ro=1).order_by('-id')
    
    return render(request, 'po/area_store/create_rca_di.html', {'data': data})
    
    
def as_issue_mat_gp_add(request,id):
    ro = RO_Info.objects.get(id=id)
    gp_det = as_issue_gatepass.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    return render(request, 'po/area_store/as_issue_mat_gp.html', {'ro':ro,"gp":gp_det,"material": material})    


def as_issue_mat_gp(request,id):
    if request.method == "POST":
        # material = request.POST.get("material")

        # person_resource = PersonResource()

        ro = RO_Info.objects.get(id=id)
        gp_dt = request.POST.get('as_gatepass_date')
        gp_no = request.POST.get('as_gatepass_no')
        gp_pr = request.POST.get('as_gk_name')

        as_gatepass=as_issue_gatepass(ro=ro,as_issue_gp_num=gp_no,as_issue_gp_date=gp_dt,as_issue_pr_name=gp_pr)
        as_gatepass.save()
    ro = RO_Info.objects.get(id=id)
    gp_det = as_issue_gatepass.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    return render(request, 'po/area_store/as_issue_mat_gp.html', {'ro':ro,"gp":gp_det,"material": material})


def export(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(
        dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response

#############upload#######


def create_rca_di_add_material(request, id):
    if request.method == "POST":
        # material = request.POST.get("material")

        # person_resource = PersonResource()

        # ro = RO_Info.objects.get(id=id)
        # gp_dt = request.POST.get('as_gatepass_date')
        # gp_no = request.POST.get('as_gatepass_no')
        # gp_pr = request.POST.get('as_gk_name')

        # as_gatepass=as_issue_gatepass(ro=ro,as_issue_gp_num=gp_no,as_issue_gp_date=gp_dt,as_issue_pr_name=gp_pr)
        # as_gatepass.save()


        dataset = Dataset()
        new_persons = request.FILES['myfile']

        # ro = RO_Info.object.get(id=id)
        imported_data = dataset.load(new_persons.read(), format='xlsx')
        for data in imported_data:
            # if data[2] == material :
            ro = RO_Info.objects.get(id=id)
            material = request.POST.get('material')
            ro_sched = RO_Material_XMR_Info(ro=ro, material=RO_Material_Info.objects.get(id=material), xmr=data[0], as_issue_gp=as_issue_gatepass.objects.filter(ro=ro).last())
            ro_sched.save()
           
  
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    gp_det = as_issue_gatepass.objects.filter(ro=ro)
    return render(request, 'po/area_store/create_rca_di1.html', {'ro': ro, "material": material, "xmr": xmr,"gp":gp_det})

def all_rca_di(request):
    data = RO_Info.objects.all()
    return render(request, 'po/area_store/all_rca_ro.html', {'data': data})


def rca_di_view(request, id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    gp_det = as_issue_gatepass.objects.filter(ro=ro)
    return render(request, 'po/area_store/rca_di_view.html',
                  {'ro': ro, "material": material, "xmr": xmr ,"gp":gp_det})


def all_oil_request(request):
    data = Oil_Request.objects.all()
    return render(request, 'po/area_store/all_oil_request.html', {'data': data})


def oil_request_forward(request, id):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    data = WO_Info.objects.filter(vendor_id=user.User_Id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        oil = Oil_Request.objects.get(id=id)
        oil.available_quantity = quantity
        oil.as_forward_to_rca=1
        oil.save()
        data = Oil_Request.objects.all()
        return render(request, 'po/area_store/all_oil_request.html', {'data': data})
    oil = Oil_Request.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=oil.ro)
    material = RO_Material_Info.objects.filter(ro_id=oil.ro)
    return render(request, 'po/area_store/oil_request_forward.html',
                  {'ro': oil.ro,'oil':oil,"material": material, "xmr": xmr})


# def rca_as_vn_info(request):
#     data = RO_Info.objects.all()
#     return render(request, 'po/area_store/rca_as_vn_info.html',{'data': data})

# def  rca_search_xmr(request,id):
#     xmr=RO_Material_XMR_Info.objects.filter(id=id)
#     ro = RO_Info.objects.get(id=id)
#     m_offer=material_offer.objects.filter(ro=id)
#     print("m_offerm_offerm_offerm_offerm_offerm_offer: ", m_offer)
#     for i in m_offer:
#         print("i.quanity_offeredi.quanity_offeredi.quanity_offeredi.quanity_offered::::::::::: ", i.quanity_offered)
#     # m_offer1=material_offer.objects.get(ro=id)
#     # m_offer1=material_offer.objects.get(id=id)

#     rmi = RO_Material_Info.objects.filter(ro_id=ro)
#     print("rmirmirmirmirmirmirmirmirmirmi: ", rmi)
#     # print("rmirmirmirmirmirmirmirmi:::::::::::::::::::::  ", rmi.mo_capacity)
#     # for j in rmi:
#     #     print("j.mo_capacity:::::::::::::::", j.mo_capacity)

#     return render(request,'po/area_store/rca_search_xmr.html',{'xmr':xmr,"m_offer":m_offer,"ro":ro, "rmi":rmi})



def rca_as_repaired_inward_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)    

    data=RO_Info.objects.filter(store=areastore.AreaStore.id,digi_flag_ro=1).order_by('-id')
    
    # data = RO_Info.objects.filter( digi_flag_ro=1).order_by("-id")
    return render(request, 'po/area_store/rca_as_repaired_inward_list.html', {'data': data})


    
def power_analyser(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)    

    data=RO_Info.objects.filter(store=areastore.AreaStore.id,digi_flag_ro=1).order_by('-id')
    # data = RO_Info.objects.all().order_by("-id")
    return render(request, 'po/area_store/power_analyser_list.html', {'data': data})



def rca_as_repaired_inward(request, id):
    
    ro = RO_Info.objects.get(id=id)
    drr_det=drr_info.objects.filter(drr_no=ro) 
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro, vendor_send=1)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    report=material_offer.objects.filter(ro=ro)
    return render(request, 'po/area_store/rca_as_repaired_inward_chg.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"drr":drr_det,"rep":report})


def power_analyser_inward(request, id):

    
    ro = RO_Info.objects.get(id=id)
    if ro.store.Name=="Area Store Bhopal" or ro.store.Name=="Depo Store Itarsi":
        drr_det=drr_info.objects.filter(drr_no=ro)
        xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
        rca_xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,physical_status=1)
        # for j in rca_xmr:
        #     print("jjjjjjjjjjjjjjjjjjjjjjjjjj",j.xmr)
        #     api_xmr=rca_test_rept_power_analyzer.objects.all()
        #     print("kkkkkkkkkkkkkkkkkkkk",api_xmr)
        #     for i in api_xmr:
        #         print("llllllllllllllllllllll",i.xmr)
        #         if i.xmr == j.xmr:
        #             print("dddddddddddddddddddddddddddddd")
        #             j.pa_api=rca_test_rept_power_analyzer.objects.get(xmr==j.xmr)

        #             j.save()
        #             print("lllllllllllllllll",j.xmr)


        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)


       

        ro1 = RO_Info.objects.get(id=id)
       
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

        xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        
        count=0
        for i in ro_mat:
            quant=i.quantity
            count=count+quant
            print(count)
            if count==xmr_re+xmr_ue:
            # i.forward_mat_to_cgm=1
            # i.save()
                rel=RO_Info.objects.get(id=id)
                rel.mrc_flag=1
                rel.save()
            else:
                rel=RO_Info.objects.get(id=id)
                rel.mrc_flag=0
                rel.save()

       
        ro1 = RO_Info.objects.get(id=id) 
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        
       
        for i in ro_mat:
            quant=i.quantity
            xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

          

            xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
            
            
            if quant==xmr_re+xmr_ue:
                i.forward_mat_to_cgm=1
                i.save()
                # rel=RO_Info.objects.get(id=id)
                # rel.mrc_flag=1
                # rel.save()

        

        ro1 = RO_Info.objects.get(id=id)
       
        rel_pa_quant=[]
        rel_ue_quant=[]
        rel_forward_cgm=[]
        rel_mat_rating=[]
        # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
        # for p in ro_mat:
        rel_mat_rating.append(ro1.id)
        rel_forward_cgm.append(ro1.mrc_flag)

        pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
        ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        rel_pa_quant.append(pa)
        rel_ue_quant.append(ue)

        relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



        ro1 = RO_Info.objects.get(id=id)
    
        pa_quant=[]
        ue_quant=[]
        forward_cgm=[]
        mat_rating=[]
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)
        for p in ro_mat:
            mat_rating.append(p.rating)
            forward_cgm.append(p.forward_mat_to_cgm )

            pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
            ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
            pa_quant.append(pa)
            ue_quant.append(ue)

        totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)


        
        return render(request, 'po/area_store/power_analyzer_inward_chg.html', {'ro': ro, "material": material, "xmr": rca_xmr, 'mo': mo, "xmr_t": xmr_tot,'drr':drr_det,"tzip":totzip,"rzip":relzip})
    
    elif (ro.store.Name=="Area Store Gwalior" or ro.store.Name=="Area Store Guna" or ro.store.Name=="Area Store Jabalpur" or ro.store.Name=="Area Store Ujjain"
	  or ro.store.Name=="Area Store Chhindwara" or ro.store.Name=="Area Store Chhatarpur" or ro.store.Name=="Area Store Satna" 
	  or ro.store.Name=="Area Store Shahdol" or ro.store.Name=="Area Store Sagar" or ro.store.Name=="Area Store Dhar"
	  or ro.store.Name=="Area Store Indore" or ro.store.Name=="Area Store Barwaha" or ro.store.Name=="Area Store Mandsaur" or ro.store.Name=="Area Store Ratlam"):
        drr_det=drr_info.objects.filter(drr_no=ro)
        xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
        rca_xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,physical_status=1)
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)
        pa_rt=Pa_report.objects.filter(rel=ro)
        print("kkkkkkkkkkkkkkkkk",pa_rt)

                
                
      


        ro1 = RO_Info.objects.get(id=id)
       
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

        xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        
        count=0
        for i in ro_mat:
            quant=i.quantity
            count=count+quant
            print(count)
            if count==xmr_re+xmr_ue:
            # i.forward_mat_to_cgm=1
            # i.save()
                rel=RO_Info.objects.get(id=id)
                rel.mrc_flag=1
                rel.save()
            else:
                rel=RO_Info.objects.get(id=id)
                rel.mrc_flag=0
                rel.save()

       
        ro1 = RO_Info.objects.get(id=id) 
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        
       
        for i in ro_mat:
            quant=i.quantity
            xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

          

            xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
            
            
            if quant==xmr_re+xmr_ue:
                i.forward_mat_to_cgm=1
                i.save()
                # rel=RO_Info.objects.get(id=id)
                # rel.mrc_flag=1
                # rel.save()

        

        ro1 = RO_Info.objects.get(id=id)
       
        rel_pa_quant=[]
        rel_ue_quant=[]
        rel_forward_cgm=[]
        rel_mat_rating=[]
        # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
        # for p in ro_mat:
        rel_mat_rating.append(ro1.id)
        rel_forward_cgm.append(ro1.mrc_flag)

        pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
        ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        rel_pa_quant.append(pa)
        rel_ue_quant.append(ue)

        relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



        ro1 = RO_Info.objects.get(id=id)
    
        pa_quant=[]
        ue_quant=[]
        forward_cgm=[]
        mat_rating=[]
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)
        for p in ro_mat:
            mat_rating.append(p.rating)
            forward_cgm.append(p.forward_mat_to_cgm )

            pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
            ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
            pa_quant.append(pa)
            ue_quant.append(ue)

        totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)


        
        return render(request, 'po/area_store/power_analyzer_inward_accepted_chg_2.html', {'ro': ro, "material": material, "xmr": rca_xmr, 'mo': mo, "xmr_t": xmr_tot,'drr':drr_det,
            "tzip":totzip,"pa_report":pa_rt,"rzip":relzip})

    
   
    

    else:
        drr_det=drr_info.objects.filter(drr_no=ro)
        xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
        rca_xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,physical_status=1)
        # for j in rca_xmr:
        #     print("jjjjjjjjjjjjjjjjjjjjjjjjjj",j.xmr)
        #     api_xmr=rca_test_rept_power_analyzer.objects.all()
        #     print("kkkkkkkkkkkkkkkkkkkk",api_xmr)
        #     for i in api_xmr:
        #         print("llllllllllllllllllllll",i.xmr)
        #         if i.xmr == j.xmr:
        #             print("dddddddddddddddddddddddddddddd")
        #             j.pa_api=rca_test_rept_power_analyzer.objects.get(xmr==j.xmr)

        #             j.save()
        #             print("lllllllllllllllll",j.xmr)


        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)


        ro1 = RO_Info.objects.get(id=id)
       
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

        xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        
        count=0
        for i in ro_mat:
            quant=i.quantity
            count=count+quant
            print(count)
            if count==xmr_re+xmr_ue:
            # i.forward_mat_to_cgm=1
            # i.save()
                rel=RO_Info.objects.get(id=id)
                rel.mrc_flag=1
                rel.save()
            else:
                rel=RO_Info.objects.get(id=id)
                rel.mrc_flag=0
                rel.save()

       
        ro1 = RO_Info.objects.get(id=id) 
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        
       
        for i in ro_mat:
            quant=i.quantity
            xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

          

            xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
            
            
            if quant==xmr_re+xmr_ue:
                i.forward_mat_to_cgm=1
                i.save()
                # rel=RO_Info.objects.get(id=id)
                # rel.mrc_flag=1
                # rel.save()

        

        ro1 = RO_Info.objects.get(id=id)
       
        rel_pa_quant=[]
        rel_ue_quant=[]
        rel_forward_cgm=[]
        rel_mat_rating=[]
        # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
        # for p in ro_mat:
        rel_mat_rating.append(ro1.id)
        rel_forward_cgm.append(ro1.mrc_flag)

        pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
        ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        rel_pa_quant.append(pa)
        rel_ue_quant.append(ue)

        relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



        ro1 = RO_Info.objects.get(id=id)
    
        pa_quant=[]
        ue_quant=[]
        forward_cgm=[]
        mat_rating=[]
        ro_mat=RO_Material_Info.objects.filter(ro=ro1)
        for p in ro_mat:
            mat_rating.append(p.rating)
            forward_cgm.append(p.forward_mat_to_cgm )

            pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
            ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
            pa_quant.append(pa)
            ue_quant.append(ue)

        totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)



      


        
        return render(request,'po/area_store/power_analyzer_inward_chg_normal.html',{'ro':ro,"material": material,"xmr": rca_xmr, 'mo': mo, "xmr_t":xmr_tot,'drr':drr_det,"tzip":totzip,"rzip":relzip})




    


def drr_rel_details(request,id):
    ro = RO_Info.objects.get(id=id)
    # xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, vendor_send=1)|Q(ro=ro,as_xmr_rej_resubmit=1))
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro, vendor_send=1,as_accepted=0)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    drr_det=drr_info.objects.filter(drr_no=ro)
    return render(request,'po/area_store/drr_info.html',{'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"drr":drr_det})


def drr_details(request,id):
    if request.method == "POST":
        info=RO_Info.objects.get(id=id)
        drr_ord_date = request.POST.get('drr_date')
        drr_challan_num=request.POST.get('challan_no')
        drr_challan_d=request.POST.get('challan_date')
        drr_veh=request.POST.get('vehicle')
        drr_quant=request.POST.get('quantity')

        data1 = drr_info(drr_no=info, drr_date=drr_ord_date,drr_vehicle=drr_veh,drr_challan_no=drr_challan_num,
                         drr_challan_date=drr_challan_d,drr_quantity=drr_quant)
        data1.save()

        ro = RO_Info.objects.get(id=id)
        drr_det=drr_info.objects.filter( drr_no=ro)
        # xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, vendor_send=1)|Q(ro=ro,as_xmr_rej_resubmit=1))
        xmr = RO_Material_XMR_Info.objects.filter(ro=ro, vendor_send=1)
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)

        return render(request,'po/area_store/drr_info.html',{'ro': ro, "material": material, "xmr": xmr,'mo': mo,"drr":drr_det})
    ro = RO_Info.objects.get(id=id)
    drr_det=drr_info.objects.filter(drr_no=ro)    
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro, vendor_send=1)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    return render(request,'po/area_store/drr_info.html',{'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"drr":drr_det})





def rca_as_repaired_inward_accepted(request,id):
    if request.method == "POST":
        
        abc = request.POST.getlist('xmr_det')
        for data in abc:
            test = RO_Material_XMR_Info.objects.get(id=data)
            reject=request.POST.get(test.xmr)
            test.as_remark=reject
            test.as_accepted = 1
            test.save()
          


        accept=request.POST.getlist("accepted")
        for data1 in accept:
            
            test1 = RO_Material_XMR_Info.objects.get(id=data1)
            test1.physical_status = 1
            test1.acceptted_date=date.today()

                   

            ro = RO_Info.objects.get(id=id)
            drr_infos=drr_info.objects.filter(drr_no=ro.id).last()
            test1.drr_details=drr_infos
            test1.save()

        reject=request.POST.getlist("rejected")
        for data2 in reject:
            test2 = RO_Material_XMR_Info.objects.get(id=data2)
            test2.physical_status = -1
            test2.acceptted_date=date.today()


            ro = RO_Info.objects.get(id=id)
            drr_infos=drr_info.objects.filter(drr_no=ro.id).last()
            test2.drr_details=drr_infos
            test2.save()
                   


        ro = RO_Info.objects.get(id=ro.id)
        drr_det=drr_info.objects.filter(drr_no=ro)
        xmr = RO_Material_XMR_Info.objects.filter(ro=ro.id,vendor_send=1)
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)
        report=material_offer.objects.filter(ro=ro)
        return render(request, 'po/area_store/rca_as_repaired_inward_chg.html', {'ro': ro, "material": material, "xmr": xmr, "mo": mo,'drr':drr_det,"rep":report})




def power_analyser_inward_accepted(request, id):
    a=1
    b=2
    c=3

    ro=RO_Info.objects.get(id=id)


    if ro.store.Name=="Area Store Bhopal" or ro.store.Name=="Depo Store Itarsi":
    
        if request.method == "POST":

                
            abc = request.POST.getlist('xmr_det')
            for data in abc:
                test = RO_Material_XMR_Info.objects.get(id=data)

                api_xmr=rca_test_rept_power_analyzer.objects.all()
                for i in api_xmr:
                    if i.xmr == test.xmr:
                        # test.pa_api=rca_test_rept_power_analyzer.objects.get(xmr=test.xmr)
                        
                        test.pa_api=rca_test_rept_power_analyzer.objects.filter(xmr=test.xmr).last()

                        test.save()
                        
                
                
                        remark=request.POST.get(test.xmr)
                        test.pa_remark=remark
                        
                        test.pa_result_date=date.today()

                        # if request.FILES:
                        #     power_report1 = request.FILES['remark']
                        #     test.analyser_rprt = power_report1
                        #     test.pa_report_flag = 1

                            

                        #     test.save()



                        if test.new_design==1 or test.design_non_star==1:
                            no_load_loss=request.POST.get('aa'+test.xmr)
                            test.pa_no_loss=test.pa_api.NLpower

                        max_load_loss=request.POST.get('bb'+test.xmr)
                        
                        test.pa_max_loss=test.pa_api.TotalLossat75  
                        
                        test.pa_result_submitted = 1

                        # if request.FILES:
                        #     power_report1 = request.FILES['power_report']
                        #     test.analyser_rprt = power_report1
                        #     test.pa_report_flag = 1
                            
                        
                        if test.new_design == 1:
                            
                            if test.material.rating=="25KVA":
                                nd=power_analyser_newdesign.objects.get(rating="25KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()

                                no_load_percent=test.pa_no_loss_per
                                
                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()

                            
                                max_load_percent=test.pa_max_loss_per
                                

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()
                                
                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()
                                    

                                
                                
                            elif test.material.rating=="63KVA":
                                nd=power_analyser_newdesign.objects.get(rating="63KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()

                                no_load_percent=test.pa_no_loss_per

                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()

                                max_load_percent=test.pa_max_loss_per
                                

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()
                                
                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()
                                
                                
                            elif test.material.rating=="100KVA":
                                nd=power_analyser_newdesign.objects.get(rating="100KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()

                                no_load_percent=test.pa_no_loss_per

                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()


                                max_load_percent=test.pa_max_loss_per
                                

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()
                                
                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()
                                

                            elif test.material.rating=="200KVA":
                                nd=power_analyser_newdesign.objects.get(rating="200KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()

                                no_load_percent=test.pa_no_loss_per

                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()

                                max_load_percent=test.pa_max_loss_per
                                

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()
                                
                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()
					
                        if test.design_non_star == 1:
			    
                            if test.material.rating=="25KVA":
                                nd=power_analyser_nonstar_newdesign.objects.get(rating="25KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()

                                no_load_percent=test.pa_no_loss_per
                    
                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()

                
                                max_load_percent=test.pa_max_loss_per
                    

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()
                        
                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()
                        
                
                            elif test.material.rating=="63KVA":
                                nd=power_analyser_newdesign.objects.get(rating="63KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()
                                
                                no_load_percent=test.pa_no_loss_per

                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()

                                max_load_percent=test.pa_max_loss_per
                    

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()
                    
                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()
				
                            elif test.material.rating=="100KVA":
                                nd=power_analyser_newdesign.objects.get(rating="100KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()

                                no_load_percent=test.pa_no_loss_per

                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()


                                max_load_percent=test.pa_max_loss_per
                   

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()
                                    
                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()
				
                            elif test.material.rating=="200KVA":
                                nd=power_analyser_newdesign.objects.get(rating="200KVA")
                                input_no_loss=float(test.pa_no_loss)
                                def_no_loss=float(nd.no_load_redstrip)
                                per=((input_no_loss-def_no_loss)/def_no_loss)*100
                                test.pa_no_loss_per=per
                                input_max_loss=float(test.pa_max_loss)
                                def_max_loss=float(nd.max_load_loss)
                                full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                                test.pa_max_loss_per=full_per
                                test.save()

                                no_load_percent=test.pa_no_loss_per

                                if no_load_percent < 0:
                                    test.pa_no_loss_per=0.0
                                    test.save()

                                max_load_percent=test.pa_max_loss_per


                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()

                        elif test.old_l1 == 1:
                            

                            if test.material.rating=="25KVA":
                                nd=power_analyser_level1.objects.get(rating="25KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()




                            elif test.material.rating=="63KVA":
                                nd=power_analyser_level1.objects.get(rating="63KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()


                                
                            elif test.material.rating=="100KVA":
                                nd=power_analyser_level1.objects.get(rating="100KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()

                                
                            elif test.material.rating=="200KVA":
                                nd=power_analyser_level1.objects.get(rating="200KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()


                        elif test.old_l2 == 1:
                            

                            if test.material.rating=="25KVA":
                                nd=power_analyser_level2.objects.get(rating="25KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0.0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0.0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()

                                
                            elif test.material.rating=="63KVA":
                                nd=power_analyser_level2.objects.get(rating="63KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0.0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0.0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()

                                

                            elif test.material.rating=="100KVA":
                                nd=power_analyser_level2.objects.get(rating="100KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0.0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0.0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()


                            elif test.material.rating=="200KVA":
                                
                                nd=power_analyser_level2.objects.get(rating="200KVA")
                                input = float(test.pa_max_loss)
                                total_loss = float(nd.total_loss_100)
                                per=((input-total_loss)/total_loss)*100
                                test.pa_max_loss_per=per
                                test.save()

                                max_load_percent=test.pa_max_loss_per

                                if max_load_percent <= 0.0:
                                    test.pa_max_loss_per=0.0
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent <= 15 and max_load_percent > 0.0:
                                    test.pa_result=1
                                    test.save()

                                elif max_load_percent > 15:
                                    test.pa_result=-1
                                    test.save()

                            test.save()

                    
                    else:
                        continue

                 





         

            

            ro1 = RO_Info.objects.get(id=id)
            
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)

            xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

            xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
            
            count=0
            for i in ro_mat:
                quant=i.quantity
                count=count+quant
                print(count)
                if count==xmr_re+xmr_ue:
                # i.forward_mat_to_cgm=1
                # i.save()
                    rel=RO_Info.objects.get(id=id)
                    rel.mrc_flag=1
                    rel.save()
                else:
                    rel=RO_Info.objects.get(id=id)
                    rel.mrc_flag=0
                    rel.save()

            
            ro1 = RO_Info.objects.get(id=id) 
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)

            
            
            for i in ro_mat:
                quant=i.quantity
                xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

                

                xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
                
                
                if quant==xmr_re+xmr_ue:
                    i.forward_mat_to_cgm=1
                    i.save()
                else:
                    i.forward_mat_to_cgm=0
                    i.save()
                    # rel=RO_Info.objects.get(id=id)
                    # rel.mrc_flag=1
                    # rel.save()

            

            ro1 = RO_Info.objects.get(id=id)
            
            rel_pa_quant=[]
            rel_ue_quant=[]
            rel_forward_cgm=[]
            rel_mat_rating=[]
            # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
            # for p in ro_mat:
            rel_mat_rating.append(ro1.id)
            rel_forward_cgm.append(ro1.mrc_flag)

            pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
            ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
            rel_pa_quant.append(pa)
            rel_ue_quant.append(ue)

            relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



            ro1 = RO_Info.objects.get(id=id)

            pa_quant=[]
            ue_quant=[]
            forward_cgm=[]
            mat_rating=[]
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)
            for p in ro_mat:
                mat_rating.append(p.rating)
                forward_cgm.append(p.forward_mat_to_cgm )

                pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
                ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
                pa_quant.append(pa)
                ue_quant.append(ue)

            totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)



            ro = RO_Info.objects.get(id=id)
            xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro)
            xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,as_accepted=1,physical_status=1)
            material = RO_Material_Info.objects.filter(ro_id=ro)
            mo = material_offer.objects.filter(ro_id=ro)
            return render(request, 'po/area_store/power_analyzer_inward_chg.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot,"aa":a,"bb":b,"tzip":totzip,
                "cc":c,"rzip":relzip})

        ro = RO_Info.objects.get(id=id)
        xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
        xmr = RO_Material_XMR_Info.objects.filter(
            ro=ro, as_accepted=1, physical_status=1, uneco_status=0)
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)
        return render(request, 'po/area_store/power_analyzer_inward_chg.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot})


    
    elif (ro.store.Name=="Area Store Gwalior" or ro.store.Name=="Area Store Guna" or ro.store.Name=="Area Store Jabalpur" or ro.store.Name=="Area Store Ujjain"or ro.store.Name=="Area Store Chhindwara" 
        or ro.store.Name=="Area Store Chhatarpur" or ro.store.Name=="Area Store Satna" or ro.store.Name=="Area Store Shahdol" or ro.store.Name=="Area Store Sagar" or ro.store.Name=="Area Store Dhar"
        or ro.store.Name=="Area Store Indore" or ro.store.Name=="Area Store Barwaha" or ro.store.Name=="Area Store Mandsaur" or ro.store.Name=="Area Store Ratlam"):
        
                
        if request.method == "POST":



            ro=RO_Info.objects.get(id=id)
            report=request.FILES['xmr_file1']
           
            dt=date.today()
            rt_data = Pa_report(rel=ro, power_report_flag=report,power_report_date=dt)
            rt_data.save()



         
            abc = request.POST.getlist('xmr_det')
            for data in abc:
                test = RO_Material_XMR_Info.objects.get(id=data)
                
                remark=request.POST.get(test.xmr)
                test.pa_remark=remark
                test.pa_result_date=date.today()





                # if request.FILES:
                #     power_report1 = request.FILES['cc'+test.xmr]
                #     test.analyser_rprt = power_report1
                #     test.pa_report_flag = 1

                #     print("ttttttttttttttttttttttttttttttt",test)

                #     test.save()




                if test.new_design==1 or test.design_non_star==1:
                    no_load_loss=request.POST.get('aa'+test.xmr)
                    test.pa_no_loss=no_load_loss

                max_load_loss=request.POST.get('bb'+test.xmr)
                
                test.pa_max_loss=max_load_loss
                
                test.pa_result_submitted = 1

                
                    
                
                if test.new_design == 1:
                    
                    if test.material.rating=="25KVA":
                        nd=power_analyser_newdesign.objects.get(rating="25KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per
                        
                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                    
                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                            

                        
                        
                    elif test.material.rating=="63KVA":
                        nd=power_analyser_newdesign.objects.get(rating="63KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                        
                        
                    elif test.material.rating=="100KVA":
                        nd=power_analyser_newdesign.objects.get(rating="100KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()


                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                        

                    elif test.material.rating=="200KVA":
                        nd=power_analyser_newdesign.objects.get(rating="200KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                
                if test.design_non_star == 1:
			    
                    if test.material.rating =="25KVA":
                        nd=power_analyser_nonstar_newdesign.objects.get(rating="25KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per
                    
                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                
                        max_load_percent=test.pa_max_loss_per
                    

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                    
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                        
                
                    elif test.material.rating=="63KVA":
                        nd=power_analyser_newdesign.objects.get(rating="63KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()
                                        
                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                        max_load_percent=test.pa_max_loss_per


                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
				
                    elif test.material.rating=="100KVA":
                        nd=power_analyser_newdesign.objects.get(rating="100KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()


                        max_load_percent=test.pa_max_loss_per


                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
				
                    elif test.material.rating=="200KVA":
                        nd=power_analyser_newdesign.objects.get(rating="200KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                        max_load_percent=test.pa_max_loss_per


                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
				

                elif test.old_l1 == 1:
                    

                    if test.material.rating=="25KVA":
                        nd=power_analyser_level1.objects.get(rating="25KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()




                    elif test.material.rating=="63KVA":
                        nd=power_analyser_level1.objects.get(rating="63KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()


                        
                    elif test.material.rating=="100KVA":
                        nd=power_analyser_level1.objects.get(rating="100KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                        
                    elif test.material.rating=="200KVA":
                        nd=power_analyser_level1.objects.get(rating="200KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()


                elif test.old_l2 == 1:
                    

                    if test.material.rating=="25KVA":
                        nd=power_analyser_level2.objects.get(rating="25KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                        
                    elif test.material.rating=="63KVA":
                        nd=power_analyser_level2.objects.get(rating="63KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                        

                    elif test.material.rating=="100KVA":
                        nd=power_analyser_level2.objects.get(rating="100KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()


                    elif test.material.rating=="200KVA":
                        
                        nd=power_analyser_level2.objects.get(rating="200KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                    test.save()





           

            

            ro1 = RO_Info.objects.get(id=id)
            
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)

            xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

            xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
            
            count=0
            for i in ro_mat:
                quant=i.quantity
                count=count+quant
                print(count)
                if count==xmr_re+xmr_ue:
                # i.forward_mat_to_cgm=1
                # i.save()
                    rel=RO_Info.objects.get(id=id)
                    rel.mrc_flag=1
                    rel.save()
                else:
                    rel=RO_Info.objects.get(id=id)
                    rel.mrc_flag=0
                    rel.save()

            
            ro1 = RO_Info.objects.get(id=id) 
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)

            
            
            for i in ro_mat:
                quant=i.quantity
                xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

                

                xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
                
                
                if quant==xmr_re+xmr_ue:
                    i.forward_mat_to_cgm=1
                    i.save()
                else:
                    i.forward_mat_to_cgm=0
                    i.save()
                    # rel=RO_Info.objects.get(id=id)
                    # rel.mrc_flag=1
                    # rel.save()

            

            ro1 = RO_Info.objects.get(id=id)
            
            rel_pa_quant=[]
            rel_ue_quant=[]
            rel_forward_cgm=[]
            rel_mat_rating=[]
            # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
            # for p in ro_mat:
            rel_mat_rating.append(ro1.id)
            rel_forward_cgm.append(ro1.mrc_flag)

            pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
            ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
            rel_pa_quant.append(pa)
            rel_ue_quant.append(ue)

            relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



            ro1 = RO_Info.objects.get(id=id)

            pa_quant=[]
            ue_quant=[]
            forward_cgm=[]
            mat_rating=[]
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)
            for p in ro_mat:
                mat_rating.append(p.rating)
                forward_cgm.append(p.forward_mat_to_cgm )

                pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
                ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
                pa_quant.append(pa)
                ue_quant.append(ue)

            totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)





            ro = RO_Info.objects.get(id=id)
            xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro)
            xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,as_accepted=1,physical_status=1)
            material = RO_Material_Info.objects.filter(ro_id=ro)
            mo = material_offer.objects.filter(ro_id=ro)
            pa_rt=Pa_report.objects.filter(rel=ro)
            return render(request, 'po/area_store/power_analyzer_inward_accepted_chg_2.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot,"aa":a,"bb":b,
                "pa_qt":pa_quant,"ue_qt":ue_quant,"mat_rt":mat_rating,"fd_cgm":forward_cgm,"tzip":totzip,"cc":c,"pa_report":pa_rt,"rzip":relzip})


        ro = RO_Info.objects.get(id=id)
        xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
        xmr = RO_Material_XMR_Info.objects.filter(
            ro=ro, as_accepted=1, physical_status=1, uneco_status=0)
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)
        
        return render(request, 'po/area_store/power_analyzer_inward_accepted_chg_2.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot})







    else:

        if request.method == "POST":

         
            abc = request.POST.getlist('xmr_det')
            for data in abc:
                test = RO_Material_XMR_Info.objects.get(id=data)
                
                remark=request.POST.get(test.xmr)
                test.pa_remark=remark
                test.pa_result_date=date.today()


                if request.FILES:
                    power_report1 = request.FILES['cc'+test.xmr]
                    test.analyser_rprt = power_report1
                    test.pa_report_flag = 1

                    

                    test.save()




                if test.new_design==1:
                    no_load_loss=request.POST.get('aa'+test.xmr)
                    test.pa_no_loss=no_load_loss

                max_load_loss=request.POST.get('bb'+test.xmr)
                
                test.pa_max_loss=max_load_loss
                
                test.pa_result_submitted = 1

                
                    
                
                if test.new_design == 1:
                    
                    if test.material.rating=="25KVA":
                        nd=power_analyser_newdesign.objects.get(rating="25KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per
                        
                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                    
                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                            

                        
                        
                    elif test.material.rating=="63KVA":
                        nd=power_analyser_newdesign.objects.get(rating="63KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                        
                        
                    elif test.material.rating=="100KVA":
                        nd=power_analyser_newdesign.objects.get(rating="100KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()


                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                        

                    elif test.material.rating=="200KVA":
                        nd=power_analyser_newdesign.objects.get(rating="200KVA")
                        input_no_loss=float(test.pa_no_loss)
                        def_no_loss=float(nd.no_load_redstrip)
                        per=((input_no_loss-def_no_loss)/def_no_loss)*100
                        test.pa_no_loss_per=per
                        input_max_loss=float(test.pa_max_loss)
                        def_max_loss=float(nd.max_load_loss)
                        full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
                        test.pa_max_loss_per=full_per
                        test.save()

                        no_load_percent=test.pa_no_loss_per

                        if no_load_percent < 0:
                            test.pa_no_loss_per=0.0
                            test.save()

                        max_load_percent=test.pa_max_loss_per
                        

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()
                        
                        elif max_load_percent > 0:
                            test.pa_result=1
                            test.save()
                        

                elif test.old_l1 == 1:
                    

                    if test.material.rating=="25KVA":
                        nd=power_analyser_level1.objects.get(rating="25KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()




                    elif test.material.rating=="63KVA":
                        nd=power_analyser_level1.objects.get(rating="63KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()


                        
                    elif test.material.rating=="100KVA":
                        nd=power_analyser_level1.objects.get(rating="100KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                        
                    elif test.material.rating=="200KVA":
                        nd=power_analyser_level1.objects.get(rating="200KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()


                elif test.old_l2 == 1:
                    

                    if test.material.rating=="25KVA":
                        nd=power_analyser_level2.objects.get(rating="25KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                        
                    elif test.material.rating=="63KVA":
                        nd=power_analyser_level2.objects.get(rating="63KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                        

                    elif test.material.rating=="100KVA":
                        nd=power_analyser_level2.objects.get(rating="100KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()


                    elif test.material.rating=="200KVA":
                        
                        nd=power_analyser_level2.objects.get(rating="200KVA")
                        input = float(test.pa_max_loss)
                        total_loss = float(nd.total_loss_100)
                        per=((input-total_loss)/total_loss)*100
                        test.pa_max_loss_per=per
                        test.save()

                        max_load_percent=test.pa_max_loss_per

                        if max_load_percent <= 0.0:
                            test.pa_max_loss_per=0.0
                            test.pa_result=1
                            test.save()

                        elif max_load_percent <= 15 and max_load_percent > 0.0:
                            test.pa_result=1
                            test.save()

                        elif max_load_percent > 15:
                            test.pa_result=-1
                            test.save()

                    test.save()






            

            ro1 = RO_Info.objects.get(id=id)
            
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)

            xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

            xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
            
            count=0
            for i in ro_mat:
                quant=i.quantity
                count=count+quant
                print(count)
                if count==xmr_re+xmr_ue:
                # i.forward_mat_to_cgm=1
                # i.save()
                    rel=RO_Info.objects.get(id=id)
                    rel.mrc_flag=1
                    rel.save()
                else:
                    rel=RO_Info.objects.get(id=id)
                    rel.mrc_flag=0
                    rel.save()

            
            ro1 = RO_Info.objects.get(id=id) 
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)

            
            
            for i in ro_mat:
                quant=i.quantity
                xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

                

                xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
                
                
                if quant==xmr_re+xmr_ue:
                    i.forward_mat_to_cgm=1
                    i.save()
                else:
                    i.forward_mat_to_cgm=0
                    i.save()
                    # rel=RO_Info.objects.get(id=id)
                    # rel.mrc_flag=1
                    # rel.save()

            

            ro1 = RO_Info.objects.get(id=id)
            
            rel_pa_quant=[]
            rel_ue_quant=[]
            rel_forward_cgm=[]
            rel_mat_rating=[]
            # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
            # for p in ro_mat:
            rel_mat_rating.append(ro1.id)
            rel_forward_cgm.append(ro1.mrc_flag)

            pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
            ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
            rel_pa_quant.append(pa)
            rel_ue_quant.append(ue)

            relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



            ro1 = RO_Info.objects.get(id=id)

            pa_quant=[]
            ue_quant=[]
            forward_cgm=[]
            mat_rating=[]
            ro_mat=RO_Material_Info.objects.filter(ro=ro1)
            for p in ro_mat:
                mat_rating.append(p.rating)
                forward_cgm.append(p.forward_mat_to_cgm )

                pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
                ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
                pa_quant.append(pa)
                ue_quant.append(ue)

            totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)



            ro = RO_Info.objects.get(id=id)
            xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro)
            xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,as_accepted=1,physical_status=1)
            material = RO_Material_Info.objects.filter(ro_id=ro)
            mo = material_offer.objects.filter(ro_id=ro)
            return render(request, 'po/area_store/power_analyzer_inward_chg_normal.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot,"aa":a,"bb":b,"pa_qt":pa_quant,"ue_qt":ue_quant,"mat_rt":mat_rating,"fd_cgm":forward_cgm,"tzip":totzip,"cc":c,"rzip":relzip})


        ro = RO_Info.objects.get(id=id)
        xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
        xmr = RO_Material_XMR_Info.objects.filter(
            ro=ro, as_accepted=1, physical_status=1, uneco_status=0)
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)
        return render(request, 'po/area_store/power_analyzer_inward_chg_normal.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot})






# def power_analyser_inward_accepted(request, id):
#     a=1
#     b=2
#     c=3

#     ro=RO_Info.objects.get(id=id)


#     if ro.store.Name=="Area Store Bhopal" or ro.store.Name=="Depo Store Itarsi":
    
#         if request.method == "POST":

                
#             abc = request.POST.getlist('xmr_det')
#             for data in abc:
#                 test = RO_Material_XMR_Info.objects.get(id=data)

#                 api_xmr=rca_test_rept_power_analyzer.objects.all()
#                 for i in api_xmr:
#                     if i.xmr == test.xmr:
#                         # test.pa_api=rca_test_rept_power_analyzer.objects.get(xmr=test.xmr)
                        
#                         test.pa_api=rca_test_rept_power_analyzer.objects.filter(xmr=test.xmr).last()

#                         test.save()
                        
                
                
#                         remark=request.POST.get(test.xmr)
#                         test.pa_remark=remark
                        
#                         test.pa_result_date=date.today()

#                         # if request.FILES:
#                         #     power_report1 = request.FILES['remark']
#                         #     test.analyser_rprt = power_report1
#                         #     test.pa_report_flag = 1

                            

#                         #     test.save()



#                         if test.new_design==1:
#                             no_load_loss=request.POST.get('aa'+test.xmr)
#                             test.pa_no_loss=test.pa_api.NLpower

#                         max_load_loss=request.POST.get('bb'+test.xmr)
                        
#                         test.pa_max_loss=test.pa_api.TotalLossat75  
                        
#                         test.pa_result_submitted = 1

#                         # if request.FILES:
#                         #     power_report1 = request.FILES['power_report']
#                         #     test.analyser_rprt = power_report1
#                         #     test.pa_report_flag = 1
                            
                        
#                         if test.new_design == 1:
                            
#                             if test.material.rating=="25KVA":
#                                 nd=power_analyser_newdesign.objects.get(rating="25KVA")
#                                 input_no_loss=float(test.pa_no_loss)
#                                 def_no_loss=float(nd.no_load_redstrip)
#                                 per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                                 test.pa_no_loss_per=per
#                                 input_max_loss=float(test.pa_max_loss)
#                                 def_max_loss=float(nd.max_load_loss)
#                                 full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                                 test.pa_max_loss_per=full_per
#                                 test.save()

#                                 no_load_percent=test.pa_no_loss_per
                                
#                                 if no_load_percent < 0:
#                                     test.pa_no_loss_per=0.0
#                                     test.save()

                            
#                                 max_load_percent=test.pa_max_loss_per
                                

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()
                                
#                                 elif max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()
                                    

                                
                                
#                             elif test.material.rating=="63KVA":
#                                 nd=power_analyser_newdesign.objects.get(rating="63KVA")
#                                 input_no_loss=float(test.pa_no_loss)
#                                 def_no_loss=float(nd.no_load_redstrip)
#                                 per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                                 test.pa_no_loss_per=per
#                                 input_max_loss=float(test.pa_max_loss)
#                                 def_max_loss=float(nd.max_load_loss)
#                                 full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                                 test.pa_max_loss_per=full_per
#                                 test.save()

#                                 no_load_percent=test.pa_no_loss_per

#                                 if no_load_percent < 0:
#                                     test.pa_no_loss_per=0.0
#                                     test.save()

#                                 max_load_percent=test.pa_max_loss_per
                                

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()
                                
#                                 elif max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()
                                
                                
#                             elif test.material.rating=="100KVA":
#                                 nd=power_analyser_newdesign.objects.get(rating="100KVA")
#                                 input_no_loss=float(test.pa_no_loss)
#                                 def_no_loss=float(nd.no_load_redstrip)
#                                 per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                                 test.pa_no_loss_per=per
#                                 input_max_loss=float(test.pa_max_loss)
#                                 def_max_loss=float(nd.max_load_loss)
#                                 full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                                 test.pa_max_loss_per=full_per
#                                 test.save()

#                                 no_load_percent=test.pa_no_loss_per

#                                 if no_load_percent < 0:
#                                     test.pa_no_loss_per=0.0
#                                     test.save()


#                                 max_load_percent=test.pa_max_loss_per
                                

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()
                                
#                                 elif max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()
                                

#                             elif test.material.rating=="200KVA":
#                                 nd=power_analyser_newdesign.objects.get(rating="200KVA")
#                                 input_no_loss=float(test.pa_no_loss)
#                                 def_no_loss=float(nd.no_load_redstrip)
#                                 per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                                 test.pa_no_loss_per=per
#                                 input_max_loss=float(test.pa_max_loss)
#                                 def_max_loss=float(nd.max_load_loss)
#                                 full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                                 test.pa_max_loss_per=full_per
#                                 test.save()

#                                 no_load_percent=test.pa_no_loss_per

#                                 if no_load_percent < 0:
#                                     test.pa_no_loss_per=0.0
#                                     test.save()

#                                 max_load_percent=test.pa_max_loss_per
                                

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()
                                
#                                 elif max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()
                                

#                         elif test.old_l1 == 1:
                            

#                             if test.material.rating=="25KVA":
#                                 nd=power_analyser_level1.objects.get(rating="25KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()




#                             elif test.material.rating=="63KVA":
#                                 nd=power_analyser_level1.objects.get(rating="63KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()


                                
#                             elif test.material.rating=="100KVA":
#                                 nd=power_analyser_level1.objects.get(rating="100KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()

                                
#                             elif test.material.rating=="200KVA":
#                                 nd=power_analyser_level1.objects.get(rating="200KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()


#                         elif test.old_l2 == 1:
                            

#                             if test.material.rating=="25KVA":
#                                 nd=power_analyser_level2.objects.get(rating="25KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0.0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0.0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()

                                
#                             elif test.material.rating=="63KVA":
#                                 nd=power_analyser_level2.objects.get(rating="63KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0.0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0.0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()

                                

#                             elif test.material.rating=="100KVA":
#                                 nd=power_analyser_level2.objects.get(rating="100KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0.0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0.0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()


#                             elif test.material.rating=="200KVA":
                                
#                                 nd=power_analyser_level2.objects.get(rating="200KVA")
#                                 input = float(test.pa_max_loss)
#                                 total_loss = float(nd.total_loss_100)
#                                 per=((input-total_loss)/total_loss)*100
#                                 test.pa_max_loss_per=per
#                                 test.save()

#                                 max_load_percent=test.pa_max_loss_per

#                                 if max_load_percent <= 0.0:
#                                     test.pa_max_loss_per=0.0
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent <= 15 and max_load_percent > 0.0:
#                                     test.pa_result=1
#                                     test.save()

#                                 elif max_load_percent > 15:
#                                     test.pa_result=-1
#                                     test.save()

#                             test.save()

                    
#                     else:
#                         continue

#                     #     return HttpResponse("xmr not found")






#             ro1 = RO_Info.objects.get(id=id)
       
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)

#             xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

#             xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        
#             count=0
#             for i in ro_mat:
#                 quant=i.quantity
#                 count=count+quant
#                 print(count)
#                 if count==xmr_re+xmr_ue:
#                 # i.forward_mat_to_cgm=1
#                 # i.save()
#                     rel=RO_Info.objects.get(id=id)
#                     rel.mrc_flag=1
#                     rel.save()
#                 else:
#                     rel=RO_Info.objects.get(id=id)
#                     rel.mrc_flag=0
#                     rel.save()

       
#             ro1 = RO_Info.objects.get(id=id) 
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        
       
#             for i in ro_mat:
#                 quant=i.quantity
#                 xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

          

#                 xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
            
            
#                 if quant==xmr_re+xmr_ue:
#                     i.forward_mat_to_cgm=1
#                     i.save()
#                     # rel=RO_Info.objects.get(id=id)
#                     # rel.mrc_flag=1
#                     # rel.save()

        

#             ro1 = RO_Info.objects.get(id=id)
       
#             rel_pa_quant=[]
#             rel_ue_quant=[]
#             rel_forward_cgm=[]
#             rel_mat_rating=[]
#             # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
#             # for p in ro_mat:
#             rel_mat_rating.append(ro1.id)
#             rel_forward_cgm.append(ro1.mrc_flag)

#             pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
#             ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
#             rel_pa_quant.append(pa)
#             rel_ue_quant.append(ue)

#             relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



#             ro1 = RO_Info.objects.get(id=id)
    
#             pa_quant=[]
#             ue_quant=[]
#             forward_cgm=[]
#             mat_rating=[]
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)
#             for p in ro_mat:
#                 mat_rating.append(p.rating)
#                 forward_cgm.append(p.forward_mat_to_cgm )

#                 pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
#                 ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
#                 pa_quant.append(pa)
#                 ue_quant.append(ue)

#             totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)





#             ro = RO_Info.objects.get(id=id)
#             xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro)
#             xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,as_accepted=1,physical_status=1)
#             material = RO_Material_Info.objects.filter(ro_id=ro)
#             mo = material_offer.objects.filter(ro_id=ro)
#             return render(request, 'po/area_store/power_analyzer_inward_chg.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot,"aa":a,"bb":b,"tzip":totzip,
#                 "cc":c,"rzip":relzip})

#         ro = RO_Info.objects.get(id=id)
#         xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
#         xmr = RO_Material_XMR_Info.objects.filter(
#             ro=ro, as_accepted=1, physical_status=1, uneco_status=0)
#         material = RO_Material_Info.objects.filter(ro_id=ro)
#         mo = material_offer.objects.filter(ro_id=ro)
#         return render(request, 'po/area_store/power_analyzer_inward_chg.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot})


    
#     elif (ro.store.Name=="Area Store Gwalior" or ro.store.Name=="Area Store Guna" or ro.store.Name=="Area Store Jabalpur" or ro.store.Name=="Area Store Ujjain" or 
# 	  ro.store.Name=="Area Store Chhindwara" or ro.store.Name=="Area Store Chhatarpur" or ro.store.Name=="Area Store Satna" 
# 	  or ro.store.Name=="Area Store Shahdol" or ro.store.Name=="Area Store Sagar" or ro.store.Name=="Area Store Dhar"
#           or ro.store.Name=="Area Store Indore" or ro.store.Name=="Area Store Barwaha" or ro.store.Name=="Area Store Mandsaur" or ro.store.Name=="Area Store Ratlam"):
        
                
#         if request.method == "POST":



#             ro=RO_Info.objects.get(id=id)
#             report=request.FILES['xmr_file1']
           
#             dt=date.today()
#             rt_data = Pa_report(rel=ro, power_report_flag=report,power_report_date=dt)
#             rt_data.save()



         
#             abc = request.POST.getlist('xmr_det')
#             for data in abc:
#                 test = RO_Material_XMR_Info.objects.get(id=data)
                
#                 remark=request.POST.get(test.xmr)
#                 test.pa_remark=remark
#                 test.pa_result_date=date.today()





#                 # if request.FILES:
#                 #     power_report1 = request.FILES['cc'+test.xmr]
#                 #     test.analyser_rprt = power_report1
#                 #     test.pa_report_flag = 1

#                 #     print("ttttttttttttttttttttttttttttttt",test)

#                 #     test.save()




#                 if test.new_design==1:
#                     no_load_loss=request.POST.get('aa'+test.xmr)
#                     test.pa_no_loss=no_load_loss

#                 max_load_loss=request.POST.get('bb'+test.xmr)
                
#                 test.pa_max_loss=max_load_loss
                
#                 test.pa_result_submitted = 1

                
                    
                
#                 if test.new_design == 1:
                    
#                     if test.material.rating=="25KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="25KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per
                        
#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()

                    
#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                            

                        
                        
#                     elif test.material.rating=="63KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="63KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per

#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()

#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                        
                        
#                     elif test.material.rating=="100KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="100KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per

#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()


#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                        

#                     elif test.material.rating=="200KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="200KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per

#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()

#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                        

#                 elif test.old_l1 == 1:
                    

#                     if test.material.rating=="25KVA":
#                         nd=power_analyser_level1.objects.get(rating="25KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()




#                     elif test.material.rating=="63KVA":
#                         nd=power_analyser_level1.objects.get(rating="63KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()


                        
#                     elif test.material.rating=="100KVA":
#                         nd=power_analyser_level1.objects.get(rating="100KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

                        
#                     elif test.material.rating=="200KVA":
#                         nd=power_analyser_level1.objects.get(rating="200KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()


#                 elif test.old_l2 == 1:
                    

#                     if test.material.rating=="25KVA":
#                         nd=power_analyser_level2.objects.get(rating="25KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

                        
#                     elif test.material.rating=="63KVA":
#                         nd=power_analyser_level2.objects.get(rating="63KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

                        

#                     elif test.material.rating=="100KVA":
#                         nd=power_analyser_level2.objects.get(rating="100KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()


#                     elif test.material.rating=="200KVA":
                        
#                         nd=power_analyser_level2.objects.get(rating="200KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

#                     test.save()





            
#             ro1 = RO_Info.objects.get(id=id)
       
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)

#             xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

#             xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        
#             count=0
#             for i in ro_mat:
#                 quant=i.quantity
#                 count=count+quant
#                 print(count)
#                 if count==xmr_re+xmr_ue:
#                 # i.forward_mat_to_cgm=1
#                 # i.save()
#                     rel=RO_Info.objects.get(id=id)
#                     rel.mrc_flag=1
#                     rel.save()
#                 else:
#                     rel=RO_Info.objects.get(id=id)
#                     rel.mrc_flag=0
#                     rel.save()

       
#             ro1 = RO_Info.objects.get(id=id) 
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        
       
#             for i in ro_mat:
#                 quant=i.quantity
#                 xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

          

#                 xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
            
            
#                 if quant==xmr_re+xmr_ue:
#                     i.forward_mat_to_cgm=1
#                     i.save()
#                     # rel=RO_Info.objects.get(id=id)
#                     # rel.mrc_flag=1
#                     # rel.save()

        

#             ro1 = RO_Info.objects.get(id=id)
       
#             rel_pa_quant=[]
#             rel_ue_quant=[]
#             rel_forward_cgm=[]
#             rel_mat_rating=[]
#             # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
#             # for p in ro_mat:
#             rel_mat_rating.append(ro1.id)
#             rel_forward_cgm.append(ro1.mrc_flag)

#             pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
#             ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
#             rel_pa_quant.append(pa)
#             rel_ue_quant.append(ue)

#             relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



#             ro1 = RO_Info.objects.get(id=id)
    
#             pa_quant=[]
#             ue_quant=[]
#             forward_cgm=[]
#             mat_rating=[]
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)
#             for p in ro_mat:
#                 mat_rating.append(p.rating)
#                 forward_cgm.append(p.forward_mat_to_cgm )

#                 pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
#                 ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
#                 pa_quant.append(pa)
#                 ue_quant.append(ue)

#             totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)






#             ro = RO_Info.objects.get(id=id)
#             xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro)
#             xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,as_accepted=1,physical_status=1)
#             material = RO_Material_Info.objects.filter(ro_id=ro)
#             mo = material_offer.objects.filter(ro_id=ro)
#             pa_rt=Pa_report.objects.filter(rel=ro)
#             return render(request, 'po/area_store/power_analyzer_inward_accepted_chg_2.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot,"aa":a,"bb":b,
#                 "pa_qt":pa_quant,"ue_qt":ue_quant,"mat_rt":mat_rating,"fd_cgm":forward_cgm,"tzip":totzip,"cc":c,"pa_report":pa_rt,"rzip":relzip})


#         ro = RO_Info.objects.get(id=id)
#         xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
#         xmr = RO_Material_XMR_Info.objects.filter(
#             ro=ro, as_accepted=1, physical_status=1, uneco_status=0)
#         material = RO_Material_Info.objects.filter(ro_id=ro)
#         mo = material_offer.objects.filter(ro_id=ro)
        
#         return render(request, 'po/area_store/power_analyzer_inward_accepted_chg_2.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot})







#     else:

#         if request.method == "POST":

         
#             abc = request.POST.getlist('xmr_det')
#             for data in abc:
#                 test = RO_Material_XMR_Info.objects.get(id=data)
                
#                 remark=request.POST.get(test.xmr)
#                 test.pa_remark=remark
#                 test.pa_result_date=date.today()


#                 if request.FILES:
#                     power_report1 = request.FILES['cc'+test.xmr]
#                     test.analyser_rprt = power_report1
#                     test.pa_report_flag = 1

                    

#                     test.save()




#                 if test.new_design==1:
#                     no_load_loss=request.POST.get('aa'+test.xmr)
#                     test.pa_no_loss=no_load_loss

#                 max_load_loss=request.POST.get('bb'+test.xmr)
                
#                 test.pa_max_loss=max_load_loss
                
#                 test.pa_result_submitted = 1

                
                    
                
#                 if test.new_design == 1:
                    
#                     if test.material.rating=="25KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="25KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per
                        
#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()

                    
#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                            

                        
                        
#                     elif test.material.rating=="63KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="63KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per

#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()

#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                        
                        
#                     elif test.material.rating=="100KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="100KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per

#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()


#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                        

#                     elif test.material.rating=="200KVA":
#                         nd=power_analyser_newdesign.objects.get(rating="200KVA")
#                         input_no_loss=float(test.pa_no_loss)
#                         def_no_loss=float(nd.no_load_redstrip)
#                         per=((input_no_loss-def_no_loss)/def_no_loss)*100
#                         test.pa_no_loss_per=per
#                         input_max_loss=float(test.pa_max_loss)
#                         def_max_loss=float(nd.max_load_loss)
#                         full_per=((input_max_loss-def_max_loss)/def_max_loss)*100
#                         test.pa_max_loss_per=full_per
#                         test.save()

#                         no_load_percent=test.pa_no_loss_per

#                         if no_load_percent < 0:
#                             test.pa_no_loss_per=0.0
#                             test.save()

#                         max_load_percent=test.pa_max_loss_per
                        

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()
                        
#                         elif max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()
                        

#                 elif test.old_l1 == 1:
                    

#                     if test.material.rating=="25KVA":
#                         nd=power_analyser_level1.objects.get(rating="25KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()




#                     elif test.material.rating=="63KVA":
#                         nd=power_analyser_level1.objects.get(rating="63KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()


                        
#                     elif test.material.rating=="100KVA":
#                         nd=power_analyser_level1.objects.get(rating="100KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

                        
#                     elif test.material.rating=="200KVA":
#                         nd=power_analyser_level1.objects.get(rating="200KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()


#                 elif test.old_l2 == 1:
                    

#                     if test.material.rating=="25KVA":
#                         nd=power_analyser_level2.objects.get(rating="25KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

                        
#                     elif test.material.rating=="63KVA":
#                         nd=power_analyser_level2.objects.get(rating="63KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

                        

#                     elif test.material.rating=="100KVA":
#                         nd=power_analyser_level2.objects.get(rating="100KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()


#                     elif test.material.rating=="200KVA":
                        
#                         nd=power_analyser_level2.objects.get(rating="200KVA")
#                         input = float(test.pa_max_loss)
#                         total_loss = float(nd.total_loss_100)
#                         per=((input-total_loss)/total_loss)*100
#                         test.pa_max_loss_per=per
#                         test.save()

#                         max_load_percent=test.pa_max_loss_per

#                         if max_load_percent <= 0.0:
#                             test.pa_max_loss_per=0.0
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent <= 15 and max_load_percent > 0.0:
#                             test.pa_result=1
#                             test.save()

#                         elif max_load_percent > 15:
#                             test.pa_result=-1
#                             test.save()

#                     test.save()





         

            
#             ro1 = RO_Info.objects.get(id=id)
       
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)

#             xmr_re= RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()  

#             xmr_ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
        
#             count=0
#             for i in ro_mat:
#                 quant=i.quantity
#                 count=count+quant
#                 print(count)
#                 if count==xmr_re+xmr_ue:
#                 # i.forward_mat_to_cgm=1
#                 # i.save()
#                     rel=RO_Info.objects.get(id=id)
#                     rel.mrc_flag=1
#                     rel.save()
#                 else:
#                     rel=RO_Info.objects.get(id=id)
#                     rel.mrc_flag=0
#                     rel.save()

       
#             ro1 = RO_Info.objects.get(id=id) 
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)

        
       
#             for i in ro_mat:
#                 quant=i.quantity
#                 xmr_re= RO_Material_XMR_Info.objects.filter(material=i, pa_result=1,physical_status =1,uneco_status=0).count()

          

#                 xmr_ue= RO_Material_XMR_Info.objects.filter(material=i, physical_status =1,uneco_status=1,pa_result=0).count()
            
            
#                 if quant==xmr_re+xmr_ue:
#                     i.forward_mat_to_cgm=1
#                     i.save()
#                     # rel=RO_Info.objects.get(id=id)
#                     # rel.mrc_flag=1
#                     # rel.save()

        

#             ro1 = RO_Info.objects.get(id=id)
       
#             rel_pa_quant=[]
#             rel_ue_quant=[]
#             rel_forward_cgm=[]
#             rel_mat_rating=[]
#             # ro_mat=RO_Material_Info.objects.filter(ro=ro1)
#             # for p in ro_mat:
#             rel_mat_rating.append(ro1.id)
#             rel_forward_cgm.append(ro1.mrc_flag)

#             pa=RO_Material_XMR_Info.objects.filter(ro=ro1, pa_result=1,physical_status =1,uneco_status=0).count()
#             ue= RO_Material_XMR_Info.objects.filter(ro=ro1, physical_status =1,uneco_status=1,pa_result=0).count()
#             rel_pa_quant.append(pa)
#             rel_ue_quant.append(ue)

#             relzip=zip(rel_mat_rating,rel_pa_quant,rel_ue_quant,rel_forward_cgm)



#             ro1 = RO_Info.objects.get(id=id)
    
#             pa_quant=[]
#             ue_quant=[]
#             forward_cgm=[]
#             mat_rating=[]
#             ro_mat=RO_Material_Info.objects.filter(ro=ro1)
#             for p in ro_mat:
#                 mat_rating.append(p.rating)
#                 forward_cgm.append(p.forward_mat_to_cgm )

#                 pa=RO_Material_XMR_Info.objects.filter(material=p, pa_result=1,physical_status =1,uneco_status=0).count()
#                 ue= RO_Material_XMR_Info.objects.filter(material=p, physical_status =1,uneco_status=1,pa_result=0).count()
#                 pa_quant.append(pa)
#                 ue_quant.append(ue)

#             totzip=zip(mat_rating,pa_quant,ue_quant,forward_cgm)



#             ro = RO_Info.objects.get(id=id)
#             xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro)
#             xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0,as_accepted=1,physical_status=1)
#             material = RO_Material_Info.objects.filter(ro_id=ro)
#             mo = material_offer.objects.filter(ro_id=ro)
#             return render(request, 'po/area_store/power_analyzer_inward_chg_normal.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot,"aa":a,"bb":b,"pa_qt":pa_quant,"ue_qt":ue_quant,"mat_rt":mat_rating,"fd_cgm":forward_cgm,"tzip":totzip,"cc":c,"rzip":relzip})


#         ro = RO_Info.objects.get(id=id)
#         xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro, as_accepted=1)
#         xmr = RO_Material_XMR_Info.objects.filter(
#             ro=ro, as_accepted=1, physical_status=1, uneco_status=0)
#         material = RO_Material_Info.objects.filter(ro_id=ro)
#         mo = material_offer.objects.filter(ro_id=ro)
#         return render(request, 'po/area_store/power_analyzer_inward_chg_normal.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo, "xmr_t": xmr_tot})






def rca_to_nabl_list(request):
    data = RO_Info.objects.all()
    return render(request,'po/area_store/rca_to_nabl_list.html',{'data': data})


def rca_to_nabl(request,id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro,physical_status=1,as_accepted=1)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro,issue_di=1) 
    var  = 0
    if not RcaProcurementInfo.objects.filter(TRF_Id=id).exists():
        return render(request,'po/area_store/rca_to_nabl.html',{'var':var, 'id':id , 'ro': ro,"xmr": xmr,"material": material,'mo':mo})
    else:
        var = 1
        return render(request,'po/area_store/rca_to_nabl.html',{'var':var, 'id':id , 'ro': ro,"xmr": xmr,"material": material,'mo':mo})


def test_request_form_rca(request, id):
    return render(request, 'po/test_request_form_rca.html', {'id':id})


def test_request_form_submit_rca(request, id):
    if request.method == "POST":
        customer_Organization_name = request.POST.get('customer_Organization_name')
        customer_Organization_address = request.POST.get('customer_Organization_address')
        contact_person_name = request.POST.get('contact_person_name')
        mobile_no = request.POST.get('mobile_no')
        email_id = request.POST.get('email_id')
        name_of_sample_product = request.POST.get('name_of_sample_product')
        customer_ref_gatepass_no = request.POST.get('customer_ref_gatepass_no')
        dated = request.POST.get('dated')
        sample_description_condition = request.POST.get('sample_description_condition')
        test_spec = request.POST.get('test_spec')
        drawings_catalogs_operating_manual = request.POST.get('drawings_catalogs_operating_manual')
        sample_identification_no = request.POST.get('sample_identification_no')
        decision_on_compliance = request.POST.get('decision_on_compliance')
        for_tolerance = request.POST.get('for_tolerance')
        mu_status = request.POST.get('mu_status')
        sign = request.POST.get('sign')
        test_name = request.POST.getlist('Test_name[]')

        trf_obj = Rcatrf_Details(TRF_Id=id, customer_Organization_name=customer_Organization_name, customer_Organization_address=customer_Organization_address,contact_person_name=contact_person_name,
                              mobile_no=mobile_no, email_id=email_id, name_of_sample_product=name_of_sample_product, customer_ref_gatepass_no=customer_ref_gatepass_no, dated=dated,
                              sample_description_condition=sample_description_condition, test_spec=test_spec, drawings_catalogs_operating_manual=drawings_catalogs_operating_manual,
                              sample_identification_no=sample_identification_no, decision_on_compliance=decision_on_compliance, for_tolerance=for_tolerance, mu_status=mu_status,
                              sign=sign)
        trf_obj.save()

        trf_id = Rcatrf_Details.objects.latest('TRF_Id')

        for data in test_name:
            test_details = Rca_TRF_Test_Details(TRF_Id=trf_id.TRF_Id,TRF_Test_Id=trf_id.TRF_Id, TRF_Test_Name=data)
            test_details.save()

        rca_obj = RcaProcurementInfo(TRF_Id=trf_id.TRF_Id, dispatch_for_nabl=1, test_request_form=1)
        rca_obj.save()
        
        return redirect('/po/rca_to_nabl/' + str(id))
    return render(request, 'po/area_store/test_request_form_submit.html')



# def RCA_di_issue_accept(request,id):
#      if request.method == "POST":
#         sched = request.POST.get("copy")
#         ro = RO_Info.objects.get(id=id)
#         ro_sched = RO_Copy(ro=ro, copy_name=sched)
#     data = material_offer.objects.get(id=id)
#     data.issue_di = 1
#     data.save()
#     ro = RO_Info.objects.get(id=id)
#     xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
#     material = RO_Material_Info.objects.filter(ro_id=ro)
#     mo=material_offer.objects.filter(id=id) 


def rca_cgm_all_work_order(request):
    # if request.method=="POST":
    #     digisigndoc=request.POST.get('digi_pdf')
    #     data3=WO_Info(digi_sign_doc=digisigndoc)
    #     data3.save()
    #     print("jjjjjjjjjjjjjjjjjjj",data3)

    
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    data = WO_Info.objects.filter(rca_cell=cell).order_by('-id')

    # download_pdf=WO_Info.objects.get(digi_flag=1)

    return render(request, 'po/area_store/rca_cgm_all_wo.html', {'data': data})
    
def rca_cgm_order_view(request, id):
    vd = WO_Info.objects.get(id=id)
    schedule = WO_Schedule_Info.objects.filter(schedule_id=vd)
    copy = WO_Copy_Info.objects.filter(wo=vd)
    today = date.today()
    # add = UserCompanyDataMain.objects.get(user_id=vd.vendor_id.ContactNo)
    return render(request, 'po/area_store/rca_cgm_order_view.html',
                  {'vd': vd, 'copy': copy, 'date': today, 'schedule': schedule})

def upload_digi(request, id):
    if request.method == "POST":
        upload_digi_doc = request.FILES['digi_pdf']
        # fs=FileSystemStorage()

        digipdf = WO_Info.objects.get(id=id)
        digipdf.digi_sign_doc = upload_digi_doc
        digipdf.digi_flag = 1

        # digipdf=WO_Info(digi_sign_doc=upload_digi_doc)
        digipdf.save()
        return render(request, 'po/area_store/upload_digi.html', {'digipdf': digipdf})
    digipdf = WO_Info.objects.get(id=id)
    return render(request, 'po/area_store/upload_digi.html', {'digipdf': digipdf})


def rca_cgm_all_release_order(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    info = RO_Info.objects.filter(rca_cell=cell).order_by('-id')
    # ro_m=RO_Material_Info.objects.all().order_by('-id')
    return render(request, 'po/area_store/rca_cgm_all_ro.html', {'data': info})
	
def rca_cgm_release_view(request, id):
    vd = RO_Info.objects.get(id=id)
    schedule = RO_Schedule_Info.objects.filter(ro_id=vd)
    schedule_ro = RO_Schedule_Info.objects.get(ro_id=vd)

    copy = RO_Copy.objects.filter(ro=vd)
    ro_m = RO_Material_Info.objects.filter(ro=vd)
    today = date.today()
    # add = UserCompanyDataMain.objects.get(user_id=vd.wo.vendor_id.ContactNo)
    return render(request, 'po/area_store/rca_cgm_release_view.html',
                  {'vd': vd, 'copy': copy, 'date': today, 'schedule': schedule, 'material': ro_m, 'schedule_ro': schedule_ro})

def upload_digi_ro(request, id):

   
    if request.method == "POST":

        upload_digi_doc_ro = request.FILES['digi_pdf_ro']

        

        digipdf_ro = RO_Info.objects.get(id=id)



        digipdf_ro.digi_sign_doc_ro = upload_digi_doc_ro
        digipdf_ro.digi_flag_ro = 1

        digipdf_ro.save()
       


       
    digipdf_ro = RO_Info.objects.get(id=id)
    return render(request, 'po/area_store/upload_digi_ro.html', {'digipdf_ro': digipdf_ro})


def delete(request, id, ro_id):
    # ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.get(id=id)
    xmr.delete()
    ro = RO_Info.objects.get(id=ro_id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro_id)
    material = RO_Material_Info.objects.filter(ro_id=ro_id)
    return render(request, 'po/area_store/create_rca_di1.html', {'ro': ro, "material": material, "xmr": xmr})    
    

def rca_di_view_accepted(request,id):
    if request.method == "POST":
        # abc = request.POST.getlist('xmr_det')
        # for data in abc:
        ro = RO_Info.objects.get(id=id)
        abc = request.POST.getlist('xmr_det')
        # data = RO_Material_XMR_Info.objects.get(id=ro)
        for data in abc:
            test = RO_Material_XMR_Info.objects.get(id=data)
            test.xmr_type_submitted = 1
            test.save()

        new = request.POST.getlist('options1')
        for data1 in new:
            test1 = RO_Material_XMR_Info.objects.get(id=data1)
            test1.new_design = 1
            test1.as_issue_mat = 1
            test1.as_issue_xmr_date=date.today() 
            test1.save()

        l2 = request.POST.getlist('options2') 
        for data2 in l2:
            test2 = RO_Material_XMR_Info.objects.get(id=data2)
            test2.old_l1 = 1
            test2.as_issue_mat = 1
            test2.as_issue_xmr_date=date.today() 
            test2.save()

        l3 = request.POST.getlist('options3')
        for data3 in l3:
            test3 = RO_Material_XMR_Info.objects.get(id=data3)
            test3.old_l2 = 1
            test3.as_issue_mat = 1
            test3.as_issue_xmr_date=date.today()  
            test3.save()


        l4 = request.POST.getlist('options4')
        for data4 in l4:
            test4 = RO_Material_XMR_Info.objects.get(id=data4)
            test4.design_non_star = 1
            test4.as_issue_mat = 1
            test4.as_issue_xmr_date=date.today() 
            test4.save()  

        # if request.POST.get("options1") == "new":
        #     data.new_design = 1
        #     data.xmr_type_submitted = 1
        #     data.as_issue_mat = 1
        # elif request.POST.get("options2") == "l1":
        #     data.old_l1 = 1
        #     data.xmr_type_submitted = 1
        #     data.as_issue_mat = 1
        # elif request.POST.get("options3") == "l2":
        #     data.old_l2 = 1
        #     data.xmr_type_submitted = 1
        #     data.as_issue_mat = 1      
        # data.save()

    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    gp_det = as_issue_gatepass.objects.filter(ro=ro)
    return render(request, 'po/area_store/rca_di_view.html',{'ro': ro, "material": material, "xmr": xmr,"gp":gp_det})    















    # ******************rohit

import datetime
from django import forms

from .forms import WorkForm,WorkFormData


def procurement_Generate_PO(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    discom = Discom_Master.objects.get(Discom_Code=officer.user_zone)
    region_discom = Region_Master.objects.get(Discom__Discom_Code=discom.Discom_Code, Region_Name_E=officer.Region )
    if request.method == "POST":
        vendor = User_Registration.objects.get(User_Id=int(request.POST.get('vendor')))
        if Purchase_Order.objects.filter(po_no=request.POST.get('po_no'), is_po_deleted = False).exists():
            po = Purchase_Order.objects.get(po_no=request.POST.get('po_no'), is_po_deleted = False)
            if po.is_po_deleted == False :
                messages = 'Purchase order is already created'
                return render(request, 'po/po_creater/creater_base.html', {'officer': officer, 'messages': messages})
            form = WorkForm()
            vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1)
            return render(request, 'po/po_creater/procurement_generate_po1.html',
                          {"officer": officer, 'vendor': vendor, 'po': po, 'form': form})
        po = Purchase_Order(vendor=vendor, region_discom=region_discom, discom=discom, zone=officer.user_zone, po_no=request.POST.get('po_no'),
                            po_prefix=request.POST.get('po_prefix'),
                            po_subject=request.POST.get('po_subject'),
                            erp_created_date=request.POST.get('date'), header=1, is_po_deleted = False,
                            header_created_by=officer.employ_name)
        po.save()
        po = Purchase_Order.objects.latest('id')
        form = WorkForm()
        vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1)
        return render(request, 'po/po_creater/procurement_generate_po1.html',
                      {"officer": officer, 'vendor': vendor, 'po': po, 'form': form})
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1)
    return render(request, 'po/po_creater/procurement_generate_po.html',
                  {"officer": officer, 'vendor': vendor})


def procurement_Generate_PO1(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    uom=UOM_Master.objects.filter(Status=1)
    if request.method == "POST":
        procurement = Purchase_Order.objects.get(id=id)
        uom=UOM_Master.objects.filter(Status=1)
        form = WorkForm(request.POST, instance=procurement)
        if form.is_valid():
            form.save()
        Item = Vendor_Material_Details.objects.filter(user_id=procurement.vendor.User_Id, Status = 1)
        vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
        Material = PO_Material.objects.filter(po=procurement)
        return render(request, 'po/po_creater/procurement_generate_po2.html',
                      {"officer": officer, 'vendor': vendor, 'po': procurement, 'Material': Material,'Item':Item, 'UOM':uom})
    po = Purchase_Order.objects.latest('id')
    form = WorkForm()
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    return render(request, 'po/po_creater/procurement_generate_po1.html',
                  {"officer": officer, 'vendor': vendor, 'po': po, 'form': form, 'UOM':uom})


def procurement_Generate_PO2(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    uom=UOM_Master.objects.filter(Status=1)
    if request.method == "POST":
        procurement = Purchase_Order.objects.get(id=id)
        code = Vendor_Material_Details.objects.get(Material_Specification=request.POST.get('specification'),user_id=procurement.vendor.User_Id)
        if procurement.zone == 'CZ':
            material_item_code = code.item_code
        elif procurement.zone == 'WZ':
            material_item_code = code.item_code_wz
        elif procurement.zone == 'EZ':
            material_item_code = code.item_code_ez
        Material = PO_Material(po=procurement, specification=request.POST.get('specification'), item_code = material_item_code,
                               unit=request.POST.get('unitOfMeasure'), Quantity=request.POST.get('quantity'),
                               Amount=request.POST.get('amount'), tax=request.POST.get('tax'),
                               total_amount=request.POST.get('total_amount'),remaining_qty = request.POST.get('quantity'))
        Material.save()
        Material = PO_Material.objects.filter(po=procurement)
        Item = Vendor_Material_Details.objects.filter(user_id=procurement.vendor.User_Id, Status = 1)
        vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
        return render(request, 'po/po_creater/procurement_generate_po2.html',
                      {"officer": officer, 'vendor': vendor, 'po': procurement, 'Material': Material,'Item':Item, 'UOM':uom})
    po = Purchase_Order.objects.get(id=id)
    schedule = PO_Schedule.objects.filter(po=po)
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    return render(request, 'po/po_creater/procurement_generate_po3.html',
                  {"officer": officer, 'vendor': vendor, 'po': po, 'schedule': schedule, 'UOM':uom})


def procurement_Generate_PO3(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        procurement = Purchase_Order.objects.get(id=id)
        schedule = PO_Schedule(po=procurement, schedule_name=request.POST.get('schedule_name'),
                               schedule_description=request.POST.get('schedule_description'))
        schedule.save()
        schedule = PO_Schedule.objects.filter(po=procurement)
        vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
        return render(request, 'po/po_creater/procurement_generate_po3.html',
                      {"officer": officer, 'vendor': vendor, 'po': procurement, 'schedule': schedule})
    po = Purchase_Order.objects.get(id=id)
    copy = PO_Copy.objects.filter(po=id)
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    return render(request, 'po/po_creater/procurement_generate_po4.html',
                  {"officer": officer, 'vendor': vendor, 'po': po, 'copy': copy})


def procurement_Generate_PO4(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        procurement = Purchase_Order.objects.get(id=id)
        copy = PO_Copy(po=procurement, copy=request.POST.get('copy_name'))
        copy.save()
        copy = PO_Copy.objects.filter(po=procurement)
        vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
        return render(request, 'po/po_creater/procurement_generate_po4.html',
                      {"officer": officer, 'vendor': vendor, 'po': procurement, 'copy': copy})
    po = Purchase_Order.objects.get(id=id)
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    return render(request, 'po/po_creater/procurement_generate_po4.html',
                  {"officer": officer, 'vendor': vendor, 'po': po})


def po_view(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = Purchase_Order.objects.get(id=id)
    po_discom = Discom_Master.objects.get(id = po.discom.id)
    sign = po_discom.Po_Main_Sign
    copy_sign = po_discom.Po_Copy_To_Sign
    p_name = po_discom.Discom_Short_Name
    if po.region_discom.region_discom_name == "MPPKVVCL, Ujjain" or po.region_discom.region_discom_name == "MPPKVVCL, Indore":
        po_region_discom = Region_Master.objects.get(id = po.region_discom.id)
        sign = po_region_discom.Po_Main_Sign
        copy_sign = po_region_discom.Po_Copy_To_Sign
        p_name = po_region_discom.region_discom_name

    if request.method == "POST":
        procurement = Purchase_Order.objects.get(id=id)
        copy = PO_Copy(po=procurement, copy=request.POST.get('copy_name'))
        copy.save()
        copy = PO_Copy.objects.filter(po=procurement)
        vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
        return render(request, 'po/po_creater/procurement_generate_po4.html',
                      {"officer": officer, 'vendor': vendor, 'po': procurement, 'copy': copy})
    po = Purchase_Order.objects.get(id=id)
    copy = PO_Copy.objects.filter(po=po)
    schedule = PO_Schedule.objects.filter(po=po)
    Material = PO_Material.objects.filter(po=po)
    company = UserCompanyDataMain.objects.get(user_id_id=po.vendor)
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    return render(request, 'po/po_creater/po_view.html',
                  {"officer": officer, 'vendor': vendor, 'po': po, 'company': company, 'copy': copy, 'sign':sign, 'copy_sign':copy_sign, 'p_name':p_name, 
                   'schedule': schedule, 'Material': Material})


def send_to_approval(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = Purchase_Order.objects.get(id=id)
    po.po_send_to_approval_status = 1
    po.po_send_to_approval_at = dtm.now().date()
    po.po_send_by_approval_by = officer.employ_name
    po.status = 1
    po.save()
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    data = Purchase_Order.objects.filter(zone=officer.user_zone, is_po_deleted = False).order_by("-id")
    return render(request, 'po/procurement_di_list.html',
                  {'data': data, "msg1":"Purchase order created and send for approval succeefully"})


# Approver Code by jeevan


def purchase_order(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = Purchase_Order.objects.filter(status=1,po_send_to_approval_status=1, zone=officer.user_zone, is_po_deleted = False).order_by("-id")
    sd = PO_SD.objects.filter(po_no=po)
    return render(request, 'po/po_approver/purchase_order.html',
                  {"officer": officer, 'po': po, 'sd':sd})


def approver_view_purchase_order(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = Purchase_Order.objects.get(id=id, is_po_deleted = False)
    po_discom = Discom_Master.objects.get(id = po.discom.id)
    sign = po_discom.Po_Main_Sign
    copy_sign = po_discom.Po_Copy_To_Sign
    p_name = po_discom.Discom_Short_Name
    if po.region_discom.region_discom_name == "MPPKVVCL, Ujjain" or po.region_discom.region_discom_name =="MPPKVVCL, Indore":
        po_region_discom = Region_Master.objects.get(id = po.region_discom.id)
        sign = po_region_discom.Po_Main_Sign
        copy_sign = po_region_discom.Po_Copy_To_Sign
        p_name = po_region_discom.region_discom_name
    copy = PO_Copy.objects.filter(po=po)
    schedule = PO_Schedule.objects.filter(po=po)
    Material = PO_Material.objects.filter(po=po)
    company = UserCompanyDataMain.objects.get(user_id_id=po.vendor)
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    return render(request, 'po/po_approver/po_view.html',
                  {"officer": officer, 'vendor': vendor, 'po': po, 'company': company, 'copy': copy, 'copy': copy, 'sign':sign, 'copy_sign':copy_sign, 'p_name':p_name,
                   'schedule': schedule, 'Material': Material})

#---------------------------------po soft delete by approver in PO----------------------------------------------------
def po_delete_approver(request, id):
    officer = Officer.objects.get(otp=request.session['otp'],employ_id = request.session['employ_id'])
    po = Purchase_Order.objects.get(id=id)
    po.is_po_deleted = True
    po.po_deleted_date = dtm.now().date()
    po.po_deleted_by = officer.employ_name
    po.save()
    return redirect('/po/purchase_order')
#-------------------------------------------------end---------------------------------------------------------------

def po_approved(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = Purchase_Order.objects.get(id=id)
    po.po_approved_status = 1
    po.po_approved_at = dtm.now().date()
    po.po_approved_by = officer.employ_name
    po.status = 1
    po.save()
    po = Purchase_Order.objects.filter(status=1, po_send_to_approval_status=1, zone=officer.user_zone, is_po_deleted = False).order_by("-id")
    return render(request, 'po/po_approver/purchase_order.html',
                  {"officer": officer, 'po': po})

#-----------------------------------------------Approver View po Documents-------------------------------------
def approver_view_po_details(request, id):
    data1 = Purchase_Order.objects.filter(id=id)
    for v in data1:
        if BankDetails.objects.filter(po_no=v).exists():
            bg = BankDetails.objects.select_related('po_no').get(po_no=v)
            for i in data1:
                if PO_SD.objects.filter(po_no=v).exists():
                    sd = PO_SD.objects.select_related('po_no').get(po_no=v)
                    return render(request, 'po/po_approver/vendor_po_details_view_approver.html', {"data": data1,'bg':bg,'sd':sd})
                else:
                    return render(request, 'po/po_approver/vendor_po_details_view_approver.html', {"data": data1,'bg':bg})
        else:
            return render(request, 'po/po_approver/vendor_po_details_view_approver.html', {"data": data1})
    return render(request, 'po/po_approver/vendor_po_details_view_approver.html', {'data1':data1})
#---------------------------------------------------end-------------------------------------------------------

def vendor_purchase_order(request):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(po_approved_status=1,zone = officer_data.user_zone).order_by("-id")
    return render(request, 'po/vendor_purchase_order_list.html', {"data": data})



def view_po_details(request, id):
    data1 = Purchase_Order.objects.filter(id=id)
    for v in data1:
        if BankDetails.objects.filter(po_no=v).exists():
            bg = BankDetails.objects.select_related('po_no').get(po_no=v)
            for i in data1:
                if PO_SD.objects.filter(po_no=v).exists():
                    sd = PO_SD.objects.select_related('po_no').get(po_no=v)
                    return render(request, 'po/vendor_po_details_view.html', {"data": data1,'bg':bg,'sd':sd})
                else:
                    return render(request, 'po/vendor_po_details_view.html', {"data": data1,'bg':bg})
        else:
            return render(request, 'po/vendor_po_details_view.html', {"data": data1})
    return render(request, 'po/vendor_po_details_view.html', {'data1':data1})
    
    
def po_upload_digital_copy(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        po = Purchase_Order.objects.get(id=id)
        #print('jjjjjjjjj',)
        po.Po_doc = request.FILES['digital']
        po.po_digital_upload_status = 1
        po.po_digital_upload_at = dtm.now().date()
        po.po_digital_upload_by = officer.employ_name
        po.save()
        po = Purchase_Order.objects.filter(status=1, po_send_to_approval_status=1, zone=officer.user_zone)
        return render(request, 'po/po_approver/purchase_order.html',
                      {"officer": officer, 'po': po})
    po = Purchase_Order.objects.get(id=id)
    return render(request, 'po/po_approver/po_digital_upload.html',
                  {"officer": officer, 'po': po})

#-----------------------------------------------------documents reject in PO--------------------------------------
def vendor_bank_details_rejected(request, po_id):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(id=po_id, zone = officer_data.user_zone)
    data.update(bank_details_approved=-1)
    data.update(bank_details=0)
    bd=BankDetails.objects.filter(po_no__id = data.id)
    bd.delete()
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone,is_po_deleted = False, po_approved_status = 1).order_by('-id')
    return render(request, 'po/bankdetails.html', {"data": data})
	
def vendor_gtp_rejected(request, po_id):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(id=po_id,zone = officer_data.user_zone)
    data.update(gtp_approved=-1)
    data.update(gtp_status=0)
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone,is_po_deleted = False, po_approved_status = 1).order_by('-id')
    return render(request, 'po/procurement_gtp_approval.html', {"data": data})

def vendor_bg_rejected(request, po_id):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    data = Purchase_Order.objects.filter(id=po_id,  zone = officer_data.user_zone)
    data.update(bg_approved=-1)
    data.update(bg_status=0)
    bg = PO_SD.objects.get(po_no__id = data.id)
    bg.delete()
    data = Purchase_Order.objects.filter(zone = officer_data.user_zone, is_po_deleted = False, po_approved_status = 1).order_by("-id")
    return render(request, 'po/po_creater/bankguarantee.html', {"data": data})
#------------------------------------------------------end-------------------------------------------------------------------------

#----------------------------------------delete function in po--------------------------------------
def material_delete(request, id, po_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    Material = PO_Material.objects.filter(id=id)
    Material.delete()
    uom=UOM_Master.objects.filter(Status=1)
    po = Purchase_Order.objects.get(id=po_id)
    schedule = PO_Schedule.objects.filter(po=po)
    Material = PO_Material.objects.filter(po=po)
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    Item = Vendor_Material_Details.objects.filter(user_id=po.vendor.User_Id, Status = 1)
    return render(request, 'po/po_creater/procurement_generate_po2.html',
                      {"officer": officer, 'vendor': vendor, 'po': po, 'Material': Material,'schedule': schedule,'Item':Item, 'UOM':uom})    


def po_delete(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = Purchase_Order.objects.get(id=id)
    copy = PO_Copy.objects.filter(po=po)
    for i in copy:
        i.delete()
    schedule = PO_Schedule.objects.filter(po=po)
    for j in schedule:
        j.delete()
    Material = PO_Material.objects.filter(po=po)
    Material.delete()
    po.delete()
    return redirect('/po/procurement_generate_po')

#--------------------------------------------------------end-------------------------------------------------


#######lokendra rejected dtr and gatepass


def rca_gatepass_order_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)    

    data=RO_Info.objects.filter(store=areastore.AreaStore.id,digi_flag_ro=1).order_by('-id')
    
    # data = RO_Info.objects.filter( digi_flag_ro=1).order_by("-id")
    return render(request, 'po/area_store/rca_gatepass_order_list.html', {'data': data})


def rca_as_gatepass_details(request,id):
    ro = RO_Info.objects.get(id=id)
    # xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, vendor_send=1)|Q(ro=ro,as_xmr_rej_resubmit=1)

    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,physical_status=-1) | Q(ro=ro,pa_result=-1) | Q(ro=ro, ph_reject_by_nabl=-1) | Q(ro=ro, machine_reject_by_nabl=-1) | Q(ro=ro, single_reject_by_nabl=-1) )
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    return render(request,'po/area_store/rca_gatepass_outward.html',{'ro': ro, "material": material, "xmr": xmr, 'mo': mo})


def rca_as_gatepass_add(request,id):
    if request.method == "POST":
        info=RO_Info.objects.get(id=id)
        gp_date = request.POST.get('gatepass_date')
        gp_num=request.POST.get('gatepass_no')
        gatekeep_name=request.POST.get('gk_name')
        veh_no=request.POST.get('vehicle_no')
        driv_name=request.POST.get('driver_name')
        driv_phone=request.POST.get('driver_phone')
        mater_rec_by=request.POST.get('mat_rece_by')
        quantity=request.POST.get('outward_qty')
        driver_aadh=request.FILES['driver_aadhar']

        data1 = rca_gatepass(gate_no=info, gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                            driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,
                            material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh)
        data1.save()

        ro = RO_Info.objects.get(id=id)

        xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,physical_status=-1) | Q(ro=ro,pa_result=-1)  | Q(ro=ro, ph_reject_by_nabl=-1) | Q(ro=ro, machine_reject_by_nabl=-1) | Q(ro=ro, single_reject_by_nabl=-1))
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)

        return render(request,'po/area_store/rca_gatepass_outward.html',{'ro': ro, "material": material, "xmr": xmr,'mo': mo})

    ro = RO_Info.objects.get(id=id)
   
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,physical_status=-1) | Q(ro=ro,pa_result=-1)  | Q(ro=ro, ph_reject_by_nabl=-1) | Q(ro=ro, machine_reject_by_nabl=-1) | Q(ro=ro, single_reject_by_nabl=-1))
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    return render(request,'po/area_store/rca_gatepass_outward.html',{'ro': ro, "material": material, "xmr": xmr, 'mo': mo})



def rca_as_rejected_dispatch(request, id):
    
    ro = RO_Info.objects.get(id=id)
    gp_det=rca_gatepass.objects.filter(gate_no=ro) 
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,physical_status=-1) | Q(ro=ro,pa_result=-1)  | Q(ro=ro, ph_reject_by_nabl=-1) | Q(ro=ro, machine_reject_by_nabl=-1) | Q(ro=ro, single_reject_by_nabl=-1))
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    return render(request, 'po/area_store/rca_as_rejected_dispatch.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"gp":gp_det})




def rca_as_rejected_dispatch_accept(request, id):
    if request.method == "POST":

        abc = request.POST.getlist('xmr_det')
        for data in abc:
            test = RO_Material_XMR_Info.objects.get(Q(id=data,physical_status=-1) | Q(id=data,pa_result=-1)  | Q(id=data, ph_reject_by_nabl=-1) | Q(id=data, machine_reject_by_nabl=-1) | Q(id=data, single_reject_by_nabl=-1))
            remarks=request.POST.get(test.xmr)
            test.xmr_rej_gp_remark=remarks
            test.xmr_rej_gp_flag=1
            test.xmr_rej_gp_submitted = 1
            test.xmr_rej_gp_date = date.today()
            ro=RO_Info.objects.get(id=id)
            gp_infos=rca_gatepass.objects.filter(gate_no=ro.id).last()
            test.gatepass_details=gp_infos
            test.vendor_send=0
            test.as_accepted=0
            test.save()

        ro = RO_Info.objects.get(id=ro.id)
        gp_det=rca_gatepass.objects.filter(gate_no=ro) 
        xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,physical_status=-1) | Q(ro=ro,pa_result=-1)  | Q(ro=ro, ph_reject_by_nabl=-1) | Q(ro=ro, machine_reject_by_nabl=-1) | Q(ro=ro, single_reject_by_nabl=-1))
        material = RO_Material_Info.objects.filter(ro_id=ro)
        mo = material_offer.objects.filter(ro_id=ro)
        return render(request, 'po/area_store/rca_as_rejected_dispatch.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"gp":gp_det})
            
    ro = RO_Info.objects.get(id=ro.id)
    gp_det=rca_gatepass.objects.filter(gate_no=ro) 
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,physical_status=-1) | Q(ro=ro,pa_result=-1)  | Q(ro=ro, ph_reject_by_nabl=-1) | Q(ro=ro, machine_reject_by_nabl=-1) | Q(ro=ro, single_reject_by_nabl=-1))
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    return render(request, 'po/area_store/rca_as_rejected_dispatch.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"gp":gp_det})
    

       
        
        
       


def rca_as_gen_gatepass(request,id):
    ro = RO_Info.objects.get(id=id)
    gp_det=rca_gatepass.objects.filter(gate_no=ro).last()
    xmr = RO_Material_XMR_Info.objects.filter(gatepass_details=gp_det,ro=ro,xmr_rej_gp_flag=1)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    return render(request,'po/area_store/gen_gatepass_updated.html', {'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"gp":gp_det})
    
    
#******************************************************************************************8

def po_creater_DI_list(request):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    offered_data = Purchase_Order.objects.filter(po_item_approved=True,zone =officer_data.user_zone ).order_by("-id")
    return render(request, 'po/po_creater/po_creater_DI_list.html', {"data": offered_data})



def create_dispatch_instruction(request,id):
    if request.session.has_key('id_list'):
        data = PO_Material_Offer.objects.filter(po = id,Offer = 1,is_di_created=False)
        po_data = Purchase_Order.objects.get(id = id)
        del request.session['id_list']
        return render(request, 'po/po_creater/po_creater_DI.html', {"data": data, "po_data": po_data})
    else:
        data = PO_Material_Offer.objects.filter(po = id,Offer = 1,is_di_created=False)
        po_data = Purchase_Order.objects.get(id = id)
        return render(request, 'po/po_creater/po_creater_DI.html', {"data": data, "po_data": po_data})



def po_approval_offered_material_view(request):
    data = PO_Material_Offer.objects.filter(Offer=0,status=0,is_di_created = False)
    return render(request, 'po/po_approver/material_offered_view.html', {"data": data})



def approver_offer_view(request, po_id,po_material_id):
    data = Purchase_Order.objects.filter(id=po_id)
    vd = PO_Material_Offer.objects.get(po_id=po_id, id = po_material_id)
    material_data = PO_Material.objects.get(id = vd.material.id)
    dispatch_info = PO_Material_Offer_Serial_No.objects.filter(offer=vd.id)
    return render(request, 'po/po_approver/approver_offer_detail_view.html', {"data": data[0],
                                                        "dispatch_info": dispatch_info, 'offer': vd, 'material_data': material_data})
 


def create_di_checked_material(request):
    
    if request.session.has_key('id_list'):
        id_list = request.session['id_list']
        data = PO_Material_Offer.objects.filter(id__in=id_list)
        po_data = Purchase_Order.objects.get(id=data[0].po.id)
   
        if request.method=="POST":
            id_list = request.POST.getlist('checkbox')
            data = PO_Material_Offer.objects.filter(id__in=id_list)
            po_data = Purchase_Order.objects.get(id=data[0].po.id)
        
            store_list = ["bhopal", "indore", "jabalpur","gwalior"]
            request.session['id_list'] = id_list
            return render(request, 'po/po_creater/create_di_form.html', {"data": data,"po_data":po_data,"store_list":store_list})
        return render(request, 'po/po_creater/create_di_form.html',{"data": data,"po_data":po_data})
    else:
        if request.method=="POST":
            id_list = request.POST.getlist('checkbox')
            data = PO_Material_Offer.objects.filter(id__in=id_list)
            po_data = Purchase_Order.objects.get(id=data[0].po.id)
        
            store_list = ["bhopal", "indore", "jabalpur","gwalior"]
            request.session['id_list'] = id_list
            return render(request, 'po/po_creater/create_di_form.html', {"data": data,"po_data":po_data,"store_list":store_list})
        return render(request, 'po/po_creater/create_di_form.html')



def create_di_areastores(request,offer_material_id,po_id,po_material_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po_id1 = Purchase_Order.objects.get(id=po_id)
    vd = PO_Material_Offer.objects.get(po_id=po_id, material_id = po_material_id,id=offer_material_id)
    # di_number = DI_Master.objects.get(po=po_id)
    offer_material_data = PO_Material_Offer.objects.get(id=offer_material_id)
    # offer_material_data.is_di_created = True
    # offer_material_data.save()
    area_store_list = Store_Info.objects.filter(Discom = officer.Discom)
    AreaStroeData = DI_Areastores.objects.filter(po=po_id1,offer_item_id =offer_material_id )
    requested_qty = request.POST.get('qty')

    if request.method=="POST":
        store = request.POST.get('store')
        # store_data_exist = DI_Areastores.objects.filter(areastore = store,po =po_id1,material_sample_code = offer_material_data.material.item_code)
        # if store_data_exist:
        #     return render(request, 'po/po_creater/create_di_for_areastores.html', {'po':po_id1,"offer_material_id":offer_material_id,"po_id":po_id,"po_material_id":po_material_id,
        # "offer_material_data": offer_material_data,"area_store_list":area_store_list,'AreaStroeData':AreaStroeData,'msg1':"You have already selected this area store"})

        qty_added= [float(requested_qty)]
        for j in AreaStroeData:
            a = j.deliverable_qty
            qty_added.append(float(a))
        already_added_qty = sum(qty_added)
        if float(already_added_qty) > float(offer_material_data.Offer_Quantity):
            return render(request, 'po/po_creater/create_di_for_areastores.html', {'po':po_id1,"offer_material_id":offer_material_id,"po_id":po_id,"po_material_id":po_material_id,
            "offer_material_data": offer_material_data,"area_store_list":area_store_list,'AreaStroeData':AreaStroeData,'msg1':"You can't add more quantity than offered quantity "})
        
        qun = request.POST.get('qty')
        store_ojb = DI_Areastores(po=po_id1,offer_item=vd,deliverable_qty=qun,areastore=store,zone = po_id1.zone,material_sample_code=vd.material.item_code)
        store_ojb.save()
        return redirect(f'/po/create_di_areastores/{offer_material_id}/{po_id}/{po_material_id}')
    else:
        return render(request, 'po/po_creater/create_di_for_areastores.html', {'po':po_id1,"offer_material_id":offer_material_id,"po_id":po_id,"po_material_id":po_material_id,
        "offer_material_data": offer_material_data,"area_store_list":area_store_list,'AreaStroeData':AreaStroeData})



def create_di_step(request,po_id):
    id_list = request.session['id_list']
    data1 = PO_Material_Offer.objects.filter(id__in=id_list)
    po_data1 = Purchase_Order.objects.get(id=data1[0].po.id)
    for i in data1:
        AreaStoreData = DI_Areastores.objects.filter(offer_item=i, po =po_data1)
        if AreaStoreData:  
            po_data= Purchase_Order.objects.get(id=po_id)
            form = WorkFormData()
            if request.method=="POST":
                if DI_Master.objects.filter(erp_di_number = request.POST.get('DI_no'), is_di_deleted = False).exists():
                    messages = 'DI is already created'
                    return render(request, 'po/po_creater/creater_base.html', {'messages': messages})
                subject = request.POST.get('di_subject')
                erp_di_no = request.POST.get('DI_no')
                di_prefix = request.POST.get('di_prefix')
                di_scheme_name = request.POST.get('di_scheme_name')
                di_scheme_code = request.POST.get('di_scheme_code')

                data = DI_Master(po=po_data,vendor = po_data.vendor,zone = po_data.zone,po_no = po_data.po_no,
                di_subject = subject, is_di_deleted = False, erp_di_number = erp_di_no,prefix = di_prefix, scheme_name=di_scheme_name, scheme_code=di_scheme_code,di_create_date=dtm.now().date())
                data.save()
                return render(request, 'po/po_creater/create_di_form2.html', {"po_data": po_data,"form":form,"erp_di_no":erp_di_no})
            AreaStroeData = DI_Areastores.objects.filter(po=po_data)
            user = User_Registration.objects.filter(User_Id=po_data.vendor.User_Id)
            address = UserCompanyDataMain.objects.get(user_id_id=user[0])
            return render(request, 'po/po_creater/create_di_form1.html', {"po_data": po_data,'address':address})
        else:
            return render(request, 'po/po_creater/create_di_form.html', {"data": data1,"po_data":po_data1,"message1":"Please select all Items areastores for delivery"})


import random
import math
def create_di_step1(request,po_id,erp_di_no):
    po_data= Purchase_Order.objects.get(id=po_id)
    po_discom = Discom_Master.objects.get(id = po_data.discom.id)
    sign = po_discom.Po_Main_Sign
    copy_sign = po_discom.Po_Copy_To_Sign
    p_name = po_discom.Discom_Short_Name
    if po_data.region_discom.region_discom_name == "MPPKVVCL, Ujjain" or po_data.region_discom.region_discom_name == "MPPKVVCL, Indore":
        po_region_discom = Region_Master.objects.get(id = po_data.region_discom.id)
        sign = po_region_discom.Po_Main_Sign
        copy_sign = po_region_discom.Po_Copy_To_Sign
        p_name = po_region_discom.region_discom_name
    user = User_Registration.objects.filter(User_Id=po_data.vendor.User_Id)
    address = UserCompanyDataMain.objects.get(user_id_id=user[0])
    date = dtm.now().date()
    copy = PO_Copy.objects.filter(po=po_data)

    def generate_erp_no():
        erp_no = ""
        digits = "0123456789"
        for i in range(6):
            erp_no += digits[math.floor(random.random() * 10)]
        return erp_no
    erp_number = generate_erp_no()

    def generate_di_no():
        di_no = ""
        digits = "0123456789"
        for i in range(6):
            di_no += digits[math.floor(random.random() * 10)]
        return di_no
    di_number = generate_di_no()

    if request.method=="POST":
        di_data = DI_Master.objects.filter(po=po_data,po_no=po_data.po_no)
        dm = DI_Master.objects.get(erp_di_number=erp_di_no,zone=po_data.zone)
        form = WorkFormData(request.POST, instance=di_data[0])
        if form['term_and_condition'].value() == None or form['term_and_condition'].value() == " ":
            return HttpResponse ("Plese fill terms and conditions")
        else:
            if form.is_valid():
                fm=form.cleaned_data['term_and_condition']
                di_data=DI_Master.objects.filter(erp_di_number=erp_di_no,zone=po_data.zone).update(term_and_condition=fm)
                di_data=DI_Master.objects.get(erp_di_number=erp_di_no,zone=po_data.zone)
                term_and_condition=di_data.term_and_condition
                # form.save()
            else:
                print("form is not valid")
            id_list = request.session['id_list']
            data1 = PO_Material_Offer.objects.filter(id__in=id_list)
            for i in data1:
                i.is_di_created = True
                i.di_master = dm
                i.save()    
            update_po_material_offer = PO_Material_Offer.objects.filter(po=po_data, id__in=id_list, Offer=1)
            di_update_data = DI_Master.objects.filter(po=po_data,erp_di_number=erp_di_no,zone=po_data.zone)
            AreaStroeData = DI_Areastores.objects.filter(po=po_data,offer_item__id__in = id_list)
            AreaStroeData.update(di_master=di_update_data[0])
            return render(request, 'po/po_creater/di_pdf.html', {'copy':copy,'user':user[0],'di_number':di_number,'erp_number':erp_number,'sign':sign, 'copy_sign':copy_sign, 'p_name':p_name,
                                                                 'date':date,'address':address,"po_data": po_data,"AreaStroeData":AreaStroeData ,
                                                                 "di_update_data":di_update_data[0], "update_po_material_offer":update_po_material_offer, 'term_and_condition':term_and_condition})
    

#-------------------------------------delete di at creator side in CPO--------------------------------------------------
def di_delete(request, id ):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    di = DI_Master.objects.get(id=id)
    offer = PO_Material_Offer.objects.filter(po=di.po, is_di_created = True, di_master_id=di.id)
    for j in offer:
        j.is_di_created = False
        j.di_master = None
        j.save()
    # offer.save()
    area = DI_Areastores.objects.filter(di_master_id=di.id, di_master__erp_di_number = di.erp_di_number)
    for i in area:
        i.delete()
    di.delete()
    return redirect('/po/po_creater_DI_list')
#-----------------------------------------------end--------------------------------------------

def send_to_approval_di(request, id, erp_di_no):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = DI_Master.objects.get(id=id, erp_di_number=erp_di_no)
    po.di_send_to_approval_status = 1
    po.di_send_by_approval_by = officer.employ_name
    po.status = 1
    po.save()
    vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
    return render(request, 'po/po_creater/procurement_generate_po.html',
                  {"officer": officer, 'vendor': vendor, "erp_di_no":erp_di_no})



def di_view_approver(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = DI_Master.objects.filter(status=1,di_send_to_approval_status=1,zone=officer.user_zone, is_di_deleted=False).order_by("-id")
    return render(request, 'po/po_approver/di_view.html',
                  {"officer": officer, 'po': po})


def di_approved(request, id, erp_di_no):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    po = DI_Master.objects.get(id=id)
    po.di_approved_status = 1
    po.di_approved_date = dtm.now().date()
    po.di_approved_by = officer.employ_name
    po.status = 1
    po.save()
    po = DI_Master.objects.filter(status=1,di_send_to_approval_status=1,zone=officer.user_zone, erp_di_number=erp_di_no, is_di_deleted=False).order_by("-id")
    print("iiiiiiiiiiiiiiii",po)
    return render(request, 'po/po_approver/di_view.html',
                  {"officer": officer, 'po': po, "erp_di_no": erp_di_no})




def approver_view_di(request, po_id, erp_di_no):
    di_update_data1 = DI_Master.objects.get(id=po_id)
    po_data= Purchase_Order.objects.get(id=di_update_data1.po.id)
    # print("ooooo",po_data)
    po_discom = Discom_Master.objects.get(id = po_data.discom.id)
    sign = po_discom.Po_Main_Sign
    copy_sign = po_discom.Po_Copy_To_Sign
    p_name = po_discom.Discom_Short_Name
    if po_data.region_discom.region_discom_name == "MPPKVVCL, Ujjain" or po_data.region_discom.region_discom_name == "MPPKVVCL, Indore":
        po_region_discom = Region_Master.objects.get(id = po_data.region_discom.id)
        sign = po_region_discom.Po_Main_Sign
        copy_sign = po_region_discom.Po_Copy_To_Sign
        p_name = po_region_discom.region_discom_name
    user = User_Registration.objects.filter(User_Id=po_data.vendor.User_Id)
    address = UserCompanyDataMain.objects.get(user_id_id=user[0])
    date = dtm.now().date()
    copy = PO_Copy.objects.filter(po=po_data)
    

    def generate_erp_no():
        erp_no = ""
        digits = "0123456789"
        for i in range(6):
            erp_no += digits[math.floor(random.random() * 10)]
        return erp_no
    erp_number = generate_erp_no()

    def generate_di_no():
        di_no = ""
        digits = "0123456789"
        for i in range(6):
            di_no += digits[math.floor(random.random() * 10)]
        return di_no
    di_number = generate_di_no()

    di_data = DI_Master.objects.get(id=po_id, erp_di_number=erp_di_no)
    di_update_data = DI_Master.objects.filter(id=po_id)
    update_po_material_offer = PO_Material_Offer.objects.filter(di_master=di_data)
    AreaStroeData = DI_Areastores.objects.filter(po=po_data, di_master__erp_di_number=erp_di_no)
    return render(request, 'po/po_approver/view_di_pdf.html', {'copy':copy,'user':user[0],'di_number':di_number,'erp_number':erp_number,'date':date, 'sign':sign, 'copy_sign':copy_sign, 'p_name':p_name,
                                                               'address':address,"po_data": po_data,"AreaStroeData":AreaStroeData ,"di_update_data":di_update_data[0],'erp_di_no' : erp_di_no,'update_po_material_offer':update_po_material_offer})


#---------------------------------di soft delete by approver in PO----------------------------------------------------
def di_delete_approver(request, di_id, erp_di_no):
    officer = Officer.objects.get(otp=request.session['otp'],employ_id = request.session['employ_id'])
    di_update_data1 = DI_Master.objects.get(id=di_id)
    po_data= Purchase_Order.objects.get(id=di_update_data1.po.id)
    di = DI_Master.objects.get(id = di_update_data1.id, erp_di_number = erp_di_no)
    offer = PO_Material_Offer.objects.filter(po=di.po, is_di_created = True, di_master_id=di.id)
    for j in offer:
        j.is_di_created = False
        j.di_master = None
        j.save()
    area = DI_Areastores.objects.filter(di_master_id=di.id, di_master__erp_di_number = di.erp_di_number)
    for i in area:
        i.delete()
    di.is_di_deleted = True
    di.di_deleted_date = dtm.now().date()
    di.di_deleted_by = officer.employ_name
    di.save()
    return redirect('/po/di_view_approver')
#----------------------------------------------end--------------------------------------------------------

def di_upload_digital_copy(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        po = DI_Master.objects.get(id=id)
        po.di_doc = request.FILES['digital']
        po.di_digital_upload_status = 1
        po.di_digital_upload_date = dtm.now().date()
        po.di_digital_upload_by = officer.employ_name
        po.save()
        po = DI_Master.objects.filter(status=1,di_send_to_approval_status=1,zone=officer.user_zone).order_by("-id")
        return render(request, 'po/po_approver/di_view.html',
                  {"officer": officer, 'po': po})
    po = DI_Master.objects.get(id=id)
    return render(request, 'po/po_approver/di_digital_upload.html',
                  {"officer": officer, 'po': po})



# def po_di_material_view(request,id):
    # if request.session.has_key('store'):
        # store_name = Store_Info.objects.get(id=request.session['store'])
        # material = PO_Material_Offer.objects.get(id=id)
        
        
        # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.item_name,Offer_status=1,po=material.po,area_store=store_name.Name)
        # print("yyyyyyyyyyyyyyyyy",serial)
        # return render(request, 'po/area_store/view_serial_number.html', {'data': serial,'dataid':id})
    # return redirect('/')



# def PoDiStatus(request,id):
    # if request.session.has_key('store'):
        # if request.method =="POST":

            # store_name = Store_Info.objects.get(id=request.session['store'])
            # di_master = DI_Areastores.objects.filter(delivered_status=True,areastore=store_name.Name)
            # material = PO_Material_Offer.objects.get(id=id)
            #di_area_status = DI_Areastores.objects.get(po=material)
            # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.item_name,Offer_status=1,po=material.po,area_store=store_name.Name)
            
            # list_all=[]
            # for data in serial:
    
                # pstatus = request.POST.get(f'{data.id}')
                # premark = request.POST.get(f'a{data.id}')
                # list_all.append(pstatus)
               
                # if pstatus == "-1":
                    # newdata = DI_Areastores.objects.filter(delivered_status=True,areastore=store_name.Name).last()
    
                    
                    # newdata.status = False
                    # newdata.p_varification = True
                    # newdata.save()


                # data.p_status=pstatus

                # data.remark=premark
                # data.save()
                
            # if ("-1" or "0") not in list_all:
                # newdata = DI_Areastores.objects.filter(delivered_status=True,areastore=store_name.Name).last()
                # newdata.send_to_gm=1
                # newdata.save()
                
            # return redirect('/po/po_di_view')
    # return redirect('/')

#-------------------------Multiple Areastore-----------------------------------------

def di_send_to_cgm(request,id):
    di_m_obj= DI_Master.objects.get(id=id)
    di_area= DI_Areastores.objects.filter(di_master=di_m_obj)

    lst=[]
    for i in di_area:
        if i.send_to_gm==2 and i.p_varification==True:
            lst.append(i)

    if len(di_area) == len(lst):
        di_m_obj.send_to_cgm = 1 
        di_m_obj.save() 
    else:
        return redirect('/po/po_di_view',{"mgs":'Other Areastore Verification is Pending'})
    return redirect('/po/po_di_view')


def di_send_to_gm(request,id):
    if request.session.has_key('store'):
        di_area = DI_Areastores.objects.get(id=id)
	
        # di_m_obj = DI_Master.objects.get(id = di_area.di_master.id)
        di_a_obj = DI_Areastores.objects.get(id = di_area.id)
        di_a_obj.p_varification=True
        di_a_obj.send_to_gm = 2
        di_a_obj.save()

        return redirect('/po/po_di_view')
    return redirect('/po/po_di_view')


def po_di_view(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])

        Areastores= DI_Areastores.objects.filter(delivered_status=True,status=True,areastore=store_name.Name).order_by("-id")

        return render(request, 'po/area_store/po_di_view.html', {'data': Areastores})
    return redirect('/')

def check_pending_areastore(request, id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_master = DI_Master.objects.get(id = id)
        area_store = DI_Areastores.objects.filter(di_master_id = id, delivered_status=True)

        return render(request, 'po/area_store/di_areastore_status.html', {'area':area_store, 'di':di_master})
    return redirect('/po/po_di_view')
#-----------------------------------------------------end----------------------------------------------------------------



# ************inward*******


        
 

# *************








# def po_di_material_view(request,id):
    # if request.session.has_key('store'):
        # store_name = Store_Info.objects.get(id=request.session['store'])
        # material = PO_Material_Offer.objects.get(id=id)
        # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.item_name,Offer_status=1,po=material.po,area_store=store_name.Name)
        # return render(request, 'po/area_store/view_serial_number.html', {'data': serial,'dataid':id})
    # return redirect('/')


def po_di_material_view(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        serial = DI_Material_Offer_Serial_No.objects.filter(material=material.offer_item.item_name,Offer_status=1,po=material.po,area_store=store_name.Name,received_material=2)
        return render(request, 'po/area_store/view_serial_number.html', {'data': serial,'dataid':id, 'material':material})
    return redirect('/')




# def PoDiStatus(request,id):
    # if request.session.has_key('store'):
        # if request.method =="POST":

            # store_name = Store_Info.objects.get(id=request.session['store'])
            # di_master = DI_Areastores.objects.filter(delivered_status=True,areastore=store_name.Name)
            # material = PO_Material_Offer.objects.get(id=id)

            #di_area_status = DI_Areastores.objects.get(po=material)
            # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.item_name,Offer_status=1,po=material.po,area_store=store_name.Name)
            # list_all=[]
            
            # drr_date = request.POST.get('drr_date')
            # challan_no=request.POST.get('challan_no')
            # challan_date=request.POST.get('challan_date')
            # vehicle=request.POST.get('vehicle')
            # quantity=request.POST.get('quantity')

            # data1 = po_drr_info(area_store=di_master[0], drr_date=drr_date, drr_vehicle=vehicle,drr_challan_no=challan_no,
                                # drr_challan_date=challan_date,drr_quantity=quantity)
            # data1.save()
            # for data in serial:
    
                # pstatus = request.POST.get(f'{data.id}')
                # premark = request.POST.get(f'a{data.id}')
                # list_all.append(pstatus)
               
                # if pstatus == "-1":
                    # newdata = DI_Areastores.objects.get(delivered_status=True,areastore=store_name.Name)
    
                    
                    # newdata.status = False
                    # newdata.p_varification = True
                    # newdata.save()
            


                # data.p_status=pstatus

                # data.remark=premark
                # data.save()
                
            # if ("-1" or "0") not in list_all:
                # newdata = DI_Areastores.objects.get(delivered_status=True,areastore=store_name.Name)
                # newdata.send_to_gm=1
                # newdata.save()
                
            # return redirect('/po/po_di_view')
    # return redirect('/')



def PoDiStatus(request,id,erp_di_no):
    if request.session.has_key('store'):
        if request.method =="POST":

            store_name = Store_Info.objects.get(id=request.session['store'])
            # di_master = DI_Areastores.objects.filter(delivered_status=True,areastore=store_name.Name)
            # material = PO_Material_Offer.objects.get(id=id)

            material = DI_Areastores.objects.get(id =id)
            serial = DI_Material_Offer_Serial_No.objects.filter(area_store_id__di_master__erp_di_number=erp_di_no,area_store_id_id=material.id,Offer_status=1,po=material.po,area_store=store_name.Name)
            list_all=[]
            
            drr_date = request.POST.get('drr_date')
            challan_no=request.POST.get('challan_no')
            challan_date=request.POST.get('challan_date')
            vehicle=request.POST.get('vehicle')
            quantity=request.POST.get('quantity')

            data1 = po_drr_info(area_store=material, drr_date=drr_date, drr_vehicle=vehicle,drr_challan_no=challan_no,
                                drr_challan_date=challan_date,drr_quantity=quantity)
            data1.save()
            for data in serial:
                # value = DI_Material_Offer_Serial_No.objects.get(id=data.id)
                pstatus = request.POST.get(f'{data.id}')
                premark = request.POST.get(f'a{data.id}')
                list_all.append(pstatus)
                if pstatus == "-1":
                    newdata = DI_Areastores.objects.get(id=id)                
                    newdata.status = False
                    newdata.p_varification = True
                    newdata.save()
                    data.p_status= -1
                    data.received_material = -1
                    data.remark=premark
                    data.save()
            

                elif pstatus == None:
                    data.received_material = data.received_material
                    data.p_status = data.p_status
                    data.remark = data.remark
                    data.save()
                    list_all[-1] = str(data.p_status)

                elif pstatus == "1":
                    data.p_status = 1
                    data.received_material = 1
                    data.remark=premark
                    data.save()
                print("aaall",list_all)

            if ("0") not in list_all and ("-1") not in list_all:
                newdata = DI_Areastores.objects.get(id=id)
                newdata.send_to_gm=1
                newdata.status=True
                newdata.save()
            

            return redirect('/po/po_di_view')
    return redirect('/')


# def di_send_to_cgm(request,id):
#     if request.session.has_key('store'):
#         di_master = DI_Areastores.objects.get(id=id)
#         di_master.send_to_gm=2
#         di_master.save()

#         # print("di_master",di_master)
#         return redirect('/po/po_di_view')
#     return redirect('/')

#----------------------------------------------end----------------------------------------------------

#--------------------------------check di status at LAS--------------------------------------------------
def nabl_check_di_status(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_area = DI_Areastores.objects.filter(send_to_gm=2, p_varification =True, areastore=store_name.Name)
        for i in di_area:
            mrc = purchase_mrc_details.objects.filter(ro_id=i.id, digi_flag_pr=1)
        return render(request, 'po/area_store/nabl_check_di_status.html', {'data': di_area, 'mrc':mrc})
    return redirect('/')

#-------------------------------------------Physically Reject at LAS---------------------------------------------------
def reject_di(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_master = DI_Areastores.objects.filter(delivered_status=True,areastore=store_name.Name,status=False,p_varification=True)
        return render(request, 'po/area_store/reject_di.html', {'data': di_master})
    return redirect('/')

def reject_di_material_view(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        serial = DI_Material_Offer_Serial_No.objects.filter(p_status=-1, Offer_status=1, area_store_id_id=material.id, area_store=store_name.Name)
        #serial = DI_Material_Offer_Serial_No.objects.filter(accepted=2,material=material.offer_item.item_name,Offer_status=1,po=material.po,area_store=store_name.Name)
        return render(request, 'po/area_store/reject_di_material_view.html', {'data': serial,'dataid':id, 'material':material})
    return redirect('/')


def create_po_gatepass(request,id,erp_di_no):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id__di_master__erp_di_number=erp_di_no,area_store_id_id=material.id,p_status='-1',area_store=store_name.Name)
        #reject_item = DI_Material_Offer_Serial_No.objects.filter(accepted=2,p_status='-1',area_store=store_name.Name)
        if request.method == "POST":
            gp_date = request.POST.get('gatepass_date')
            gp_num=request.POST.get('gatepass_no')
            gatekeep_name=request.POST.get('gk_name')
            veh_no=request.POST.get('vehicle_no')
            driv_name=request.POST.get('driver_name')
            driv_phone=request.POST.get('driver_phone')
            mater_rec_by=request.POST.get('mat_rece_by')
            quantity=request.POST.get('outward_qty')
            driver_aadh=request.FILES['driver_aadhar']

            data1 = po_gatepass(area_store=material, gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,aname = store_name.Name,
                                material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh)
            data1.save()
            material.gatepass = 1
            material.save()
            for i in reject_item:
                i.accepted = 1
                i.save()

            return render(request, 'po/area_store/po_gatepass_outward_print.html', {'data': material,'material':reject_item,'data1':data1})
        
        return render(request, 'po/area_store/po_gatepass_outward.html', {'data': material,'material':reject_item})
    return redirect('/')
#-----------------------------------------------------------end-------------------------------------------------------------------

#-------------------------------------drr and gatepass details-----------------------------------------------------------------------
def gatepass(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_master = po_gatepass.objects.filter(aname = store_name.Name)
        return render(request, 'po/area_store/gatepass_history.html', {'data': di_master})
    return redirect('/')


def gatepass_history(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        data1 = po_gatepass.objects.get(id=id)
        reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id__di_master=data1.area_store.di_master.id,p_status='-1',area_store=store_name.Name)
        return render(request, 'po/area_store/po_gatepass_outward_print_new.html', {'data1': data1, 'item':reject_item})
    return redirect('/')

def po_receiving_material(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        drr_info = po_drr_info.objects.filter(area_store__areastore=store_name.Name).order_by('-id')
        return render(request, 'po/area_store/po_drr_info_history.html', {'data': drr_info})
    return redirect('/')

def drr_info_history(request, id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        drr = po_drr_info.objects.get(id=id)
        data = po_drr_info.objects.filter(id=drr.id, area_store_id=drr.area_store.id,area_store__areastore=store_name.Name)
        # drr_view = DI_Material_Offer_Serial_No.objects.filter(p_status='1',area_store=store_name.Name)
        return render(request, 'po/area_store/po_drr_info_history_view.html', {'info':data})
    return redirect('/')
#--------------------------------------------------end-----------------------------------------------------
    
#--------------------------------- po NABL Approved Items-------------------------------------------------

def nabl_approved_di_items(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_master = DI_Areastores.objects.filter(samp_accepted_flag=1,send_to_gm=2, areastore=store_name.Name)
        print("di_master.......", di_master)
        return render(request, 'po/area_store/nabl_approve_di.html', {'data': di_master})
    return redirect('/')

def nabl_approve_di_material_view(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        # reject_serial = sample_code_table_cp.objects.filter(phy_rejected=-1, area_store_id_id=material.id, area_store=store_name.Name)
        approve_serial = sample_code_table_cp.objects.filter(phy_accepted=1,di_area_store__samp_accepted_flag=1,di_area_store=material.id,di_area_store__areastore=store_name.Name)
        # approve_serial = DI_Material_Offer_Serial_No.objects.filter(area_store_id__samp_accepted_flag=1,area_store_id=material.id, material=material.offer_item.item_name , area_store=store_name.Name)
        return render(request, 'po/area_store/po_nabl_approve_di_material_view.html', {'data': approve_serial,'dataid':id, 'material':material})
    return redirect('/')
#-------------------------------------end--------------------------------------------------------------------------

#---------------------------------------------------PO NABL REJECTED------------------------------------------------
def nabl_reject_di(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_master = DI_Areastores.objects.filter(samp_rejected_flag=1,send_to_gm=2, areastore=store_name.Name)
        return render(request, 'po/area_store/nabl_reject_di.html', {'data': di_master})
    return redirect('/')

def nabl_reject_di_material_view(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        reject_serial = sample_code_table_cp.objects.filter(phy_rejected=1,di_area_store__samp_rejected_flag=1,di_area_store=material.id,di_area_store__areastore=store_name.Name)
        # reject_serial = DI_Material_Offer_Serial_No.objects.filter(area_store_id__samp_rejected_flag=1,area_store_id=material.id, material=material.offer_item.item_name , area_store=store_name.Name)
        return render(request, 'po/area_store/nabl_reject_di_material_view.html', {'data': reject_serial,'dataid':id, 'material':material})
    return redirect('/')

def create_nabl_reject_di_gatepass(request,id,erp_di_no):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id__di_master__erp_di_number=erp_di_no,area_store_id=material.id,area_store_id__samp_rejected_flag=1,area_store=store_name.Name)
        if request.method == "POST":
            gp_date = request.POST.get('gatepass_date')
            gp_num=request.POST.get('gatepass_no')
            gatekeep_name=request.POST.get('gk_name')
            veh_no=request.POST.get('vehicle_no')
            driv_name=request.POST.get('driver_name')
            driv_phone=request.POST.get('driver_phone')
            mater_rec_by=request.POST.get('mat_rece_by')
            quantity=request.POST.get('outward_qty')
            driver_aadh=request.FILES['driver_aadhar']

            data1 = DI_nabl_rejected_gatepass(area_store=material, gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,gatepass_flag=1,aname = store_name.Name,
                                material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh)
            data1.save()

            material.gatepass = 2
            material.save()

            offer_material= PO_Material_Offer.objects.get(po_id=material.po.id, material=material.offer_item.material, di_master_id= material.di_master.id)
            # offer_material.status= -2
            # offer_material.save()

            offer_serial_no=PO_Material_Offer_Serial_No.objects.filter(offer=offer_material.id)
            for k in offer_serial_no:
                k.status=-1
                k.save()
            
            update_material=PO_Material.objects.get(po_id=material.po.id, item_code = material.material_sample_code, specification=material.offer_item.item_name)
            update_material.remaining_qty = (float(update_material.remaining_qty) + float(material.deliverable_qty))
            update_material.dispatch_qty= (float(update_material.dispatch_qty) - float(material.deliverable_qty))
            if update_material.remaining_qty != 0:
                update_material.Offer=0
            update_material.save()
        

            po_exist_offer_data = PO_Material_Offer.objects.filter(po=material.po, material=material.offer_item.material , item_code = material.offer_item.item_code, status=1).order_by('id')
            if len(po_exist_offer_data)>=1:
                i = po_exist_offer_data.last()
                i.remaining_qty = update_material.remaining_qty
                i.dispatch_qty = update_material.dispatch_qty
                i.save()

            for i in reject_item:
                i.nabl_reject_status = True
                i.save()

            return render(request, 'po/area_store/nabl_rejected_gatepass_outward_print.html', {'data': material,'material':reject_item,'data1':data1})
        
        return render(request, 'po/area_store/nabl_rejected_gatepass_outward.html', {'data': material,'material':reject_item})
    return redirect('/')



def rejected_di_send_to_Vendor(request, id):
    di_m_obj= DI_Master.objects.get(id=id)
    di_area= DI_Areastores.objects.filter(di_master=di_m_obj)
    offer_material= PO_Material_Offer.objects.get(di_master__id=id)
    lst=[]
    for i in di_area:
        if i.gatepass==2 and i.samp_rejected_flag==1:
            lst.append(i)
    if len(di_area) == len(lst):
        di_m_obj.nabl_status = -1 
        di_m_obj.save()
        offer_material.status= -2
        offer_material.save()
    else:
        return redirect('/po/nabl_reject_di')
    return redirect('/po/nabl_reject_di')
#----------------------------------------------------end---------------------------------------------

# =========================    PO sampling Anil   =================================

import random
import math
def sample_select(request,id):
    if request.session.has_key('employ_login_id'):
        emp_id = request.session['employ_login_id']
        area = Officer.objects.get(employ_login_id=emp_id)
        zone=area.user_zone
        di_as_obj = DI_Areastores.objects.get(id=id,zone=zone)
        # di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id=di_as_obj)
        
        di_master_obj = DI_Master.objects.get(id = di_as_obj.di_master.id)
        
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        
        di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids)
        
        print("di_mosn_obj==========di_mosn_obj===========di_mosn_obj",di_mosn_obj)
        
        a = di_mosn_obj.count()
        
        area_store = []
        s_no = []
        
        for i in di_mosn_obj :
            a = i.area_store
            b = i.serial_no
            area_store.append(a)
            s_no.append(b)
            
        
        s = area_store.count('Area Store Bhopal')        
        if s < 2:
            pass

        mat_name = di_as_obj.offer_item.material.specification
        
        user_id = di_as_obj.po.vendor.User_Id #
        
        item_code = di_as_obj.material_sample_code
                
        
        lst_serial_number = []
        
        offer_qty =  di_as_obj.offer_item.total_quantity
        di_qty =  di_as_obj.offer_item.dispatch_qty
        for i in di_mosn_obj:
            lst_serial_number.append(i.serial_no)

        sample_percent = 0
        sample_unit = 0
        flag = -1

        ps_obj = product_sampling.objects.filter(Q(item_code = item_code) | Q(item_code_ez = item_code) | Q(item_code_wz = item_code))
                    
        
        for i in ps_obj:
            sample_type = i.sampling.sample_type
            if sample_type == 0:
                flag = 0
                lot_size_min = i.sampling.lot_size_min
                lot_size_max = i.sampling.lot_size_max
                if di_qty >= lot_size_min and di_qty <= lot_size_max:
                    sample_unit = i.sampling.sample_unit
                else:
                    pass
            elif sample_type == 1:
                sample_percent = i.sampling.sample_percentage
                flag = 1
        final_random_sample_mat = ""
        
        
        if flag == 0:
            random.shuffle(lst_serial_number)
            final_random_sample_mat = lst_serial_number[:sample_unit]
            
            
        elif flag == 1:            
            length_serial_number =  len(lst_serial_number)
            random_mat_round_number = math.ceil((length_serial_number * sample_percent ) / 100)
            random.shuffle(lst_serial_number)
            final_random_sample_mat = lst_serial_number[:random_mat_round_number]
                    
        
        area_name = []
        
        
        for i in di_mosn_obj:
            if i.serial_no in final_random_sample_mat:
                area_name.append(i.area_store)
                
        final_zip =  zip(final_random_sample_mat, di_mosn_obj, area_name)
        return render(request, 'officer/po_forward_nabl.html', {'data1': di_as_obj,'final_zip':final_zip, 'Di_id':id, 'final_random_sample_mat':final_random_sample_mat})

    return redirect('/')


def sample_select_submit(request,id, final_random_sample_mat):
    emp_id = request.session['employ_login_id']
    area = Officer.objects.get(employ_login_id=emp_id)
    zone = area.user_zone
    di_obj = DI_Areastores.objects.get(id=id,zone=zone)
    s = final_random_sample_mat[2:-2]
    ss = s.split("', '")
    for i in ss:        
        di_master_obj = DI_Master.objects.get(id = di_obj.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        obj = DI_Material_Offer_Serial_No.objects.filter(serial_no=i.strip(),area_store_id__in=di_area_master_ids)
        
        for j in obj:
            j.as_accepted=1
            j.save()
            
    for i in di_area_master:
        i.sampling_flag = 1
        i.save()
    
    return redirect('/po/po_sample_list')

def select_testing_nabl(request,id):
    if request.session.has_key('employ_login_id'):
        material = DI_Areastores.objects.get(id=id)
        zone = material.zone
        item_code = material.material_sample_code
        
        
        di_master_obj = DI_Master.objects.get(id = material.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
    
        
        di_area_master_ids = [obj.id for obj in di_area_master]
              
                
        di_mo_data = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,as_accepted=1)
             
        nabl = NABL_Registration_Test.objects.filter(Material_Item_Code = item_code).only('user_id')
        
        nabl2 = NABL_Registration_Test.objects.filter(Material_Item_Code = item_code).values('user_id').distinct('user_id')

        lst_nabl = []
        for k in nabl2:
            print(k['user_id'],"2222222222")
            try:
                user = User_Registration.objects.get(User_Id = k['user_id'])
                
                lst_nabl.append(user.CompanyName_E)
            except Exception as e:
                pass 
        
        if request.method == "POST":
            nabl_name = request.POST.get('nabl')
            nabl_number = User_Registration.objects.filter(CompanyName_E=request.POST.get('nabl')).earliest('CompanyName_E')
            
            for i in di_area_master:
                i.nabl_name = nabl_name
                i.nabl_status = 1
                i.nabl_number = nabl_number.ContactNo
                i.save()
            di_master_obj.nabl_number = nabl_number.ContactNo
            di_master_obj.nabl_name = request.POST.get('nabl')
            di_master_obj.save()
            return redirect('/po/po_sample_list')
        return render(request, 'officer/select_testing_nabl.html', {'data': material,'nabl':lst_nabl,"di_mo_data":di_mo_data})
    return redirect('/')
  



def view_sampled_material(request,id):
    if request.session.has_key('employ_login_id'):
        material = DI_Areastores.objects.get(id=id)
        lst_as = []
        item_code = []
        serial_no = []        
        
        di_master_obj = DI_Master.objects.get(id = material.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids, as_accepted=1)
        
        for j in di_mosn_obj:
            serial_no.append(j.serial_no)
            item_code.append(j.area_store_id.material_sample_code)
        return render(request, 'officer/view_sampled_material.html', {'di_mosn_obj':di_mosn_obj})
    return redirect('/')


def po_sample_list(request):
    if request.session.has_key('employ_login_id'):
        emp_id = request.session['employ_login_id']
        area = Officer.objects.get(employ_login_id=emp_id)       
        zone=area.user_zone
        di_as_obj = DI_Areastores.objects.filter(di_master__send_to_cgm=1,zone=zone).distinct('di_master')
        return render(request, 'officer/nabl_order.html', {'data1': di_as_obj})

    return redirect('/')

def po_pending_sample_list(request):
    if request.session.has_key('employ_login_id'):
        emp_id = request.session['employ_login_id']
        area = Officer.objects.get(employ_login_id=emp_id)       
        zone=area.user_zone
        di_as_obj = DI_Areastores.objects.filter(di_master__send_to_cgm=1,zone=zone,sampling_flag = 0).order_by('di_master', 'id').distinct('di_master')
        # di_as_obj=di_as_obj.order_by('-id')
        # print("di_obj",di_as_obj)       

        return render(request, 'officer/nabl_order.html', {'data1': di_as_obj})
    return redirect('/')


def po_logout(request):
    request.session.flush()
    return redirect('/')


def po_trf_create(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_as_obj = DI_Areastores.objects.filter(Q(di_master__send_to_cgm = 1,areastore=store_name.Name, nabl_status=1) & (Q(sampling_flag = 1) | Q(sampling_flag = 2))).order_by("-id")
        test_item_code = product_sampling.objects.filter(item_code = "M-0502029")
        print("test_item_code=============test_item_code============test_item_code:::::::::",test_item_code)
        return render(request, 'po/area_store/po_trf_details.html', {'data1': di_as_obj})

def po_nabl_result(request):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        di_as_obj = DI_Areastores.objects.filter(di_master__send_to_cgm = 1,areastore=store_name.Name, nabl_status=1,sampling_flag = 1).order_by("-id")
        return render(request, 'po/area_store/po_nabl_sample_result.html', {'data1': di_as_obj})

    return redirect('/')

def po_nabl_items_result(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        
        material = DI_Areastores.objects.get(id=id)
    
        gatepass_obj = po_nabl_gatepass.objects.get(area_store = material)
  
        sample_obj_2 = sample_code_table_cp.objects.filter(Gatepass = gatepass_obj)
            
        sample_obj = sample_code_table_cp.objects.filter(Gatepass = gatepass_obj,outward_generated=1)     
                
        return render(request, 'po/area_store/po_nabl_items_result.html',{'name':sample_obj})

    return redirect('/')
    
def po_di_sampled_item(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        
        di_master_obj = DI_Master.objects.get(id = material.di_master.id)
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        di_area_master_ids = [obj.id for obj in di_area_master]
        serial = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,area_store=store_name.Name,as_accepted=1)
        return render(request, 'po/area_store/view_sampled_item.html', {'data': serial,'dataid':id})
    return redirect('/')


def po_nabl_gatepass_details(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        
        di_master_obj = DI_Master.objects.get(id = material.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        
        # print("di_mosn_obj============di_mosn_obj====di_mosn_obj",di_mosn_obj)
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        
        # di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids, as_accepted=1)
        
        reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,area_store=store_name.Name,as_accepted=1)
        
        outward_qty = reject_item.count()
        
        if request.method == "POST":
            gp_date = request.POST.get('gatepass_date')
            gp_num=request.POST.get('gatepass_no')
            gatekeep_name=request.POST.get('gk_name')
            veh_no=request.POST.get('vehicle_no')
            driv_name=request.POST.get('driver_name')
            driv_phone=request.POST.get('driver_phone')
            mater_rec_by=request.POST.get('mat_rece_by')
            quantity=request.POST.get('outward_qty')
            driver_aadh=request.FILES['driver_aadhar']

            data1 = po_nabl_gatepass(area_store=material, gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,aname = store_name.Name,
                                material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh,nabl_name = material.nabl_name,nabl_number = material.nabl_number)
            data1.save()
            
            for i in di_area_master:
                i.nabl_gatepass = 1
                i.save()            
            
            for i in reject_item:
                i.accepted = 1
                i.save()
                
            data2 = po_nabl_gatepass.objects.filter(area_store=material).values('id')
            gp_id = data2[0]['id']
            
            

            return render(request, 'po/area_store/po_nabl_gatepass_print.html', {'data': material,'material':reject_item,'data1':data1,'gp_id':gp_id,'outward_qty':outward_qty })
        
        return render(request, 'po/area_store/po_nabl_gatepass.html', {'data': material,'material':reject_item,'outward_qty':outward_qty })
    return redirect('/')

def po_nabl_gatepass_print(request, id):
    store_name = Store_Info.objects.get(id=request.session['store'])
    material = DI_Areastores.objects.get(id=id)
    
    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)

    
    di_area_master_ids = [obj.id for obj in di_area_master]
            
    
    reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,area_store=store_name.Name,as_accepted=1)
    
    outward_qty = reject_item.count()
    
    print("outward_qty============outward_qty===============outward_qty",outward_qty)
    
    data1 = po_nabl_gatepass.objects.filter(area_store=material).earliest('id')
    print("data1=========data1=============data1:::::::::",data1.id)
    return render(request, 'po/area_store/po_nabl_gatepass_print2.html', {'data': material,'material':reject_item, 'data1':data1,'outward_qty':outward_qty})

def po_nabl_gatepass_upload(request, id):
    if request.method == "POST":
        gp_file = request.FILES['gp_file']
        data1 = po_nabl_gatepass.objects.get(id=id)
        data1.gatepass = gp_file
        data1.save()
        return redirect('/po/po_trf_create')
    return redirect('/po/po_trf_create')
    
    
def po_test_request_form_submit(request,id):
    material = DI_Areastores.objects.get(id=id)

    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)

    trf = po_nabl_gatepass.objects.get(area_store=material)
    if request.method == "POST":
        material = DI_Areastores.objects.get(id=id)
        po_nabl_garepass = po_nabl_gatepass.objects.get(area_store=material)
        customer_Organization_name = request.POST.get('customer_Organization_name') #1
        customer_Organization_address = request.POST.get('customer_Organization_address') #2
        contact_person_name = request.POST.get('contact_person_name') #3
        contact_person_designation = request.POST.get('contact_person_designation') #4
        mobile_no = request.POST.get('mobile_no') #4
        email_id = request.POST.get('email_id') #5
        name_of_sample_product = request.POST.get('name_of_sample_product') #6
        customer_ref_gatepass_no = request.POST.get('customer_ref_gatepass_no') #7
        trf_file = request.POST.get('trf_file') #9

        trf_obj = PO_TRF_Details(areastore = material.areastore,area_store_id = material,
                              customer_Organization_name=customer_Organization_name, 
                              customer_Organization_address=customer_Organization_address,
                              contact_person_name=contact_person_name,
                              contact_person_designation=contact_person_designation,
                              mobile_no = mobile_no, email_id = email_id,
                              name_of_sample_product=name_of_sample_product,
                              customer_ref_gatepass_no=customer_ref_gatepass_no, 
                              trf_generated = 1,gatepass_doc=po_nabl_garepass)
        trf_obj.save()
       
        for i in di_area_master:
            i.nabl_trf = 1
            i.save()
        trf_data = PO_TRF_Details.objects.filter(area_store_id=material).earliest('TRF_Id')
        return render(request, 'po/area_store/po_test_request_view.html', {'material': material,'trf':trf_data,'trf2':trf})
    return render(request, 'po/area_store/po_test_request_form.html',{'material': material,'trf':trf})

def po_nabl_update(request,id):
    material = DI_Areastores.objects.get(id=id)
    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
    
    for i in di_area_master:
        i.send_to_nabl = 1
        i.save()
    return redirect('/po/po_trf_create')


def select_received_material(request,id, erp_di_no):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id, di_master__erp_di_number=erp_di_no)
        serial = DI_Material_Offer_Serial_No.objects.filter(material=material.offer_item.item_name,area_store_id=material.id,Offer_status=1,po=material.po,area_store=store_name.Name)
        qty_material = len(serial)
        if request.method =="POST":
            for data in serial:
                pstatus = request.POST.get(f'{data.id}')


                if pstatus == None:
                    
                    data.received_material = data.received_material
                    data.save()

                elif pstatus == 1:
                    data.received_material = data.received_material
                    data.save()

                elif pstatus == -1:
                    data.received_material = data.received_material
                    data.save()

                else:                    
                    data.received_material = pstatus
                    data.save()
            return redirect(f'/po/po_di_material_view/{id}')
        return render(request, 'po/area_store/select_received_material.html', {'data': serial,'dataid':id, 'qty_material':qty_material, 'erp_di_no':erp_di_no})

    return redirect('/')

def select_material_for_getpass(request,id,erp_di_no):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        serial = DI_Material_Offer_Serial_No.objects.filter(area_store_id__di_master__erp_di_number=erp_di_no,area_store_id_id=material.id,Offer_status=1,po=material.po,area_store=store_name.Name)
        #serial = DI_Material_Offer_Serial_No.objects.filter(accepted=0,p_status='-1',material=material.offer_item.item_name,Offer_status=1,po=material.po,area_store=store_name.Name)
        if request.method =="POST":
            for data in serial:
                pstatus = request.POST.get(f'{data.id}')
                # print("yyyyyyyyyyyyyyyyyyyy",pstatus.p_status)
                # print("xxxxxxxxxxxxxxxxxx",pstatus.received_material)

                if pstatus == None:
                    
                    data.accepted = data.accepted
                    data.save()

                elif pstatus == 1:
                    data.accepted = data.accepted
                    data.save()


                else:                    
                    data.accepted = pstatus
                    data.save()
                # print("zzzzzzzzzzzzz",pstatus.p_status)
                # print("wwwwwwwwwwww",pstatus.received_material)
            return redirect(f'/po/create_po_gatepass/{id}/{erp_di_no}')

        return render(request, 'po/area_store/select_material_for_getpass.html', {'data': serial,'dataid':id})
    return redirect('/')

   
def forward_nabl_order(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    zone=officer.user_zone
    data2= RO_Info.objects.filter(mrc_flag=1,complete_sampled_by_cgm=0)     
    j=[]
    for i in data2:
        try:
            if i.rca_cell.user_zone == zone:
                j.append(i)
                print("SSSSSS",j)
        except Exception as e:
            pass    
    for i in j:
        print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiii :::::::::::::::::::::::::::: ", i.id)
    return render(request, 'po/area_store/forward_nabl_order.html', {'data': j})


def forward_nabl_order2(request,id):
    # officer = Officer.objects.get(employ_id= request.session['officer'])
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    zone=officer.user_zone
    
    # data = RO_Info.objects.all().order_by("-id")
    # cell =RCA_Cell.objects.get(Region = officer.Region)
    ro = RO_Info.objects.get(id=id)
    material = RO_Material_Info.objects.filter(ro_id=ro,forward_mat_to_cgm=1)
    # for i in material:
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA",i)
    data= RO_Info.objects.all().order_by("-id")
    j=[]
    for i in data:
        if i.rca_cell.user_zone==zone:
            j.append(i)
            
            return render(request, 'po/area_store/forward_nabl_order2.html', {'data': j,'ro':ro,'material':material})
    return render(request, 'po/area_store/forward_nabl_order2.html', {'data': j,'ro':ro,'material':material})
    
def forward_nabl(request, id):
    xmr_random1 = ""
    xmr_random2 = ""
    xmr_random3 = ""
    xmr_random4 = ""
    ro = RO_Info.objects.get(id=id)
    if ro.ro_nabl_lot_reject == 0:
        if ro.nabl_manual_rej_flag ==  0:     
            xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro,pa_result=1,uneco_status=0)
            xmr_tot2 = RO_Material_XMR_Info.objects.filter(ro=ro,pa_result=1,uneco_status=0)
            xmr_record = xmr_tot | xmr_tot2
            ddd = xmr_record.count()
            ddd2 = 0.1*ddd
            A = xmr_record.filter(Q(xmr_sampled_flag=0)|Q(ph_reject_by_nabl=0))
            if 0 < ddd <= 10:
                ro = RO_Info.objects.get(id=id)
                xmr_random1 = A.order_by('?')[:2]
                ro_xmr_random = RO_Info.objects.get(id=id)
                ro_xmr_random.random_flag = 1
                ro_xmr_random.any_release_sampled = 1
                ro_xmr_random.complete_sampled_by_cgm = 1
                ro_xmr_random.ro_sampling_date=date.today()
                ro_xmr_random.save()
                now = ro_xmr_random.ro_sampling_date
                date_time = now.strftime("%d-%m-%Y")
                
                for obj in xmr_random1:
                    obj.xmr_sampled_flag = 1
                    obj.xmr_initial_sampled_flag = 1
                    obj.save()
                    # material=RO_Material_Info.objects.get(id=obj.material.id)
                    # material.mat_sampled_flag = 1
                    # material.finally_sampled = 1
                    # material.flag_25_sampled=1
                    # material.save()
                    
                
            elif ddd > 10:
                ro = RO_Info.objects.get(id=id)
                xmr_random1 = A.order_by('?')[:math.ceil(ddd2)]
                ro_xmr_random = RO_Info.objects.get(id=id)
                ro_xmr_random.random_flag = 1
                ro_xmr_random.any_release_sampled = 1
                ro_xmr_random.complete_sampled_by_cgm = 1
                ro_xmr_random.ro_sampling_date=date.today()
                ro_xmr_random.save()
                now = ro_xmr_random.ro_sampling_date
                date_time = now.strftime("%d-%m-%Y")

                for obj in xmr_random1:
                    obj.xmr_sampled_flag = 1
                    obj.xmr_initial_sampled_flag = 1
                    obj.save()
                    # material=RO_Material_Info.objects.get(id=obj.material.id)
                    # material.mat_sampled_flag = 1
                    # material.finally_sampled = 1
                    # material.flag_25_sampled=1
                    # material.save()

        elif ro.nabl_manual_rej_flag ==  1:
                # m_obj = RO_Material_Info.objects.filter(ro_id=ro)
                # print("SSSSSSSSSSSSSSSSSSSSSSSSSS",m_obj)
            xmr_random_re=RO_Material_XMR_Info.objects.filter(ro=ro,xmr_sampled_flag=0,pa_result=1)
            xmr_rej_ph=RO_Material_XMR_Info.objects.filter(ro=ro,ph_reject_by_submit=1)
            ddd3=xmr_rej_ph.count()
            print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",ddd3)
            xmr_random1=xmr_random_re.order_by('?')[:ddd3]
            for obj in xmr_random1:
                obj.xmr_sampled_flag=1
                obj.xmr_replaced=1
                obj.save()
            ro_xmr_random=RO_Info.objects.get(id=id)
            ro_xmr_random.random_flag=1
            ro_xmr_random.any_release_sampled = 1
            ro_xmr_random.complete_sampled_by_cgm = 1
            ro_xmr_random.ro_resampling_date=date.today()
            ro_xmr_random.save()
            now = ro_xmr_random.ro_resampling_date
            date_time = now.strftime("%d-%m-%Y")

    elif ro.ro_nabl_lot_reject ==  1:     
        xmr_tot = RO_Material_XMR_Info.objects.filter(ro=ro,pa_result=1,uneco_status=0)
        xmr_tot2 = RO_Material_XMR_Info.objects.filter(ro=ro,pa_result=1,uneco_status=0)
        xmr_record = xmr_tot | xmr_tot2
        ddd = xmr_record.count()
        ddd2 = 0.1*ddd
        A = xmr_record.filter(Q(xmr_sampled_flag=0)|Q(ph_reject_by_nabl=0))
        if 0 < ddd <= 10:
            ro = RO_Info.objects.get(id=id)
            xmr_random1 = A.order_by('?')[:2]
            ro_xmr_random = RO_Info.objects.get(id=id)
            ro_xmr_random.random_flag = 1
            ro_xmr_random.any_release_sampled = 1	
            ro_xmr_random.complete_sampled_by_cgm = 1
            ro_xmr_random.ro_resampling_date=date.today()
            ro_xmr_random.save()
            now = ro_xmr_random.ro_resampling_date
            date_time = now.strftime("%d-%m-%Y")
                
            for obj in xmr_random1:
                obj.xmr_sampled_flag = 1
                obj.xmr_second_sampled_flag = 1
                obj.save()
                # material=RO_Material_Info.objects.get(id=obj.material.id)
                # material.mat_sampled_flag = 1
                # material.finally_sampled = 1
                # material.flag_25_sampled=1
                # material.save()
                
            
        elif ddd > 10:
            ro = RO_Info.objects.get(id=id)
            xmr_random1 = A.order_by('?')[:math.ceil(ddd2)]
            ro_xmr_random = RO_Info.objects.get(id=id)
            ro_xmr_random.random_flag = 1
            ro_xmr_random.any_release_sampled = 1
            ro_xmr_random.complete_sampled_by_cgm = 1
            ro_xmr_random.ro_resampling_date=date.today()
            ro_xmr_random.save()
            now = ro_xmr_random.ro_resampling_date
            date_time = now.strftime("%d-%m-%Y")

            for obj in xmr_random1:
                obj.xmr_sampled_flag = 1
                obj.xmr_second_sampled_flag = 1
                obj.save()
    
 
    xmr_random=""
    if xmr_random1:
        xmr_random=xmr_random1
        if xmr_random2:
            xmr_random=list(chain(xmr_random1,xmr_random2))
            if xmr_random3:
                xmr_random=list(chain(xmr_random1,xmr_random2, xmr_random3))
                if xmr_random4:
                    xmr_random=list(chain(xmr_random1,xmr_random2, xmr_random3, xmr_random4))


    elif xmr_random2:
        xmr_random=xmr_random2
        if xmr_random3:
            xmr_random=list(chain(xmr_random2, xmr_random3))
            if xmr_random4:
                xmr_random=list(chain(xmr_random2, xmr_random3, xmr_random4))

    elif xmr_random3:
        xmr_random=xmr_random3
        if xmr_random4:
            xmr_random=list(chain(xmr_random3, xmr_random4))

    elif xmr_random4:
        xmr_random=xmr_random4
       
    
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=0)
    xmr_ue = RO_Material_XMR_Info.objects.filter(ro=ro,uneco_status=1).count()
    print("xmr__counttttttttttttttt",type(xmr_ue))
    material = RO_Material_Info.objects.filter(ro_id=ro)
    material_count = RO_Material_Info.objects.filter(ro_id=ro).aggregate(Sum('quantity'))
    print("quaitytytyyyyyyyyyyyyyyy",material_count)
    print("quaitytytyyyyyyyyyyyyyyy",material_count)
    print("quaitytytyyyyyyyyyyyyyyy",material_count.values())
    print("quaitytytyyyyyyyyyyyyyyy",material_count['quantity__sum'])
    mat_count=material_count['quantity__sum']
    print("mmmmmmmmmmmmmmm",type(mat_count))
    mo = material_offer.objects.filter(ro_id=ro)
    ro_nabl_dispatch_check = RO_Info.objects.get(id=id)
    dispatch_for_nabl = ro_nabl_dispatch_check.dispatch_for_nabl
    test_request_form = ro_nabl_dispatch_check.test_request_form
    return render(request, 'po/area_store/forward_nabl.html', {'test_request_form':test_request_form,
            'dispatch_for_nabl':dispatch_for_nabl,'ro': ro, "material": material, "xmr": xmr, 'mo': mo,"xmr_random": xmr_random,'xmr_ue':xmr_ue,'mat_count':mat_count})



def forward_nabl_submit(request, id):
    
    ro = RO_Info.objects.get(id=id)
    xmr_random1=""
    if ro.ro_nabl_lot_reject == 0:
        if ro.nabl_manual_rej_flag == 0:
            xmr_random1 = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_initial_sampled_flag=1)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
        elif ro.nabl_manual_rej_flag == 1:
            xmr_random1 = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_second_sampled_flag = 1)
    elif ro.ro_nabl_lot_reject == 1:
        xmr_random1 = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_second_sampled_flag = 1)
        print("44444444$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4",xmr_random1)
    else:
        print("2@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # xmr_random1 = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_sampled_flag=1)

    ro = RO_Info.objects.get(id=id)
    material = RO_Material_Info.objects.filter(ro_id=ro)
 
    mo = material_offer.objects.filter(ro_id=ro)
    return render(request, 'po/area_store/forward_nabl_submit.html', {"xmr_random1": xmr_random1, "ro": ro, "mo": mo,"material":material})
    
    
    
def ro_for_trf(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data2=RO_Info.objects.filter(store=areastore.AreaStore.id,mrc_flag=1)
    k=[]
    for i in data2:      
        k.append(i)
    return render(request, 'po/area_store/ro_for_trf.html' , {'data': k})



def ro_for_trf2(request, id):
    ro = RO_Info.objects.get(id=id)
    material = RO_Material_Info.objects.filter(ro=ro)
    release=RO_Info.objects.all()
    final_mat_lst = []
    if ro.ro_nabl_lot_reject == 0:
        if ro.nabl_manual_rej_flag == 0:
            xmr_random1 = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_initial_sampled_flag=1)
            for j in xmr_random1:
                final_mat_lst.append(j.xmr)
        elif ro.nabl_manual_rej_flag == 1:
            xmr_random1 = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_replaced=1)
            for j in xmr_random1:
                final_mat_lst.append(j.xmr)
    elif ro.ro_nabl_lot_reject == 1:
        xmr_random1 = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_sampled_flag=1,xmr_second_sampled_flag=1)
        for j in xmr_random1:
            final_mat_lst.append(j.xmr)
    else:
        pass
    ro = RO_Info.objects.get(id=id)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo = material_offer.objects.filter(ro_id=ro)
    data= RO_Info.objects.filter(mrc_flag=1).order_by("-id")
    ro_nabl_dispatch_check = RO_Info.objects.get(id=id)
    dispatch_for_nabl = ro_nabl_dispatch_check.dispatch_for_nabl
    test_request_form = ro_nabl_dispatch_check.test_request_form
    #f3 = str(final_mat_lst)
    #f3 = f3.replace('/','-') 
    return render(request, 'po/area_store/ro_for_trf2.html' , {'test_request_form':test_request_form,
            'dispatch_for_nabl':dispatch_for_nabl, "xmr_random1": xmr_random1, "ro": ro, "material": material,"mo": mo,
            'final_mat_lst': str(final_mat_lst)})     

            
            
def select_nabl(request, ro_id, final_mat_lst):  
    f1 = final_mat_lst[2:-2]
    f2 = f1.split("', '")
    return render(request, 'po/area_store/select_nabl.html', {'ro_id':ro_id,'final_mat_lst':final_mat_lst})


def select_nabl2(request, ro_id, final_mat_lst, user_zone): 
    usr_obj = User_Registration.objects.filter(User_type = "NABL", User_zone = user_zone)
    store_name = Store_Info.objects.get(id=request.session['store'])
    f1 = final_mat_lst[2:-2]
    f2 = f1.split("', '")
    lst_xmr_id = []
    lst_capacity = []
    lst_type = []
    for xmr_id in f2:
        rmxi_obj = RO_Material_XMR_Info.objects.filter(ro=ro_id,xmr = xmr_id)
        for k in rmxi_obj:
            lst_capacity.append(k.material.rating)
            if k.new_design == 1:
                lst_type.append("Non-star(New Design)")
            elif k.old_l1 == 1:
                lst_type.append("Old L1")
            elif k.old_l2 == 1:
                lst_type.append("Old L2")
            elif k.design_non_star == 1:
                lst_type.append("Non-star(Old Desgin")
        lst_xmr_id.append(xmr_id)
    final_zip = zip(lst_xmr_id, lst_capacity, lst_type)

    if request.method == "POST":
        nabl_name_sub_radio = request.POST.get("sub_radio")
        ro = RO_Info.objects.get(id=ro_id)
        material=RO_Material_Info.objects.filter(ro=ro)
        for i in material:
            if i.mat_rejection_flag == 0:
                xmr_sample_mat=RO_Material_XMR_Info.objects.filter(ro=ro,xmr_sampled_flag=1)
            elif i.mat_rejection_flag == 1:
                xmr_sample_mat=RO_Material_XMR_Info.objects.filter(ro=ro,xmr_replaced=1)
        usr_obj2 = User_Registration.objects.get(CompanyName_E = nabl_name_sub_radio)
        return render(request, 'po/area_store/Gatepass_areastore.html', {'ro_id':ro_id, 'xmr_sample_mat':xmr_sample_mat,
                                                                        'discom_name_radio':user_zone,
                                                                        'nabl_name_sub_radio':nabl_name_sub_radio,
                                                                        'f2':f2, 'usr_obj2':usr_obj2, 'store_name':store_name, 
                                                                        'final_zip':final_zip})
    return render(request, 'po/area_store/select_nabl2.html', {'ro_id':ro_id,'final_mat_lst':final_mat_lst, 
                                                            'usr_obj':usr_obj, 'user_zone':user_zone, 'store_name':store_name})

def Gatepass_save(request, usr_obj2, roid):
    if request.method == "POST":
        DispatcherNameOfEntity = request.POST.get("DispatcherNameOfEntity")
        LoaOrderNo = request.POST.get("LoaOrderNo")
        NameOfItem = request.POST.get("NameOfItem")
        LoaOrderDate = request.POST.get("LoaOrderDate")
        DescriptionOfItem = request.POST.get("DescriptionOfItem")
        ManufacturerName = request.POST.get("ManufacturerName")
        VehicleNumber = request.POST.get("VehicleNumber")
        DINoDate = request.POST.get("DINoDate")
        DriverName = request.POST.get("DriverName")
        DriverContactNo = request.POST.get("DriverContactNo")
        IssueDate = request.POST.get("IssueDate")
        IssuedTo = request.POST.get("IssuedTo")
        VerifiedBy = request.POST.get("VerifiedBy")
        Gatekeeper = request.POST.get("Gatekeeper")
        IssuingAuthority = request.POST.get("IssuingAuthority")
        VerifiedByDesignation = request.POST.get("VerifiedByDesignation")
        GatekeeperDesignation = request.POST.get("GatekeeperDesignation")
        IssuingAuthorityDesignation = request.POST.get("IssuingAuthorityDesignation")
        ReceiverNameOfEntity = request.POST.get("ReceiverNameOfEntity")
        ReceiverContactPerson = request.POST.get("ReceiverContactPerson")
        ReceiverDetails = request.POST.get("ReceiverDetails")
        ReceiverContact = request.POST.get("ReceiverContact")

        usr_obj2 = User_Registration.objects.get(User_Id = usr_obj2)
        User = usr_obj2

        material_obj = Add_material_nabl(DispatcherNameOfEntity = DispatcherNameOfEntity, LoaOrderNo=LoaOrderNo,
                                        NameOfItem=NameOfItem, LoaOrderDate=LoaOrderDate, DescriptionOfItem=DescriptionOfItem, 
                                        ManufacturerName=ManufacturerName, VehicleNumber=VehicleNumber, 
                                        DINoDate=DINoDate, DriverName=DriverName, DriverContactNo=DriverContactNo,
                                        IssueDate=IssueDate, IssuedTo=IssuedTo, VerifiedBy=VerifiedBy, Gatekeeper=Gatekeeper, 
                                        IssuingAuthority=IssuingAuthority, VerifiedByDesignation=VerifiedByDesignation, 
                                        GatekeeperDesignation=GatekeeperDesignation, 
                                        IssuingAuthorityDesignation=IssuingAuthorityDesignation, 
                                        ReceiverNameOfEntity=ReceiverNameOfEntity,
                                        ReceiverContactPerson=ReceiverContactPerson, ReceiverDetails=ReceiverDetails, 
                                        ReceiverContact=ReceiverContact, User=User, Zone=usr_obj2.User_zone, 
                                        roid=roid, login_number = usr_obj2.ContactNo)
        material_obj.save()

        XMRList = request.POST.getlist("XMRList")
        CapacityList = request.POST.getlist("CapacityList")
        TypeList = request.POST.getlist("TypeList")
        RemarkList = request.POST.getlist("RemarkList")
        Gatepass = material_obj

        for i in range(len(XMRList)):
            if sample_code_table.objects.filter(XMRList=XMRList[i], Gatepass=material_obj).exists():
                pass
            else:
                sct_obj = sample_code_table(ro_id=roid, XMRList=XMRList[i], CapacityList=CapacityList[i], TypeList=TypeList[i],
                                            RemarkList=RemarkList[i],  Gatepass = Gatepass)
                sct_obj.save()

        final_zip = zip(XMRList, CapacityList, TypeList, RemarkList)
    return render(request, 'po/area_store/Gatepass_areastore2.html', {'usr_obj2':usr_obj2, 'material_obj':material_obj,
                                                                        'sct_obj':final_zip})

    

def Gatepass_areastore(request, ro_id):
    ro = RO_Info.objects.get(id=ro_id)
    material=RO_Material_Info.objects.filter(ro=ro)
    for i in material:
        if i.mat_rejection_flag==0:
            xmr_sample_mat=RO_Material_XMR_Info.objects.filter(ro=ro,xmr_sampled_flag=1)
        else:
            xmr_sample_mat=RO_Material_XMR_Info.objects.filter(ro=ro,xmr_replaced=1)
    return render(request, 'po/area_store/Gatepass_areastore.html', {'ro_id':ro_id, 'xmr_sample_mat':xmr_sample_mat})



def Gatepass_areastore2(request, ro_id, discom_name_radio, nabl_name_sub_radio):
    print("Gatepass_areastore2")
    if request.method == "POST":
        ro_obj = RO_Info.objects.get(id=ro_id)
        wo_obj = WO_Info.objects.get(id=ro_obj.wo.id)

        driver_name = request.POST.get("driver_name")
        driver_mobile = request.POST.get("driver_mobile")
        receiver_name = request.POST.get("receiver_name")
        vehicle_number = request.POST.get("vehicle_number")
        Material_name = request.POST.get("Material_name")
        trnsfrmr_type = request.POST.get("trnsfrmr_type")
        manufacturer_name = request.POST.get("manufacturer_name")
        rating = request.POST.get("rating")
        order_number = request.POST.get("order_number")
        order_date = request.POST.get("order_date")
        di_number = request.POST.get("di_number")
        di_date = request.POST.get("di_date")
        xmr_snos = request.POST.getlist("xmr_snos")
        send_to_lab = request.POST.get("send_to_lab")
        letter_no = request.POST.get("letter_no")
        date_within = request.POST.get("date_within")
        out_date = request.POST.get("out_date")
        issue_auth = request.POST.get("issue_auth")
        inspectioner_sign = request.POST.get("inspectioner_sign")
        receiver_sign = request.POST.get("receiver_sign")
        gatekeeper_sign = request.POST.get("gatekeeper_sign")

        material_obj = Add_material_nabl(user_id=wo_obj.vendor_id.User_Id, ro_id=ro_id, driver_name=driver_name, 
                                            driver_mobile=driver_mobile,
                                            receiver_name=receiver_name, vehicle_number=vehicle_number,
                                            trnsfrmr_type=trnsfrmr_type, Material_name=Material_name,
                                            manufacturer_name=manufacturer_name, 
                                            rating=rating,order_number=order_number,order_date=order_date,
                                            di_number=di_number,di_date=di_date,xmr_snos=xmr_snos,
                                            send_to_lab=send_to_lab, letter_no=letter_no,date_within=date_within,
                                            out_date=out_date, issue_auth=issue_auth, inspectioner_sign=inspectioner_sign,
                                            receiver_sign=receiver_sign, gatekeeper_sign=gatekeeper_sign,
                                            discom_name_radio=discom_name_radio, 
                                            nabl_name_sub_radio=nabl_name_sub_radio)
        material_obj.save()
    
    return render(request, 'po/area_store/Gatepass_areastore2.html', 
        {'id':material_obj.id, 'user_id':wo_obj.vendor_id.User_Id, 'ro_id':ro_id, 'driver_name':driver_name, 
        'driver_mobile':driver_mobile,
        'receiver_name':receiver_name, 'vehicle_number':vehicle_number,
        'trnsfrmr_type':trnsfrmr_type, 'manufacturer_name':manufacturer_name, 
        'rating':rating,'order_number':order_number,'order_date':order_date,
        'di_number':di_number,'di_date':di_date,'xmr_snos':xmr_snos,
        'send_to_lab':send_to_lab, 'letter_no':letter_no,'date_within':date_within,
        'out_date':out_date, 'issue_auth':issue_auth, 'inspectioner_sign':inspectioner_sign,
        'receiver_sign':receiver_sign, 'gatekeeper_sign':gatekeeper_sign,
        'discom_name_radio':discom_name_radio, 'nabl_name_sub_radio':nabl_name_sub_radio
        })


def uplaod_gatepass(request, gatepass_id):
    amn_obj = Add_material_nabl.objects.all()
    if request.method == "POST":
        if request.FILES['digitalCert']:
            filename = request.FILES['digitalCert']  
            amn_obj2 = Add_material_nabl.objects.get(id=gatepass_id)
            amn_obj2.gatepassAreaStore_file = filename
            amn_obj2.gatepass_generated = 1
            amn_obj2.save()
            amn_obj2 = Add_material_nabl.objects.all()
        return render(request, 'po/area_store/TRF_generate.html', {'amn_obj':amn_obj2})
    else:
        return render(request, 'po/area_store/TRF_generate.html', {'amn_obj':amn_obj})


def TRF_generate(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    amn_obj = Add_material_nabl.objects.filter(gatepass_generated = 1, Zone = officer.user_zone).order_by('-id')
    trf_obj = TRF_Details.objects.all().order_by('TRF_Id')
    return render(request, 'po/area_store/TRF_generate.html', {'amn_obj':amn_obj, 'trf_obj':trf_obj})


def SendMatToNabl(request, gatepass_id, TRF_Id, roid):
    if request.method == "POST":
        amn_obj = Add_material_nabl.objects.get(id = gatepass_id, TRF_Id = TRF_Id)
        sc_obj = sample_code_table.objects.filter(Gatepass = amn_obj)
        for i in sc_obj:
            xmer_obj=RO_Material_XMR_Info.objects.get(xmr=i.XMRList,ro=roid, )
            mat_obj=RO_Material_Info.objects.get(id=xmer_obj.material.id, rating = i.CapacityList)
            mat_obj.mat_sampl_process_complete=1
            mat_obj.save()
        amn_obj.SendMatToNabl = 1
        amn_obj.save()
    amn_obj = Add_material_nabl.objects.filter(gatepass_generated = 1).order_by('-id')
    trf_obj = TRF_Details.objects.all().order_by('TRF_Id')
    return render(request, 'po/area_store/TRF_generate.html', {'amn_obj':amn_obj, 'trf_obj':trf_obj})


def NABL_Report(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data1=RO_Info.objects.filter(store=areastore.AreaStore.id, any_release_sampled=1).order_by('-id')
    return render(request, 'po/area_store/NABL_Report.html', {'data': data1})
    
    
def NABL_Report2(request, ro_id):
    sc_obj = sample_code_table.objects.filter(ro_id = ro_id)
    lst_rca_order_no = []
    lst_allot_no = []
    lst_xmr_id = []
    lst_rating = []
    lst_report = []
    lst_userzone = []
    lst_passfail = []
    for i in sc_obj:
        lst_xmr_id.append(i.XMRList)
        lst_rating.append(i.CapacityList)
	
        if i.result_pass == 1:
                lst_passfail.append("Pass")
        elif i.result_pass == 0:
            lst_passfail.append("Fail")
        else:
            lst_passfail.append("None")
		
        if i.sampleCode_report:
            lst_report.append(i.sampleCode_report)
        else:
            lst_report.append("")
        
        xmr_new=RO_Material_XMR_Info.objects.get(xmr=i.XMRList, ro = i.ro_id)
        lst_allot_no.append(xmr_new.ro.id)
        lst_rca_order_no.append(xmr_new.ro.wo.id)
        lst_userzone.append(xmr_new.ro.rca_cell.user_zone)
    final_zip = zip(lst_userzone, lst_rca_order_no, lst_allot_no, lst_xmr_id, lst_rating, lst_report, lst_passfail)
    return render(request,'po/area_store/NABL_Report2.html', {'final_zip':final_zip})   


def sampling_details(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    zone=officer.user_zone
    data2= RO_Info.objects.filter(mrc_flag=1,any_release_sampled=1)

    j=[]
    for i in data2:
        try:
            if i.rca_cell.user_zone == zone:
                j.append(i)
        except Exception as e:
            pass    
    return render(request, 'po/area_store/sampling_details.html', {'data': j})
	
	
def sampling_details2(request,id):
    # officer = Officer.objects.get(employ_id= request.session['officer'])
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    zone=officer.user_zone
    
    # data = RO_Info.objects.all().order_by("-id")
    # cell =RCA_Cell.objects.get(Region = officer.Region)
    ro = RO_Info.objects.get(id=id)
    material = RO_Material_Info.objects.filter(ro_id=ro,forward_mat_to_cgm=1)
    xmr_random = ""
    if ro.ro_nabl_lot_reject == 0:
        if ro.nabl_manual_rej_flag == 0:
            xmr_random = RO_Material_XMR_Info.objects.filter(ro=ro,xmr_initial_sampled_flag=1)
        elif ro.nabl_manual_rej_flag == 1:
            xmr_random = RO_Material_XMR_Info.objects.filter(ro=ro,xmr_sampled_flag=1,xmr_second_sampled_flag = 1)
    elif ro.ro_nabl_lot_reject == 1:
        xmr_random = RO_Material_XMR_Info.objects.filter(ro=ro,xmr_sampled_flag=1,xmr_second_sampled_flag = 1)
    data= RO_Info.objects.all().order_by("-id")
    j=[]
    for i in data:
        if i.rca_cell.user_zone==zone:
            j.append(i)
            
            return render(request, 'po/area_store/sampling_details2.html', {'data': j,'ro':ro,'material':material,'xmr_random':xmr_random})
    return render(request, 'po/area_store/sampling_details2.html', {'data': j,'ro':ro,'material':material,'xmr_random':xmr_random})


def sampling_nabl_details(request, id):
    ro = RO_Info.objects.get(id=id)
    xmr_random=""
    if ro.ro_nabl_lot_reject == 0:
        if ro.nabl_manual_rej_flag == 0:
            xmr_random = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_initial_sampled_flag=1)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
        elif ro.nabl_manual_rej_flag == 1:
            xmr_random = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_second_sampled_flag = 1)
    elif ro.ro_nabl_lot_reject == 1:
        xmr_random = RO_Material_XMR_Info.objects.filter(ro=ro, xmr_second_sampled_flag = 1)
        print("44444444$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4",xmr_random)
    else:
        print("2@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    material = RO_Material_Info.objects.filter(ro_id=ro,forward_mat_to_cgm=1)
    # xmr_random=RO_Material_XMR_Info.objects.filter(ro=ro,xmr_sampled_flag=1)
    return render(request,'po/area_store/sampling_nabl_details.html',{'ro':ro,'xmr_random':xmr_random,'material':material})



def sampling_details_store(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data2= RO_Info.objects.filter(store=areastore.AreaStore.id,mrc_flag=1,any_release_sampled=1)
    return render(request, 'po/area_store/sampling_details_store.html', {'data': data2})
    
def sampling_details2_store(request,id):
    # officer = Officer.objects.get(employ_id= request.session['officer'])
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    zone=officer.user_zone
    
    # data = RO_Info.objects.all().order_by("-id")
    # cell =RCA_Cell.objects.get(Region = officer.Region)
    ro = RO_Info.objects.get(id=id)
    material = RO_Material_Info.objects.filter(ro_id=ro,forward_mat_to_cgm=1)
    # for i in material:
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA",i)
    data= RO_Info.objects.all().order_by("-id")
    j=[]
    for i in data:
        if i.rca_cell.user_zone==zone:
            j.append(i)
            
            return render(request, 'po/area_store/sampling_details2_store.html', {'data': j,'ro':ro,'material':material})
    return render(request, 'po/area_store/sampling_details2_store.html', {'data': j,'ro':ro,'material':material})
   

def sampling_nabl_details_store(request, id,vd):
    ro = RO_Info.objects.get(id=id)
    material = RO_Material_Info.objects.filter(ro_id=ro,forward_mat_to_cgm=1,id=vd)
    xmr_random=RO_Material_XMR_Info.objects.filter(material=vd,xmr_sampled_flag=1)
    return render(request,'po/area_store/sampling_nabl_details_store.html',{'ro':ro,'material':material,'xmr_random':xmr_random})










def rca_nabl_mat_rec_list(request):
    
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data1=RO_Info.objects.filter(store=areastore.AreaStore.id,mrc_flag=1,ro_nabl_comp_rej=1).order_by('-id')   
    return render(request,'po/area_store/rca_nabl_mat_rec_list.html',{'data': data1})



def rca_nabl_aprov_mat_list(request,id):
    ro = RO_Info.objects.get(id=id)
    data=RO_Material_Info.objects.filter(ro_id=ro,nabl_mat_lot_reject=1,nabl_mat_lot_submit=1)
    print("llllllllllllll",data)
    return render(request,'po/area_store/rca_nabl_aprov_mat_list.html',{'data': data})



# def rca_nabl_aprov_gatepass_details(request,id):
#     ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
#     xmr = RO_Material_XMR_Info.objects.filter(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,uneco_status=0)
#     gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
#     data=RO_Material_Info.objects.filter(ro=ro)
#     return render(request,'po/area_store/rca_nabl_aprov_gatepass.html',{"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})

def rca_nabl_aprov_gatepass_details(request,id):
    ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=0) | Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=1))
    # gp_det=as_nablpass_gatepass.objects.filter(inward_mat=material1)
    gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
    data=RO_Material_Info.objects.filter(ro=ro)
   
    
    return render(request,'po/area_store/rca_nabl_aprov_gatepass.html',{"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})




# def rca_nabl_aprov_gatepass(request,id):
#     if request.method == "POST":
#         mat=RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
#         gp_date = request.POST.get('gatepass_date')
#         gp_num=request.POST.get('gatepass_no')
#         gatekeep_name=request.POST.get('gk_name')
#         veh_no=request.POST.get('vehicle_no')
#         driv_name=request.POST.get('driver_name')
#         driv_phone=request.POST.get('driver_phone')
#         mater_rec_by=request.POST.get('mat_rece_by')
#         quantity=request.POST.get('inward_qty')
        
#         data1 = as_nabllotpass_gp(lotp_inward_no=mat,lotp_in_date=gp_date, lotp_in_num=gp_num, lotp_in_gk_name=gatekeep_name,
#                             lotp_in_vehicle_no=veh_no,lotp_in_driver_name=driv_name,lotp_in_driver_phone=driv_phone,
#                             lotp_in_rec_by=mater_rec_by,lotp_in_quantity=quantity)
#         data1.save()


#         ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
#         xmr = RO_Material_XMR_Info.objects.filter(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1)
#         gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
#         data=RO_Material_Info.objects.filter(ro=ro)
#         return render(request,'po/area_store/rca_nabl_aprov_gatepass.html',{'material': ro, "xmr": xmr,"gp":gp_det,"data1":data})

    
#     ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
#     xmr = RO_Material_XMR_Info.objects.filter(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1)
#     gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
#     data=RO_Material_Info.objects.filter(ro=ro)
#     return render(request,'po/area_store/rca_nabl_aprov_gatepass.html',{'material': ro, "xmr": xmr,"gp":gp_det,"data1":data})



def rca_nabl_aprov_gatepass(request,id):
    if request.method == "POST":
        # info=RO_Info.objects.get(id=id)
        mat=RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
        gp_date = request.POST.get('gatepass_date')
        gp_num=request.POST.get('gatepass_no')
        gatekeep_name=request.POST.get('gk_name')
        veh_no=request.POST.get('vehicle_no')
        driv_name=request.POST.get('driver_name')
        driv_phone=request.POST.get('driver_phone')
        mater_rec_by=request.POST.get('mat_rece_by')
        quantity=request.POST.get('inward_qty')
        




        data1 = as_nabllotpass_gp(lotp_inward_no=mat,lotp_in_date=gp_date, lotp_in_num=gp_num, lotp_in_gk_name=gatekeep_name,
                            lotp_in_vehicle_no=veh_no,lotp_in_driver_name=driv_name,lotp_in_driver_phone=driv_phone,
                            lotp_in_rec_by=mater_rec_by,lotp_in_quantity=quantity)
        data1.save()





        ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
        xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=0) | Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=1))
        gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
        data=RO_Material_Info.objects.filter(ro=ro)
        return render(request,'po/area_store/rca_nabl_aprov_gatepass.html',{'material': ro, "xmr": xmr,"gp":gp_det,"data1":data})

    
    ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=0) | Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=1))
    gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
    data=RO_Material_Info.objects.filter(ro=ro)
    return render(request,'po/area_store/rca_nabl_aprov_gatepass.html',{'material': ro, "xmr": xmr,"gp":gp_det,"data1":data})
   




# def rca_nabl_gp_xmr(request, id):
#     ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
#     xmr = RO_Material_XMR_Info.objects.filter(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1)
#     gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
#     data=RO_Material_Info.objects.filter(ro=ro)
    
#     return render(request, 'po/area_store/rca_nabl_gp_xmr.html', {"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})



def rca_nabl_gp_xmr(request, id):
    ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=0) | Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=1))
    gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
    data=RO_Material_Info.objects.filter(ro=ro)
    
    return render(request, 'po/area_store/rca_nabl_gp_xmr.html', {"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})



# def rca_nabl_gp_xmr_add(request, id):
#     if request.method == "POST":

#         abc = request.POST.getlist('xmr_det')
#         for data in abc:
#             test =RO_Material_XMR_Info.objects.get(id=data, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1)
#             test.as_nabl_approve_flag=1
#             test.as_nabl_approve_submitted=1
#             test.as_nabl_approve_date = date.today()
#             data1=RO_Info.objects.get(id=id,mrc_flag=1,ro_nabl_comp_rej=1)
#             data1.ro_as_nabl_receive_flag=1
#             data1.save()
#             ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)           
#             gp_infos=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro).last()
#             test.as_nabl_lotgp=gp_infos
#             test.save()

#         ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
#         xmr = RO_Material_XMR_Info.objects.filter(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1)
#         gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
#         data=RO_Material_Info.objects.filter(ro=ro)

#         return render(request, 'po/area_store/rca_nabl_gp_xmr.html', {"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})

#     ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
#     xmr = RO_Material_XMR_Info.objects.filter(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1)
#     gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
#     data=RO_Material_Info.objects.filter(ro=ro)
#     return render(request, 'po/area_store/rca_nabl_gp_xmr.html', {"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})



def rca_nabl_gp_xmr_add(request, id):
    if request.method == "POST":

        abc = request.POST.getlist('xmr_det')
        for data in abc:
            test =RO_Material_XMR_Info.objects.get(id=data, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1)
            test.as_nabl_approve_flag=1
            test.as_nabl_approve_submitted=1
            test.as_nabl_approve_date = date.today()
            data1=RO_Info.objects.get(id=id,mrc_flag=1,ro_nabl_comp_rej=1)
            data1.ro_as_nabl_receive_flag=1
            data1.save()
            ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)           
            gp_infos=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro).last()
            test.as_nabl_lotgp=gp_infos
            test.save()

        ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
        xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=0) | Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=1))
        gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
        data=RO_Material_Info.objects.filter(ro=ro)
        return render(request, 'po/area_store/rca_nabl_gp_xmr.html', {"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})

    ro = RO_Info.objects.get(id=id,ro_nabl_comp_rej=1)
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=0) | Q(ro=ro, machine_reject_by_nabl=1,nachine_reject_nabl_submit=1,single_reject_by_nabl=1))
    gp_det=as_nabllotpass_gp.objects.filter(lotp_inward_no=ro)
    data=RO_Material_Info.objects.filter(ro=ro)
    return render(request, 'po/area_store/rca_nabl_gp_xmr.html', {"material": ro, "xmr": xmr,"gp":gp_det,"data1":data})



def rca_mrc_order_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data1=RO_Info.objects.filter(store=areastore.AreaStore.id,ro_as_nabl_receive_flag=1).order_by('-id') 
    
    return render(request,'po/area_store/rca_mrc_all_ro.html',{'data': data1})





def rca_mrc_aprov_mat_list(request,id):
    ro = RO_Info.objects.get(id=id)
    data=RO_Material_Info.objects.filter(ro_id=ro,nabl_mat_lot_reject=1,nabl_mat_lot_submit=1,nabl_as_lot_receive=1)
    print("llllllllllllll",data)
    return render(request,'po/area_store/rca_mrc_aprov_mat_list.html',{'data': data})


# def rca_mrc_add_release(request,id):
#     if request.method == "POST":
        
#         ro = RO_Info.objects.get(id=id)
#         ordr_date = request.POST.get('mrc_order_date')
#         data1 = rca_mrc_details(ro=ro, mrc_date=ordr_date)
#         data1.save()
# 	ro.ro_mrc_initiate=1
#         ro.save()
#         ro = RO_Info.objects.get(id=id)
#         info=RO_Material_Info.objects.filter(ro=ro)
#         mr = rca_mrc_details.objects.get(ro=ro)
#         return render(request,'po/area_store/rca_mrc_add_copy.html',{'mr': mr,'data': ro,"mat":info})
    
#     ro = RO_Info.objects.get(id=id)
#     return render(request,'po/area_store/rca_create_mrc_release.html',{'data': ro})

def rca_mrc_add_release(request,id):
    if request.method == "POST":
        
        ro = RO_Info.objects.get(id=id)
        ordr_date = request.POST.get('mrc_order_date')
        data1 = rca_mrc_details(ro=ro, mrc_date=ordr_date)
        data1.save()
        ro.ro_mrc_initiate=1
        ro.save()
        ro = RO_Info.objects.get(id=id)
        info=RO_Material_Info.objects.filter(ro=ro)
        mr = rca_mrc_details.objects.get(ro=ro)
        return render(request,'po/area_store/rca_mrc_add_copy.html',{'mr': mr,'data': ro,"mat":info})
    
    ro = RO_Info.objects.get(id=id)
    return render(request,'po/area_store/rca_create_mrc_release.html',{'data': ro})


def rca_mrc_add_copy(request,id):
    if request.method == "POST":
        sched = request.POST.get("copy")
        mr =  rca_mrc_details.objects.get(id=id)
        # ro = RO_Info.objects.get(id=id)
        mrc_copy_det = rca_mrc_copy(mr=mr, copy_name=sched)
        mrc_copy_det.save()
        copy = rca_mrc_copy.objects.filter(mr=mr)
        return render(request, 'po/area_store/rca_mrc_add_copy.html', {'mr': mr, "copy": copy})
    return render(request, 'po/area_store/rca_mrc_add_copy.html')



def rca_mrc_add_comment(request,id):
    if request.method == "POST":
        comm = request.POST.get("comment")
        mr = rca_mrc_details.objects.get(id=id)
        mrc_comment_det =  rca_mrc_comment( mr_no=mr, add_comment=comm)
        mrc_comment_det.save()
        mr = rca_mrc_details.objects.get(id=id)
        ro = RO_Info.objects.get(id=mr.ro.id)
        ro.final_ro_mrc=1
        ro.save()
        

     
        mr = rca_mrc_details.objects.get(id=id)
        comment = rca_mrc_comment.objects.filter(mr_no=mr)
        return render(request,"po/area_store/rca_mrc_add_comment.html",{'mr': mr, "comment": comment})
    mr = rca_mrc_details.objects.get(id=id)
    comment = rca_mrc_comment.objects.filter(mr_no=mr)
    return render(request,"po/area_store/rca_mrc_add_comment.html",{'mr': mr, "comment": comment})



    






import numpy as np

def rca_mrc_view(request,id):
    
    mr = rca_mrc_details.objects.get( id=id)
    ro = RO_Info.objects.get(id=mr.ro.id)
    
   
    drr_total=[]

    ro_xmr_pa=RO_Material_XMR_Info.objects.filter(ro=ro,pa_result=1,as_nabl_approve_flag=1,uneco_status=0)
    
    for i in ro_xmr_pa:
        x=i.drr_details
        drr_total.append(x)

    uni_list=[]
    for y in drr_total:
        if y not in uni_list:
            uni_list.append(y)
   

    pa_len=len(ro_xmr_pa)
    quan_len=pa_len
   
    comment = rca_mrc_comment.objects.filter(mr_no=mr)
    copy = rca_mrc_copy.objects.filter(mr=mr)
    rec_gp = as_nabllotpass_gp.objects.filter(lotp_inward_no=mr.ro)

    mt=[]
    mt_des=[]


    mat=RO_Material_Info.objects.filter(ro=ro)
    for i in mat:
        mt.append(i.rating)
        mt_des.append(i.description)

    deliv = []
    mlist=[]
    for i in mat:
        ro_mat_xmr=RO_Material_XMR_Info.objects.filter(material=i,pa_result=1,uneco_status=0,as_nabl_approve_flag=1)
        l=len(ro_mat_xmr)
        deliv.append(l)

        xmr_no=[]
        for j in ro_mat_xmr:
            xmr_no.append(j.xmr)
        mlist.append(xmr_no)

    ro_mat_xmr=ro_mat_xmr=RO_Material_XMR_Info.objects.filter(ro=ro,pa_result=1,uneco_status=0,as_nabl_approve_flag=1)

    mzip=zip(mt,mt_des,deliv,mlist)
    ro_ue=[]

    ro_xmr=RO_Material_XMR_Info.objects.filter(ro=mr.ro,uneco_status=1,physical_status=1)
    for ue in ro_xmr:
        ro_ue.append(ue)
        
    return render(request,'po/area_store/rca_mrc.html',{"comment": comment,"copy": copy,'mr': mr,"drr":uni_list,"qt_xmr":quan_len,"rec_gate":rec_gp,"mat_del":mat,"del":deliv,"ro_mat_dtr":ro_mat_xmr,"xr_no":xmr_no,"matzip":mzip,"ro":ro,"ro_ue":ro_ue})



def upload_digi_mr(request, id):

    if request.method == "POST":

        upload_digi_doc_mr = request.FILES['digi_pdf_mr']

        mr = rca_mrc_details.objects.get(id=id)

        mr.digi_sign_mr = upload_digi_doc_mr
        mr.digi_flag_mr = 1

        mr.save()
        mr = rca_mrc_details.objects.get(id=id)
        return render(request, 'po/area_store/upload_digi_mr.html', {'mr': mr})
       
    mr = rca_mrc_details.objects.get(id=id)
    return render(request, 'po/area_store/upload_digi_mr.html', {'mr': mr})




def cgm_all_mrc(request):
    mr=rca_mrc_details.objects.filter( digi_flag_mr=1).order_by('-id')
    return render(request,'po/area_store/cgm_all_mrc.html',{'data': mr})



def rca_mrc_release_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data1=RO_Info.objects.filter(store=areastore.AreaStore.id,mrc_flag=1,ro_as_nabl_receive_flag=1)
    info=rca_mrc_details.objects.all()
    lt=[]
    for mr in info:
        mr.ro.store == areastore.AreaStore.id
        lt.append(mr)
          
    return render(request,'po/area_store/rca_mrc_release_list.html',{"data":lt})


def po_view_DI_list(request):
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    offered_data = DI_Master.objects.filter(zone =officer_data.user_zone ).order_by("-id")
    return render(request, 'po/po_creater/po_view_DI_list.html', {"data": offered_data, "officer":officer_data})

    

def send_di_for_approval(request,di_id,erp_di_no):
    data = DI_Master.objects.get(id = di_id )
    data.di_send_to_approval_status = True
    data.status = 1
    data.save()
    employ_login_id = request.session['employ_login_id']
    officer_data = Officer.objects.get(employ_login_id = employ_login_id)
    offered_data = DI_Master.objects.filter(zone =officer_data.user_zone, erp_di_number=erp_di_no )
    return render(request, 'po/po_creater/po_view_DI_list.html', {"data": offered_data,"msg1":"DI send for approval successfully","erp_di_no":erp_di_no})

def creater_view_di(request, po_id, erp_di_no):
    di_update_data1 = DI_Master.objects.get(id=po_id)
    po_data= Purchase_Order.objects.get(id=di_update_data1.po.id)
    print("ooooo",po_data)
    user = User_Registration.objects.filter(CompanyName_E=po_data.vendor)
    address = UserCompanyDataMain.objects.get(user_id=user[0].ContactNo)
    date = dtm.now().date()
    copy = PO_Copy.objects.filter(po=po_data)
    di_data = DI_Master.objects.filter(id=po_id)
    di_update_data = DI_Master.objects.filter(id=po_id)
    AreaStroeData = DI_Areastores.objects.filter(po=po_data, di_master__erp_di_number=erp_di_no)
    return render(request, 'po/po_creater/creater_view_di_pdf.html', {'copy':copy,'user':user[0],'date':date,'address':address,"po_data": po_data,"AreaStroeData":AreaStroeData ,"di_update_data":di_update_data[0],'erp_di_no':erp_di_no})


def power_analyzer_api_report(request,id,ro):
    
    xm=RO_Material_XMR_Info.objects.get(id=id,ro=ro,pa_result=1,physical_status=1,uneco_status=0)
    
    cal_rat=(xm.pa_api.NlHvVolts / xm.pa_api.NlLvVolts)*1.734
    apt_lim_lower=(xm.pa_api.NlHvVolts / xm.pa_api.NlLvVolts) * 1.734 * .995
    apt_lim_upper=(xm.pa_api.NlHvVolts / xm.pa_api.NlLvVolts) * 1.734 * 1.005
    avg_rest_ohm=(xm.pa_api.HvRes1+xm.pa_api.HvRes2+xm.pa_api.HvRes3)/3
    avg_rest_mlohm=(xm.pa_api.LvRes1+xm.pa_api.LvRes2+xm.pa_api.LvRes3)/3
    phase_rest=xm.pa_api.LVRperphaseat75*1000
    
    return render(request,'po/area_store/power_analyzer_api_rpt.html',{"dtr":xm,"c_rat":cal_rat,"ap_lower":apt_lim_lower,"ap_upper":apt_lim_upper,"ag_rt_ohm":avg_rest_ohm,
        "ag_rt_alohm":avg_rest_mlohm,"ph_rt": phase_rest})    


def po_vendor_list(request):
    data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',cgm_approval=1,digital_cert_upload=1,blacklisted=0)
    lst_oyt = []
    address = []
    for i in data:
        cert = certificate_details.objects.filter(User_Id = i.User_Id).last()
        lst_oyt.append(cert)
    
    for j in data:
        add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
        address.append(add)

    to_daaa =datetime.datetime.today()
    final_lst = zip(data,lst_oyt,address)
    return render(request, 'po/po_creater/all_vendor_details_po_creater.html', {'data':data,'to_daaa':to_daaa,'final_lst':final_lst})
   
    

def vendor_check_material_po_creater(request,id):
    data = User_Registration.objects.get(User_Id = id)
    material = Vendor_Material_Details.objects.filter(user_id = data)
    list_data = []
    for i in material:
        list_data.append(i.Material_Name)

    if request.method =="POST":
        get_data_value= request.POST.get('get_data_value')
        value_data = Vendor_Material_Details.objects.filter(user_id = data,Material_Name=get_data_value)
        return render(request, 'po/po_creater/vendor_all_material_po_creater.html', {'data':value_data}) 
    return render(request, 'po/po_creater/view_vendor_material_po_creater.html', {'data':set(list_data),'id':id})      



def po_approver_vendor_list(request):
    data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',cgm_approval=1,digital_cert_upload=1,blacklisted=0)
    lst_oyt = []
    address = []
    for i in data:
        cert = certificate_details.objects.filter(User_Id = i.User_Id).last()
        lst_oyt.append(cert)
    
    for j in data:
        add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
        address.append(add)

    to_daaa =datetime.datetime.today()
    final_lst = zip(data,lst_oyt,address)
    return render(request, 'po/po_approver/all_vendor_details_po_approver.html', {'data':data,'to_daaa':to_daaa,'final_lst':final_lst})
   
    

def vendor_check_material_po_approver(request,id):
    data = User_Registration.objects.get(User_Id = id)
    material = Vendor_Material_Details.objects.filter(user_id = data)
    list_data = []
    for i in material:
        list_data.append(i.Material_Name)

    if request.method =="POST":
        get_data_value= request.POST.get('get_data_value')
        value_data = Vendor_Material_Details.objects.filter(user_id = data,Material_Name=get_data_value)
        return render(request, 'po/po_approver/vendor_all_material_po_approver.html', {'data':value_data}) 
    return render(request, 'po/po_approver/view_vendor_material_po_approver.html', {'data':set(list_data),'id':id})      





#  --------------shubham tripathi code start here-----------------
from main.views import *
from django.db.models import Sum
from django.db.models import Count
curl=settings.CURRENT_URL

def po_officer_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()
    if officer is not None:
        order_type=request.GET.get('ordertype')
        # orole=officer.role.Role_Name
        if ((officer.role.Role_Name == "PO_CREATER" or officer.role.Role_Name == "GM" or officer.role.Role_Name == "DGM")):
            po_data = Purchase_Order.objects.annotate(total_invoice_ammount=Sum('purchase_order_data__total_invoice_amount'),num_invoice=Count('purchase_order_data')).filter(~Q(status=-1),po_approved_status=1,discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            pomd = PO_Material.objects.values('po').annotate(total_amount=Sum('total_amount'))
            # return render(request, 'po/po_invoice/officer_po_invoice_list.html', {'orole':orole,'officer': officer,'pomd':pomd,'po_data':po_data})
            return render(request, 'po/po_invoice/officer_creater_po_invoicelist.html', {'officer': officer,'pomd':pomd,'po_data':po_data})
        
        elif ((officer.role.Role_Name == "PO_APPROVER" or officer.role.Role_Name == "CGM")):
            po_data = Purchase_Order.objects.annotate(total_invoice_ammount=Sum('purchase_order_data__total_invoice_amount'),num_invoice=Count('purchase_order_data')).filter(~Q(status=-1),po_approved_status=1,discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            pomd = PO_Material.objects.values('po').annotate(total_amount=Sum('total_amount'))
            return render(request, 'po/po_invoice/officer_approver_po_invoicelist.html', {'officer': officer,'pomd':pomd,'po_data':po_data})
        
        elif ((officer.role.Role_Name == "CFO" or officer.role.Role_Name == "AO_BILLS" or officer.role.Role_Name == "DGM_EM" or officer.role.Role_Name == "DGM_CBPU")):
            po_data = Purchase_Order.objects.annotate(total_invoice_ammount=Sum('purchase_order_data__total_invoice_amount'),num_invoice=Count('purchase_order_data')).filter(~Q(status=-1),po_approved_status=1,discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            # po_data = Purchase_Order.objects.filter(~Q(status=-1),po_approved_status=1,discom_id=officer.Discom_id).order_by('-id')
            pomd = PO_Material.objects.values('po').annotate(total_amount=Sum('total_amount'))
            return render(request, 'po/po_invoice/finance_officer_poinvoice_list.html', {'officer': officer,'pomd':pomd,'po_data':po_data})
    else:
        return redirect(str(curl)+'mpeb_login')



def po_approver_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "PO_APPROVER":
            order_type=request.GET.get('ordertype')
            po_id=request.POST.get('po_id')
            invoice_id=request.POST.get('invoice_id')
            status=request.POST.get('status')
            officer_id=request.POST.get('officer_id')
    
            if int(status) == 1:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=3,assign_officer_id=officer_id)
                return redirect(po_officer_invoice_list)
            else:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
                return redirect(po_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            po_id=request.GET.get('poid')
            po_data=Purchase_Order.objects.filter(~Q(status=-1),po_approved_status=1,id=po_id,discom_id=officer.Discom_id).last()
            ofdata=Officer.objects.filter(role__Role_Name=("PO_CREATER"),Discom_id=po_data.discom_id)
            pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
            in_data = Invoice.objects.filter(~Q(status=-1),purchase_order_id=po_id,order_type = order_type).order_by('-id')
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'po/po_invoice/po_approver_invoice_list.html', {"pomd":pomd,"officer":officer,"ofdata":ofdata,'po_data':po_data,"in_data":in_data,'in_amount':in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def po_approver_invoice(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "PO_APPROVER":
            order_type=request.GET.get('ordertype')        
            po_id=request.POST.get('po_id')
            invoice_id=request.POST.get('invoice_id')
            cgm_status=request.POST.get('cgm_status')
            cgm_remark=request.POST.get('cgm_remark')
            gm_status=request.POST.get('gm_status')
            if int(cgm_status) == 1 and int(gm_status) == 1:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=5,cgm_remark=cgm_remark,cgm_status=cgm_status)
            elif int(cgm_status) == 1 and int(gm_status) == 2:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=3,cgm_remark=cgm_remark,cgm_status=cgm_status)
            else:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=cgm_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name,cgm_status=cgm_status,cgm_remark=cgm_remark)
            
            inup = Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).last()
            try:
                cgm_document = request.FILES['cgm_document']
                old_image = inup.cgm_document
                if old_image:
                    if os.path.exists(old_image.path):
                        os.remove(old_image.path)
                inup.cgm_document = cgm_document
                inup.save()
# for save invoice history  action 1 for accept and 2 for reject
                if int(cgm_status) == 1:
                    cgm_status = "Accepted"
                else:
                    cgm_status = "REJECTED"
                in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=cgm_remark,invoice_document=cgm_document,action=cgm_status).save()
            except Exception as e:
                pass
        return redirect(po_officer_invoice_list)
    else:
        return redirect(str(curl)+'mpeb_login')

def po_creator_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "PO_CREATER":
            order_type=request.GET.get('ordertype')        
            po_id=request.POST.get('po_id')
            invoice_id=request.POST.get('invoice_id')
            gm_status=request.POST.get('gm_status')
            gm_remark=request.POST.get('gm_remark')
            if int(gm_status) == 1:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=4,gm_remark=gm_remark,gm_status=gm_status)
            else:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=4,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name,gm_status=gm_status,gm_remark=gm_remark)
            
            inup = Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).last()
            try:
                gm_document = request.FILES['gm_document']
                old_image = inup.gm_document
                if old_image:
                    if os.path.exists(old_image.path):
                        os.remove(old_image.path)
                inup.gm_document = gm_document
                inup.save()
                if int(gm_status) == 1:
                    gm_status = "Accepted"
                else:
                    gm_status = "Rejected"
                in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=gm_remark,invoice_document=gm_document,action=gm_status).save()
            except Exception as e:
                pass
            return redirect(po_officer_invoice_list)

        else:
            order_type=request.GET.get('ordertype')
            po_id=request.GET.get('poid')
            po_data=Purchase_Order.objects.filter(~Q(status=-1),po_approved_status=1,id=po_id,discom_id=officer.Discom_id).last()
            pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
            in_data=Invoice.objects.filter(status__in=[5,0,1,2,3,4],assign_officer_id=officer.employ_id,purchase_order_id=po_id,order_type = order_type)
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'po/po_invoice/po_creater_invoice_list.html', {'officer': officer,'po_data':po_data,"in_data":in_data,"pomd":pomd,'in_amount':in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def po_cfo_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "CFO":
            order_type=request.GET.get('ordertype')        
            po_id=request.POST.get('po_id')
            invoice_id=request.POST.get('invoice_id')
            cfo_status=request.POST.get('cfo_status')
            cfo_remark=request.POST.get('cfo_remark')
            dgm_cbpu_status=request.POST.get('dgm_cbpu_status')

            if int(cfo_status) == 1 and int(dgm_cbpu_status) == 0:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(cfo_remark=cfo_remark,cfo_status=cfo_status)
            elif int(cfo_status) == 1 and int(dgm_cbpu_status) == 2:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(dgm_cbpu_status=3,cfo_remark=cfo_remark,cfo_status=cfo_status)
            else:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(cfo_remark=cfo_remark,cfo_status=cfo_status,status=cfo_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
                
            inup = Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).last()
            if int(cfo_status) == 1:
                cfo_status = "Accepted"
            else:
                cfo_status = "Rejected"

            try:
                if 'cfo_document' in request.FILES:
                    cfo_document = request.FILES['cfo_document']
                    old_image = inup.cfo_document
                    if old_image:
                        if os.path.exists(old_image.path):
                            os.remove(old_image.path)
                    inup.cfo_document = cfo_document
                    inup.save()
                    in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=cfo_remark,invoice_document=cfo_document,action=cfo_status).save()
                else:
                    in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=cfo_remark,action=cfo_status).save()                    
            except Exception as e:
                pass
            return redirect(po_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            po_id=request.GET.get('poid')
            po_data=Purchase_Order.objects.filter(~Q(status=-1),po_approved_status=1,id=po_id,discom_id=officer.Discom_id).last()
            pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
            in_data = Invoice.objects.filter(status__in=[1,2,5],purchase_order_id=po_id,order_type = order_type,gm_status=1,cgm_status=1)
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'po/po_invoice/po_cfo_invoicelist.html', {"officer":officer,"pomd":pomd,'po_data':po_data,"in_data":in_data,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def po_dgmcbpu_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "DGM_CBPU":
            order_type=request.GET.get('ordertype')        
            po_id=request.POST.get('po_id')
            invoice_id=request.POST.get('invoice_id')
            dgm_cbpu_status=request.POST.get('dgm_cbpu_status')
            dgm_cbpu_remark=request.POST.get('dgm_cbpu_remark')
            ao_bills_status=request.POST.get('ao_bills_status')

            if int(dgm_cbpu_status) == 1 and int(ao_bills_status) == 0:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(dgm_cbpu_remark=dgm_cbpu_remark,dgm_cbpu_status=dgm_cbpu_status)
            elif int(dgm_cbpu_status) == 1 and int(ao_bills_status) == 2:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(ao_bills_status=3,dgm_cbpu_remark=dgm_cbpu_remark,dgm_cbpu_status=dgm_cbpu_status)
            else:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(cfo_status=3,dgm_cbpu_remark=dgm_cbpu_remark,dgm_cbpu_status=dgm_cbpu_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
            
            inup = Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).last()
            
            if int(dgm_cbpu_status) == 1:
                dgm_cbpu_status = "Accepted"
            else:
                dgm_cbpu_status = "Rejected"
            try:
                if 'dgm_cbpu_document' in request.FILES:
                    dgm_cbpu_document = request.FILES['dgm_cbpu_document']
                    old_image = inup.dgm_cbpu_document
                    if old_image:
                        if os.path.exists(old_image.path):
                            os.remove(old_image.path)
                    inup.dgm_cbpu_document = dgm_cbpu_document
                    inup.save()
                    in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=dgm_cbpu_remark,invoice_document=dgm_cbpu_document,action=dgm_cbpu_status).save()
                else:
                    in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=dgm_cbpu_remark,action=dgm_cbpu_status).save()
                    print("shubham else condition ---------")
            except Exception as e:
                pass
            return redirect(po_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            po_id=request.GET.get('poid')
            po_data=Purchase_Order.objects.filter(~Q(status=-1),po_approved_status=1,id=po_id).last()
            pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
            in_data=Invoice.objects.filter(status__in=[1,2,5],purchase_order_id=po_id,order_type = order_type,gm_status=1,cgm_status=1,cfo_status__in=[1,3])
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'po/po_invoice/po_cbpu_invoicelist.html', {'officer': officer,'po_data':po_data,"in_data":in_data,"pomd":pomd ,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def po_aubills_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        if request.method == "POST" and officer.role.Role_Name == "AO_BILLS":
            order_type=request.GET.get('ordertype')        
            po_id=request.POST.get('po_id')
            invoice_id=request.POST.get('invoice_id')
            ao_bills_status=request.POST.get('ao_bills_status')
            ao_bills_remark=request.POST.get('ao_bills_remark')
            dgm_em_status=request.POST.get('dgm_em_status')
            if int(ao_bills_status) == 1 and int(dgm_em_status) == 0:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(ao_bills_remark=ao_bills_remark,ao_bills_status=ao_bills_status)
            elif int(ao_bills_status) == 1 and int(dgm_em_status) == 2:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(dgm_em_status=3,ao_bills_remark=ao_bills_remark,ao_bills_status=ao_bills_status)                
            else:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(dgm_cbpu_status=3,ao_bills_remark=ao_bills_remark,ao_bills_status=ao_bills_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
            inup = Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).last()
            try:
                ao_bills_document = request.FILES['ao_bills_document']
                old_image = inup.ao_bills_document
                if old_image:
                    if os.path.exists(old_image.path):
                        os.remove(old_image.path)
                inup.ao_bills_document = ao_bills_document
                inup.save()
                if int(ao_bills_status) == 1:
                    ao_bills_status = "Accepted"
                else:
                    ao_bills_status = "Rejected"

                in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=ao_bills_remark,invoice_document=ao_bills_document,action=ao_bills_status).save()
            except Exception as e:
                pass
            return redirect(po_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            po_id=request.GET.get('poid')
            po_data=Purchase_Order.objects.filter(~Q(status=-1),po_approved_status=1,id=po_id).last()
            pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
            in_data=Invoice.objects.filter(status__in=[1,2,5],purchase_order_id=po_id,order_type = order_type,gm_status=1,dgm_cbpu_status__in=[1,3])
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'po/po_invoice/po_aubills_invoicelist.html', {'officer': officer,'po_data':po_data,"in_data":in_data,"pomd":pomd,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def po_dgmem_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        if request.method == "POST" and officer.role.Role_Name == "DGM_EM":
            order_type=request.GET.get('ordertype')        
            po_id=request.POST.get('po_id')
            invoice_id=request.POST.get('invoice_id')
            dgm_em_status=request.POST.get('dgm_em_status')
            dgm_em_remark=request.POST.get('dgm_em_remark')
            if int(dgm_em_status) == 1:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(status=1,dgm_em_remark=dgm_em_remark,dgm_em_status=dgm_em_status)
            else:
                Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).update(ao_bills_status=3,dgm_em_remark=dgm_em_remark,dgm_em_status=dgm_em_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
            inup = Invoice.objects.filter(purchase_order_id=po_id,id=invoice_id).last()
            try:
                dgm_em_document = request.FILES['dgm_em_document']
                old_image = inup.dgm_em_document
                if old_image:
                    if os.path.exists(old_image.path):
                        os.remove(old_image.path)
                inup.dgm_em_document = dgm_em_document
                inup.save()
                if int(dgm_em_status) == 1:
                    dgm_em_status = "Accepted"
                else:
                    dgm_em_status = "Rejected"

                in_history=InvoiceHistory(invoice_id=inup.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=ao_bills_remark,invoice_document=ao_bills_document,action=ao_bills_status).save()            
            except Exception as e:
                pass
            return redirect(po_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            po_id=request.GET.get('poid')
            po_data=Purchase_Order.objects.filter(~Q(status=-1),po_approved_status=1,id=po_id).last()
            pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
            in_data=Invoice.objects.filter(status__in=[1,2,5],purchase_order_id=po_id,order_type = order_type,gm_status=1,cgm_status=1,cfo_status=1,ao_bills_status__in=[1,3])
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'po/po_invoice/po_dgmem_invoicelist.html', {'officer': officer,'po_data':po_data,"in_data":in_data,"pomd":pomd,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

#-----------------shubham tripathi code end here-----------------------------------

#****************************partial mrc code lok**********************


def partial_mrc_sign_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data1=RO_Info.objects.filter(store=areastore.AreaStore.id,mrc_flag=1,ro_as_nabl_receive_flag=1)
    info=partial_mrc_details.objects.all()
    lt=[]
    for pr in info:
        pr.ro.store == areastore.AreaStore
        lt.append(pr)
          
    return render(request,'po/area_store/partial_mrc_sign_list.html',{"data":lt})




def upload_digi_partial_mrc(request, id):

    if request.method == "POST":

        upload_digi_doc_pr = request.FILES['digi_pdf_pr']

        pr = partial_mrc_details.objects.get(id=id)

        pr.digi_sign_pr = upload_digi_doc_pr
        pr.digi_flag_pr = 1

        pr.save()
        pr = partial_mrc_details.objects.get(id=id)
        return render(request, 'po/area_store/upload_digi_pr.html', {'pr': pr})
       
    pr = partial_mrc_details.objects.get(id=id)
    return render(request, 'po/area_store/upload_digi_pr.html', {'pr': pr})



def partial_mrc_order_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
    areastore=AreaStore_Officer.objects.get(Officer=officer)
    data1=RO_Info.objects.filter(Q(store=areastore.AreaStore.id,ro_nabl_sin_rej=1) | Q(store=areastore.AreaStore.id,ro_nabl_mac_rej=1)).order_by('-id')
    return render(request,'po/area_store/partial_mrc_all_ro.html',{'data': data1})



def partial_mrc_add_release(request,id):
    if request.method == "POST":
        ro = RO_Info.objects.get(id=id)
        ordr_date = request.POST.get('mrc_order_date')
        data1 = partial_mrc_details(ro=ro, partial_date=ordr_date)
        data1.save()
        pr = partial_mrc_details.objects.latest("id")
        return render(request,'po/area_store/partial_mrc_add_copy.html',{'pr':pr})
  
    ro = RO_Info.objects.get(id=id)
    return render(request,'po/area_store/partial_create_mrc_release.html',{'data': ro})




def partial_mrc_add_copy(request,id):
    if request.method == "POST":
        sched = request.POST.get("copy")
        pr =  partial_mrc_details.objects.get(id=id)
        
        mrc_copy_det = partial_mrc_copy(ro=pr, copy_name=sched)
        mrc_copy_det.save()
        pr =  partial_mrc_details.objects.get(id=id)
        copy = partial_mrc_copy.objects.filter(ro=pr)
        return render(request, 'po/area_store/partial_mrc_add_copy.html', {'pr': pr, "copy": copy})
    return render(request, 'po/area_store/partial_mrc_add_copy.html')




def partial_mrc_add_comment(request,id):
    if request.method == "POST":
        comm = request.POST.get("comment")
        pr = partial_mrc_details.objects.get(id=id)
        pr_comment_det = partial_mrc_comment( ro=pr, add_comment=comm)
        pr_comment_det.save()
        
        pr = partial_mrc_details.objects.get(id=id)
        comment = partial_mrc_comment.objects.filter(ro=pr)
        return render(request,"po/area_store/partial_mrc_add_comment.html",{'pr': pr, "comment": comment})
    pr = partial_mrc_details.objects.get(id=id)
    comment = partial_mrc_comment.objects.filter(ro=pr)
    return render(request,"po/area_store/partial_mrc_add_comment.html",{'pr': pr, "comment": comment})





def partial_mrc_add_xmr(request,id):
    pr=partial_mrc_details.objects.get(id=id)
    ro=RO_Info.objects.get(id=pr.ro.id)
    material=RO_Material_Info.objects.filter(ro=pr.ro)
    ro_xmr_pa=RO_Material_XMR_Info.objects.filter(Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0, partial_mrc_xmr_submit =0) | Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0, partial_mrc_xmr_submit =0)) 
    xmr_pr_submitted=RO_Material_XMR_Info.objects.filter(Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =1) | Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =1))     
    return render(request,"po/area_store/partial_mrc_add_xmr.html",{'pr': pr,"xmr":ro_xmr_pa,'ro':ro,'material':material,"xmr_sub":xmr_pr_submitted})


def partial_mrc_xmr_accepted(request,id):
     
    if request.method == "POST":
        abc = request.POST.getlist('xmr_det')
        for data in abc:
            test = RO_Material_XMR_Info.objects.get(id=data)
            test.partial_mrc_xmr_submit=1
            pr_det=partial_mrc_details.objects.get(id=id)
            test.partial_mrc_det=pr_det
            test.save()

        pr=partial_mrc_details.objects.get(id=id)
        ro=RO_Info.objects.get(id=pr.ro.id)
        material=RO_Material_Info.objects.filter(ro=pr.ro)
        ro_xmr_pa=RO_Material_XMR_Info.objects.filter(Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =0) | Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =0)) 
        xmr_pr_submitted=RO_Material_XMR_Info.objects.filter(Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =1) | Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =1)) 
        return render(request, 'po/area_store/partial_mrc_add_xmr.html', {'pr': pr,"xmr":ro_xmr_pa,'ro':ro,'material':material,"xmr_sub":xmr_pr_submitted})
    pr=partial_mrc_details.objects.get(id=id)
    ro=RO_Info.objects.get(id=pr.ro.id)
    material=RO_Material_Info.objects.filter(ro=pr.ro)
    ro_xmr_pa=RO_Material_XMR_Info.objects.filter(Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =0) | Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =0))
    xmr_pr_submitted=RO_Material_XMR_Info.objects.filter(Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =1) | Q(ro=pr.ro,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =1)) 
   
    
    return render(request,"po/area_store/partial_mrc_add_xmr.html",{'pr': pr,"xmr":ro_xmr_pa,'ro':ro,'material':material,"xmr_sub":xmr_pr_submitted})
    
    


import numpy as np

def partial_mrc_view(request,id):
    
    pr = partial_mrc_details.objects.get(id=id)
    ro = RO_Info.objects.get(id=pr.ro.id)

    
    drr_total=[]
    
    xmr_pr_submitted=RO_Material_XMR_Info.objects.filter(Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =1) | Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =1))

 
    
    for i in  xmr_pr_submitted:
        x=i.drr_details
        drr_total.append(x)

    uni_list=[]
    for y in drr_total:
        if y not in uni_list:
            uni_list.append(y)
   

    pa_len=len(xmr_pr_submitted)
    quan_len=pa_len
   
    comment = partial_mrc_comment.objects.filter(ro=pr)
   
    copy = partial_mrc_copy.objects.filter(ro=pr)
  

    
    
    
    tot_mt=[]
    tot_des=[]
    
    for d in xmr_pr_submitted:
        tot_mt.append(d.material.rating)
        tot_des.append(d.material.description)
        
    mt=[]
    mt_des=[]
        
    for s in tot_mt:
        if s not in mt:
            mt.append(s)
            
    for t in tot_des:
        if t not in mt_des:
            mt_des.append(t)
        
        
        
   

    deliv = []
    mlist=[]
    
    xmr_pr_submitted=RO_Material_XMR_Info.objects.filter(Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =1) | Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =1))
    
    
    
    
    for i in mt:
        
        count=0
        xmr_no=[]
       
        xmr_pr_submitted=RO_Material_XMR_Info.objects.filter(Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =1) | Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =1))
        for x in xmr_pr_submitted:
            print("iiiiiii",i)
            if x.material.rating == i:
                count=count+1
                        
                xmr_no.append(x.xmr)
           
        mlist.append(xmr_no)
       
              
        deliv.append(count)
              
    
       
       

   
    mzip=zip(mt,mt_des,deliv,mlist)


  
    
    xmr_pr_submitted=RO_Material_XMR_Info.objects.filter(Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,single_reject_nabl_submit=1, single_reject_by_nabl=0,partial_mrc_xmr_submit =1) | Q(partial_mrc_det=pr,pa_result=1,as_nabl_approve_flag=0,uneco_status=0,ph_reject_by_submit=1,ph_reject_by_nabl=0,partial_mrc_xmr_submit =1))


        
    return render(request,'po/area_store/partial_mrc_view.html',{"comment": comment,"copy": copy,'pr': pr,"drr":uni_list,"qt_xmr":quan_len,"del":deliv,"ro_mat_dtr":xmr_pr_submitted,"matzip":mzip,"ro":ro})

#*****************partial mrc code end********************

#*************PO MRC GENERATE*******************

def po_mrc_order_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    data1=DI_Areastores.objects.filter(samp_accepted_flag=1, nabl_status=1,po__zone=officer.user_zone).order_by('-id')
    return render(request,'po/mrc/po_mrc_all.html',{'data': data1})

def view_test_result(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    data1=DI_Areastores.objects.get(id=id)
    nabl_result=sample_code_table_cp.objects.filter(di_area_store = data1)
    reject_count=sample_code_table_cp.objects.filter(di_area_store = data1, phy_rejected=1).count()
    return render(request,'po/mrc/test_result.html',{'data': nabl_result})



def po_mrc_add_release(request,id):
    if request.method == "POST":
        
        ro = DI_Areastores.objects.get(id=id)
        ordr_date = request.POST.get('mrc_order_date')
        data1 = purchase_mrc_details(ro=ro, mrc_date=ordr_date)
        data1.save()
        ro.mrc_create_flag=True
        ro.save()
        di = DI_Master.objects.get(erp_di_number=ro.di_master.erp_di_number)
        di.nabl_status=1
        di.mrc_status = True
        di.save()
        offer=PO_Material_Offer.objects.get(id=ro.offer_item.id)
        offer.status=2
        offer.save()
        info=DI_Material_Offer_Serial_No.objects.filter(area_store_id=ro)
        mr = purchase_mrc_details.objects.get(ro=ro)
        return render(request,'po/mrc/po_mrc_add_copy.html',{'mr': mr,'data': ro,"mat":info})
   
    ro = DI_Areastores.objects.get(id=id)
    return render(request,'po/mrc/po_create_mrc_release.html',{'data': ro})


def po_mrc_add_copy(request,id):
    if request.method == "POST":
        sched = request.POST.get("copy")
        mr =  purchase_mrc_details.objects.get(id=id)
        mrc_copy_det = purchase_mrc_copy(ro=mr, copy_name=sched)
        mrc_copy_det.save()
        copy = purchase_mrc_copy.objects.filter(ro=mr)
        return render(request, 'po/mrc/po_mrc_add_copy.html', {'mr': mr, "copy": copy})
    return render(request, 'po/mrc/po_mrc_add_copy.html')


def po_mrc_add_comment(request,id):
    if request.method == "POST":
        comm = request.POST.get("comment")
        mr = purchase_mrc_details.objects.get(id=id)
        mr_comment_det = purchase_mrc_comment( ro=mr, add_comment=comm)
        mr_comment_det.save()
        mr = purchase_mrc_details.objects.get(id=id)
        comment = purchase_mrc_comment.objects.filter(ro=mr)
        return render(request,"po/mrc/po_mrc_add_comment.html",{'mr': mr, "comment": comment})
    mr = purchase_mrc_details.objects.get(id=id)
    comment = purchase_mrc_comment.objects.filter(ro=mr)
    return render(request,"po/mrc/po_mrc_add_comment.html",{'mr': mr, "comment": comment})

def po_view_mrc(request,id):
    pr=purchase_mrc_details.objects.get(id=id)
    ro=DI_Areastores.objects.get(id=pr.ro.id)
    drr = po_drr_info.objects.filter(area_store_id = ro.id)
    # grn = po_drr_info.objects.get(id = drr.id)
    comment=purchase_mrc_comment.objects.get(ro=pr)
    deliverable_qty=ro.deliverable_qty
    reject_count=sample_code_table_cp.objects.filter(di_area_store_id=ro.id, phy_rejected=1).count()
    mrc_count = deliverable_qty - int(reject_count)
    return render(request,"po/mrc/po_view_mrc.html",{'pr': pr,'ro':ro, 'comment':comment, 'mrc_count':mrc_count, 'grn':drr})



def po_mrc_release_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    store_name = Store_Info.objects.get(id=request.session['store'])
    data1=DI_Areastores.objects.filter(areastore = store_name.Name, mrc_create_flag=True,samp_accepted_flag=1,po__zone=officer.user_zone)
    info=purchase_mrc_details.objects.filter(ro__po__zone=officer.user_zone)
    return render(request,'po/mrc/po_mrc_release_list.html',{"data":info, "data1":data1})


def upload_digital_po_mrc(request, id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.employ_id
    if request.method == "POST":
        upload_digi_doc_mr = request.FILES['digi_pdf_pr']

        mr = purchase_mrc_details.objects.get(id=id)
        mr.digi_sign_pr = upload_digi_doc_mr
        mr.digi_flag_pr = 1
        mr.save()
        info=purchase_mrc_details.objects.filter(id=id)
        return render(request, 'po/mrc/po_mrc_release_list.html', {"data":info})
       
    mr = purchase_mrc_details.objects.get(id=id)
    return render(request, 'po/mrc/upload_digital_po_mrc.html', {'mr': mr})

#-----------------------------------end--------------------------------------------------

#------------------------------view po mrc-----------------------------------------------
def las_view_mrc(request,id):
    ro=DI_Areastores.objects.get(id=id)
    try:
        pr=purchase_mrc_details.objects.get(ro_id=id)
        view=purchase_mrc_details.objects.filter(id=pr.id)
    except:
        return redirect('/po/nabl_check_di_status')
    return render(request,"po/area_store/po_view_mrc.html",{'pr': view,'ro':ro})


def view_mrc_creator(request,erp_di_no):
    di=DI_Master.objects.get(erp_di_number=erp_di_no)
    ro=DI_Areastores.objects.filter(di_master=di, di_master__erp_di_number=erp_di_no)
    for i in ro:
        try:
            pr=purchase_mrc_details.objects.get(ro_id=i.id)
            view=purchase_mrc_details.objects.filter(id=pr.id)
        except Exception as e:
            return redirect('/po/po_view_DI_list')
        return render(request,"po/po_creater/po_view_mrc.html",{'pr': view,'ro':ro})
    return redirect ('/')


def view_mrc_approver(request,erp_di_no):
    di=DI_Master.objects.get(erp_di_number=erp_di_no)
    ro=DI_Areastores.objects.filter(di_master=di, di_master__erp_di_number=erp_di_no)
    for i in ro:
        try:
            pr=purchase_mrc_details.objects.get(ro_id=i.id)
            view=purchase_mrc_details.objects.filter(id=pr.id)
        except Exception as e:
            return redirect('/po/po_view_DI_list')
        return render(request,"po/po_creater/po_view_mrc.html",{'pr': view,'ro':ro})
    return redirect ('/')
#---------------------------end--------------------------------------------------------



###################  PO Reampling  Start ######################################

def po_resampling(request,id):
    if request.session.has_key('employ_login_id'):
        emp_id = request.session['employ_login_id']
        area = Officer.objects.get(employ_login_id=emp_id)
        zone=area.user_zone
        
        di_as_obj = DI_Areastores.objects.get(id=id,zone=zone)
        # di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id=di_as_obj)
        
        di_master_obj = DI_Master.objects.get(id = di_as_obj.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,as_accepted=0)
        

        
        print("di_mosn_obj============di_mosn_obj====di_mosn_obj",di_mosn_obj)
        
        area_store = []
        s_no = []
        
        for i in di_mosn_obj :
            a = i.area_store
            b = i.serial_no
            area_store.append(a)
            s_no.append(b)
            
        
        s = area_store.count('Area Store Bhopal')        
        if s < 2:
            pass

        mat_name = di_as_obj.offer_item.material.specification 
        user_id = di_as_obj.po.vendor.User_Id #
        item_code = di_as_obj.material_sample_code
        lst_serial_number = []

        offer_qty =  di_as_obj.offer_item.total_quantity
        di_qty =  di_as_obj.offer_item.dispatch_qty
        for i in di_mosn_obj:
            lst_serial_number.append(i.serial_no)
            
        sample_percent = 0
        sample_unit = 0
        flag = -1

        ps_obj = product_sampling.objects.filter(Q(item_code = item_code) | Q(item_code_ez = item_code) | Q(item_code_wz = item_code))
        for i in ps_obj:
            sample_type = i.sampling.sample_type
            if sample_type == 0:
                flag = 0
                lot_size_min = i.sampling.lot_size_min
                lot_size_max = i.sampling.lot_size_max
                if di_qty >= lot_size_min and di_qty <= lot_size_max:
                    sample_unit = i.sampling.sample_unit
                else:
                    pass
            elif sample_type == 1:
                sample_percent = i.sampling.sample_percentage
                flag = 1
        final_random_sample_mat = ""
        
        
        if flag == 0:
            random.shuffle(lst_serial_number)
            final_random_sample_mat = lst_serial_number[:sample_unit]
            
            
        elif flag == 1:            
            length_serial_number =  len(lst_serial_number)
            random_mat_round_number = math.ceil((length_serial_number * sample_percent ) / 100)
            random.shuffle(lst_serial_number)
            final_random_sample_mat = lst_serial_number[:random_mat_round_number]
        
        
        area_name = []
        
        
        for i in di_mosn_obj:
            if i.serial_no in final_random_sample_mat:
                area_name.append(i.area_store)
                
        print("area_name==========area_name========area_name",area_name)
        final_zip =  zip(final_random_sample_mat, di_mosn_obj, area_name)
        return render(request, 'officer/po_resampling.html', {'data1': di_as_obj,'final_zip':final_zip, 'Di_id':id, 'final_random_sample_mat':final_random_sample_mat})
    return redirect('/')

def po_resampling_submit(request,id, final_random_sample_mat):
    emp_id = request.session['employ_login_id']
    area = Officer.objects.get(employ_login_id=emp_id)
    zone = area.user_zone
    di_obj = DI_Areastores.objects.get(id=id,zone=zone)
    s = final_random_sample_mat[2:-2]
    ss = s.split("', '")
    for i in ss:
        di_master_obj = DI_Master.objects.get(id = di_obj.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        obj = DI_Material_Offer_Serial_No.objects.filter(serial_no=i.strip(),area_store_id__in=di_area_master_ids,as_accepted=0)
        for j in obj:
            j.as_accepted=2
            j.save()
    for i in di_area_master:
        i.sampling_flag = 2
        i.save()
    
    return redirect('/po/po_sample_list')





def view_Resamled_material(request,id):
    if request.session.has_key('employ_login_id'):
        material = DI_Areastores.objects.get(id=id)
        di_area_store = DI_Master.objects.filter(id = material.di_master.id)
        lst_as = []
        item_code = []
        serial_no = []
        di_master_obj = DI_Master.objects.get(id = material.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids, as_accepted=2)
        for j in di_mosn_obj:
            serial_no.append(j.serial_no)
            item_code.append(j.area_store_id.material_sample_code)
        return render(request, 'officer/view_Resampled_material.html', {'di_mosn_obj':di_mosn_obj})
    return redirect('/')


def po_nabl_gatepass_resampling(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        material = DI_Areastores.objects.get(id=id)
        
        
        di_master_obj = DI_Master.objects.get(id = material.di_master.id)
        
        di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
        
        di_area_master_ids = [obj.id for obj in di_area_master]
        
        
        # di_mosn_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids, as_accepted=1)
        
        reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,area_store=store_name.Name,as_accepted=2)
        
        # reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id=material,area_store=store_name.Name,as_accepted=2)
        
        outward_qty = reject_item.count()
        
        if request.method == "POST":
            gp_date = request.POST.get('gatepass_date')
            gp_num=request.POST.get('gatepass_no')
            gatekeep_name=request.POST.get('gk_name')
            veh_no=request.POST.get('vehicle_no')
            driv_name=request.POST.get('driver_name')
            driv_phone=request.POST.get('driver_phone')
            mater_rec_by=request.POST.get('mat_rece_by')
            quantity=request.POST.get('outward_qty')
            driver_aadh=request.FILES['driver_aadhar']

            data1 = po_nabl_gatepass(area_store=material, gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,aname = store_name.Name,
                                material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh,nabl_name = material.nabl_name,nabl_number = material.nabl_number)
            data1.save()
            # material.nabl_gatepass = 2
            # material.save()
            
            for i in di_area_master:
                i.nabl_gatepass = 2
                i.save()            
            
            for i in reject_item:
                i.accepted = 2
                i.save()
                

            data2 = po_nabl_gatepass.objects.filter(area_store=material).values('id')
            gp_id = data2[0]['id']
            
            return render(request, 'po/area_store/po_nabl_gatepass_resampling_print.html', {'data': material,'material':reject_item,'data1':data1,'gp_id':gp_id,'outward_qty':outward_qty})
        
        return render(request, 'po/area_store/po_nabl_resampling_gatepass.html', {'data': material,'material':reject_item,'outward_qty':outward_qty})
    return redirect('/')


def po_nabl_gatepass_print_resampling(request, id):
    store_name = Store_Info.objects.get(id=request.session['store'])
    material = DI_Areastores.objects.get(id=id)
    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)

    
    di_area_master_ids = [obj.id for obj in di_area_master]
            
    
    reject_item = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,area_store=store_name.Name,as_accepted=2)
    
    outward_qty = reject_item.count()

    gp_id = po_nabl_gatepass.objects.filter(area_store=material).latest('id')
    print("my_objects=============my_objects==========my_objects",gp_id)
    
    
    return render(request, 'po/area_store/po_nabl_gatepass_resampling_print2.html', {'data': material,'material':reject_item, 'data1':gp_id,'outward_qty':outward_qty})


def po_resampling_test_request_form_submit(request,id):
    material = DI_Areastores.objects.get(id=id)
    
    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
    
    trf = po_nabl_gatepass.objects.filter(area_store=material).distinct('area_store')
        
    print("trf================trf=====trf",trf)
    if request.method == "POST":
        
        gatepass_id = request.POST.get('gatepass_id')
        
        material = DI_Areastores.objects.get(id=id)
        # po_nabl_garepass = po_nabl_gatepass.objects.get(area_store=material)
        
        my_objects = po_nabl_gatepass.objects.filter(area_store=material)    
        
        
        po_nabl_garepass = my_objects.latest('area_store')
        
        # latest_obj_from_fk1 = my_object.fk1_related_objects.latest()

        my_objects = po_nabl_gatepass.objects.filter(area_store=material)
        latest_object = my_objects.latest('area_store')
        
        customer_Organization_name = request.POST.get('customer_Organization_name') #1
        customer_Organization_address = request.POST.get('customer_Organization_address') #2
        contact_person_name = request.POST.get('contact_person_name') #3
        contact_person_designation = request.POST.get('contact_person_designation') #4
        mobile_no = request.POST.get('mobile_no') #4
        email_id = request.POST.get('email_id') #5
        name_of_sample_product = request.POST.get('name_of_sample_product') #6
        customer_ref_gatepass_no = request.POST.get('customer_ref_gatepass_no') #7
        trf_file = request.POST.get('trf_file') #9


        trf_obj = PO_TRF_Details(areastore = material.areastore,area_store_id = material,
                              customer_Organization_name=customer_Organization_name, 
                              customer_Organization_address=customer_Organization_address,
                              contact_person_name=contact_person_name,
                              contact_person_designation=contact_person_designation,
                              mobile_no = mobile_no, email_id = email_id,
                              name_of_sample_product=name_of_sample_product,
                              customer_ref_gatepass_no=customer_ref_gatepass_no, 
                              trf_generated = 2, gatepass_doc=po_nabl_garepass)
        trf_obj.save()
       
        for i in di_area_master:
            i.nabl_trf = 2
            i.save()
        # trf_data = PO_TRF_Details.objects.get(area_store_id=material)
        trf_data = PO_TRF_Details.objects.filter(area_store_id=material).latest('TRF_Id')
        material.save()
        
        return render(request, 'po/area_store/po_Resampling_test_request_view.html', {'material': material,'trf':trf_data})

    return render(request, 'po/area_store/po_Resampling_test_request_form.html',{'material': material,'trf':trf})

def po_nabl_resampling_trf_upload(request, id):
    if request.method == "POST":
        trf_file = request.FILES['trf_file']
        data1 = PO_TRF_Details.objects.get(TRF_Id=id)
        print("data1=========data1========data1=========data1",data1)
        print("trf_file=========trf_file========trf_file=========trf_file",trf_file)
        
        data1.TRFAreastore_file = trf_file
        data1.save()
        return redirect('/po/po_trf_create')
    return redirect('/po/po_trf_create')

def po_resampling_nabl_update(request,id):
    material = DI_Areastores.objects.get(id=id)
    
    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
    for i in di_area_master:
        i.send_to_nabl = 2
        i.save()
    return redirect('/po/po_trf_create')
    
    
def po_nabl_items_resampling_result(request,id):
    if request.session.has_key('store'):
        store_name = Store_Info.objects.get(id=request.session['store'])
        
        material = DI_Areastores.objects.get(id=id)
    
        gatepass_obj = po_nabl_gatepass.objects.get(area_store = material)
                
        sample_obj_2 = sample_code_table_cp.objects.filter(Gatepass = gatepass_obj)
        
        sample_obj = sample_code_table_cp.objects.filter(Gatepass = gatepass_obj,outward_generated=2)
        
        return render(request, 'po/area_store/po_nabl_items_resampling_result.html',{'name':sample_obj})

    return redirect('/')    

##########################  PO Resampling End =========================================




###### handle logout ########

def handle_logout(request):
    it=request.session.items()
    
    # for i,j in it:
    #     print("jjjjjjjjj",i,j)

    # jt=request.session.keys()

    # for i in jt:
    #     print("jjjjjjjjj",i)
        
    request.session.flush()
    return redirect("/") 
