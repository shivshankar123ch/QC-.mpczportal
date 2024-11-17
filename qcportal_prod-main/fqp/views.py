from django.shortcuts import render,redirect
from main.models import *
from fqp.models import *
from tkc.models import *
from django.db import connection
import math

from main import constants as const
import time
from django.contrib import messages
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from django.core import validators
from django.conf import settings
from copy import deepcopy
import random
from django.db.models import Subquery
curl=settings.CURRENT_URL


from main import custom_message as cmsg
# Create your views here.




# wotask_id = 15953
# task_data=Wo_Order_Task.objects.filter(id=wotask_id).first()
# if task_data is not None:
#     ofc=Officer.objects.filter(Q(is_active=True,Region_id=task_data.region_id) & ((Q(role__Role_Name="WO_CREATER") | Q(role__Role_Name="WO_APPROVER")) | 
#     Q(role__Role_Name="GM(CIRCLE)",Circle_id=task_data.circle_id,Division_id__isnull=True,DC_Zone__isnull=True) | 
#     Q(role__Role_Name="DGM_ONM",Circle_id=task_data.circle_id,Division_id=task_data.division_id,DC_Zone_id__isnull=True) | 
#     Q(role__Role_Name="DGM_STC",Circle_id=task_data.circle_id,Division_id__isnull=True,DC_Zone_id__isnull=True) | 
#     (Q(role__Role_Name="PMA",Circle_id=task_data.circle_id) & (Q(Division_id__isnull=True,DC_Zone_id__isnull=True) | Q(Division_id=task_data.division_id,DC_Zone_id=task_data.distribution_center_id) | Q(Division_id=task_data.division_id,DC_Zone_id__isnull=True))) | 
#     Q(role__Role_Name="JE",Circle_id=task_data.circle_id,Division_id=task_data.division_id,DC_Zone=task_data.distribution_center_id)))
#     template_id = 1007605812683859871 
#     userdata = ofc
#     var1 = " " + str(task_data.gis_feeder_id) + " "
#     var2 = " " + str(task_data.wo.Header.Contract_Description) + " "
#     otherdata = ""
#     message_type = "FQP Intimation Creation"
#     cmsg.send_message(template_id,userdata,var1,var2,otherdata,message_type)#for send message when intimation created


def project_base(request):
    return render(request, 'projectSection/base.html')


def approver_base(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    return render(request, 'approver/base.html',{'officer':officer})


import json;
import requests as req
from requests.auth import HTTPBasicAuth


def search_wo(request):
    data = User_Registration.objects.filter(cgm_approval=1, User_type='TKC')
    return render(request, 'projectSection/search_wo.html', {"data": data})


def generate_wo(request):
    if request.method == "POST":
        request.session['Authentication_id'] = request.POST.get('vendor')
        request.session['po_no'] = request.POST.get('po_no')
        URL = " http://nprodap1.mpcz.in:8004/webservices/rest/qc_portal_get_po/get_po/"
        Username = 'QC_EBS_USER';
        Password = "Welcome123";
        data = {
            "register_vendor": {
                "@xmlns": "http://xmlns.oracle.com/apps/ap/rest/qc_portal_register_vendor/register_vendor/",
                "RESTHeader": {
                    "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
                    "Responsibility": "JAI_PAYABLES",
                    "RespApplication": "JA",
                    "SecurityGroup": "STANDARD",
                    "NLSLanguage": "AMERICAN",
                    "Org_Id": "82"
                },
                "InputParameters": {
                    "P_PO_NUMBER": request.POST.get('po_no'),
                    "P_PAN_CARD": User_Registration.objects.get(Authentication_id=request.POST.get('vendor')).Pancard

                }
            }
        }

        json_data = json.dumps(data)
        auth_values = HTTPBasicAuth(Username, Password)
        headers = {'Content-type': 'application/json'}
        res = req.post(url=URL, auth=auth_values, headers=headers, data=json_data)
        if res.status_code == 200:
            data = res.json()
            OutputParameters = data['OutputParameters']
            P_PO_RECORD = OutputParameters['P_PO_RECORD']
            if not P_PO_RECORD:
                P_ERRORS = OutputParameters['P_ERRORS']
                P_ERRORS_ITEM = P_ERRORS['P_ERRORS_ITEM']
                for P_ERRORS_ITEM in P_ERRORS_ITEM:
                    ERROR_MESSAGE = P_ERRORS_ITEM['ERROR_MESSAGE']
                    messages.warning(request, ERROR_MESSAGE)
                    data = User_Registration.objects.filter(cgm_approval=1, User_type='TKC')
                    return render(request, 'projectSection/search_wo.html', {"data": data})
            else:
                P_PO_RECORD_ITEM = P_PO_RECORD['P_PO_RECORD_ITEM']
                for data in P_PO_RECORD_ITEM:
                    R_HEADERS = data['R_HEADERS']
                    material = data['T_LINES']['T_LINES_ITEM']
                    # for data in data['T_LINES']['T_LINES_ITEM']:
                    #     print('11111111111', data['R_LINES']['ITEM'])
                    #     material.append(data)
                    #     for data in data['T_SHIPMENTS']['T_SHIPMENTS_ITEM']:
                    #         print('22222222222', data['R_SHIPMENTS']['SHIP_TO_ORG'])
                    #         for data in data['T_DISTRIBUTIONS']['T_DISTRIBUTIONS_ITEM']:
                    #             print('3333333333', data['RATE_DATE'])
                    print('jjjjjjjjjjjjjjjjjjj', request.session['Authentication_id'])
                    return render(request, 'projectSection/generate_wo.html', {'data': R_HEADERS, 'material': material})
    data = User_Registration.objects.filter(cgm_approval=1, User_type='TKC')
    return render(request, 'projectSection/generate_wo.html', {"data": data})


def generate_wo1(request):
    if request.method == "POST":
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        tendor = request.POST.get('tendor')
        nit = request.POST.get('nit')
        loa = request.POST.get('loa')
        user = User_Registration.objects.get(Authentication_id=request.session['Authentication_id'])
        if TKCWoInfo.objects.filter(erp_po_id=request.session['po_no']).exists():
            procurement = TKCWoInfo.objects.filter(erp_po_id=request.session['po_no'])
            print(request.session['po_no'])
            print('procurement', procurement)
            quantity = procurement[0].milestone
            return render(request, 'projectSection/generate_wo1.html',
                          {"procurement": procurement[0], 'quantity': range(int(quantity))})
        else:
            procurement = TKCWoInfo(tkc_id=user.Authentication_id, erp_po_id=request.session['po_no'],
                                    milestone=quantity, supplier=user,
                                    price=price, nit_no=nit, tendor_no=tendor, wo_no=loa, supplier_pan=user.Pancard)
            procurement.save()
            vd = TKCWoInfo.objects.latest('id')
            if len(request.FILES) != 0:
                upload_file = request.FILES['loa_file']
                vd.Loa = upload_file
                vd.save()
            tkc = User_Registration.objects.filter(Authentication_id=request.session['Authentication_id'])
            procurement = TKCWoInfo.objects.filter(id=vd.id)
            cdatetime = datetime.datetime.now().date()
            return render(request, 'projectSection/generate_wo1.html',
                          {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                           'quantity': range(int(quantity))})


from django import forms

from .forms import WorkForm


def generate_wo2(request, PO_id):
    if request.method == "POST":
        procurement = TKCWoInfo.objects.filter(id=PO_id)
        procurement_obj = TKCWoInfo.objects.get(id=PO_id)
        if TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj).exists():
            # counter = 100
            # id = 1000
            # for data in range(int(procurement[0].milestone)):
            #     print('jjjjjjjjjjjjjjjj', request.POST.get(str(id)))
            #     schedule = TKCScheduleInfo.objects.get(id = request.POST.get(str(id)))
            #     task = request.POST.get(str(data))
            #     if task != '':
            #         schedule.task = task
            #     percentage = request.POST.get(str(counter))
            #     if task != '':
            #         schedule.percentage = percentage
            #     schedule.save()
            #     counter = counter + 1
            #     id = id + 1
            tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
            cdatetime = datetime.datetime.now().date()
            data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
            form = WorkForm()
            return render(request, 'projectSection/generate_wo2.html',
                          {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                           'data': data, 'form': form})

        else:
            counter = 100
            for data in range(int(procurement[0].milestone)):
                task = request.POST.get(str(data))
                percentage = request.POST.get(str(counter))
                tkc = TKCScheduleInfo(TKCWoInfo=procurement_obj, phase=data + 1, percentage=percentage,
                                      task=task)
                tkc.save()
                counter = counter + 1
            tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
            cdatetime = datetime.datetime.now().date()
            data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
            form = WorkForm()
            return render(request, 'projectSection/generate_wo2.html',
                          {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                           'data': data, 'form': form})


def edit_wo3(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'projectSection/generate_wo2.html',
                  {"procurement": procurement_obj})


def generate_wo3(request, PO_id):
    if request.method == "POST":
        procurement = TKCWoInfo.objects.get(id=PO_id)
        form = WorkForm(request.POST, instance=procurement)
        if form.is_valid():
            form.save()
        procurement = TKCWoInfo.objects.filter(id=PO_id)
        procurement_obj = TKCWoInfo.objects.get(id=PO_id)
        tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
        URL = " http://nprodap1.mpcz.in:8004/webservices/rest/qc_portal_get_po/get_po/"
        Username = 'QC_EBS_USER';
        Password = "Welcome123";
        data = {
            "register_vendor": {
                "@xmlns": "http://xmlns.oracle.com/apps/ap/rest/qc_portal_register_vendor/register_vendor/",
                "RESTHeader": {
                    "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
                    "Responsibility": "JAI_PAYABLES",
                    "RespApplication": "JA",
                    "SecurityGroup": "STANDARD",
                    "NLSLanguage": "AMERICAN",
                    "Org_Id": "82"
                },
                "InputParameters": {
                    "P_PO_NUMBER": procurement_obj.erp_po_id,
                    "P_PAN_CARD": procurement_obj.supplier_pan
                }
            }
        }
        json_data = json.dumps(data)
        auth_values = HTTPBasicAuth(Username, Password)
        headers = {'Content-type': 'application/json'}
        res = req.post(url=URL, auth=auth_values, headers=headers, data=json_data)
        if res.status_code == 200:
            data = res.json()
            OutputParameters = data['OutputParameters']
            P_PO_RECORD = OutputParameters['P_PO_RECORD']
            if not P_PO_RECORD:
                P_ERRORS = OutputParameters['P_ERRORS']
                P_ERRORS_ITEM = P_ERRORS['P_ERRORS_ITEM']
                for P_ERRORS_ITEM in P_ERRORS_ITEM:
                    ERROR_MESSAGE = P_ERRORS_ITEM['ERROR_MESSAGE']
                    messages.warning(request, ERROR_MESSAGE)
                    data = User_Registration.objects.filter(cgm_approval=1, User_type='TKC')
                    return render(request, 'projectSection/search_wo.html', {"data": data})
            else:
                P_PO_RECORD_ITEM = P_PO_RECORD['P_PO_RECORD_ITEM']
                for data in P_PO_RECORD_ITEM:
                    R_HEADERS = data['R_HEADERS']
                    material = data['T_LINES']['T_LINES_ITEM']
                    print('okkkkkkkkkkkkkkkk', material)
                    # for data in data['T_LINES']['T_LINES_ITEM']:
                    #     print('11111111111', data['R_LINES']['ITEM'])
                    #     material.append(data)
                    #     for data in data['T_SHIPMENTS']['T_SHIPMENTS_ITEM']:
                    #         print('22222222222', data['R_SHIPMENTS']['SHIP_TO_ORG'])
                    #         for data in data['T_DISTRIBUTIONS']['T_DISTRIBUTIONS_ITEM']:
                    #             print('3333333333', data['RATE_DATE'])
                    cdatetime = datetime.datetime.now().date()
                    data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
                    return render(request, 'projectSection/view_wo.html',
                                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                                   'data': data, 'R_HEADERS': R_HEADERS, 'material': material})


def view_wo(request, PO_id):
    procurement = TKCWoInfo.objects.filter(id=PO_id)
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
    return render(request, 'projectSection/view_wo.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                   'data': data})


def all_wo(request):
    procurement = TKCWoInfo.objects.all().order_by('id')
    return render(request, 'projectSection/all_wo.html', {'data': procurement})


def approve_all_wo(request):
    procurement = TKCWoInfo.objects.filter(create_status=1).order_by('id')
    return render(request, 'approver/all_wo.html', {'data': procurement})


def tkc_all_purchase(request):
    tkc = TKCProcurementInfo.objects.all()
    return render(request, 'po/procurement_tkc_po1.html', {'tkc': tkc})


def tkc_tier1_inspection(request):
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'projectSection/tkc_tier1_Inspectin.html', {"officer": officer})


def tkc_tier2_inspection(request):
    officer = InspectingOfficerInfo.objects.all()
    return render(request, 'projectSection/tkc_tier2_inpection.html', {"officer": officer})


def upload_agreement(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'projectSection/upload_agreement.html', {'data': procurement_obj})


def upload_agreement_save(request, PO_id):
    if request.method == "POST":
        procurement_obj = TKCWoInfo.objects.get(id=PO_id)
        if len(request.FILES) != 0:
            upload_file = request.FILES['loa_file']
            procurement_obj.agreement = upload_file
            procurement_obj.save()
        procurement = TKCWoInfo.objects.all()
        return render(request, 'projectSection/all_wo.html', {'data': procurement})


def upload_loa(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'projectSection/upload_loa.html', {'data': procurement_obj})


def upload_loa_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.Loa = upload_file
        procurement_obj.save()
    procurement = TKCWoInfo.objects.all()
    return render(request, 'projectSection/all_wo.html', {'data': procurement})


# def wo_delete(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     procurement_obj.delete()
#     procurement = TKCWoInfo.objects.all().order_by('id')
#     return render(request, 'projectSection/all_wo.html', {'data': procurement})


def wo_approval(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    procurement_obj.create_status = 1
    procurement_obj.created_at = datetime.datetime.now()
    # procurement_obj.created_by = request.session['officer'].employ_name
    procurement_obj.save()
    procurement = TKCWoInfo.objects.all().order_by('id')
    return render(request, 'projectSection/all_wo.html', {'data': procurement})


# def wo_approved(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     return render(request, 'approver/upload_loa.html', {'data': procurement_obj})

def officersop(request):
    return render(request,'fqp/officersop/officersop.html')

def wo_approved_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.Loa = upload_file
        procurement_obj.save()
    procurement_obj.approve_status = 1
    procurement_obj.approve_remark = request.POST.get('remark')
    procurement_obj.approved_at = datetime.datetime.now()
    # procurement_obj.approved_by = request.session['officer'].employ_name
    procurement_obj.save()
    procurement = TKCWoInfo.objects.filter(create_status=1).order_by('id')
    return render(request, 'approver/all_wo.html', {'data': procurement})


def wo_rejected(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'approver/rejected_wo.html', {'data': procurement_obj})


def wo_rejected_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    procurement_obj.approve_status = -1
    procurement_obj.approve_remark = request.POST.get('remark')
    procurement_obj.approved_at = datetime.datetime.now()
    # procurement_obj.approved_by = request.session['officer'].employ_name
    procurement_obj.save()
    procurement = TKCWoInfo.objects.all(create_status=1).order_by('id')
    return render(request, 'approver/all_wo.html', {'data': procurement})


def all_bg(request):
    procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
    return render(request, 'projectSection/all_bg.html', {'data': procurement})


def all_bg_approval(request):
    procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
    return render(request, 'approver/all_bg.html', {'data': procurement})


def bg_view_approved(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'approver/bg_view.html', {'data': procurement_obj})


# def bg_approval(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     if request.method == "POST":
#         procurement_obj.Bg.review_remark = request.POST.get('remark')
#         procurement_obj.Bg.bg_review = 1
#         # procurement_obj.Bg.review_by = request.session['officer'].employ_name
#         procurement_obj.Bg.review_at = datetime.datetime.now()
#         procurement_obj.Bg.save()
#         procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
#         return render(request, 'approver/all_bg.html', {'data': procurement})
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     return render(request, 'approver/bg_approval.html', {'data': procurement_obj})


# def bank_approval(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     if request.method == "POST":
#         procurement_obj.Bg.approved_remark = request.POST.get('remark')
#         action = request.POST.get('action')
#         if action == 'OK':
#             procurement_obj.Bg.bg_approved = 1
#         else:
#             procurement_obj.Bg.bg_approved = -1
#         # procurement_obj.Bank.approved_by = request.session['officer'].employ_name
#         procurement_obj.Bg.approved_at = datetime.datetime.now()
#         procurement_obj.Bg.save()
#         procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
#         return render(request, 'approver/all_bg.html', {'data': procurement})
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     return render(request, 'approver/bank_approval.html', {'data': procurement_obj})


def all_pert_approval(request):
    procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
    return render(request, 'approver/all_pert.html', {'data': procurement})


#
# def pert_approval(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     if request.method == "POST":
#         procurement_obj.Pert.approved_remark = request.POST.get('remark')
#         action = request.POST.get('action')
#         if action == 'OK':
#             procurement_obj.Pert.pert_approved = 1
#         else:
#             procurement_obj.Pert.pert_approved = -1
#         # procurement_obj.Pert.approved_by = request.session['officer'].employ_name
#         procurement_obj.Pert.approved_at = datetime.datetime.now()
#         procurement_obj.Pert.save()
#         procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
#         return render(request, 'approver/all_pert.html', {'data': procurement})
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     return render(request, 'approver/pert_review.html', {'data': procurement_obj})


#
# def bg_approval_save(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     if request.method == "POST":
#         action = request.POST.get('action')
#         if action == 'OK':
#             procurement_obj.bg_approve = 1
#             procurement_obj.save()
#         else:
#             procurement_obj.bg_approve = -1
#             procurement_obj.bg_submit = 0
#             procurement_obj.save()
#     procurement = TKCWoInfo.objects.filter(bg_submit=1).order_by('id')
#     return render(request, 'projectSection/all_bg.html', {'data': procurement})


# def bg_approval(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     return render(request, 'projectSection/bg_approval.html', {'data': procurement_obj})


def bg_view(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'projectSection/bg_view.html', {'data': procurement_obj})


def bg_review(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if request.method == "POST":
        procurement_obj.Bg.review_remark = request.POST.get('remark')
        procurement_obj.Bg.bg_review = 1
        # procurement_obj.Bg.review_by = request.session['officer'].employ_name
        procurement_obj.Bg.review_at = datetime.datetime.now()
        procurement_obj.Bg.save()
        procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
        return render(request, 'projectSection/all_bg.html', {'data': procurement})
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'projectSection/bg_review.html', {'data': procurement_obj})


def bank_review(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if request.method == "POST":
        procurement_obj.Bank.review_remark = request.POST.get('remark')
        procurement_obj.Bank.bank_review = 1
        # procurement_obj.Bank.review_by = request.session['officer'].employ_name
        procurement_obj.Bank.review_at = datetime.datetime.now()
        procurement_obj.Bank.save()
        procurement = TKCWoInfo.objects.filter(Bank__bank_submit=1).order_by('id')
        return render(request, 'projectSection/all_bg.html', {'data': procurement})
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'projectSection/bank_review.html', {'data': procurement_obj})


def all_pert(request):
    procurement = TKCWoInfo.objects.filter(Pert__pert_submit=1).order_by('id')
    return render(request, 'projectSection/all_pert.html', {'data': procurement})


def pert_review(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if request.method == "POST":
        procurement_obj.Pert.review_remark = request.POST.get('remark')
        procurement_obj.Pert.pert_review = 1
        # procurement_obj.Pert.review_by = request.session['officer'].employ_name
        procurement_obj.Pert.review_at = datetime.datetime.now()
        procurement_obj.Pert.save()
        procurement = TKCWoInfo.objects.filter(Pert__pert_submit=1).order_by('id')
        return render(request, 'projectSection/all_pert.html', {'data': procurement})
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'projectSection/pert_review.html', {'data': procurement_obj})


def bg_approval_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'OK':
            procurement_obj.bg_approve = 1
            procurement_obj.save()
        else:
            procurement_obj.bg_approve = -1
            procurement_obj.bg_submit = 0
            procurement_obj.save()
    procurement = TKCWoInfo.objects.filter(bg_submit=1).order_by('id')
    return render(request, 'projectSection/all_bg.html', {'data': procurement})


def upload_schedule(request):
    return render(request, 'projectSection/upload_schedule.html')


def vendor_ins_approval(request):
    data = TKCWoInfo.objects.all()
    return render(request, 'projectSection/Vendor_approval.html', {"data": data})


def vendor_ins_approved(request, WO_id):
    wo = TKCWoInfo.objects.get(id=WO_id)
    data = TKCVendor.objects.filter(TKCWoInfo=wo, approval_submit=1)
    return render(request, 'projectSection/Vendor_approved.html', {"data": data})


def vendor_ins_approval_save(request, v_id):
    vendor = TKCVendor.objects.get(id=v_id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'OK':
            vendor.approval_approved = 1
            vendor.save()
        else:
            vendor.approval_approved = -1
            vendor.approval_submit = 0
            vendor.save()
    data = TKCVendor.objects.filter(TKCWoInfo=vendor.TKCWoInfo, approval_submit=1)
    return render(request, 'projectSection/Vendor_approved.html', {"data": data})


def vendor_ins_reject(request, v_id):
    vendor = TKCVendor.objects.get(id=v_id)
    vendor.status = -1
    vendor.save()
    data = TKCWoInfo.objects.all()
    return render(request, 'projectSection/Vendor_approval.html', {"data": data})


def all_pdi(request):
    data = TKCWoInfo.objects.all()
    return render(request, 'projectSection/all_pdi.html', {"data": data})


def all_material_offer(request):
    data = TKCWoInfo.objects.all()
    return render(request, 'projectSection/all_material_offer.html', {"data": data})


def material_offer(request, PO_id):
    wo = TKCWoInfo.objects.get(id=PO_id)
    data = TKCVendor.objects.filter(TKCWoInfo=wo, material_offer=1)
    return render(request, 'projectSection/material_offer.html', {"data": data})


def material_offer_approval_save(request, PO_id):
    vendor = TKCVendor.objects.get(id=PO_id)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'OK':
            vendor.offer_approved = 1
            vendor.save()
        else:
            vendor.offer_approved = -1
            vendor.material_offer = 0
            vendor.save()
    data = TKCWoInfo.objects.all()
    return render(request, 'projectSection/all_material_offer.html', {"data": data})


def pdi_schedule(request):
    data = TKCWoInfo.objects.all()
    return render(request, 'projectSection/all_pdi.html', {"data": data})


def pdi_schedule_set(request, PO_id):
    wo = TKCWoInfo.objects.get(id=PO_id)
    data = TKCVendor.objects.filter(TKCWoInfo=wo, material_offer=1)
    return render(request, 'projectSection/pdi.html', {"data": data})


# jeevan New code


import datetime
from django import forms
from django.contrib import messages
from .forms import WorkForm, Term_And_Condition


def procurement_Generate_WO(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    discom = Discom_Master.objects.get(Discom_Code=officer.user_zone)
    if request.method == "POST":
        vendor = User_Registration.objects.get(User_Id=int(request.POST.get('vendor')))
        work_obj = works_master.objects.get(id = int(request.POST.get('package')))
        if TKCWoInfo.objects.filter(Contract_Number=request.POST.get('contract_no'), Status=1).exists():
            wo = TKCWoInfo.objects.get(Contract_Number=request.POST.get('contract_no'), Status=1)
            if wo.Wo_Send_To_Approval_Status == 1:
                return render(request, 'fqp/wo_creater/creater_base.html', {'officer': officer})
            messages.add_message(request, messages.INFO, 'Work order already exists')
            Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo1.html',
                          {"officer": officer, 'wo': wo, 'Price': Price})
        wo = TKCWoInfo(supplier=vendor, Discom=discom, zone=officer.user_zone,
                       Contract_Number=request.POST.get('contract_no'),
                       Supplier_Erp_no=request.POST.get('Supplier_Erp_no'),
                       Contract_Date=request.POST.get('contract_date'),
                       Contract_Effective_Date=request.POST.get('contract_effective_date'),
                       Created_At=datetime.datetime.now(), Created_By=officer.employ_name, Status=1,pakage =work_obj )
        wo.save()
        wo = TKCWoInfo.objects.latest('id')
        wo_header = TKCWoInfo_Header(TKCWoInfo=wo, Scheme_code=request.POST.get('scheme_code'),
                                     Scheme_Name=request.POST.get('scheme_name'),
                                     Payment_Mode=request.POST.get('payment_mode'),
                                     Payment_Term=request.POST.get('payment_term'),
                                     Quotation_No=request.POST.get('quotation_no'),
                                     Contract_Offer_No=request.POST.get('contract_offer_no'),
                                     Contract_Offer_Date=request.POST.get('contract_offer_date'),
                                     Contract_Description=request.POST.get('order_description'),
                                     Nit_No=request.POST.get('nit_no'),
                                     Nit_Date=request.POST.get('nit_date'),
                                     Document_Sale_Open_Date=request.POST.get('Document_Sale_Open_Date'),
                                     Document_Sale_Closed_Date=request.POST.get('Document_Sale_Closed_Date'),
                                     Bid_Submission_Date=request.POST.get('Bid_Submission_Date'),
                                     Bid_Opening_Date=request.POST.get('Bid_Opening_Date'),
                                     WO_Prefix=request.POST.get('wo_prefix'),
                                     Created_At=datetime.datetime.now(), Created_By=officer.employ_name, Status=1)
        wo_header.save()
        wo.Header = TKCWoInfo_Header.objects.latest('id')
        wo.save()
        Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
        messages.add_message(request, messages.INFO, 'Work Order Created Successfully')
        return render(request, 'fqp/wo_creater/generate_wo1.html',
                      {"officer": officer, 'wo': wo, 'Price': Price})
    vendor = User_Registration.objects.filter(User_type='TKC', cgm_approval=1)
    package_data = works_master.objects.all()
    payment_mode = Payment_Mode_Master.objects.filter(Status=1)
    return render(request, 'fqp/wo_creater/generate_wo.html',
                  {"officer": officer, 'vendor': vendor, 'payment_mode': payment_mode,'package_data':package_data})


def procurement_Generate_WO1(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Item_Name=request.POST.get('item'),
                                                   Amount=request.POST.get('amount'), Status=1).exists():
            Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
            messages.add_message(request, messages.INFO, 'Item Already Exists')
            return render(request, 'fqp/wo_creater/generate_wo1.html',
                          {"officer": officer, 'wo': wo, 'Price': Price})
        price = TKCWoInfo_Contract_Price(TKCWoInfo=wo, Item_Name=request.POST.get('item'),
                                         Amount=request.POST.get('amount'), Created_At=datetime.datetime.now(),
                                         Created_By=officer.employ_name, Status=1)
        price.save()
        messages.add_message(request, messages.INFO, 'Item Save')
        Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo1.html',
                      {"officer": officer, 'wo': wo, 'Price': Price})
    messages.add_message(request, messages.INFO, 'Item Found')
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo1.html',
                  {"officer": officer, 'wo': wo, 'Price': Price})


def delete_amount(request, id, amount_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Contract_Price.objects.filter(id=amount_id, Status=1).exists():
        price = TKCWoInfo_Contract_Price.objects.get(id=amount_id, Status=1)
        price.Status = -1
        price.save()
        messages.add_message(request, messages.INFO, 'Item Deleted')
    messages.add_message(request, messages.INFO, 'Item Not Found')
    Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo1.html',
                  {"officer": officer, 'wo': wo, 'Price': Price})


def procurement_Generate_WO2(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Name=request.POST.get('item'),
                                            Status=1).exists():
            type = TKCWoInfo_Advance_Type.objects.filter(Status=1)
            Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo2.html',
                          {"officer": officer, 'wo': wo, 'Advance': Advance, 'type': type})
        Advance = TKCWoInfo_Advance(TKCWoInfo=wo, Name=request.POST.get('item'),
                                    Amount_Percentage=request.POST.get('amount'), Created_At=datetime.datetime.now(),
                                    Created_By=officer.employ_name, Status=1)
        Advance.save()
        type = TKCWoInfo_Advance_Type.objects.filter(Status=1)
        Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo2.html',
                      {"officer": officer, 'wo': wo, 'Advance': Advance, 'type': type})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    type = TKCWoInfo_Advance_Type.objects.filter(Status=1)
    Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo2.html',
                  {"officer": officer, 'wo': wo, 'Advance': Advance, 'type': type})


def delete_advance(request, id, amount_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Advance.objects.filter(id=amount_id, Status=1).exists():
        Advance = TKCWoInfo_Advance.objects.get(id=amount_id, Status=1)
        Advance.Status = -1
        Advance.save()
    type = TKCWoInfo_Advance_Type.objects.filter(Status=1)
    Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo2.html',
                  {"officer": officer, 'wo': wo, 'Advance': Advance, 'type': type})


def procurement_Generate_WO3(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Stage=request.POST.get('Stage'), Status=1).exists():
            Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
            messages.add_message(request, messages.INFO, 'Item Exists')
            return render(request, 'fqp/wo_creater/generate_wo3.html',
                          {"officer": officer, 'wo': wo, 'Time': Time})
        Advance = TKCWoInfo_Time_Schedule(TKCWoInfo=wo, Stage=request.POST.get('Stage'),
                                          Month=request.POST.get('Month'), Days=request.POST.get('Day'),
                                          Completion_date=request.POST.get('Completion_date'),
                                          Contract_Amount_Percentage=request.POST.get('Contract_Amount_Percentage'),
                                          Stage_Amount=request.POST.get('Stage_Amount'),
                                          Remarks=request.POST.get('Remarks'), Created_At=datetime.datetime.now(),
                                          Created_By=officer.employ_name, Status=1)
        Advance.save()
        messages.add_message(request, messages.INFO, 'Item Save')
        Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo3.html',
                      {"officer": officer, 'wo': wo, 'Time': Time})
    messages.add_message(request, messages.INFO, 'Item Found')
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo3.html',
                  {"officer": officer, 'wo': wo, 'Time': Time})


def delete_time(request, id, time_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Time_Schedule.objects.filter(id=time_id, Status=1).exists():
        Advance = TKCWoInfo_Time_Schedule.objects.get(id=time_id, Status=1)
        Advance.Status = -1
        Advance.save()
        messages.add_message(request, messages.INFO, 'Item Deleted')
    else:
        messages.add_message(request, messages.INFO, 'Item Not Found')
    Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo3.html',
                  {"officer": officer, 'wo': wo, 'Time': Time})


def procurement_Generate_WO4(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Schedule_No=request.POST.get('Schedule_No'),
                                                    Status=1).exists():
            UOM = UOM_Master.objects.filter(Status=1)
            Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo4.html',
                          {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})
        Supply = TKCWoInfo_Schedule_Supply(TKCWoInfo=wo, Schedule_No=request.POST.get('Schedule_No'),
                                           Schedule_Description=request.POST.get('Schedule_Description'),
                                           Unit=request.POST.get('Unit'),
                                           Quantity=request.POST.get('Quantity'),
                                           Unit_Price_With_Tax=request.POST.get('Unit_Price_With_Tax'),
                                           Created_At=datetime.datetime.now(),
                                           Created_By=officer.employ_name, Status=1)
        Supply.save()
        UOM = UOM_Master.objects.filter(Status=1)
        Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo4.html',
                      {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    UOM = UOM_Master.objects.filter(Status=1)
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo4.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})


def delete_schedule_supply(request, id, schedule_supply_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Schedule_Supply.objects.filter(id=schedule_supply_id, Status=1).exists():
        Advance = TKCWoInfo_Schedule_Supply.objects.get(id=schedule_supply_id, Status=1)
        Advance.Status = -1
        Advance.save()
    UOM = UOM_Master.objects.filter(Status=1)
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo4.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})


def procurement_Generate_WO5(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Schedule_No=request.POST.get('Schedule_No'),
                                                          Status=1).exists():
            UOM = UOM_Master.objects.filter(Status=1)
            Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo5.html',
                          {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})
        Supply = TKCWoInfo_Schedule_Installation(TKCWoInfo=wo, Schedule_No=request.POST.get('Schedule_No'),
                                                 Schedule_Description=request.POST.get('Schedule_Description'),
                                                 Unit=request.POST.get('Unit'),
                                                 Quantity=request.POST.get('Quantity'),
                                                 Unit_Price_With_Tax=request.POST.get('Unit_Price_With_Tax'),
                                                 Created_At=datetime.datetime.now(),
                                                 Created_By=officer.employ_name, Status=1)
        Supply.save()
        UOM = UOM_Master.objects.filter(Status=1)
        Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo5.html',
                      {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    UOM = UOM_Master.objects.filter(Status=1)
    Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo5.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})


def delete_schedule_install(request, id, schedule_install_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Schedule_Installation.objects.filter(id=schedule_install_id, Status=1).exists():
        Advance = TKCWoInfo_Schedule_Installation.objects.get(id=schedule_install_id, Status=1)
        Advance.Status = -1
        Advance.save()
    UOM = UOM_Master.objects.filter(Status=1)
    Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo5.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM})


def procurement_Generate_WO6(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Schedule_Supply_Item.objects.filter(
                Schedule_Supply=TKCWoInfo_Schedule_Supply.objects.get(id=request.POST.get('Schedule_Supply')),
                Item_Code=request.POST.get('Item_Code'),
                Status=1).exists():
            UOM = UOM_Master.objects.filter(Status=1)
            Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1)
            Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo6.html',
                          {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})
        Supply = TKCWoInfo_Schedule_Supply_Item(
            TKCWoInfo = wo,
            Schedule_Supply=TKCWoInfo_Schedule_Supply.objects.get(id=request.POST.get('Schedule_Supply')),
            Item_Description=request.POST.get('Item_Description'),
            Item_Code=request.POST.get('Item_Code'),
            Unit=request.POST.get('Unit'),
            Quantity=request.POST.get('Quantity'),
            Unit_Price_With_Tax=request.POST.get('Unit_Price_With_Tax'),
            Created_At=datetime.datetime.now(),
            Created_By=officer.employ_name, Status=1)
        Supply.save()
        UOM = UOM_Master.objects.filter(Status=1)
        Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1)
        Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo6.html',
                      {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    UOM = UOM_Master.objects.filter(Status=1)
    Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1)
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo6.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})


def delete_schedule_supply_item(request, id, schedule_install_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Schedule_Supply_Item.objects.filter(id=schedule_install_id, Status=1).exists():
        Advance = TKCWoInfo_Schedule_Supply_Item.objects.get(id=schedule_install_id, Status=1)
        Advance.Status = -1
        Advance.save()
    UOM = UOM_Master.objects.filter(Status=1)
    Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1)
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo6.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})


def procurement_Generate_WO7(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Schedule_Installation_Item.objects.filter(
                Schedule_Installation=TKCWoInfo_Schedule_Installation.objects.get(
                    id=request.POST.get('Schedule_Supply')),
                Item_Code=request.POST.get('Item_Code'),
                Status=1).exists():
            UOM = UOM_Master.objects.filter(Status=1)
            Supply_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo,
                                                                              Status=1)
            Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo7.html',
                          {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})
        Supply = TKCWoInfo_Schedule_Installation_Item(
            TKCWoInfo = wo,
            Schedule_Installation=TKCWoInfo_Schedule_Installation.objects.get(id=request.POST.get('Schedule_Supply')),
            Item_Description=request.POST.get('Item_Description'),
            Item_Code=request.POST.get('Item_Code'),
            Unit=request.POST.get('Unit'),
            Quantity=request.POST.get('Quantity'),
            Unit_Price_With_Tax=request.POST.get('Unit_Price_With_Tax'),
            Created_At=datetime.datetime.now(),
            Created_By=officer.employ_name, Status=1)
        Supply.save()
        UOM = UOM_Master.objects.filter(Status=1)
        Supply_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo, Status=1)
        Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo7.html',
                      {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    UOM = UOM_Master.objects.filter(Status=1)
    Supply_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo, Status=1)
    Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo7.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})


def delete_schedule_install_item(request, id, schedule_install_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Schedule_Installation_Item.objects.filter(id=schedule_install_id, Status=1).exists():
        Advance = TKCWoInfo_Schedule_Installation_Item.objects.get(id=schedule_install_id, Status=1)
        Advance.Status = -1
        Advance.save()
    UOM = UOM_Master.objects.filter(Status=1)
    Supply_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo, Status=1)
    Supply = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo7.html',
                  {"officer": officer, 'wo': wo, 'Supply': Supply, 'UOM': UOM, 'Supply_Item': Supply_Item})


def procurement_Generate_WO8(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Major_Item.objects.filter(TKCWoInfo=wo,
                                               Item_Code=request.POST.get('Item_Code'),
                                               Status=1).exists():
            UOM = UOM_Master.objects.filter(Status=1)
            Major_Item = TKCWoInfo_Major_Item.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo8.html',
                          {"officer": officer, 'wo': wo, 'UOM': UOM, 'Major_Item': Major_Item})
        Supply = TKCWoInfo_Major_Item(TKCWoInfo=wo,
                                      Item_Description=request.POST.get('Item_Description'),
                                      Item_Code=request.POST.get('Item_Code'),
                                      Unit=request.POST.get('Unit'),
                                      Quantity=request.POST.get('Quantity'),
                                      Unit_Price_With_Tax=request.POST.get('Unit_Price_With_Tax'),
                                      Created_At=datetime.datetime.now(),
                                      Created_By=officer.employ_name, Status=1)
        Supply.save()
        UOM = UOM_Master.objects.filter(Status=1)
        Major_Item = TKCWoInfo_Major_Item.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo8.html',
                      {"officer": officer, 'wo': wo, 'UOM': UOM, 'Major_Item': Major_Item})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    UOM = UOM_Master.objects.filter(Status=1)
    Major_Item = TKCWoInfo_Major_Item.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo8.html',
                  {"officer": officer, 'wo': wo, 'UOM': UOM, 'Major_Item': Major_Item})


def delete_major_item(request, id, schedule_install_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Major_Item.objects.filter(id=schedule_install_id, Status=1).exists():
        Advance = TKCWoInfo_Major_Item.objects.get(id=schedule_install_id, Status=1)
        Advance.Status = -1
        Advance.save()
    UOM = UOM_Master.objects.filter(Status=1)
    Major_Item = TKCWoInfo_Major_Item.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo8.html',
                  {"officer": officer, 'wo': wo, 'UOM': UOM, 'Major_Item': Major_Item})


def procurement_Generate_WO9(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id, Status=1)
        if TKCWoInfo_Variable_Item.objects.filter(TKCWoInfo=wo,
                                                  Item_Code=request.POST.get('Item_Code'),
                                                  Status=1).exists():
            UOM = UOM_Master.objects.filter(Status=1)
            Variable_Item = TKCWoInfo_Variable_Item.objects.filter(TKCWoInfo=wo, Status=1)
            return render(request, 'fqp/wo_creater/generate_wo9.html',
                          {"officer": officer, 'wo': wo, 'UOM': UOM, 'Variable_Item': Variable_Item})
        Supply = TKCWoInfo_Variable_Item(TKCWoInfo=wo,
                                         Item_Description=request.POST.get('Item_Description'),
                                         Item_Code=request.POST.get('Item_Code'),
                                         Unit=request.POST.get('Unit'),
                                         Quantity=request.POST.get('Quantity'),
                                         Unit_Price_With_Tax=request.POST.get('Unit_Price_With_Tax'),
                                         Created_At=datetime.datetime.now(),
                                         Created_By=officer.employ_name, Status=1)
        Supply.save()
        UOM = UOM_Master.objects.filter(Status=1)
        Variable_Item = TKCWoInfo_Variable_Item.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo9.html',
                      {"officer": officer, 'wo': wo, 'UOM': UOM, 'Variable_Item': Variable_Item})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    UOM = UOM_Master.objects.filter(Status=1)
    Variable_Item = TKCWoInfo_Variable_Item.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo9.html',
                  {"officer": officer, 'wo': wo, 'UOM': UOM, 'Variable_Item': Variable_Item})


def delete_variable_item(request, id, schedule_install_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Variable_Item.objects.filter(id=schedule_install_id, Status=1).exists():
        Advance = TKCWoInfo_Variable_Item.objects.get(id=schedule_install_id, Status=1)
        Advance.Status = -1
        Advance.save()
    UOM = UOM_Master.objects.filter(Status=1)
    Variable_Item = TKCWoInfo_Variable_Item.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo9.html',
                  {"officer": officer, 'wo': wo, 'UOM': UOM, 'Variable_Item': Variable_Item})


# def procurement_Generate_WO10(request, id):
#     officer = Officer.objects.get(employ_id=request.session['employ_id'])
#     if request.method == "POST":
#         wo = TKCWoInfo.objects.get(id=id, Status=1)
#         form = Term_And_Condition(request.POST, instance=wo)
#         if form.is_valid():
#             form.save()
#         copy_to = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
#         return render(request, 'fqp/wo_creater/generate_wo11.html',
#                       {"officer": officer, 'wo': wo, 'copy_to': copy_to})
#     wo = TKCWoInfo.objects.get(id=id, Status=1)
#     form = Term_And_Condition()
#     return render(request, 'fqp/wo_creater/generate_wo10.html',
#                   {"officer": officer, 'wo': wo, 'form': form})



#updated code for manual and Integration process:-giving provision of t&c to user in manual and automated gbpa process
def procurement_Generate_WO10(request, id,message_rendered=None):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if message_rendered == 'True' and request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id)
        form = Term_And_Condition(request.POST, instance=wo)
        if form.is_valid():
            form.save()
        # copy_to = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
        copy_to = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo)
        message_rendered = False
        message =messages.info(request, f'Please add copy-to details')
        return render(request, 'fqp/wo_creater/generate_wo11.html',
        {"officer": officer, 'wo': wo, 'copy_to': copy_to,'message_rendered':message_rendered})
    
    elif request.method == "POST":
        # wo = TKCWoInfo.objects.get(id=id, Status=1)
        wo = TKCWoInfo.objects.get(id=id)
        form = Term_And_Condition(request.POST, instance=wo)
        if form.is_valid():
            form.save()
        copy_to = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
        return render(request, 'fqp/wo_creater/generate_wo11.html',
                      {"officer": officer, 'wo': wo, 'copy_to': copy_to})
    
    wo = TKCWoInfo.objects.get(id=id)
    # wo = TKCWoInfo.objects.get(id=id, Status=1)
    form = Term_And_Condition()
    return render(request, 'fqp/wo_creater/generate_wo10.html',
                {"officer": officer, 'wo': wo, 'form': form,'message_rendered':message_rendered})


# def procurement_Generate_WO11(request, id):
#     officer = Officer.objects.get(employ_id=request.session['employ_id'])
#     if request.method == "POST":
#         wo = TKCWoInfo.objects.get(id=id, Status=1)
#         if TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo,
#                                             Copy_To=request.POST.get('Copy_To'),
#                                             Copy_To_URL=request.POST.get('Copy_To_URL'),
#                                             Status=1).exists():
#             Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
#             return render(request, 'fqp/wo_creater/generate_wo11.html',
#                           {"officer": officer, 'wo': wo, 'Copy_To': Copy_To})
#         Supply = TKCWoInfo_Copy_To(TKCWoInfo=wo,
#                                    Copy_To=request.POST.get('Copy_To'),
#                                    Copy_To_URL=request.POST.get('Copy_To_URL'),
#                                    Created_At=datetime.datetime.now(),
#                                    Created_By=officer.employ_name, Status=1)
#         Supply.save()
#         Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
#         return render(request, 'fqp/wo_creater/generate_wo11.html',
#                       {"officer": officer, 'wo': wo, 'Copy_To': Copy_To})
#     wo = TKCWoInfo.objects.get(id=id, Status=1)
#     Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
#     return render(request, 'fqp/wo_creater/generate_wo11.html',
#                   {"officer": officer, 'wo': wo, 'Copy_To': Copy_To})



#updated code for manual and Integration process:-giving provision of copy_to to user in manual and automated gbpa process
def procurement_Generate_WO11(request, id,message_rendered=None):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if message_rendered == True and request.method == "POST":
        Supply = TKCWoInfo_Copy_To(TKCWoInfo=wo,
                                   Copy_To=request.POST.get('Copy_To'),
                                   Copy_To_URL=request.POST.get('Copy_To_URL'),
                                   Created_At=datetime.datetime.now(),
                                   Created_By=officer.employ_name, Status=1)
        Supply.save()
        # Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
        Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo)
        return render(request, 'fqp/wo_creater/generate_wo11.html',
                      {"officer": officer, 'wo': wo, 'Copy_To': Copy_To,'message_rendered':message_rendered})
    
    if request.method == "POST":
        # wo = TKCWoInfo.objects.get(id=id, Status=1)
        wo = TKCWoInfo.objects.get(id=id)
        if TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo,
                                            Copy_To=request.POST.get('Copy_To'),
                                            Copy_To_URL=request.POST.get('Copy_To_URL'),
                                            Status=1).exists():
            # Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
            Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo)
            return render(request, 'fqp/wo_creater/generate_wo11.html',
                          {"officer": officer, 'wo': wo, 'Copy_To': Copy_To})
        Supply = TKCWoInfo_Copy_To(TKCWoInfo=wo,
                                   Copy_To=request.POST.get('Copy_To'),
                                   Copy_To_URL=request.POST.get('Copy_To_URL'),
                                   Created_At=datetime.datetime.now(),
                                   Created_By=officer.employ_name, Status=1)
        Supply.save()
        # Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
        Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo)
        return render(request, 'fqp/wo_creater/generate_wo11.html',
                      {"officer": officer, 'wo': wo, 'Copy_To': Copy_To})
    
    # wo = TKCWoInfo.objects.get(id=id, Status=1)
    wo = TKCWoInfo.objects.get(id=id)
    # Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
    Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo)
    return render(request, 'fqp/wo_creater/generate_wo11.html',
                  {"officer": officer, 'wo': wo, 'Copy_To': Copy_To})



def delete_copy_to(request, id, schedule_install_id):
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if TKCWoInfo_Copy_To.objects.filter(id=schedule_install_id, Status=1).exists():
        Advance = TKCWoInfo_Copy_To.objects.get(id=schedule_install_id, Status=1)
        Advance.Status = -1
        Advance.save()
    Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
    return render(request, 'fqp/wo_creater/generate_wo11.html',
                  {"officer": officer, 'wo': wo, 'Copy_To': Copy_To})


def wo_view(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        procurement = Purchase_Order.objects.get(id=id)
        copy = PO_Copy(po=procurement, copy=request.POST.get('copy_name'))
        copy.save()
        copy = PO_Copy.objects.filter(po=procurement)
        vendor = User_Registration.objects.filter(User_type='VENDOR', cgm_approval=1, User_zone=officer.user_zone)
        return render(request, 'po/po_creater/procurement_generate_po4.html',
                      {"officer": officer, 'vendor': vendor, 'po': procurement, 'copy': copy})
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    Header = TKCWoInfo_Header.objects.filter(TKCWoInfo=wo, Status=1)
    Company = UserCompanyDataMain.objects.get(user_id_id=wo.supplier)
    Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
    Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
    Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
    Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1)
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    Install_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo, Status=1)
    Install = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    Major_Item = TKCWoInfo_Major_Item.objects.filter(TKCWoInfo=wo, Status=1)
    Variable_Item = TKCWoInfo_Variable_Item.objects.filter(TKCWoInfo=wo, Status=1)
    Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
    total_loa_amount = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1).aggregate(Sum("Amount"))
    total_amount= total_loa_amount['Amount__sum']
    wo.loa_amount = total_amount
    wo.save()

    query = f'''SELECT "Item_Code", sum("Quantity") FROM public.fqp_tkcwoinfo_schedule_supply_item where "TKCWoInfo_id" = {id} group by "Item_Code"'''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()

    for i in row:        
         Supply_Item_name = TKCWoInfo_Schedule_Supply_Item.objects.filter(Item_Code =i[0])
         for j in Supply_Item_name:
                item_name = j.Item_Description
                unit_name = j.Unit
                if tkc_wo_items_boq.objects.filter(wo =id , item_code = i[0]).exists():
                    pass
                else:    
                    boq_save = tkc_wo_items_boq(wo =wo , material_name = item_name, item_code = i[0],total_order_qty = i[1],balance_qty = i[1],uom=unit_name)
                    boq_save.save()

    return render(request, 'fqp/wo_creater/wo_view.html',
                  {"officer": officer, 'wo': wo, 'Header': Header, 'Company': Company, 'Time': Time, 'Price': Price,
                   "Advance": Advance, 'Supply_Item': Supply_Item, 'Supply': Supply, 'Install_Item': Install_Item,
                   'Install': Install, 'Major_Item': Major_Item, 'Install': Install, 'Variable_Item': Variable_Item,
                   'Copy_To': Copy_To})


def send_to_approval(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id)
    wo.Wo_Send_To_Approval_Status = 1
    wo.Wo_Send_To_Approval_At = datetime.datetime.now().date()
    wo.Wo_Send_To_Approval_By = officer.employ_name
    wo.Status = 1
    wo.save()
    vendor = User_Registration.objects.filter(User_type='TKC', cgm_approval=1, User_zone=officer.user_zone)
    payment_mode = Payment_Mode_Master.objects.filter(Status=1)
    messages.add_message(request, messages.INFO, 'Work order Send Successfully for Approval')
    return render(request, 'fqp/wo_creater/generate_wo.html',
                  {"officer": officer, 'vendor': vendor, 'payment_mode': payment_mode})


def wo_delete(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id)
    wo.Deleted_At = datetime.datetime.now().date()
    wo.Deleted_By = officer.employ_name
    wo.Status = -1
    wo.save()
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone)
    return render(request, 'fqp/wo_creater/work_order.html',
                  {"officer": officer, 'wo': wo})


def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request, 'main/mpeb_reg.html')


def procurement_previous_wo(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone).order_by('-id')
    return render(request, 'fqp/wo_creater/work_order.html',
                  {"officer": officer, 'wo': wo})


def wo_upload_agreement_copy(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id)
        wo.Wo_Agreement = request.FILES['digital']
        wo.Wo_Agreement_Upload_Status = 1
        wo.Wo_Agreement_Upload_At = datetime.datetime.now().date()
        wo.Wo_Agreement_Upload_By = officer.employ_name
        wo.save()
        wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone)
        return render(request, 'fqp/wo_creater/work_order.html',
                      {"officer": officer, 'wo': wo})
    wo = TKCWoInfo.objects.get(id=id)
    return render(request, 'fqp/wo_creater/wo_agreement_upload.html',
                  {"officer": officer, 'wo': wo})


def bank_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if BankDetails.objects.filter(Bank_Id=wo_id, Status=1).exists():
            Advance = BankDetails.objects.get(Bank_Id=wo_id, Status=1)
            print('Advance',Advance)
            if int(request.POST.get('action')):
                Advance.bank_approved = 1
            else:
                Advance.bank_approved = -1
            Advance.approved_remark = request.POST.get('remark')
            Advance.approved_at = datetime.datetime.now().date()
            Advance.approved_by = officer.employ_name
            Advance.save()
            # wo = TKCWoInfo.objects.filter()
            Bank = BankDetails.objects.filter(user_id=Advance.user_id, bank_submit=1, Status=1)
            return render(request, 'fqp/wo_creater/approve_bank.html', {"officer": officer, 'Bank': Bank})
    wo = TKCWoInfo.objects.get(id=wo_id)
    Bank = BankDetails.objects.filter(user_id=wo.supplier.User_Id, bank_submit=1, Status=1)
    return render(request, 'fqp/wo_creater/approve_bank.html', {"officer": officer, 'wo': wo, 'Bank': Bank})


def bg_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if TKCWoInfo_Bg.objects.filter(id=wo_id, Status=1).exists():
            Advance = TKCWoInfo_Bg.objects.get(id=wo_id, Status=1)
            if int(request.POST.get('action')):
                Advance.BG_Approved_Status = 1
            else:
                Advance.BG_Approved_Status = -1
            Advance.BG_Approved_Remark = request.POST.get('remark')
            # Advance.BG_Approved_copy = request.FILES[wo_id]
            Advance.BG_Approved_At = datetime.datetime.now().date()
            Advance.BG_Approved_By = officer.employ_name
            Advance.save()
            BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=Advance.TKCWoInfo, BG_Submit=1, Status=1)
            return render(request, 'fqp/wo_creater/approve_bg.html', {"officer": officer,'BG': BG})
    wo = TKCWoInfo.objects.get(id=wo_id)
    BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=wo, BG_Submit=1, Status=1)
    return render(request, 'fqp/wo_creater/approve_bg.html', {"officer": officer, 'wo': wo, 'BG': BG})


def loc_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if TKCWoInfo_LOC.objects.filter(id=wo_id, Status=1).exists():
            Advance = TKCWoInfo_LOC.objects.get(id=wo_id, Status=1)
            if int(request.POST.get('action')):
                Advance.LOC_Approved_Status = 1
            else:
                Advance.LOC_Approved_Status = -1
            Advance.LOC_Approved_Remark = request.POST.get('remark')
            Advance.LOC_Approved_At = datetime.datetime.now().date()
            Advance.LOC_Approved_By = officer.employ_name
            Advance.save()
            LOC = TKCWoInfo_LOC.objects.filter(TKCWoInfo=Advance.TKCWoInfo, LOC_Submit=1, Status=1)
            return render(request, 'fqp/wo_creater/approve_loc.html', {"officer": officer,'LOC': LOC})
    wo = TKCWoInfo.objects.get(id=wo_id)
    LOC = TKCWoInfo_LOC.objects.filter(TKCWoInfo=wo, LOC_Submit=1, Status=1)
    return render(request, 'fqp/wo_creater/approve_loc.html', {"officer": officer, 'wo': wo, 'LOC': LOC})


def pert_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if TKCWoInfo_Pert.objects.filter(id=wo_id, Status=1).exists():
            Advance = TKCWoInfo_Pert.objects.get(id=wo_id, Status=1)
            if int(request.POST.get('action')):
                Advance.Pert_Approved_Status = 1
            else:
                Advance.Pert_Approved_Status = -1
            Advance.Pert_Approved_Remark = request.POST.get('remark')
            Advance.Pert_Approved_At = datetime.datetime.now().date()
            Advance.Pert_Approved_By = officer.employ_name
            Advance.save()
            Pert = TKCWoInfo_Pert.objects.filter(TKCWoInfo=Advance.TKCWoInfo, Pert_Submit=1, Status=1)
            return render(request, 'fqp/wo_creater/approve_pert.html', {"officer": officer,'Pert': Pert})
    wo = TKCWoInfo.objects.get(id=wo_id)
    Pert = TKCWoInfo_Pert.objects.filter(TKCWoInfo=wo, Pert_Submit=1, Status=1)
    return render(request, 'fqp/wo_creater/approve_pert.html', {"officer": officer, 'wo': wo, 'Pert': Pert})


def mqpdoc_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if TKC_MqpPlanDocuments.objects.filter(id=wo_id, status=1).exists():
            Advance = TKC_MqpPlanDocuments.objects.get(id=wo_id, status=1)
            if int(request.POST.get('action')):
                Advance.mqpdoc_approved_status = 1
            else:
                Advance.mqpdoc_approved_status = -1
            Advance.mqpdoc_approved_remark = request.POST.get('remark')
            Advance.mqpdoc_approved_at = datetime.datetime.now().date()
            Advance.mqpdoc_approved_by = officer.employ_name
            Advance.save()
            mqpdoc = TKC_MqpPlanDocuments.objects.filter(tkcwoinfo=Advance.tkcwoinfo, mqpdoc_submit=1, status=1)
            return render(request, 'fqp/wo_creater/approve_mqpdoc.html', {"officer": officer,'mqpdoc': mqpdoc})
    wo = TKCWoInfo.objects.get(id=wo_id)
    mqpdoc = TKC_MqpPlanDocuments.objects.filter(tkcwoinfo=wo, mqpdoc_submit=1, status=1)
    return render(request, 'fqp/wo_creater/approve_mqpdoc.html', {"officer": officer, 'wo': wo, 'mqpdoc': mqpdoc})



def fqpdoc_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if TKC_FqpPlanDocuments.objects.filter(id=wo_id, status=1).exists():
            Advance = TKC_FqpPlanDocuments.objects.get(id=wo_id, status=1)
            if int(request.POST.get('action')):
                Advance.fqpdoc_approved_status = 1
            else:
                Advance.fqpdoc_approved_status = -1
            Advance.fqpdoc_approved_remark = request.POST.get('remark')
            Advance.fqpdoc_approved_at = datetime.datetime.now().date()
            Advance.fqpdoc_approved_by = officer.employ_name
            Advance.save()
            fqpdoc = TKC_FqpPlanDocuments.objects.filter(tkcwoinfo=Advance.tkcwoinfo, fqpdoc_submit=1, status=1)
            return render(request, 'fqp/wo_creater/approve_fqpdoc.html', {"officer": officer,'fqpdoc': fqpdoc})
    wo = TKCWoInfo.objects.get(id=wo_id)
    fqpdoc = TKC_FqpPlanDocuments.objects.filter(tkcwoinfo=wo, fqpdoc_submit=1, status=1)
    return render(request, 'fqp/wo_creater/approve_fqpdoc.html', {"officer": officer, 'wo': wo, 'fqpdoc': fqpdoc})

    
def otherdoc_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if TKCOtherDocuments.objects.filter(id=wo_id, status=1).exists():
            Advance = TKCOtherDocuments.objects.get(id=wo_id, status=1)
            if int(request.POST.get('action')):
                Advance.otherdoc_approved_status = 1
            else:
                Advance.otherdoc_approved_status = -1
            Advance.otherdoc_approved_remark = request.POST.get('remark')
            Advance.otherdoc_approved_at = datetime.datetime.now().date()
            Advance.otherdoc_approved_by = officer.employ_name
            Advance.save()
            otherdoc = TKCOtherDocuments.objects.filter(tkcwoinfo=Advance.tkcwoinfo, otherdoc_submit=1, status=1)
            return render(request, 'fqp/wo_creater/approve_otherdoc.html', {"officer": officer,'otherdoc': otherdoc})
    wo = TKCWoInfo.objects.get(id=wo_id)
    otherdoc = TKCOtherDocuments.objects.filter(tkcwoinfo=wo, otherdoc_submit=1, status=1)
    return render(request, 'fqp/wo_creater/approve_otherdoc.html', {"officer": officer, 'wo': wo, 'otherdoc': otherdoc})
    
    

def vendor_approval(request, wo_id,tkc_vendor_id):
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_discom = wo.Discom.Discom_Code
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        other_gtp_doc = request.FILES['other_gtp_doc']
        if TKCVendor.objects.filter(id=tkc_vendor_id, Status=1).exists():
            Advance = TKCVendor.objects.get(id=tkc_vendor_id, Status=1)
            if int(request.POST.get('action')):
                Advance.TKCVendor_Approved_Status = 1
            else:
                Advance.TKCVendor_Approved_Status = -1
            Advance.TKCVendor_Approved_Remark = request.POST.get('remark')
            Advance.TKCVendor_Approved_At = datetime.datetime.now().date()
            Advance.TKCVendor_Approved_By = officer.employ_name
            Advance.other_acceptance_rejection_doc = other_gtp_doc
            Advance.save()
            Vendor = TKCVendor.objects.filter(TKCWoInfo=Advance.TKCWoInfo, TKCVendor_Submit=1, Status=1)
            return render(request, 'fqp/wo_creater/approve_vendor.html',
                          {"officer": officer,'Vendor': Vendor,"wo_discom":wo_discom})
    Vendor = TKCVendor.objects.filter(TKCWoInfo=wo, TKCVendor_Submit=1, Status=1)
    return render(request, 'fqp/wo_creater/approve_vendor.html', {"officer": officer, 'wo': wo, 'Vendor': Vendor,"wo_discom":wo_discom})

def material_offer_approval_offer_data(request,id, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id)
    wo_discom = wo.Discom.Discom_Code
    offer = offer_material_site_stores.objects.filter(id__in=Subquery(offer_material_site_stores.objects.filter(wo=wo).distinct('offer_no').values('id'))).order_by('-Material_Offer_Submit_Submit_At')
    return render(request, 'fqp/wo_creater/approver_offer_step1.html', {"officer": officer, 'wo': wo, 'offer': offer,"wo_discom":wo_discom})
    


#(updated code on prod) offered material approval/rejection by wo_creator with choose categories 
def material_offer_approval(request,wo_id,offer_no,wo_material_boq_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_discom = wo.Discom.Discom_Code
    if request.method == "POST":
        other_acceptance_rejection_document = request.FILES['other_acceptance_rejection_doc']
        if int(request.POST.get('actionVal')):
            offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material = wo_material_boq_id,wo_id = wo_id)
            for i in offer_data:
                i.Material_Offer_Submit_Approved_Status = 1
                i.Material_Offer_Submit_Approved_Remark = request.POST.get('remark')
                i.Material_Offer_Submit_Approved_At = datetime.datetime.now().date()
                i.Material_Offer_Submit_Approved_By = officer.employ_name
                i.TKCVendor.other_acceptance_rejection_doc = other_acceptance_rejection_document
                i.save()
            if request.POST.get('material_category') == 'PDI & DI & Sampling':
                for j in offer_data:
                    j.is_pdi_required = True
                    j.is_di_required = True
                    j.is_sampling_required = True
                    j.material_category = request.POST.get('material_category')
                    j.save()
            elif request.POST.get('material_category') == 'PDI & DI (Sampling Not Required)':
                for k in offer_data:
                    k.is_pdi_required = True
                    k.is_di_required = True
                    k.is_sampling_required = False
                    k.accept_from_nabl = 1
                    k.received_from_nabl =1
                    k.material_category = request.POST.get('material_category')
                    k.save()
            elif request.POST.get('material_category') == 'Direct DI (PDI & Sampling Not Required)':
                for n in offer_data:
                    n.is_pdi_required = False
                    n.is_di_required = True
                    n.is_sampling_required = False
                    n.PDI_Assign = 1
                    n.PDI_Complete = 1
                    n.PDI_Approved_Status = 1
                    n.PDI_Approved_Remark = 'PDI Bypass option choosed by wo_creator'
                    n.accept_from_nabl =1
                    n.received_from_nabl = 1
                    n.material_category = request.POST.get('material_category')
                    n.save()        
            elif request.POST.get('material_category') == 'DI & Sampling (PDI Not Required)':
                for m in offer_data:
                    m.is_pdi_required = False
                    m.is_di_required = True
                    m.is_sampling_required = True
                    m.PDI_Assign = 1
                    m.PDI_Complete = 1
                    m.PDI_Approved_Status = 1
                    m.PDI_Approved_Remark = 'PDI Bypass option choosed by wo_creator'
                    m.material_category = request.POST.get('material_category')
                    m.save()
                         
        else:
            offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material = wo_material_boq_id)
            total_rejected_qty = offer_data.aggregate(Sum('quantity'))['quantity__sum']
            for p in offer_data:
                p.Material_Offer_Submit_Approved_Status = -1
                p.Material_Offer_Submit_Approved_Remark = request.POST.get('remark')
                p.Material_Offer_Submit_Approved_At = datetime.datetime.now().date()
                p.Material_Offer_Submit_Approved_By = officer.employ_name
                p.TKCVendor.other_acceptance_rejection_doc = other_acceptance_rejection_document
                p.save()
            boq_data  = tkc_wo_items_boq.objects.get(id = wo_material_boq_id)
            remaining_qty = boq_data.balance_qty
            boq_data.balance_qty = float(remaining_qty) + total_rejected_qty
            boq_data.save()
        offer = offer_material_site_stores.objects.filter(offer_no=offer_no).distinct("wo_material")
        item_offer_count = {}
        for i in offer:
            offer_count = offer_material_site_stores.objects.filter(wo_material = i.wo_material).distinct('offer_no').count()
            item_offer_count[i.wo_material.id] = offer_count
        zipped_offer_data = zip(offer,item_offer_count.items())
        return render(request, 'fqp/wo_creater/approve_offer.html', {"officer": officer, 'wo': wo, 'offer': zipped_offer_data,"wo_discom":wo_discom})
    offer = offer_material_site_stores.objects.filter(offer_no=offer_no).distinct("wo_material")
    item_offer_count = {}
    for i in offer:
        offer_count = offer_material_site_stores.objects.filter(wo_material = i.wo_material).distinct('offer_no').count()
        item_offer_count[i.wo_material.id] = offer_count
    zipped_offer_data = zip(offer,item_offer_count.items())
    return render(request, 'fqp/wo_creater/approve_offer.html', {"officer": officer, 'wo': wo, 'offer': zipped_offer_data,"wo_discom":wo_discom})


def view_offered_material_details(request,wo_id,offer_no,wo_material_boq_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_discom = wo.Discom.Discom_Code
    offer = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_id = wo_id,wo_material = wo_material_boq_id)
    return render(request, 'fqp/wo_creater/approve_offer_materials_detail.html', {"officer": officer, 'wo': wo, 'offer': offer,"wo_discom":wo_discom,"wo_id":wo_id,"offer_no":offer_no,"wo_material_boq_id":wo_material_boq_id})


def material_offer_approved(request,id, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id)
    if request.method == "POST":
        if offer_material_site_stores.objects.filter(id=wo_id).exists():
            offer_data = offer_material_site_stores.objects.filter(id=wo_id)
            # Advance = offer_material_site_stores.objects.get(id=wo_id, Status=1)
            if int(request.POST.get('action')):
                for i in offer_data:
                    Advance = offer_material_site_stores.objects.get(id=i.id)
                    Advance.Material_Offer_Submit_Approved_Status = 1
                    Advance.Material_Offer_Submit_Approved_Remark = request.POST.get('remark')
                    Advance.Material_Offer_Submit_Approved_At = datetime.datetime.now().date()
                    Advance.Material_Offer_Submit_Approved_By = officer.employ_name
                    Advance.save()
            else:
                for i in offer_data:
                    Advance = offer_material_site_stores.objects.get(id=i.id)
                    Advance.Material_Offer_Submit_Approved_Status = -1
                    Advance.Material_Offer_Submit_Approved_Remark = request.POST.get('remark')
                    Advance.Material_Offer_Submit_Approved_At = datetime.datetime.now().date()
                    Advance.Material_Offer_Submit_Approved_By = officer.employ_name
                    Advance.save()
            offer = offer_material_site_stores.objects.filter(TKCVendor__TKCWoInfo=wo,
                                                  Material_Offer_Submit=1, Status=1)
            return render(request, 'fqp/wo_approver/approved_offer.html', {"officer": officer, 'wo': wo, 'offer': offer})
    offer = offer_material_site_stores.objects.filter(TKCVendor__TKCWoInfo=wo, is_offered=True)
    return render(request, 'fqp/wo_approver/approved_offer.html', {"officer": officer, 'wo': wo, 'offer': offer})




# Approver Code by jeevan


def work_order(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone)
    return render(request, 'fqp/wo_approver/work_order.html',
                  {"officer": officer, 'wo': wo})


def approver_view_work_order(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id, Status=1)
    Header = TKCWoInfo_Header.objects.filter(TKCWoInfo=wo, Status=1)
    Company = UserCompanyDataMain.objects.filter(user_id_id=wo.supplier)
    Price = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo=wo, Status=1)
    Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
    Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1).order_by('Schedule_Supply__Schedule_No')
    Install_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo, Status=1).order_by('Schedule_Installation__Schedule_No')
    Install = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    Major_Item = TKCWoInfo_Major_Item.objects.filter(TKCWoInfo=wo, Status=1)
    Variable_Item = TKCWoInfo_Variable_Item.objects.filter(TKCWoInfo=wo, Status=1)
    Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
    gbpa_order_status=wo.is_gbpa_order
    print("+=============================",gbpa_order_status)
    print("Company------>",Company[0].CompanyName_E)
    return render(request, 'fqp/wo_approver/wo_view.html',
                  {"officer": officer, 'wo': wo, 'Header': Header, 'Company': Company, 'Time': Time, 'Price': Price,
                   "Advance": Advance, 'Supply_Item': Supply_Item, 'Supply': Supply, 'Install_Item': Install_Item,
                   'Install': Install, 'Major_Item': Major_Item, 'Install': Install, 'Variable_Item': Variable_Item,
                   'Copy_To': Copy_To,'gbpa_order':gbpa_order_status})


def wo_reject(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id)
    wo.Wo_Send_To_Approval_Status = 0
    wo.save()
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone)
    return render(request, 'fqp/wo_approver/work_order.html',
                  {"officer": officer, 'wo': wo})


def wo_approved(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id)
    wo.Wo_Approved_Status = 1
    wo.Wo_Approved_At = datetime.datetime.now().date()
    wo.Wo_Approved_By = officer.employ_name
    wo.save()
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    messages.add_message(request, messages.INFO, 'Work Order Approved Successfully')
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone)
    return render(request, 'fqp/wo_approver/work_order.html',
                  {"officer": officer, 'wo': wo})


def wo_upload_digital_copy(request, id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        wo = TKCWoInfo.objects.get(id=id)
        if request.FILES['digital']:
            wo.Wo_Digital = request.FILES['digital']
            wo.Wo_Digital_Upload_Status = 1
            wo.Wo_Digital_Upload_At = datetime.datetime.now().date()
            wo.Wo_Digital_Upload_By = officer.employ_name
            wo.save()
        wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone)
        return render(request, 'fqp/wo_approver/work_order.html',
                      {"officer": officer, 'wo': wo})
    wo = TKCWoInfo.objects.get(id=id)
    return render(request, 'fqp/wo_approver/po_digital_upload.html',
                  {"officer": officer, 'wo': wo})


def bank_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    Bank = BankDetails.objects.filter(user_id=wo.supplier.User_Id, bank_submit=1, Status=1)
    return render(request, 'fqp/wo_approver/bank_view.html', {"officer": officer, 'wo': wo, 'Bank': Bank})


def bg_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=wo, BG_Submit=1, Status=1)
    return render(request, 'fqp/wo_approver/bg_view.html', {"officer": officer, 'wo': wo, 'BG': BG})


def loc_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    LOC = TKCWoInfo_LOC.objects.filter(TKCWoInfo=wo, LOC_Submit=1, Status=1)
    return render(request, 'fqp/wo_approver/loc_view.html', {"officer": officer, 'wo': wo, 'LOC': LOC})


def pert_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    Pert = TKCWoInfo_Pert.objects.filter(TKCWoInfo=wo, Pert_Submit=1, Status=1)
    return render(request, 'fqp/wo_approver/pert_view.html', {"officer": officer, 'wo': wo, 'Pert': Pert})


def otherdoc_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    otherdoc = TKCOtherDocuments.objects.filter(tkcwoinfo=wo, otherdoc_submit=1, status=1)
    return render(request, 'fqp/wo_approver/otherdoc_view.html', {"officer": officer, 'wo': wo, 'otherdoc': otherdoc})

def mqpdoc_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    mqpdoc = TKC_MqpPlanDocuments.objects.filter(tkcwoinfo=wo, mqpdoc_submit=1, status=1)
    return render(request, 'fqp/wo_approver/mqpdoc_view.html', {"officer": officer, 'wo': wo, 'mqpdoc': mqpdoc})


def fqpdoc_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    fqpdoc = TKC_FqpPlanDocuments.objects.filter(tkcwoinfo=wo, fqpdoc_submit=1, status=1)
    return render(request, 'fqp/wo_approver/fqpdoc_view.html', {"officer": officer, 'wo': wo, 'fqpdoc': fqpdoc})


def vendor_view(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    Vendor = TKCVendor.objects.filter(TKCWoInfo=wo, TKCVendor_Submit=1, Status=1)
    return render(request, 'fqp/wo_approver/vendor.html', {"officer": officer, 'wo': wo, 'Vendor': Vendor})
    
    
# Nodal officer


def view_item(request):
    officer = Officer.objects.get(Division__Division_Name_E=request.session['Division'])
    # offer = Wo_Material_Dispatch_details.objects.filter(Division__Division_Name_E = officer.Division.Division_Name_E,delivery_status=1).distinct('wo_material')
    # # offer = tkc_di_master.objects.filter(wo_material__DI_Division__Division_Name_E = officer.Division.Division_Name_E,di_approved_status=1)
    # return render(request, 'fqp/Nodal/item.html', {"officer": officer, 'offer': offer})
    
# ***********************************************************************rohit******************************************
def item_received(request,item_id):
    officer = Officer.objects.get(Division__Division_Name_E=request.session['Division'])
    Advance = Offer_Material.objects.get(id=item_id)
    item_code_table = Offer_Material_Item_Code.objects.filter(Division__Division_Name_E = officer.Division.Division_Name_E,Offer_Material =Advance)
       
    if request.method =="POST":
        for data in item_code_table:
            
            pstatus = request.POST.get(f'{data.id}')
            if pstatus == None:
                
                data.Physical_Status = data.Physical_Status
                data.save()

            elif pstatus == 1:
                data.Physical_Status = data.Physical_Status
                data.save()

            elif pstatus == -1:
                data.Physical_Status = data.Physical_Status
                data.save()

            else:                    
                data.Physical_Status = pstatus
                data.save()
        return redirect(f"/fqp/wo_pdi_material_view/{item_id}")
    return render(request, 'fqp/Nodal/fqp_select_received_material.html', {'data': item_code_table,'dataid':item_id})

    
    
def wo_pdi_material_view(request,id):

    Advance = Offer_Material.objects.get(id = id)
    item_code_table = Offer_Material_Item_Code.objects.filter(Offer_Material = Advance,Physical_Status = 2)
    return render(request, 'fqp/Nodal/fqp_view_serial_number.html', {'data': item_code_table,'dataid':id})
    
    
    
def FqpDiStatus(request,id):
   
    if request.method =="POST":

        Advance = Offer_Material.objects.get(id = id)
        serial = Offer_Material_Item_Code.objects.filter(Offer_Material = Advance,Physical_Status = 2)
        # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.offer_item.item_name,Offer_status=1,po=material.po,area_store=store_name.Name,area_store_id = material)
        list_all=[]
        
        drr_date = request.POST.get('drr_date')
        challan_no=request.POST.get('challan_no')
        challan_date=request.POST.get('challan_date')
        vehicle=request.POST.get('vehicle')
        quantity=request.POST.get('quantity')

        data1 = fqp_drr_info(area_store=Advance, drr_date=drr_date, drr_vehicle=vehicle,drr_challan_no=challan_no,
                            drr_challan_date=challan_date,drr_quantity=quantity)
        data1.save()
        for data in serial:
            # value = DI_Material_Offer_Serial_No.objects.get(id=data.id)
            pstatus = request.POST.get(f'{data.id}')
            premark = request.POST.get(f'a{data.id}')
            list_all.append(pstatus)
            if pstatus == "-1":
                
                data.Physical_Status= -1
                data.Status = -1
                data.Physical_Remark=premark
                data.save()
        

            elif pstatus == None:
                data.Physical_Status = data.Physical_Status
                data.Status = data.Status
                data.Physical_Remark = data.Physical_Remark
                data.save()
                list_all[-1] = str(data.Physical_Status)

            elif pstatus == "1":
                data.Physical_Status = 1
                data.Status = 1
                data.Physical_Remark=premark
                data.save()
        list_check = []
        zero = 0

        if ("0") not in list_all and ("-1") not in list_all:
            serial = Offer_Material_Item_Code.objects.filter(Offer_Material = Advance)
            for i in serial:
                list_check.append(i.Physical_Status)
                print("rtrtrtrtrtrtrtrtrtrtrtrt",list_check)
                if zero not in list_check:
                    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                    newdata = Offer_Material.objects.get(id=id, Status=1)                
                    newdata.Physical_Status = 1
                    newdata.save()

                else:
                    newdata = Offer_Material.objects.get(id=id, Status=1)                
                    newdata.Physical_Status = 0
                    newdata.save()
            
        else: 
            newdata = Offer_Material.objects.get(id=id, Status=1)                
            newdata.Physical_Status = -1
            newdata.save()
    

        return redirect('/fqp/view_item')

      
    
    
    
def fqp_di_send_to_cgm(request,id):
    di_master = Offer_Material.objects.get(id=id, Status=1,Physical_Status=1)
    di_master.send_to_cgm = 1
    di_master.save()
    return redirect('/fqp/view_item')

    
    
def fqp_reject_di(request):
    # store_name = Store_Info.objects.get(id=request.session['store'])
    officer = Officer.objects.get(Division__Division_Name_E=request.session['Division'])
    # offer = Offer_Material.objects.filter(Physical_Status='-1')
    # offer = Wo_Material_Dispatch_details.objects.filter(Division__Division_Name_E = officer.Division.Division_Name_E,wo_material__Physical_Status = "-1").distinct('wo_material')
    
    # return render(request, 'fqp/Nodal/fqp_reject_di.html', {'data': offer})
    
    
def fqp_reject_di_material_view(request,id):
    Advance = Offer_Material.objects.get(id=id)
    serial = Offer_Material_Item_Code.objects.filter(Offer_Material = Advance,Physical_Status='-1',Status = '-1')
    return render(request, 'fqp/Nodal/fqp_reject_di_material_view.html', {'data': serial,'dataid':id})
   



def fqp_select_material_for_getpass(request,id):
  
    Advance = Offer_Material.objects.get(id=id)
    serial = Offer_Material_Item_Code.objects.filter(Offer_Material = Advance,Physical_Status='-1',Status = '-1')
    
    if request.method =="POST":
        for data in serial:
            pstatus = request.POST.get(f'{data.id}')
            if pstatus == None:
                data.Status = -1
                data.save()

            elif pstatus == 1:
                data.Status = data.pstatus
                data.save()


            else:                    
                data.Status = pstatus
                data.save()
          
        return redirect(f'/fqp/fqp_create_po_gatepass/{id}')

    return render(request, 'fqp/Nodal/fqp_select_material_for_getpass.html', {'data': serial,'dataid':id})



def fqp_create_po_gatepass(request,id):
    if request.session.has_key('store'):
        Advance = Offer_Material.objects.get(id=id)
        serial = Offer_Material_Item_Code.objects.filter(Offer_Material = Advance,Physical_Status='-1',Status = 2)
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

            data1 = fqp_wo_gatepass(area_store=Advance, gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,
                                material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh)
            data1.save()
          
            for i in serial:
                i.gatepass = 1
                i.save()

            return render(request, 'fqp/Nodal/fqp_wo_gatepass_outward_print.html', {'data': Advance,'material':serial,'data1':data1})
        
        return render(request, 'fqp/Nodal/fqp_wo_gatepass_outward.html', {'data': Advance,'material':serial})
    return redirect('/')



def fqp_gatepass(request):
    if request.session.has_key('store'):
        # store_name = Store_Info.objects.get(id=request.session['store'])
        di_master = fqp_wo_gatepass.objects.all()
        return render(request, 'fqp/Nodal/fqp_gatepass_history.html', {'data': di_master})
    return redirect('/')


def fqp_gatepass_history(request,id):
    data1 = fqp_wo_gatepass.objects.get(id=id)
    
    return render(request, 'fqp/Nodal/fqp_gatepass_outward_print_new.html', {'data1': data1})
        


def fqp_wo_sample_list(request):
    # sampling = Wo_Material_Dispatch_details.objects.filter(wo_material__Physical_Status=1)
    sampling = tkc_di_master.objects.filter(wo_material__Physical_Status=1)
    print("ffffff",sampling)
    # for i in sampling:
    return render(request, 'officer/wo_sampling.html', {'data1': sampling})





def fqp_sample_select(request,id):

    di_as_obj = Offer_Material.objects.get(id=id)
    lst_serial_number = []
    di_mosn_obj = Offer_Material_Item_Code.objects.filter(Offer_Material = di_as_obj)
    
    for i in di_mosn_obj:
        mat_name = i.Offer_Material.TKCVendor.Material_id.Material_Specification
        item_code = i.Offer_Material.TKCVendor.Material_id.item_code
        lst_serial_number.append(i.Item_Serial_No)

        
    
    print("pawwawaw",lst_serial_number)
    ps_obj = product_sampling.objects.get(item_code = item_code)
    if ps_obj.sampling.sample_type == 1:
        sample_percent = ps_obj.sampling.sample_percentage
    else:
        pass

    length_serial_number =  len(lst_serial_number)
    # import random
    random.shuffle(lst_serial_number)

    # import math
    random_mat_round_number = math.ceil((length_serial_number * sample_percent ) / 100)
    final_random_sample_mat = lst_serial_number[:random_mat_round_number]
    
    for i in final_random_sample_mat:
        obj = Offer_Material_Item_Code.objects.filter(Item_Serial_No=i)
        obj.update(is_sampled=1)
        
        
        
        di_as_obj.send_to_cgm=2
        di_as_obj.save()
    
    lst_as = []
    lst_mat_name = []
    for i in final_random_sample_mat:
        dmosn_obj = Offer_Material_Item_Code.objects.get(Item_Serial_No = i)
        lst_mat_name.append(dmosn_obj.Offer_Material.TKCVendor.Material_id.Material_Specification)
        
        dmosn_obj.Offer_Material.send_to_cgm=3
        dmosn_obj.Offer_Material.nabl_status=1
        
        dmosn_obj.save()
    
    final_zip = zip(final_random_sample_mat, lst_mat_name)
        


    html = "<html><body>Random Material Ids are %s. </body></html>" % final_random_sample_mat
    return render(request, 'officer/fqp_wo_forward_nabl.html', {'data1': di_as_obj, 'final_zip':final_zip})


from nabl.models import *


def fqp_select_testing_nabl(request,id):
    material = Offer_Material.objects.get(id=id)
    nabl = NABL_Registration_Test.objects.filter(Material_Item_Code= material.TKCVendor.Material_id.item_code)
    all_query=[]
    for data in nabl:
        user = User_Registration.objects.filter(User_Id=data.user_id)
        all_query.append(user)

    if request.method == "POST":
        nabl_name = request.POST.get('nabl')
        nabl_number = User_Registration.objects.get(CompanyName_E=request.POST.get('nabl'))
        material.nabl_name = nabl_name
        material.nabl_status = 1
        material.nabl_number = nabl_number.ContactNo
        material.send_to_cgm=3
        material.save()
            
        return redirect('/fqp/fqp_wo_sample_list')
    return render(request, 'officer/fqp_select_testing_nabl.html', {'data': material,'nabl':all_query})




def fqp_view_samled_material(request,id):
    material = Offer_Material.objects.get(id=id)
    di_area_store = Offer_Material_Item_Code.objects.filter(Offer_Material = material,is_sampled=1)
    
    return render(request, 'officer/fqp_view_sampled_material.html', {'final_zip':di_area_store})
            

  
def fqp_wo_trf_create(request):
    # if request.session.has_key('store'):
    # store_name = Store_Info.objects.get(id=request.session['store'])
    di_as_obj = tkc_di_master.objects.filter(wo_material__send_to_cgm=3,wo_material__nabl_status=1)

    return render(request, 'fqp/Nodal/fqp_wo_trf_details.html', {'data1': di_as_obj})
    # return redirect('/')
    
    
    
def fqp_wo_di_sampled_item(request,id):
    officer = Officer.objects.get(Division__Division_Name_E=request.session['Division'])
    material = Offer_Material.objects.get(id=id)
    serial = Offer_Material_Item_Code.objects.filter(Offer_Material = material,is_sampled=1,Division__Division_Name_E = officer.Division.Division_Name_E)
    return render(request, 'fqp/Nodal/fqp_view_sampled_item.html', {'data': serial,'dataid':id})
    
    
    
    
    
def fqp_wo_nabl_gatepass_new(request,id):
    # if request.session.has_key('store'):
    #     store_name = Store_Info.objects.get(id=request.session['store'])
    material = Offer_Material.objects.get(id=id)
    obj_item = Offer_Material_Item_Code.objects.filter(Offer_Material = material,is_sampled=1,Division__Division_Name_E=request.session['Division'])
   
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
        gatepass = request.FILES['gatepass']
    
        data1 = fqp_wo_nabl_gatepass(area_store = material,gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                            driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,gate_pass=gatepass,Store_Address=reject_item[0].Store_Address,Division = reject_item[0].Division, 
                            material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh,aname = material.nabl_name)
        data1.save()
        material.nabl_gatepass = 1
        material.save()
        
        return render(request, 'fqp/Nodal/fqp_wo_nabl_gatepass_print.html', {'data': material,'material':obj_item,'data1':data1})
    
    return render(request, 'fqp/Nodal/fqp_wo_nabl_gatepass.html', {'data': material,'material':obj_item})
    # return redirect('/')
    


def fqp_test_request_form_submit(request,id):
    material =  Offer_Material.objects.get(id=id)
    gate_pass_number = fqp_wo_nabl_gatepass.objects.filter(area_store = material)
    if request.method == "POST":
        material = Offer_Material.objects.get(id=id)
        customer_Organization_name = request.POST.get('customer_Organization_name')
        customer_Organization_address = request.POST.get('customer_Organization_address')
        contact_person_name = request.POST.get('contact_person_name')
        contact_person_designation = request.POST.get('contact_person_designation')
        mobile_no = request.POST.get('mobile_no')
        email_id = request.POST.get('email_id')
        name_of_sample_product = request.POST.get('name_of_sample_product')
        customer_ref_gatepass_no = request.POST.get('customer_ref_gatepass_no')
        dated = request.POST.get('dated')

        if request.FILES['trf_file' or None]:
            trf_file = request.FILES['trf_file'] 

        trf_obj = Fqp_Work_Order_Trf_Details(area_store_id = material ,TRFAreastore_file=trf_file,
                              customer_Organization_name=customer_Organization_name, 
                              customer_Organization_address=customer_Organization_address,
                              contact_person_name=contact_person_name,
                              contact_person_designation=contact_person_designation, 
                              mobile_no=mobile_no, email_id=email_id, 
                              name_of_sample_product=name_of_sample_product, 
                              customer_ref_gatepass_no=customer_ref_gatepass_no, 
                              dated=dated,  trf_generated = 1,nabl_name = material.nabl_name,nabl_number=material.nabl_number)
        trf_obj.save()
       
        material.send_to_nabl = 1
        trf_data = Fqp_Work_Order_Trf_Details.objects.filter(area_store_id=material).last()
        material.save()
        return render(request, 'fqp/Nodal/fqp_wo_test_request_view.html', {'material': material,'trf':trf_data,'gate_pass_number':gate_pass_number[0]})


    return render(request, 'fqp/Nodal/fqp_wo_test_request_form.html',{'material': material,'gate_pass_number':gate_pass_number[0]})

    
# *****************************************************************end********************************************************    
#TKC DI code 
def di_offers_list(request,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo,DI_Created_Status=0,PDI_Complete=1,PDI_Approved_Status=1,Material_Offer_Submit_Approved_Status = 1,is_di_required = True).distinct('offer_no')
    return render (request,'fqp/wo_creater/wo_di_offers_list.html',{"officer": officer,'offer_material_data':offer_details,"wo":wo})
    # return render (request,'fqp/wo_creater/pending_di_list.html',{"officer": officer,'offer_material_data':offer_details,"wo":wo})


def view_offer_approved_material(request,wo_id,offer_no):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1,DI_Created_Status=0,Material_Offer_Submit_Approved_Status = 1,is_di_required = True)
    if len(offer_details) == 0:
        offer_details = ""
    return render (request,'fqp/wo_creater/wo_di_offers_material_list.html',{"officer": officer,'offer_material_data':offer_details,"wo":wo,"offer_no":offer_no})


from fqp.forms import TKC_T_C_WorkFormData,TKCCopyWorkFormData

def create_tkc_di_step1(request,wo_id,offer_no):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    material = offer_material_site_stores.objects.filter(TKCVendor__TKCWoInfo = wo)
    if request.method=="POST":
        subject = request.POST.get('di_subject')
        erp_di_no = request.POST.get('DI_no')
        di_prefix = request.POST.get('di_prefix')

        data = tkc_di_master(wo=wo,offer_no = offer_no,zone = wo.zone,wo_no = wo.wo_no,
        di_subject = subject,erp_di_number = erp_di_no,prefix = di_prefix)
        data.save()
        offer_data = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1,is_di_required = True,DI_Created_Status=0,is_di_created = False)
        di_ref_no = offer_no + str(random.randint(1000, 999999999))
        if offer_material_site_stores.objects.filter(di_offer_ref_no = di_ref_no).exists():
            di_ref_no = offer_no + str(random.randint(1000, 999999999))
        for i in offer_data:
            i.di_offer_ref_no = di_ref_no
            i.save()
        create_Di_id=data.id
        
        return redirect(f"/fqp/Tkc-Di-Terms/{wo_id}/{create_Di_id}/{offer_no}/{di_ref_no}")
    return render (request,'fqp/wo_creater/wo_create_di_step1.html',{"officer": officer,'offer_material_data':material,"wo":wo,"offer_no":offer_no})


def TkcDiTerms(request,wo_id,create_Di_id,offer_no,di_ref_no):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    form = TKC_T_C_WorkFormData()
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_di  = tkc_di_master.objects.get(id = create_Di_id)
    if request.method=="POST":
         form = TKC_T_C_WorkFormData(request.POST,instance=wo_di)
         if form.is_valid():
             wo_di.term_and_condition = form.cleaned_data['term_and_condition']
             wo_di.save()
             return redirect(f"/fqp/create_di_step2/{wo_id}/{create_Di_id}/{offer_no}/{di_ref_no}")
    return render (request,'fqp/wo_creater/wo_create_di_step2.html',{'wo':wo,"form":form,'wo_di':wo_di,"offer_no":offer_no,"di_ref_no":di_ref_no})
        
    
def create_di_step2(request,wo_id,create_Di_id,offer_no,di_ref_no):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    form = TKCCopyWorkFormData()
    wo = TKCWoInfo.objects.get(id=wo_id)
    address = UserCompanyDataMain.objects.get(user_id_id=wo.supplier)
    wo_di_object  = tkc_di_master.objects.get(id = create_Di_id)
    # offer_details_1 = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1)
    if wo_di_object.final_di_submit == True:
        offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,Material_Offer_Submit_Approved_Status = 1,PDI_Complete=1,PDI_Approved_Status=1,is_di_required = True,di_offer_ref_no = di_ref_no).order_by('-id')
    else:
        offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,Material_Offer_Submit_Approved_Status = 1,PDI_Complete=1,PDI_Approved_Status=1,is_di_required = True,DI_Created_Status=0,is_di_created = False,di_offer_ref_no = di_ref_no).order_by('-id')
    boq_id_list = []
    for i in offer_details:
        offer_vendor = i.TKCVendor
        boq_id_list.append(i.wo_material.id)
    boq_unique_ids_set = set(boq_id_list)
    new_list = list(boq_unique_ids_set)
    boq_data_dict = {} 
    boq_material_data = tkc_wo_items_boq.objects.filter(id__in = new_list)  
    vendor_address = UserCompanyDataMain.objects.get(user_id_id=offer_vendor.Vendor)
    if request.method=="POST":
        di_data_exist = tkc_di_master.objects.filter(id = create_Di_id,offer_no = offer_no,final_di_submit = True )
        if len(di_data_exist) > 0:
            boq_data_dict = {} 
            boq_material_data = tkc_wo_items_boq.objects.filter(id__in = new_list)
            for var in boq_material_data:
                offer_ietm_qty = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,wo_material = var,DI_Created_Status = 1,is_di_created = True,Material_Offer_Submit_Approved_Status = 1,di_offer_ref_no = di_ref_no).aggregate(Sum('quantity'))
                offered_qty = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,wo_material = var,Material_Offer_Submit_Approved_Status = 1,di_offer_ref_no = di_ref_no).aggregate(Sum('quantity'))
                boq_data_list = []
                boq_data_list.append(var.item_code)
                boq_data_list.append(var.uom)
                boq_data_list.append(var.total_order_qty)
                boq_data_list.append(float(var.dispatch_qty) - offer_ietm_qty['quantity__sum']) 
                boq_data_list.append(var.balance_qty)
                boq_data_list.append(var.balance_di_qty)
                boq_data_list.append(offered_qty['quantity__sum'])
                boq_data_dict[var.material_name] = boq_data_list 
            return render (request,'fqp/wo_creater/wo_di_view.html',{'wo':wo, "wo_di":wo_di_object,"address":address,"offer_no":offer_no,"offer_details":offer_details,"vendor_address":vendor_address,"boq_data_dict":boq_data_dict})
        if wo_di_object.final_di_submit == False:
            for jj in boq_material_data:
                offer_materials_record = offer_material_site_stores.objects.filter(wo_material = jj,offer_no = offer_no,di_offer_ref_no =di_ref_no,is_di_required = True,DI_Created_Status=0,is_di_created = False).aggregate(Sum('quantity'))
                already_dispatch_item_qty = float(jj.total_order_qty) - float(jj.dispatch_qty)  
                jj.balance_di_qty = already_dispatch_item_qty - offer_materials_record['quantity__sum']
                jj.save()
        for var in boq_material_data:
            boq_data_list = []
            offered_qty = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,wo_material = var,Material_Offer_Submit_Approved_Status = 1,di_offer_ref_no = di_ref_no).aggregate(Sum('quantity'))
            boq_data_list.append(var.item_code)
            boq_data_list.append(var.uom)
            boq_data_list.append(var.total_order_qty)
            boq_data_list.append(var.dispatch_qty)
            boq_data_list.append(var.balance_qty)
            boq_data_list.append(var.balance_di_qty)
            boq_data_list.append(offered_qty['quantity__sum'])
            boq_data_dict[var.material_name] = boq_data_list
        form = TKCCopyWorkFormData(request.POST,instance=wo_di_object)
        if form.is_valid():
            wo_di_object.copy_to = form.cleaned_data['copy_to']
            wo_di_object.save()
            for i in offer_details:
                i.DI_Created_Status = 1
                i.is_di_created = True
                i.tkc_di = wo_di_object
                i.DI_Created_At = datetime.datetime.now()
                i.DI_Created_By = officer.employ_name
                i.save()
                offer_qty = i.quantity
                boq_data = tkc_wo_items_boq.objects.get(id = i.wo_material.id)
                boq_previous_dispatch_qty= float(boq_data.dispatch_qty)     
                boq_data.dispatch_qty = boq_previous_dispatch_qty + float(offer_qty) 
                boq_data.save()
            wo_di_object.final_di_submit = True 
            wo_di_object.save()
            if tkc_di_master_deleted_history.objects.filter(wo = wo,offer_no = offer_no,erp_di_number = wo_di_object.erp_di_number).exists():
               tkc_di_history = tkc_di_master_deleted_history.objects.get(wo = wo,offer_no = offer_no,erp_di_number = wo_di_object.erp_di_number)
               tkc_di_history.revised_di_created = True
               tkc_di_history.save()
            else:
                pass              
            return render (request,'fqp/wo_creater/wo_di_view.html',{'wo':wo, "wo_di":wo_di_object,"address":address,"offer_no":offer_no,"offer_details":offer_details,"vendor_address":vendor_address,"boq_data_dict":boq_data_dict})
            
    return render (request,'fqp/wo_creater/wo_create_di_step3.html',{'wo':wo,"form":form,"wo_di":wo_di_object,"address":address,"offer_no":offer_no,"di_ref_no":di_ref_no})
        
            
# def SendWoDiForApproval(request,wo_id):
#     officer = Officer.objects.get(employ_id=request.session['employ_id'])
#     wo_di_object  = tkc_di_master.objects.get(id = wo_id)
#     wo_di_object.di_send_to_approval_status = True
#     wo_di_object.di_send_by_approval_by =officer.employ_name
#     wo_di_object.save()
#     wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone)
#     return render(request, 'fqp/wo_creater/work_order.html',
#                   {"officer": officer, 'wo': wo,'msg1':"Work Order DI Send For Approval successfully "})

def SendPendingWoDiForApproval(request,di_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_di_object  = tkc_di_master.objects.get(id = di_id)
    wo_di_object.di_send_to_approval_status = True
    wo_di_object.di_send_by_approval_by =officer.employ_name
    wo_di_object.save()
    wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone)
    # all_wo_di_objects  = tkc_di_master.objects.all().order_by('id')
    all_wo_di_objects  = tkc_di_master.objects.filter(zone=officer.user_zone).order_by('id')
    return render(request, 'fqp/wo_creater/all_wo_di.html',
                  {"wo_di_objects": all_wo_di_objects, 'wo': wo,'msg1':"Work Order DI Send For Approval successfully "})
    
    
def delete_di_data(request,di_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_di_object  = tkc_di_master.objects.get(id = di_id)
    if offer_material_site_stores.objects.filter(offer_no = wo_di_object.offer_no, tkc_di = wo_di_object).exists():
        offer_details = offer_material_site_stores.objects.filter(offer_no = wo_di_object.offer_no, tkc_di = wo_di_object)
        offer_material_data = offer_details.values_list('wo_material',flat = True)
            
        unique_boq_ids = list(set(offer_material_data))
        for j in unique_boq_ids:
            boq_data = tkc_wo_items_boq.objects.get(id = j)
            offer_details_sum = offer_material_site_stores.objects.filter(offer_no = wo_di_object.offer_no, tkc_di = wo_di_object,wo_material = boq_data).aggregate(Sum('quantity'))
            di_item_qty = offer_details_sum['quantity__sum']
            old_dispatch_qty = boq_data.dispatch_qty
            boq_data.dispatch_qty = float(old_dispatch_qty) - di_item_qty
            boq_data.save()
            
        for i in offer_details:
            i.tkc_di = None
            i.is_di_created = False
            i.DI_Created_Status = 0
            i.di_offer_ref_no = None
            i.save()
        
        wo_di_object.delete()
    
        wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone).order_by('-id')
        return render(request, 'fqp/wo_creater/work_order.html',
                    {"officer": officer, 'wo': wo,"msg1":"DI deleted successfully,Now you can create it again."})
    else:
        wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone).order_by('-id')
        return render(request, 'fqp/wo_creater/work_order.html',
                    {"officer": officer, 'wo': wo,"msg1":"Unable to delete the DI"})
        
        
def approver_delete_di_data(request,di_id,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_obj = TKCWoInfo.objects.get(id=wo_id)
    wo_di_object  = tkc_di_master.objects.get(id = di_id)
    if offer_material_site_stores.objects.filter(offer_no = wo_di_object.offer_no, tkc_di = wo_di_object).exists():
        offer_details = offer_material_site_stores.objects.filter(offer_no = wo_di_object.offer_no, tkc_di = wo_di_object)
        offer_material_data = offer_details.values_list('wo_material',flat = True)
            
        unique_boq_ids = list(set(offer_material_data))
        for j in unique_boq_ids:
            boq_data = tkc_wo_items_boq.objects.get(id = j)
            offer_details_sum = offer_material_site_stores.objects.filter(offer_no = wo_di_object.offer_no, tkc_di = wo_di_object,wo_material = boq_data).aggregate(Sum('quantity'))
            di_item_qty = offer_details_sum['quantity__sum']
            old_dispatch_qty = boq_data.dispatch_qty
            boq_data.dispatch_qty = float(old_dispatch_qty) - di_item_qty
            boq_data.save()
            
        for i in offer_details:
            i.tkc_di = None
            i.is_di_created = False
            i.DI_Created_Status = 0
            i.di_offer_ref_no = None
            i.save()
        
        history_data = tkc_di_master_deleted_history(wo = wo_di_object.wo,offer_no =wo_di_object.offer_no, zone = wo_di_object.zone, di_send_to_approval_status = wo_di_object.di_send_to_approval_status,
                                                     di_send_by_approval_by = wo_di_object.di_send_by_approval_by, di_approved_status = wo_di_object.di_approved_status,di_approved_by = wo_di_object.di_approved_by,
                                                     di_subject = wo_di_object.di_subject,erp_di_number = wo_di_object.erp_di_number,prefix = wo_di_object.prefix,term_and_condition = wo_di_object.term_and_condition,
                                                     copy_to = wo_di_object.copy_to,created_date = wo_di_object.created_date,created_di_doc = wo_di_object.created_di_doc)
        
        history_data.save()
        wo_di_object.delete()
        
        tkc_data  = tkc_di_master.objects.filter(wo = wo_obj, di_send_to_approval_status = True)
        return render(request, 'fqp/wo_approver/work_order_di.html',
                  {"officer": officer, 'tkc_data': tkc_data,"wo_obj":wo_obj,'msg1':'DI Rejected Successfully'})
        
    # else:
    #     tkc_data  = tkc_di_master.objects.filter(wo = wo_obj, di_send_to_approval_status = True)
    #     return render(request, 'fqp/wo_approver/work_order_di.html',
    #               {"officer": officer, 'tkc_data': tkc_data,"wo_obj":wo_obj,'msg1':'DI Unable to Reject'})
        
    
    
    
def all_wo_di(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_di_objects  = tkc_di_master.objects.filter(zone =officer.Discom.Discom_Code).order_by('-id')
    print('zone-------------->',officer.user_zone)
    return render(request, 'fqp/wo_creater/all_wo_di.html',
                  {"wo_di_objects": wo_di_objects,'zone':officer.user_zone})
    

def created_di_view(request,wo_id,create_Di_id,offer_no):
    wo = TKCWoInfo.objects.get(id=wo_id)
    address = UserCompanyDataMain.objects.get(user_id_id=wo.supplier)
    wo_di_object  = tkc_di_master.objects.get(id = create_Di_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1)
    for i in offer_details:
        offer_vendor = i.TKCVendor
    vendor_address = UserCompanyDataMain.objects.get(user_id_id=offer_vendor.Vendor)
    return render (request,'fqp/wo_creater/wo_di_view.html',{'wo':wo, "wo_di":wo_di_object,"address":address,"offer_no":offer_no,"offer_details":offer_details,"vendor_address":vendor_address,"boq_data_dict":boq_data_dict})
            
        
        
            
    
def WorkOrderDI(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    tkc_data  = tkc_di_master.objects.filter(zone=officer.user_zone, di_send_to_approval_status = True).distinct('wo')
    return render(request, 'fqp/wo_approver/work_order_di_page1.html',
                  {"officer": officer, 'tkc_data': tkc_data})
    
    
def work_order_dispatch_instruction_list(request,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_obj = TKCWoInfo.objects.get(id=wo_id)
    tkc_data  = tkc_di_master.objects.filter(wo = wo_obj, di_send_to_approval_status = True)
    return render(request, 'fqp/wo_approver/work_order_di.html',
                  {"officer": officer, 'tkc_data': tkc_data,"wo_obj":wo_obj})
    

        
def approver_view_work_order_di(request,di_id,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    address = UserCompanyDataMain.objects.get(user_id_id=wo.supplier)
    wo_di_object  = tkc_di_master.objects.get(id = di_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = wo_di_object.offer_no,PDI_Complete=1,PDI_Approved_Status=1,DI_Created_Status=1)
    for i in offer_details:
        offer_vendor = i.TKCVendor
    vendor_address = UserCompanyDataMain.objects.get(user_id_id=offer_vendor.Vendor)
    # if officer.user_zone=='EZ':
    #     return render(request, 'fqp/wo_approver/erp_work_order_di.html',
    #     {"officer": officer, 'tkc_data': tkc_data1,"msg1":"Di Approved Successfully"})
    return render (request,'fqp/wo_approver/wo_di_view.html',{'wo':wo, "wo_di":wo_di_object,"address":address,"offer_details":offer_details,"vendor_address":vendor_address})
            
    
def WoDiApproval(request,di_id,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_obj = TKCWoInfo.objects.get(id=wo_id)
    tkc_data  = tkc_di_master.objects.get(id = di_id)
    tkc_data.di_approved_status = 1
    tkc_data.di_approved_by = officer.employ_name
    tkc_data.save()
    tkc_data1  = tkc_di_master.objects.filter(wo = wo_obj, di_send_to_approval_status = True)
    return render(request, 'fqp/wo_approver/work_order_di.html',
                {"officer": officer, 'tkc_data': tkc_data1,"wo_obj":wo_obj,"zone":officer.user_zone})


def upload_digital_work_order_di(request,di_id,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_obj = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        tkc_data  = tkc_di_master.objects.get(id = di_id)
        tkc_data.tkc_di_doc = request.FILES['digital']
        tkc_data.di_digital_upload_status = 1
        tkc_data.di_digital_upload_by = officer.employ_name
        tkc_data.save()
        tkc1 = tkc_di_master.objects.filter(wo = wo_obj, di_send_to_approval_status = True)
        return render(request, 'fqp/wo_approver/work_order_di.html',
                    {"officer": officer, 'tkc_data': tkc1,"msg1":"DI Digital Order Upload Successfully"})
    tkc_data2  = tkc_di_master.objects.get(id = di_id)
    return render(request, 'fqp/wo_approver/di_upload_digital_order.html',
                {"officer": officer, 'tkc_data': tkc_data2,'wo_id':wo_id})
    

# ********************************************* BOQ Code *****************************************************************

def all_discom(request):
    discom = Discom_Master.objects.all().values()
    data=list(discom)   
    return JsonResponse(data, safe=False)

def circle_master(request,discom_id):
    discom = Discom_Master.objects.get(id=discom_id)
    all_record = Circle_Master.objects.filter(Region__Discom=discom).values()    
    data=list(all_record)   
    return JsonResponse({"data": data})


def tag_circle(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')    
    return render(request, 'fqp/wo_creater/tag_circle.html',{"officer": officer, 'wo': wo})

from django.http import JsonResponse

def tag_circle_by_wo(request,wo_no,discom_id):
    tag_circle_data=Tag_Circle.objects.filter(wo_no=wo_no,id=discom_id).values()    
    tc_data=list(tag_circle_data)
    return JsonResponse({"data":tc_data})

    
@csrf_exempt
def wo_region_save(request):    
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    circle_name = request.POST.getlist('Circle_Name')    
    wo_id = request.POST.get('work_order_id')
    discom = request.POST.get('region_new')    
    disom_instance = Discom_Master.objects.get(id = int(discom))    
    wo = TKCWoInfo.objects.get(id=wo_id)
    for i in circle_name:
        circle_instance  = Circle_Master.objects.get(Circle_Name_E = i)
        circle_data = Tag_Circle(wo_no = wo, discom=disom_instance,circle = circle_instance, circle_name= i, Created_At = datetime.datetime.now(),Created_By = officer.employ_name)
        circle_data.save() 
    total_circle = Circle_Master.objects.filter(Region__Discom=discom)     
    tag_circle = Tag_Circle.objects.filter(wo_no=wo, discom=disom_instance)
    untag_circle = []
    for i in total_circle:
        for j in tag_circle:
            if i == j.circle:
                pass
            else:
                untag_circle.append(i)
    print(untag_circle)  
    
    if discom == '1':
        wo.cz_circle_added = 1
        wo.save()
    elif discom == '2':
        wo.wz_circle_added = 2
        wo.save()
    elif discom == '3':
        wo.ez_circle_added = 3
        wo.save()  
        
    
    
    wo_data = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
    return render(request, 'fqp/wo_creater/tag_circle.html',
                  {"officer": officer, 'wo': wo_data})

def wo_boq_list(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
    return render(request, 'fqp/wo_creater/update_boq.html',
                  {"officer": officer, 'wo': wo})

def update_boq(request,wo_id): 
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id).values() 
   
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)

    if len(stored_data) != 0:

        #reloading
        item_code_list = []
        item_dict = {}
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)
            for k in stored_item_data:
                item_qty_list.append(k.circle_quantity)
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list   
    else:
        item_dict = 0
        circle_list = 0
    
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')       
    return render(request, 'fqp/wo_creater/update_boq_info.html',{'wo':wo, "item_dict":item_dict, "circle_list":circle_list, "boq_data" : boq_data,"circles":circles, "wo_instance":wo_instance})
    
    
def update_boq_info(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
    return render(request, 'fqp/wo_creater/update_boq_info.html',
                {"officer": officer, 'wo': wo})
                
import itertools
@csrf_exempt
def save_boq(request,wo_id, identifier):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])     
    circles = Tag_Circle.objects.filter(wo_no=wo_id)
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id) 
      
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1)  
    if identifier == 1:
        if tkc_update_boq.objects.filter(wo=wo_id).exists():
            exist_data = tkc_update_boq.objects.filter(wo=wo_id)
            exist_data.delete()            
    else:
        pass
 
    for i in boq_data:   
        item_name = i.item_code  
        material_name = i.material_name
        total_order_qty= i.total_order_qty
        circle_boq_data = request.POST.getlist(item_name)        
        for j,k in zip(circle_boq_data,circle_list):
            if j in validators.EMPTY_VALUES:
                m = None
            else:
                m = float(j)
            data = tkc_update_boq(wo=wo, circle_quantity=m, material_name=material_name, item_code=item_name, total_order_qty=total_order_qty, circles_name=k.circle_name, updated_at=datetime.datetime.now(), created_at=datetime.datetime.now(), Created_By=officer.employ_name)
            data.save()
            wo.is_boq_added  = 2
            wo.save()
    items_qty = {}
    
    for req in boq_data:
        item_name = req.item_code
        circle_boq_data = request.POST.getlist(item_name)  
        items_qty[item_name] = circle_boq_data
        
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)   

    if len(stored_data) != 0:
    
        item_code_list = []
        item_dict = {}        
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)            
            for k in stored_item_data:                                
                if k.circle_quantity == None:
                    k.circle_quantity = 0
                item_qty_list.append(k.circle_quantity)
                circle_list.append(k.circles_name)                
            item_dict[j]=item_qty_list 
            a = sum(item_qty_list)
            total = "{:.2f}".format(a)
            item_qty_list.append(total)                        
             
    else:
        item_dict = 0
        circle_list = 0
    print("::::::::", item_qty_list)
    wo_instance = TKCWoInfo.objects.get(id=wo_id)
    return render(request, 'fqp/wo_creater/update_boq_edit.html',
                    {"officer": officer, 'wo': wo, "item_dict": item_dict, "boq_data": boq_data, "circles":circles, "wo_instance":wo_instance,"items_qty":items_qty,"circle_list":circle_list})

import itertools
@csrf_exempt
def save_boq_info(request,wo_id, identifier):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_instance = TKCWoInfo.objects.get(id=wo_id)     
    circles = Tag_Circle.objects.filter(wo_no=wo_id)
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id) 
     
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1) 
         
    if identifier == 1 :
        if tkc_update_boq.objects.filter(wo=wo_id).exists():
            exist_data = tkc_update_boq.objects.filter(wo=wo_id)
            exist_data.delete() 
            print("delete")          
        
    else:
        pass                
        
    for i in boq_data:   
        item_name = i.item_code  
        material_name = i.material_name
        total_order_qty= i.total_order_qty
        circle_boq_data = request.POST.getlist(item_name)
        for j,k in zip(circle_boq_data,circle_list): 
            if j in validators.EMPTY_VALUES:
                m = None
            else:
                m = float(j)
            data = tkc_update_boq(wo=wo,boq_item=i, circle_quantity=m, material_name=material_name, item_code=item_name, total_order_qty=total_order_qty, circles_name=k.circle_name, updated_at=datetime.datetime.now(), created_at=datetime.datetime.now())
            data.save()
            wo.is_boq_added  = 5
            wo.save()
    items_qty = {}
    for req in boq_data:
        item_name = req.item_code
        circle_boq_data = request.POST.getlist(item_name)  
        items_qty[item_name] = circle_boq_data       

    # print("{{{{{{{{{{{}}}}}}}}}}}", items_qty)
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)   
    
    if len(stored_data) != 0:           
        item_code_list = []
        item_dict = {}        
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)            
            for k in stored_item_data:                
                if k.circle_quantity == None:
                    k.circle_quantity = ''
                item_qty_list.append(k.circle_quantity)
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list                            
             
    else:
        item_dict = 0
        circle_list = 0
    print("{{{{{{dict}}}}}}", item_dict)
    wo_data = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
    if wo.is_boq_added  == 5:
        wo.is_boq_added = 1
        wo.save()
        return render(request, 'fqp/wo_creater/update_boq.html',{"wo":wo_data})
        
    else:
        return render(request, 'fqp/wo_creater/update_boq_edit.html',
                    {"officer": officer, 'wo': wo_data, "item_dict": item_dict, "boq_data": boq_data, "circles":circles, "wo_instance":wo_instance,"circle_list":circle_list})

    
    
def update_boq_edit(request,wo_id): 
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_instance = TKCWoInfo.objects.get(id=wo_id)     
    circles = Tag_Circle.objects.filter(wo_no=wo_id)
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)   
     
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1)  

    stored_data = tkc_update_boq.objects.filter(wo=wo_id) 
    if len(stored_data) != 0:    
        item_code_list = []
        item_dict = {}
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)
            for k in stored_item_data:
                if k.circle_quantity == None:
                    k.circle_quantity = ''                    
                item_qty_list.append(int(k.circle_quantity))
                circle_list.append(k.circles_name)
            item_qty_list.append(sum(item_qty_list))
            item_dict[j]=item_qty_list   
            
    else:
        item_dict = 0
        circle_list = 0

    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
    return render(request, 'fqp/wo_creater/update_boq_edit.html',
                    {"officer": officer, 'wo': wo, "item_dict": item_dict, 'stored_data':stored_data, "boq_data": boq_data, "circles":circles, "wo_instance":wo_instance,"circle_list":circle_list})



#verify boq at approver side
def proj_verify_boq_list(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
    return render(request, 'fqp/wo_approver/proj_verify_boq_list.html',
                {"officer": officer, 'wo': wo})
    
def proj_verify_boq_info(request, wo_id):  
    officer = Officer.objects.get(employ_id=request.session['employ_id'])   
         
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)    
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id)  
    stored_data = tkc_update_boq.objects.filter(wo=wo_id, gm_status=1)
    if len(stored_data) == 0 :
        circle = " "
        
    circle_lst = []
    for i in stored_data:
        circle = i.circles_name
        if circle in circle_lst:
            pass
        else:
            circle_lst.append(circle)
    len_circle_lst = len(circle_lst)
    len_tag_circle = len(circles) 
     
    pma = []
    gm = []   
    for i in stored_data:
        pma.append(i.pma_boq_recommendation)
        gm.append(i.gm_boq_recommendation)
    pma_recommendation_data = set(pma)
    gm_recommendation_data = set(gm)   
    
    if len(stored_data) != 0 :    
        item_code_list = []
        circle = []
        
        item_dict = {}        
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            item_qty_list = []  
                      
            stored_item_data = tkc_update_boq.objects.filter(item_code=j,wo=wo_id).order_by('id')
            for k in stored_item_data:                
                circle.append(k.circles_name)          
                
                item_qty_list.append(k.circle_quantity)
                item_qty_list.append(k.gm_verified_circle_qty)                           
            item_dict[j]=item_qty_list               
           

    else:
        item_dict = 0 
        circle_list = 0 
    
    approved_circle = []
    [approved_circle.append(x) for x in circle if x not in approved_circle]
     
      
    return render(request, 'fqp/wo_approver/proj_verify_boq_info.html',
                {"officer": officer, 'wo': wo, 'len_tag_circle':len_tag_circle,'len_circle_lst':len_circle_lst, 'gm_recommendation_data':gm_recommendation_data, 'pma_recommendation_data':pma_recommendation_data, 'approved_circle':approved_circle, 'boq_data':boq_data, 'requested_data':requested_data, 'stored_data':stored_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})
    
    
def proj_accept_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])    
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)     
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)     
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id)  
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)      
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)
    
    circle_lst = []
    for i in stored_data:
        circle = i.circles_name
        if circle in circle_lst:
            pass
        else:
            circle_lst.append(circle)
    len_circle_lst = len(circle_lst)
    len_tag_circle = len(circles)  
    
    
    for i in stored_data:
        pma_recommendation_data = i.pma_boq_recommendation
        gm_recommendation_data= i.gm_boq_recommendation
   
    
    approved_circle = []
    for i in stored_data:
        approved_circle.append(i.circles_name)
    approved_circle = set(approved_circle)
    
    data = tkc_update_boq.objects.filter(wo=wo_id)
    for k in data:
        k.Officer_name = officer.employ_name
        k.updated_at = datetime.datetime.now()
        k.save() 
    
    wo.approver_status=1
    wo.save()
        
    if len(stored_data) != 0 :    
        item_code_list = []
        item_dict = {}        
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            item_qty_list = [] 
            stored_item_data = tkc_update_boq.objects.filter(item_code=j,wo=wo_id).order_by('id')            
            for k in stored_item_data:
                # item_qty_list.append(k.circle_quantity)
                item_qty_list.append(k.gm_verified_circle_qty)                
            item_dict[j]=item_qty_list 
            a = sum(item_qty_list)
            total = "{:.2f}".format(a)
            data = tkc_wo_items_boq.objects.get(wo=wo, item_code= j)
            data.old_loa_qty = data.total_order_qty
            data.total_order_qty = total
            data.save()
            if (float(data.total_order_qty)) >= float(data.old_loa_qty):
                data.balance_qty = float(data.balance_qty) + (float(data.total_order_qty) - float(data.old_loa_qty))  
                data.save() 
            elif (float(data.total_order_qty)) <= float(data.old_loa_qty):
                data.balance_qty = float(data.balance_qty) + (float(data.old_loa_qty) - float(data.total_order_qty))  
                data.save() 

    else:
        item_dict = 0 
        circle_list = 0                      
                 
    
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')        
    return render(request, 'fqp/wo_approver/proj_verify_boq_list.html',
                {"officer": officer, 'wo': wo, 'len_tag_circle':len_tag_circle, 'len_circle_lst':len_circle_lst, 'gm_recommendation_data':gm_recommendation_data, 'pma_recommendation_data':pma_recommendation_data, 'approved_circle':approved_circle, 'boq_data':boq_data, 'requested_data':requested_data, 'stored_data':stored_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})


def proj_view_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])    
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)     
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)       
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id)     
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)
    
    circle_lst = []
    for i in stored_data:
        circle = i.circles_name
        if circle in circle_lst:
            pass
        else:
            circle_lst.append(circle)
    len_circle_lst = len(circle_lst)
    len_tag_circle = len(circles)  
    
    for i in stored_data:
        pam_recommendation_data = i.pma_boq_recommendation
        gm_recommendation_data= i.gm_boq_recommendation
   
    
    approved_circle = []
    for i in stored_data:
        approved_circle.append(i.circles_name)
    approved_circle = set(approved_circle)
    

    if len(stored_data) != 0 :    
        item_code_list = []
        item_dict = {}        
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            item_qty_list = []            
            stored_item_data = tkc_update_boq.objects.filter(item_code=j,wo=wo_id).order_by('id')            
            for k in stored_item_data:
                item_qty_list.append(k.circle_quantity)
                item_qty_list.append(k.gm_verified_circle_qty)                
            item_dict[j]=item_qty_list              
           

    else:
        item_dict = 0 
        circle_list = 0  
  
    
    wo.approver_status=1
    wo.save()         
    
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
        
    return render(request, 'fqp/wo_approver/proj_view_boq.html',
                {"officer": officer, 'wo': wo, 'len_tag_circle':len_tag_circle, 'len_circle_lst':len_circle_lst, 'gm_recommendation_data':gm_recommendation_data, 'pam_recommendation_data':pam_recommendation_data, 'approved_circle':approved_circle, 'boq_data':boq_data, 'requested_data':requested_data, 'stored_data':stored_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})


         
def proj_reject_boq(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id']) 
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)       
    stored_circle_data = tkc_update_boq.objects.filter(wo=wo_id)
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id) 
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id)
    wo.approver_status=2
    wo.save()
    mgs= "BOQ Quantity has been Rejected"
    
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)   
    return render(request, 'fqp/wo_approver/proj_reject_boq.html',
                {"officer": officer, 'wo': wo, 'mgs':mgs, 'wo_instance':wo_instance})
    
    
# ********************************************* BOQ Code *****************************************************************


# ------------------------------shubham tripathi code start from here----------16 march 2023-------------
def officer_fqpintimation(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        wo_data = FqpIntimation.objects.filter(wo_id__Discom_id=officer.Discom_id).distinct('wo__id')
        if officer.role.Role_Name =="WO_CREATER":
            return render(request, 'fqp/wo_creater/fqpintimation/wo_intimation.html', {'officer': officer,'wo_data':wo_data})
        elif officer.role.Role_Name =="WO_APPROVER":
            # wo_data = TKCWoInfo.objects.filter(Discom_id=officer.Discom_Id)
            return render(request, 'fqp/wo_approver/fqpintimation/wo_intimation.html', {'officer': officer,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'mpeb_login')


def officer_fqpintimation_list(request):
    wo_id=request.GET.get('woid')
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        wo_fqpi_data=FqpIntimation.objects.filter(~Q(status=-1),wo_id=wo_id)
        wo_data=TKCWoInfo.objects.filter(Discom_id=officer.Discom_id,id=wo_id)
        if officer.role.Role_Name =="WO_CREATER":
            return render(request, 'fqp/wo_creater/fqpintimation/tkc_intimation_list.html', {'officer': officer,'wo_fqpi_data':wo_fqpi_data,'wo_data':wo_data})
        elif officer.role.Role_Name =="WO_APPROVER":
            return render(request, 'fqp/wo_approver/fqpintimation/tkc_intimation_list.html', {'officer': officer,'wo_fqpi_data':wo_fqpi_data,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'mpeb_login')

def officer_fqpintimation_observation_detail(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        fqpintimation_id = request.GET.get('fqpintimation_id')
        int_data=FqpIntimation.objects.filter(id=fqpintimation_id)
        observation_data=FqpIntimation_Observation_Info.objects.filter(fqpintimation_id=fqpintimation_id)
        officer_data=FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id)
        close_inti=FqpIntimation_Observation_Close.objects.filter(fqpintimation_id=fqpintimation_id)
        if officer.role.Role_Name =="WO_CREATER":
            return render(request, 'fqp/wo_creater/fqpintimation/tkc_fqpintimation_observation_detail.html', {'officer': officer,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation_data':observation_data})
        elif officer.role.Role_Name =="WO_APPROVER":
            return render(request, 'fqp/wo_approver/fqpintimation/tkc_fqpintimation_observation_detail.html', {'officer': officer,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation_data':observation_data})
    else:
        return redirect(str(curl)+'mpeb_login')
# ------------------shubham tripahti code end here-----------------------------------------------------


#  --------------shubham tripathi code start here-----------------
# from main.views import *
from django.db.models import Sum
from django.db.models import Count
import os

curl=settings.CURRENT_URL

def wo_officer_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()
    if officer is not None:
        order_type=request.GET.get('ordertype')
        if ((officer.role.Role_Name == "WO_CREATER" or officer.role.Role_Name == "GM" or officer.role.Role_Name == "DGM")):
            wo_data = TKCWoInfo.objects.annotate(total_invoice_ammount=Sum('work_order_data__total_invoice_amount'),num_invoice=Count('work_order_data')).filter(Wo_Approved_Status=1,Discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'fqp/wo_invoice/officer_creater_wo_invoicelist.html', {'officer': officer,'wo_amt':wo_amt,'wo_data':wo_data})
        
        elif ((officer.role.Role_Name == "GM(CIRCLE)")):
            wo_data = TKCWoInfo.objects.annotate(total_invoice_ammount=Sum('work_order_data__total_invoice_amount'),num_invoice=Count('work_order_data')).filter(Wo_Approved_Status=1,Discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'fqp/wo_invoice/tkc_gm_circle_wo_invoice_list.html', {'officer': officer,'wo_amt':wo_amt,'wo_data':wo_data})
        
        elif ((officer.role.Role_Name == "DGM_STC")):
            wo_data = TKCWoInfo.objects.annotate(total_invoice_ammount=Sum('work_order_data__total_invoice_amount'),num_invoice=Count('work_order_data')).filter(Wo_Approved_Status=1,Discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'fqp/wo_invoice/tkc_dgm_stc_wo_invoice_list.html', {'officer': officer,'wo_amt':wo_amt,'wo_data':wo_data})

        elif ((officer.role.Role_Name == "DGM_ONM")):
            wo_data = TKCWoInfo.objects.annotate(total_invoice_ammount=Sum('work_order_data__total_invoice_amount'),num_invoice=Count('work_order_data')).filter(Wo_Approved_Status=1,Discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'fqp/wo_invoice/tkc_dgm_onm_wo_invoice_list.html', {'officer': officer,'wo_amt':wo_amt,'wo_data':wo_data})

        elif ((officer.role.Role_Name == "WO_APPROVER" or officer.role.Role_Name == "CGM")):
            wo_data = TKCWoInfo.objects.annotate(total_invoice_ammount=Sum('work_order_data__total_invoice_amount'),num_invoice=Count('work_order_data')).filter(Wo_Approved_Status=1,Discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'fqp/wo_invoice/officer_approver_wo_invoicelist.html', {'officer': officer,'wo_amt':wo_amt,'wo_data':wo_data})
        
        elif ((officer.role.Role_Name == "CFO" or officer.role.Role_Name == "AO_BILLS" or officer.role.Role_Name == "DGM_EM" or officer.role.Role_Name == "DGM_CBPU")):
            wo_data = TKCWoInfo.objects.annotate(total_invoice_ammount=Sum('work_order_data__total_invoice_amount'),num_invoice=Count('work_order_data')).filter(Wo_Approved_Status=1,Discom_id=officer.Discom_id,num_invoice__gt=0).order_by('-id')
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'fqp/wo_invoice/finance_officer_woinvoice_list.html', {'officer': officer,'wo_amt':wo_amt,'wo_data':wo_data})

    else:
        return redirect(str(curl)+'mpeb_login')



def wo_approver_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        if request.method == "POST" and officer.role.Role_Name == "WO_APPROVER":
            order_type=request.GET.get('ordertype')
            wo_id=request.POST.get('wo_id')
            invoice_id=request.POST.get('invoice_id')
            status=request.POST.get('status')
            officer_id=request.POST.get('officer_id')

            if int(status) == 1:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=3,assign_officer_id=officer_id)
                return redirect(wo_officer_invoice_list)
            else:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
                return redirect(wo_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            wo_id=request.GET.get('woid')
            wo_data=TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id,Discom_id=officer.Discom_id).last()
            ofdata=Officer.objects.filter(role__Role_Name=("WO_CREATER"),Discom_id=wo_data.Discom_id)
            wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
            in_data = Invoice.objects.filter(~Q(status=-1),work_order_id=wo_id,order_type = order_type).order_by('-id')
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,work_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'fqp/wo_invoice/wo_approver_invoice_list.html', {"officer":officer,"ofdata":ofdata,'wo_data':wo_data,"in_data":in_data,'in_amount':in_amount,'wo_amt':wo_amt})
    else:
        return redirect(str(curl)+'mpeb_login')

def wo_approver_invoice(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "WO_APPROVER":
            order_type=request.GET.get('ordertype')        
            wo_id=request.POST.get('wo_id')
            invoice_id=request.POST.get('invoice_id')
            cgm_status=request.POST.get('cgm_status')
            cgm_remark=request.POST.get('cgm_remark')
            gm_status=request.POST.get('gm_status')
            if int(cgm_status) == 1 and int(gm_status) == 1:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=5,cgm_remark=cgm_remark,cgm_status=cgm_status)
            elif int(cgm_status) == 1 and int(gm_status) == 2:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=3,cgm_remark=cgm_remark,cgm_status=cgm_status)
            else:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=cgm_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name,cgm_status=cgm_status,cgm_remark=cgm_remark)
            
            inup = Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).last()
            try:
                cgm_document = request.FILES['cgm_document']
                print("cgm_document--------------",cgm_document,"------cname-----",cgm_document.name)
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
        return redirect(wo_officer_invoice_list)
    else:
        return redirect(str(curl)+'mpeb_login')

def wo_creator_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "WO_CREATER":
            order_type=request.GET.get('ordertype')        
            wo_id=request.POST.get('wo_id')
            invoice_id=request.POST.get('invoice_id')
            gm_status=request.POST.get('gm_status')
            gm_remark=request.POST.get('gm_remark')
            if int(gm_status) == 1:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=4,gm_remark=gm_remark,gm_status=gm_status)
            else:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=4,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name,gm_status=gm_status,gm_remark=gm_remark)
            
            inup = Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).last()
            try:
                gm_document = request.FILES['gm_document']
                print("gm documen--------------",gm_document,"------name-----",gm_document.name)
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
            return redirect(wo_officer_invoice_list)

        else:
            order_type=request.GET.get('ordertype')
            wo_id=request.GET.get('woid')
            wo_data=TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id,Discom_id=officer.Discom_id).last()
            # pomd = wO_Material.objects.filter(~Q(status=-1),wo_id=wo_id).aggregate(Sum('total_amount'))
            wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
            in_data=Invoice.objects.filter(status__in=[5,0,1,2,3,4],assign_officer_id=officer.employ_id,work_order_id=wo_id,order_type = order_type)
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,work_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'fqp/wo_invoice/wo_creater_invoice_list.html', {'officer': officer,'wo_data':wo_data,'wo_amt':wo_amt,"in_data":in_data,'in_amount':in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def wo_cfo_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "CFO":
            order_type=request.GET.get('ordertype')        
            wo_id=request.POST.get('wo_id')
            invoice_id=request.POST.get('invoice_id')
            cfo_status=request.POST.get('cfo_status')
            cfo_remark=request.POST.get('cfo_remark')
            dgm_cbpu_status=request.POST.get('dgm_cbpu_status')

            if int(cfo_status) == 1 and int(dgm_cbpu_status) == 0:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(cfo_remark=cfo_remark,cfo_status=cfo_status)
            elif int(cfo_status) == 1 and int(dgm_cbpu_status) == 2:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(dgm_cbpu_status=3,cfo_remark=cfo_remark,cfo_status=cfo_status)
            else:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(cfo_remark=cfo_remark,cfo_status=cfo_status,status=cfo_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
                
            inup = Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).last()

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
            return redirect(wo_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            wo_id=request.GET.get('woid')
            TKCWoInfo
            wo_data=TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id,Discom_id=officer.Discom_id).last()
            wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
            in_data = Invoice.objects.filter(status__in=[1,2,5],work_order_id=wo_id,order_type = order_type,gm_status=1,cgm_status=1)
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,work_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'fqp/wo_invoice/wo_cfo_invoicelist.html', {"officer":officer,"wo_amt":wo_amt,'wo_data':wo_data,"in_data":in_data,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def wo_dgmcbpu_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # orole=officer.role.Role_Name
        if request.method == "POST" and officer.role.Role_Name == "DGM_CBPU":
            order_type=request.GET.get('ordertype')        
            wo_id=request.POST.get('wo_id')
            invoice_id=request.POST.get('invoice_id')
            dgm_cbpu_status=request.POST.get('dgm_cbpu_status')
            dgm_cbpu_remark=request.POST.get('dgm_cbpu_remark')
            ao_bills_status=request.POST.get('ao_bills_status')

            if int(dgm_cbpu_status) == 1 and int(ao_bills_status) == 0:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(dgm_cbpu_remark=dgm_cbpu_remark,dgm_cbpu_status=dgm_cbpu_status)
            elif int(dgm_cbpu_status) == 1 and int(ao_bills_status) == 2:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(ao_bills_status=3,dgm_cbpu_remark=dgm_cbpu_remark,dgm_cbpu_status=dgm_cbpu_status)
            else:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(cfo_status=3,dgm_cbpu_remark=dgm_cbpu_remark,dgm_cbpu_status=dgm_cbpu_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
            
            inup = Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).last()
            
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
            except Exception as e:
                pass
            return redirect(wo_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            wo_id=request.GET.get('woid')
            wo_data=TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id,Discom_id=officer.Discom_id).last()
            wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
            in_data=Invoice.objects.filter(status__in=[1,2,5],work_order_id=wo_id,order_type = order_type,gm_status=1,cgm_status=1,cfo_status__in=[1,3])
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,work_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'fqp/wo_invoice/wo_cbpu_invoicelist.html', {'officer': officer,'wo_data':wo_data,"in_data":in_data,"wo_amt":wo_amt ,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def wo_aubills_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        if request.method == "POST" and officer.role.Role_Name == "AO_BILLS":
            order_type=request.GET.get('ordertype')        
            wo_id=request.POST.get('wo_id')
            invoice_id=request.POST.get('invoice_id')
            ao_bills_status=request.POST.get('ao_bills_status')
            ao_bills_remark=request.POST.get('ao_bills_remark')
            dgm_em_status=request.POST.get('dgm_em_status')
            if int(ao_bills_status) == 1 and int(dgm_em_status) == 0:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(ao_bills_remark=ao_bills_remark,ao_bills_status=ao_bills_status)
            elif int(ao_bills_status) == 1 and int(dgm_em_status) == 2:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(dgm_em_status=3,ao_bills_remark=ao_bills_remark,ao_bills_status=ao_bills_status)                
            else:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(dgm_cbpu_status=3,ao_bills_remark=ao_bills_remark,ao_bills_status=ao_bills_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
            inup = Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).last()
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
            return redirect(wo_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            wo_id=request.GET.get('woid')
            wo_data=TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id,Discom_id=officer.Discom_id).last()
            wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
            in_data=Invoice.objects.filter(status__in=[1,2,5],work_order_id=wo_id,order_type = order_type,gm_status=1,dgm_cbpu_status__in=[1,3])
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,work_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'fqp/wo_invoice/wo_aubills_invoicelist.html', {'officer': officer,'wo_data':wo_data,"in_data":in_data,"wo_amt":wo_amt,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

def wo_dgmem_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        if request.method == "POST" and officer.role.Role_Name == "DGM_EM":
            order_type=request.GET.get('ordertype')        
            wo_id=request.POST.get('wo_id')
            invoice_id=request.POST.get('invoice_id')
            dgm_em_status=request.POST.get('dgm_em_status')
            dgm_em_remark=request.POST.get('dgm_em_remark')
            if int(dgm_em_status) == 1:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=1,dgm_em_remark=dgm_em_remark,dgm_em_status=dgm_em_status)
            else:
                Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(ao_bills_status=3,dgm_em_remark=dgm_em_remark,dgm_em_status=dgm_em_status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
            inup = Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).last()
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
            return redirect(wo_officer_invoice_list)
        else:
            order_type=request.GET.get('ordertype')
            wo_id=request.GET.get('woid')
            wo_data=TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id,Discom_id=officer.Discom_id).last()
            wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
            in_data=Invoice.objects.filter(status__in=[1,2,5],work_order_id=wo_id,order_type = order_type,gm_status=1,cgm_status=1,cfo_status=1,ao_bills_status__in=[1,3])
            in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,work_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
            return render(request, 'fqp/wo_invoice/wo_dgmem_invoicelist.html', {'officer': officer,'wo_data':wo_data,"in_data":in_data,"wo_amt":wo_amt,"in_amount":in_amount})
    else:
        return redirect(str(curl)+'mpeb_login')

#-----------------shubham tripathi code end here-----------------------------------
#-----------------Below Code Added By Aayush Joshi for API-Integration Process-----------------------------------------------

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Added By Aayush Joshi
def fetch_gbpa_order_view(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    User_type = User_Registration.objects.filter(cgm_approval=1, User_type='TKC')
    return render(request, 'fqp/wo_creater/fetch_gbpa_order.html',{"User_type": User_type,"officer": officer})

#Added By Aayush Joshi
def checking_if_gbpa_no_and_revision_present_in_db(request,gbpa_no):
    data = TKCWoInfo.objects.all()
    len_data =len(data)
    
    count=0
    for i in data:
        count=count+1
        if gbpa_no == i.Contract_Number: 
            print("-------------gbpa_no found already present -------------------",gbpa_no)
            gbpa_val = i.Contract_Number
            print("gbpa_val-----", gbpa_val)
            return True
        if count == len_data:
            return False


#Added By Aayush Joshi
def gbpa_api_call(request):
    print("in gbpa_api_call")
    if request.method == "POST":
        gbpa_no=request.POST.get("gbpa_no")

        # URL=const.tkc_po_header_api
        # URL="http://ebssitapp1.mpezerp.com:8001/webservices/rest/xxtkc_turnkey_po_hdr_pkg/get_tkc_po_hdr_details/"
        URL="http://epic.mpezerp.com:80/webservices/rest/XXTKC_TURNKEY_PO_HDR_PKG/get_tkc_po_hdr_details/"
        data={
        "get_TKC_po_hdr_details": {
            "@xmlns": "http://xmlns.oracle.com/apps/po/rest/xxtkc_turnkey_po_hdr_pkg/get_tkc_po_hdr_details/",
            "RESTHeader":{
                "xmlns":"http://xmlns.oracle.com/apps/fnd/rest/header",
                "Responsibility":"JAI_PURCHASING",
                "RespApplication":"JA",
                "SecurityGroup":"STANDARD",            
                "NLSLanguage": "AMERICAN" 
                
                
            },
            "InputParameters": {
                "P_GBPA_NO": gbpa_no,
                "P_CREATION_DATE":"",
                "P_SCHEME_CODE":""
            }
                }
            }

        json_data = json.dumps(data)
        auth_values = HTTPBasicAuth(const.Username, const.Password)
        # try:
            # print('in try:::::')
            #calling API here with all the payload and endpoint details.

        res = req.post(url=URL, auth=auth_values, headers=const.headers, data=json_data) 
        approved_tk_vendor=User_Registration.objects.filter(cgm_approval=1, User_type='TKC') 
        
        if res.status_code == 200:
            print("code matched")
            tkcheader_data = res.json()
            if tkcheader_data['OutputParameters']['P_TKC_PO_HDR_REC']==None:
                message =messages.error(request, f'Unable to create Workorder for GBPA No.{gbpa_no} as it is invalid.')
                officer = Officer.objects.get(employ_id=request.session['employ_id'])
                return render(request, 'fqp/wo_creater/fetch_gbpa_order.html', {'message': message,"User_type": approved_tk_vendor,"officer": officer})

            def validate_supplier_and_gbpa_with_api_data(request,tkcheader_data,gbpa_no):
                # print("in validate_supplier_and_gbpa_with_api_data")
                user_entered_supplier_name=request.POST.get('vendor')
                tkcheader_data=tkcheader_data['OutputParameters']['P_TKC_PO_HDR_REC']['P_TKC_PO_HDR_REC_ITEM'] 
                api_fetched_supplier_name=tkcheader_data[0]['VENDOR_NAME']
                contract_number=tkcheader_data[0]['ORDER_NUMBER']
               
                if user_entered_supplier_name in api_fetched_supplier_name and gbpa_no == contract_number:
                    # print("gbpa and supplier name matched.")
                    return True,api_fetched_supplier_name
                else:
                    # print("gbpa and supplier name not matched.")
                    return False,api_fetched_supplier_name
            
            if tkcheader_data['OutputParameters']['P_TKC_PO_HDR_REC'] is not None:
                print("#validating user_entered_data with API data.")
                status,api_fetched_supplier_name=validate_supplier_and_gbpa_with_api_data(request,tkcheader_data,gbpa_no)
                if status == True:
                    #checking if gbpa no is already present in db , if it already present we should update it on the basis of revison value ,else we need to create a new entry for the same . 
                    if checking_if_gbpa_no_and_revision_present_in_db(request,gbpa_no) == False:
                        created_wo=tkc_po_header_data_insertion(request,tkcheader_data)
                        is_data_inserted,creation_date=tkc_po_header_data_insertion_two(request,tkcheader_data,created_wo)
                        if is_data_inserted:
                            bool,data=po_line_api_call(request,gbpa_no)
                            if bool == True and data:
                                # approved_tk_vendor_ids=User_Registration.objects.filter(cgm_approval=1, User_type='TKC').values("User_Id")   
                                if tkc_po_line_api_data_insertion(request,data,created_wo):
                                    print("cool data of all schedules with items and  all  installation with items all are added successfully.")
                                    # message =messages.success(request, f'New Work Order Created for GBPA {gbpa_no}')
                                    # return render(request, 'fqp/wo_creater/fetch_gbpa_order.html', {'message': message,"User_type": approved_tk_vendor,"supplier_id":supplier_id})
                                    bool_val,del_sch_data=get_del_sch_api_call(request,gbpa_no,creation_date)
                                    print("bool_val,del_sch_data---->",bool_val,del_sch_data)
                                    if bool_val == True and del_sch_data:
                                        message_rendered = False
                                        if schedule_time_api_data_insertion(request,del_sch_data,created_wo):
                                            officer = Officer.objects.get(employ_id=request.session['employ_id'])
                                            wo = TKCWoInfo.objects.get(id=created_wo.id)
                                            form = Term_And_Condition()
                                            message =messages.success(request, f'New Work Order Created for GBPA {gbpa_no}')
                                            message_rendered = True
                                            return render(request, 'fqp/wo_creater/generate_wo10.html',
                                                        {"officer": officer, 'wo': wo, 'form': form,'message_rendered':message_rendered})
                                    elif bool_val == False and del_sch_data == False:
                                        officer = Officer.objects.get(employ_id=request.session['employ_id'])
                                        wo = TKCWoInfo.objects.get(id=created_wo.id)
                                        form = Term_And_Condition()
                                        message =messages.success(request, f'New Work Order Created for GBPA {gbpa_no}')
                                        message_rendered = True
                                        return render(request, 'fqp/wo_creater/generate_wo10.html',
                                                    {"officer": officer, 'wo': wo, 'form': form,'message_rendered':message_rendered})


                    else:
                        selected_supplier_id=User_Registration.objects.filter(cgm_approval=1, User_type='TKC',CompanyName_E=api_fetched_supplier_name).values("User_Id")  
                        # print("selected_supplier_id=====>",selected_supplier_id[0]['User_Id'])
                        selected_supplier_object=TKCWoInfo.objects.get(Contract_Number=gbpa_no,supplier_id=selected_supplier_id[0]['User_Id'])
                        # print(" selected_supplier_object:====>", selected_supplier_object.id)
                        # print("THIS GBPA FOR SUPPLIER ALREADY PRESENT SO WE , Need to Update the Already Present GBPA No.")
                        message =messages.info(request, f'GBPA No. {gbpa_no} FOR THESE SUPPLIER ALREADY PRESENT.')
                        officer = Officer.objects.get(employ_id=request.session['employ_id'])
                        return render(request, 'fqp/wo_creater/fetch_gbpa_order.html', {'message': message,"User_type": approved_tk_vendor,"supplier_id":selected_supplier_object.id,"officer": officer})
                else:
                    officer = Officer.objects.get(employ_id=request.session['employ_id'])
                    message =messages.error(request, f'Unable to create Workorder for GBPA No.{gbpa_no} as it is belongs to {api_fetched_supplier_name}.')
                    return render(request, 'fqp/wo_creater/fetch_gbpa_order.html', {'message': message,"User_type": approved_tk_vendor,"officer": officer})
                    
        else:
            print("in else : api code 400,500,404 etc.",res.status_code)
        # except Exception as e:
        #     print("in exception ",e)
        #     error_in_response ="API IS NOT RESPONDING..... "
        #     print("error_in_response===>",error_in_response)
    else:
        print("in else gbpa api")
        return fetch_gbpa_order_view(request)

#Added By Aayush
def get_del_sch_api_call(request,gbpa_no,creation_date):
    print("in get_del_sch_api_call ,get_del_sch_api_call")
    # URL="http://ebssitapp1.mpezerp.com:8001/webservices/rest/XXTKC_DEL_SCH_API_PKG/get_del_sch_details/"
    URL="http://epic.mpezerp.com:80/webservices/rest/XXTKC_DEL_SCH_API_PKG/get_del_sch_details/"
    
    data={
    "get_del_sch_details": {
        "@xmlns": "http://xmlns.oracle.com/apps/po/rest/ XXTKC_DEL_SCH_API_PKG/get_del_sch_details/",
        "RESTHeader": {
            "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
            "Responsibility": "JAI_PURCHASING",
            "RespApplication": "JA",
            "SecurityGroup": "STANDARD",
            "NLSLanguage": "AMERICAN",
            "Org_Id": "83"
        },
        "InputParameters": {
            "P_GBPA_NUM":gbpa_no,
            "P_CREATION_DATE":creation_date

        }
    }
}

    json_data = json.dumps(data)
    auth_values = HTTPBasicAuth("QC_EBS_USER", "Qc_ebs@23")
    # try:
        # print('in try:::::')
        #calling API here with all the payload and endpoint details.
    res = req.post(url=URL, auth=auth_values, headers=const.headers, data=json_data) 
    approved_tkc_vendor=User_Registration.objects.filter(cgm_approval=1, User_type='TKC')
    if res.status_code == 200:
        print("----code matched---")
        tkcheader_data = res.json()
        if tkcheader_data['OutputParameters']['P_TKC_DESCH_REC']==None:
            print("heerer")
            # message =messages.info(request, f'Unable to create Workorder for GBPA No.{gbpa_no} as it is invalid.')
            # officer = Officer.objects.get(employ_id=request.session['employ_id'])
            # return render(request, 'fqp/wo_creater/fetch_gbpa_order.html', {'message': message,"User_type": approved_tkc_vendor,"officer": officer})
            return False,False
        else:
            print("in else---",res.status_code,tkcheader_data)
            return True,tkcheader_data
    else:
        print("======22222========in else==============")
        return False,False

#Added By Aayush
def tkc_po_header_data_insertion(request,tkcheader_data):

    tkcheader_data=tkcheader_data['OutputParameters']['P_TKC_PO_HDR_REC']['P_TKC_PO_HDR_REC_ITEM'] 
    length_tkcheader_data=len(tkcheader_data)
    
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    discom = Discom_Master.objects.get(Discom_Code=officer.user_zone)

    try:
        vendor_name = User_Registration.objects.get(CompanyName_E=tkcheader_data[0]['VENDOR_NAME'])
        User_type = User_Registration.objects.filter(cgm_approval=1, User_type='TKC')
    except:
        message =messages.info(request, f'Unable to Create Work Order for the supplier:{vendor_name}, as this Supplier is not registered Yet.')
        officer = Officer.objects.get(employ_id=request.session['employ_id'])
        return render(request, 'fqp/wo_creater/fetch_gbpa_order.html', {'message': message,"User_type": User_type,"officer": officer})

    wo = TKCWoInfo(supplier=vendor_name, Discom=discom, zone=officer.user_zone,
    Contract_Number=tkcheader_data[0]['ORDER_NUMBER'],
    Supplier_Erp_no=tkcheader_data[0]['VENDOR_ID'],
    price=tkcheader_data[0]['AMOUNT_LIMIT'],
    Contract_Date=date_format_conversion(tkcheader_data[0]['APPROVED_DATE']),
    Contract_Effective_Date=date_format_conversion(tkcheader_data[0]['EFFECTIVE_DATE']),Status=1)
    wo.save()

    #Advances data insertion
    keys_to_check = ["MATADV_PERC", "EREADV_PERC", "PERSEC_PERC", "MAJMATADV_PERC"]

    for key in keys_to_check :
        if key in tkcheader_data[0]:
            if key == "MATADV_PERC":
                name='Materials Advance'
                percentage_amount=tkcheader_data[0]['MATADV_PERC']
            elif key == 'EREADV_PERC':
                name='Material Erection Advance'
                percentage_amount=tkcheader_data[0]['EREADV_PERC']
            elif key == 'PERSEC_PERC':
                name='Performance Security'
                percentage_amount=tkcheader_data[0]['PERSEC_PERC']
            elif key == 'MAJMATADV_PERC':
                name='Major Material Advance'
                percentage_amount=tkcheader_data[0]['MAJMATADV_PERC']
            
            Advance = TKCWoInfo_Advance(TKCWoInfo=wo, Name=name,
            Amount_Percentage=percentage_amount, Created_At=datetime.datetime.now(),
            Created_By=officer.employ_name, Status=1)
            Advance.save()

    wo = TKCWoInfo.objects.latest('id')
    return wo

#Added By Aayush
def tkc_po_header_data_insertion_two(request,tkcheader_data,wo):
    tkcheader_data=tkcheader_data['OutputParameters']['P_TKC_PO_HDR_REC']['P_TKC_PO_HDR_REC_ITEM'] 
    length_tkcheader_data=len(tkcheader_data)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    discom = Discom_Master.objects.get(Discom_Code=officer.user_zone)
    wo_header = TKCWoInfo_Header(TKCWoInfo=wo, Scheme_code=tkcheader_data[0]['SCHEME_CODE'],
    Scheme_Name=tkcheader_data[0]['SCHEME_NAME'],
    VENDOR_NAME=tkcheader_data[0]['VENDOR_NAME'],
    VENDOR_SITE_CODE=tkcheader_data[0]['VENDOR_SITE_CODE'],
    VENDOR_ADDRESS=tkcheader_data[0]['VENDOR_ADDRESS'],
    VENDOR_COMMUNICATION=tkcheader_data[0]['VENDOR_COMMUNICATION'],
    Payment_Mode=tkcheader_data[0]['PAYMENT_MODE'],
    Payment_Term=tkcheader_data[0]['PAYMENT_TERM'],
    Quotation_No=tkcheader_data[0]['RFQ_NUMBER'],
    Contract_Offer_No=tkcheader_data[0]['SCHEME_CODE'],
    Contract_Description=tkcheader_data[0]['ORDER_DESCRIPTION'],
    Document_Sale_Open_Date=date_and_time_format_conversion(tkcheader_data[0]['RFQ_DATE_OF_SALE_BID_START']),
    Document_Sale_Closed_Date=date_and_time_format_conversion(tkcheader_data[0]['RFQ_DATE_OF_SALE_BID_END']),
    Bid_Submission_Date=date_and_time_format_conversion(tkcheader_data[0]['RFQ_DUE_DATE_OF_SUBMI']),
    Bid_Opening_Date=date_and_time_format_conversion(tkcheader_data[0]['RFQ_DUE_DATE_OF_OPENING']),
    WO_Prefix=tkcheader_data[0]['ORDER_NUMBER'],
    Created_At=date_format_conversion(tkcheader_data[0]['CREATION_DATE']), Created_By=officer, Status=1)               
    wo_header.save()
    wo.Header = TKCWoInfo_Header.objects.latest('id')
    wo.save()
    return True,tkcheader_data[0]['CREATION_DATE']

#Added By Aayush
def date_format_conversion(date_to_format):
    #conversioning "date" data as per preffered-format .
    date_obj = datetime.datetime.strptime(date_to_format, '%d-%b-%Y')
    year, month, day = date_obj.year, date_obj.month, date_obj.day
    # print(year, month, day)
    # Replacing month name with month number
    month_number = datetime.datetime.strptime(date_to_format, "%d-%b-%Y").month
    # Creating the date object with year, month, and day
    date = datetime.date(year, month, day)
    # print("date_format_conversion------->",date)
    return date

#Added By Aayush
def date_format_conversion_other_method(date_to_format):
    print("#conversioning date data as per preffered-format .")
    import datetime
    date_format = '%Y/%m/%d'
    parsed_date = datetime.datetime.strptime(date_to_format, date_format)
    date_only = parsed_date.date()
    print(date_only)
    return date_only

#Added By Aayush
def date_and_time_format_conversion(date_to_format):
    date_obj = datetime.datetime.strptime(date_to_format, '%d-%b-%y %H:%M:%S')
    year, month, day = date_obj.year, date_obj.month, date_obj.day
    # print("date vals year, month, day ",year, month, day )
    # Replacing month name with month number
    month_number = datetime.datetime.strptime(date_to_format, '%d-%b-%y %H:%M:%S').month
    # Creating the date object with year, month, and day
    date= datetime.date(year, month, day)
    # print("date_and_time_format_conversion----",date)
    return date

#Added By Aayush
def po_line_api_call(request,gbpa_no):
    print("in-po_line_api_call ")
    # URL=const.tkc_po_header_api
    # URL="http://ebssitapp1.mpezerp.com:8001/webservices/rest/XXTKC_TURNKEY_POL_DTL_PKG/get_turnkey_pol_details/"
    URL="http://epic.mpezerp.com:80/webservices/rest/XXTKC_TURNKEY_POL_DTL_PKG/get_turnkey_pol_details/"
    data = {
    "get_TKC_po_line_details": {
        "@xmlns": "http://xmlns.oracle.com/apps/po/rest/XXTKC_TURNKEY_POL_DTL_PKG/get_turnkey_pol_details/",
        "RESTHeader":{
            "xmlns":"http://xmlns.oracle.com/apps/fnd/rest/header",
            "Responsibility":"JAI_PURCHASING",
            "RespApplication":"JA",
            "SecurityGroup":"STANDARD",            
            "NLSLanguage": "AMERICAN" 
            
            
        },
        "InputParameters": {
            "P_GBPA_NUM": gbpa_no
            
        }
    }
}

    json_data = json.dumps(data)
    auth_values = HTTPBasicAuth(const.Username, const.Password)
    # try:
        # print('in try:::::')
        #calling API here with all the payload and endpoint details.

    res = req.post(url=URL, auth=auth_values, headers=const.headers, data=json_data)        
    if res.status_code == 200:
        print("code matched")
        tkcheader_data = res.json()
        if tkcheader_data['OutputParameters']['P_TKC_ORDER_REC_TYPE'] is not None:
            # print("GBPA IS VALID ")
            # print(True,tkcheader_data)
            return True,tkcheader_data
        else:
            return False,False
    else:
        print("in else : api code 400,500,404 etc.")
    # except Exception as e:
    #     print("in exception ",e)
    #     error_in_response ="API IS NOT RESPONDING..... "
    #     print("error_in_response===>",error_in_response)


#Added By Aayush
def tkc_po_line_api_data_insertion(request,tkcheader_data,wo):
    #storing supply & installation ("basic-details") from line api data .
    is_sch_supply_data_inserted,sch_supply_obj_list,schedule_no_list=schedule_supply_api_data_insertion(request,tkcheader_data,wo) 
    is_sch_installation_data_inserted,last_added_installation_schedule_obj_list,installation_schedule_no_list=schedule_installation_api_data_insertion(request,tkcheader_data,wo)

    if  is_sch_supply_data_inserted and is_sch_installation_data_inserted == True:
        
        # Note : now we are storing supply & installation ("items") details from line api data .
        is_sch_supply_items_data_inserted,last_added_supply_items_schedule_obj,schedule_no_list=schedule_supply_items_api_data_insertion(request,tkcheader_data,wo,sch_supply_obj_list,schedule_no_list)
        
        is_sch_installation_items_data_inserted,sch_installation_items_obj_list,installation_items_schedule_no_list=schedule_installation_items_api_data_insertion(request,tkcheader_data,wo,last_added_installation_schedule_obj_list,installation_schedule_no_list)
                
        if  is_sch_supply_items_data_inserted and is_sch_installation_items_data_inserted == True:
            print("data insertion completed in 'items table' of both supply and installation table",is_sch_supply_items_data_inserted,last_added_supply_items_schedule_obj)
            return True
   
    elif  is_sch_supply_data_inserted  == True:
        is_sch_supply_items_data_inserted,last_added_supply_items_schedule_obj,schedule_no_list=schedule_supply_items_api_data_insertion(request,tkcheader_data,wo,sch_supply_obj_list,schedule_no_list)
        if  is_sch_supply_items_data_inserted == True:
            print("data insertion completed in 'items table' of  supply table",is_sch_supply_items_data_inserted,last_added_supply_items_schedule_obj,schedule_no_list)
            return True
    else:
        print("There is some problem in storing schedule details in db.")


#Added By Aayush
def schedule_supply_api_data_insertion(request,tkcheader_data,wo):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    schedule_no_list=[]
    last_added_supply_schedule_obj_list=[]
    count = 1
    sch_no_found_on_line_type_supply_count = 0
    for i in range(len(tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM'])):
        indexed_data=tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM'][i]
        
        if indexed_data['LINE_TYPE'] == 'Supply':
            if  indexed_data['SCHEDULE_NO'] not in schedule_no_list and indexed_data['LINE_TYPE'] == 'Supply':
                Supply = TKCWoInfo_Schedule_Supply(TKCWoInfo=wo, Schedule_No=indexed_data['SCHEDULE_NO'],
                                                Schedule_Description=indexed_data['SCHEDULE_DESCRIPTION'],
                                                Unit=indexed_data['ITEM_UOM'],
                                                Quantity=indexed_data['SCHEDULE_QTY'],
                                                Unit_Price_With_Tax=indexed_data['UNIT_PRICE'],
                                                Created_By=officer.employ_name, Status=1)
                Supply.save()
                last_added_supply_schedule_obj=TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo).last()
                if last_added_supply_schedule_obj is not None:
                    schedule_no_list.append(indexed_data['SCHEDULE_NO'])
                    last_added_supply_schedule_obj_list.append(last_added_supply_schedule_obj)
                    sch_no_found_on_line_type_supply_count = sch_no_found_on_line_type_supply_count+1
                    continue
            else:
                count=count+1
                continue
        elif count==len(tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM']) and last_added_supply_schedule_obj_list == None: 
            # print("------- Supplyfull length completed-----Not Found--")
            return False,False,False
        else:
            count=count+1
            continue
    
    if  sch_no_found_on_line_type_supply_count==len(last_added_supply_schedule_obj_list):
            # print(f"sch_no_found_on_line_type_supply_count is :{sch_no_found_on_line_type_supply_count} and last_added_supply_schedule_obj_list values is :,{last_added_supply_schedule_obj_list}")
            return True,last_added_supply_schedule_obj_list,schedule_no_list
    else:
        return False,False,False


def schedule_installation_api_data_insertion(request,tkcheader_data,wo):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    schedule_no_list=[]
    last_added_installation_schedule_obj_list=[]
    count = 1
    sch_no_found_on_line_type_installation_count = 0
    for i in range(len(tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM'])):
        indexed_data=tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM'][i]
        if indexed_data['LINE_TYPE'] == 'Installation':
            # line_type_count=line_type_count+1
            if  indexed_data['SCHEDULE_NO'] not in schedule_no_list and indexed_data['LINE_TYPE'] == 'Installation':
                schedule_no_list.append(indexed_data['SCHEDULE_NO'])
                Supply = TKCWoInfo_Schedule_Installation(TKCWoInfo=wo, Schedule_No=indexed_data['SCHEDULE_NO'],
                                                Schedule_Description=indexed_data['SCHEDULE_DESCRIPTION'],
                                                Unit=indexed_data['ITEM_UOM'],
                                                Quantity=indexed_data['SCHEDULE_QTY'],
                                                Unit_Price_With_Tax=indexed_data['UNIT_PRICE'],
                                                # Created_At=datetime.datetime.now(),
                                                Created_By=officer.employ_name, Status=1
                                                )
                Supply.save()
                last_added_installation_schedule_obj=TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo).last()
                if last_added_installation_schedule_obj is not None:
                    # schedule_no_list.append(indexed_data['SCHEDULE_NO'])
                    last_added_installation_schedule_obj_list.append(last_added_installation_schedule_obj)
                    sch_no_found_on_line_type_installation_count = sch_no_found_on_line_type_installation_count+1
                    continue
            else:
                count=count+1
                continue
        elif count==len(tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM']): 
            print("------- Installation length completed-----Not Found--")
            return False,False,False
        else:
            count=count+1
            continue
    if  sch_no_found_on_line_type_installation_count==len(last_added_installation_schedule_obj_list):
            # print(f"sch_no_found_on_line_type_supply_count is :{sch_no_found_on_line_type_supply_count} and last_added_supply_schedule_obj_list values is :,{last_added_supply_schedule_obj_list}")
            return True,last_added_installation_schedule_obj_list,schedule_no_list
    else:
        return False,False,False


#Added By Aayush
def schedule_supply_items_api_data_insertion(request,tkcheader_data,wo,sch_supply_obj_list,schedule_no_list):
    print("in function schedule_supply_items_api_data_insertion")
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    schedule_no_list_inner=[]
    last_added_supply_schedule_items_obj_list=[]
    tkcheader_data=tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM']
    for j in range(len(sch_supply_obj_list)):
        # print("for loop ka value chl rha h :",j)
        if j == len(sch_supply_obj_list):
            print("length of j completed")
            break
        else:
            indexed_sch_obj=sch_supply_obj_list[j]
            indexed_sch_no_obj=schedule_no_list[j]
            count = 0
            sch_no_found_on_line_type_supply_count = 0
            for i in range(len(tkcheader_data)):
                indexed_data=tkcheader_data[i]

                if count==len(tkcheader_data):
                    print("COUNT WITH LENGTH COMPLETED")
                    break

                if indexed_data['LINE_TYPE'] == 'Supply' and indexed_data['SCHEDULE_NO']==indexed_sch_no_obj:
                    # print("condition matched----with",indexed_sch_no_obj)
                    Supply = TKCWoInfo_Schedule_Supply_Item(TKCWoInfo=wo,
                    Schedule_Supply=indexed_sch_obj,
                    Item_Description=indexed_data['ITEM_DESCRIPTION'],
                    Item_Code=indexed_data['ITEM_CODE'],
                    Unit=indexed_data['ITEM_UOM'],
                    Quantity=indexed_data['SCH_ITEM_QTY'],
                    Unit_Price_With_Tax=indexed_data['UNIT_PRICE'],                                            
                    # Created_At=datetime.datetime.now(),
                    Created_By=officer.employ_name, Status=1)
                    Supply.save()
                    print("just saved Item_Description :",indexed_data['ITEM_DESCRIPTION'],"for indexed_sch_no",indexed_sch_no_obj)
                    last_added_supply_items_schedule_obj=TKCWoInfo_Schedule_Supply_Item.objects.filter(TKCWoInfo=wo).last()
                    # print("last_added_supply_items_schedule_obj----->",last_added_supply_items_schedule_obj)
                    if last_added_supply_items_schedule_obj is not None:
                        if indexed_data['SCHEDULE_NO'] not in schedule_no_list_inner:
                            print("Appending-----")
                            schedule_no_list_inner.append(indexed_data['SCHEDULE_NO'])
                            last_added_supply_schedule_items_obj_list.append(last_added_supply_items_schedule_obj)
                            sch_no_found_on_line_type_supply_count = sch_no_found_on_line_type_supply_count+1
                            print("RECORD ADDED COUNT:",count)
                            count=count+1
                            continue
                else:
                    count=count+1
                    # print("SUPPLY NOT FOUND count :",count)
                    continue
                # if  sch_no_found_on_line_type_supply_count==len(last_added_supply_schedule_items_obj_list):
                #     print(f"sch_no_found_on_line_type_supply_count is :{sch_no_found_on_line_type_supply_count} and last_added_supply_schedule_obj_list values is :,{last_added_supply_schedule_items_obj_list}")
                #     return True,last_added_supply_schedule_items_obj_list
                # else:
                #     return False,False
            # print("schedule_no_list_inner--",schedule_no_list_inner)
    
    print("schedule_no_list:",len(schedule_no_list))
    print("schedule_no_list_inner:",len(schedule_no_list_inner))
    if  len(schedule_no_list)==len(schedule_no_list_inner):
        return True,schedule_no_list_inner,schedule_no_list
    else:
        return False,False,False


def schedule_installation_items_api_data_insertion(request,tkcheader_data,wo,sch_installation_obj_list,schedule_no_list):
    print("in function schedule_supply_items_api_data_insertion")
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    schedule_no_list_inner=[]
    last_added_installation_schedule_items_obj_list=[]
    tkcheader_data=tkcheader_data["OutputParameters"]['P_TKC_ORDER_REC_TYPE']['P_TKC_ORDER_REC_TYPE_ITEM']
    for j in range(len(sch_installation_obj_list)):
        # print("for loop ka value chl rha h :",j)
        if j == len(sch_installation_obj_list):
            print("length of j completed")
            break
        else:
            # print("outer loop value ----",j)
            indexed_sch_obj=sch_installation_obj_list[j]
            # print("indexed_sch_obj",indexed_sch_obj)
            indexed_sch_no_obj=schedule_no_list[j]
            # print("indexed_sch_no_obj",indexed_sch_no_obj)
            count = 0
            sch_no_found_on_line_type_supply_count = 0
            for i in range(len(tkcheader_data)):
                # print("inner loop value",i,"count inner:",count)
                indexed_data=tkcheader_data[i]

                if count==len(tkcheader_data):
                    print("COUNT WITH LENGTH COMPLETED")
                    break

                if indexed_data['LINE_TYPE'] == 'Installation' and indexed_data['SCHEDULE_NO']==indexed_sch_no_obj:
                    # print("condition matched----with",indexed_sch_no_obj)
                    Supply = TKCWoInfo_Schedule_Installation_Item(
                    TKCWoInfo=wo,
                    Schedule_Installation=indexed_sch_obj,
                    Item_Description=indexed_data['ITEM_DESCRIPTION'],
                    Item_Code=indexed_data['ITEM_CODE'],
                    Unit=indexed_data['ITEM_UOM'],
                    Quantity=indexed_data['SCH_ITEM_QTY'],
                    Unit_Price_With_Tax=indexed_data['UNIT_PRICE'],                                            
                    # Created_At=datetime.datetime.now(),
                    Created_By=officer.employ_name, Status=1)
                    Supply.save()
                    last_added_installation_items_schedule_obj=TKCWoInfo_Schedule_Installation_Item.objects.filter(TKCWoInfo=wo).last()
                    # Supply.save()
                    last_added_installation_items_schedule_obj=TKCWoInfo_Schedule_Installation_Item.objects.filter(TKCWoInfo=wo).last()
                    if last_added_installation_items_schedule_obj is not None:
                        if indexed_data['SCHEDULE_NO'] not in schedule_no_list_inner:
                            print("Appending-----")
                            schedule_no_list_inner.append(indexed_data['SCHEDULE_NO'])
                            last_added_installation_schedule_items_obj_list.append(last_added_installation_items_schedule_obj)
                            sch_no_found_on_line_type_supply_count = sch_no_found_on_line_type_supply_count+1
                            print("RECORD ADDED COUNT:",count)
                            count=count+1
                            continue
                else:
                    count=count+1
                    print("SUPPLY NOT FOUND count :",count)
                    continue    
    if  len(schedule_no_list)==len(schedule_no_list_inner):
        return True,last_added_installation_schedule_items_obj_list,schedule_no_list_inner
    else:
        return False,False,False


def schedule_time_api_data_insertion(request,tkcheader_data,wo):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    stage_no_list=[]
    tkcheader_data=tkcheader_data["OutputParameters"]['P_TKC_DESCH_REC']['P_TKC_DESCH_REC_ITEM']
    last_added_installation_schedule_obj_list=[]
    count = 1
    sch_no_found_on_line_type_installation_count = 0
    for i in range(len(tkcheader_data)):
        indexed_data=tkcheader_data[i]
        # print("printing schedule list:",stage_no_list,"indexed_data===>",indexed_data)
        if  indexed_data['STAGE'] not in stage_no_list :
            stage_no_list.append(indexed_data['STAGE'])
            Advance = TKCWoInfo_Time_Schedule(TKCWoInfo=wo, Stage=indexed_data['STAGE'],
                                                Month=indexed_data['MONTH_'], Days=indexed_data['DAYS'],
                                                # Completion_date=date_format_conversion(indexed_data['COMPLETION_DATE']),
                                                Completion_date=date_format_conversion_other_method(indexed_data['COMPLETION_DATE']),
                                                Contract_Amount_Percentage=indexed_data['CONTRACT_AMOUNT_PERCENTAGE'],
                                                Stage_Amount=indexed_data['STAGE_AMOUNT'],
                                                Remarks=indexed_data['REMARK'], Created_At=date_format_conversion_other_method(indexed_data['DATE_']),
                                                Created_By=indexed_data['CREATED_BY'], Status=1)   
            Advance.save()
            last_added_installation_schedule_obj=TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo).last()
            if last_added_installation_schedule_obj is not None:
                last_added_installation_schedule_obj_list.append(last_added_installation_schedule_obj)
                sch_no_found_on_line_type_installation_count = sch_no_found_on_line_type_installation_count+1
                continue
        else:
            count=count+1
            continue
    
    return True

#Added By Aayush
def wo_view_created_by_gbpa(request, id):
    print("=====================in wo_view_created_by_gbpa=====================",id)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=id)
    print("wo:---->",wo)

    Header = TKCWoInfo_Header.objects.filter(TKCWoInfo=wo, Status=1)
    # Company = UserCompanyDataMain.objects.filter(user_id=wo.supplier.ContactNo) 
    Company = UserCompanyDataMain.objects.filter(CompanyName_E=wo.supplier) 
    # UserCompanyDataMain.objects.get(user_id_id=v_id) 
    Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
    Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
    Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1).order_by('Schedule_Supply__Schedule_No')
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    Install_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo, Status=1).order_by('Schedule_Installation__Schedule_No')
    Install = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)

    query = f'''SELECT "Item_Code", sum("Quantity") FROM public.fqp_tkcwoinfo_schedule_supply_item where "TKCWoInfo_id" = {id} and "Status" = 1 group by "Item_Code"'''
    print("query:-----",query)
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    print(row,"----------fqp_tkcwoinfo_schedule_supply_item row data----------------------")

    for i in row:        
         Supply_Item_name = TKCWoInfo_Schedule_Supply_Item.objects.filter(Item_Code =i[0])
         for j in Supply_Item_name:
                item_name = j.Item_Description
                print("id::::::==>",id)
                if tkc_wo_items_boq.objects.filter(wo =id , item_code = i[0]).exists():
                    print(j,"----------data already exist----------------------")
                    pass
                else:
                    print(j,"----------data saving----------------------")
                    boq_save = tkc_wo_items_boq(wo =wo , material_name = item_name, item_code = i[0],total_order_qty = i[1],balance_qty = i[1])
                    print("boq_save:",boq_save)
                    boq_save.save()
    return render(request, 'fqp/wo_creater/wo_gbpa_view.html',
                  {"officer": officer, 'wo': wo, 'Company': Company,'Header': Header,'Supply_Item': Supply_Item, 'Supply': Supply, 'Install_Item': Install_Item,
                   'Install': Install,'Install': Install,'Time': Time,"Advance": Advance,'Copy_To': Copy_To})


def view_workorder(request, v_id):
    print("=====================in view_workorder=====================",v_id)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=v_id)
    print("wo:---->",wo)

    Header = TKCWoInfo_Header.objects.filter(TKCWoInfo=wo, Status=1)
    Company = UserCompanyDataMain.objects.filter(CompanyName_E=wo.supplier) 
    # UserCompanyDataMain.objects.get(user_id_id=v_id) 
    Time = TKCWoInfo_Time_Schedule.objects.filter(TKCWoInfo=wo, Status=1)
    Advance = TKCWoInfo_Advance.objects.filter(TKCWoInfo=wo, Status=1)
    Supply_Item = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__TKCWoInfo=wo, Status=1).order_by('Schedule_Supply__Schedule_No')
    Supply = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo=wo, Status=1)
    Install_Item = TKCWoInfo_Schedule_Installation_Item.objects.filter(Schedule_Installation__TKCWoInfo=wo, Status=1).order_by('Schedule_Installation__Schedule_No')
    Install = TKCWoInfo_Schedule_Installation.objects.filter(TKCWoInfo=wo, Status=1)
    Copy_To = TKCWoInfo_Copy_To.objects.filter(TKCWoInfo=wo, Status=1)
    gbpa_order_status=wo.is_gbpa_order
    print("================================",gbpa_order_status)

    query = f'''SELECT "Item_Code", sum("Quantity") FROM public.fqp_tkcwoinfo_schedule_supply_item where "TKCWoInfo_id" = {v_id} and "Status" = 1 group by "Item_Code"'''
    print("query:-----",query)
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    print(row,"----------fqp_tkcwoinfo_schedule_supply_item row data----------------------")

    for i in row:        
         Supply_Item_name = TKCWoInfo_Schedule_Supply_Item.objects.filter(Item_Code =i[0])
         for j in Supply_Item_name:
                item_name = j.Item_Description
                # print("id::::::==>",v_id)
                if tkc_wo_items_boq.objects.filter(wo =v_id , item_code = i[0]).exists():
                    print(j,"----------data? already exist----------------------")
                    pass
                else:
                    # print(j,"----------data saving----------------------")
                    boq_save = tkc_wo_items_boq(wo =wo , material_name = item_name, item_code = i[0],total_order_qty = i[1],balance_qty = i[1])
                    print("boq_save:",boq_save)
                    boq_save.save()

    return render(request, 'fqp/wo_creater/wo_gbpa_view.html',
                  {"officer": officer, 'wo': wo, 'Company': Company,'Header': Header,'Supply_Item': Supply_Item, 'Supply': Supply, 'Install_Item': Install_Item,
                   'Install': Install,'Install': Install,'Time': Time,"Advance": Advance,'Copy_To': Copy_To,'gbpa_order':gbpa_order_status})

# +++++++++++++++++++++++++++++++GBPA API Integration Code end's here: Added By Aayush Joshi++++++++++ 


# Code for PS Sir dashboard

def ps_logout(request):
    try:
        del request.session['employ_login_id']
    except:
        pass
    return render(request, 'main/index.html')


def ps_base_data():
    tkcs = User_Registration.objects.filter(User_type = 'TKC').count()
    all_wo = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1).count()
    all_pdi = PDI_Inspection_Info.objects.filter(Status = 1,Material__PDI_Complete = 1).distinct('offer_no').count()
    all_di = tkc_di_master.objects.all().count()
    data = {"tkcs":tkcs,"all_wo":all_wo,"all_di":all_di,"all_pdi":all_pdi}   
    return data

def ps_dashboard(request):
    tkcs = User_Registration.objects.filter(User_type = 'TKC').count()
    all_wo = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1).count()
    all_pdi = PDI_Inspection_Info.objects.filter(Status = 1,Material__PDI_Complete = 1).count() 
    all_di = tkc_di_master.objects.all().count()
    
    works_data = works_master.objects.all()
                            
    package_work_data = {}
    value_list = []
    for work in works_data:
        value_list = [] 
        wo = TKCWoInfo.objects.filter(pakage = work,Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1).count()
        value_list.append(work.id)
        value_list.append(wo)
        package_work_data[work.package_name] = value_list
    return render(request, 'ps-dashboard/ps_dashboard.html',{"tkcs":tkcs,"all_wo":all_wo,"all_di":all_di,"all_pdi":all_pdi,"works_data":works_data,"package_work_data":package_work_data})



def all_discom_work_orders(request):
    cz_wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1, zone = 'CZ').count()
    ez_wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1, zone = 'EZ').count()
    wz_wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1, zone = 'WZ').count()
    base_data = ps_base_data()
    discom_list = ['CZ','EZ','WZ']
    
    data = {"cz_wo_data":cz_wo_data,"ez_wo_data":ez_wo_data,"wz_wo_data":wz_wo_data,"discom_list":discom_list}
    response = data|base_data
    
    return render(request,'ps-dashboard/discom_wo_data.html',response)


def wo_discom_data(request,discom):
    discom_wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1,zone = discom)
    data = {"discom_wo_data":discom_wo_data}
    base_data = ps_base_data()
    response = data|base_data
    return render(request,'ps-dashboard/discom_wise_wo_data.html',response)


def work_order_offer_data(request,wo_id):
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    wo_offer_data = offer_material_site_stores.objects.filter(wo = wo_data,Material_Offer_Submit_Approved_Status = 1).distinct('offer_no')
    data = {"wo_offer_data":wo_offer_data,"wo_data":wo_data}
    base_data = ps_base_data()
    response = data|base_data
    return render(request,'ps-dashboard/wo_offer_data.html',response)



def offer_data_details(request,offer_no,wo_id):
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    offer_materials_data = offer_material_site_stores.objects.filter(offer_no = offer_no)
    data = {"offer_materials_data":offer_materials_data,"wo_data":wo_data,"offer_no":offer_no}
    base_data = ps_base_data()
    response = data|base_data
    return render(request,'ps-dashboard/wo_offer_materials_data.html',response)

def all_discom_dispatch_instruction(request):
    cz_di_data = tkc_di_master.objects.filter(di_approved_status = 1,di_digital_upload_status = 1, zone = 'CZ').count()
    ez_di_data = tkc_di_master.objects.filter(di_approved_status = 1,di_digital_upload_status = 1, zone = 'EZ').count()
    wz_di_data = tkc_di_master.objects.filter(di_approved_status = 1,di_digital_upload_status = 1, zone = 'WZ').count()
    base_data = ps_base_data()
    discom_list = ['CZ','EZ','WZ']
    
    data = {"cz_di_data":cz_di_data,"ez_di_data":ez_di_data,"wz_di_data":wz_di_data,"discom_list":discom_list}
    response = data|base_data
    
    return render(request,'ps-dashboard/discom_di_data.html',response)

def di_discom_data(request,discom):
    discom_di_data = tkc_di_master.objects.filter(di_approved_status = 1,di_digital_upload_status = 1, zone = discom)
    data = {"discom_di_data":discom_di_data}
    base_data = ps_base_data()
    response = data|base_data
    return render(request,'ps-dashboard/discom_wise_di_data.html',response)


def all_discom_material_offer(request):
    cz_offer_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1, wo__zone = 'CZ').distinct('offer_no').count()
    ez_offer_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1, wo__zone = 'EZ').distinct('offer_no').count()
    wz_offer_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1, wo__zone = 'WZ').distinct('offer_no').count()
    base_data = ps_base_data()
    discom_list = ['CZ','EZ','WZ']
    
    data = {"cz_offer_data":cz_offer_data,"ez_offer_data":ez_offer_data,"wz_offer_data":wz_offer_data,"discom_list":discom_list}
    response = data|base_data
    
    return render(request,'ps-dashboard/discom_offer_material_data.html',response)

def material_offer_discom_data(request,discom):
    offer_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1, wo__zone = discom).distinct('offer_no')
    data = {"offer_data":offer_data}
    base_data = ps_base_data()
    response = data|base_data
    return render(request,'ps-dashboard/discom_wise_offer_data.html',response)


def package_wo_Data(request,package_id):
    discom_list = ['CZ','EZ','WZ']
    works_data = works_master.objects.get(id = package_id)
    package_name = works_data.package_name
    data_dict = {}
   
    for i in discom_list:
        discom_data = []
        wo_id_list = [] 
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1, zone = i,pakage = package_id)
        wo_count = wo_data.count()
        for j in wo_data:
            wo_id_list.append(j.id)
        
        offer_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1,wo__in = wo_id_list)
        offer_count = offer_data.count()
        pdi_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1,wo__in = wo_id_list,PDI_Complete = 1,PDI_Approved_Status = 1).distinct('offer_no')
        pdi_count = pdi_data.count()
        di_data = tkc_di_master.objects.filter(di_approved_status = 1,di_digital_upload_status = 1, wo__in = wo_id_list)
        di_count = di_data.count()
        discom_data.append(wo_count)
        discom_data.append(offer_count)   
        discom_data.append(pdi_count)
        discom_data.append(di_count)


        data_dict[i] = discom_data
        
    return render(request,'ps-dashboard/package_discom_wo_data.html',{"data_dict":data_dict,"package_id":package_id,"package_name":package_name})

    
def package_discom_wo_Data(request,package_id,discom):
    works_data = works_master.objects.get(id = package_id)
    package_name = works_data.package_name
    wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1, zone = discom,pakage = package_id)
    data_dict = {}
    
    for i in wo_data:
        discom_data = []
        offer_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1,wo = i)
        offer_count = offer_data.count()
        pdi_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1,wo = i,PDI_Complete = 1,PDI_Approved_Status = 1).distinct('offer_no')
        pdi_count = pdi_data.count()
        di_data = tkc_di_master.objects.filter(di_approved_status = 1,di_digital_upload_status = 1, wo = i)
        di_count = di_data.count()
        discom_data.append(i.supplier.CompanyName_E)   
        discom_data.append(offer_count)   
        discom_data.append(pdi_count)
        discom_data.append(di_count)
        discom_data.append(i.Wo_Digital)
        discom_data.append(i.id)
        
        data_dict[i.Contract_Number] = discom_data
        
        
    return render(request,'ps-dashboard/package_discom_all_wo_dataa.html',{"data_dict":data_dict,"package_id":package_id,"package_name":package_name})
    
    

def work_order_offer_details(request,wo_no,package_id):
    works_data = works_master.objects.get(id = package_id)
    package_name = works_data.package_name
    wo_obj = TKCWoInfo.objects.get(id = wo_no)
    offer_material_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1,wo = wo_obj).distinct('offer_no')
    return render(request,'ps-dashboard/package_wo_offer_material_data.html',{"offer_material_data":offer_material_data,"package_id":package_id,"package_name":package_name})



def work_order_pdi_details(request,wo_no,package_id):
    works_data = works_master.objects.get(id = package_id)
    package_name = works_data.package_name
    wo_obj = TKCWoInfo.objects.get(id = wo_no)
    pdi_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status = 1,wo = wo_obj,PDI_Assign = 1,PDI_Complete=1).distinct('offer_no')
    return render(request,'ps-dashboard/package_wo_pdi_data.html',{"pdi_data":pdi_data,"package_id":package_id,"package_name":package_name})
    
    
    
def work_order_offer_material_details(request,offer_no,package_id):
    works_data = works_master.objects.get(id = package_id)
    package_name = works_data.package_name
    offer_data = offer_material_site_stores.objects.filter(offer_no = offer_no)
    return render(request,'ps-dashboard/offer_material_wise_data.html',{"offer_data":offer_data,"package_id":package_id,"package_name":package_name})
    

def work_order_dispatch_instruction(request,offer_no,package_id):
    works_data = works_master.objects.get(id = package_id)
    package_name = works_data.package_name
    di_data = tkc_di_master.objects.filter(offer_no = offer_no,di_approved_status =1,di_digital_upload_status = 1)
    return render(request,'ps-dashboard/offer_material_di_data.html',{"di_data":di_data,"package_id":package_id,"package_name":package_name})
    

def created_di_list(request,wo_id):
    wo_obj = TKCWoInfo.objects.get(id = wo_id)
    wo_di_objects  = tkc_di_master.objects.filter(wo = wo_obj).order_by('-id')
    return render(request, 'fqp/wo_creater/created_wo_di.html',
                  {"wo_di_objects": wo_di_objects,"wo_obj":wo_obj})
    
    
def upload_di_copy(request,offer_no,erp_di_no,wo_id):
    print("herer")
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    di_pdf =  request.FILES['di_doc']
    di_object  = tkc_di_master.objects.get(offer_no = offer_no,erp_di_number = erp_di_no)
    di_object.created_di_doc = di_pdf
    di_object.di_send_to_approval_status = 1
    di_object.di_send_by_approval_by =officer.employ_name
    di_object.save()
    wo_obj = TKCWoInfo.objects.get(id = wo_id)
    wo_di_objects  = tkc_di_master.objects.filter(wo = wo_obj).order_by('-id')
    return render(request, 'fqp/wo_creater/created_wo_di.html',
                  {"wo_di_objects": wo_di_objects,"wo_obj":wo_obj})
    
# code for bypass PDI detail    
# def bypass_pdi_offer(request):
#     offer=offer_material_site_stores.objects.filter(is_pdi_required=False,Material_Offer_Submit_Approved_Status=1,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1).distinct('offer_no')
    
#     return render(request,'fqp/wo_creater/bypass_pdi_offer.html',{'list':offer})
        
# def view_offer_wo(request,offer_no):
#     offer=offer_material_site_stores.objects.filter(offer_no=offer_no,Material_Offer_Submit_Approved_Status=1,is_pdi_required=False,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1)
    
#     qun_list = []
#     total_qun = []
#     item_code_list  = []

#     for j in offer:
#         item_code_list.append(j.wo_material.item_code)

#     if(len(set(item_code_list))!=len(item_code_list)):
#         new_obj = offer.distinct('wo_material__item_code')
#         for i in new_obj:
#             offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code =i.wo_material.item_code,Material_Offer_Submit_Approved_Status=1,is_pdi_required=False)
#             for k in offer_material:
#                 qun_list.append(k.quantity)
#             qty_sum = sum(qun_list)
#             total_qun.append(qty_sum)
#             qun_list.clear()

#     else:
#         new_obj = offer
#         for i in offer:
#             total_qun.append(i.quantity)

#     final_data = zip(new_obj,total_qun)
#     return render(request,'fqp/wo_creater/view_offer.html',{"offer":final_data})
    

#Added By Aayush
def di_api_call(request,gbpa_no):
    URL="http://epic.mpezerp.com:80/webservices/rest/qc_portal_tkc_di/get_di/"
    data={
    "get_di": {
    "@xmlns": "http://xmlns.oracle.com/apps/po/rest/qc_portal_tkc_di/get_di",

    "RESTHeader": {

    "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",

    "Responsibility": "JAI_PURCHASING",

    "RespApplication": "JA",

    "SecurityGroup": "STANDARD",

    "NLSLanguage": "AMERICAN",

    "Org_Id": "83"
    },
    "InputParameters": {

    "P_CONTRACT_NO": gbpa_no
    }
    }
    }
    json_data = json.dumps(data)
    auth_values = HTTPBasicAuth(const.Username, const.Password)
    # try:
        # print('in try:::::')
        #calling API here with all the payload and endpoint details.
    res = req.post(url=URL, auth=auth_values, headers=const.headers, data=json_data) 
    print("res",res)
    if res.status_code == 200:
        print("code matched")
        return True,res.json()
################################################################################################################

#Added By Aayush
def inspection_api_call(request,gbpa_no):
    URL="http://epic.mpezerp.com:80/webservices/rest/qc_portal_tkc_insp/get_insp/"
    data={
        "get_insp": {
        "@xmlns": "http://xmlns.oracle.com/apps/po/rest/qc_portal_tkc_insp/get_insp/",
        "RESTHeader": {
        "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
        "Responsibility": "JAI_PURCHASING",
        "RespApplication": "JA",
        "SecurityGroup": "STANDARD",
        "NLSLanguage": "AMERICAN",
        "Org_Id": "83"
        },
        "InputParameters": {
        "P_CONTRACT_NO": gbpa_no}}}

    json_data = json.dumps(data)
    auth_values = HTTPBasicAuth(const.Username, const.Password)
    # try:
        # print('in try:::::')
        #calling API here with all the payload and endpoint details.
    res = req.post(url=URL, auth=auth_values, headers=const.headers, data=json_data) 
    print("RESPONSE",res)
    
    print("res code==========>",res.status_code,type(res.status_code))
    if res.status_code == 200:
        # print("code matched")
        inspection_data = res.json()
        if inspection_data['OutputParameters']['P_PO_INSP']is None:
            return False,False
        elif inspection_data['OutputParameters']['P_ERRORS']is not None:
            return res.status_code,inspection_data['OutputParameters']['P_PO_INSP']['P_ERRORS']['P_ERRORS_ITEM']['ERROR_MESSAGE']
        elif inspection_data['OutputParameters']['P_PO_INSP']['P_PO_INSP_ITEM'] is not None:
            return res.status_code,inspection_data        
    else:
        return res.status_code,False


#Added By Aayush
def verify_and_create_di(request,wo_id,offer_no):

    # print("wo_id",wo_id,"offer_no",offer_no)
    distinct_offer_list=[]
    distinct_offer_list_with_material_status={}
    materials_list_for_each_offer_dict={}
    offer_avaialibility_in_api_dict={}
    inspection_ref_no_list=[]
    inspection_item_code_list=[]
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    # offer_details = offer_material_site_stores.objects.filter(wo = wo,DI_Created_Status=0).distinct('offer_no')
    offer_details = offer_material_site_stores.objects.filter(wo = wo).distinct('offer_no')


    for obj in offer_details:
        # print(obj.wo_material.id)
        material_offer_no=obj.offer_no
        
        #fetching details of material for each offered materials 
        # offer_details_for_specific_offer_no = offer_material_site_stores.objects.filter(wo = wo, offer_no = material_offer_no,PDI_Complete=1,PDI_Approved_Status=1,DI_Created_Status=0)
        offer_details_for_specific_offer_no = offer_material_site_stores.objects.filter(wo = wo, offer_no = material_offer_no,PDI_Complete=1,PDI_Approved_Status=1)

        #checking presence of materials in each offer, and assigning "status" to True for material presence else false.
        if offer_details_for_specific_offer_no.exists():
            
            #As materials are presents in offer no ,giving material present status to True. 
            distinct_offer_list_with_material_status[obj.offer_no]=True
        
            for j in offer_details_for_specific_offer_no:
                if j.offer_no in materials_list_for_each_offer_dict:
                    materials_list_for_each_offer_dict[f'{j.offer_no}'].append(j.wo_material.item_code)
                else:    
                    materials_list_for_each_offer_dict[j.offer_no]=[j.wo_material.item_code]
        
        else:
            #As materials are not presents in offer no ,giving materials present status to False.
            distinct_offer_list_with_material_status[obj.offer_no]=False

    inspection_api_status,inspection_api_res_data=inspection_api_call(request,gbpa_no=wo.Contract_Number)
    # inspection_api_status,inspection_api_res_data=inspection_api_call(request,gbpa_no=1285)
    # print("inspection_api_status,inspection_api_res_data",inspection_api_status,inspection_api_res_data)
    
    if inspection_api_status != 200 and inspection_api_res_data == False:
        return HttpResponse("THERE IS SOME PROBLEM WITH API ,UNABLE TO GET DATA FROM API")

    #calling inspection API and fetching data for each offer no for Passes Contract Number.
    if inspection_api_status == 200 and inspection_api_res_data ['OutputParameters']['P_PO_INSP']['P_PO_INSP_ITEM'] is not None:
        inspection_api_data=inspection_api_res_data ['OutputParameters']['P_PO_INSP']['P_PO_INSP_ITEM']
        total_inspection_list_length=len(inspection_api_data)
        print('total_inspection_list_length',total_inspection_list_length)

        '''fetching each offer no and verifying each proposed "offer" in API data and creating
        new dictionary called offer_avaialibility_in_api_dict, i.e checking "offer no" availability in API responsed DATA''' 
        for offered_materials_offer_no , material_code in materials_list_for_each_offer_dict.items():
            for inspection_item in range(0,len(inspection_api_data)):
                # print("inspection_api_data[inspection_item]['INSP_DET_REMARKS']::::",inspection_api_data[inspection_item]['INSP_DET_REMARKS'])
                if inspection_api_data[inspection_item].get('INSP_DET_REMARKS') is not None and offered_materials_offer_no in inspection_api_data[inspection_item].get('INSP_DET_REMARKS') :
                    print("here on:",inspection_item,"INSP_DET_REMARKS is :",inspection_api_data[inspection_item]['INSP_DET_REMARKS'])
                    
                    if offered_materials_offer_no in offer_avaialibility_in_api_dict and 'inspection_no' in offer_avaialibility_in_api_dict[offered_materials_offer_no]:
                        
                        inspection_ref_no_list.append(inspection_api_data[inspection_item]['INSPECTION_REF'])
                        inspection_item_code_list.append(inspection_api_data[inspection_item]['ITEM_CODE'])    
                        
                        offer_avaialibility_in_api_dict[offered_materials_offer_no]={
                        "inspection_no": inspection_ref_no_list,
                        "Verified_Item_Code": inspection_item_code_list
                        }

                    else:    
                        inspection_ref_no_list.append(inspection_api_data[inspection_item]['INSPECTION_REF'])
                        inspection_item_code_list.append(inspection_api_data[inspection_item]['ITEM_CODE'])   
                        # offer_avaialibility_in_api_dict[offered_materials_offer_no]=[inspection_api_data[inspection_item]["ITEM_CODE"]]
                        
                        offer_avaialibility_in_api_dict[offered_materials_offer_no]={
                        "inspection_no": inspection_ref_no_list,
                        "Verified_Item_Code": inspection_item_code_list
                        }
                        # print("created new dictionary for once:",offer_avaialibility_in_api_dict,"for offer no:",offered_materials_offer_no)
                        # offer_avaialibility_in_api_dict[offered_materials_offer_no]['inspection_no']=[inspection_api_data[inspection_item]["INSPECTION_REF"]]
            
                else:
                    # print("in else")
                    pass
            
            #Emptying item code list and reference no list again for other offer numbers.
            inspection_item_code_list=[]
            inspection_ref_no_list=[]
    else:
        print("Unable to get the data from inspection API  ")
    
    #calling METHOD: offered_materials_checking_in_api
    all_verified_materials_with_ref_no_dictionary=offered_materials_checking_in_api(request,materials_list_for_each_offer_dict,offer_avaialibility_in_api_dict,offer_no)
    #calling METHOD: di_creation_for_offered_materials
    pending_di_dictionary_with_approved_materials=di_creation_for_offered_materials(request,all_verified_materials_with_ref_no_dictionary,offer_no,wo_id,gbpa_no=wo.Contract_Number)    
    return pending_di_dictionary_with_approved_materials

#Added By Aayush Joshi
def offered_materials_checking_in_api(request,offered_material_after_pdi,all_inspected_materials_in_insp_api,offer_no):
    
    #here in this function we are checking if the Offered Matrials are presents in inspection API , so that we can proceed further for DI creation.
    # print("offered_material_after_pdi::",offered_material_after_pdi,offer_no)
    
    #declaring dict and list 
    di_approval_dict={}
    all_verified_materials_with_ref_no_dictionary={}
    inspected_materials_with_inspection_ref_no={}
    offer_no_list=[]
    inspection_ref_no_list=[]
    inspection_item_code_list=[]

    
    #removing duplicates appended inspection no.
    for key, value in all_inspected_materials_in_insp_api.items():
        # Remove duplicates from the 'Verified_Item_Code' list using set()
        updated_list_item_code = list(set(value['Verified_Item_Code']))
        # Remove duplicates from the 'inspection_no' list using set()
        updated_list_inspection_no=list(set(value['inspection_no']))
        # Update the dictionary with the new list of values
        inspected_materials_with_inspection_ref_no[key] = {'inspection_no':updated_list_inspection_no, 'Verified_Item_Code': updated_list_item_code}
    
    # print("inspected_materials_with_inspection_ref_no--->",inspected_materials_with_inspection_ref_no)
    
    for offer_no, values in offered_material_after_pdi.items():
        for value in values:
            if offer_no in inspected_materials_with_inspection_ref_no:
                if value in inspected_materials_with_inspection_ref_no[offer_no]['Verified_Item_Code']:
                    # print(f"{value} exists in {offer_no} in inspected_materials_with_inspection_ref_no")
                    if offer_no in all_verified_materials_with_ref_no_dictionary and 'inspection_no' in all_verified_materials_with_ref_no_dictionary[offer_no]:
                        # print("in already created dict")
                        offer_no_list.append(offer_no)
                    
                        inspection_ref_no_list=list(set(inspection_ref_no_list))
                        
                        if inspected_materials_with_inspection_ref_no[offer_no]['inspection_no'] not in inspection_ref_no_list:
                            inspection_ref_no_list.extend(inspected_materials_with_inspection_ref_no[offer_no]['inspection_no'])
                            
                            # print(inspection_ref_no_list)
                            inspection_ref_no_list=list(set(inspection_ref_no_list))
                            # print(inspection_ref_no_list)
                        
                        if value not in inspection_item_code_list:
                            inspection_item_code_list.append(value)
                        
                        #updating already created di dict
                        all_verified_materials_with_ref_no_dictionary[offer_no]={
                        "inspection_no": inspection_ref_no_list,
                        "Verified_Item_Code": inspection_item_code_list
                        }
                    else:
                        # print("i am in else and working on creating dictionary eligible_to_create_di_dictionary")
                        offer_no_list.append(offer_no)
                        if inspected_materials_with_inspection_ref_no[offer_no]['inspection_no'] not in inspection_ref_no_list:
                            inspection_ref_no_list.extend(inspected_materials_with_inspection_ref_no[offer_no]['inspection_no'])
                            inspection_ref_no_list=list(set(inspection_ref_no_list))
                        if value not in inspection_item_code_list:
                            inspection_item_code_list.append(value)
                                            
                        all_verified_materials_with_ref_no_dictionary[offer_no]={
                        "inspection_no": inspection_ref_no_list,
                        "Verified_Item_Code": inspection_item_code_list
                        }
                        # print('all_verified_materials_with_ref_no_dictionary--->',all_verified_materials_with_ref_no_dictionary)
                else:
                    # print(f"{value} does not exist in {offer_no} in inspection")
                    continue
            else:
                # print("offer_no not presents in inspected data")
                pass
        #emptying list again to re-use    
        inspection_ref_no_list=[]
        inspection_item_code_list=[]        
    

    #returning all verified/inspected items with inspection_no/ref_no for each offer-no. 
    print("returning all_verified_materials_with_ref_no_dictionary")
    return all_verified_materials_with_ref_no_dictionary


#Added By Aayush Joshi
def di_creation_for_offered_materials(request,all_verified_materials_with_ref_no_dictionary,offer_no,wo_id,gbpa_no):

    di_api_status,di_api_res_data=di_api_call(request,gbpa_no)
    count=1
    pending_di_dictionary_with_approved_materials={}
    
    #calling DI API and fetching data for each offer no for Passes Contract Number.
    # if di_api_status and di_api_res_data['OutputParameters']['P_PO_DI']['P_PO_DI_ITEM'] is not None:
    if di_api_status and di_api_res_data is not None:
        di_api_data=di_api_res_data['OutputParameters']['P_PO_DI']['P_PO_DI_ITEM']
        total_di_api_data_length=len(di_api_data)
        
        for key,value in all_verified_materials_with_ref_no_dictionary.items():
            print("OUTER COUNT------------->",count)
            inspection_key_to_check_list=all_verified_materials_with_ref_no_dictionary[key]['inspection_no']

            verified_item_to_check=all_verified_materials_with_ref_no_dictionary[key]['Verified_Item_Code']

            if key == offer_no:
                print("key matched now creating dictionary for this offer no by matching inspection no")
                for inspection_key in inspection_key_to_check_list:
                    for index in range(total_di_api_data_length):   
                        if inspection_key in di_api_data[index]['INSPECTION_REF2']:
                            print("matched inspection_key--->",inspection_key)
                            print("verified_item_to_check--->",verified_item_to_check)
                            for item_code in verified_item_to_check:
                                if item_code in di_api_data[index]['DI_DET_ITEM_CODE'] and inspection_key in di_api_data[index]['INSPECTION_REF2']:
                                    print("item_code",item_code,di_api_data[index]['DI_DET_ITEM_CODE'])
                                    print("item_code",inspection_key,di_api_data[index]['INSPECTION_REF2'])
                                    print("-------------both matched---------------")
                                    
                                    print("beofre count increase",count)
                                    if di_api_data[index]['DI_REF'] in pending_di_dictionary_with_approved_materials:
                                        print("di_api_data[index]['DI_REF']",di_api_data[index]['DI_REF'],'already in' ,pending_di_dictionary_with_approved_materials)
                                        
                                        count=count+1
                                        print("in already created dict")
                                        print("count-------->",count)
                                        
                                        pending_di_dictionary_with_approved_materials[di_api_data[index]['DI_REF']][f"di_data{count}"] = di_api_data[index]
                                        pending_di_dictionary_with_approved_materials[di_api_data[index]['DI_REF']][f"di_data{count}"]["offer_no"] = f"{offer_no}"                                    
                                        print("---------222222222222-OFFER-NO-ADDED---pending_di_dictionary_with_approved_materials----------",pending_di_dictionary_with_approved_materials)
                                        print("-------continue------")
                                        continue
                                        print("--------after continue---------")
                                    
                                    else:
                                        print("creating dict",count)
                                        count=1
                                        pending_di_dictionary_with_approved_materials[di_api_data[index]['DI_REF']] = {
                                            f"di_data{count}": di_api_data[index]}
                                        pending_di_dictionary_with_approved_materials[di_api_data[index]['DI_REF']][f"di_data{count}"]["offer_no"] = f"{offer_no}"
                                        print("pending_di_dictionary_with_approved_materials----------->",pending_di_dictionary_with_approved_materials)
                                        continue
                                else:
                                    print("------------------------------------in else-----------------------------------------")
                                    print("item_code",item_code,di_api_data[index]['DI_DET_ITEM_CODE'])
                                    print("item_code",inspection_key,di_api_data[index]['INSPECTION_REF2'])
                                    print("***********************************************************************************")
                                    # count=1
                                    print(count)
                                    continue
                        else:
                            continue    
            else:
                # print('offer_no is different')
                pass
    else:
        print("di api is not responding")
    
    # print('pending_di_dictionary_with_approved_materials---->',pending_di_dictionary_with_approved_materials)
    return pending_di_dictionary_with_approved_materials

#Added By Aayush Joshi
def view_and_create_multiple_DI(request,wo_id,offer_no,creating_di=None,item_code=None,di_created_status=None,message=None):
    print("in view_and_create_multiple_DI",request,wo_id,offer_no,creating_di,item_code,di_created_status)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    my_dict={}
    wo = TKCWoInfo.objects.get(id=wo_id)
    print('wo',wo)
    material = offer_material_site_stores.objects.filter(TKCVendor__TKCWoInfo = wo)
    # print('material',material)
    #viewing Multiple-Di list data here.

    tkc_di_data=tkc_di_master.objects.filter(wo=wo,offer_no = offer_no,zone = wo.zone)
    print("tkc_di_data$$$$$$$$$$$$$$$$$$",tkc_di_data)

    #calling function to create DI through ERP Data.
    erp_di_data_to_view_and_create=verify_and_create_di(request,wo_id,offer_no)
    # print("exiting from if",erp_di_data_to_view_and_create)
    if not erp_di_data_to_view_and_create :
        offer_details = offer_material_site_stores.objects.filter(wo = wo).distinct('offer_no')
        print("in this condition i am ")
        message = messages.error(request, f"Unable to view or create any DI as No ERP-DI data found for this offer no:{offer_no}")
        return render (request,'fqp/wo_creater/pending_di_list.html',{"officer": officer,'offer_material_data':offer_details,"wo":wo})
    erp_di_data_to_view_and_create=checking_if_di_already_created(tkc_di_data,erp_di_data_to_view_and_create)
    # print('erp_di_data_to_view_and_create',erp_di_data_to_view_and_create)
    return render (request,'fqp/wo_creater/create_erp_di_list_page.html',{"officer": officer,"erp_di_data_to_view_and_create":erp_di_data_to_view_and_create,'offer_material_data':material,"wo":wo,"offer_no":offer_no,"wo_id":wo_id,"item_code":item_code})
    
    
#Added By Aayush Joshi
def create_erp_di_entry(request,wo_id,di_no,offer_no):
    print("Creating erp_di_entry")
    erp_di_no1=di_no
    # print('erp_di_no1--->',erp_di_no1)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    material = offer_material_site_stores.objects.filter(TKCVendor__TKCWoInfo = wo)
    erp_di_data_to_view_and_create=verify_and_create_di(request,wo_id,offer_no)
    print('erp_di_data_to_view_and_create------>',erp_di_data_to_view_and_create)
    wo_zone = wo.zone
    if wo_zone == 'EZ':
        
        '''checking eligibility of DI , by checking total quanity of each "offered item" .
        -e.g. if itemcode 'I1001' total quantity for offer no '3996' is 200,
        DI CREATION ELIGIBILITY:
        -DI CREATION POSSIBLE if :-creating DI for this item code 'I1001' for 50qty which is coming in API,and available total qty for item-code is 200.   
        -DI CREATION Not POSSIBLE if: :-creating DI for this item code 'I1001' for 500qty which is coming in API,and available total qty for item-code is 200.
        '''
        material=offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1).distinct('wo_material')
        print('erp_di_data_to_view_and_create',erp_di_data_to_view_and_create)
        offered_item_codes_remaining_quantity_data=calculate_total_offered_items_quantity_check(wo,wo_id,offer_no,erp_di_data_to_view_and_create)
        # print('offered_item_codes_remaining_quantity_data',offered_item_codes_remaining_quantity_data)
        if offered_item_codes_remaining_quantity_data:
            di_no=str('D/'+di_no)
            if di_no in erp_di_data_to_view_and_create:
                print("yes di-no already present in erp_di_data_to_view_and_create")
                selected_di_data=erp_di_data_to_view_and_create[di_no]
                di_creation_status,msg,quantity_to_substract=assigning_items_to_di(offered_item_codes_remaining_quantity_data,di_no,selected_di_data)
                print("di_creation_status,msg,quantity_to_substract",di_creation_status,msg,quantity_to_substract)
                if  di_creation_status :   
                    print("di_creation_status ",di_creation_status)         
                    for di_key,di_values in erp_di_data_to_view_and_create.items():
                        print('erp_di_data_to_view_and_create::::',erp_di_data_to_view_and_create)
                        if di_no in di_key:
                            erp_di_no=erp_di_data_to_view_and_create[di_key]['di_data1']['DI_REF']
                            di_det_remarks=erp_di_data_to_view_and_create[di_key]['di_data1']['DI_DET_REMARKS']
                            di_uom=erp_di_data_to_view_and_create[di_key]['di_data1']['UOM']
                            di_receiver_name=erp_di_data_to_view_and_create[di_key]['di_data1']['RECEIVER_NAME']
                            di_site_store_name=erp_di_data_to_view_and_create[di_key]['di_data1']['DI_REMARKS']
                            if request.method=="POST":
                                subject = di_det_remarks
                                erp_di_no = di_key
                                di_prefix = di_key
                                print(wo, offer_no,wo.zone, erp_di_no)
                                if tkc_di_master.objects.filter(wo=wo,offer_no = offer_no,zone = wo.zone,erp_di_number = erp_di_no).exists():
                                    di_creation_status=False
                                    message = messages.success(request, f"DI already created with this DI No:{erp_di_no}")
                                    return view_and_create_multiple_DI(request,wo_id,offer_no,creating_di=None,item_code=None,di_created_status=di_creation_status,message=message)
                                else:
                                    print("in else:====>>",di_site_store_name)
                                    data = tkc_di_master(wo=wo,offer_no = offer_no,zone = wo.zone,wo_no = wo.wo_no,
                                    di_subject = subject,erp_di_number = erp_di_no,prefix = di_prefix,di_site_store_location=di_site_store_name)
                                    data.save()
                                
                                    for outer_key,inner_dict in quantity_to_substract.items():
                                        print('--------------QQQQQQQQQQQQQQQQQQQQ-----------',quantity_to_substract)
                                        print(outer_key,"outer_key")
                                        count=0
                                        for inner_key,value in inner_dict.items():
                                            count=count+1
                                            item = Offered_Item_Remaining_Quantity.objects.get(item_code=value[0],offer_no=outer_key)
                                            print("subtract from remaining :",float(item.remaining_quantity)-float(value[1]))
                                            item.remaining_quantity=float(item.remaining_quantity) - float(value[1])
                                            
                                            print("Adding in already Created DI :",float(item.remaining_quantity)-float(value[1]))
                                            item.already_di_issued_quantity=float(item.already_di_issued_quantity) + float(value[1])
                                            print("item.remaining_quantity---->",item.remaining_quantity)
                                            item.save()

                                            for mt in material:
                                                if mt.wo_material.item_code == value[0]:
                                                    print("OBJECT NAME:",mt,wo,type(erp_di_no),erp_di_no)

                                                #inserting data into mapping table here also.
                                                    di_mapping_data=di_mapping(wo=wo,offer_obj = mt,
                                                    erp_di_number = erp_di_no,di_quantity=value[1],di_obj=data,uom=di_uom,di_receiver_name=di_receiver_name)
                                                    di_mapping_data.save()
                                                    continue
                                    create_Di_id=data.id
                                    return redirect(f"/fqp/erp-tkc-Di-Terms/{wo_id}/{create_Di_id}/{offer_no}/{di_no}")
                            else:
                                # print("in else direct",erp_di_no)
                                return render (request,'fqp/wo_creater/wo_create_di_step1.html',{"officer": officer,'offer_material_data':material,"wo":wo,"offer_no":offer_no,"di_subject":di_det_remarks,"di_no":erp_di_no,"erp_di_no":erp_di_no1,"zone":wo_zone})
                        continue
                else:
                    print("==============aaaaaaaaaa")
                    message = messages.error(request, msg)
                    return view_and_create_multiple_DI(request,wo_id,offer_no,creating_di=None,item_code=None,di_created_status=di_creation_status,message=message)

#Added By Aayush Joshi
def erp_di_offers_list(request,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo).distinct('offer_no')
    return render (request,'fqp/wo_creater/pending_di_list.html',{"officer": officer,'offer_material_data':offer_details,"wo":wo})

#Added By Aayush Joshi
# def view_erp_offered_approved_material(request,wo_id,offer_no):
    # officer = Officer.objects.get(employ_id=request.session['employ_id'])
    # wo = TKCWoInfo.objects.get(id=wo_id)
    # offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1,DI_Created_Status=0)
    # return render (request,'fqp/wo_creater/wo_di_offers_material_list.html',{"officer": officer,'offer_material_data':offer_details,"wo":wo,"offer_no":offer_no})

#Added By Aayush Joshi
def calculate_total_offered_items_quantity_check(wo,wo_id,offer_no,erp_di_data_to_view_and_create):

    item_code_id_list=[]
    balanced_item_qty_dict={}
    nested_item_code_and_qty_dict={}
    quantity=None
    # offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1,DI_Created_Status=0)
    offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1)
    
    for index,obj in enumerate(offer_details):
        # print("index no :",index,'\n',"obj:-",obj.wo_material.id,"obj:-",obj.wo_material.item_code)
        
        print("offer_details[0].is_pdi_required--->",offer_details[0].is_pdi_required)
        if offer_details[0].is_pdi_required == True:
            if obj.wo_material.id in item_code_id_list:
                # quantity=int(obj.passed_quantity) + int(quantity)
                print("offer_details.pdi_required == True")
                print("here in obj.passed_quantity",obj.passed_quantity)
                quantity=int(obj.passed_quantity)
            
            else:
                item_code_id_list.append(obj.wo_material.id)
                print("here in obj.passed_quantity",obj.passed_quantity)
                quantity=int(obj.passed_quantity)
        else:
            print("offer_details.pdi_required == False")
            if obj.wo_material.id in item_code_id_list:
                # quantity=int(obj.passed_quantity) + int(quantity) 
                print("here in only quantity",obj.quantity)
                quantity=int(obj.quantity)
            
            else:
                item_code_id_list.append(obj.wo_material.id)
                quantity=int(obj.quantity)
        
        if f"{offer_no}" in nested_item_code_and_qty_dict:
            nested_item_code_and_qty_dict[f"{offer_no}"][obj.wo_material.item_code] = {"quantity": int(quantity)}
        else:
            nested_item_code_and_qty_dict[f"{offer_no}"] = {obj.wo_material.item_code: {"quantity": int(quantity)}}
    
    print("********************************************************")
    print('nested_item_code_and_qty_dict',nested_item_code_and_qty_dict)
    print("********************************************************")
    #storing total quantity of Items in a Table .
    for offer_no , item_data in nested_item_code_and_qty_dict.items():
        for items in item_data:
            try:
                # Try to get an existing entry with the given item_code IF Available.
                item = Offered_Item_Remaining_Quantity.objects.get(item_code=items,offer_no=offer_no)
            except Offered_Item_Remaining_Quantity.DoesNotExist:
                item = Offered_Item_Remaining_Quantity.objects.create(offer_no=offer_no, item_code=items, remaining_quantity=nested_item_code_and_qty_dict[offer_no][items]["quantity"],total_quantity=nested_item_code_and_qty_dict[offer_no][items]["quantity"])
    return Offered_Item_Remaining_Quantity.objects.all()

#Added By Aayush Joshi
# def assigning_items_to_di(offered_item_codes_remaining_quantity_data,di_no,selected_di_data): 
#     selected_di_item_codes_list=[]
#     verified_materials_quantity_material_list=[]
#     exceeded_di_quantity_then_offered_quantity_item_code_list=[]
#     msg='di_quantity_exceeded_then_offered_quantity'
#     quantity_to_substract={}
#     count=1
#     print("offered_item_codes_remaining_quantity_data:::=====>",offered_item_codes_remaining_quantity_data)
#     for item_code in offered_item_codes_remaining_quantity_data:
#         offer_offer_no=item_code.offer_no
#         offer_item_code=item_code.item_code
#         offer_item_remaining_quantity=item_code.remaining_quantity
#         offer_item_total_quantity=item_code.total_quantity
#         print('selected_di_data::---',selected_di_data,len(selected_di_data))
#         for selected_di_item_code in selected_di_data:
#             print('selected_di_dataselected_di_dataselected_di_dataselected_di_data',selected_di_data)
#             print("selected_di_item_codeselected_di_item_codeselected_di_item_code",selected_di_item_code)
#             if offer_item_code in selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'] and offer_offer_no in selected_di_data[selected_di_item_code]['offer_no'] :
#                 selected_di_item_codes_list.append(selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'])
#                 if int(float(selected_di_data[selected_di_item_code]['DI_DET_QTY'])) <= int(float(offer_item_remaining_quantity)):
#                     verified_materials_quantity_material_list.append(selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'])
#                     di_created_msg="DI created"
#                     if selected_di_data[selected_di_item_code]['offer_no'] in quantity_to_substract:
#                         quantity_to_substract[selected_di_data[selected_di_item_code]['offer_no']].update({f"itemcode{count}":[selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'],selected_di_data[selected_di_item_code]['DI_DET_QTY']]})
#                         count=count+1
#                     else:
#                         quantity_to_substract[selected_di_data[selected_di_item_code]['offer_no']] = {f"itemcode{count}":[selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'],selected_di_data[selected_di_item_code]['DI_DET_QTY']]}
#                         count=count+1
#                 else:
#                     exceed_msg =f"Unable to create DI. The requested quantity:{selected_di_data[selected_di_item_code]['DI_DET_QTY']} exceeds the total offered-accepted quantity {offer_item_remaining_quantity}."
#                     exceeded_di_quantity_then_offered_quantity_item_code_list.append(int(selected_di_data[selected_di_item_code]['DI_DET_QTY']))
#             else:
#                 print("Selected Item Code is Not present in Remaining Quantity Table")
#                 pass

#     '''Below, we are performing verification to ensure that the quantity of the selected item codes in the dictionary is less than or equal to the total offered quantity for each item code. 
#     Additionally, we are validating the length of both the list to ensure that the quantity of material of the selected DI has been verified and is less than the offered material.'''    


#     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&from assigning_items_to_di",quantity_to_substract)
#     if quantity_to_substract:
#         pass
#     else:
#         exceed_msg= 'Items Not Available to Create DI'
#         return False,exceed_msg,quantity_to_substract

#     print("****************************************************************",quantity_to_substract)
    
#     if len(selected_di_item_codes_list) == len(verified_materials_quantity_material_list):
#         print("length matched")
#         #we are able to create DI as both of the materials in DI are less than quantity of total offered_material. 
#         print(True,di_created_msg,quantity_to_substract)
#         return True,di_created_msg,quantity_to_substract
#     else:
#         print(False,exceed_msg,quantity_to_substract)
#         print("HEEEEEERRRRRRRRREEEEEEEEEE")
#         return False,exceed_msg,quantity_to_substract

#Added By Aayush
def create_erp_di_step2(request,wo_id,create_Di_id,offer_no,di_no):
    # print("------in create_erp_di_step2-------",create_Di_id,di_no)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    form = TKCCopyWorkFormData()
    wo = TKCWoInfo.objects.get(id=wo_id)
    address = UserCompanyDataMain.objects.get(user_id_id=wo.supplier)
    wo_di_object  = tkc_di_master.objects.get(id = create_Di_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1).distinct('wo_material')
    print("offer_details--->",offer_details)
    for i in offer_details:
        offer_vendor = i.TKCVendor
    vendor_address = UserCompanyDataMain.objects.get(user_id_id=offer_vendor.Vendor)
    if request.method=="POST":
        form = TKCCopyWorkFormData(request.POST,instance=wo_di_object)
        if form.is_valid():
            wo_di_object.copy_to = form.cleaned_data['copy_to']
            wo_di_object.save()
            
            #going to for rendering data.
            f_di_no=str(di_no)
            f_di_no='D/'+f_di_no
            di_mapping_data = di_mapping.objects.filter(wo = wo,erp_di_number=f_di_no,di_obj_id=wo_di_object)
            offer_details_list,boq_obj_list_data=filtered_data_to_view_DI(request,wo,f_di_no,offer_no,wo_di_object,create_Di_id,di_mapping_data)
                        
            zipped_data = zip(offer_details_list, di_mapping_data, boq_obj_list_data)

            # return render (request,'fqp/wo_creater/wo_di_view.html',{'wo':wo, "wo_di":wo_di_object,"address":address,"offer_no":offer_no,"offer_details":offer_details,"vendor_address":vendor_address})
            return render (request,'fqp/wo_creater/wo_erp_di_view.html',{'wo':wo, "wo_di":wo_di_object,"address":address,"offer_no":offer_no,"offer_details":offer_details,"vendor_address":vendor_address,'zipped_data': zipped_data})
    print('++++++++out++++++++',di_no)
    return render (request,'fqp/wo_creater/wo_create_di_step3.html',{'wo':wo,"form":form,"wo_di":wo_di_object,"address":address,"offer_no":offer_no,"di_no":di_no})

#Added By Aayush
def erp_tkc_DiTerms(request,wo_id,create_Di_id,offer_no,erp_di_no):
    print(wo_id,create_Di_id,offer_no,erp_di_no)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    form = TKC_T_C_WorkFormData()
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_di  = tkc_di_master.objects.get(id = create_Di_id)
    if request.method=="POST":
         form = TKC_T_C_WorkFormData(request.POST,instance=wo_di)
         if form.is_valid():
             wo_di.term_and_condition = form.cleaned_data['term_and_condition']
             wo_di.save()
             str_erp_di_no=str(erp_di_no)
             erp_di_no='D/'+str_erp_di_no
             return redirect(f"/fqp/create_erp_di_step2/{wo_id}/{create_Di_id}/{offer_no}/{erp_di_no}")
    print("--------OUT------")
    return render (request,'fqp/wo_creater/wo_create_di_step2.html',{'wo':wo,"form":form,'wo_di':wo_di,"offer_no":offer_no,"di_no":erp_di_no})
        
#Added By Aayush
def filtered_data_to_view_DI(request,wo,f_di_no,offer_no,wo_di_object,create_Di_id,di_mapping_data):
    offer_details_list = []
    boq_obj_list_data=[]
    
    for obj in di_mapping_data:
        offer_detail = offer_material_site_stores.objects.filter(wo = wo,id=obj.offer_obj_id,offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1).distinct('wo_material')
        print('offer_detail',offer_detail)
        if offer_detail:
            offer_details_list.append(offer_detail)

    for queryset in offer_details_list:

        for obj in queryset:
            if obj.wo_material:
                item_code = obj.wo_material.item_code   
                boq_data = Offered_Item_Remaining_Quantity.objects.filter(offer_no=offer_no,item_code=item_code)
                if boq_data and boq_data not in boq_obj_list_data:
                    boq_obj_list_data.append(boq_data)
                    continue
        
    print('offer_details_list===',offer_details_list)
    print("boq_obj_list_data",boq_obj_list_data)
    return offer_details_list,boq_obj_list_data

#Added By Aayush
def erp_approver_view_work_order_di(request,di_id,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    address = UserCompanyDataMain.objects.get(user_id_id=wo.supplier)
    wo_di_object  = tkc_di_master.objects.get(id = di_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = wo_di_object.offer_no,PDI_Complete=1,PDI_Approved_Status=1)
    for i in offer_details:
        offer_vendor = i.TKCVendor
    print('di_id:======>',wo_di_object.erp_di_number)
    vendor_address = UserCompanyDataMain.objects.get(user_id_id=offer_vendor.Vendor)
    di_mapping_data = di_mapping.objects.filter(wo = wo,erp_di_number=wo_di_object.erp_di_number,di_obj_id=wo_di_object)
    offer_details_list,boq_obj_list_data=filtered_data_to_view_DI(request,wo,wo_di_object.erp_di_number,wo_di_object.offer_no,wo_di_object,di_id,di_mapping_data)
    zipped_data = zip(offer_details_list, di_mapping_data, boq_obj_list_data)
    return render (request,'fqp/wo_approver/erp_wo_di_view.html',{'officer':officer,'wo':wo,'wo_id':wo_id, "wo_di":wo_di_object,"address":address,"offer_details":offer_details,"vendor_address":vendor_address,"zipped_data":zipped_data})

#Added By Aayush
def ERPWorkOrderDI(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    print("offer-zone",officer.user_zone)
    tkc_data  = tkc_di_master.objects.filter(zone=officer.user_zone, di_send_to_approval_status = True).distinct('wo')
    return render(request, 'fqp/wo_approver/work_order_erp_di_page1.html',
                  {"officer": officer, 'tkc_data': tkc_data})

#code for fake call in creater side
#fake call in wo creater for fake call upload
def fake_call(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=-2,Material__PDI_Complete=1).distinct('offer_no')
    return render(request,'fqp/wo_creater/fake_call.html',{"pdi_assign":pdi_assign})
# show item wise detail in creator side 
def pdi_against_wo(request,offer_no):
    data1 = PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    unique_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    for i in unique_data:
        offer_no=i.offer_no 
    return render(request, 'fqp/wo_creater/vendor_factory_inspection_assined_pdi.html', {'data1': data1,'unique_data':unique_data,'offer_no':offer_no})

# show pdi details item wise in creator side
def pdi_inspection_data_wo(request,item_code,offer_no):
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code=item_code)
    for each in offer_material:
        id=each.id
        flag=each.PDI_Approved_Status
        
    pdi=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    for each in pdi:
        task_id=each.offer_no

    representative_data=Pdi_Inspection_Representive_data.objects.filter(task__offer_no=task_id)
    pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    factory_image=PDI_Factory_image.objects.filter(Offer_Material=id)

    return render(request,'fqp/wo_creater/pdi_view.html',{"representative_data":representative_data,"item_code":item_code,"pdi_data":pdi_data,"list": offer_material,"pdi":pdi,"flag":flag,"offer_no":offer_no,'pdi_images':factory_image})

# code for uplaodin fake call letter by creator
@csrf_exempt
def all_fake_called_data(request,offer_no):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=-2,Material__PDI_Complete=1).distinct('offer_no')
    
    pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)

    if request.method == "POST":
        pdi_file = request.FILES['fake_call_letter']
        for i in pdi_data:   
            i.fake_call_letter=pdi_file             
            i.save()
    return render(request,'fqp/wo_creater/fake_call.html',{"pdi_assign":pdi_assign})




def view_erp_offered_approved_material(request,wo_id,offer_no):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id)
    offer_details = offer_material_site_stores.objects.filter(wo = wo, offer_no = offer_no,PDI_Complete=1,PDI_Approved_Status=1,Material_Offer_Submit_Approved_Status = 1)
    if len(offer_details) == 0:
        offer_details = ""
    return render (request,'fqp/wo_creater/erp_wo_di_offers_material_list.html',{"officer": officer,'offer_material_data':offer_details,"wo":wo,"offer_no":offer_no})


def new_dashboard_ps(request):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC').distinct('user__CompanyName_E')
    
    return render(request, 'ps-dashboard/new_dashboard_data_ps.html',{'con':contractor})


def new_dashboard_history_ps(request,name):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC',user__CompanyName_E=name).order_by('date')
    return render(request, 'ps-dashboard/new_dashboard_data_history_ps.html',{'con':contractor})



def active_inactive_contractor_list_ps(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    from datetime import datetime
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.date.today()
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Authentication_id__isnull=False)).order_by('CompanyName_E')
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
    to_daaa =datetime.datetime.today()
    return render(request, 'ps-dashboard/active_inactive_contractor_list_ps.html', {'data':data,'officer':officer,'contractor':contractor_class,'doc':doc,'to_daaa':to_daaa,'today':today})


def contractor_view_details_ps(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        data_new = User_Registration.objects.get(User_Id=id)
        if data[0].User_type == "TKC":
            type = TKC_Payment.objects.get(id=data[0].Oyt)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
            doc = TKC_Document.objects.filter(user_id=data[0].User_Id)

            doc11 = TKC_Document.objects.filter(user_id=data[0].User_Id).last()
            if doc11.new_data == 1:
                doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                return render(request, 'ps-dashboard/contractor_view_details_ps.html',
                            {'data': data[0],'officer':officer,'doc': doc, 'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})

            elif doc[0].new_data == 0:
                return render(request, 'ps-dashboard/contractor_view_details_ps.html',
                            {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})


    return redirect('/')




def day_wise_count_tkc_ps(request):
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.date.today()
    # contractor = reject_and_approve_summary.objects.filter(Q(user__User_type = 'VENDOR',user__finance_approval=0,user__complete_data=1) | Q(user__complete_data=1,user__User_type = 'VENDOR',user__work_approval=0))
    contractor = User_Registration.objects.filter(Q(User_type = 'VENDOR',finance_approval=0,complete_data=1) | Q(complete_data=1,User_type = 'VENDOR',work_approval=0))
    dgm_days = []

    for j in contractor:
        if not j.reg_date:
            dgm_days.append(4)
        
        else:
            p_days = today-j.reg_date
            dgm_days.append(p_days.days)
    new_data = zip(contractor,dgm_days)
    return render(request, 'ps-dashboard/day_wise_count_tkc_ps.html',{'con':contractor,'today':today,'new_data':new_data})

def new_dashboard_history(request,name):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'VENDOR',user__CompanyName_E=name).order_by('date')
    return render(request, 'ps-dashboard/new_dashboard_data_history_vendor_ps.html',{'con':contractor}) 


def gtp_drawing_auditor_dashboard_ps(request):
    gtp = TKCVendor.objects.filter(TKCWoInfo__zone='CZ').distinct('TKCWoInfo__Contract_Number')
    return render(request, 'ps-dashboard/new_dashboard_data_gtp_data_ps.html',{'gtp':gtp})


def view_gtp_wo_wise_ps(request,id):
    gtp = TKCVendor.objects.filter(TKCWoInfo__id=id)
    return render(request, 'ps-dashboard/view_gtp_wo_wise_ps.html',{'gtp':gtp})    
    
#Added By Aayush Joshi
def assigning_items_to_di(offered_item_codes_remaining_quantity_data,di_no,selected_di_data): 
    selected_di_item_codes_list=[]
    verified_materials_quantity_material_list=[]
    exceeded_di_quantity_then_offered_quantity_item_code_list=[]
    msg='di_quantity_exceeded_then_offered_quantity'
    quantity_to_substract={}
    count=1
    print("offered_item_codes_remaining_quantity_data:::=====>",offered_item_codes_remaining_quantity_data)
    
    for selected_di_item_code in selected_di_data:
        for item_code in offered_item_codes_remaining_quantity_data:
            offer_offer_no=item_code.offer_no
            offer_item_code=item_code.item_code
            offer_item_remaining_quantity=item_code.remaining_quantity
            offer_item_total_quantity=item_code.total_quantity
            print('selected_di_data::---',selected_di_data,len(selected_di_data))
            # for selected_di_item_code in selected_di_data:
            print('selected_di_dataselected_di_dataselected_di_dataselected_di_data',selected_di_data)
            print("selected_di_item_codeselected_di_item_codeselected_di_item_code",selected_di_item_code)
            if selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'] in offer_item_code and selected_di_data[selected_di_item_code]['offer_no'] in offer_offer_no :
                selected_di_item_codes_list.append(selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'])
                print("FOUND IN OFFERED MATERIAL")
                if int(float(selected_di_data[selected_di_item_code]['DI_DET_QTY'])) <= int(float(offer_item_remaining_quantity)):
                    print(f"ITEMS AVAILABLE TO CREATE DI AS selected DI quantity:{int(float(selected_di_data[selected_di_item_code]['DI_DET_QTY']))} ,is less than {int(float(offer_item_remaining_quantity))}")
                    verified_materials_quantity_material_list.append(selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'])
                    di_created_msg="DI created"
                    if selected_di_data[selected_di_item_code]['offer_no'] in quantity_to_substract:
                        quantity_to_substract[selected_di_data[selected_di_item_code]['offer_no']].update({f"itemcode{count}":[selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'],selected_di_data[selected_di_item_code]['DI_DET_QTY']]})
                        count=count+1
                    else:
                        quantity_to_substract[selected_di_data[selected_di_item_code]['offer_no']] = {f"itemcode{count}":[selected_di_data[selected_di_item_code]['DI_DET_ITEM_CODE'],selected_di_data[selected_di_item_code]['DI_DET_QTY']]}
                        count=count+1
                else:
                    print("Unable to create DI. The requested quantityUnable to create DI. The requested quantity")
                    exceed_msg =f"Unable to create DI. The requested quantity:{selected_di_data[selected_di_item_code]['DI_DET_QTY']} exceeds the total remaining balanced-quantity {offer_item_remaining_quantity}."
                    print("HEEEEEEEEEEERRRRRRRRREEEEEEEEEE")
                    exceeded_di_quantity_then_offered_quantity_item_code_list.append(float(selected_di_data[selected_di_item_code]['DI_DET_QTY']))
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&from assigning_items_to_di",quantity_to_substract)
                    return False,exceed_msg,quantity_to_substract
            else:
                print("Selected Item Code is Not present in Remaining Quantity Table")
                pass

    '''Below, we are performing verification to ensure that the quantity of the selected item codes in the dictionary is less than or equal to the total offered quantity for each item code. 
    Additionally, we are validating the length of both the list to ensure that the quantity of material of the selected DI has been verified and is less than the offered material.'''    


    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&from assigning_items_to_di",quantity_to_substract)
    if quantity_to_substract:
        pass
    else:
        exceed_msg= 'Items Not Available to Create DI'
        return False,exceed_msg,quantity_to_substract

    print("****************************************************************",quantity_to_substract)
    
    if len(selected_di_item_codes_list) == len(verified_materials_quantity_material_list):
        print("length matched")
        #we are able to create DI as both of the materials in DI are less than quantity of total offered_material. 
        print(True,di_created_msg,quantity_to_substract)
        return True,di_created_msg,quantity_to_substract
    else:
        print(False,exceed_msg,quantity_to_substract)
        print("HEEEEEERRRRRRRRREEEEEEEEEE")
        return False,exceed_msg,quantity_to_substract

#Added By Aayush
def checking_if_di_already_created(tkc_di_data,erp_di_data_to_view_and_create):
    print('tkc_di_data',tkc_di_data)
    total_tkc_data=len(tkc_di_data)
    keys_to_update = []  # Store the keys that need to be updated
    for di_no in erp_di_data_to_view_and_create:
        for i in range(total_tkc_data):
            print("erp DI NO:",di_no,type(di_no))
            print("dino in database::::",tkc_di_data[i].erp_di_number,type(tkc_di_data[i].erp_di_number))
            if di_no == tkc_di_data[i].erp_di_number:
                keys_to_update.append(di_no)
                break
    for key in keys_to_update:
        erp_di_data_to_view_and_create[key]["Already_Created"] = True

    for key in erp_di_data_to_view_and_create:
        if key not in keys_to_update:
            erp_di_data_to_view_and_create[key]["Already_Created"] = False

    print("in checking_if_di_already_created")
    print("erp_di_data_to_view_and_create",erp_di_data_to_view_and_create)
    return erp_di_data_to_view_and_create

# PDI details for PS sir
def all_discom_pdi(request):
    all_pdi_info={}
    discom_list = ['CZ','EZ','WZ']
    all_pdi_info["approved"]=pdi_data(discom_list,1,None)
    all_pdi_info["asigned"]=pdi_data(discom_list,None,None)
    all_pdi_info["pending"]=pdi_data(discom_list,0,0)
    all_pdi_info["pending_approve"]=pdi_data(discom_list,0,1)
    all_pdi_info["rejected"]=pdi_data(discom_list,-1,1)
    
    cz_pending_assign = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status=1,PDI_Assign=0,wo__zone='CZ',PDI_Approved_Status=0).distinct('offer_no').count()
    ez_pending_assign = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status=1,PDI_Assign=0,wo__zone='EZ',PDI_Approved_Status=0).distinct('offer_no').count()
    wz_pending_assign = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status=1,PDI_Assign=0,wo__zone='WZ',PDI_Approved_Status=0).distinct('offer_no').count()
    
    data = {"cz_pdi_rejected_data":all_pdi_info["rejected"]["CZ"],"ez_pdi_rejected_data":all_pdi_info["rejected"]["EZ"],"wz_pdi_rejected_data":all_pdi_info["rejected"]["WZ"],"cz_assigned_pdi":all_pdi_info["asigned"]["CZ"],"ez_assigned_pdi":all_pdi_info["asigned"]["EZ"],"wz_assigned_pdi":all_pdi_info["asigned"]["WZ"],"cz_pdi_approved_data":all_pdi_info["approved"]["CZ"],"ez_pdi_approved_data":all_pdi_info["approved"]["EZ"],"wz_pdi_approved_data":all_pdi_info["approved"]["WZ"],"discom_list":discom_list,'cz_pdi_pending_data':all_pdi_info["pending_approve"]["CZ"],'wz_pdi_pending_data':all_pdi_info["pending_approve"]["WZ"],'ez_pdi_pending_data':all_pdi_info["pending_approve"]["EZ"],'cz_pdi_pending_ins_data':all_pdi_info["pending"]["CZ"],'ez_pdi_pending_ins_data':all_pdi_info["pending"]["EZ"],'wz_pdi_pending_ins_data':all_pdi_info["pending"]["WZ"],'cz_pending_assign':cz_pending_assign,'wz_pending_assign':wz_pending_assign,'ez_pending_assign':ez_pending_assign}
    response = data
    
    return render(request,'ps-dashboard/all_discom_pdi.html',response)
def pdi_data(discom_list,j,k):
    data={}
    if k == None:
        if j != None and j!=-1:
            for i in discom_list:
                pdi_approved_data = PDI_Inspection_Info.objects.filter(Material__PDI_Approved_Status = j, wo__zone = i).distinct('offer_no').count()
                
                data[i]=pdi_approved_data
        else:
            for i in discom_list:
                pdi_assigned = PDI_Inspection_Info.objects.filter( wo__zone = i).distinct('offer_no').count()
                
                data[i]=pdi_assigned
    elif j==-1:
        for i in discom_list:
            pdi_rejected_data = PDI_Inspection_Info.objects.filter(Material__PDI_Approved_Status = j,wo__zone = i) or PDI_Inspection_Info.objects.filter(Material__PDI_Approved_Status = -2,wo__zone= i).distinct('offer_no').count()
            data[i]=pdi_rejected_data
    else:
        for i in discom_list:
            pdi_pending=PDI_Inspection_Info.objects.filter(Material__PDI_Approved_Status= j,wo__zone= i,Material__PDI_Complete=k).distinct('offer_no').count()
            data[i]=pdi_pending
    return data
        
def all_assigned_pdi_ps(request,zone):
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=zone).distinct('offer_no')
    return render(request,'ps-dashboard/all_pdi_assigned_ps.html',{"pdi_assign":pdi_assign})

def pdi_against_wo_ps(request,offer_no):
    data1 = PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    unique_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    for i in unique_data:
        offer_no=i.offer_no 
    return render(request, 'ps-dashboard/pdi_details.html', {'data1': data1,'unique_data':unique_data,'offer_no':offer_no})

def all_approved_pdi_ps(request,zone):
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,Material__PDI_Approved_Status=1,wo__zone=zone).distinct('offer_no')
    return render(request,'ps-dashboard/all_pdi_assigned_ps.html',{"pdi_assign":pdi_assign})

def all_pending_ins_pdi_ps(request,zone):
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,Material__PDI_Complete=0,Material__PDI_Approved_Status=0,wo__zone=zone).distinct('offer_no')
    return render(request,'ps-dashboard/all_pdi_assigned_ps.html',{"pdi_assign":pdi_assign})

def all_pending_pdi_appr_ps(request,zone):
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,Material__PDI_Complete=1,Material__PDI_Approved_Status=0,wo__zone=zone).distinct('offer_no')
    return render(request,'ps-dashboard/all_pdi_assigned_ps.html',{"pdi_assign":pdi_assign})

def all_rejected_pdi_ps(request,zone):
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Approved_Status = -1,wo__zone = zone) or PDI_Inspection_Info.objects.filter(Material__PDI_Approved_Status = -2,wo__zone= zone).distinct('offer_no')
    return render(request,'ps-dashboard/all_pdi_assigned_ps.html',{"pdi_assign":pdi_assign})

def pdi_pending_assign_ps(request,zone):
    wo = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status=1,PDI_Assign=0,wo__zone=zone,PDI_Approved_Status=0).distinct('offer_no')
    
    return render(request, 'ps-dashboard/pending_pdi_assign_ps.html',
                  {'list': wo})

def view_offer_ps(request,offer_no):
    offer=offer_material_site_stores.objects.filter(offer_no=offer_no,Material_Offer_Submit_Approved_Status=1)
    
    qun_list = []
    total_qun = []
    item_code_list  = []

    for j in offer:
        item_code_list.append(j.wo_material.item_code)

    if(len(set(item_code_list))!=len(item_code_list)):
        new_obj = offer.distinct('wo_material__item_code')
        for i in new_obj:
            offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code =i.wo_material.item_code,Material_Offer_Submit_Approved_Status=1)
            for k in offer_material:
                qun_list.append(k.quantity)
            qty_sum = sum(qun_list)
            total_qun.append(qty_sum)
            qun_list.clear()

    else:
        new_obj = offer
        for i in offer:
            total_qun.append(i.quantity)

    final_data = zip(new_obj,total_qun)
    return render(request,'ps-dashboard/view_offer_ps.html',{"offer":final_data})

#Added By Aayush
def erp_work_order_dispatch_instruction_list(request,wo_id):
    print("erp_work_order_dispatch_instruction_list",wo_id)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_obj = TKCWoInfo.objects.get(id=wo_id)
    tkc_data  = tkc_di_master.objects.filter(wo = wo_obj, di_send_to_approval_status = True)
    print(len(tkc_data))
    print(wo_obj,tkc_data)
    return render(request, 'fqp/wo_approver/erp_work_order_di.html',
    {"officer": officer, 'tkc_data': tkc_data,"wo_obj":wo_obj})


# --------------------shubham tripathi fqqp intimantion new code integrateed here-----------------------
def officer_new_fqpintimation_wo(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        if officer.role.Role_Name == "WO_CREATER":            
            wo_data = TKCWoInfo.objects.filter(Discom_id=officer.Discom_id).order_by('-id')
            base_template_name = "fqp/wo_creater/creater_base.html"
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
        
        elif officer.role.Role_Name == "WO_APPROVER":
            wo_data = Wo_Order_Task.objects.filter(wo__Discom_id=officer.Discom_id).distinct('wo__id')
            base_template_name = "fqp/wo_approver/approver_base.html"
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

        elif officer.role.Role_Name == "PMA":            
            # base_template_name = "po/area_store/pma_officer.html"
            base_template_name = "officer/pma_login.html"
            if officer.Discom is not None and officer.Region is None and officer.Circle is None and officer.Division is None:
                wo_data = Wo_Order_Task.objects.filter(wo__Discom_id=officer.Discom_id).distinct('wo__id')
                return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

            elif officer.Discom is not None and officer.Region is not None and officer.Circle is None and officer.Division is None:
                wo_data = Wo_Order_Task.objects.filter(wo__Discom_id=officer.Discom_id,region_id=officer.Region_id).distinct('wo__id')
                return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is None:
                wo_data = Wo_Order_Task.objects.filter(wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).distinct('wo__id')
                return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None:
                wo_data = Wo_Order_Task.objects.filter(wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id).distinct('wo__id')
                return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
            else:
                wo_data=""
                return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
        
        elif officer.role.Role_Name == "GM(CIRCLE)":
            base_template_name = "officer/gm_circle_login.html"
            wo_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).distinct('wo__id')
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})            

        elif officer.role.Role_Name == "DGM_STC":            
            base_template_name = "officer/dgm_stc_login.html"
            wo_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id__pakage_id__in=[7,8,9,10],wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).distinct('wo__id')
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

        elif officer.role.Role_Name == "DGM_ONM":            
            base_template_name = "officer/dgm_onm_login.html"
            wo_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id__pakage_id__in=[2,3,4,5,6],wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id).distinct('wo__id')
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

        elif officer.role.Role_Name == "JE":
            base_template_name = "officer/je_dashboard.html"
            wo_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id,distribution_center_id=officer.DC_Zone).distinct('wo__id')
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
        else:
            wo_data=""
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'mpeb_login')



def officer_new_fqpintimation_task_create(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        if request.method == "POST":
            wo_id = request.POST.get('wo_id')
            region_id = request.POST.get('region_id')
            circle_id = request.POST.get('circle_id')
            division_id = request.POST.get('division_id')
            distribution_center_id = request.POST.get('distribution_center_id')
            gis_feeder_id = request.POST.get('gis_feeder_id')
            erp_estimate_no = request.POST.get('erp_estimate_no')
            erp_gbpa_no = request.POST.get('erp_gbpa_no')
            package_name_and_no = request.POST.get('package_name_and_no')
            description_of_work = request.POST.get('description_of_work')
            substation_name_on_which_work_proposed = request.POST.get('substation_name_on_which_work_proposed')
            feeder_name_on_which_work_proposed = request.POST.get('feeder_name_on_which_work_proposed')
            if distribution_center_id is not None and division_id is not None:
                intimation_data = Wo_Order_Task.objects.create(officer_id=officer.employ_id,wo_id=wo_id,region_id=region_id,circle_id=circle_id,division_id=division_id,distribution_center_id=distribution_center_id,gis_feeder_id=gis_feeder_id,erp_estimate_no=erp_estimate_no,erp_gbpa_no=erp_gbpa_no,package_name_and_no=package_name_and_no,description_of_work=description_of_work,feeder_name_on_which_work_proposed=feeder_name_on_which_work_proposed,substation_name_on_which_work_proposed=substation_name_on_which_work_proposed)
            elif division_id is not None and distribution_center_id is None or distribution_center_id =="":
                intimation_data = Wo_Order_Task.objects.create(officer_id=officer.employ_id,wo_id=wo_id,region_id=region_id,circle_id=circle_id,division_id=division_id,gis_feeder_id=gis_feeder_id,erp_estimate_no=erp_estimate_no,erp_gbpa_no=erp_gbpa_no,package_name_and_no=package_name_and_no,description_of_work=description_of_work,feeder_name_on_which_work_proposed=feeder_name_on_which_work_proposed,substation_name_on_which_work_proposed=substation_name_on_which_work_proposed)
            elif distribution_center_id is None or distribution_center_id =="" and division_id is None or division_id =="":
                intimation_data = Wo_Order_Task.objects.create(officer_id=officer.employ_id,wo_id=wo_id,region_id=region_id,circle_id=circle_id,gis_feeder_id=gis_feeder_id,erp_estimate_no=erp_estimate_no,erp_gbpa_no=erp_gbpa_no,package_name_and_no=package_name_and_no,description_of_work=description_of_work,feeder_name_on_which_work_proposed=feeder_name_on_which_work_proposed,substation_name_on_which_work_proposed=substation_name_on_which_work_proposed)            
            else:
                intimation_data = Wo_Order_Task.objects.create(officer_id=officer.employ_id,wo_id=wo_id,region_id=region_id,circle_id=circle_id,division_id=division_id,gis_feeder_id=gis_feeder_id,erp_estimate_no=erp_estimate_no,erp_gbpa_no=erp_gbpa_no,package_name_and_no=package_name_and_no,description_of_work=description_of_work,feeder_name_on_which_work_proposed=feeder_name_on_which_work_proposed,substation_name_on_which_work_proposed=substation_name_on_which_work_proposed)                
            milestone = request.POST.getlist('milestone_id[]')
            if intimation_data is not None:
                for i in milestone:
                    wo_mile_data= Wo_Task_Milestone.objects.create(milestone_id=i,wo_task_id=intimation_data.id)           
            return redirect('officer_new_fqpintimation_wo')
        else:
            wo_id = request.GET.get('woid')
            wo_data=TKCWoInfo.objects.filter(id=wo_id).first()
            rm_data=Region_Master.objects.filter(Discom_id = wo_data.Discom)
            mile_data = Milestone_Main.objects.all()
            base_template_name = "fqp/wo_creater/creater_base.html"            
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_task_create.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'rm_data':rm_data,"mile_data":mile_data})
    else:
        return redirect(str(curl)+'mpeb_login')


def officer_new_fqpintimation_addmilestone(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        if request.method == "POST":
            wo_id = request.POST.get('wo_id')
            taskid = request.POST.get('taskid')
            milestone = request.POST.getlist('milestone_id[]')
            if taskid is not None:
                for i in milestone:
                    wo_mile_data= Wo_Task_Milestone.objects.create(milestone_id=i,wo_task_id=taskid)            
            return redirect('officer_new_fqpintimation_wo')
        else:
            wo_id = request.GET.get('woid')
            wo_taskid = request.GET.get('wo_taskid')
            wo_task_data=Wo_Order_Task.objects.filter(wo_id=wo_id,id=wo_taskid).first()
            
            mile_data = Milestone_Main.objects.all()
            task_mile_data = Wo_Task_Milestone.objects.filter(wo_task_id=wo_taskid)            
            return render(request, 'fqp/new_fqpintimation/addmilestone.html', {'officer': officer,'wo_task_data':wo_task_data,"mile_data":mile_data,'task_mile_data':task_mile_data})
    else:
        return redirect(str(curl)+'mpeb_login')

        



def officer_new_fqpintimation_tasklist(request):
    wo_id=request.GET.get('woid')
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        wo_data=TKCWoInfo.objects.filter(Discom_id=officer.Discom_id,id=wo_id)
        mldata=Wo_Task_Milestone.objects.all()
        
        if officer.role.Role_Name =="WO_CREATER":
            wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id).order_by('-id')
            base_template_name = "fqp/wo_creater/creater_base.html"
            return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})
        
        elif officer.role.Role_Name =="WO_APPROVER":
            wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id).order_by('-id')
            base_template_name = "fqp/wo_approver/approver_base.html"
            return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})
        
        elif officer.role.Role_Name == "PMA":
            # base_template_name = "po/area_store/pma_officer.html"
            base_template_name = "officer/pma_login.html"
            if officer.Discom_id is not None and officer.Region_id is None and officer.Circle_id is None and officer.Division_id is None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id).order_by('-id')
                return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is None and officer.Division_id is None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id).order_by('-id')
                return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).order_by('-id')
                return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id).order_by('-id')
                return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})
        
            else:
                wo_task_data=""
                return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})
        
        elif officer.role.Role_Name == "GM(CIRCLE)":
            base_template_name = "officer/gm_circle_login.html"
            wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).order_by('-id')
            return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

        elif officer.role.Role_Name == "DGM_STC":            
            base_template_name = "officer/dgm_stc_login.html"
            wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id__pakage_id__in=[7,8,9,10],wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).order_by('-id')
            return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

        elif officer.role.Role_Name == "DGM_ONM":            
            base_template_name = "officer/dgm_onm_login.html"
            wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id__pakage_id__in=[2,3,4,5,6],wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id).order_by('-id')
            return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

        elif officer.role.Role_Name == "JE":
            base_template_name = "officer/je_dashboard.html"
            wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id,distribution_center_id=officer.DC_Zone).order_by('-id')            
            return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

        else:
            wo_data=""
            wo_task_data=""
            return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

    else:
        return redirect(str(curl)+'mpeb_login')


def officer_new_fqpintimation_list(request):
    wo_id=request.GET.get('woid')
    wo_taskid=request.GET.get('wotaskid')
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        wo_data=TKCWoInfo.objects.filter(Discom_id=officer.Discom_id,id=wo_id)
        wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id)
        wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id)        
        fqpinti_mile_cat_data = New_FqpIntimation_milestone_category.objects.all().order_by('-id')
        if officer.role.Role_Name =="WO_CREATER":
            base_template_name = "fqp/wo_creater/creater_base.html"
            return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name =="WO_APPROVER":
            base_template_name = "fqp/wo_approver/approver_base.html"
            return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "PMA":            
            # base_template_name = "po/area_store/pma_officer.html"
            base_template_name = "officer/pma_login.html"
            if officer.Discom_id is not None and officer.Region_id is None and officer.Circle_id is None and officer.Division_id is None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id).order_by('-id')
                wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task__id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id)
                return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is None and officer.Division_id is None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id).order_by('-id')
                wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id).distinct('wo__id')
                return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).order_by('-id')
                wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).order_by('-id')
                return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None:
                wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id).order_by('-id')
                wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_id=wo_id,wo_task__id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id)
                return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})
            else:
                wo_task_data=""
                wo_fqpi_data=""
                return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "GM(CIRCLE)":
            base_template_name = "officer/gm_circle_login.html"
            wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).order_by('-id')
            wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).order_by('-id')
            return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "DGM_STC":            
            base_template_name = "officer/dgm_stc_login.html"
            wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),wo_id__pakage_id__in=[7,8,9,10],id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id).order_by('-id')
            wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wotask_milestone__milestone__id__in=[2,3,6]).order_by('-id')
            return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "DGM_ONM":            
            base_template_name = "officer/dgm_onm_login.html"
            wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),wo_id__pakage_id__in=[2,3,4,5,6],id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id).order_by('-id')
            wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wotask_milestone__milestone__id__in=[1,4,5]).order_by('-id')
            return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "JE":            
            base_template_name = "officer/je_dashboard.html"
            wo_task_data = Wo_Order_Task.objects.filter(~Q(status=-1),id=wo_taskid,wo_id=wo_id,wo__Discom_id=officer.Discom_id,region_id=officer.Region_id,circle_id=officer.Circle_id,division_id=officer.Division_id,distribution_center_id=officer.DC_Zone).order_by('-id')
            wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_taskid,wo_task_id__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wo_task__distribution_center_id=officer.DC_Zone).order_by('-id')
            return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})
        else:
            wo_task_data=""
            wo_fqpi_data=""
            base_template_name = ""
            return render(request, 'fqp/new_fqpintimation/officer_intimation_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_fqpi_data':wo_fqpi_data,'wo_task_data':wo_task_data,'wo_data':wo_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})
    else:
        return redirect(str(curl)+'mpeb_login')

def officer_new_fqpintimation_observation_detail(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        fqpintimation_id = request.GET.get('fqpintimationid')
        wo_id = request.GET.get('woid')
        wotask_id = request.GET.get('wotaskid')
        fqpinti_mile_cat_data = New_FqpIntimation_milestone_category.objects.all()
        task_data=Wo_Order_Task.objects.filter(id=wotask_id,wo__Discom_id=officer.Discom_id)
        int_data=New_FqpIntimation.objects.filter(wo_task_id=wotask_id,id=fqpintimation_id,wo_task_id__wo__Discom_id=officer.Discom_id,)
        observation=New_FqpIntimation_Observation.objects.filter(fqpintimation_id=fqpintimation_id)
        officer_data=New_FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id)
        close_inti=New_FqpIntimation_Observation_Close.objects.filter(fqpintimation_id=fqpintimation_id)
        
        observation_data = New_FqpIntimation_Observation_data.objects.filter(observation__fqpintimation_id=fqpintimation_id)
        if officer.role.Role_Name =="WO_CREATER":
            base_template_name = "fqp/wo_creater/creater_base.html"
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_observation_detail.html', {'officer': officer,'base_template_name':base_template_name,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name =="WO_APPROVER":
            base_template_name = "fqp/wo_approver/approver_base.html"
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_observation_detail.html', {'officer': officer,'base_template_name':base_template_name,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "PMA":            
            # base_template_name = "po/area_store/pma_officer.html"
            base_template_name = "officer/pma_login.html"
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_observation_detail.html', {'officer': officer,'base_template_name':base_template_name,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "GM(CIRCLE)":
            base_template_name = "officer/gm_circle_login.html"
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_observation_detail.html', {'officer': officer,'base_template_name':base_template_name,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "DGM_STC":            
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_observation_detail.html', {'officer': officer,'base_template_name':base_template_name,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "DGM_ONM":            
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_observation_detail.html', {'officer': officer,'base_template_name':base_template_name,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})

        elif officer.role.Role_Name == "JE":
            base_template_name = "officer/je_dashboard.html"
            return render(request, 'fqp/new_fqpintimation/officer_fqpintimation_observation_detail.html', {'officer': officer,'base_template_name':base_template_name,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})
    else:
        return redirect(str(curl)+'mpeb_login')


def officer_new_fqpintimation_resurvey_observation(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        if officer.role.Role_Name=="DGM_STC" or officer.role.Role_Name=="DGM_ONM": 
            if request.method == "POST":
                fqpintimation_id = request.POST.get('fqpintimation_id')
                observation_id=request.POST.get('observation_id')
                observation_info_id=request.POST.get('observation_info_id')
                observation_count = request.POST.get('observation_count')
                re_survey_remark = request.POST.get('re_survey_remark')
                re_survey_status=request.POST.get('re_survey_status')
                re_survey_date = request.POST.get('re_survey_date')
                re_survey_image = request.FILES['re_survey_image']
                if int(observation_count) <= 2:
                    New_FqpIntimation_Observation.objects.filter(id=observation_id,fqpintimation_id=fqpintimation_id).update(observation_count=int(observation_count),observation_status=re_survey_status)
                    New_FqpIntimation_Observation_data.objects.filter(observation_id=observation_id,id=observation_info_id).update(officer_id=officer.employ_id,re_survey_remark=re_survey_remark,re_survey_status=re_survey_status,re_survey_date=re_survey_date,re_survey_image=re_survey_image)
                    if 1 == int(re_survey_status):
                        New_FqpIntimation.objects.filter(id=fqpintimation_id).update(intimation_status = re_survey_status)
#--------------- for save message to contractor when task created against to that work order
                    inti_data=New_FqpIntimation.objects.filter(id=fqpintimation_id).first()
                    try:
                        wo_data=TKCWoInfo.objects.filter(id=inti_data.wo_task_id.wo_id).first()
                        if wo_data is not None:
                            userdata=User_Registration.objects.filter(User_Id=wo_data.supplier_id)
                            # print("ofc---len--------------",len(ofc))
                            template_id = 1007035105565881711 
                            # userdata = userdata
                            var1 = " " + str(inti_data.wo_task_id.gis_feeder_id)+" "
                            var2 = " " + str(wo_data.Header.Contract_Description)+ " "
                            otherdata = ""
                            message_type = "FQP Intimation Review"
                            if userdata is not None:
                                cmsg.send_message(template_id,userdata,var1,var2,otherdata,message_type)#for send message when intimation created
                        else:
                            pass
                    except Exception as e:
                        pass
                # return redirect('officer_new_fqpintimation_wo')
                return redirect(request.META.get('HTTP_REFERER'))

        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(str(curl)+'mpeb_login')


#Added By Aayush
def receiving_api_call(request,contract_no):
    print("in receiving_api_call------------------>",contract_no)
    URL="http://epic.mpezerp.com:80/webservices/rest/qc_portal_tkc_rcv/get_rcv/"
    data={
        "get_rcv": {
        "@xmlns": "http://xmlns.oracle.com/apps/po/rest/qc_portal_tkc_rcv/get_rcv/",
        "RESTHeader": {
        "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
        "Responsibility": "JAI_PURCHASING",
        "RespApplication": "JA",
        "SecurityGroup": "STANDARD",
        "NLSLanguage": "AMERICAN",
        "Org_Id": "83"
        },
        "InputParameters": {
        "P_CONTRACT_NO":contract_no
        }
        }
        }
        
    json_data = json.dumps(data)
    auth_values = HTTPBasicAuth(const.Username, const.Password)
    # try:
        # calling API here with all the payload and endpoint details.
    res = req.post(url=URL, auth=auth_values, headers=const.headers, data=json_data) 
    if res.status_code == 200:
        receiving_data = res.json()
        if receiving_data['OutputParameters']['P_PO_RCV']is None:
            return False,False
        elif receiving_data['OutputParameters']['P_ERRORS']is not None:
            return res.status_code,receiving_data['OutputParameters']['P_PO_RCV']['P_ERRORS']['P_ERRORS_ITEM']['ERROR_MESSAGE']
        elif receiving_data['OutputParameters']['P_PO_RCV']['P_PO_RCV_ITEM'] is not None:
            print("heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyy")
            print(res.status_code,receiving_data)
            print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
            return res.status_code,receiving_data        
    else:
        print("in else---------->",res.status_code,False)
        return res.status_code,False

    # except:
    #     return False,False


# Added By Aayush
def view_receiving_details(request,wo_id,di_no,offer_no):
    print("in view_receiving_details")
    erp_di_no="D/"+str(di_no)
    print('erp_di_no--->',erp_di_no)
    print("di_no",di_no)
    print(wo_id,di_no,offer_no)
    offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,wo=wo_id).first()
    if not tkc_di_master.objects.filter(erp_di_number = erp_di_no,offer_no=offer_no).exists():
        message = messages.error(request, f"No DI Available for this DI No.{di_no}")
        return render (request,'fqp/wo_creater/receiving_details.html',{"officer": officer,"wo":wo,"di_no":di_no,"receiving_details_data":receiving_details_data})
    
    tkc_di_master_obj=tkc_di_master.objects.get(erp_di_number = erp_di_no,offer_no=offer_no)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.get(id=wo_id, Status=1)
    contract_number=wo.Contract_Number
    
    #calling receiving api 
    receiving_api_status,receiving_api_res_data=receiving_api_call(request,contract_number)

    if receiving_api_status == 200 and receiving_api_res_data is not None :
        print(receiving_api_status)
        receiving_data_len=len((receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM']))
        for index in range(0,receiving_data_len):

            api_di_no=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]['DI_REF2']
            print("api_di_no",api_di_no,type(api_di_no),erp_di_no)
            if str(erp_di_no) in api_di_no:
                print("di_no found :::::",di_no)      
                if not receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["RCV_DET_QTY"] == '0':
                    receiving_ref_no=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["RECEIVING_REF"]
                    receiving_location=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["RCV_LOCATION"]
                    receiving_delievery_date=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["DELIVERY_DATE"]
                    inspection_no=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["INSPECTION_REF3"]
                    inspection_date=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["INSPECTION_DATE3"]
                    receiving_item_code=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["RCV_DET_ITEM_CODE"]
                    receiving_item_code_desc=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["RCV_DET_ITEM_DESC"]
                    receiving_det_qty=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["RCV_DET_QTY"]
                    receiving_remarks=receiving_api_res_data['OutputParameters']["P_PO_RCV"]['P_PO_RCV_ITEM'][index]["RCV_DET_REMARKS"]
                    
                    print("--------------------------------------------------------------------------------------------------------------")
                    
                    if di_receiving_details_data.objects.filter(di_obj=tkc_di_master_obj,receiving_item_code=receiving_item_code,inspection_number=inspection_no,receiving_ref_number=receiving_ref_no).exists():
                        print("Receiving for this DI is already done.")
                        message = messages.success(request, f"Receiving for this DI is already done {di_no}.")
                        pass
                    #     print("tkc_di_master_obj",tkc_di_master_obj)
                    #     receiving_details_data=di_receiving_details_data.objects.filter(di_obj=tkc_di_master_obj,inspection_number=inspection_no)
                    #     print("hhhhhhhhhhhhhhhhhhhhhreceiving_details_data",receiving_details_data)
                    #     return render (request,'fqp/wo_creater/receiving_details.html',{"officer": officer,"offer_no":offer_no,"wo":wo,"di_no":di_no,"receiving_details_data":receiving_details_data})
                    else:
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        receiving_details_data=di_receiving_details_data(wo=wo,di_obj=tkc_di_master_obj,offer_obj=offer_material,
                        receiving_ref_number=receiving_ref_no,erp_di_number = di_no,rec_delievery_date=receiving_delievery_date,
                        receiving_location=receiving_location,inspection_number=inspection_no,inspection_date=inspection_date,
                        receiving_item_code=receiving_item_code,receiving_item_code_desc=receiving_item_code_desc,
                        receiving_quantity=receiving_det_qty,receiving_remarks=receiving_remarks)
                        receiving_details_data.save()
                        print("record added")
                        continue
                else:
                    continue
            else:
                continue
        
            if di_receiving_details_data.objects.filter(di_obj=tkc_di_master_obj,inspection_number=inspection_no).exists():
                print("Receiving for this DI is already done.")
                message = messages.success(request, f"Receiving for this DI is already done {di_no}.")
                print("tkc_di_master_obj",tkc_di_master_obj)
                receiving_details_data=di_receiving_details_data.objects.filter(di_obj=tkc_di_master_obj,inspection_number=inspection_no)
                return render (request,'fqp/wo_creater/receiving_details.html',{"officer": officer,"offer_no":offer_no,"wo":wo,"di_no":di_no,"receiving_details_data":receiving_details_data})
        print("Receiving for this DI is not done Yet")
        message = messages.success(request, f"DI Receiving for this DI no. {di_no} is not done Yet .")
        return render (request,'fqp/wo_creater/receiving_details.html',{"officer": officer,"wo":wo,"di_no":di_no})
    else:
        return render(request, 'main/error_page.html')


def upload_erp_di_copy(request,offer_no,erp_di_no,wo_id):
    print("herer",type(erp_di_no),erp_di_no)
    erp_di_no='D/'+str(erp_di_no)
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    di_pdf =  request.FILES['di_doc']
    di_object  = tkc_di_master.objects.get(offer_no = offer_no,erp_di_number = erp_di_no)
    di_object.created_di_doc = di_pdf
    di_object.di_send_to_approval_status = 1
    di_object.di_send_by_approval_by =officer.employ_name
    di_object.save()
    wo_obj = TKCWoInfo.objects.get(id = wo_id)
    wo_di_objects  = tkc_di_master.objects.filter(wo = wo_obj).order_by('-id')
    return render(request, 'fqp/wo_creater/created_wo_di.html',
                  {"wo_di_objects": wo_di_objects,"wo_obj":wo_obj})

def delete_non_approved_di(request,di_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    print("di_id",di_id)
    di_object  = tkc_di_master.objects.get(id=di_id)
    erp_di_id='D/'+str(di_id)
    wo_id=di_object.wo_id
    erp_di_number=di_object.erp_di_number
    di_offer_no=di_object.offer_no
    print("di_offer_no",di_offer_no)
    offered_material_data = offer_material_site_stores.objects.filter(offer_no=di_offer_no)
    di_object  = tkc_di_master.objects.get(id=di_id)
    if di_object :
        di_mapping_data = di_mapping.objects.filter(wo = wo_id,erp_di_number=erp_di_number,di_obj_id=di_object)
        print("di_mapping_data",di_mapping_data)
        if di_mapping_data is not None :
            for i in di_mapping_data:
                offer_id=i.offer_obj_id
                di_quantity=i.di_quantity
                di_mapping_erp_di_number=i.erp_di_number
                di_mapping_wo_id=i.wo_id
                for material in offered_material_data:
                    if offer_id == material.id:
                        print("item_code----->",offer_id,material.id)
                        print("material.wo_material_id",material.wo_material_id)
                        boq_data  = tkc_wo_items_boq.objects.filter(id = material.wo_material_id).values_list('item_code', flat=True)
                        item_code=boq_data.first()
                        # print("wo_id---->",wo_id)
                        item = Offered_Item_Remaining_Quantity.objects.get(item_code=item_code,offer_no=di_offer_no)
                        print("Addition in remaining Quantity :",int(item.remaining_quantity)+int(di_quantity))
                        item.remaining_quantity=int(item.remaining_quantity) + int(di_quantity)
                        print(item.remaining_quantity)
                        item.already_di_issued_quantity=int(item.already_di_issued_quantity) - int(di_quantity)
                        print("item.already_di_issued_quantity---->",item.already_di_issued_quantity)
                        if item.already_di_issued_quantity < 0:
                            item.already_di_issued_quantity = 0
                            item.save()
                        else:
                            item.save()
            di_mapping_data.delete()
            print("di_mapping_data--->",di_mapping_data)
            print(di_id,erp_di_number,type(erp_di_number))
            di_object  = tkc_di_master.objects.get(id=di_id,erp_di_number=erp_di_number)
            print("di_object--->",di_object)
            di_object.delete()
            message = messages.success(request, f"DI Deleted Successfully for DI No:{erp_di_number}")
            return redirect('all_wo_di')
        else:
            pass
        
# to do list for wo_creater
    
def to_do_list(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])  
    officer_zone = officer.Discom.Discom_Code
    BG = TKCWoInfo_Bg.objects.filter(BG_Approved_Status=0, BG_Submit=0, TKCWoInfo__Discom__Discom_Code=officer_zone, Status=-1).distinct('TKCWoInfo')
    len_bg = len(BG)
    gtp = TKCVendor.objects.filter(TKCVendor_Submit=1, TKCWoInfo__Discom__Discom_Code=officer_zone, TKCVendor_Approved_Status=0).distinct('TKCWoInfo')
    len_gtp = len(gtp)
    material_offer = offer_material_site_stores.objects.filter(Material_Offer_Submit=1, Material_Offer_Submit_Approved_Status=0, wo__Discom__Discom_Code=officer_zone,offer_no__isnull = False).distinct('wo')
    len_material_offer = len(material_offer)
    di_data = offer_material_site_stores.objects.filter(is_di_created = False, DI_Created_Status=0, wo__Discom__Discom_Code=officer_zone,).distinct('wo')
    len_di_data = len(di_data)
    mrc_data = offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, tkc_mrc_initiate=0,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone)
    len_mrc_data = len(mrc_data)
    print("{{{{{{{}}}}}}}",  len_mrc_data)
   
    return render(request, 'fqp/wo_creater/to_do_list.html',{"len_bg":len_bg, "len_gtp":len_gtp, "len_material_offer":len_material_offer,
                                                             "len_di_data":len_di_data, 'len_mrc_data':len_mrc_data})
                                                         
                                                             


def bg_approval_list(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])   
    officer_zone = officer.Discom.Discom_Code      
    BG = TKCWoInfo_Bg.objects.filter(BG_Approved_Status=0, TKCWoInfo__Discom__Discom_Code=officer_zone, BG_Submit=0, Status=-1).distinct('TKCWoInfo')
    data_dict = {}
    for i in BG:
        data_list = []         
        data_list.append(i.TKCWoInfo.Contract_Number)
        data_list.append(i.TKCWoInfo.Header.Contract_Description)        
        data_list.append(i.TKCWoInfo.supplier.CompanyName_E)   
        
        data_dict[i.TKCWoInfo.id] = data_list
    return render(request, 'fqp/wo_creater/bg_approval_list.html', {"officer": officer, 'BG': BG, 'data_dict' : data_dict})
    

def bg_approval_data(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])     
    officer_zone = officer.Discom.Discom_Code          
    BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo =wo_id, TKCWoInfo__Discom__Discom_Code=officer_zone, BG_Approved_Status=0, BG_Submit=0, Status=-1)
    return render(request, 'fqp/wo_creater/bg_approval_data.html', {"officer": officer, 'BG': BG})


def submit_bg_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        if TKCWoInfo_Bg.objects.filter(id=wo_id, Status=1).exists():
            Advance = TKCWoInfo_Bg.objects.get(id=wo_id, Status=1)
            if int(request.POST.get('action')):
                Advance.BG_Approved_Status = 1
            else:
                Advance.BG_Approved_Status = -1
            Advance.BG_Approved_Remark = request.POST.get('remark')
            # Advance.BG_Approved_copy = request.FILES[wo_id]
            Advance.BG_Approved_At = datetime.datetime.now().date()
            Advance.BG_Approved_By = officer.employ_name
            Advance.save()
            BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=Advance.TKCWoInfo, BG_Approved_Status=0, BG_Submit=0, Status=-1)
            return render(request, 'fqp/wo_creater/bg_approval_data.html', {"officer": officer,'BG': BG})
    wo = TKCWoInfo.objects.get(id=wo_id)
    BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=wo, BG_Approved_Status=0, BG_Submit=0, Status=-1)
    return render(request, 'fqp/wo_creater/bg_approval_data.html', {"officer": officer, 'wo': wo, 'BG': BG})



def pending_gtp_approval(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_discom = officer.Discom.Discom_Code     
    Vendor = TKCVendor.objects.filter(TKCVendor_Submit=1 , TKCVendor_Approved_Status=0, TKCWoInfo__Discom__Discom_Code=wo_discom).distinct('TKCWoInfo')
    data_dict = {}
    for i in Vendor:
        data_list = [] 
        gtp_count = TKCVendor.objects.filter(TKCWoInfo = i.TKCWoInfo,TKCVendor_Submit=1, TKCWoInfo__Discom__Discom_Code=wo_discom, TKCVendor_Approved_Status=0).count()
        data_list.append(i.TKCWoInfo.Contract_Number)
        data_list.append(i.TKCWoInfo.Header.Contract_Description)        
        data_list.append(i.TKCWoInfo.supplier.CompanyName_E)
        data_list.append(gtp_count)
        
        data_dict[i.TKCWoInfo.id] = data_list
    # wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone).order_by('-id')
    return render(request, 'fqp/wo_creater/pending_gtp_approval.html',
                  {"officer": officer,  'data_dict': data_dict, 'wo_discom':wo_discom})

def pending_gtp(request, wo_id):
    # wo_discom = wo.Discom.Discom_Code
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_discom = officer.Discom.Discom_Code
    Vendor = TKCVendor.objects.filter(TKCWoInfo =wo_id ,TKCVendor_Submit=1, TKCWoInfo__Discom__Discom_Code=wo_discom, TKCVendor_Approved_Status=0)
    return render(request, 'fqp/wo_creater/pending_gtp.html', {"officer": officer,  'Vendor': Vendor, 'wo_discom':wo_discom, 'wo_id' : wo_id})

def submit_vendor_approval(request, wo_id,tkc_vendor_id):
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_discom = wo.Discom.Discom_Code
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    if request.method == "POST":
        other_gtp_doc = request.FILES['other_gtp_doc']
        if TKCVendor.objects.filter(id=tkc_vendor_id, Status=1).exists():
            Advance = TKCVendor.objects.get(id=tkc_vendor_id, Status=1)
            if int(request.POST.get('action')):
                Advance.TKCVendor_Approved_Status = 1
            else:
                Advance.TKCVendor_Approved_Status = -1
            Advance.TKCVendor_Approved_Remark = request.POST.get('remark')
            Advance.TKCVendor_Approved_At = datetime.datetime.now().date()
            Advance.TKCVendor_Approved_By = officer.employ_name
            Advance.other_acceptance_rejection_doc = other_gtp_doc
            Advance.save()
            # Vendor = TKCVendor.objects.filter(TKCWoInfo=Advance.TKCWoInfo, TKCVendor_Submit=1, Status=1)
            Vendor = TKCVendor.objects.filter(TKCWoInfo =wo_id ,TKCVendor_Submit=1 , TKCVendor_Approved_Status=0)
            return render(request, 'fqp/wo_creater/pending_gtp.html',
                          {"officer": officer,'Vendor': Vendor,"wo_discom":wo_discom})
    # Vendor = TKCVendor.objects.filter(TKCWoInfo=wo, TKCVendor_Submit=1, Status=1)
    Vendor = TKCVendor.objects.filter(TKCWoInfo =wo_id ,TKCVendor_Submit=1 , TKCVendor_Approved_Status=0)
    return render(request, 'fqp/wo_creater/pending_gtp.html', {"officer": officer, 'wo': wo, 'Vendor': Vendor,"wo_discom":wo_discom})



def material_offer_approval_list(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])    
    wo_discom = officer.Discom.Discom_Code
    offer = offer_material_site_stores.objects.filter(Material_Offer_Submit=1, wo__Discom__Discom_Code=wo_discom, Material_Offer_Submit_Approved_Status=0, offer_no__isnull = False).distinct('wo')
    data_dict = {}
    for i in offer:
        data_list = [] 
        offer_count = offer_material_site_stores.objects.filter(wo = i.wo, Material_Offer_Submit=1, wo__Discom__Discom_Code=wo_discom, Material_Offer_Submit_Approved_Status=0, offer_no__isnull = False).distinct("offer_no").count()
        data_list.append(i.wo.Contract_Number)
        data_list.append(i.wo.Header.Contract_Description)        
        data_list.append(i.wo.supplier.CompanyName_E)
        data_list.append(offer_count)
        
        data_dict[i.wo.id] = data_list
    return render(request, 'fqp/wo_creater/material_offer_approval_list.html', {"officer": officer, 'data_dict' : data_dict, 'offer': offer, "wo_discom":wo_discom})
    

def pending_material_offer_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])    
    wo_discom = officer.Discom.Discom_Code
    offer = offer_material_site_stores.objects.filter(wo =wo_id, Material_Offer_Submit=1, wo__Discom__Discom_Code=wo_discom, Material_Offer_Submit_Approved_Status=0, offer_no__isnull = False).distinct("offer_no")
    return render(request, 'fqp/wo_creater/pending_material_offer_approval.html', {"officer": officer, "wo_discom":wo_discom, "offer":offer})
   
 
 
  
def pending_di_list(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    officer_zone = officer.Discom.Discom_Code
    offer_details = offer_material_site_stores.objects.filter(PDI_Approved_Status=1,PDI_Complete=1,is_di_created = False, wo__Discom__Discom_Code=officer_zone, DI_Created_Status=0, is_di_required=True, Material_Offer_Submit_Approved_Status=1,offer_no__isnull = False).distinct('wo')
    data_dict = {}
    for i in offer_details:
        data_list = [] 
        di_count = offer_material_site_stores.objects.filter(PDI_Approved_Status=1,PDI_Complete=1,wo = i.wo, is_di_created = False, wo__Discom__Discom_Code=officer_zone, DI_Created_Status=0, is_di_required=True, Material_Offer_Submit_Approved_Status=1,offer_no__isnull = False).distinct('offer_no').count()
        # print("di_count", di_count)
        data_list.append(i.wo.Contract_Number)
        data_list.append(i.wo.Header.Contract_Description)        
        data_list.append(i.wo.supplier.CompanyName_E)
        data_list.append(di_count)
        
        data_dict[i.wo.id] = data_list
    return render (request,'fqp/wo_creater/pending_di_offer.html',
                   {"officer": officer,'offer_material_data':offer_details, "data_dict" : data_dict})

 
 
def pending_di(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    officer_zone = officer.Discom.Discom_Code
    offer_details = offer_material_site_stores.objects.filter(wo = wo_id, PDI_Approved_Status=1,PDI_Complete=1,wo__Discom__Discom_Code=officer_zone, is_di_created = False, DI_Created_Status=0, is_di_required=True, Material_Offer_Submit_Approved_Status=1,offer_no__isnull = False ).distinct('offer_no')
    return render (request,'fqp/wo_creater/pending_di.html',{"officer": officer,'offer_material_data':offer_details})
    
def officer_invoice_list(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()
    wo_data = TKCWoInfo.objects.annotate(total_invoice_ammount=Sum('work_order_data__total_invoice_amount'),num_invoice=Count('work_order_data')).filter(Wo_Approved_Status=1, Discom_id=officer.Discom_id, num_invoice__gt=0).order_by('-id')
    wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
    return render(request, 'fqp/wo_invoice/officer_creater_wo_invoicelist.html', {'officer': officer,'wo_amt':wo_amt,'wo_data':wo_data})
        

def officer_fqpintimation_data(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        wo_data = FqpIntimation.objects.filter(wo_id__Discom_id=officer.Discom_id, intimation_status=0).distinct('wo__id')
        if officer.role.Role_Name =="WO_CREATER":
            return render(request, 'fqp/wo_creater/fqpintimation/fqp_intimation.html', {'officer': officer,'wo_data':wo_data})
        elif officer.role.Role_Name =="WO_APPROVER":
            # wo_data = TKCWoInfo.objects.filter(Discom_id=officer.Discom_Id)
            return render(request, 'fqp/wo_approver/fqpintimation/fqp_intimation.html', {'officer': officer,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'mpeb_login')
    
    
def fqp_fqpintimation_list(request):
    wo_id=request.GET.get('woid')
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        wo_fqpi_data=FqpIntimation.objects.filter(~Q(status=-1),wo_id=wo_id, intimation_status=0)
        wo_data=TKCWoInfo.objects.filter(Discom_id=officer.Discom_id,id=wo_id)
        if officer.role.Role_Name =="WO_CREATER":
            return render(request, 'fqp/wo_creater/fqpintimation/tkc_intimation_list.html', {'officer': officer,'wo_fqpi_data':wo_fqpi_data,'wo_data':wo_data})
        elif officer.role.Role_Name =="WO_APPROVER":
            return render(request, 'fqp/wo_approver/fqpintimation/tkc_intimation_list.html', {'officer': officer,'wo_fqpi_data':wo_fqpi_data,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'mpeb_login')
    
    
def officer_fqp_intimation(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        fqpintimation_id = request.GET.get('fqpintimation_id')
        int_data=FqpIntimation.objects.filter(id=fqpintimation_id, intimation_status=0)
        observation_data=FqpIntimation_Observation_Info.objects.filter(fqpintimation_id=fqpintimation_id, observation_status=0)
        officer_data=FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id, status=0)
        close_inti=FqpIntimation_Observation_Close.objects.filter(fqpintimation_id=fqpintimation_id, status=0)
        if officer.role.Role_Name =="WO_CREATER":
            return render(request, 'fqp/wo_creater/fqpintimation/fqp_intimation_list.html', {'officer': officer,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation_data':observation_data})
        elif officer.role.Role_Name =="WO_APPROVER":
            return render(request, 'fqp/wo_approver/fqpintimation/tkc_fqpintimation_observation_detail.html', {'officer': officer,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation_data':observation_data})
    else:
        return redirect(str(curl)+'mpeb_login')
    
    
def new_fqpintimation_data(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        if officer.role.Role_Name == "WO_CREATER":            
            wo_data = TKCWoInfo.objects.filter(Discom_id=officer.Discom_id).order_by('-id')
            base_template_name = "fqp/wo_creater/creater_base.html"
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
        
        elif officer.role.Role_Name == "WO_APPROVER":
            wo_data = Wo_Order_Task.objects.filter(wo__Discom_id=officer.Discom_id).distinct('wo__id')
            base_template_name = "fqp/wo_approver/approver_base.html"
            return render(request, 'fqp/new_fqpintimation/wo_intimation.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

        else:
            wo_data=""
            return render(request, 'fqp/new_fqpintimation/intimation_data.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'mpeb_login')
    
    
# def officer_new_fqpintimation_tasklist(request):
#     wo_id=request.GET.get('woid')
#     officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
#     if officer is not None:
#         wo_data=TKCWoInfo.objects.filter(Discom_id=officer.Discom_id,id=wo_id)
#         mldata=Wo_Task_Milestone.objects.all()
        
#         if officer.role.Role_Name =="WO_CREATER":
#             wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id).order_by('-id')
#             base_template_name = "fqp/wo_creater/creater_base.html"
#             return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})
        
#         elif officer.role.Role_Name =="WO_APPROVER":
#             wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom_id=officer.Discom_id).order_by('-id')
#             base_template_name = "fqp/wo_approver/approver_base.html"
#             return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})
            
      
#         else:
#             wo_data=""
#             wo_task_data=""
#             return render(request, 'fqp/new_fqpintimation/officer_intimation_tasklist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'wo_task_data':wo_task_data,"mldata":mldata})

#     else:
#         return redirect(str(curl)+'mpeb_login')
   
    


# to do list for wo_approver    
    
def approver_todo_list(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    officer_zone = officer.Discom.Discom_Code
    wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=0, Wo_Digital_Upload_Status=0, Discom__Discom_Code=officer_zone)
    len_wo_data = len(wo_data)
    tkc_data  = tkc_di_master.objects.filter(di_approved_status=0, wo__Discom__Discom_Code=officer_zone, di_digital_upload_status=0, di_send_to_approval_status = True).distinct('wo')
    len_tkc_data  = len(tkc_data )
    mrc_data = offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, tkc_mrc_initiate=0,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone)
    len_mrc_data = len(mrc_data)
    print("{{{{{{{}}}}}}}",  len_mrc_data)

    return render(request, 'fqp/wo_approver/approver_todo_list.html', {"len_wo_data": len_wo_data, "len_tkc_data": len_tkc_data, 'len_mrc_data':len_mrc_data})
    


    
def pending_wo_approval(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    officer_zone = officer.Discom.Discom_Code
    wo = TKCWoInfo.objects.filter(Wo_Approved_Status=0, Discom__Discom_Code=officer_zone, Wo_Digital_Upload_Status=0)     
    return render(request, 'fqp/wo_approver/pending_wo_approval.html',{"wo" : wo}) 

# # def pending_di_approval(request):
# #     officer = Officer.objects.get(employ_id=request.session['employ_id'])
# #     tkc_data  = tkc_di_master.objects.filter(di_approved_status=0, di_digital_upload_status=0, di_send_to_approval_status = True).distinct('wo')
# #     return render(request, 'fqp/wo_approver/pending_di_approval.html',{"officer": officer,'tkc_data': tkc_data})

def pending_di_list_data(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])  
    officer_zone = officer.Discom.Discom_Code
    tkc_data  = tkc_di_master.objects.filter(di_approved_status=0, wo__Discom__Discom_Code=officer_zone, di_digital_upload_status=0, di_send_to_approval_status = True).distinct('wo')       
    
    data_dict = {}
    for i in tkc_data:
        data_list = []         
        data_list.append(i.wo.Contract_Number)
        data_list.append(i.wo.Header.Contract_Description)        
        data_list.append(i.wo.supplier.CompanyName_E)   
        data_dict[i.wo.id] = data_list
    return render(request, 'fqp/wo_approver/pending_di_approval.html',{"officer": officer,'data_dict': data_dict})




def pending_di_approval(request, wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    officer_zone = officer.Discom.Discom_Code
    tkc_data  = tkc_di_master.objects.filter(wo =wo_id, di_approved_status=0, wo__Discom__Discom_Code=officer_zone, di_digital_upload_status=0, di_send_to_approval_status = True)      
    wo = TKCWoInfo.objects.get(id=wo_id)         
    
    return render(request, 'fqp/wo_approver/pending_di_data.html', {"officer": officer, 'tkc_data': tkc_data, 'wo':wo })


def wo_di_approval(request,di_id,wo_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    officer_zone = officer.Discom.Discom_Code
    wo_obj = TKCWoInfo.objects.get(id=wo_id)
    tkc_data  = tkc_di_master.objects.get(id = di_id)
    tkc_data.di_approved_status = 1
    tkc_data.di_approved_by = officer.employ_name
    tkc_data.save()
    tkc_data1  = tkc_di_master.objects.filter(di_approved_status=0, di_digital_upload_status=0, wo__Discom__Discom_Code=officer_zone, di_send_to_approval_status = True)
    return render(request, 'fqp/wo_approver/pending_di_data.html',
                {"officer": officer, 'tkc_data': tkc_data1,"wo":wo_obj})


def fqp_intimation_data(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        wo_data = FqpIntimation.objects.filter(wo_id__Discom_id=officer.Discom_id).distinct('wo__id')
        if officer.role.Role_Name =="WO_CREATER":
            return render(request, 'fqp/wo_creater/fqpintimation/wo_intimation.html', {'officer': officer,'wo_data':wo_data})
        elif officer.role.Role_Name =="WO_APPROVER":
            # wo_data = TKCWoInfo.objects.filter(Discom_id=officer.Discom_Id)
            return render(request, 'fqp/wo_approver/fqpintimation/wo_intimation.html', {'officer': officer,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'mpeb_login')
    
    
    
def all_rejected_wo_di(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo_di_objects  = tkc_di_master_deleted_history.objects.all().order_by('-id')
    return render(request, 'fqp/wo_creater/all_rejected_wo_di.html',
                  {"wo_di_objects": wo_di_objects,'zone':officer.user_zone})
    
    
def view_site_store_serial_no(request,offer_id):
    offer_data = offer_material_site_stores.objects.get(id = offer_id)
    offer_serial_data = offer_material_serial_number.objects.filter(offer = offer_data)
    return render(request, 'fqp/wo_creater/offer_data_serial_no.html',
                  {"offer_data": offer_data,'offer_serial_data': offer_serial_data})
    
    
    
    
    
    
    
# --------sampling code by PD MISHRA and shubham Tripathi-----------------------------------
def officer_sampling_wo(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        print("login id-----------------",officer.employ_login_id)
        # wo_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[7,8,9,10],is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).distinct('wo_id').order_by('-wo_id')
        # print(wo_data,"--------------wo_data-----------")
        if officer.role.Role_Name == "DGM_STC":
            wo_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[7,8,9,10],site_store_fk__Division__Circle_id=officer.Circle_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).distinct('wo_id').order_by('-wo_id')
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/sampling/sampling_wo_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

        elif officer.role.Role_Name == "DGM_ONM":
            wo_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[2,3,4,5,6],site_store_fk__Division__Circle_id=officer.Circle_id,site_store_fk__Division_id=officer.Division_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).distinct('wo_id').order_by('-wo_id')
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/sampling/sampling_wo_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
        else:
            return redirect(str(curl)+'mpeb_login')
    else:
        return redirect(str(curl)+'mpeb_login')

def officer_sampling_offerlist(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    from decimal import Decimal
    if officer is not None:
        woid=request.GET.get('woid')
        print("############")
        
        if officer.role.Role_Name == "DGM_STC":
            offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[7,8,9,10],site_store_fk__Division__Circle_id=officer.Circle_id,wo_id=woid,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).distinct('tkc_di')
        elif officer.role.Role_Name == "DGM_ONM":
            offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[2,3,4,5,6],site_store_fk__Division__Circle_id=officer.Circle_id,site_store_fk__Division_id=officer.Division_id,wo_id=woid,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).distinct('tkc_di')
        else:        
            offer_data = offer_material_site_stores.objects.filter(wo_id=woid,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).distinct('tkc_di')

        sampling_flag=[]
        for i in offer_data:
            qun=offer_material_site_stores.objects.filter(tkc_di=i.tkc_di).values_list('quantity')
            print("########",qun)
            total_sum = Decimal('0.0')
            for item in qun:
                total_sum += item[0]

            total_sum=math.ceil(total_sum)
            print("##########total sum",total_sum)
            qun_s=offer_material_serial_number.objects.filter(offer_no=i.offer_no,Physical_Status=1,offer__tkc_di=i.tkc_di,Physical_Status_officer_check=1)
            serial_sum=0
            # for i in qun_s:  # commented by shubham tripathi becoze batch quanti nan not woriking 
            #     if i.serial_no is None:
            #         if i.batch_qty != "Nan" :
            #             serial_sum=serial_sum + float(i.batch_qty)
            #         else:
            #             pass
            #     else:
            #         serial_sum= serial_sum + float(1.0)
            
            for i in qun_s:
                if i.serial_no is None:
                    if not math.isnan(i.batch_qty):# add by shubham triapathi for remove nan error on batch quantity
                        serial_sum = serial_sum + float(i.batch_qty)
                    else:
                        pass
                else:
                    serial_sum = serial_sum + float(1.0)

            serial_sum=math.ceil(serial_sum) 
            print("serial_sum",serial_sum)
            if  total_sum == serial_sum:
                flag=1
                print("you can sample this di")
            else:
                flag=0  
            sampling_flag.append(flag)  
        final_data=zip(offer_data,sampling_flag)
        # offer_data = offer_material_serial_number.objects.filter(offer__wo_id=woid,offer__is_di_created=True,offer__wo_id__Discom_id=officer.Discom_id,offer__PDI_Assign=1,offer__PDI_Complete=1,offer__PDI_Approved_Status=1,offer__is_sampling_required=True,offer__Physical_Status=0).annotate(total_serial_no=Count('id')).distinct('offer__tkc_di')
        # offer_data = offer_data.values_list('tkc_di').distinct('tkc_di')
        wo_data = TKCWoInfo.objects.filter(id=woid,Discom_id=officer.Discom_id)
        
        print("wo_data",wo_data)
        if officer.role.Role_Name == "DGM_STC":
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/sampling/sampling_offerlist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'offer_data':final_data})
        elif officer.role.Role_Name == "DGM_ONM":
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/sampling/sampling_offerlist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'offer_data':final_data})            
    else:
        return redirect(str(curl)+'mpeb_login')






def view_offer_sampling(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer.role.Role_Name == "DGM_STC" or "DGM_ONM":
        offer_no=request.GET.get('offerno')
        tkc_di_id=request.GET.get('tkcdiid')
        print("ofe no---------------",offer_no)
        print("tkc_di_id ---------------",tkc_di_id)

        
        if officer.role.Role_Name =="DGM_STC":
            offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[7,8,9,10],offer_no=offer_no,tkc_di_id=tkc_di_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Approved_Status=1,is_sampling_required=True)
        elif officer.role.Role_Name =="DGM_ONM":
            offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[2,3,4,5,6],offer_no=offer_no,tkc_di_id=tkc_di_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Approved_Status=1,is_sampling_required=True)        
        else:
            offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Approved_Status=1,is_sampling_required=True)
        print("offier-----------",offer_data)
        qun_list = []
        total_qun = []
        item_code_list  = []

        for j in offer_data:
            item_code_list.append(j.wo_material.item_code)
        

        if(len(set(item_code_list))!=len(item_code_list)):
            new_obj = offer_data.distinct('wo_material__item_code')
            for i in new_obj:
                offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,wo_material__item_code =i.wo_material.item_code,Material_Offer_Submit_Approved_Status=1,is_sampling_required=True)
                for k in offer_material:
                    qun_list.append(k.quantity)
                qty_sum = sum(qun_list)
                total_qun.append(qty_sum)
                qun_list.clear()

        else:
            new_obj = offer_data
            for i in offer_data:
                total_qun.append(i.quantity)

        final_data = zip(new_obj,total_qun)

    # for show work order detail    
        wo_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,is_sampling_required=True).first()

    
        if officer.role.Role_Name == "DGM_STC":
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/sampling/item_details.html', {'officer': officer,'base_template_name':base_template_name,'offer_data':final_data,'wo_data':wo_data})
        elif officer.role.Role_Name == "DGM_ONM":
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/sampling/item_details.html', {'officer': officer,'base_template_name':base_template_name,'offer_data':final_data,'wo_data':wo_data})
            
    else:
        return redirect(str(curl)+'mpeb_login')
    






def officer_di_sampling(request,offer_no,tkc_di_id):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer.role.Role_Name == "DGM_STC" or "DGM_ONM":
        # offer_no=request.GET.get('offerno')
        # tkc_di_id=request.GET.get('tkcdiid')
        print("offer no---------------------------",offer_no)
        offer_data1 = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).first()
        if offer_data1.sampling == 1:
            return redirect(request.META.get('HTTP_REFERER'))
        offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True)
        qun_list = []
        total_qun = []
        item_code_list  = []

        for j in offer_data:
            item_code_list.append(j.wo_material.item_code)
        #     print("----------",item_code_list)
        print("fi----------",set(item_code_list))


        offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,wo_material__item_code__in =set(item_code_list),Material_Offer_Submit_Approved_Status=1,is_sampling_required=True).count()
    
        if(len(set(item_code_list))!=len(item_code_list)):
            new_obj = offer_data.distinct('wo_material__item_code')
            for i in new_obj:
                offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,wo_material__item_code =i.wo_material.item_code,Material_Offer_Submit_Approved_Status=1,is_sampling_required=True)
                for k in offer_material:
                    qun_list.append(k.quantity)
                qty_sum = sum(qun_list)
                total_qun.append(qty_sum)
                qun_list.clear()

        else:
            new_obj = offer_data
            for i in offer_data:
                total_qun.append(i.quantity)

        final_data = zip(new_obj,total_qun)
        qun_mt=0
        steel_list=[]
        for i,j in final_data:
            quantity=float(j)
            print("i----------object",i)
            item_code = i.wo_material.item_code
            product_data=product_sampling.objects.filter(item_code=item_code).first()
            # print("product_data--------------------",product_data)
            if product_data is not None and quantity is not None and offer_no is not None and tkc_di_id is not None:
                # print("product_data",product_data.sampling_id)
                product_sampling_info=Sampling_Info.objects.get(id=product_data.sampling_id)
                # print("product_sampling_info",product_sampling_info)
                offer_s=offer_material_serial_number.objects.filter(offer_no=offer_no,wo_material__item_code=item_code,Physical_Status_officer_check=1).first()
                print("icode-----------------",item_code,"os---------",offer_s)

                
                if product_sampling_info.sample_type == 0:
                    print("in if qunatity")
                    if product_sampling_info.name_of_material == "Steel Support/Section":
                        print("insteel section")
                        import re

                        # Input string
                        input_string = product_data.item_code_description
                        print("input_string",input_string)

                        # Regular expression pattern
                        pattern = r"=\s*(.*?)\s*[kK]g"
                        print("pattern",pattern)
                        # Find the matching string
                        match = re.search(pattern, input_string)
                        print("Match",match)
                        if match:
                            # Extract the desired data
                            data = match.group(1)
                            print(float(data))
                            data=float(data)
                            sample_data_s=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=0,Physical_Status=1,Physical_Status_officer_check=1))
                            print("length sample_data",len(sample_data_s))
                            material_name=product_sampling_info.name_of_material
                            P_S_I_steel=Sampling_Info.objects.filter(name_of_material=material_name)
                            qun_mt=qun_mt+(data/1000)*quantity
                            qun_mt=math.ceil(qun_mt)
                            print("qun_mt",qun_mt)
                            steel_list=steel_list+sample_data_s
                            sample_data_s=[]
                            # for i in P_S_I:
                            #     if i.lot_size_min<=qun_mt and i.lot_size_max >= qun_mt:
                            #         sample_unit=i.sample_unit
                            #         print("sample_unit",sample_unit)
                            #         break
                            
                            # for i in range(sample_unit):
                            #     ran=random.randint(0,len(sample_data)-1)
                            #     if sample_data[ran].is_sampled == 0:
                            #         sample_data[ran].is_sampled=1
                            #         sample_data[ran].save()
                            #     else:
                            #         sample_unit=sample_unit+1
                            #     print("sample_data[ran]",sample_data[ran])
                            offer_d=offer_material_site_stores.objects.filter(offer_no=offer_no,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True,wo_material__item_code=item_code)
                            print(len(offer_d))
                            for i in offer_d:
                                i.sampling=1
                                i.save()
                    elif offer_s.serial_no == None:
                        sample_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=0,Physical_Status=1,Physical_Status_officer_check=1))
                        qun=len(sample_data)
                        print("length sample_data",len(sample_data))
                        material_name=product_sampling_info.name_of_material
                        P_S_I=Sampling_Info.objects.filter(name_of_material=material_name)
                        sample_unit = 0
                        for i in P_S_I:
                            if i.lot_size_min<=qun and i.lot_size_max >= qun:
                                sample_unit=i.sample_unit
                                print("sample_unit",sample_unit)
                                break
                        
                        if sample_unit != 0:
                            for i in range(sample_unit):
                                ran=random.randint(0,len(sample_data)-1)
                                if sample_data[ran].is_sampled == 0:
                                    sample_data[ran].is_sampled=1
                                    sample_data[ran].sampled_by = officer
                                    sample_data[ran].sampled_date = datetime.datetime.now()
                                    sample_data[ran].save()
                                else:
                                    sample_unit=sample_unit+1
                                print("sample_data[ran]",sample_data[ran])
                            offer_d=offer_material_site_stores.objects.filter(offer_no=offer_no,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True,wo_material__item_code=item_code)
                            print(len(offer_d))
                            for i in offer_d:
                                i.sampling=1
                                i.save() 
                        else:
                            offer_d=offer_material_site_stores.objects.filter(offer_no=offer_no,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True,tkc_di_id=tkc_di_id)
                            print(len(offer_d))
                            for i in offer_d:
                                i.sampling=0
                                i.save() 
                            message =messages.warning(request, f'Item code Quantity not in sampling range please contact with QC Team')
                            return redirect(request.META.get('HTTP_REFERER'))




                    else:
                        print("###### in if")
                        sample_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=0,Physical_Status=1,Physical_Status_officer_check=1))
                        print("length sample_data",len(sample_data))
                        material_name=product_sampling_info.name_of_material
                        P_S_I=Sampling_Info.objects.filter(name_of_material=material_name)
                        sample_unit = 0
                        for i in P_S_I:
                            if i.lot_size_min<=quantity and i.lot_size_max >= quantity:
                                sample_unit=i.sample_unit
                                print("sample_unit",sample_unit)
                                break
                            

                        if sample_unit != 0:
                            for i in range(sample_unit):
                                ran=random.randint(0,len(sample_data)-1)
                                if sample_data[ran].is_sampled == 0:
                                    sample_data[ran].is_sampled=1
                                    sample_data[ran].sampled_by = officer
                                    sample_data[ran].sampled_date = datetime.datetime.now()
                                    sample_data[ran].save()
                                else:
                                    sample_unit=sample_unit+1
                                print("sample_data[ran]",sample_data[ran])
                            offer_d=offer_material_site_stores.objects.filter(offer_no=offer_no,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True,wo_material__item_code=item_code)
                            print(len(offer_d))
                            for i in offer_d:
                                i.sampling=1
                                i.save() 
                        else:
                            offer_d=offer_material_site_stores.objects.filter(offer_no=offer_no,is_di_created=True,tkc_di_id=tkc_di_id,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True)
                            print(len(offer_d))
                            for i in offer_d:
                                i.sampling=0
                                i.save() 
                            message =messages.warning(request, f'Item code not in sampling range please contact with QC Team')
                            
                            return redirect(request.META.get('HTTP_REFERER'))


                else:
                    sample_data=list(offer_material_serial_number.objects.filter(offer_no=offer_no,wo_material__item_code=item_code,is_sampled=0,Physical_Status_officer_check=1))
                    per=product_sampling_info.sample_percentage
                    sample_unit=(quantity*per)/100
                    sample_unit=int(math.ceil(sample_unit))

                    for i in range(sample_unit):
                        ran=random.randint(0,len(sample_data))
                        if sample_data[ran].is_sampled == 0:
                            sample_data[ran].is_sampled=1
                            sample_data[ran].sampled_by = officer
                            sample_data[ran].sampled_date = datetime.datetime.now()
                            sample_data[ran].save()
                        else:
                            sample_unit=sample_unit+1
                        print("sample_data[ran]",sample_data[ran])
                    offer_d=offer_material_site_stores.objects.filter(offer_no=offer_no,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True,wo_material__item_code=item_code)
                    print(len(offer_d))
                    for i in offer_d:
                        i.sampling=1
                        i.save()
            else:
                offer_d=offer_material_site_stores.objects.filter(offer_no=offer_no,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True)
                print(len(offer_d))
                for i in offer_d:
                    i.sampling=0
                    i.save() 
                message =messages.warning(request, f'Item code not found please contact with QC Team')
                
                return redirect(request.META.get('HTTP_REFERER'))

        if steel_list != []: 
            for i in P_S_I_steel:
                if i.lot_size_min<=qun_mt and i.lot_size_max >= qun_mt:
                    sample_unit=i.sample_unit
                    print("sample_unit",sample_unit)
                    break
            for i in range(sample_unit):
                ran=random.randint(0,len(steel_list)-1)
                if steel_list[ran].is_sampled == 0:
                    steel_list[ran].is_sampled=1
                    steel_list[ran].sampled_by = officer
                    steel_list[ran].sampled_date = datetime.datetime.now()
                    steel_list[ran].save()
                else:
                    sample_unit=sample_unit+1
                print("sample_data[ran]",steel_list[ran])
            print("------------qunmt",qun_mt)
            
        return redirect(request.META.get('HTTP_REFERER'))
            
    else:
        return redirect(str(curl)+'mpeb_login')
    

def officer_sampling_details(request,offer_no,item_code):
    # print("sampling_data",sampling_data)
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()    
    if officer is not None:
        sampling_data=offer_material_serial_number.objects.filter(offer_no=offer_no,wo_material__item_code =item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1)
        if officer.role.Role_Name == "DGM_STC":
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/sampling/sample_details.html', {'officer': officer,'base_template_name':base_template_name,'offer_data':sampling_data})
        elif officer.role.Role_Name == "DGM_ONM":
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/sampling/sample_details.html', {'officer': officer,'base_template_name':base_template_name,'offer_data':sampling_data})
        else:
            return redirect(str(curl)+'mpeb_login')
    else:
        return redirect(str(curl)+'mpeb_login')
        

def officer_sampling_details_di(request,offer_no):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        sampling_data=offer_material_serial_number.objects.filter(offer_no=offer_no,is_sampled=1)
        print("sampling_data",sampling_data)
        if officer.role.Role_Name == "DGM_STC":
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/sampling/sample_details.html', {'officer': officer,'base_template_name':base_template_name,'offer_data':sampling_data})
        elif officer.role.Role_Name == "DGM_ONM":
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/sampling/sample_details.html', {'officer': officer,'base_template_name':base_template_name,'offer_data':sampling_data})
        else:
            return redirect(str(curl)+'mpeb_login')
    else:
        return redirect(str(curl)+'mpeb_login')



def officer_gatepass_trf_wo(request):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        if officer.role.Role_Name == "DGM_STC":
            wo_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[7,8,9,10],site_store_fk__Division__Circle_id=officer.Circle_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,sampling=1).distinct('wo_id').order_by('-wo_id')
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/sampling/gatepass_trf_wo_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})

        elif officer.role.Role_Name == "DGM_ONM":
            wo_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[2,3,4,5,6],site_store_fk__Division__Circle_id=officer.Circle_id,site_store_fk__Division_id=officer.Division_id,is_di_created=True,wo_id__Discom_id=officer.Discom_id,sampling=1,is_sampling_required=True).distinct('wo_id').order_by('-wo_id')
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/sampling/gatepass_trf_wo_list.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data})
        else:
            return redirect(str(curl)+'mpeb_login')
    else:
        return redirect(str(curl)+'mpeb_login')

def officer_gatepass_trf_offerlist(request,woid):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    from decimal import Decimal
    if officer is not None:
        # woid=request.GET.get('woid')
        wo_data = TKCWoInfo.objects.filter(id=woid,Discom_id=officer.Discom_id)
        if officer.role.Role_Name == "DGM_STC":
            offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[7,8,9,10],site_store_fk__Division__Circle_id=officer.Circle_id,wo_id=woid,is_di_created=True,wo_id__Discom_id=officer.Discom_id,sampling=1,is_sampling_required=True).distinct('tkc_di')
            
            base_template_name = "officer/dgm_stc_login.html"
            return render(request, 'fqp/sampling/gatepass_trf_offerlist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'offer_data':offer_data})
        elif officer.role.Role_Name == "DGM_ONM":
            offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[2,3,4,5,6],site_store_fk__Division__Circle_id=officer.Circle_id,site_store_fk__Division_id=officer.Division_id,wo_id=woid,is_di_created=True,wo_id__Discom_id=officer.Discom_id,sampling=1,is_sampling_required=True).distinct('tkc_di')
            base_template_name = "officer/dgm_onm_login.html"
            return render(request, 'fqp/sampling/gatepass_trf_offerlist.html', {'officer': officer,'base_template_name':base_template_name,'wo_data':wo_data,'offer_data':offer_data})            
        else:
            # offer_data = offer_material_site_stores.objects.filter(wo_id=woid,is_di_created=True,wo_id__Discom_id=officer.Discom_id,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True).distinct('tkc_di')
            return redirect(str(curl)+'mpeb_login')
    else:
        return redirect(str(curl)+'mpeb_login')


def officer_view_gatepasslist(request,tkc_di_id,wo_id,offer_no):
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    wo_data = TKCWoInfo.objects.filter(id=wo_id,Discom_id=officer.Discom_id)
    if officer is not None and officer.role.Role_Name == "DGM_STC":
        base_template_name = "officer/dgm_stc_login.html"
        offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[7,8,9,10],site_store_fk__Division__Circle_id=officer.Circle_id,wo_id=wo_id,offer_no=offer_no,tkc_di_id=tkc_di_id,nabl_status=1,sampling=1,site_store_gatepass=1)
        gate_pass_data=offer_material_serial_number.objects.filter(offer_id__in=offer_data).exclude(site_store_gatepass_id__isnull = True).distinct('site_store_gatepass_id')        
        print("-gpd-------------",gate_pass_data)
        return render(request, 'fqp/sampling/site_store_gatepass_list.html', {'officer': officer,'offer_data': offer_data,'wo_data':wo_data,'gate_pass_data':gate_pass_data,'base_template_name':base_template_name})
    elif officer is not None and officer.role.Role_Name == "DGM_ONM":
        base_template_name = "officer/dgm_onm_login.html"
        offer_data = offer_material_site_stores.objects.filter(wo__pakage_id__in=[2,3,4,5,6],site_store_fk__Division__Circle_id=officer.Circle_id,site_store_fk__Division_id=officer.Division_id,offer_no=offer_no,tkc_di_id=tkc_di_id,nabl_status=1,sampling=1,site_store_gatepass=1).distinct('nabl_name')    
        gate_pass_data=offer_material_serial_number.objects.filter(offer_id__in=offer_data).exclude(site_store_gatepass_id__isnull = True).distinct('site_store_gatepass_id')
        return render(request, 'fqp/sampling/site_store_gatepass_list.html', {'officer': officer,'offer_data': offer_data,'wo_data':wo_data,'gate_pass_data':gate_pass_data,'base_template_name':base_template_name})
    else:
        # offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,nabl_status=1,sampling=1,site_store_gatepass=1).distinct('nabl_name')
        return redirect(str(curl)+'mpeb_login')

def officer_create_wo_offer_trf(request,tkc_di_id,site_store_gatepass_id,offer_no):
    
    officer = Officer.objects.filter(is_active=True,otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).first()
    if officer is not None:
        # offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,nabl_status=1,site_store_gatepass=1).first()
        # material = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,nabl_status=1,site_store_gatepass=1)
        # serial_no = offer_material_serial_number.objects.filter(offer__in = material,is_sampled=1)
        if request.method == "POST":
            # material = offer_material_site_stores.objects.filter(offer_no=offer_no).last()
            customer_Organization_name = request.POST.get('customer_Organization_name')
            customer_Organization_address = request.POST.get('customer_Organization_address')
            contact_person_name = request.POST.get('contact_person_name')
            contact_person_designation = request.POST.get('contact_person_designation')
            mobile_no = request.POST.get('mobile_no')
            email_id = request.POST.get('email_id')
            name_of_sample_product = request.POST.get('name_of_sample_product')
            customer_ref_gatepass_no = request.POST.get('customer_ref_gatepass_no')
            dated = request.POST.get('dated')

            tkc_diid = request.POST.get('tkc_diid')
            offerno = request.POST.get('offerno')
            # nabl_number = request.POST.get('nabl_number')
            nabl_user_id = request.POST.get('nabl_user_id')
            site_store_gatepass_id = request.POST.get('site_store_gatepass_id')
            serial_no_id = request.POST.getlist('serial_no_id[]')
            offer_id = request.POST.getlist('offer_id[]')
            
            if request.FILES['trf_file' or None]:
                trf_file = request.FILES['trf_file'] 

            trf_obj = Tkc_Work_Order_Trf_Details(offer_no=offerno,tkc_di_id = tkc_diid,TRFAreastore_file=trf_file,
                                customer_Organization_name=customer_Organization_name, 
                                customer_Organization_address=customer_Organization_address,
                                contact_person_name=contact_person_name,
                                contact_person_designation=contact_person_designation, 
                                mobile_no=mobile_no, email_id=email_id, 
                                name_of_sample_product=name_of_sample_product, 
                                customer_ref_gatepass_no=customer_ref_gatepass_no, 
                                dated=dated,  trf_generated = 1,nabl_user_id=nabl_user_id,site_store_gatepass_id=site_store_gatepass_id)

            trf_obj.save()
            if trf_obj is not None:
                trf_data=offer_material_serial_number.objects.filter(site_store_gatepass_id=site_store_gatepass_id,offer_no=offer_no)
                for i in trf_data:
                    i.site_store_trf_id=trf_obj.TRF_Id
                    i.save()
                offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,site_store_fk__Division__Circle_id=officer.Circle_id,site_store_gatepass=1).update(trf_status=1,send_to_nabl=1)
            # print("trf obj-------------",trf_obj)
            #     for i in gate_pass_data:
            #         print("gpd----i---------",i)
            #         offer_material_serial_number.objects.filter(id=i.serial_no_id, offer_id = i.offer_id, tkc_di_id=i.tkc_di_id).update(trf_created_status=True)
            #         offer_material_site_stores.objects.filter(id=i.offer_id,tkc_di_id=i.tkc_di_id,offer_no=offer_no).update(trf_status=1)
            #         tkc_wo_nabl_gatepass_detail.objects.filter(id=i.id,offer_id = i.offer_id,tkc_di_id=i.tkc_di_id).update(wo_trf_id=gatepass.id)
            # return redirect(request.META.get('HTTP_REFERER'))
            return redirect(officer_gatepass_trf_wo)
        else:            
            if officer is not None and officer.role.Role_Name == "DGM_STC":
                base_template_name = "officer/dgm_stc_login.html"                
                gate_pass_data = tkc_wo_nabl_gatepass.objects.filter(id=site_store_gatepass_id,offer_no=offer_no,tkc_di_id=tkc_di_id,site_store__Division__Circle_id=officer.Circle_id)                
                serial_data=offer_material_serial_number.objects.filter(site_store_gatepass_id__in=gate_pass_data,offer__site_store_gatepass=1,offer__wo__pakage_id__in=[7,8,9,10]).exclude(site_store_gatepass_id__isnull = True)
                return render(request, 'fqp/sampling/wo_test_request_form.html',{'officer': officer,'serial_data':serial_data,'gate_pass_data':gate_pass_data,'base_template_name':base_template_name})
            elif officer is not None and officer.role.Role_Name == "DGM_ONM":
                base_template_name = "officer/dgm_onm_login.html"
                gate_pass_data = tkc_wo_nabl_gatepass.objects.filter(id=site_store_gatepass_id,offer_no=offer_no,tkc_di_id=tkc_di_id,site_store__Division__Circle_id=officer.Circle_id,site_store__Division_id=officer.Division_id)
                serial_data=offer_material_serial_number.objects.filter(site_store_gatepass_id__in=gate_pass_data,offer__site_store_gatepass=1,offer__wo__pakage_id__in=[2,3,4,5,6]).exclude(site_store_gatepass_id__isnull = True)
                return render(request, 'fqp/sampling/wo_test_request_form.html',{'officer': officer,'serial_data':serial_data,'gate_pass_data':gate_pass_data,'base_template_name':base_template_name})


            # offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,nabl_status=1,site_store_gatepass=1)
            # serial_no = offer_material_serial_number.objects.filter(offer__in = offer_data,is_sampled=1)
            # return render(request, 'fqp/sampling/wo_test_request_form.html',{'material': material,'offer_data':offer_data,'gate_pass_data':gate_pass_data,'gatepass_detail_data':gatepass_detail_data})

# <------------------------------------  Lokesh Code starts from here  --------------------------->

# <-------Lokesh 12-08-2023------->




# run this function to show the invoice list to pick invoice 
def tkc_show_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        # if request.method == "POST" and officer.role.Role_Name == "WO_APPROVER":
        wo_id=request.GET.get('woid')
        
        print("SSSSSSSSSSSSSSSSSSS",wo_id)
        # inv_data = Invoice.objects.filter(work_order = wo_id).last()
        # print("INCCCVVVVVVVVV",inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++DATATAAAAAAAAAAAa",wo_data)
        inv_data = Invoice.objects.filter(~Q(invoicetype_id__in=[1,3,4,5]),work_order = wo_id)   #add this filter in Invoice searching
        print("NNNNNNNNNNNNNNNNNNNNNNNN", inv_data)
        # ofc_name = officer.employ_name
        print("Oficer Name", officer.employ_name)
        return render(request,'fqp/wo_invoice/tkc_show_current_invoice_list.html',{'invce_data':inv_data,'wo_data':wo_data,'officer':officer})

            # if int(status) == 1:
            #     Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=3,assign_officer_id=officer_id)
            #     return redirect(wo_officer_invoice_list)
            # else:
            #     Invoice.objects.filter(work_order_id=wo_id,id=invoice_id).update(status=status,rejected_by_officer=officer.employ_name,rejected_by_role=officer.role.Role_Name)
            #     return redirect(wo_officer_invoice_list)
        # else:
        #     order_type=request.GET.get('ordertype')
        #     wo_id=request.GET.get('woid')
        #     wo_data=TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id,Discom_id=officer.Discom_id).last()
        #     ofdata=Officer.objects.filter(role__Role_Name=("WO_CREATER"),Discom_id=wo_data.Discom_id)
        #     wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
        #     in_data = Invoice.objects.filter(~Q(status=-1),work_order_id=wo_id,order_type = order_type).order_by('-id')
        #     in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,work_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
        #     return render(request, 'fqp/wo_invoice/tkc_show_current_invoice_list.html', {"officer":officer,"ofdata":ofdata,'wo_data':wo_data,"in_data":in_data,'in_amount':in_amount,'wo_amt':wo_amt})
    else:
        return redirect(str(curl)+'mpeb_login')


def tkc_gm_circle_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        invoice_id=request.GET.get('invoice_id')
        print("AAAAAAAAAAAAAAAAAAAAAA", invoice_id)
        print("SSSSSSSSSSSSSSSSSSS",wo_id)
        # inv_data = Invoice.objects.filter(id=invoice_id).last()    #try to get by invoice id
        inv_data = Invoice.objects.filter(work_order = wo_id, id=invoice_id).last()
        
        print("INCCCVVVVVVVVV",inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++DATATAAAAAAAAAAAa",wo_data)
        invc_data = Invoice.objects.filter(~Q(invoicetype_id__in=[1,3,4,5]))
        print("NNNNNNNNNNNNNNNNNNNNNNNN", invc_data)
        # ofc_name = officer.employ_name
        print("Oficer Name", officer.employ_name)
        try:
            circle_wo = Circle_Master.objects.filter(id = inv_data.circle.id).last()
            print("CCCCCCCCCCCCCCCCCCC",circle_wo)
        except Exception as e:
            pass
        
        # try:
        #     officer_lov = Officer.objects.filter(Circle = circle_wo)
        #     print("OOFOFOFOFF",officer_lov)
        # except Exception as e:
        #     pass
        # invoice_data = Invoice.objects.filter(work_order = wo_id).last()
        # if request.method == "POST" and officer.role.Role_Name == "GM(CIRCLE)":
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            invoice_id2=request.GET.get('invoice_id1')
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            print("wwwwooooooidd111",wo_id2)
            print("VVVVVVVVVVVVVVVVVVV",invoice_data)
            officer_select_by_gm_circle = request.POST.get('officer_select_by_gm_circle')
            gm_circle_remark = request.POST.get('gm_circle_remark')
            doc_name_gm_circle = request.POST.get('doc_name_gm_circle')
            gm_circle_submit_status = request.POST.get('gm_circle_submit_status')
            dgm_circle_submit_status = request.POST.get('dgm_circle_submit_status')
            gm_circle_submit_name=request.POST.get('gm_circle_submit_name')
            gm_circle_remark_sec = request.POST.get('gm_circle_remark_sec')
            doc_name_gm_circle_sec = request.POST.get('doc_name_gm_circle_sec')
            today_date=datetime.datetime.now()
            print("$$$$$$$$$$$$$$$$$$$", gm_circle_submit_name)
            print("FFFFFFFFFFFF",request.FILES)
            if int(gm_circle_submit_status) == 1 and int(dgm_circle_submit_status) == 0 :
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(officer_select_by_gm_circle_id = officer_select_by_gm_circle,
                                                                                                gm_circle_remark=gm_circle_remark,
                                                                                                 
                                                                                                doc_name_gm_circle=doc_name_gm_circle,
                                                                                                gm_circle_submit_name=gm_circle_submit_name,
                                                                                                gm_circle_submit_status = gm_circle_submit_status,
                                                                                                gm_circle_action=today_date)
                
                    
                
            elif int(gm_circle_submit_status) == 1 and int(dgm_circle_submit_status) == 1:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(officer_select_by_gm_circle_id = officer_select_by_gm_circle,
                                                                                                gm_circle_remark_sec=gm_circle_remark_sec,
                                                 
                                                                                                doc_name_gm_circle_sec=doc_name_gm_circle_sec,
                                                                                                gm_circle_submit_status = 3,
                                                                                                gm_circle_action_sec=today_date)
            else:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(officer_select_by_gm_circle_id = officer_select_by_gm_circle,
                                                                                                gm_circle_remark=gm_circle_remark,
                                                                                                 
                                                                                                doc_name_gm_circle=doc_name_gm_circle,
                                                                                                gm_circle_submit_status = 2,
                                                                                                gm_circle_action=today_date)
            try:
                if 'doc_by_gm_circle' in request.FILES:
                    print("#####################intry")
                    inv_data3=Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).first()
                    doc_by_gm_circle = request.FILES['doc_by_gm_circle']
                    inv_data3.doc_by_gm_circle = doc_by_gm_circle
                    inv_data3.save()
                    print("----------------------",inv_data3.id)
                    # in_history=InvoiceHistory(invoice_id=inv_data2.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=cfo_remark,invoice_document=cfo_document,action=cfo_status).save()
                
                elif 'doc_by_gm_circle_sec' in request.FILES:
                    print("#####################intry")
                    inv_data3=Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).first()
                    doc_by_gm_circle_sec = request.FILES['doc_by_gm_circle_sec']
                    inv_data3.doc_by_gm_circle_sec = doc_by_gm_circle_sec
                    inv_data3.save()
                    print("----------------------",inv_data3.id)

                else:
                    pass
                    # in_history=InvoiceHistory(invoice_id=inv_data2.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=cfo_remark,action=cfo_status).save()                    
            except Exception as e:
                print(e)
                pass
            return redirect(tkc_show_current_invoice_list)
        
            # print("SSSSSSSSSSSSSSSS$$$$$$$$$",inv_data2)
            # return render(request,'fqp/wo_invoice/tkc_show_current_invoice_list.html')

        officer_lov = None 
        try:
            officer_lov = Officer.objects.filter(Circle = circle_wo)
            print("OOFOFOFOFF",officer_lov)
        except Exception as e:
            pass

        # return HttpResponse("amana")
        return render(request,'fqp/wo_invoice/tkc_gm_circle_current_invoice_list.html',{'invce_data':inv_data,'wo_data':wo_data,'officer_lov':officer_lov,'wo_id':wo_id,'officer':officer})

    

def tkc_dgm_circle_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        invoice_id=request.GET.get('invoice_id')     # sending id is remained
        print("tkc_dgm_circle_current_invoice_list",wo_id)
        print("AAAAAAAAAAAAAAAAAAAAAA", invoice_id)
        inv_data = Invoice.objects.filter(work_order = wo_id, id=invoice_id).last()
        print("tkc_dgm_circle_current_invoice_list",inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++tkc_dgm_circle_current_invoice_list",wo_data)

        try:
            circle_wo = Circle_Master.objects.filter(id = inv_data.circle.id).last()
            print("CCCCCCCCCCCCCCCCCCC",circle_wo)
        except Exception as e:
            pass
        
        
        # invoice_data = Invoice.objects.filter(work_order = wo_id).last()
        # if request.method == "POST" and officer.role.Role_Name == "DGM_STC" and officer.role.Role_Name == "DGM_ONM":
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            invoice_id2=request.GET.get('invoice_id1')
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            print("wwwwooooooidd111",wo_id2)
            officer_select_by_dgm_circle = request.POST.get('officer_select_by_dgm_circle')
            dgm_circle_remark = request.POST.get('dgm_circle_remark')
            doc_by_dgm_circle = request.FILES['doc_by_dgm_circle']
            doc_name_dgm_circle = request.POST.get('doc_name_dgm_circle')
            dgm_circle_submit_status = request.POST.get('dgm_circle_submit_status')
            gm_circle_submit_status = request.POST.get('gm_circle_submit_status')
            today_date=datetime.datetime.now()

            if int(gm_circle_submit_status) == 1 and int(dgm_circle_submit_status) == 1 :
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(officer_select_by_dgm_circle_id = officer_select_by_dgm_circle,
                                                                                                dgm_circle_remark=dgm_circle_remark,
                                                                                                 
                                                                                                doc_name_dgm_circle=doc_name_dgm_circle,
                                                                                                dgm_circle_submit_status = dgm_circle_submit_status,
                                                                                                dgm_circle_action=today_date)
            else:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(officer_select_by_dgm_circle_id = officer_select_by_dgm_circle,
                                                                                                dgm_circle_remark=dgm_circle_remark,
                                                                                                 
                                                                                                doc_name_dgm_circle=doc_name_dgm_circle,
                                                                                                dgm_circle_submit_status = 2,
                                                                                                dgm_circle_action=today_date)
            try:
                if 'doc_by_dgm_circle' in request.FILES:
                    print("#####################intry")
                    inv_data3=Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).first()
                    doc_by_dgm_circle = request.FILES['doc_by_dgm_circle']
                    inv_data3.doc_by_dgm_circle = doc_by_dgm_circle
                    inv_data3.save()
                    print("----------------------",inv_data3.id)
                    # in_history=InvoiceHistory(invoice_id=inv_data2.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=cfo_remark,invoice_document=cfo_document,action=cfo_status).save()
                else:
                    pass
                    # in_history=InvoiceHistory(invoice_id=inv_data2.id,officer_id=officer.employ_id,role=officer.role.Role_Name,invoice_remark=cfo_remark,action=cfo_status).save()                    
            except Exception as e:
                pass
            return redirect(tkc_show_current_invoice_list)
            # print("SSSSSSSSSSSSSSSS$$$$$$$$$",inv_data2)
            # return render(request,'fqp/wo_invoice/tkc_show_current_invoice_list.html')

    
        officer_lov = None 
        try:
            officer_lov = Officer.objects.filter(Circle = circle_wo)
            print("OOFOFOFOFF",officer_lov)
        except Exception as e:
            pass
        # return HttpResponse("amana")
        return render(request,'fqp/wo_invoice/tkc_dgm_circle_current_invoice_list.html',{'invce_data':inv_data,'wo_data':wo_data,'officer_lov':officer_lov,'wo_id':wo_id,'officer':officer})




def tkc_cgmproject_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        print("SSSSSSSSSSSSSSSSSSS",wo_id)
        invoice_id2=request.GET.get('invoice_id')
        inv_data = Invoice.objects.filter(work_order = wo_id,id=invoice_id2).last()
        # inv_data = Invoice.objects.filter(work_order = wo_id).last()
        print("INCCCVVVVVVVVV",inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++DATATAAAAAAAAAAAa",wo_data)

        try:
            circle_wo = Circle_Master.objects.filter(id = inv_data.circle.id).last()
            print("CCCCCCCCCCCCCCCCCCC",circle_wo)
        except Exception as e:
            pass
        
        
        # invoice_data = Invoice.objects.filter(work_order = wo_id).last()
        # if request.method == "POST" and officer.role.Role_Name == "CFO":
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            invoice_id2=request.GET.get('invoice_id1')
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            # invoice_data = Invoice.objects.filter(work_order = wo_id2).last()
            print("wwwwooooooidd111",wo_id2)
            
            officer_select_by_cgmproject = request.POST.get('officer_select_by_cgmproject')
            cgmproject_remark = request.POST.get('cgmproject_remark')
            doc_by_cgmproject = request.FILES['doc_by_cgmproject']
            doc_name_cgmproject = request.POST.get('doc_name_cgmproject')
            cgmproject_submit_status = request.POST.get('cgmproject_submit_status')
            # today_date=datetime.datetime.now()
            inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(officer_select_by_cgmproject_id = officer_select_by_cgmproject,
                                                                                                cgmproject_remark=cgmproject_remark,
                                                                                                doc_by_cgmproject = doc_by_cgmproject, 
                                                                                                doc_name_cgmproject=doc_name_cgmproject,
                                                                                                cgmproject_submit_status = cgmproject_submit_status)

            print("SSSSSSSSSSSSSSSS$$$$$$$$$",inv_data2)
            return render(request,'fqp/wo_invoice/tkc_cgmproject_current_invoice_list.html')

        
        officer_lov = None 
        try:
            officer_lov = Officer.objects.filter(Circle = circle_wo)
            print("OOFOFOFOFF",officer_lov)
        except Exception as e:
            pass
        # return HttpResponse("amana")
        return render(request,'fqp/wo_invoice/tkc_cgmproject_current_invoice_list.html',{'invce_data':inv_data,'wo_data':wo_data,'officer_lov':officer_lov,'wo_id':wo_id,'officer':officer})


# <------- Lokesh 01-08-23 ------->
def tkc_dgmproject_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        print(wo_id)
        invoice_id2=request.GET.get('invoice_id')
        inv_data = Invoice.objects.filter(work_order = wo_id,id=invoice_id2).last()
        print("0000888880000",inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++DATATAAAAAAAAAAAa",wo_data)

        try:
            circle_wo = Circle_Master.objects.filter(id = inv_data.circle.id).last()
            print("CCCCCCCCCCCCCCCCCCC",circle_wo)
        except Exception as e:
            pass
        
        
        # if request.method == "POST" and officer.role.Role_Name == "DGM_STC" and officer.role.Role_Name == "DGM_ONM":
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            invoice_id2=request.GET.get('invoice_id1')
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            print("999999999", wo_id2)
            dgmproject_remark = request.POST.get('dgmproject_remark')
            doc_by_dgmproject = request.FILES['doc_by_dgmproject']
            doc_name_dgmproject = request.POST.get('doc_name_dgmproject')
            dgmproject_submit_status = request.POST.get('dgmproject_submit_status')
            cgmproject_submit_status = request.POST.get('cgmproject_submit_status')
            # today_date=datetime.datetime.now()
            print("BBBBBBBBBFFFFFFFFFFFFFFFFF",dgmproject_submit_status)
            print("wwwwwwwwwwwwwwwwwwwwwwwwww",cgmproject_submit_status)
            if int(dgmproject_submit_status) == 1 and int(cgmproject_submit_status) == 1:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(dgmproject_remark=dgmproject_remark,
                                                                                                doc_by_dgmproject = doc_by_dgmproject, 
                                                                                                doc_name_dgmproject=doc_name_dgmproject,
                                                                                                dgmproject_submit_status = dgmproject_submit_status)
            else:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(dgmproject_remark=dgmproject_remark,
                                                                                                dgmproject_submit_status = 2,
                                                                                                doc_by_dgmproject = doc_by_dgmproject, 
                                                                                                doc_name_dgmproject=doc_name_dgmproject)

        
            print("lllllllllll", inv_data2)
            return render(request,'fqp/wo_invoice/tkc_dgmproject_current_invoice_list.html')
            
        officer_lov = None 
        try:
            officer_lov = Officer.objects.filter(Circle = circle_wo)
            print("OOFOFOFOFF",officer_lov)
        except Exception as e:
            pass
        return render(request,'fqp/wo_invoice/tkc_dgmproject_current_invoice_list.html', {'invce_data':inv_data, 'wo_data':wo_data,'officer':officer})






# <------- Lk 02-08-23 ------->
def tkc_cfoproject_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        print("SSSSSSSSSSSSSSSSSSS",wo_id)
        invoice_id=request.GET.get('invoice_id')
        print("AAAAAAAAAAAAAAAAAAAAAA", invoice_id)
        inv_data = Invoice.objects.filter(work_order = wo_id, id=invoice_id).last()
        # inv_data = Invoice.objects.filter(work_order = wo_id).last()
        print("INCCCVVVVVVVVV",inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++DATATAAAAAAAAAAAa",wo_data)

        try:
            circle_wo = Circle_Master.objects.filter(id = inv_data.circle.id).last()
            print("CCCCCCCCCCCCCCCCCCC",circle_wo)
        except Exception as e:
            pass
        
        
        # if request.method == "POST" and officer.role.Role_Name == "DGM_STC" and officer.role.Role_Name == "DGM_ONM":
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            print("999999999", wo_id2)
            invoice_id2=request.GET.get('invoice_id1')
            print("UUUUUUUUUUUUUU",invoice_id2)
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            cfoproject_remark = request.POST.get('cfoproject_remark')
            officer_select_by_cfoproject = request.POST.get('officer_select_by_cfoproject')
            cfoproject_submit_status = request.POST.get('cfoproject_submit_status')
            gm_circle_submit_status = request.POST.get('gm_circle_submit_status')
            dgm_circle_submit_status = request.POST.get('dgm_circle_submit_status')
            cfoproject_submit_name = request.POST.get('cfoproject_submit_name')
            
            today_date=datetime.datetime.now()        

            if int(gm_circle_submit_status) == 3 and int(dgm_circle_submit_status) == 1:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(cfoproject_remark=cfoproject_remark,
                                                                                                officer_select_by_cfoproject_id = officer_select_by_cfoproject,
                                                                                                cfoproject_submit_status = cfoproject_submit_status,
                                                                                                cfoproject_submit_name=cfoproject_submit_name,
                                                                                                cfoproject_action=today_date)
            else:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(cfoproject_remark=cfoproject_remark,
                                                                                                officer_select_by_cfoproject_id = officer_select_by_cfoproject,
                                                                                                cfoproject_submit_name=cfoproject_submit_name,
                                                                                                cfoproject_submit_status = 2,
                                                                                                cfoproject_action=today_date)
        
            # print("lllllllllll", inv_data2)
            # return render(request,'fqp/wo_invoice/tkc_dgmproject_current_invoice_list.html')
            return redirect(tkc_show_current_invoice_list)
        officer_lov = None 
        try:
            officer_lov = Officer.objects.filter(Circle = circle_wo)
            print("OOFOFOFOFF",officer_lov)
        except Exception as e:
            pass
        
        return render(request,'fqp/wo_invoice/tkc_cfoproject_current_invoice_list.html', {'invce_data':inv_data,'wo_data':wo_data,'officer_lov':officer_lov,'officer':officer})




    
# <------- Lk 03-08-23 ------->
def tkc_dgmcbpu_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        print("SSSSSSSSSSSSSSSSSSS",wo_id)
        invoice_id=request.GET.get('invoice_id')
        print("AAAAAAAAAAAAAAAAAAAAAA", invoice_id)
        inv_data = Invoice.objects.filter(work_order = wo_id, id=invoice_id).last()
        # inv_data = Invoice.objects.filter(work_order = wo_id).last()
        print("INCCCVVVVVVVVV",inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++DATATAAAAAAAAAAAa",wo_data)

        try:
            circle_wo = Circle_Master.objects.filter(id = inv_data.circle.id).last()
            print("CCCCCCCCCCCCCCCCCCC",circle_wo)
        except Exception as e:
            pass
        
        # try:
        #     officer_lov = Officer.objects.filter(Circle = circle_wo)
        #     print("OOFOFOFOFF",officer_lov)
        # except Exception as e:
        #     pass

        # officer_lov = Officer.objects.filter(officer.role.Role_Name == "CFO")
        
        # if request.method == "POST" and officer.role.Role_Name == "DGM_CBPU":                                  
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            invoice_id2=request.GET.get('invoice_id1')
            print("UUUUUUUUUUUUUU",invoice_id2)
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            # invoice_data = Invoice.objects.filter(work_order = wo_id2).last()
            print("999999999", wo_id2)
            dgmcbpu_remark = request.POST.get('dgmcbpu_remark')
            officer_select_by_dgmcbpu = request.POST.get('officer_select_by_dgmcbpu')
            dgmcbpu_submit_status = request.POST.get('dgmcbpu_submit_status')
            today_date=datetime.datetime.now()
            # cfoproject_submit_status = request.POST.get('cfoproject_submit_status')
            # dgmproject_submit_status = request.POST.get('dgmproject_submit_status')
            # cgmproject_submit_status = request.POST.get('cgmproject_submit_status')
            # print("HHHHHHHHHHHHHHHHHHHHHHHHHH",dgmcbpu_submit_status)
            # print("rrrrrrrrrrrrrrrrrrrrrrrrrr",cfoproject_submit_status)
            # print("BBBBBBBBBFFFFFFFFFFFFFFFFF",dgmproject_submit_status)
            # print("wwwwwwwwwwwwwwwwwwwwwwwwww",cgmproject_submit_status)

            if int(dgmcbpu_submit_status) == 1 : 
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(dgmcbpu_remark=dgmcbpu_remark,
                                                                                                officer_select_by_dgmcbpu_id = officer_select_by_dgmcbpu,
                                                                                                dgmcbpu_submit_status=dgmcbpu_submit_status,
                                                                                                dgmcbpu_action=today_date)
            else:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(dgmcbpu_remark=dgmcbpu_remark,
                                                                                                officer_select_by_dgmcbpu_id = officer_select_by_dgmcbpu,
                                                                                                dgmcbpu_submit_status=2,
                                                                                                dgmcbpu_action=today_date)   
        
            # print("lllllllllll", inv_data2)
            # return render(request,'fqp/wo_invoice/tkc_dgmcbpu_current_invoice_list.html')
            return redirect(tkc_show_current_invoice_list)

        officer_lov = None 
        try:
            officer_lov = Officer.objects.filter(Circle = circle_wo)
            print("OOFOFOFOFF",officer_lov)
        except Exception as e:
            pass
        return render(request,'fqp/wo_invoice/tkc_dgmcbpu_current_invoice_list.html', {'invce_data':inv_data, 
                                                                                        'wo_data':wo_data,
                                                                                        'officer_lov':officer_lov,
                                                                                        'officer':officer})



# <------- Lk 03-08-23 ------->
def tkc_aocbpu_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        print(wo_id)
        invoice_id=request.GET.get('invoice_id')
        print("AAAAAAAAAAAAAAAAAAAAAA", invoice_id)
        inv_data = Invoice.objects.filter(work_order = wo_id, id=invoice_id).last()
        # inv_data = Invoice.objects.filter(work_order = wo_id).last()
        print(inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("wo++++++++DATATAAAAAAAAAAAa",wo_data)

        # if request.method == "POST" and officer.role.Role_Name == "AO_BILLS":
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            invoice_id2=request.GET.get('invoice_id1')
            print("UUUUUUUUUUUUUU",invoice_id2)
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            # invoice_data = Invoice.objects.filter(work_order = wo_id2).last()
            print("999999999", wo_id2)
            aocbpu_erp_voucher_number = request.POST.get('aocbpu_erp_voucher_number')
            aocbpu_invoice_verfiy_amount = request.POST.get('aocbpu_invoice_verfiy_amount')
            aocbpu_invoice_cgst_amount = request.POST.get('aocbpu_invoice_cgst_amount')
            aocbpu_invoice_sgst_amount = request.POST.get('aocbpu_invoice_sgst_amount')
            aocbpu_invoice_igst_amount = request.POST.get('aocbpu_invoice_igst_amount')
            aocbpu_labour_welfare_cess = request.POST.get('aocbpu_labour_welfare_cess')
            aocbpu_liquidity_damage_amount = request.POST.get('aocbpu_liquidity_damage_amount')
            aocbpu_mob_adv_recovery_amount = request.POST.get('aocbpu_mob_adv_recovery_amount')
            aocbpu_material_adv_recovery_amount = request.POST.get('aocbpu_material_adv_recovery_amount')
            aocbpu_recovery_of_intrest_on_advanced = request.POST.get('aocbpu_recovery_of_intrest_on_advanced')
            aocbpu_retention_amount = request.POST.get('aocbpu_retention_amount')
            aocbpu_other_recovery_amount = request.POST.get('aocbpu_other_recovery_amount')
            aocbpu_miscelleneous_recovery_amount = request.POST.get('aocbpu_miscelleneous_recovery_amount')
            aocbpu_final_net_payable_amount = request.POST.get('aocbpu_final_net_payable_amount')
            aocbpu_remark = request.POST.get('aocbpu_remark')
            aocbpu_submit_status = request.POST.get('aocbpu_submit_status')
            gm_circle_submit_status = request.POST.get('gm_circle_submit_status')
            today_date=datetime.datetime.now()
            print("HHHHHHHHHHHHHHHHHHHHHHHHHH",gm_circle_submit_status)
            # print("rrrrrrrrrrrrrrrrrrrrrrrrrr",cfoproject_submit_status)
            # print("BBBBBBBBBFFFFFFFFFFFFFFFFF",dgmproject_submit_status)
            # print("wwwwwwwwwwwwwwwwwwwwwwwwww",cgmproject_submit_status)
            # if int(gm_circle_submit_status) == 1 and int(dgm_circle_submit_status) == 1 and int(cgmproject_submit_status) == 1 and int(dgmproject_submit_status) == 1:
            if int(aocbpu_submit_status) == 1: 
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(aocbpu_erp_voucher_number=aocbpu_erp_voucher_number,
                                                                                                aocbpu_invoice_verfiy_amount = aocbpu_invoice_verfiy_amount,
                                                                                                aocbpu_invoice_cgst_amount=aocbpu_invoice_cgst_amount,
                                                                                                aocbpu_invoice_sgst_amount=aocbpu_invoice_sgst_amount,
                                                                                                aocbpu_invoice_igst_amount=aocbpu_invoice_igst_amount,
                                                                                                aocbpu_labour_welfare_cess=aocbpu_labour_welfare_cess,
                                                                                                aocbpu_liquidity_damage_amount=aocbpu_liquidity_damage_amount,
                                                                                                aocbpu_mob_adv_recovery_amount=aocbpu_mob_adv_recovery_amount,
                                                                                                aocbpu_material_adv_recovery_amount=aocbpu_material_adv_recovery_amount,
                                                                                                aocbpu_recovery_of_intrest_on_advanced=aocbpu_recovery_of_intrest_on_advanced,
                                                                                                aocbpu_retention_amount=aocbpu_retention_amount,
                                                                                                aocbpu_other_recovery_amount=aocbpu_other_recovery_amount,
                                                                                                aocbpu_miscelleneous_recovery_amount=aocbpu_miscelleneous_recovery_amount,
                                                                                                aocbpu_final_net_payable_amount=aocbpu_final_net_payable_amount,
                                                                                                aocbpu_remark=aocbpu_remark,
                                                                                                aocbpu_submit_status=aocbpu_submit_status,
                                                                                                aocbpu_action=today_date)
            else:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(aocbpu_erp_voucher_number=aocbpu_erp_voucher_number,
                                                                                                aocbpu_invoice_verfiy_amount = aocbpu_invoice_verfiy_amount,
                                                                                                aocbpu_invoice_cgst_amount=aocbpu_invoice_cgst_amount,
                                                                                                aocbpu_invoice_sgst_amount=aocbpu_invoice_sgst_amount,
                                                                                                aocbpu_invoice_igst_amount=aocbpu_invoice_igst_amount,
                                                                                                aocbpu_labour_welfare_cess=aocbpu_labour_welfare_cess,
                                                                                                aocbpu_liquidity_damage_amount=aocbpu_liquidity_damage_amount,
                                                                                                aocbpu_mob_adv_recovery_amount=aocbpu_mob_adv_recovery_amount,
                                                                                                aocbpu_material_adv_recovery_amount=aocbpu_material_adv_recovery_amount,
                                                                                                aocbpu_recovery_of_intrest_on_advanced=aocbpu_recovery_of_intrest_on_advanced,
                                                                                                aocbpu_retention_amount=aocbpu_retention_amount,
                                                                                                aocbpu_other_recovery_amount=aocbpu_other_recovery_amount,
                                                                                                aocbpu_miscelleneous_recovery_amount=aocbpu_miscelleneous_recovery_amount,
                                                                                                aocbpu_final_net_payable_amount=aocbpu_final_net_payable_amount,
                                                                                                aocbpu_remark=aocbpu_remark,
                                                                                                aocbpu_submit_status=2,
                                                                                                aocbpu_action=today_date)
            
            # print("lllllllllll", inv_data2)
            # return render(request,'fqp/wo_invoice/tkc_aocbpu_current_invoice_list.html')
            return redirect(tkc_show_current_invoice_list)   

        return render(request,'fqp/wo_invoice/tkc_aocbpu_current_invoice_list.html', {'invce_data':inv_data, 
                                                                                        'wo_data':wo_data,
                                                                                        'officer':officer})
                                                                                        



# <------- Lk 03-08-23 ------->
def tkc_dgmem_current_invoice_list(request):
    officer = Officer.objects.filter(otp=request.session['otp'],employ_login_id = request.session['employ_login_id'],user_zone = request.session['zone']).last()  
    if officer is not None:
        wo_id=request.GET.get('woid')
        print(wo_id)
        invoice_id=request.GET.get('invoice_id')
        print("AAAAAAAAAAAAAAAAAAAAAA", invoice_id)
        inv_data = Invoice.objects.filter(work_order = wo_id, id=invoice_id).last()
        # inv_data = Invoice.objects.filter(work_order = wo_id).last()
        print(inv_data)
        wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,id=wo_id).last()
        print("#######1234#########",wo_data)

        # if request.method == "POST" and officer.role.Role_Name == "DGM_EM":
        if request.method == 'POST':
            wo_id2=request.GET.get('woid1')
            invoice_id2=request.GET.get('invoice_id1')
            print("UUUUUUUUUUUUUU",invoice_id2)
            invoice_data = Invoice.objects.filter(work_order = wo_id2,id=invoice_id2).last()
            # invoice_data = Invoice.objects.filter(work_order = wo_id2).last()
            print("999999999", wo_id2)
            dgmem_erp_payment_voucher_no = request.POST.get('dgmem_erp_payment_voucher_no')
            dgmem_pfms_no = request.POST.get('dgmem_pfms_no')
            dgmem_utr_no = request.POST.get('dgmem_utr_no')
            dgmem_remark = request.POST.get('dgmem_remark')
            dgmem_submit_name = request.POST.get('dgmem_submit_name')
            dgmem_submit_status = request.POST.get('dgmem_submit_status')
            gm_circle_submit_status = request.POST.get('gm_circle_submit_status')
            today_date=datetime.datetime.now()
            # cgmproject_submit_status = request.POST.get('cgmproject_submit_status')
            print("HHHHHHHHHHHHHHHHHHHHHHHHHH",gm_circle_submit_status)
            print("rrrrrrrrrrrrrrrrrrrrrrrrrr",dgmem_submit_status)
            # print("BBBBBBBBBFFFFFFFFFFFFFFFFF",dgmproject_submit_status)
            # print("wwwwwwwwwwwwwwwwwwwwwwwwww",cgmproject_submit_status)
            if int(dgmem_submit_status) == 1: 
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(dgmem_erp_payment_voucher_no=dgmem_erp_payment_voucher_no,
                                                                                                dgmem_pfms_no = dgmem_pfms_no,
                                                                                                dgmem_utr_no=dgmem_utr_no,
                                                                                                dgmem_remark=dgmem_remark,
                                                                                                dgmem_submit_status=dgmem_submit_status,
                                                                                                dgmem_submit_name=dgmem_submit_name,
                                                                                                dgmem_action=today_date)
            else:
                inv_data2 = Invoice.objects.filter(work_order = wo_id2,id = invoice_data.id).update(dgmem_erp_payment_voucher_no=dgmem_erp_payment_voucher_no,
                                                                                                dgmem_pfms_no = dgmem_pfms_no,
                                                                                                dgmem_utr_no=dgmem_utr_no,
                                                                                                dgmem_remark=dgmem_remark,
                                                                                                dgmem_submit_name=dgmem_submit_name,
                                                                                                dgmem_submit_status=2,
                                                                                                dgmem_action=today_date)
            # print("lllllllllll", inv_data2)
            # return render(request,'fqp/wo_invoice/tkc_dgmem_current_invoice_list.html')
            return redirect(tkc_show_current_invoice_list)
        
        return render(request,'fqp/wo_invoice/tkc_dgmem_current_invoice_list.html', {'invce_data':inv_data, 
                                                                                        'wo_data':wo_data,
                                                                                        'officer':officer})

