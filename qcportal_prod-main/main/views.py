import imp
from po.models import *
from django.db import connection
from fqp.models import *
import time
from datetime import date, datetime
from paywix.payu import Payu
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import datetime
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from vendor.models import *
from nabl.models import *
from tkc.models import *
from rca.models import *
from geopy.geocoders import Nominatim
import random
import math
import requests
from django.contrib import messages
from django.db.models import Q
from .utils import password_reset_token
from .forms import PasswordForgotForm, PasswordResetForm
from django.views.generic import FormView
import os
from django.core.mail import send_mail
from django.conf import settings
import psycopg2
from roof_top.models import *
import datetime
import socket
from django.core import validators
from main import payloads as payload
from main import constants as const

# Create your views here.



def home(request):
    return render(request, 'main/login.html')

def user(request):
    if request.method == "POST":
        user = request.POST.get('user')
        if user == 'VENDOR':

            return render(request, 'main/main_login.html',{'user':user})

        if user == 'TKC':

            return render(request, 'main/main_login.html',{'user':user})

        if user == 'NABL':

            return render(request, 'main/main_login.html',{'user':user})

        if user == 'SITE_STORE':

            return render(request, 'main/main_login.html',{'user':user})

        if user == 'user_vendor':
            return render(request, 'main/main_login.html')


        elif user == 'admin':

            return redirect('mpeb_login')

        elif user == 'registration':

            return redirect('reg')
        
        elif user == 'roof':
            return render(request,'roof/index.html')
        elif user == 'ca': 
            return redirect('ca/login')
            
        elif user == 'rca':
            return render(request,'rca/rca_login.html')    
    return render(request, 'main/index.html')


def logout(request):
    del request.session['otp']
    return redirect('login')


def success_reg(request):
    return render(request, 'main/sucess.html')


def success_payu(request):
    return render(request, 'main/sucess_payment.html')


def test1(request):
    return render(request, 'main/base1.html')


def index(request):
    return render(request, 'officer/index.html')


def index_login(request):
    return render(request, 'main/index_login.html')


all_otp = []


def login(request):
    if request.method == "POST":
        mobile_no = request.POST.get('mobile')
        otp = request.POST.get('otp')
        user_type = request.POST.get('type')
        if user_type == "SITE_STORE":
            print("This is site store dashboard")
            if SiteStore_Master.objects.filter(contact_no=mobile_no):
                data11 = SiteStore_Master.objects.filter(otp=otp)
                request.session['otp'] = otp
                if data11:                  
                                  
                    return render(request, 'site_store/site_store.html',
                                      {'data11': data11})
                else:
                    messages.warning(
                    request, "Otp Mismatched, Kindly Entered Correct Otp")
        if User_Registration.objects.filter(ContactNo=mobile_no,User_type=user_type).exists():
            data = User_Registration.objects.get(ContactNo=mobile_no,User_type=user_type)
            request.session['mobile_no'] = mobile_no
            request.session['otp'] = otp
            request.session['uid'] = mobile_no
            request.session['User_type'] = user_type

            uid = mobile_no
            uidd = otp
            user = user_type
            if data.Otp == otp:
                if data.User_type == "VENDOR":
                    if User_Registration.objects.filter(ContactNo=uid, payment=1, rca_vendor=0,User_type = user):
                        data11 = User_Registration.objects.filter(Otp=uidd,User_type = user)
                        con = User_Registration.objects.get(Otp=uidd,User_type = user)
                        payu_count = Payudata_main.objects.filter(Contact_No=con.ContactNo).count()
                        return render(request, 'vendor/basicinfo.html',
                                      {"userdata": data, 'data11': data11, 'payu_count': payu_count})
                    elif User_Registration.objects.filter(ContactNo=uid, payment=1, rca_vendor=1,User_type = user):
                        data11 = User_Registration.objects.filter(Otp=uidd,User_type = user)
                        return render(request, 'vendor/RCA_vendor_base.html', {"userdata": data, 'data11': data11})
                    # elif BankDetails.objects.filter(user_id=uid).exists() and UserCompanyDataMain.objects.filter(
                            # user_id=uid).exists() and AuthorisedPerson.objects.filter(user_id=uid).exists():

                        # data = BankDetails.objects.filter(user_id=uid)
                        # data1 = UserCompanyDataMain.objects.filter(
                            # user_id=uid)
                        # data2 = BankDetails.objects.filter(user_id=uid)
                        # return render(request, 'main/reg_fifth.html', {'data': data2[0]})
                    elif AuthorisedPerson.objects.filter(
                            user_id_id=data).exists() and UserCompanyDataMain.objects.filter(user_id_id=data).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid,User_type = user)

                        data = User_Registration.objects.get(ContactNo=mobile_no,User_type = user)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id_id=data)
                        data2 = AuthorisedPerson.objects.filter(
                            user_id_id=data)
                        return render(request, 'main/reg_fifth.html',
                                      {'data1': data1[0], 'data': data, 'data2': data2[0]})
                    elif UserCompanyDataMain.objects.filter(user_id_id=data).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid,User_type = user)
                        data = User_Registration.objects.get(ContactNo=mobile_no,User_type = user)

                        data1 = UserCompanyDataMain.objects.filter(
                            user_id_id=data)
                        return render(request, 'main/reg_third.html', {'data1': data1[0], 'data': data})

                    else:
                        data = User_Registration.objects.filter(
                            ContactNo=uid,User_type = user)
                        return render(request, 'main/reg_second.html', {'data': data[0]})

                elif data.User_type == "TKC":
                    from datetime import datetime
                    import datetime                    
                    abc = request.session['otp']
                    if User_Registration.objects.filter(ContactNo=uid, payment=1,User_type = user):
                        data11 = User_Registration.objects.filter(Otp=uidd,User_type = user)
                        con = User_Registration.objects.get(Otp=uidd,User_type = user)
                        payu_count = Payudata_main.objects.filter(Contact_No=con.ContactNo).count()
                        if con.Authentication_id:
                            if TKC_Document.objects.filter(user_id=con.User_Id, Types_of_Docs='Electrical License').exists():
                                if con.activation_before_expired == 0 or con.activation_after_expired == 0:
                                    exp = TKC_Document.objects.filter(user_id=con.User_Id, Types_of_Docs='Electrical License').first()
                                    expi_date = exp.Doc_expiry_date
                                    from datetime import date
                                    from datetime import time
                                    from datetime import datetime
                                    import datetime
                                    to_daaa =datetime.datetime.today()
                                    oyt_name = TKC_Payment.objects.get(id = data.Oyt )
                                    name = oyt_name.Name
                                    if con.Authentication_id:
                                        cert = data.Authentication_id
                                        return render(request, 'tkc/basicinfo.html',
                                            {"userdata": data, 'abc': abc, 'data11': data11, 'payu_count': payu_count,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'oyt':name})
                                    return render(request, 'tkc/basicinfo.html',
                                            {"userdata": data, 'abc': abc, 'data11': data11, 'payu_count': payu_count,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'oyt':name})
                                else:
                                    exp = TKC_Document.objects.filter(user_id=con.User_Id, Types_of_Docs='Electrical License').first()
                                    expi_date = exp.Doc_expiry_date
                                    from datetime import date
                                    from datetime import time
                                    from datetime import datetime
                                    import datetime
                                    to_daaa =datetime.datetime.today()
                                    oyt_name = TKC_Payment.objects.get(id = data.Oyt )
                                    name = oyt_name.Name
                                    if con.Authentication_id:
                                        cert = data.Authentication_id
                                        return render(request, 'tkc/basicinfo.html',
                                            {"userdata": data, 'abc': abc, 'data11': data11, 'payu_count': payu_count,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'oyt':name})
                                    return render(request, 'tkc/basicinfo.html',
                                            {"userdata": data, 'abc': abc, 'data11': data11, 'payu_count': payu_count,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'oyt':name})
                            return render(request, 'tkc/basicinfo.html',
                                      {"userdata": data, 'abc': abc, 'data11': data11, 'payu_count': payu_count})
                        return render(request, 'tkc/basicinfo.html',
                                      {"userdata": data, 'abc': abc, 'data11': data11, 'payu_count': payu_count})
                    # elif BankDetails.objects.filter(user_id=uid).exists() and UserCompanyDataMain.objects.filter(
                    #         user_id=uid).exists() and AuthorisedPerson.objects.filter(user_id=uid).exists():
                    #     data1 = UserCompanyDataMain.objects.filter(
                    #         user_id=uid)
                    #     data2 = BankDetails.objects.filter(user_id=uid)
                    #     return render(request, 'main/reg_fifth.html', {'data': data2[0]})
                    elif AuthorisedPerson.objects.filter(
                            user_id_id=data).exists() and UserCompanyDataMain.objects.filter(user_id_id=data).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        data = User_Registration.objects.get(ContactNo=mobile_no,User_type = user)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id_id=data)
                        data2 = AuthorisedPerson.objects.filter(
                            user_id_id=data)
                        return render(request, 'main/reg_fifth.html',
                                      {'data1': data1[0], 'data': data, 'data2': data2[0]})
                    elif UserCompanyDataMain.objects.filter(user_id_id=data).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid,User_type = user)

                        data = User_Registration.objects.get(ContactNo=mobile_no,User_type = user)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id_id=data)
                        return render(request, 'main/reg_third.html', {'data1': data1[0], 'data': data})
                    else:
                        data = User_Registration.objects.get(
                            ContactNo=uid,User_type = user)
                        return render(request, 'main/reg_second.html', {'data': data})
                else:
                    abc = request.session['otp']
                    if User_Registration.objects.filter(ContactNo=uid, Basic_Details=1,User_type = user):
                        return render(request, 'nabl/basics.html', {"userdata": data})
                    if NABL_Document.objects.filter(
                            user_id=request.session['otp']) and UserCompanyDataMain.objects.filter(
                        user_id_id=data).exists():
                        return render(request, 'nabl/user_base.html', {"userdata": data, 'abc': abc})
                    # elif BankDetails.objects.filter(user_id=uid).exists():
                    #     data11 = User_Registration.objects.filter(
                    #         ContactNo=uid)
                    #     data1 = UserCompanyDataMain.objects.filter(
                    #         user_id=uid)
                    #     data2 = AuthorisedPerson.objects.filter(
                    #         user_id=uid)
                    #     return render(request, 'nabl/basics.html', {"userdata": data})
                    #     # return render(request, 'nabl/basics.html',
                    #     #             {'data1': data1[0], 'data': data[0], 'data2': data2[0]})

                    elif AuthorisedPerson.objects.filter(
                            user_id_id=data).exists() and UserCompanyDataMain.objects.filter(user_id_id=data).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid,User_type = user)

                        data = User_Registration.objects.get(ContactNo=mobile_no,User_type = user)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id_id=data)
                        data2 = AuthorisedPerson.objects.filter(
                            user_id_id=data)
                        return render(request, 'main/reg_fifth.html',
                                      {'data1': data1[0], 'data': data, 'data2': data2[0]})
                    elif UserCompanyDataMain.objects.filter(user_id_id=data).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid,User_type = user)

                        data = User_Registration.objects.get(ContactNo=mobile_no,User_type = user)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id_id=data)
                        return render(request, 'main/reg_third.html', {'data1': data1[0], 'data': data})
                    else:
                        data = User_Registration.objects.filter(
                            ContactNo=uid,User_type = user)
                        return render(request, 'main/reg_second.html', {'data': data[0]})
            else:
                messages.warning(
                    request, "Otp Mismatched, Kindly Entered Correct Otp")
        else:
            messages.warning(
                request, "Mobile Number is not registered,Kindly Register first")
    return render(request, 'main/main_login.html')


def otp_verify(request):
    global all_otp
    if request.session.has_key('otp'):
        if request.method == "POST":
            uidd = request.session['otp']
            service_type = request.POST.get('captcha')
            data = User_Registration.objects.get(Otp=uidd)
            uid = data.ContactNo
            if service_type == all_otp[-1]:
                if data.User_type:
                    if data.User_type == "VENDOR":
                        if User_Registration.objects.filter(ContactNo=uid, payment=1, rca_vendor=0):
                            data11 = User_Registration.objects.filter(Otp=uidd)
                            return render(request, 'vendor/basicinfo.html', {"userdata": data, 'data11': data11})

                        elif User_Registration.objects.filter(ContactNo=uid, payment=1, rca_vendor=1):
                            data11 = User_Registration.objects.filter(Otp=uidd)
                            return render(request, 'vendor/RCA_vendor_base.html', {"userdata": data, 'data11': data11})


                        elif BankDetails.objects.filter(user_id=uid).exists() and UserCompanyDataMain.objects.filter(
                                user_id=uid).exists() and AuthorisedPerson.objects.filter(user_id=uid).exists():

                            data = BankDetails.objects.filter(user_id=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            data2 = BankDetails.objects.filter(user_id=uid)
                            return render(request, 'main/reg_fourth.html', {'data': data2[0]})
                        elif AuthorisedPerson.objects.filter(
                                user_id=uid).exists() and UserCompanyDataMain.objects.filter(user_id=uid).exists():
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            data2 = AuthorisedPerson.objects.filter(
                                user_id=uid)
                            return render(request, 'main/reg_third.html',
                                          {'data1': data1[0], 'data': data[0], 'data2': data2[0]})
                        elif UserCompanyDataMain.objects.filter(user_id=uid).exists():
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            return render(request, 'main/reg_second.html', {'data1': data1[0], 'data': data[0]})

                        else:
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            return render(request, 'main/reg_second.html', {'data': data[0]})

                    elif data.User_type == "TKC":
                        abc = request.session['otp']
                        if User_Registration.objects.filter(ContactNo=uid, payment=1):
                            data11 = User_Registration.objects.filter(Otp=uidd)
                            return render(request, 'tkc/basicinfo.html',
                                          {"userdata": data, 'abc': abc, 'data11': data11})
                        elif BankDetails.objects.filter(user_id=uid).exists() and UserCompanyDataMain.objects.filter(
                                user_id=uid).exists() and AuthorisedPerson.objects.filter(user_id=uid).exists():
                            data = BankDetails.objects.filter(ContactNo=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            data2 = BankDetails.objects.filter(user_id=uid)
                            return render(request, 'main/reg_fourth.html', {'data': data2[0]})
                        elif AuthorisedPerson.objects.filter(
                                user_id=uid).exists() and UserCompanyDataMain.objects.filter(user_id=uid).exists():
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            data2 = AuthorisedPerson.objects.filter(
                                user_id=uid)
                            return render(request, 'main/reg_third.html',
                                          {'data1': data1[0], 'data': data[0], 'data2': data2[0]})
                        elif UserCompanyDataMain.objects.filter(user_id=uid).exists():
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            return render(request, 'main/reg_second.html', {'data1': data1[0], 'data': data[0]})
                        else:
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            return render(request, 'main/reg_second.html', {'data': data[0]})
                    else:
                        abc = request.session['otp']
                        if User_Registration.objects.filter(ContactNo=uid, payment=1):
                            return render(request, 'nabl/base1.html', {"userdata": data})
                        if NABL_Document.objects.filter(
                                user_id=request.session['otp']) and UserCompanyDataMain.objects.filter(
                            user_id=uid).exists():
                            return render(request, 'nabl/user_base.html', {"userdata": data, 'abc': abc})
                        elif AuthorisedPerson.objects.filter(
                                user_id=uid).exists() and UserCompanyDataMain.objects.filter(user_id=uid).exists():
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            data2 = AuthorisedPerson.objects.filter(
                                user_id=uid)
                            return render(request, 'main/reg_third.html',
                                          {'data1': data1[0], 'data': data[0], 'data2': data2[0]})
                        elif UserCompanyDataMain.objects.filter(user_id=uid).exists():
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            data1 = UserCompanyDataMain.objects.filter(
                                user_id=uid)
                            return render(request, 'main/reg_second.html', {'data1': data1[0], 'data': data[0]})
                        else:
                            data = User_Registration.objects.filter(
                                ContactNo=uid)
                            return render(request, 'main/reg_second.html', {'data': data[0]})

            else:
                messages.warning(request, "Invalid OTP")
        return render(request, 'main/otp_verify.html')


def type_of_user(request):
    data = User_Registration.objects.get(Otp=request.session['oid'])
    if request.method == "POST":
        get_data = User_Registration.objects.get(Otp=request.session['oid'])
        get_data.User_type = request.POST.get('user')
        get_data.save()
        return redirect('test')
    return render(request, 'main/select_user_type.html')


def user_type(request):
    return render(request, 'main/usertype.html')


def thanks(request):
    return render(request, 'main/thankyou.html')


def test(request):
    data = User_Registration.objects.get(Otp=request.session['otp'])
    data11 = User_Registration.objects.filter(Otp=request.session['otp'])
    if data.User_type == "VENDOR":

        return render(request, 'vendor/base1.html', {"userdata": data})

    elif data.User_type == "TKC":
        otp = data.Otp
        abc = request.session['otp']
        return render(request, 'tkc/base1.html', {"userdata": data, 'abc': abc, 'dddd': data11})

    else:
        return render(request, 'nabl/nabl_base.html', {"userdata": data})

    # return render(request, 'main/user.html', {"userdata": data})


def user_data_show(request):
    data = User_Registration.objects.get(Otp=request.session['oid'])
    return render(request, 'main/user_data_show.html', {"userdata": data})


def reg(request):
    type_data = OwnerShip_Type_Table_Master.objects.all()
    return render(request, 'main/reg_first.html', {'type': type_data})


def reg_first(request):
    try:
        type_data = OwnerShip_Type_Table_Master.objects.all()
        if request.method == "POST":
            mobile = request.POST.get('mobile')
            data = User_Registration.objects.filter(ContactNo=mobile)
            User_type = request.POST.get('user')
            service_type = request.POST.get('service_type')
            company_name_e = request.POST.get('company_name_e')
            company_name_h = request.POST.get('company_name_h')
            name_of_authorized_e = request.POST.get('name_of_authorized_e')
            name_of_authorized_h = request.POST.get('name_of_authorized_h')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            zone = request.POST.get('zone')
            one = company_name_e
            two = company_name_h
            three = name_of_authorized_e
            four = name_of_authorized_h
            five = User_type
            six = mobile
            seven = email
            data = User_Registration.objects.filter(ContactNo=mobile,User_type=User_type)
            if User_Registration.objects.filter(ContactNo=mobile,User_type=User_type).exists():
                messages.warning(request, "Mobile Number already registered")
                return render(request, 'main/reg_first.html',
                              {'one': one, 'two': two, 'three': three, 'four': four, 'five': five, 'six': six,
                               'seven': seven, 'type': type_data})
         
            else:
                user_details = User_Registration(User_type=User_type, Type_of_business=service_type,
                                                 CompanyName_E=company_name_e, User_zone=zone,
                                                 CompanyName_H=company_name_h, Authorised_person_H=name_of_authorized_h,
                                                 Authorised_person_E=name_of_authorized_e, ContactNo=mobile,
                                                 Email_Id=email)
                user_details.save()
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007022255202070533&mobile_number=" + str(
                    mobile) + "&v1=" + str(company_name_e) + "&v2=" + str() + "&v3=" + "MP" + str(zone) + "&v4=" + str(mobile) + "&v5=" + str(
                    'https://qcportal.mpcz.in/')
                response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

                print(datetime.now())
                sms_template = message_template_log(template_id = '1007022255202070533',date = datetime.now(),mobile_number = mobile)
                sms_template.save()
                
                send_mail(
                    'Quality Monitoring Portal-Registration Complete',
                    'Thank you for your Registration, your user id is your mobile number, please login to portal https://qcportal.mpcz.in/ for completing the registration process',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.warning(request, "You are successfully registered")
                data = User_Registration.objects.filter(ContactNo=mobile,User_type=User_type)
                request.session['uid'] = mobile
                request.session['User_type'] = User_type
                return render(request, 'main/main_login.html')
    except Exception as e:
        return render(request, 'main/main_login.html')

    return render(request, 'main/reg_first.html', {'type': type_data})

def reg_second(request):
    if request.session.has_key('uid'):
        if request.method == "POST":
            uid = request.session['uid']
            add1 = request.POST.get('add1')
            add2 = request.POST.get('add2')
            add3 = request.POST.get('add3')
            add4 = request.POST.get('add4')
            # Company_Fax = request.POST.get('fax')
            Company_Pan_No = request.POST.get('pan')
            # Company_Gumastha_No = request.POST.get('reg_no')
            Company_Gst_No = request.POST.get('gst')
            # reg_date = request.POST.get('reg_date')
            Company_Address_1 = request.POST.get("add1")
            Company_Address_2 = request.POST.get("add2")
            p_code = request.POST.get("zip")
            state = request.POST.get("add4")
            district = request.POST.get("add3")
            City = request.POST.get("city")
            Office_Address_1 = request.POST.get("add5")
            Office_Address_2 = request.POST.get("add6")
            p_code_2 = request.POST.get("zip2")
            state_2 = request.POST.get("add7")
            district_2 = request.POST.get("add8")
            City_2 = request.POST.get("city2")
            data = User_Registration.objects.filter(ContactNo=uid,User_type=request.session['User_type'])
            user_type_nabl  = data[0].User_type
            data_new = User_Registration.objects.get(ContactNo=uid,User_type=request.session['User_type'])
            
            # if user_type_nabl == 'TKC' or user_type_nabl =="VENDOR":
          
            #     if UserCompanyDataMain.objects.filter(Company_Gst_No=Company_Gst_No).exists():
            #         abc = UserCompanyDataMain.objects.filter(Company_Gst_No=Company_Gst_No)
            #         messages.warning(request, "GST number already exists for ")
            #         return render(request, 'main/reg_second.html',{'data': data[0],'abc':abc[0]})
            #     elif UserCompanyDataMain.objects.filter(Company_Pan_No=Company_Pan_No).exists():
            #         abc = UserCompanyDataMain.objects.filter(Company_Pan_No=Company_Pan_No)
            #         messages.warning(request, "PAN  number already exists for")
            #         return render(request, 'main/reg_second.html',{'data': data[0],'abc':abc[0]})

            #     else:
            #         data = User_Registration.objects.filter(ContactNo=uid,User_type=request.session['User_type'])
            #         company = UserCompanyDataMain(user_id_id=data_new,user_id=uid, CompanyName_E=data[0].CompanyName_E,
            #                                     CompanyName_H=data[0].CompanyName_H, Company_Contact_No=uid,
            #                                     Company_Fax=Company_Fax, Company_Pan_No=Company_Pan_No,
            #                                     Company_Gumastha_No=Company_Gumastha_No, Company_Gst_No=Company_Gst_No,
            #                                     Registration_Date=reg_date, Company_add_1=Company_Address_1,
            #                                     Company_add_2=Company_Address_2, Company_pin_code=p_code, Company_state=state,
            #                                     Company_dist=district, Company_city=City, Company_t_add_1=Office_Address_1,
            #                                     Company_t_add_2=Office_Address_2, Company_t_pin_code=p_code_2,
            #                                     Company_t_state=state_2, Company_t_dist=district_2, Company_t_city=City_2)
            #         company.save()
            #         data = User_Registration.objects.get(ContactNo=uid,User_type=request.session['User_type'])
            #         return render(request, 'main/reg_third.html', {'data': data})
            # else:
            data = User_Registration.objects.filter(ContactNo=uid,User_type=request.session['User_type'])
            company = UserCompanyDataMain(user_id_id=data_new,user_id=uid, CompanyName_E=data[0].CompanyName_E,
                                        CompanyName_H=data[0].CompanyName_H, Company_Contact_No=uid,
                                        Company_Pan_No=Company_Pan_No,
                                        Company_Gst_No=Company_Gst_No,
                                        Company_add_1=Company_Address_1,
                                        Company_add_2=Company_Address_2, Company_pin_code=p_code, Company_state=state,
                                        Company_dist=district, Company_city=City, Company_t_add_1=Office_Address_1,
                                        Company_t_add_2=Office_Address_2, Company_t_pin_code=p_code_2,
                                        Company_t_state=state_2, Company_t_dist=district_2, Company_t_city=City_2)
            company.save()
            data = User_Registration.objects.get(ContactNo=uid,User_type=request.session['User_type'])
            return render(request, 'main/reg_third.html', {'data': data})
    return render(request, 'main/main_login.html')




def reg_third(request):
    if request.session.has_key('uid'):
        uid = request.session['uid']
        data = User_Registration.objects.filter(ContactNo=uid,User_type=request.session['User_type'])
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        # aadhar = request.POST.get('aadhar')
        auth_per_addresslin1 = request.POST.get('add5')
        auth_per_addresslin2 = request.POST.get('add6')
        auth_per_state = request.POST.get('state')
        auth_per_district = request.POST.get('district')
        auth_per_city = request.POST.get('city')
        auth_per_pincode = request.POST.get('zip')
        direct_name = request.POST.get("dir_name")
        direct_name_hindi = request.POST.get("dir_name_hindi")
        direct_dob = request.POST.get('dir_dob')
        direct_mobile = request.POST.get('dir_mobile')
        direct_email = request.POST.get('dir_email')
        # direct_aadhar = request.POST.get('dir_aadhar')
        direct_addresslin1 = request.POST.get('dir_add1')
        direct_addresslin2 = request.POST.get('dir_add2')
        direct_state = request.POST.get('dir_state')
        direct_district = request.POST.get('dir_district')
        direct_city = request.POST.get('dir_city')
        direct_pincode = request.POST.get('dir_zip')

        # url = https://sms.mpcz.in/api/v1/send-otp?app_key=f9hqGlTRKQLv9jwyTjHExUUWP&app_secret=kqKO0eJrouKQFa5&dlt_template_id=1207160939529646113&mobile_number=8839070121&v1=Application&v2=1

        # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}

        # # proxyDict = {"http" : "proxy.mpcz.in:8080"}

        # # for server set proxy
        # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}

        # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=f9hqGlTRKQLv9jwyTjHExUUWP&app_secret=kqKO0eJrouKQFa5&dlt_template_id=1207160939529646113&mobile_number=" + str(uid) + "&v1=Application&v2="
        # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
        data_new = User_Registration.objects.get(ContactNo=uid,User_type=request.session['User_type'])
        person = AuthorisedPerson(user_id_id = data_new,user_id=uid, Authorised_P_Name_E=data[0].Authorised_person_E,
                                  Authorised_P_Name_H=data[0].Authorised_person_H,
                                  Authorised_P_DOB=dob, Authorised_P_Number=mobile,
                                  Authorised_P_add_1=auth_per_addresslin1, Authorised_P_add_2=auth_per_addresslin2,
                                  Authorised_P_state=auth_per_state, Authorised_P_District=auth_per_district,
                                  Authorised_P_City=auth_per_city, Authorised_P_pin_code=auth_per_pincode,
                                  Director_P_Name_E=direct_name, Director_P_Name_H=direct_name_hindi,
                                  Director_P_DOB=direct_dob, Director_P_Number=direct_mobile,
                                  Director_P_Email=direct_email,
                                  Director_P_add_1=direct_addresslin1, Director_P_add_2=direct_addresslin2,
                                  Director_P_pin_code=direct_pincode, Director_P_state=direct_state,
                                  Director_P_District=direct_district, Director_P_City=direct_city

                                  )
        person.save()
        return render(request, 'main/reg_fifth.html', {'user': data[0]})
    return render(request, 'main/main_login.html.html')


def reg_fourth(request):
    if request.session.has_key('uid'):
        uid = request.session['uid']
        bank_name = request.POST.get('bank_name')
        ifsc = request.POST.get('ifsc')
        ac_holder_name = request.POST.get('ac_holder_name')
        ac_number = request.POST.get('ac_number')
        bank = BankDetails(user_id=uid, Bank_name=bank_name, Account_Holder_Name=ac_holder_name,
                           Account_Number=ac_number, IFSC=ifsc)
        bank.save()

        data = User_Registration.objects.filter(ContactNo=uid)
        data111 = User_Registration.objects.get(ContactNo=uid)
        ssss = data111.ContactNo

        return render(request, 'main/reg_fifth.html', {'user': data[0]})
    return render(request, 'main/main_login.html')


def reg_fifth(request):
    if request.session.has_key('uid'):
        if request.method == "POST":
            uid = request.session['uid']
            data = User_Registration.objects.filter(ContactNo=uid,User_type=request.session['User_type'])
            if data[0].User_type == "NABL":
                data.update(Basic_Details=1)
                return render(request,'main/index.html')
            return render(request, 'main/reg_sixth.html', {'c_type': data[0]})
    return render(request, 'main/main_login.html')


def reg_sixth(request):
    if request.session.has_key('uid'):
        uid = request.session['uid']
        data = User_Registration.objects.filter(ContactNo=uid,User_type=request.session['User_type'])
        data.update(Basic_Details=1)
        return redirect('payu_demo_registration')
    return render(request, 'main/main_login.html')

# ............................LOGIN FOR FI AND W&p..........


# old by  rohit.....................
# def mpeb_login(request):
#     if request.method == 'POST':
#         if User_Registration.objects.filter(user_name="mpeb"):
#             if User_Registration.objects.filter(password="12345"):
#                 return redirect('mpeb_base')
#
#             else:
#                 return render(request, 'main/mpeb_reg.html')
#         return render(request, 'main/mpeb_reg.html')
#     return render(request, 'main/mpeb_reg.html')

# poornima..........................................
def mpeb_base(request):
    return render(request, 'main/mpeb_base.html')


def mpeb_login(request):
    if request.method == "POST":
        employ_login_id = request.POST.get('employ_login_id')
#         hostname = socket.gethostname()
#         IPAddr = socket.gethostbyname(hostname)
#         print("ipppp",IPAddr)
        
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         print("ipttttttttttttttrohitkkkkppnew",ip)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
            print("ipipipipipip",ip_address)
        else:
            ip = request.META.get('REMOTE_ADDR')
            print("nnneeewwwipipiipi",ip)
        
        
        if Officer.objects.filter(employ_login_id=employ_login_id).exists():
            if employ_login_id == 'PS_OFFICE_DISCOM_RCA' or  employ_login_id == 'PS_OFFICE_DGM_WORK' or employ_login_id == 'PS_OFFICE_DGM_FINANCE' or employ_login_id == 'PS_OFFICE':
                data = Officer.objects.get(employ_login_id=employ_login_id)
                data.otp = '123456'
                data.save()
                otp = '123456'
                # sms_otp = Officer.objects.get(employ_login_id=employ_login_id)
                # sms_number = sms_otp.mobile
                # # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                # # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(
                # #     sms_number) + "&v1=" + str(otp) + "&v2=" + str()
                # # response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                request.session['employ_login_id'] = employ_login_id
                request.session['otp'] = otp
                print("yyyyyyyyyyyy",otp)
                #messages.warning(request, otp)
                return redirect('mpeb_verify_otp')
            def generateOTP():
                digits = "123456789"
                OTP = ""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 9)]
                return OTP

            otp = generateOTP()
            data = Officer.objects.get(employ_login_id=employ_login_id)
            data.otp = otp
            data.save()
            sms_otp = Officer.objects.get(employ_login_id=employ_login_id)
            sms_number = sms_otp.mobile
            zone = sms_otp.user_zone
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(
                sms_number) + "&v1=" + str(otp) + "&v2=" + str()
                
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = sms_number)
            sms_template.save()
            # response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            request.session['employ_login_id'] = employ_login_id
            request.session['otp'] = otp
            request.session['zone'] = zone
            #messages.warning(request, otp)
            return redirect('mpeb_verify_otp')
        
        elif InspectingOfficerInfo.objects.filter(officer_employ_id=employ_login_id).exists():
            #if employ_login_id == 'PS_OFFICE_DISCOM_RCA' or  employ_login_id == 'PS_OFFICE_DGM_WORK' or employ_login_id == 'PS_OFFICE_DGM_FINANCE' or employ_login_id == 'PS_OFFICE_CGM_QC':
            data1 = InspectingOfficerInfo.objects.get(officer_employ_id=employ_login_id)
            data1.otp = '123456'
            data1.save()
            otp = '123456'
           
            request.session['employ_login_id'] = employ_login_id
            request.session['otp'] = otp
            def generateOTP():
                digits = "123456789"
                OTP = ""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 9)]
                return OTP

            otp = generateOTP()
            data1 = InspectingOfficerInfo.objects.get(officer_employ_id=employ_login_id)
            data1.Otp = otp
            data1.save()
            sms_otp = InspectingOfficerInfo.objects.get(officer_employ_id=employ_login_id)
            sms_number = sms_otp.contact_no
            zone = sms_otp.user_zone
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(
                sms_number) + "&v1=" + str(otp) + "&v2=" + str()
                
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = sms_number)
            sms_template.save()
            response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            request.session['employ_login_id'] = employ_login_id
            request.session['otp'] = otp
            request.session['zone'] = zone
            return redirect('mpeb_verify_otp')
    return render(request, 'main/mpeb_reg.html')


def user_finance_base(request):
    return render(request, 'main/userfinancebase.html')


def works_base(request):
    return render(request, 'officer/dgm_base.html')


def mpeb_verify_otp(request):
    if request.session['employ_login_id']:
        if request.method == 'POST':
            if request.POST.get('captcha') == request.session['otp']:
                if Officer.objects.filter(otp=request.session['otp']) & Officer.objects.filter(
                        employ_login_id=request.session['employ_login_id']):
                    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                               User_type='VENDOR').count()
                    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                               User_type='VENDOR').count()
                    total = approve + pending

                    approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                                   User_type='TKC').count()
                    pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                                   User_type='TKC').count()
                    total_tkc = approve_tkc + pending_tkc
                    request.session['total_approved_vendor'] = approve
                    request.session['total_pending_vendor'] = pending
                    request.session['total_registered_vendor'] = approve + pending
                    officer = Officer.objects.get(
                        employ_login_id=request.session['employ_login_id'])
                    if officer.role.Role_Name == 'DGM (QC)' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        return render(request, 'officer/dgm_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'DGM (QC)WZ' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        return render(request, 'officer/dgm_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'DGM (QC)EZ' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        return render(request, 'officer/dgm_base.html', {'data': officer})
                    
                    
                    elif officer.role.Role_Name == 'PS_OFFICE_CGM_QC' and officer.role.user_zone == 'CZ':
                        if request.session.has_key('employ_login_id'):
                            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
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
                        
                        else:
                            return render(request, 'main/main_login.html',{"error_msg":'You need to login again'})

                    
                    elif officer.role.Role_Name == 'DGM(W&P)' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone


                        return render(request, 'officer/dgm_work.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})



                    elif officer.role.Role_Name == 'DGM(W&P)EZ' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])

                        request.session['officer'] = officer.user_zone

                        return render(request, 'officer/dgm_work.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
                    
                    elif officer.role.Role_Name == 'PMA' and officer.role.user_zone == 'CZ':                        
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])                      
                        request.session['officer'] = officer.user_zone                 
                        return render(request, 'officer/pma_login.html', {'data': officer})
                    
                    
                    elif officer.role.Role_Name == 'JE' and officer.user_zone == 'CZ' or officer.role.Role_Name == 'JE' and officer.user_zone == 'EZ' or officer.role.Role_Name == 'JE' and officer.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone 
                        return render(request, 'officer/je_dashboard.html',{"officer":officer})


                    elif officer.role.Role_Name == 'GM(CIRCLE)' and officer.role.user_zone == 'CZ':                        
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                            
                        request.session['officer'] = officer.user_zone                  
                    
                        return render(request, 'officer/gm_circle_login.html', {'data': officer})
                    
                    
                    elif officer.role.Role_Name == 'DGM_STC' and officer.role.user_zone == 'CZ':                        
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                            
                        request.session['officer'] = officer.user_zone                  
                    
                        return render(request, 'officer/dgm_stc_login.html', {'data': officer})
                    
                    
                    elif officer.role.Role_Name == 'DGM_ONM' and officer.role.user_zone == 'CZ':                        
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                            
                        request.session['officer'] = officer.user_zone                  
                    
                        return render(request, 'officer/dgm_onm_login.html', {'data': officer})


                    

                    elif officer.role.Role_Name == 'DGM(W&P)WZ' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])

                        request.session['officer'] = officer.user_zone

                        return render(request, 'officer/dgm_work.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})



                    # elif officer.mobile == '9981393754':
                    #     officer = Officer.objects.get(
                    #         employ_login_id=request.session['employ_login_id'])
                    #     approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                    #                                                User_type='VENDOR').count()
                    #     pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                    #                                                User_type='VENDOR').count()
                    #     total = approve + pending

                    #     approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                    #                                                    User_type='TKC').count()
                    #     pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                    #                                                    User_type='TKC').count()
                    #     total_tkc = approve_tkc + pending_tkc

                    #     return render(request, 'officer/dgm_work.html', {'data': officer, 'approve': approve, 'pending': pending, 'total': total, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
                    elif officer.role.Role_Name == 'DGM(Finance)' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,User_zone='CZ',
                                                                   User_type='VENDOR').count()
                        pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,User_zone='CZ',
                                                                   User_type='VENDOR').count()
                        total = approve + pending

                        approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,User_zone='CZ',
                                                                       User_type='TKC').count()
                        pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,User_zone='CZ',
                                                                       User_type='TKC').count()
                        total_tkc = approve_tkc + pending_tkc

                        request.session['officer'] = officer.user_zone



                        return render(request, 'officer/dgm_finance.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})



# ***************CHANGE

                    elif officer.role.Role_Name == 'DGM (Finance)EZ' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,User_zone='EZ',
                                                                   User_type='VENDOR').count()
                        pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,User_zone='EZ',
                                                                   User_type='VENDOR').count()
                        total = approve + pending

                        approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,User_zone='EZ',
                                                                       User_type='TKC').count()
                        pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,User_zone='EZ',
                                                                       User_type='TKC').count()
                        total_tkc = approve_tkc + pending_tkc

                        request.session['officer'] = officer.user_zone
                        return render(request, 'officer/dgm_finance.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})



                    elif officer.role.Role_Name == 'DGM (Finance)WZ' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,User_zone='WZ',
                                                                   User_type='VENDOR').count()
                        pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,User_zone='WZ',
                                                                   User_type='VENDOR').count()
                        total = approve + pending

                        approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,User_zone='WZ',
                                                                       User_type='TKC').count()
                        pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,User_zone='WZ',
                                                                       User_type='TKC').count()
                        total_tkc = approve_tkc + pending_tkc

                        request.session['officer'] = officer.user_zone
                        return render(request, 'officer/dgm_finance.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


                    elif officer.role.Role_Name == 'CGM (QC)' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
                        request.session['officer'] = officer.user_zone
                        request.session['employ_id'] = officer.employ_id
                        request.session['zone'] = officer.user_zone
                        request.session['employ_login_id'] = officer.employ_login_id                 
                        return render(request, 'main/mpeb_base.html',{'data': officer})

                    elif officer.role.Role_Name == 'CGM (QC)WZ' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
                        request.session['officer'] = officer.user_zone
                        request.session['zone'] = officer.user_zone
                        request.session['employ_id'] = officer.employ_id
                        request.session['employ_login_id'] = officer.employ_login_id                 

                        return render(request, 'main/mpeb_base.html',{'data': officer})

                    elif officer.role.Role_Name == 'CGM (QC)EZ' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
                        request.session['officer'] = officer.user_zone
                        request.session['zone'] = officer.user_zone
                        request.session['employ_id'] = officer.employ_id
                        request.session['employ_login_id'] = officer.employ_login_id                 

                        return render(request, 'main/mpeb_base.html',{'data': officer})




                    elif officer.role.Role_Name == 'GM(WORKS)' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        request.session['zone'] = officer.user_zone    
                        return render(request, 'officer/gm_work_base.html',{'officer': officer})


                    elif officer.role.Role_Name == 'GM(WORKS)_EAST' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        request.session['zone'] = officer.user_zone    
                        return render(request, 'officer/gm_work_base.html',{'officer': officer})


                    elif officer.role.Role_Name == 'GM(WORKS)_WEST' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        request.session['zone'] = officer.user_zone    
                        return render(request, 'officer/gm_work_base.html',{'officer': officer})


                    elif officer.role.Role_Name == 'DGM ( Procurement )':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'po/procurement_dashboard.html', {'data': officer})
                    elif officer.role.Role_Name == 'CGM ( Procurement )':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'officer/cgm_procurement.html', {'data': officer})
                        
                    elif officer.role.Role_Name == 'Areastore' and str(officer.otp) == request.session['otp']:
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.employ_id
                        request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
                        return render(request, 'po/area_store/areastore_base.html', {'data': officer})
                    
                    elif officer.role.Role_Name == 'Areastore_Circle' and str(officer.otp) == request.session['otp']:
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.employ_id
                        return render(request, 'rca/As_circle_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'NABL001':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'po/nabl/dasbordbase.html', {'data': officer})
                    
                    elif officer.role.Role_Name == 'Field_Officer':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'officer/field_officer.html',{'data': officer})    


                    elif officer.role.Role_Name == 'RCA(Cell)' and str(officer.otp) == request.session['otp']:
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.employ_id
                        return render(request, 'rca/RCA_base.html', {'data': officer})

                    

                    elif officer.role.Role_Name == '7000551592':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'officer/tmqm_base.html', {'data': officer})
                    elif officer.role.Role_Name == 'Project (Creator)':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'projectSection/base.html', {'data': officer})

                    elif officer.role.Role_Name == 'Commercial Section' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'CA/commercial_sales.html')


                    elif officer.role.Role_Name == 'RoofTop_Approver' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        user_zone = officer.user_zone
                        request.session['user_zone'] = officer.user_zone
                        return render(request, 'officer/RoofTop_Approver_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'RoofTop_Approver_EZ' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        user_zone = officer.user_zone
                        request.session['user_zone'] = officer.user_zone
                        return render(request, 'officer/RoofTop_Approver_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'RoofTop_Approver_WZ' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        user_zone = officer.user_zone
                        request.session['user_zone'] = officer.user_zone
                        return render(request, 'officer/RoofTop_Approver_base.html', {'data': officer})






                    elif officer.role.Role_Name == 'RoofTop_Viewer' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        user_zone = officer.user_zone
                        request.session['user_zone'] = officer.user_zone
                        return render(request, 'officer/RoofTop_Viewer_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'RoofTop_Viewer_EZ' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        request.session['user_zone'] = officer.user_zone
                        return render(request, 'officer/RoofTop_Viewer_base.html', {'data': officer})
                    
                    elif officer.role.Role_Name == 'RoofTop_Viewer_WZ' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone
                        user_zone = officer.user_zone
                        request.session['user_zone'] = officer.user_zone
                        return render(request, 'officer/RoofTop_Viewer_base.html', {'data': officer})
                   
                    elif officer.role.Role_Name == 'IT Cell' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'CA/ae_dashboard.html')


                   
                    elif officer.role.Role_Name == 'Finance Section' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'CA/fi_dashborad.html')
                        
                    elif officer.role.Role_Name == 'DISCOM' and officer.role.user_zone == 'CZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone 
                        return render(request, 'officer/discom_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'DISCOM_EZ' and officer.role.user_zone == 'EZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone 
                        return render(request, 'officer/discom_base.html', {'data': officer})

                    elif officer.role.Role_Name == 'DISCOM_WZ' and officer.role.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone 
                        return render(request, 'officer/discom_base.html', {'data': officer})  

                    elif officer.role.Role_Name == 'CGM Region' and str(officer.otp) == request.session['otp']:
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.employ_id
                        return render(request, 'officer/cgmr_base.html', {'data': officer})        

                    elif officer.role.Role_Name == 'PO_CREATER':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['employ_id'] = officer.employ_id
                        return render(request, 'po/po_creater/creater_base.html', {'officer': officer})
                    elif officer.role.Role_Name == 'PO_APPROVER':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['employ_id'] = officer.employ_id
                        return render(request, 'po/po_approver/approver_base.html', {'officer': officer})
 

                    elif officer.mobile == '94069 13401':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'CA/fi_dashborad.html')
                        
                    elif officer.role.Role_Name == 'WO_CREATER':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['employ_id'] = officer.employ_id
                        request.session['officer'] = officer.user_zone
                        return render(request, 'fqp/wo_creater/creater_base.html', {'officer': officer})
                    elif officer.role.Role_Name == 'WO_APPROVER':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['employ_id'] = officer.employ_id
                        request.session['officer'] = officer.user_zone
                        return render(request, 'fqp/wo_approver/approver_base.html', {'officer': officer})

                    elif officer.role.Role_Name == 'GM(Store)' and str(officer.otp) == request.session['otp']:
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.employ_id
                        request.session['store'] = AreaStore_Officer.objects.get(Officer=officer).AreaStore.id
                        return render(request, 'officer/gm_store_base.html', {'data': officer})  
                        
                        
                    elif officer.role.Role_Name == 'Nodal':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['employ_id'] = officer.employ_id
                        return render(request, 'fqp/nodal/nodal_base.html', {'officer': officer})
                    

# -------------created by shubham tripathi for finance section required for invoice------------------
                    elif officer.role.Role_Name == 'CFO' and officer.user_zone == 'CZ' or officer.role.Role_Name == 'CFO' and officer.user_zone == 'EZ' or officer.role.Role_Name == 'CFO' and officer.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'po/po_finance/pofinance_base.html',{"officer":officer})
                        
                    elif officer.role.Role_Name == 'DGM_CBPU' and officer.user_zone == 'CZ' or officer.role.Role_Name == 'DGM_CBPU' and officer.user_zone == 'EZ' or officer.role.Role_Name == 'DGM_CBPU' and officer.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone 
                        return render(request, 'po/po_finance/pofinance_base.html',{"officer":officer})

                    elif officer.role.Role_Name == 'AO_BILLS' and officer.user_zone == 'CZ' or officer.role.Role_Name == 'AO_BILLS' and officer.user_zone == 'EZ' or officer.role.Role_Name == 'AO_BILLS' and officer.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone 
                        return render(request, 'po/po_finance/pofinance_base.html',{"officer":officer})

                    elif officer.role.Role_Name == 'DGM_EM' and officer.user_zone == 'CZ' or officer.role.Role_Name == 'DGM_EM' and officer.user_zone == 'EZ' or officer.role.Role_Name == 'DGM_EM' and officer.user_zone == 'WZ':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['officer'] = officer.user_zone 
                        return render(request, 'po/po_finance/pofinance_base.html',{"officer":officer})
# -------------end here shubham tripathi for finance section required for invoice------------------ 

                    
                    elif officer.role.Role_Name == 'auditor':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        request.session['employ_id'] = officer.employ_id
                        return render(request, 'officer/auditor_base.html', {'officer': officer})

                elif InspectingOfficerInfo.objects.filter(Otp=request.session['otp']) & InspectingOfficerInfo.objects.filter(officer_employ_id=request.session['employ_login_id']): 
                    ins_officer = InspectingOfficerInfo.objects.get(officer_employ_id=request.session['employ_login_id'])
                    officer_id=ins_officer.id
                    pdi_data=PDI_Inspection_Info.objects.filter(officer=officer_id).distinct('offer_no')
                    return render(request, 'officer/inspection_officer.html', {'officer': ins_officer,"pdi_data":pdi_data}) 
                    
                messages.warning(
                    request, 'please login with right credentials ')
                redirect('mpeb_login')
    return render(request, 'main/mpeb_verify_otp.html')


def Finance_login(request):
    if request.method == 'POST':
        if User_Registration.objects.filter(user_name="finance"):
            if User_Registration.objects.filter(password="12345"):
                return render(request, 'main/userfinancebase.html')
            else:
                return render(request, 'main/finnance_officer_sign.html')
        return render(request, 'main/finnance_officer_sign.html')
    return render(request, 'main/finnance_officer_sign.html')


def wokring_login(request):
    if request.method == 'POST':
        if User_Registration.objects.filter(user_name="working"):
            if User_Registration.objects.filter(password="12345"):
                return render(request, 'main/user_wnp_base.html')
            else:
                return render(request, 'main/working_officer_sign.html')
        return render(request, 'main/working_officer_sign.html')
    return render(request, 'main/working_officer_sign.html')


def vendor_wnp_evaluate(request, id):
    data = User_Registration.objects.filter(User_Id=id)
    if data[0].User_type == "NABL":
        doc = NABL_Document.objects.filter(user_id=data[0].User_Id, Status=1)
        # Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
        # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)
        return render(request, 'officer/nabl_wnp_evaluate.html',
                      {'data': data[0], 'doc': doc})
    doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
    Factory = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
    Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
    return render(request, 'officer/vendor_wnp_evaluate.html',
                  {'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material})


def vendor_wnp_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = User_Registration.objects.filter(User_Id=id)
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
            # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)
            data = User_Registration.objects.filter(work_approval=0)
            counter = 100
            comment = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                data.Primary_verification_Date = datetime.datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status = 1
                else:
                    data.Primary_verification_Status = 2
                    data.Status = 0
                    test = data.Primary_remark_rejection_counter
                    test = test + 1
                    data.Primary_remark_rejection_counter = test
                data.save()
                counter = counter + 1
                comment = comment + 1
            data = NABL_Document.objects.filter(
                user_id=id).filter(Primary_verification_Status=2)
            if not data:
                data = User_Registration.objects.get(User_Id=id)
                data.work_approval = 1
                data.finance_approval = 1
                data.save()
            data = User_Registration.objects.filter(work_approval=0)
            return render(request, 'officer/work_pending_vendor.html', {'data': data})

    return redirect('/')


def work_pending_vendor(request):
    data = User_Registration.objects.filter(work_approval=0)
    return render(request, 'officer/work_pending_vendor.html', {'data': data})




# anupam
def vendor_cgm_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = User_Registration.objects.filter(User_Id=id)
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            usr_obj = User_Registration.objects.get(User_Id=id)
            comm = request.POST.get(str('remark'))
            doc.CGM_remark = comm
            result = request.POST.get(str('action'))
            if result == 'OK':
                data = User_Registration.objects.get(User_Id=id)
                vmaterial = Vendor_Material_Details.objects.filter(user_id=data.User_Id,Primary_verification_Status=1)
                for i in vmaterial:
                    i.new_status = 1
                    i.save()
                
                # send_mail(
                #     'Approval status of C.G.M ',
                #     'Hello ! Your application is approved by C.G.M',
                #     settings.EMAIL_HOST_USER,
                #     [data.Email_Id],
                #     fail_silently=False,
                # )
                from datetime import date
                User_Zone = usr_obj.User_zone
                User = usr_obj.User_type
                vendor_type = "00"
                nabl_type = "00"
                tkc_type = "00"
                today = date.today()
                date = today.strftime("%m%y")
                list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                s = ""
                if User_Zone == "CZ":
                    s = "CZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "TKC":
                        s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)

                if User_Zone == "EZ":
                    s = "EZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "TKC":
                        s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)

                if User_Zone == "WZ":
                    s = "WZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "TKC":
                        s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)

                data = User_Registration.objects.filter(User_Id=id)
                company_name = data[0].CompanyName_E
                issue_date = today.strftime("%d/%m/%Y")
                from datetime import datetime
                valid_upto = datetime(2024, 1, 11)
                valid_upto = valid_upto.strftime("%d/%m/%Y")
                data11 = User_Registration.objects.filter(User_Id=id)
               
                data11 = User_Registration.objects.get(User_Id=id)
                vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id,Primary_verification_Status=1)

                sms = User_Registration.objects.get(User_Id=id)
                mobile = sms.ContactNo
                name_sms = sms.CompanyName_E
                zone = sms.User_zone
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                # # for server set proxy
                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277221739526680&mobile_number=" + str(
                    mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('VENDOR') + "&v4=" + "MP" + str(zone) + "&v5=" + str(
                    'https://qcportal.mpcz.in/')
                    
                sms_template = message_template_log(template_id = '1007277221739526680',date = datetime.now(),mobile_number = mobile)
                sms_template.save()
                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

                # send_mail(
                #     'Approval status of CGM (QC) ',
                #     'Your application is finally approved by CGM(QC) and your registration number is ' + s,
                #     settings.EMAIL_HOST_USER,
                #     [data11.Email_Id],
                #     fail_silently=False,
                # )
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                td = datetime.datetime.now()
                officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                officer_mobile = officer.mobile
                def generateOTP():
                    OTP = ""
                    digits = "0123456789"
                    for i in range(6):
                        OTP += digits[math.floor(random.random() * 10)]
                    return OTP
                otptt = generateOTP()
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
                response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
                sms_template.save()
                request.session['otptt'] = otptt
                print("ggggggggg",otptt)
                request.session['officer_mobile'] = officer_mobile
                otp_ofcr = User_Registration.objects.filter(User_Id=id)
                otp_ofcr.update(Otp=otptt)

                usr_obj = User_Registration.objects.get(User_Id=id)
                otp = usr_obj.Otp

                return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})
                # return render(request, 'vendor/cert2.html', {'td':td,'vmaterial':vmaterial,'data': data[0], 'company_name': company_name, 'no': s, 'd1': valid_upto, 'd2': issue_date})

            else:
                data = User_Registration.objects.get(User_Id=id)
                data.cgm_approval = -1
                data.final_rejection = -1
                data.save()
                # send_mail(
                    # 'Rejection status of C.G.M (QC) ',
                    # 'Hello ! Your application is finally rejected by C.G.M (QC)',
                    # settings.EMAIL_HOST_USER,
                    # [data.Email_Id],
                    # fail_silently=False,
                # )
                data = User_Registration.objects.filter(work_approval=1, finance_approval=1, qc_approval=1, cgm_approval=0)
                return render(request, 'officer/cgm_pending_vendor.html', {'data': data})
    return redirect('/')

import datetime
import calendar
def officer_otp(request, id, otp):
    if request.method == "POST":
        # try:
        
        from datetime import date
        from datetime import time
        from datetime import datetime
        import datetime
        
        data_usr_obj = User_Registration.objects.get(User_Id=id)
        User_Zone = data_usr_obj.User_zone
        date_save = datetime.datetime.now()
        data_usr_obj.date_of_approved = date_save
        data_usr_obj.save

        if (data_usr_obj.upgrade == 1  or data_usr_obj.activation == 1) and data_usr_obj.User_type == 'TKC':
            tkc_obj = TKC_Payment.objects.get(id=data_usr_obj.Oyt)
            Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
            cmobile = data_usr_obj.ContactNo
            UCDM_obj = UserCompanyDataMain.objects.get(user_id_id=data_usr_obj)

            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            current_time = td.strftime("%H:%M:%S")
            company_name = data_usr_obj.CompanyName_E
            import calendar
            day = datetime.datetime.now().date()
            exp = TKC_Document.objects.get(user_id=data_usr_obj.User_Id, Types_of_Docs='Electrical License')
            expi_date = exp.Doc_expiry_date
        
            try:
                cert_det_obj = certificate_details.objects.get(User_Id=id)
                cert_det_obj.update(electic_liecense_date = expi_date)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(tkc_class_contractor = tkc_obj.Name)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(valid_upto = expi_date)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(day = day)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(current_time = current_time)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(User_Zone = User_Zone)
            except Exception as e:
                pass

            try:
                #t1 = str(data_usr_obj.Authentication_id)
                #t2 = "CZC" + t1 
                cert_det_obj.update(no = data_usr_obj.Authentication_id)
            except Exception as e:
                pass

            data_usr_obj11 = User_Registration.objects.filter(User_Id=id)
            data_usr_obj11.update(upgrade = 0)
            data_usr_obj11.update(activation = 0)
            data_usr_obj11.update(digital_cert_upload = 0)
            
            data_usr_obj33 = User_Registration.objects.get(User_Id=id)
            data_usr_obj33.cgm_approval = 1
            
            data_usr_obj22 = User_Registration.objects.get(User_Id=id)
            
            usr_obj = User_Registration.objects.get(User_Id=id)
            
            mat_list = []
            
            if User_Zone == "CZ":
                if certificate_details.objects.filter(User_Id=id).exists():
                    certificate_details_new = certificate_details.objects.filter(User_Id=id)
                    certificate_details_new.update(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                else:
                    cert_obj = certificate_details(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                    cert_obj.save()
                    
                return render(request, 'tkc/tkc_cert_cz.html',
                                        {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': data_usr_obj22,
                                        'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data_usr_obj22,
                                        'company_name': data_usr_obj22.CompanyName_E, 'no': data_usr_obj22.Authentication_id, 
                                        'day': day, 'valid_upto': expi_date,
                                        'User_Zone': data_usr_obj22.User_zone})
            elif User_Zone == "EZ":
                if certificate_details.objects.filter(User_Id=id).exists():
                    certificate_details_new = certificate_details.objects.filter(User_Id=id)
                    certificate_details_new.update(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                else:
                    cert_obj = certificate_details(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                    cert_obj.save()
                    
                return render(request, 'tkc/tkc_cert_ez.html',
                                        {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': data_usr_obj22,
                                        'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data_usr_obj22,
                                        'company_name': data_usr_obj22.CompanyName_E, 'no': data_usr_obj22.Authentication_id, 
                                        'day': day, 'valid_upto': expi_date,
                                        'User_Zone': data_usr_obj22.User_zone})
            elif User_Zone == "WZ":
                if certificate_details.objects.filter(User_Id=id).exists():
                    certificate_details_new = certificate_details.objects.filter(User_Id=id)
                    certificate_details_new.update(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                else:
                    cert_obj = certificate_details(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                    cert_obj.save()
                    
                return render(request, 'tkc/tkc_cert_wz.html',
                                        {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': data_usr_obj22,
                                        'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data_usr_obj22,
                                        'company_name': data_usr_obj22.CompanyName_E, 'no': data_usr_obj22.Authentication_id, 
                                        'day': day, 'valid_upto': expi_date,
                                        'User_Zone': data_usr_obj22.User_zone})
            else:
                pass
                
                
                
                
        if (data_usr_obj.add_material == 4) and data_usr_obj.User_type == 'VENDOR':
            Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
            cmobile = data_usr_obj.ContactNo
            UCDM_obj = UserCompanyDataMain.objects.get(user_id_id=data_usr_obj)

            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            current_time = td.strftime("%H:%M:%S")
            company_name = data_usr_obj.CompanyName_E
            import calendar
            day = datetime.datetime.now().date()
            usr_obj = User_Registration.objects.get(User_Id=id)
            from datetime import date
            User_Zone = usr_obj.User_zone
            User = usr_obj.User_type
            vendor_type = "00"
            nabl_type = "01"
            tkc_type = "02"
            today = date.today()
            date = today.strftime("%m%y")
            list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            s = ""
            expi_date = ""
            vmaterial = Vendor_Material_Details.objects.filter(user_id=usr_obj.User_Id,Primary_verification_Status=1,new_status=1)
        
            try:
                cert_det_obj = certificate_details.objects.get(User_Id=id)
                cert_det_obj.update(electic_liecense_date = expi_date)
            except Exception as e:
                pass
         
            try:
                cert_det_obj.update(valid_upto = expi_date)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(day = day)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(current_time = current_time)
            except Exception as e:
                pass
            try:
                cert_det_obj.update(User_Zone = User_Zone)
            except Exception as e:
                pass

            try:
                mat_list = []
                vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id,Primary_verification_Status=1,new_status=1)
                for i in vmaterial:
                    mat_list.append(i.Material_Specification)
                cert_det_obj.update(vmaterial=mat_list)
            except Exception as e:
                pass

            try:
                #t1 = str(data_usr_obj.Authentication_id)
                #t2 = "CZC" + t1 
                cert_det_obj.update(no = data_usr_obj.Authentication_id)
            except Exception as e:
                pass

            data_usr_obj11 = User_Registration.objects.filter(User_Id=id)
            data_usr_obj11.update(upgrade = 0)
            data_usr_obj11.update(activation = 0)
            data_usr_obj11.update(digital_cert_upload = 0)
            
            data_usr_obj33 = User_Registration.objects.get(User_Id=id)
            data_usr_obj33.cgm_approval = 1
            
            data_usr_obj22 = User_Registration.objects.get(User_Id=id)
            
            usr_obj = User_Registration.objects.get(User_Id=id)
            
            mat_list = []
            data = User_Registration.objects.filter(User_Id=id)
            import calendar
            day = datetime.datetime.now().date()
            three_year_delta = datetime.timedelta(days=1096 if ((day.month >= 3 and calendar.isleap(day.year + 3)) or (
                    day.month < 3 and calendar.isleap(day.year))) else 1095)
            valid_upto = day + three_year_delta
            
            if User_Zone == "CZ":
                if certificate_details.objects.filter(User_Id=id).exists():
                    mat_list = []
                    for i in vmaterial:
                        mat_list.append(i.Material_Specification)
                    new_material = certificate_details.objects.filter(User_Id=id)
                    new_material.update(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                else:
                    mat_list = []
                    for i in vmaterial:
                        mat_list.append(i.Material_Specification)
                    cert_obj = certificate_details(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                    cert_obj.save()
                data = User_Registration.objects.filter(User_Id=id)
                data.update(add_material=0)
                    
                return render(request, 'vendor/cert_cz.html',
                                        {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': vmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': usr_obj.Authentication_id, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})
            elif User_Zone == "EZ":
                if certificate_details.objects.filter(User_Id=id).exists():
                    mat_list = []
                    for i in vmaterial:
                        mat_list.append(i.Material_Specification)
                    new_material = certificate_details.objects.filter(User_Id=id)
                    new_material.update(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                else:
                    mat_list = []
                    for i in vmaterial:
                        mat_list.append(i.Material_Specification)
                    cert_obj = certificate_details(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                    cert_obj.save()
                data = User_Registration.objects.filter(User_Id=id)
                data.update(add_material=0)
                    
                return render(request, 'vendor/cert_ez.html',
                                        {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': vmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': usr_obj.Authentication_id, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})
            elif User_Zone == "WZ":
                if certificate_details.objects.filter(User_Id=id).exists():
                    mat_list = []
                    for i in vmaterial:
                        mat_list.append(i.Material_Specification)
                    new_material = certificate_details.objects.filter(User_Id=id)
                    new_material.update(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                else:
                    mat_list = []
                    for i in vmaterial:
                        mat_list.append(i.Material_Specification)
                    cert_obj = certificate_details(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E,
                                                        company_name=company_name,
                                                        Company_add_1=UCDM_obj.Company_add_1,
                                                        Company_add_2=UCDM_obj.Company_add_2,
                                                        Company_dist=UCDM_obj.Company_dist,
                                                        Company_state=UCDM_obj.Company_state,
                                                        Company_pin_code=UCDM_obj.Company_pin_code,
                                                        no = data_usr_obj22.Authentication_id, User_type=usr_obj.User_type,
                                                        vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                        employ_name=Officer_obj.employ_name,
                                                        designation=Officer_obj.designation, current_time=current_time,
                                                        tkc_class_contractor=tkc_obj.Name,
                                                        electic_liecense_date=expi_date, User_Zone=User_Zone)
                    cert_obj.save()
                data = User_Registration.objects.filter(User_Id=id)
                data.update(add_material=0)
                    
                return render(request, 'vendor/cert_wz.html',
                                        {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': vmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': usr_obj.Authentication_id, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})
            else:
                pass


        # except Exception as e:
        #     data = User_Registration.objects.filter(work_approval=1, finance_approval=1, cgm_approval=0)
        #     return render(request, 'officer/cgm_pending_tkc.html', {'data': data})
                
        if certificate_details.objects.filter(User_Id=id).exists():
            return HttpResponse("Certificate already generated. Please login and check the generated certificate on the dashboard")
        else:
            data = User_Registration.objects.filter(User_Id=id)
            officer_otp = request.POST.get('officer_otp')
            usr_obj = User_Registration.objects.get(User_Id=id)

            data = User_Registration.objects.filter(User_Id=id)
            company_name = data[0].CompanyName_E

            data111 = User_Registration.objects.get(User_Id=id)
            data111.cgm_approval = 1
            data111.save()
            cmobile = data111.ContactNo
            vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id,Primary_verification_Status=1,new_status=1)
            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            current_time = td.strftime("%H:%M:%S")
            UCDM_obj = UserCompanyDataMain.objects.get(user_id_id=data_usr_obj)

            #import datetime as datetime
            import calendar
            day = datetime.datetime.now().date()
            three_year_delta = datetime.timedelta(days=1096 if ((day.month >= 3 and calendar.isleap(day.year + 3)) or (
                    day.month < 3 and calendar.isleap(day.year))) else 1095)
            valid_upto = day + three_year_delta
            employ_login_id = request.session['employ_login_id']
            Officer_obj = Officer.objects.get(employ_login_id=employ_login_id)
            if officer_otp.strip() == ((usr_obj.Otp).strip()):
                from datetime import date
                User_Zone = usr_obj.User_zone
                User = usr_obj.User_type
                vendor_type = "00"
                nabl_type = "01"
                tkc_type = "02"
                today = date.today()
                date = today.strftime("%Y%m%d")
                list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                s = ""
                expi_date = ""
                tkc_class_contractor = ""
                if User_Zone == "CZ":
                    s = "CZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                        for i in vmaterial:
                            mat_list.append(i.Material_Specification)
                        cert_obj = certificate_details(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor="tkc_obj.Name",
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'vendor/cert_cz.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': vmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)

                        nabl_exp = NABL_Document.objects.get(user_id=data[0].User_Id,
                                                             Types_of_Docs='NABL Accreditation Certificate')
                        nabl_expi_date = nabl_exp.Doc_expiry_date

                        nabl_mat_list = []
                        nablmaterial = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
                        for i in nablmaterial:
                            nabl_mat_list.append(i.Material_Specification_Name)

                        cert_obj = certificate_details(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=nabl_mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor="tkc_obj.Name",
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone,
                                                       nabl_cert_exp=nabl_expi_date, nabl_cert_number=nabl_exp.Document_Name,
                                                       nabl_accredited_issue = nabl_exp.Doc_issue_date, 
                                                       nabl_accredited_expiry = nabl_exp.Doc_expiry_date)
                        cert_obj.save()
                        return render(request, 'vendor/cert_cz.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': nablmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': nabl_expi_date,
                                       'User_Zone': User_Zone, 'nabl_cert_number':nabl_exp.Document_Name,
                                       'nabl_accredited_issue' : nabl_exp.Doc_issue_date,
                                       'nabl_accredited_expiry' : nabl_exp.Doc_expiry_date})

                    elif User == "TKC":
                        Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
                        s = s + "C" + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        tkc_obj = TKC_Payment.objects.get(id=usr_obj.Oyt)
                        if User_Registration.objects.filter(Authentication_id=s).exists():
                            s = s + "C" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                            data11 = User_Registration.objects.filter(User_Id=id)
                            data11.update(Authentication_id=s)                            
                        else:
                            data11 = User_Registration.objects.filter(User_Id=id)
                            data11.update(Authentication_id=s)
                        exp = TKC_Document.objects.get(user_id=data[0].User_Id, Types_of_Docs='Electrical License')
                        expi_date = exp.Doc_expiry_date
                        mat_list = []
                        for i in vmaterial:
                            mat_list.append(i.Material_Name)
                        cert_obj = certificate_details(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E, 
                                                       company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor=tkc_obj.Name,
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'tkc/tkc_cert_cz.html',
                                      {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': usr_obj,
                                       'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': expi_date,
                                       'User_Zone': User_Zone})

                if User_Zone == "EZ":
                    s = "EZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                        for i in vmaterial:
                            mat_list.append(i.Material_Specification)
                        cert_obj = certificate_details(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor="tkc_obj.Name",
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'vendor/cert_ez.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': vmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)

                        nabl_exp = NABL_Document.objects.get(user_id=data[0].User_Id,
                                                             Types_of_Docs='NABL Accreditation Certificate')
                        nabl_expi_date = nabl_exp.Doc_expiry_date

                        nabl_mat_list = []
                        nablmaterial = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
                        for i in nablmaterial:
                            nabl_mat_list.append(i.Material_Specification_Name)

                        cert_obj = certificate_details(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=nabl_mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor="tkc_obj.Name",
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone,
                                                       nabl_cert_exp=nabl_expi_date, nabl_cert_number=nabl_exp.Document_Name,
                                                       nabl_accredited_issue = nabl_exp.Doc_issue_date, 
                                                       nabl_accredited_expiry = nabl_exp.Doc_expiry_date)
                        cert_obj.save()
                        return render(request, 'vendor/cert_ez.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': nablmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone, 'nabl_cert_number':nabl_exp.Document_Name,
                                       'nabl_accredited_issue' : nabl_exp.Doc_issue_date,
                                       'nabl_accredited_expiry' : nabl_exp.Doc_expiry_date})

                    elif User == "TKC":
                        Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
                        s = s + "C" + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        tkc_obj = TKC_Payment.objects.get(id=usr_obj.Oyt)
                        if User_Registration.objects.filter(Authentication_id=s).exists():
                            s = s + "C" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                            data11 = User_Registration.objects.filter(User_Id=id)
                            data11.update(Authentication_id=s)                            
                        else:
                            data11 = User_Registration.objects.filter(User_Id=id)
                            data11.update(Authentication_id=s)
                        exp = TKC_Document.objects.get(user_id=data[0].User_Id, Types_of_Docs='Electrical License')
                        expi_date = exp.Doc_expiry_date

                      
                        mat_list = []
                        for i in vmaterial:
                            mat_list.append(i.Material_Name)
                        cert_obj = certificate_details(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E, 
                                                       company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor=tkc_obj.Name,
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'tkc/tkc_cert_ez.html',
                                      {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': usr_obj,
                                       'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': expi_date,
                                       'User_Zone': User_Zone})

                if User_Zone == "WZ":
                    s = "WZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                        for i in vmaterial:
                            mat_list.append(i.Material_Specification)
                        cert_obj = certificate_details(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor="tkc_obj.Name",
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'vendor/cert_wz.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': vmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)

                        nabl_exp = NABL_Document.objects.get(user_id=data[0].User_Id,
                                                             Types_of_Docs='NABL Accreditation Certificate')
                        nabl_expi_date = nabl_exp.Doc_expiry_date

                        nabl_mat_list = []
                        nablmaterial = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
                        for i in nablmaterial:
                            nabl_mat_list.append(i.Material_Specification_Name)

                        cert_obj = certificate_details(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=nabl_mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor="tkc_obj.Name",
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone,
                                                       nabl_cert_exp=nabl_expi_date, nabl_cert_number=nabl_exp.Document_Name,
                                                       nabl_accredited_issue = nabl_exp.Doc_issue_date,
                                                       nabl_accredited_expiry = nabl_exp.Doc_expiry_date)
                        cert_obj.save()
                        return render(request, 'vendor/cert_wz.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'vmaterial': nablmaterial, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone, 'nabl_cert_number':nabl_exp.Document_Name,
                                       'nabl_accredited_issue' : nabl_exp.Doc_issue_date,
                                       'nabl_accredited_expiry' : nabl_exp.Doc_expiry_date})

                    elif User == "TKC":
                        Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])

                        s = s + "C" + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        tkc_obj = TKC_Payment.objects.get(id=usr_obj.Oyt)
                        if User_Registration.objects.filter(Authentication_id=s).exists():
                            s = s + "C" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                            data11 = User_Registration.objects.filter(User_Id=id)
                            data11.update(Authentication_id=s)                            
                        else:
                            data11 = User_Registration.objects.filter(User_Id=id)
                            data11.update(Authentication_id=s)
                        exp = TKC_Document.objects.get(user_id=data[0].User_Id, Types_of_Docs='Electrical License')
                        expi_date = exp.Doc_expiry_date
                        mat_list = []
                        for i in vmaterial:
                            mat_list.append(i.Material_Name)
                        cert_obj = certificate_details(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E,
                                                       company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_type,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       tkc_class_contractor=tkc_obj.Name,
                                                       electic_liecense_date=expi_date, User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'tkc/tkc_cert_wz.html',
                                      {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': usr_obj,
                                       'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': expi_date,
                                       'User_Zone': User_Zone})

            else:
                return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})
    else:
        return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})


def cert_all(request, reg_id):
    cert_obj = certificate_details.objects.get(no=reg_id)    
    User_Id = cert_obj.User_Id,
    Authorised_person_E = cert_obj.Authorised_person_E
    company_name = cert_obj.company_name
    Company_add_1 = cert_obj.Company_add_1
    Company_add_2 = cert_obj.Company_add_2
    Company_dist = cert_obj.Company_dist
    Company_state = cert_obj.Company_state
    Company_pin_code = cert_obj.Company_pin_code
    no = cert_obj.no
    User_type = cert_obj.User_type
    vmaterial = cert_obj.vmaterial

    day = cert_obj.day
    valid_upto = cert_obj.valid_upto
    employ_name = cert_obj.employ_name
    designation = cert_obj.designation
    current_time = cert_obj.current_time
    tkc_class_contractor = cert_obj.tkc_class_contractor
    electic_liecense_date = cert_obj.electic_liecense_date
    User_Zone = cert_obj.User_Zone
    nabl_exp_date = cert_obj.nabl_cert_exp
    nabl_cert_number = cert_obj.nabl_cert_number

    cert_u_obj = certificate_details.objects.get(no=reg_id)
 
    cert_u=cert_u_obj.vmaterial[1:len(cert_u_obj.vmaterial)-1]
    cert_list=cert_u.replace("'","").split(",")   

    return render(request, 'main/cert_all.html', {'Authorised_person_E':Authorised_person_E,'company_name': company_name, 
                                                  'Company_add_1': Company_add_1,
                                                  'Company_add_2': Company_add_2, 'Company_dist': Company_dist,
                                                  'Company_state': Company_state, 'Company_pin_code': Company_pin_code,
                                                  'no': reg_id, 'User_type': User_type, 'vmaterial': vmaterial,
                                                  'day': day, 'valid_upto': valid_upto,
                                                  'employ_name': employ_name, 'designation': designation,
                                                  'current_time': current_time,
                                                  'tkc_class_contractor': tkc_class_contractor,
                                                  'electic_liecense_date': electic_liecense_date,
                                                  'User_Zone': User_Zone, 'nabl_exp_date':nabl_exp_date,
                                                  'nabl_cert_number':nabl_cert_number, 
                                                  'cert_u_obj':cert_u_obj,'cert_list':cert_list})


def uplaod_cert(request, no):
    usr_obj1 = User_Registration.objects.get(Authentication_id=no)
    if request.method == "POST":
        if request.FILES['digitalCert']:
            filename = request.FILES['digitalCert']  
            cert_det_obj = certificate_details.objects.get(no=no)
            usr_obj = User_Registration.objects.get(Authentication_id=no)
            cert_det_obj.image = filename
            cert_det_obj.save()
            usr_obj.digital_cert_upload=1
            usr_obj.cert_image = filename
            usr_obj.save()

        if usr_obj1.User_type == 'TKC':
            return redirect('/digital_sign_cert/TKC')

        else:
            return redirect('/digital_sign_cert/VENDOR')

    else:
        return redirect('/digital_sign_cert/TKC')


def digital_sign_cert(request, user_type):
    if request.session.has_key('zone'):
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        if request.session['zone'] == 'WZ':
            if user_type == "TKC":
                usr_obj = User_Registration.objects.filter(officer_create=0,digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='WZ').order_by('User_Id')
                lst_oyt = []
                for i in usr_obj:
                    var_oyt = ""
                    if i.Oyt == '9':
                        var_oyt = "TKC"
                    elif i.Oyt == '8':
                        var_oyt = "A5"
                    elif i.Oyt == '7':
                        var_oyt = "A4"
                    elif i.Oyt == '6':
                        var_oyt = "A3"
                    elif i.Oyt == '5':
                        var_oyt = "A2 (with OYT)"
                    elif i.Oyt == '3':
                        var_oyt = "A1 (With OYT)"
                    elif i.Oyt == '1':
                        var_oyt = "B"
                    lst_oyt.append(var_oyt)
                final_list = zip(lst_oyt, usr_obj)
                return render(request, 'officer/digital_sign_cert_tkc.html', {'usr_obj':usr_obj,'final_list':final_list,'officer':officer})
               
            elif user_type == "VENDOR" or user_type == "NABL" :
                usr_obj = User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='WZ').order_by('User_Id')
                return render(request, 'officer/digital_sign_cert_nablVendor.html', {'usr_obj':usr_obj,'officer':officer})
            elif user_type == "RCA":
                usr_obj = Rca_User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type="VENDOR",User_zone='WZ').order_by('User_Id')
                return render(request, 'officer/digital_sign_cert_rca.html', {'usr_obj':usr_obj,'officer':officer})

        elif request.session['zone'] == 'CZ':
            if user_type == "TKC":
                usr_obj = User_Registration.objects.filter(officer_create=0,digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='CZ').order_by('User_Id')
                lst_oyt = []
                for i in usr_obj:
                    var_oyt = ""
                    if i.Oyt == '9':
                        var_oyt = "TKC"
                    elif i.Oyt == '8':
                        var_oyt = "A5"
                    elif i.Oyt == '7':
                        var_oyt = "A4"
                    elif i.Oyt == '6':
                        var_oyt = "A3"
                    elif i.Oyt == '5':
                        var_oyt = "A2 (with OYT)"
                    elif i.Oyt == '3':
                        var_oyt = "A1 (With OYT)"
                    elif i.Oyt == '1':
                        var_oyt = "B"
                    lst_oyt.append(var_oyt)
                final_list = zip(lst_oyt, usr_obj)
                return render(request, 'officer/digital_sign_cert_tkc.html', {'usr_obj':usr_obj,'final_list':final_list,'officer':officer})
            elif user_type == "VENDOR" or user_type == "NABL" :
                usr_obj = User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='CZ').order_by('User_Id')
                return render(request, 'officer/digital_sign_cert_nablVendor.html', {'usr_obj':usr_obj,'officer':officer})
            elif user_type == "RCA":
                usr_obj = Rca_User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type="VENDOR",User_zone='CZ').order_by('User_Id')
                return render(request, 'officer/digital_sign_cert_rca.html', {'usr_obj':usr_obj,'officer':officer})

        elif request.session['zone'] == 'EZ':
            if user_type == "TKC":
                usr_obj = User_Registration.objects.filter(officer_create=0,digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='EZ').order_by('User_Id')
                lst_oyt = []
                for i in usr_obj:
                    var_oyt = ""
                    if i.Oyt == '9':
                        var_oyt = "TKC"
                    elif i.Oyt == '8':
                        var_oyt = "A5"
                    elif i.Oyt == '7':
                        var_oyt = "A4"
                    elif i.Oyt == '6':
                        var_oyt = "A3"
                    elif i.Oyt == '5':
                        var_oyt = "A2 (with OYT)"
                    elif i.Oyt == '3':
                        var_oyt = "A1 (With OYT)"
                    elif i.Oyt == '1':
                        var_oyt = "B"
                    lst_oyt.append(var_oyt)
                final_list = zip(lst_oyt, usr_obj)
                return render(request, 'officer/digital_sign_cert_tkc.html', {'usr_obj':usr_obj,'final_list':final_list,'officer':officer})
            elif user_type == "VENDOR" or user_type == "NABL" :
                usr_obj = User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='EZ').order_by('User_Id')
                return render(request, 'officer/digital_sign_cert_nablVendor.html', {'usr_obj':usr_obj,'officer':officer})
            elif user_type == "RCA":
                usr_obj = Rca_User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type="VENDOR",User_zone='EZ').order_by('User_Id')
                return render(request, 'officer/digital_sign_cert_rca.html', {'usr_obj':usr_obj,'officer':officer})
    else:
        return redirect('/')

def cert_upload_download(request, id):
    var_show = "1"
    x1 = [""]
    usr_obj = User_Registration.objects.get(User_Id = id)
    try:
        if usr_obj.User_type == 'TKC':
            cert_u_obj = certificate_details.objects.get(User_Id=id)
            return render(request, 'officer/certificate_upload_download.html', {'vmat':x1,'cert_u_obj':cert_u_obj, 'var_show':var_show})
        elif usr_obj.User_type == 'NABL':
            cert_u_obj = certificate_details.objects.get(User_Id=id)
            str_vmat1 = str(cert_u_obj.vmaterial[2:-2])
            x1 = str_vmat1.split("', '")
            usr_obj = User_Registration.objects.get(User_Id = id)
            return render(request, 'officer/certificate_upload_download.html', {'vmaterial':x1,'cert_u_obj':cert_u_obj, 'var_show':var_show})
        elif usr_obj.User_type == 'VENDOR':
            cert_u_obj = certificate_details.objects.get(User_Id=id)
            str_vmat1 = cert_u_obj.vmaterial[2:-2]
            x1 = str_vmat1.split("', '")
            usr_obj = User_Registration.objects.get(User_Id = id)
            return render(request, 'officer/certificate_upload_download.html', {'vmaterial':x1,'cert_u_obj':cert_u_obj, 'var_show':var_show})
    except Exception as e:
        print("Exception is : ", e)
        return HttpResponse(e)

def certificate_submit(request, User_type):
    if User_type == "TKC":
        return render(request, 'officer/gmwdasbordbase.html')
    elif User_type == "NABL":
        return render(request, 'main/mpeb_base.html')
    elif User_type == "VENDOR":
        return render(request, 'main/mpeb_base.html')

def show_cert(request, Authentication_id):
    var_show = ""
    try:
        usr_obj = User_Registration.objects.get(Authentication_id = Authentication_id)
        if usr_obj.User_type == 'TKC':
            cert_u_obj = certificate_details.objects.get(User_Id=usr_obj.User_Id)
            return render(request, 'officer/certificate_upload_download.html', {'vmaterial':x1,'cert_u_obj':cert_u_obj, 'var_show':var_show})
        elif usr_obj.User_type == 'NABL':
            cert_u_obj = certificate_details.objects.get(User_Id=usr_obj.User_Id)
            str_vmat1 = str(cert_u_obj.vmaterial[2:-2])
            x1 = str_vmat1.split("', '")
            usr_obj = User_Registration.objects.get(User_Id = usr_obj.User_Id)
            return render(request, 'officer/certificate_upload_download.html', {'vmaterial':x1,'cert_u_obj':cert_u_obj, 'var_show':var_show})
        elif usr_obj.User_type == 'VENDOR':
            cert_u_obj = certificate_details.objects.get(User_Id=usr_obj.User_Id)
            str_vmat1 = cert_u_obj.vmaterial[2:-2]
            x1 = str_vmat1.split("', '")
            usr_obj = User_Registration.objects.get(User_Id = usr_obj.User_Id)
            return render(request, 'officer/certificate_upload_download.html', {'vmaterial':x1,'cert_u_obj':cert_u_obj, 'var_show':var_show})

    except Exception as e:
        return HttpResponse(e)


def show_digital_sign_cert_cgm(request, User_type):
    cert_u_obj = User_Registration.objects.filter(User_type=User_type, digital_cert_upload="1")
    return render(request, 'officer/show_digital_sign_cert_cgm.html', {'cert_u_obj':cert_u_obj, "User_type":User_type})


def vendor_cgm_evaluate_save1(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            import random
            from datetime import date
            import datetime
            User_Zone = "CZ"
            User = "NABL"
            vendor_type = "00"
            nabl_type = "00"
            tkc_type = "00"
            today = date.today()
            date = today.strftime("%m%y")

            list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            s = ""

            if User_Zone == "CZ":
                s = "CZ"
                if User == "Vendor":
                    s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
            data = User_Registration.objects.filter(User_Id=id)
            issue_date = today.strftime("%d/%m/%Y")

            valid_upto = datetime.datetime(2024, 1, 11)
            valid_upto = valid_upto.strftime("%d/%m/%Y")

            return render(request, 'nabl/cert2.html', {'data': data[0], 'no': s, 'd1': valid_upto, 'd2': issue_date})
        return render(request, 'nabl/cert2.html')
    return redirect('/')



def finance_base(request):
    return render(request, 'main/user_wnp_base.html')


def cgm_base(request):
    return render(request, 'officer/cgm_base.html')


def Test(request):
    return render(request, 'officer/index.html')


# ------------------------------------------------------------------------------------------

# def dgm_work_pending(request):
#     data = User_Registration.objects.filter(
#         work_approval=0, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/dgm_work_pending.html', {'data': data})


# def vendor_dgm_work_pending(request):
#     data = User_Registration.objects.filter(
#         work_approval=0, Complete_Details=1, User_type='VENDOR')
#     return render(request, 'officer/vendor_dgm_work_pending.html', {'data': data})


# def factory_initiate(request, id):
#     if request.method == 'POST':
#         data = User_Registration.objects.get(User_Id=id)
#         data.factory_approval_status = 1
#         data.save()
#         data = User_Registration.objects.filter(factory_approval=0, factory_approval_payment=1, User_type='VENDOR')
#         return render(request, 'officer/vendor_dgm_qc_pending.html', {'data': data})

# def factory_initiate(request):
#     data = User_Registration.objects.filter(
#         factory_approval=0, factory_approval_payment=1, User_type='VENDOR')
#     return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data})

def factory_initiate(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone='WZ').order_by('User_Id')
            return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone='CZ').order_by('User_Id')
            return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data})


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone='EZ').order_by('User_Id')
            return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data})
    return redirect('/')

def factory_inspection_initiate(request, id):
    data = User_Registration.objects.get(User_Id=id)
    c_add = UserCompanyDataMain.objects.get(user_id_id=data)
    c_name = data.CompanyName_E
    officer = InspectingOfficerInfo.objects.all()
    if request.method == 'POST':
        officer = request.POST.get('officer')
        officer = InspectingOfficerInfo.objects.get(id=officer)

        mobile = officer.contact_no
        name_sms = officer.officer_name
        oid = officer.officer_employ_id
        pws = officer.officer_password

        date = request.POST.get('date')
        import datetime
        today = datetime.datetime.now()
        data = User_Registration.objects.get(User_Id=id)
        assign_by_officer = request.session['employ_login_id']
        data1 = Factory_Inspection_Info(vendor=data, officer=officer, assign_date=today, execution_date=date,assigned_by = assign_by_officer)
        data1.save()
        data.factory_approval_status = 1
        data.save()
        vendor_con = data.ContactNo
        vendor_com = data.CompanyName_E
        zone = data.User_zone
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
        # for server set proxy
        # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007254789662546256&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(c_name) + "&v4=" + str() + "&v5=" + str(zone) + "&v6=" + str(date) + "&v7=" + str(oid) + "&v8=" + str(pws) + "&v9=" + str('https://shorturl.at/jkyJ8') + "&v10=" + str()
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007254789662546256',date = datetime.datetime.now(),mobile_number = mobile)
        sms_template.save()
        
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007363155209103912&mobile_number=" + str(
                            vendor_con) + "&v1=" + str(vendor_com) + "&v2=" + str() + "&v3=" + str() + "&v4=" + str(date)
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007363155209103912',date = datetime.datetime.now(),mobile_number = vendor_con)
        sms_template.save()
        data = User_Registration.objects.filter(
            factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR', User_zone=request.session['officer'])
        return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data, 'employee': officer})
    return render(request, 'officer/vendor_factory_inspection.html', {'data': data, 'c_add':c_add,'employee': officer})


# ------------------------------------------------------------------------------------------------------------

# def vendor_dgm_work_complete(request):
#     data = User_Registration.objects.filter(
#         work_approval=1, Complete_Details=1, User_type='VENDOR')
#     approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
#                                                                    User_type='VENDOR').count()
#     pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1,User_type='VENDOR').count()
#     total = approve + pending

#     return render(request, 'officer/vendor_dgm_work_complete.html', {'data': data,'total':total})


# def tkc_dgm_work_complete(request):
#     data = User_Registration.objects.filter(
#         work_approval=1, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/tkc_dgm_work_complete.html', {'data': data})


# def vendor_dgm_work_pending_resubmit(request):
#     data = User_Registration.objects.filter(
#         work_approval=2, Complete_Details=1, User_type='VENDOR')
#     return render(request, 'officer/vendor_dgm_work_pending_resubmit.html', {'data': data})


# def tkc_dgm_work_pending_resubmit(request):
#     data = User_Registration.objects.filter(
#         work_approval=2, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/tkc_dgm_work_pending_resubmit.html', {'data': data})

# ----------------------------------------------------------------------------------------------------------

def nabl_dgm_work_pending_resubmit(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(qc_approval=2, Complete_Details=1,User_type='NABL',User_zone='WZ')
            return render(request, 'officer/nabl_dgm_work_pending_resubmit.html', {'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(qc_approval=2, Complete_Details=1,User_type='NABL',User_zone='CZ')
            return render(request, 'officer/nabl_dgm_work_pending_resubmit.html', {'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(qc_approval=2, Complete_Details=1,User_type='NABL',User_zone='EZ')
            return render(request, 'officer/nabl_dgm_work_pending_resubmit.html', {'data': data})



    return redirect('/')


# -poornima change niche side count show 13april---------------------------------------------------------------------------------------------------------


# def dgm_work_evaluate_save(request, id):
#     if request.method == 'POST':
#         data = User_Registration.objects.filter(User_Id=id)
#         if data[0].User_type == "TKC":
#             doc = TKC_Document.objects.filter(
#                 user_id=data[0].User_Id, Approval_doc=1)
#             counter = 100
#             comment = 0
#             nz = 0
#             for data in doc:
#                 comm = request.POST.get(str(comment))
#                 result = request.POST.get(str(counter))
#                 if comm != '':
#                     data.Primary_remark = comm
#                 data.Primary_verification_Date = datetime.now().date()
#                 if result == 'OK':
#                     data.Primary_verification_Status = 1
#                 elif result == 'NOT':
#                     nz = 1
#                     user = User_Registration.objects.get(User_Id=id)
#                     user.work_approval = 2
#                     user.save()
#                     data.Primary_verification_Status = 2
#                     data.Status = 0
#                     nameee = data.Types_of_Docs
#                     sms = User_Registration.objects.get(User_Id=id)
#                     mobile = sms.ContactNo
#                     name_sms = sms.CompanyName_E
#                     header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                     # proxyDict = {"http" : "proxy.mpcz.in:8000"}
#                     # for server set proxy
#                     # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#                     # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
#                     #     mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
#                     #     nameee) + "&v4=" + str() + "&v5=" + str(
#                     #     'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(works)') + "&v9=" + str(
#                     #     'https://qcportal.mpcz.in/')
#                     # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
#                     test = data.Primary_remark_rejection_counter
#                     test = test + 1
#                     data.Primary_remark_rejection_counter = test
#                     if test >= 3:
#                         user.final_rejection = 1
#                         user.work_approval = -1
#                         send_mail(
#                             'Approval status of DGM(Works) ',
#                             'Hello ! Your application is finally rejected by DGM (Works) now.',
#                             settings.EMAIL_HOST_USER,
#                             [user.Email_Id],
#                             fail_silently=False,
#                         )
#                     user.save()

#                 data.save()
#                 counter = counter + 1
#                 comment = comment + 1
#             data = TKC_Document.objects.filter(
#                 user_id=id).filter(Primary_verification_Status=2)
#             # if nz == 1:
#             #     # send_mail(
#             #     #     'Approval status of DGM(Works) ',
#             #     #     'Hello ! Your are not approved by DGM (Works)',
#             #     #     settings.EMAIL_HOST_USER,
#             #     #     [user.Email_Id],
#             #     #     fail_silently=False,
#             #     # )
#             # else:
#             #     pass

#             if not data:
#                 data = User_Registration.objects.get(User_Id=id)
#                 data.work_approval = 1
#                 data.save()
#                 send_mail(
#                     'Approval status of DGM(Works) ',
#                     'Hello ! Your are approved by DGM (Works)',
#                     settings.EMAIL_HOST_USER,
#                     [data.Email_Id],
#                     fail_silently=False,
#                 )
#             data = User_Registration.objects.filter(
#                 work_approval=0, Complete_Details=1, User_type='TKC')
#             return render(request, 'officer/dgm_work_pending.html',
#                           {'data': data, 'doc': doc})
#         if data[0].User_type == "VENDOR":
#             doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
#             counter = 100
#             comment = 0
#             for data in doc:
#                 comm = request.POST.get(str(comment))
#                 result = request.POST.get(str(counter))
#                 if comm != '':
#                     data.Primary_remark = comm
#                 data.Primary_verification_Date = datetime.now().date()
#                 if result == 'OK':
#                     data.Primary_verification_Status = 1
#                 else:
#                     user = User_Registration.objects.get(User_Id=id)
#                     user.work_approval = 2
#                     data.Primary_verification_Status = 2
#                     data.Status = 0
#                     nameee = data.Types_of_Docs
#                     sms = User_Registration.objects.get(User_Id=id)
#                     mobile = sms.ContactNo
#                     name_sms = sms.CompanyName_E
#                     header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                     # proxyDict = {"http" : "proxy.mpcz.in:8000"}
#                     # for server set proxy
#                     # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#                     # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
#                     #     mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
#                     #     nameee) + "&v4=" + str() + "&v5=" + str(
#                     #     'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(works)') + "&v9=" + str(
#                     #     'https://qcportal.mpcz.in/')
#                     # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

#                     send_mail(
#                         'Approval status of DGM(Works) ',
#                         'Hello ! Your are not approved by DGM (Works)',
#                         settings.EMAIL_HOST_USER,
#                         [user.Email_Id],
#                         fail_silently=False,
#                     )

#                     test = data.Primary_remark_rejection_counter
#                     if test >= 3:
#                         user.final_rejection = 1
#                         user.work_approval = -1
#                         send_mail(
#                             'Approval status of DGM(Works) ',
#                             'Hello ! Your application is finally rejected by DGM (Works) now.',
#                             settings.EMAIL_HOST_USER,
#                             [user.Email_Id],
#                             fail_silently=False,
#                         )
#                     user.save()
#                     test = test + 1
#                     data.Primary_remark_rejection_counter = test
#                 data.save()
#                 counter = counter + 1
#                 comment = comment + 1
#             data = Vendor_Document.objects.filter(
#                 user_id=id).filter(Primary_verification_Status=2)
#             if not data:
#                 data = User_Registration.objects.get(User_Id=id)
#                 data.work_approval = 1
#                 data.save()
#                 # send_mail(
#                 #     'Approval status of DGM(Works) ',
#                 #     'Hello ! Your are approved by DGM (Works)',
#                 #     settings.EMAIL_HOST_USER,
#                 #     [data.Email_Id],
#                 #     fail_silently=False,
#                 # )
#                 if data.finance_approval == 1:
#                     send_mail(
#                         'Approved Profile ',
#                         'Hello ! Your profile approved make payment for FI',
#                         settings.EMAIL_HOST_USER,
#                         [data.Email_Id],
#                         fail_silently=False,
#                     )
#                 sms = User_Registration.objects.get(User_Id=id)
#                 mobile = sms.ContactNo
#                 name_sms = sms.CompanyName_E
#                 # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                 # # proxyDict = {"http" : "proxy.mpcz.in:8000"}
#                 # # for server set proxy
#                 # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#                 # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007180239560227172&mobile_number=" + str(
#                 #     mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
#                 #     'https://qcportal.mpcz.in/') + "&v4=" + str('10000')
#                 # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

#             data = User_Registration.objects.filter(
#                 work_approval=0, Complete_Details=1, User_type='VENDOR')
#             return redirect('vendor_dgm_work_pending')
#     data = User_Registration.objects.filter(
#         work_approval=0, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/dgm_work_pending.html', {'data': data})


# ----------------------------------------------------------------------------------------------------------

# def dgm_finance_pending(request):
#     data = User_Registration.objects.filter(
#         finance_approval=0, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/dgm_finance_pending.html', {'data': data})


# def dgm_finance_complete_tkc(request):
#     data = User_Registration.objects.filter(
#         finance_approval=1, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/dgm_finance_complete_tkc.html', {'data': data})


# def dgm_finance_all_tkc(request):
#     data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/dgm_finance_all.html', {'data': data})

# def vendor_dgm_finance_pending_rejection_tkc(request):
#     data = User_Registration.objects.filter(
#         finance_approval=2, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/vendor_dgm_finance_pending_rejection_tkc.html', {'data': data})


# def vendor_dgm_finance_pending_rejection_vendor(request):
#     data = User_Registration.objects.filter(
#         finance_approval=2, Complete_Details=1, User_type='VENDOR')
#     return render(request, 'officer/vendor_dgm_finance_pending_rejection_vendor.html', {'data': data})


# def vendor_dgm_finance_pending(request):
#     data = User_Registration.objects.filter(
#         finance_approval=0, Complete_Details=1, User_type='VENDOR')
#     return render(request, 'officer/dgm_finance_pending.html', {'data': data})


# def vendor_dgm_finance_complate(request):
#     data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1,
#                                             User_type='VENDOR') | User_Registration.objects.filter(finance_approval=2,
#                                                                                                    Complete_Details=1,
#                                                                                                    User_type='VENDOR')
#     return render(request, 'officer/dgm_finance_complete.html', {'data': data})


# def vendor_dgm_finance_all(request):
#     data = User_Registration.objects.filter(Complete_Details=1,
#                                             User_type='VENDOR') | User_Registration.objects.filter(finance_approval=2,
#                                                                                                    Complete_Details=1,
#                                                                                                    User_type='VENDOR')
#     return render(request, 'officer/dgm_finance_total.html', {'data': data})

# ----------------------------------------------------------------------------------------------------------


def vendor_dgm_finance_pending_rejection(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(
            finance_approval=2, Complete_Details=1, User_type='VENDOR')
        return render(request, 'officer/vendor_dgm_finance_pending_rejection.html', {'data': data})

    return redirect('/')

def vendor_dgm_finance_total_approved(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(
            finance_approval=1, Complete_Details=1, User_type='VENDOR')
        return render(request, 'officer/vendor_dgm_finance_total_approved.html', {'data': data})
    return redirect('/')



# change by poo

# def dgm_finance_evaluate(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "VENDOR":
#         # doc2 = Vendor_Document.objects.filter(user_id=data[0].User_Id)
#         # doc = Vendor_Turnover.objects.filter(user_id=data[0].User_Id)
#         doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
#         no_preview_path = os.getcwd() + "/media/documents/No_Preview.pdf"
#         try:
#             for i in doc1:
#                 if i.Ddocfile.url == "":
#                     abc = i.update(Balance_Sheet=no_preview_path)
#                     abc.save()
#         except Exception as e:
#             pass
#         return render(request, 'officer/vendor_dgm_finance_evaluate.html',
#                       {'doc1': doc1, 'data': data[0]})
#     if data[0].User_type == "TKC":
#         doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
#         doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
#         return render(request, 'officer/dgm_finance_evaluate.html',
#                       {'data': data[0], 'doc': doc, 'doc1': doc1})


# def dgm_finance_evaluate_save(request, id):
#     if request.method == 'POST':
#         data = User_Registration.objects.filter(User_Id=id)
#         if data[0].User_type == "TKC":
#             doc = TKC_Document.objects.filter(
#                 user_id=data[0].User_Id, Approval_doc=2)
#             counter = 100
#             comment = 0
#             nn = 0
#             for data in doc:
#                 comm = request.POST.get(str(comment))
#                 result = request.POST.get(str(counter))
#                 if comm != '':
#                     data.Primary_remark = comm
#                 data.Primary_verification_Date = datetime.now().date()
#                 if result == 'OK':
#                     data.Primary_verification_Status = 1
#                 elif result == 'NOT':
#                     nn = 1
#                     user = User_Registration.objects.get(User_Id=id)
#                     user.finance_approval = 2
#                     user.save()
#                     data.Primary_verification_Status = 2
#                     data.Status = 0
#                     test = data.Primary_remark_rejection_counter
#                     # nameee = data.document_name
#                     sms = User_Registration.objects.get(User_Id=id)
#                     mobile = sms.ContactNo
#                     name_sms = sms.CompanyName_E
#                     header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                     # proxyDict = {"http" : "proxy.mpcz.in:8000"}
#                     # for server set proxy
#                     proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#                     # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
#                     # mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
#                     # nameee) + "&v4=" + str() + "&v5=" + str(
#                     # 'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(finance)') + "&v9=" + str(
#                     # 'https://qcportal.mpcz.in/')
#                     # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

#                     if test >= 3:
#                         user.final_rejection = 1
#                         user.finance_approval = -1
#                         # send_mail(
#                         #     'Approval status of DGM(Finance) ',
#                         #     'Hello ! Your application is finally rejected by DGM (Finance) now',
#                         #     settings.EMAIL_HOST_USER,
#                         #     [user.Email_Id],
#                         #     fail_silently=False,
#                         # )
#                     user.save()
#                     test = test + 1
#                     data.Primary_remark_rejection_counter = test
#                 data.save()
#                 counter = counter + 1
#                 comment = comment + 1
#             data = TKC_Document.objects.filter(
#                 user_id=id).filter(Primary_verification_Status=2, Approval_doc=2)
#             # if nn == 1:
#             #     # send_mail(
#             #     #     'Rejection status of DGM(Finance) ',
#             #     #     'Hello ! Your application is not approved by DGM (Finance).',
#             #     #     settings.EMAIL_HOST_USER,
#             #     #     [user.Email_Id],
#             #     #     fail_silently=False,
#             #     # )
#             # else:
#             #     pass
#             if not data:
#                 data = User_Registration.objects.get(User_Id=id)
#                 data.finance_approval = 1
#                 data.save()
#                 # send_mail(
#                 #     'Approval status of DGM(Finance) ',
#                 #     'Hello ! Your application is approved by DGM (Finance).',
#                 #     settings.EMAIL_HOST_USER,
#                 #     [data.Email_Id],
#                 #     fail_silently=False,
#                 # )

#             data = User_Registration.objects.filter(
#                 finance_approval=0, Complete_Details=1, User_type='TKC')
#             return render(request, 'officer/dgm_finance_pending.html', {'data': data})
#         if data[0].User_type == "VENDOR":
#             doc = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
#             counter = 100
#             comment = 0
#             for data in doc:
#                 comm = request.POST.get(str(comment))
#                 result = request.POST.get(str(counter))
#                 if comm != '':
#                     data.Primary_remark = comm
#                 data.Primary_verification_Date = datetime.now().date()
#                 if result == 'OK':
#                     data.Primary_verification_Status = 1
#                 else:
#                     user = User_Registration.objects.get(User_Id=id)
#                     user.finance_approval = 2
#                     data.Primary_verification_Status = 2
#                     data.Status = 0
#                     nameee = data.document_name
#                     sms = User_Registration.objects.get(User_Id=id)
#                     mobile = sms.ContactNo
#                     name_sms = sms.CompanyName_E
#                     header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                     # proxyDict = {"http" : "proxy.mpcz.in:8000"}
#                     # for server set proxy
#                     proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#                     url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
#                         mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
#                         nameee) + "&v4=" + str() + "&v5=" + str(
#                         'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(finance)') + "&v9=" + str(
#                         'https://qcportal.mpcz.in/')
#                     response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

#                     # send_mail(
#                     #     'Rejection status of DGM(Finance) ',
#                     #     'Hello ! Your are not approved by DGM (Finance)',
#                     #     settings.EMAIL_HOST_USER,
#                     #     [user.Email_Id],
#                     #     fail_silently=False,
#                     # )
#                     test = data.Primary_remark_rejection_counter
#                     if test >= 3:
#                         user.final_rejection = 1
#                         user.finance_approval = -1
#                         # send_mail(
#                         #     'Rejection status of DGM(Finance) ',
#                         #     'Hello ! Your application is finally rejected by DGM (Finance) now',
#                         #     settings.EMAIL_HOST_USER,
#                         #     [user.Email_Id],
#                         #     fail_silently=False,
#                         # )
#                     user.save()
#                     test = test + 1
#                     data.Primary_remark_rejection_counter = test
#                 data.save()
#                 counter = counter + 1
#                 comment = comment + 1
#             data = Vendor_BalanceSheet.objects.filter(
#                 user_id=id).filter(Primary_verification_Status=2)
#             if not data:
#                 data = User_Registration.objects.get(User_Id=id)
#                 data.finance_approval = 1
#                 data.save()
#                 # send_mail(
#                 #     'Approval status of DGM(Finance) ',
#                 #     'Hello ! You are approved by DGM (Finance)',
#                 #     settings.EMAIL_HOST_USER,
#                 #     [data.Email_Id],
#                 #     fail_silently=False,
#                 # )
#                 if data.work_approval == 1:
#                     send_mail(
#                         'Approved Profile ',
#                         'Hello ! Your profile approved make payment for FI',
#                         settings.EMAIL_HOST_USER,
#                         [data.Email_Id],
#                         fail_silently=False,
#                     )
#                 sms = User_Registration.objects.get(User_Id=id)
#                 mobile = sms.ContactNo
#                 name_sms = sms.CompanyName_E
#                 header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                 # proxyDict = {"http" : "proxy.mpcz.in:8000"}
#                 # for server set proxy
#                 # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

#                 # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007180239560227172&mobile_number=" + str(
#                 #     mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
#                 #     'https://qcportal.mpcz.in/') + "&v4=" + str('10000')
#                 # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

#             data = User_Registration.objects.filter(
#                 finance_approval=0, Complete_Details=1, User_type='VENDOR')
#             return render(request, 'officer/dgm_finance_pending.html', {'data': data})
#     data = User_Registration.objects.filter(
#         finance_approval=0, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/dgm_finance_pending.html', {'data': data})


# *************************** Dgm qc ***************************88
def dgm_qc_pending(request):
    data = User_Registration.objects.filter(
        qc_approval=0, Complete_Details=1, User_type='TKC')
    return render(request, 'officer/dgm_qc_pending.html', {'data': data})


def vendor_dgm_qc_pending(request):
    data = User_Registration.objects.filter(
        work_approval=1, finance_approval=1, User_type='VENDOR')
    return render(request, 'officer/vendor_dgm_qc_pending.html', {'data': data})


def dgm_qc_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        if data[0].User_type == "VENDOR":
            doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            return render(request, 'officer/vendor_dgm_qc_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1})
        if data[0].User_type == "TKC":
            doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1)
            return render(request, 'officer/dgm_qc_evaluate.html',
                        {'data': data[0], 'doc': doc})
    return redirect('/')


def dgm_qc_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = User_Registration.objects.filter(User_Id=id)
            if data[0].User_type == "TKC":
                doc = TKC_Document.objects.filter(
                    user_id=data[0].User_Id, Approval_doc=1)
                counter = 100
                comment = 0
                for data in doc:
                    comm = request.POST.get(str(comment))
                    result = request.POST.get(str(counter))
                    if comm != '':
                        data.Primary_remark = comm

                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    data.Primary_verification_Date = datetime.datetime.now()
                    if result == 'OK':
                        data.Primary_verification_Status = 1
                    else:
                        data.Primary_verification_Status = 2
                        data.Status = 0
                        test = data.Primary_remark_rejection_counter
                        test = test + 1
                        data.Primary_remark_rejection_counter = test
                    data.save()
                    counter = counter + 1
                    comment = comment + 1
                data = TKC_Document.objects.filter(
                    user_id=id).filter(Primary_verification_Status=2)
                if not data:
                    data = User_Registration.objects.get(User_Id=id)
                    data.qc_approval = 1
                    data.save()
                data = User_Registration.objects.filter(qc_approval=0)
                return render(request, 'officer/dgm_qc_evaluate.html',
                            {'data': data[0], 'doc': doc})

            if data[0].User_type == "VENDOR":
                doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
                counter = 100
                comment = 0
                for data in doc:
                    comm = request.POST.get(str(comment))
                    result = request.POST.get(str(counter))
                    if comm != '':
                        data.Primary_remark = comm
                    data.Primary_verification_Date = datetime.datetime.now()
                    if result == 'OK':
                        data.Primary_verification_Status = 1
                    else:
                        user = User_Registration.objects.get(User_Id=id)
                        user.qc_approval = 2

                        data.Primary_verification_Status = 2
                        data.Status = 0
                        test = data.Primary_remark_rejection_counter
                        if test >= 8:
                            user.final_rejection = 1
                            user.qc_approval = -1
                        user.save()
                        test = test + 1
                        data.Primary_remark_rejection_counter = test
                    data.save()
                    counter = counter + 1
                    comment = comment + 1
                data = Vendor_Document.objects.filter(
                    user_id=id).filter(Primary_verification_Status=2)
                if not data:
                    data = User_Registration.objects.get(User_Id=id)
                    data.qc_approval = 1
                    data.save()
                data = User_Registration.objects.filter(
                    qc_approval=0, Complete_Details=1, User_type='VENDOR')
                return render(request, 'officer/dgm_qc_pending.html', {'data': data})

            data = User_Registration.objects.filter(
                qc_approval=0, Complete_Details=1, User_type='TKC')
            return render(request, 'officer/dgm_qc_pending.html', {'data': data})
    return redirect('/')


class PasswordForgetView(FormView):
    template_name = "main/forgot-password.html"
    form_class = PasswordForgotForm
    success_url = "/mail_sent"

    # forms=PasswordForgotForm()
    def form_valid(self, form):
        a = "http://127.0.0.1:8000"
        email = form.cleaned_data.get("email")

        customer = User_Registration.objects.get(Email_Id=email)
        user = customer
        url = self.request.META['HTTP_HOST']

        text_content = 'Please Click the link below to reset your password.  '
        html_content = a + "/password-reset/" + email + \
                       "/" + password_reset_token.make_token(user) + "/"
        # send_mail(
        #     'Contact Number Reset Link | MPMKVVCL',
        #     text_content +
        #     html_content,
        #     settings.EMAIL_HOST_USER,
        #     [email],
        #     fail_silently=False,
        # )
        return super().form_valid(form)


def msgsent(request):
    return render(request, 'main/sentmail.html')


class PasswordResetView(FormView):
    template_name = "main/reset-password.html"
    form_class = PasswordResetForm
    success_url = "/login"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User_Registration.objects.get(Email_Id=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return HttpResponse("something is worng")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User_Registration.objects.get(Email_Id=email)
        user.ContactNo = password
        user.save()
        return super().form_valid(form)


def vendor(request):
    User_Zone = "CZ"
    User = "VENDOR"
    vendor_type = "00"
    nabl_type = "00"
    tkc_type = "00"
    today = date.today()
    date = today.strftime("%m%y")
    list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    s = ""
    if User_Zone == "CZ":
        s = "CZ"
        if User == "VENDOR":
            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                list1) + random.choice(list1)
        elif User == "NABL":
            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                list1) + random.choice(list1)
        elif User == "TKC":
            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                list1) + random.choice(list1)

    data = User_Registration.objects.filter(User_Id=id)
    issue_date = today.strftime("%d/%m/%Y")

    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    valid_upto = datetime.datetime(2024, 1, 11)
    valid_upto = valid_upto.strftime("%d/%m/%Y")
    return render(request, 'vendor/cert2.html', {'data': data[0], 'no': s, 'd1': valid_upto, 'd2': issue_date})


def cert_vendor(request, id):
    User_Zone = "CZ"
    vendor_type = "00"
    date = time.strftime("%Y%m%d")
    list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    reg_no = ""

    if User_Zone == "CZ":
        reg_no = "CZ"
        reg_no = reg_no + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
            list1) + random.choice(list1)
    elif User_Zone == "CZ":
        reg_no = "CZ"
        reg_no = reg_no + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
            list1) + random.choice(list1)
    elif User_Zone == "CZ":
        reg_no = "CZ"
        reg_no = reg_no + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
            list1) + random.choice(list1)

    # company_name for certificates
    # zone
    # save reg no generate
    data = User_Registration.objects.filter(User_Id=id)
    material = Vendor_Material_Details.objects.filter(user_id=id,Primary_verification_Status=1,new_status=1)
    data.update(Authentication_id=reg_no)
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    td = datetime.datetime.now()
    return render(request, 'main/cert_vendor.html', {'td': td, 'no': reg_no, 'data': data[0], 'material': material})


def vendor_cgm_evaluate_view(request, id):
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
                if data_new.upgrade_payment == 1:
                    type_upgrate = TKC_Payment.objects.get(id=data[0].Upgrade_Oyt)
                else:
                    type_upgrate = TKC_Payment.objects.get(id=data[0].Oyt)
                return render(request, 'officer/vendor_cgm_evaluate_view.html',
                            {'data': data[0],'officer':officer,'doc': doc, 'doc1': doc1,'type_upgrate':type_upgrate,'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})

            elif doc[0].new_data == 0:
                return render(request, 'officer/vendor_cgm_evaluate_view.html',
                            {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})


    return redirect('/')


def tkc_total(request):
    if request.session.has_key('employ_login_id'):
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',cgm_approval=1,User_zone='WZ')
            return render(request, 'officer/tkc_total_vendor.html', {'data': data,'officer':officer})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',cgm_approval=1,User_zone='CZ')
            return render(request, 'officer/tkc_total_vendor.html', {'data': data,'officer':officer})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',cgm_approval=1,User_zone='EZ')
            return render(request, 'officer/tkc_total_vendor.html', {'data': data,'officer':officer})

        
    return redirect('/')


   
def search_contractor(request):
     if request.session.has_key('employ_login_id'):
        if request.method == 'GET':
            search = request.GET.get('search')
            data = User_Registration.objects.filter(Q(Authorised_person_E__icontains=search) | Q(CompanyName_E__icontains=search) | Q(
                ContactNo__icontains=search))
            paginator = Paginator(data,500, orphans=1)
            page_no = request.GET.get('page')
            page_obj = paginator.get_page(page_no)
            return render(request, 'officer/tkc_total_vendor.html', {'data': page_obj})
     return redirect('/')


def cgm_rejected_tkc(request):
    if request.session.has_key('employ_login_id'):
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, cgm_approval=2, User_type='TKC',User_zone='WZ')
            lst_oyt = []
            lst_upgrade_oyt = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)
            
            for j in data:
                var_Upgrade_Oyt = ""
                if j.Upgrade_Oyt == '9':
                    var_Upgrade_Oyt = "TKC"
                elif j.Upgrade_Oyt == '8':
                    var_Upgrade_Oyt = "A5"
                elif j.Upgrade_Oyt == '7':
                    var_Upgrade_Oyt = "A4"
                elif j.Upgrade_Oyt == '6':
                    var_Upgrade_Oyt = "A3"
                elif j.Upgrade_Oyt == '5':
                    var_Upgrade_Oyt = "A2 (with OYT)"
                elif j.Upgrade_Oyt == '3':
                    var_Upgrade_Oyt = "A1 (With OYT)"
                elif j.Upgrade_Oyt == '1':
                    var_Upgrade_Oyt = "B"
                lst_upgrade_oyt.append(var_Upgrade_Oyt)

            final_lst = zip(lst_upgrade_oyt,lst_oyt, data)


            return render(request, 'officer/cgm_rejected_tkc.html', {'data': data,'final_lst':final_lst,'officer':officer})



        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, cgm_approval=2, User_type='TKC',User_zone='CZ')
            lst_oyt = []
            lst_upgrade_oyt = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)
            
            for j in data:
                var_Upgrade_Oyt = ""
                if j.Upgrade_Oyt == '9':
                    var_Upgrade_Oyt = "TKC"
                elif j.Upgrade_Oyt == '8':
                    var_Upgrade_Oyt = "A5"
                elif j.Upgrade_Oyt == '7':
                    var_Upgrade_Oyt = "A4"
                elif j.Upgrade_Oyt == '6':
                    var_Upgrade_Oyt = "A3"
                elif j.Upgrade_Oyt == '5':
                    var_Upgrade_Oyt = "A2 (with OYT)"
                elif j.Upgrade_Oyt == '3':
                    var_Upgrade_Oyt = "A1 (With OYT)"
                elif j.Upgrade_Oyt == '1':
                    var_Upgrade_Oyt = "B"
                lst_upgrade_oyt.append(var_Upgrade_Oyt)

            final_lst = zip(lst_upgrade_oyt,lst_oyt, data)


            return render(request, 'officer/cgm_rejected_tkc.html', {'data': data,'final_lst':final_lst,'officer':officer})


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, cgm_approval=2, User_type='TKC',User_zone='EZ')
            lst_oyt = []
            lst_upgrade_oyt = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)
            
            for j in data:
                var_Upgrade_Oyt = ""
                if j.Upgrade_Oyt == '9':
                    var_Upgrade_Oyt = "TKC"
                elif j.Upgrade_Oyt == '8':
                    var_Upgrade_Oyt = "A5"
                elif j.Upgrade_Oyt == '7':
                    var_Upgrade_Oyt = "A4"
                elif j.Upgrade_Oyt == '6':
                    var_Upgrade_Oyt = "A3"
                elif j.Upgrade_Oyt == '5':
                    var_Upgrade_Oyt = "A2 (with OYT)"
                elif j.Upgrade_Oyt == '3':
                    var_Upgrade_Oyt = "A1 (With OYT)"
                elif j.Upgrade_Oyt == '1':
                    var_Upgrade_Oyt = "B"
                lst_upgrade_oyt.append(var_Upgrade_Oyt)

            final_lst = zip(lst_upgrade_oyt,lst_oyt, data)


            return render(request, 'officer/cgm_rejected_tkc.html', {'data': data,'final_lst':final_lst,'officer':officer})



    return redirect('/')


# poornima 13 april niche chnage*********************************************************************************************

# def nabl_dgm_qc_evaluate_save(request, id):
#     if request.method == 'POST':
#         data = User_Registration.objects.filter(User_Id=id)
#         if data[0].User_type == "NABL":
#             doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
#             counter = 100
#             comment = 0
#             kk = 0
#             for data in doc:
#                 comm = request.POST.get(str(comment))
#                 result = request.POST.get(str(counter))
#                 if comm != '':
#                     data.Primary_remark = comm
#                 data.Primary_verification_Date = datetime.now().date()
#                 if result == 'OK':
#                     data.Primary_verification_Status = 1
#                 else:
#                     kk = 1
#                     user = User_Registration.objects.get(User_Id=id)
#                     user.qc_approval = 2

#                     data.Primary_verification_Status = 2
#                     data.Status = 0
#                     test = data.Primary_remark_rejection_counter
#                     if test >= 3:
#                         user.final_rejection = 1
#                         user.qc_approval = -1
#                         send_mail(
#                             'Approval status of DGM(QC) ',
#                             'Hello ! Your application is finally rejected by DGM (QC) now',
#                             settings.EMAIL_HOST_USER,
#                             [user.Email_Id],
#                             fail_silently=False,
#                         )
#                     user.save()
#                     test = test + 1
#                     data.Primary_remark_rejection_counter = test
#                 data.save()
#                 counter = counter + 1
#                 comment = comment + 1
#             data = NABL_Document.objects.filter(
#                 user_id=id).filter(Primary_verification_Status=2)

#             if kk == 1:
#                 send_mail(
#                     'Rejection status of DGM(QC) ',
#                     'Hello ! Your application is not approved by DGM (QC).',
#                     settings.EMAIL_HOST_USER,
#                     [user.Email_Id],
#                     fail_silently=False,
#                 )
#             else:
#                 pass

            # if not data:
                # data = User_Registration.objects.get(User_Id=id)
                # data.qc_approval = 1
                # data.save()

#                 send_mail(
#                     'Approval status of DGM(QC) ',
#                     'Hello ! Your application is approved by DGM (QC).',
#                     settings.EMAIL_HOST_USER,
#                     [data.Email_Id],
#                     fail_silently=False,
#                 )
#             data = User_Registration.objects.filter(
#                 qc_approval=0, Complete_Details=1, User_type='NABL')
#             return render(request, 'officer/nabl_dgm_qc_pending.html', {'data': data})

#         data = User_Registration.objects.filter(
#             qc_approval=0, Complete_Details=1, User_type='NABL')
#         return render(request, 'officer/nabl_dgm_qc_pending.html', {'data': data})


# def nabl_dgm_qc_evaluate(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "NABL":
#         # doc = NABL_Document.objects.filter(user_id=id)
#         # doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
#         doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
#         return render(request, 'officer/nabl_dgm_qc_evaluate.html',
#                       {'data': data[0], 'doc': doc})


# def nabl_dgm_qc_pending(request):
#     data = User_Registration.objects.filter(qc_approval=0, Complete_Details=1,
#                                             User_type='NABL') | User_Registration.objects.filter(qc_approval=2,
#                                                                                                  Complete_Details=1,
#                                                                                                  User_type='NABL')
#     return render(request, "officer/nabl_dgm_qc_pending.html", {'data': data})


# def nabl_cgm_evaluate(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "NABL":
#         doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
#         # Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
#         # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)
#         return render(request, 'officer/nabl_cgm_evaluate.html',
#                       {'data': data[0], 'doc': doc})
# anupam
import datetime
from datetime import datetime 
def nabl_cgm_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = User_Registration.objects.filter(User_Id=id)
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            usr_obj = User_Registration.objects.get(User_Id=id)

            comm = request.POST.get(str('remark'))
            doc.CGM_remark = comm
            result = request.POST.get(str('action'))
            if result == 'OK':
                data = User_Registration.objects.get(User_Id=id)
                
                # send_mail(
                #     'Approval status of CGM(QC) ',
                #     'Hello ! Your application is approved by CGM (QC).',
                #     settings.EMAIL_HOST_USER,
                #     [data.Email_Id],
                #     fail_silently=False,
                # )
                from datetime import date
                User_Zone = usr_obj.User_zone
                User = usr_obj.User_type
                vendor_type = "00"
                nabl_type = "00"
                tkc_type = "00"
                today = date.today()
                date = today.strftime("%m%y")
                list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                s = ""
                if User_Zone == "CZ":
                    s = "CZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "TKC":
                        s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)

                if User_Zone == "EZ":
                    s = "EZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "TKC":
                        s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)

                if User_Zone == "WZ":
                    s = "WZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "NABL":
                        s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                    elif User == "TKC":
                        s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)

                data = User_Registration.objects.filter(User_Id=id)
                company_name = data[0].CompanyName_E
                issue_date = today.strftime("%d/%m/%Y")
                from datetime import datetime
                valid_upto = datetime(2024, 1, 11)
                valid_upto = valid_upto.strftime("%d/%m/%Y")
                data11 = User_Registration.objects.filter(User_Id=id)
                data11.update(Authentication_id=s)
                data11 = User_Registration.objects.get(User_Id=id)
                # send_mail(
                #     'Approval status of CGM (QC) ',
                #     'Your application is finally approved by CGM(QC) and your registration number is ' + s,
                #     settings.EMAIL_HOST_USER,
                #     [data11.Email_Id],
                #     fail_silently=False,
                # )

                officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                officer_mobile = officer.mobile
                def generateOTP():
                    OTP = ""
                    digits = "0123456789"
                    for i in range(6):
                        OTP += digits[math.floor(random.random() * 10)]
                    return OTP
                otptt = generateOTP()
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
                response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})

                sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.now(),mobile_number = officer_mobile)
                sms_template.save()
                request.session['otptt'] = otptt

                otp_ofcr = User_Registration.objects.filter(User_Id=id)
                otp_ofcr.update(Otp=otptt)

                usr_obj = User_Registration.objects.get(User_Id=id)
                otp = usr_obj.Otp

                return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})

                # return render(request, 'vendor/cert2.html',
                #               {'User_Zone': User_Zone, 'data': data[0], 'company_name': company_name, 'no': s,
                #                'd1': valid_upto, 'd2': issue_date})

            else:
                data = User_Registration.objects.get(User_Id=id)
                data.cgm_approval = -1
                data.final_rejection = -1
                data.save()
                # send_mail(
                    # 'Rejection status of CGM(QC) ',
                    # 'Hello ! Your application is finally rejected by CGM (QC).',
                    # settings.EMAIL_HOST_USER,
                    # [data.Email_Id],
                    # fail_silently=False,
                # )
                data = User_Registration.objects.filter(
                    qc_approval=1, cgm_approval=0)
                return render(request, 'officer/cgm_pending_nabl.html', {'data': data})

    return redirect('/')


# def cgm_pending_nabl(request):
#     data = User_Registration.objects.filter(
#         qc_approval=1, cgm_approval=0, User_type='NABL')
#     return render(request, 'officer/cgm_pending_nabl.html', {'data': data})


# poo24-03 with html file and mpeb_base

# def cgm_total_nabl(request):
#     data = User_Registration.objects.filter(
#         qc_approval=1, cgm_approval=0, User_type='NABL')
#     return render(request, 'officer/cgm_total_nabl.html', {'data': data})

# ...CGM-TKC.....


def cgm_pending_tkc(request):
    if request.session.has_key('employ_login_id'):
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, cgm_approval=0, User_type='TKC',finance_approval=1,work_approval=1,User_zone='WZ')
            lst_oyt = []
            lst_upgrade_oyt = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)
            for j in data:
                var_Upgrade_Oyt = ""
                if j.Upgrade_Oyt == '9':
                    var_Upgrade_Oyt = "TKC"
                elif j.Upgrade_Oyt == '8':
                    var_Upgrade_Oyt = "A5"
                elif j.Upgrade_Oyt == '7':
                    var_Upgrade_Oyt = "A4"
                elif j.Upgrade_Oyt == '6':
                    var_Upgrade_Oyt = "A3"
                elif j.Upgrade_Oyt == '5':
                    var_Upgrade_Oyt = "A2 (with OYT)"
                elif j.Upgrade_Oyt == '3':
                    var_Upgrade_Oyt = "A1 (With OYT)"
                elif j.Upgrade_Oyt == '1':
                    var_Upgrade_Oyt = "B"
                lst_upgrade_oyt.append(var_Upgrade_Oyt)
            final_lst = zip(lst_upgrade_oyt,lst_oyt, data)
            return render(request, 'officer/cgm_pending_tkc.html', {'data': data,'officer':officer,'final_lst':final_lst})
        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, cgm_approval=0, User_type='TKC',finance_approval=1,work_approval=1,User_zone='EZ')
            lst_oyt = []
            lst_upgrade_oyt = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)
            for j in data:
                var_Upgrade_Oyt = ""
                if j.Upgrade_Oyt == '9':
                    var_Upgrade_Oyt = "TKC"
                elif j.Upgrade_Oyt == '8':
                    var_Upgrade_Oyt = "A5"
                elif j.Upgrade_Oyt == '7':
                    var_Upgrade_Oyt = "A4"
                elif j.Upgrade_Oyt == '6':
                    var_Upgrade_Oyt = "A3"
                elif j.Upgrade_Oyt == '5':
                    var_Upgrade_Oyt = "A2 (with OYT)"
                elif j.Upgrade_Oyt == '3':
                    var_Upgrade_Oyt = "A1 (With OYT)"
                elif j.Upgrade_Oyt == '1':
                    var_Upgrade_Oyt = "B"
                lst_upgrade_oyt.append(var_Upgrade_Oyt)
            final_lst = zip(lst_upgrade_oyt,lst_oyt, data)
            return render(request, 'officer/cgm_pending_tkc.html', {'data': data,'officer':officer,'final_lst':final_lst})
        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, cgm_approval=0, User_type='TKC',finance_approval=1,work_approval=1,User_zone='CZ')
            lst_oyt = []
            lst_upgrade_oyt = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)
            for j in data:
                var_Upgrade_Oyt = ""
                if j.Upgrade_Oyt == '9':
                    var_Upgrade_Oyt = "TKC"
                elif j.Upgrade_Oyt == '8':
                    var_Upgrade_Oyt = "A5"
                elif j.Upgrade_Oyt == '7':
                    var_Upgrade_Oyt = "A4"
                elif j.Upgrade_Oyt == '6':
                    var_Upgrade_Oyt = "A3"
                elif j.Upgrade_Oyt == '5':
                    var_Upgrade_Oyt = "A2 (with OYT)"
                elif j.Upgrade_Oyt == '3':
                    var_Upgrade_Oyt = "A1 (With OYT)"
                elif j.Upgrade_Oyt == '1':
                    var_Upgrade_Oyt = "B"
                lst_upgrade_oyt.append(var_Upgrade_Oyt)
            final_lst = zip(lst_upgrade_oyt,lst_oyt, data)
            return render(request, 'officer/cgm_pending_tkc.html', {'data': data,'officer':officer,'final_lst':final_lst})
    return redirect('/')


# def cgm_complete_tkc(request):
#     data = User_Registration.objects.filter(
#         cgm_approval=1, work_approval=1, finance_approval=1, User_type='TKC')
#     return render(request, 'officer/cgm_complete_tkc.html', {'data': data})

def cgm_complete_tkc(request):
    if request.session.has_key('employ_login_id'):
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        if request.session['officer'] == 'WZ':
            alldata =  User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,finance_approval=0,User_zone='WZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,work_approval=0,User_zone='WZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,finance_approval=2,User_zone='WZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,work_approval=2,User_zone='WZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/cgm_complete_tkc.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})

        elif request.session['officer'] == 'CZ':
            alldata =  User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,finance_approval=0,User_zone='CZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,work_approval=0,User_zone='CZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,finance_approval=2,User_zone='CZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,work_approval=2,User_zone='CZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/cgm_complete_tkc.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})

        elif request.session['officer'] == 'EZ':
            alldata =  User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,finance_approval=0,User_zone='EZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,work_approval=0,User_zone='EZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,finance_approval=2,User_zone='EZ') | User_Registration.objects.filter(officer_create=0,Complete_Details=1,User_type='TKC',complete_data=1,work_approval=2,User_zone='EZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/cgm_complete_tkc.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})

    return redirect('/')

def Inactive_tkc(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(
        cgm_approval=1, work_approval=1, finance_approval=1, User_type='TKC')
        contractor_class = TKC_Payment.objects.all()
        doc = TKC_Document.objects.all()
        paginator = Paginator(data, 20, orphans=1)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)
        return render(request, 'officer/Inactive_tkc.html', {'data': page_obj,'contractor':contractor_class,'doc':doc})
    return redirect('/')

def Active_tkc(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1, User_type='TKC')
        contractor_class = TKC_Payment.objects.all()
        doc = TKC_Document.objects.all()
        paginator = Paginator(data, 20, orphans=1)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)
        return render(request, 'officer/Active_tkc.html', {'data': page_obj,'contractor':contractor_class,'doc':doc})
    return redirect('/')

  

def tkc_cgm_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        # data.update(cgm_approval=1)
        if data[0].User_type == "TKC":
            if BankDetails.objects.filter(user_id=data[0].ContactNo).exists():
                bank = BankDetails.objects.filter(user_id=data[0].ContactNo)
                if (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 0) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  0):
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=0)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0],'officer':officer ,'doc': doc, 'doc1': doc1,'payment':payment,'CompanyData':CompanyData1,'bank':bank[0]})
                elif (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 1) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  1):
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1,'payment':payment,'CompanyData':CompanyData1,'bank':bank[0]})

                elif (data[0].upgrade_payment == 1 and  data[0].activation_before_expired == 0) |  (data[0].upgrade_payment == 1 and  data[0].activation_after_expired ==  0):
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    if data[0].Upgrade_Oyt:
                        up_oyt = TKC_Payment.objects.get(id=data[0].Upgrade_Oyt)
                        return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0],'Upgrade_Oyt':up_oyt,'officer':officer ,'doc': doc, 'doc1': doc1,'payment':payment,'CompanyData':CompanyData1,'bank':bank[0]})

                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1,'payment':payment,'CompanyData':CompanyData1,'bank':bank[0]})

                else:
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1,'payment':payment,'CompanyData':CompanyData1,'bank':bank[0]})

            else:
                if (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 0) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  0):
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=0)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1,'payment':payment,'CompanyData':CompanyData1})
                elif (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 1) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  1):
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1,'payment':payment,'CompanyData':CompanyData1})

                elif (data[0].upgrade_payment == 1 and  data[0].activation_before_expired == 0) |  (data[0].upgrade_payment == 1 and  data[0].activation_after_expired ==  0):
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    if data[0].Upgrade_Oyt:
                        up_oyt = TKC_Payment.objects.get(id=data[0].Upgrade_Oyt)
                        return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0],'Upgrade_Oyt':up_oyt,'officer':officer ,'doc': doc, 'doc1': doc1,'payment':payment,'CompanyData':CompanyData1})
                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1,'payment':payment,'CompanyData':CompanyData1})

                else:
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                    doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    payment = TKC_Payment.objects.get(id=data[0].Oyt)
                    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                    return render(request, 'officer/tkc_cgm_evaluate.html',
                                {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1,'payment':payment,'CompanyData':CompanyData1})
    return redirect('/')


def tkc_cgm_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            print("ttttwwwwwwwwwooooooo")
            data = User_Registration.objects.filter(User_Id=id)
            doc = TKC_Document.objects.filter(user_id=data[0].User_Id)
            late = TKC_Document.objects.filter(user_id=data[0].User_Id)
            latest = late.latest('new_data')
            if latest.new_data == 0:
                exp = TKC_Document.objects.get(user_id=data[0].User_Id, Types_of_Docs='Electrical License',new_data=0)
                expi_date = exp.Doc_expiry_date
                doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=0)
            elif latest.new_data == 1:
                exp = TKC_Document.objects.get(user_id=data[0].User_Id, Types_of_Docs='Electrical License',new_data=1)
                expi_date = exp.Doc_expiry_date
                doc = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)

            
            counter = 100
            comment = 0
            nz = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                data.Primary_verification_Date = datetime.datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status_approver = 1
                elif result == 'NOT':
                    nz = 1
                    user = User_Registration.objects.get(User_Id=id)
                    officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_name = officer_table.employ_name
                    offcier_designation = officer_table.designation
                    summary = reject_and_approve_summary(user=user,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=comm,document=data.Ddocfile,document_name=data.Types_of_Docs)
                    summary.save()
                    user.cgm_approval = 2
                    user.gm_work_reject_date = datetime.datetime.now()
                    user.save()
                    data.Primary_verification_Status_approver = 2
                    print('dataname',data.Types_of_Docs)
                    data.Approver_Status = 1
                    nameee = data.Types_of_Docs
                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    zone = sms.User_zone
                    name_sms = sms.CompanyName_E
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    # for server set proxy
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007768706917984539&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                        nameee) + "&v4=" + str('and other') + "&v5=" + str('GM(works)') + "&v6=" + "MP" + str(zone) + "&v6=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    sms_template = message_template_log(template_id = '1007768706917984539',date = datetime.datetime.now(),mobile_number = mobile)
                    sms_template.save()
                    
                data.save()
                counter = counter + 1
                comment = comment + 1
                data = TKC_Document.objects.filter(
                    user_id=id).filter(Primary_verification_Status_approver=2)

            if not data:
                usr_obj = User_Registration.objects.get(User_Id=id)
                officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                officer_name = officer_table.employ_name
                offcier_designation = officer_table.designation
                summary = reject_and_approve_summary(user=usr_obj,type="APPROVE",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
                summary.save()
                data1 = User_Registration.objects.get(User_Id=id)
                upgrade_id = data1.Upgrade_Oyt
                usr_obj.status = 1
                usr_obj.gm_work_approved_date = datetime.datetime.now()
                usr_obj.save()
                if data1.upgrade_payment==0 and data1.activation_before_expired==0 and data1.activation_after_expired ==0:
                    data = User_Registration.objects.filter(User_Id=id)
                    late = TKC_Document.objects.filter(user_id=data[0].User_Id)
                    
                    latest = late.latest('new_data')
                
                    if latest.new_data == 1:
                        delete1 = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data = 0)
                        delete1.delete()

                        delete1_new = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                        delete1_new.update(new_data=0,Primary_verification_Status_approver=0)
                
                    data = User_Registration.objects.get(User_Id=id)
                    
                    data.activation_before_expired = 0
                    data.activation_after_expired = 0
                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    data.date_of_approved = datetime.datetime.now()
                    data.save()
                
                    
                
                    # send_mail(
                    #     'Approval status of GM (Works) ',
                    #     'Hello ! Your are approved by GM (Works)',
                    #     settings.EMAIL_HOST_USER,
                    #     [data.Email_Id],
                    #     fail_silently=False,
                    # )
                    from datetime import date
                    User_zone_check = usr_obj.User_zone
                    User = usr_obj.User_type
                    vendor_type = "00"
                    nabl_type = "00"
                    tkc_type = "00"
                    today = date.today()
                    date = today.strftime("%m%y")
                    list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    s = ""
                    if User_zone_check == "CZ":
                        s = "CZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    if User_zone_check == "EZ":
                        s = "EZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    if User_zone_check == "WZ":
                        s = "WZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    data = User_Registration.objects.filter(User_Id=id)
                    company_name = data[0].CompanyName_E
                    issue_date = today.strftime("%d/%m/%Y")
                    valid_upto = expi_date
                    data11 = User_Registration.objects.get(User_Id=id)
                    # data11.Authentication_id = s
                    # data11.save()

                    # vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)

                    # send_mail(
                    #     'Approval status of GM (works) ',
                    #     'Your application is finally approved by GM(Works) and your registration number is ' + s,
                    #     settings.EMAIL_HOST_USER,
                    #     [data11.Email_Id],
                    #     fail_silently=False,
                    # )
                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    td = datetime.datetime.now()

                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
                    zone = sms.User_zone
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}

                    #proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    #for server set proxy

                    # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                    
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277221739526680&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('TKC') + "&v4=" + "MP" + str(zone)  + "&v5=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1007277221739526680',date = datetime.datetime.now(),mobile_number = mobile)
                    sms_template.save()

                    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_mobile = officer.mobile
                    def generateOTP():
                        OTP = ""
                        digits = "0123456789"
                        for i in range(6):
                            OTP += digits[math.floor(random.random() * 10)]
                        return OTP
                    otptt = generateOTP()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
                    response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
                    sms_template.save()

                    request.session['otptt'] = otptt
                    request.session['officer_mobile'] = officer_mobile
                    otp_ofcr = User_Registration.objects.filter(User_Id=id)
                    otp_ofcr.update(Otp=otptt)

                    usr_obj = User_Registration.objects.get(User_Id=id)
                    otp = usr_obj.Otp
    
                    if usr_obj.officer_create == 0:

                        return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})

                    else:
                        return render(request, 'main/officer_otp_new_tkc.html', {'id': id, 'otp': otp})

                    # return render(request, 'vendor/cert2.html',
                    #               {'User_Zone': User_Zone, 'td': td, 'data': data[0], 'company_name': company_name, 'no': s,
                    #                'd1': valid_upto, 'd2': issue_date})
                


                elif data1.upgrade_payment==1:
                    data = User_Registration.objects.filter(User_Id=id)
                    late = TKC_Document.objects.filter(user_id=data[0].User_Id)
                    
                    latest = late.latest('new_data')
                
                    if latest.new_data == 1:
                        delete1 = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data = 0)
                        delete1.delete()

                        delete1_new = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                        delete1_new.update(new_data=0,Primary_verification_Status_approver=0)

                    data = User_Registration.objects.get(User_Id=id)
                    data.cgm_approval = 1
                    data.Oyt = upgrade_id
                    data.Upgrade_Oyt = upgrade_id
                    data.upgrade_payment = 0
                    data.activation_before_expired = 0
                    data.activation_after_expired = 0
                    data.save()
                    
                    # bdetail_delete = BankDetails.objects.filter(user_id=data.ContactNo, new_data=0)
                    # bdetail_delete.delete()
                    # bdetail = BankDetails.objects.filter(user_id=data.ContactNo, new_data=1)
                    # bdetail.update(new_data=0)
                    # send_mail(
                    #     'Approval status of GM (Works) ',
                    #     'Hello ! Your are approved by GM (Works)',
                    #     settings.EMAIL_HOST_USER,
                    #     [data.Email_Id],
                    #     fail_silently=False,
                    # )
                    from datetime import date
                    User_Zone_tt = usr_obj.User_zone
                    User = usr_obj.User_type
                    vendor_type = "00"
                    nabl_type = "00"
                    tkc_type = "00"
                    today = date.today()
                    date = today.strftime("%m%y")
                    list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    s = ""
                    if User_Zone_tt == "CZ":
                        s = "CZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    if User_Zone_tt == "EZ":
                        s = "EZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    if User_Zone_tt == "WZ":
                        s = "WZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    data = User_Registration.objects.filter(User_Id=id)
                    company_name = data[0].CompanyName_E
                    issue_date = today.strftime("%d/%m/%Y")
                    valid_upto = expi_date
                    data11 = User_Registration.objects.get(User_Id=id)
                    # data11.Authentication_id = s
                    # data11.save()

                    # vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)

                    # send_mail(
                    #     'Approval status of GM (works) ',
                    #     'Your application is finally approved by GM(Works) and your registration number is ' + s,
                    #     settings.EMAIL_HOST_USER,
                    #     [data11.Email_Id],
                    #     fail_silently=False,
                    # )
                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    td = datetime.datetime.now()

                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
                    zone = sms.User_zone
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}

                    #proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    #for server set proxy

                    # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                    
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277221739526680&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('TKC') + "&v4=" + "MP" + str(zone)  + "&v5=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1007277221739526680',date = datetime.datetime.now(),mobile_number = mobile)
                    sms_template.save()

                    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_mobile = officer.mobile
                    def generateOTP():
                        OTP = ""
                        digits = "0123456789"
                        for i in range(6):
                            OTP += digits[math.floor(random.random() * 10)]
                        return OTP
                    otptt = generateOTP()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
                    response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
                    sms_template.save()

                    request.session['otptt'] = otptt
                    request.session['officer_mobile'] = officer_mobile
                    otp_ofcr = User_Registration.objects.filter(User_Id=id)
                    otp_ofcr.update(Otp=otptt)

                    usr_obj = User_Registration.objects.get(User_Id=id)
                    otp = usr_obj.Otp
                    if usr_obj.officer_create == 0:

                        return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})

                    else:
                        return render(request, 'main/officer_otp_new_tkc.html', {'id': id, 'otp': otp})
                elif data1.activation_before_expired==1 or data1.activation_after_expired ==1 :
                    data = User_Registration.objects.filter(User_Id=id)
                    late = TKC_Document.objects.filter(user_id=data[0].User_Id)
                    
                    latest = late.latest('new_data')
                
                    if latest.new_data == 1:
                        delete1 = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data = 0)
                        delete1.delete()

                        delete1_new = TKC_Document.objects.filter(user_id=data[0].User_Id,new_data=1)
                        delete1_new.update(new_data=0,Primary_verification_Status_approver=0)

                    data = User_Registration.objects.get(User_Id=id)
                    data.cgm_approval = 1
                    data.activation_before_expired = 0
                    data.activation_after_expired = 0
                    data.upgrade_payment = 0
                    data.save()
                    
                    # bdetail_delete = BankDetails.objects.filter(user_id=data.ContactNo, new_data=0)
                    # bdetail_delete.delete()
                    # bdetail = BankDetails.objects.filter(user_id=data.ContactNo, new_data=1)
                    # bdetail.update(new_data=0)
                    # send_mail(
                    #     'Approval status of GM (Works) ',
                    #     'Hello ! Your are approved by GM (Works)',
                    #     settings.EMAIL_HOST_USER,
                    #     [data.Email_Id],
                    #     fail_silently=False,
                    # )
                    from datetime import date
                    User_Zone_tt = usr_obj.User_zone
                    User = usr_obj.User_type
                    vendor_type = "00"
                    nabl_type = "00"
                    tkc_type = "00"
                    today = date.today()
                    date = today.strftime("%m%y")
                    list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    s = ""
                    if User_Zone_tt == "CZ":
                        s = "CZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    if User_Zone_tt == "EZ":
                        s = "EZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    if User_Zone_tt == "WZ":
                        s = "WZ"
                        if User == "VENDOR":
                            s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "NABL":
                            s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)
                        elif User == "TKC":
                            s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                                list1) + random.choice(list1)

                    data = User_Registration.objects.filter(User_Id=id)
                    company_name = data[0].CompanyName_E
                    issue_date = today.strftime("%d/%m/%Y")
                    valid_upto = expi_date
                    data11 = User_Registration.objects.get(User_Id=id)
                    # data11.Authentication_id = s
                    # data11.save()

                    # vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)

                    # send_mail(
                    #     'Approval status of GM (works) ',
                    #     'Your application is finally approved by GM(Works) and your registration number is ' + s,
                    #     settings.EMAIL_HOST_USER,
                    #     [data11.Email_Id],
                    #     fail_silently=False,
                    # )
                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    td = datetime.datetime.now()

                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
                    zone = sms.User_zone
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}

                    #proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    #for server set proxy

                    # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                    
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277221739526680&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('TKC') + "&v4=" + "MP" + str(zone)  + "&v5=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1007277221739526680',date = datetime.datetime.now(),mobile_number = mobile)
                    sms_template.save()

                    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_mobile = officer.mobile
                    def generateOTP():
                        OTP = ""
                        digits = "0123456789"
                        for i in range(6):
                            OTP += digits[math.floor(random.random() * 10)]
                        return OTP
                    otptt = generateOTP()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
                    response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
                    sms_template.save()

                    request.session['otptt'] = otptt
                    request.session['officer_mobile'] = officer_mobile
                    otp_ofcr = User_Registration.objects.filter(User_Id=id)
                    otp_ofcr.update(Otp=otptt)

                    usr_obj = User_Registration.objects.get(User_Id=id)
                    otp = usr_obj.Otp

                

                    if usr_obj.officer_create == 0:

                        return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})

                    else:
                        return render(request, 'main/officer_otp_new_tkc.html', {'id': id, 'otp': otp})

             
            return redirect('cgm_pending_tkc')
    return redirect('/')


# change by poornima

# def resubmit_view(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "VENDOR":
#         doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)

#         no_preview_path = os.getcwd() + "/media/documents/vendor/work_data/No_Preview.pdf"

#         try:
#             for i in doc:
#                 if i.Ddocfile.url == "":
#                     abc = i.update(Ddocfile=no_preview_path)
#                     abc.save()
#         except Exception as e:
#             pass

#         return render(request, 'officer/vendor_resubmit_pending_view.html', {'data': data[0], 'doc': doc})

#     if data[0].User_type == "TKC":
#         doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1)
#         return render(request, 'officer/tkc_resubmit_pending_view_work.html', {'data': data[0], 'doc': doc})

#     if data[0].User_type == "NABL":
#         doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
#         return render(request, 'officer/nabl_resubmit_pending_view_work.html', {'data': data[0], 'doc': doc})

#     return render(request, 'officer/tkc_resubmit_pending_view_work.html', {'data': data[0]})


# def resubmit_finance_evaluate(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "VENDOR":
#         # doc2 = Vendor_Document.objects.filter(user_id=data[0].User_Id)
#         # doc = Vendor_Turnover.objects.filter(user_id=data[0].User_Id)
#         doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
#         no_preview_path = os.getcwd() + "/media/documents/No_Preview.pdf"

#         try:
#             for i in doc1:
#                 if i.Ddocfile.url == "":
#                     abc = i.update(Balance_Sheet=no_preview_path)
#                     abc.save()
#         except Exception as e:
#             pass
#         return render(request, 'officer/resubmit_dgm_finance_evaluate.html',
#                       {'doc1': doc1, 'data': data[0]})
#     if data[0].User_type == "TKC":
#         doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
#         doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
#         return render(request, 'officer/tkc_resubmit_dgm_finance_evaluate.html',
#                       {'data': data[0], 'doc': doc, 'doc1': doc1})


# def dgm_finance_view(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
#     doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
#     return render(request, 'officer/dgm_finance_view.html',
#                   {'data': data[0], 'doc': doc, 'doc1': doc1})


# def vendor_dgm_finance_pending_rejection_tkc(request):
#     data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/vendor_dgm_finance_pending_rejection_tkc.html', {'data': data})
# Anupam

def gp_inward(request):
    trf_obj = TRF_Details.objects.all()
    return render(request, 'officer/gp_inward.html', {'trf_obj': trf_obj})


def gp_inward_rca(request):
    rca_trf_obj = Rcatrf_Details.objects.all()
    return render(request, 'officer/gp_inward_rca.html', {'trf_obj': rca_trf_obj})


def gp_view(request, trf_id):
    trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_view.html', {'employees': trf_obj, 'trf_id': trf_id})


def gp_view_rca(request, trf_id):
    rca_trf_obj = Add_material_rca.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_view_rca.html', {'employees': rca_trf_obj, 'trf_id': trf_id})


def employees_list2(request, trf_id):
    try:
        trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
        return render(request, 'officer/one.html', {'employees': trf_obj, 'trf_id': trf_id})
    except Exception as e:
        return render(request, 'officer/one.html', {'trf_id': trf_id})


def employees_list2_rca(request, trf_id):
    try:
        trf_obj = Add_material_rca.objects.filter(TRF_Id=trf_id)
        return render(request, 'officer/one_rca.html', {'employees': trf_obj, 'trf_id': trf_id})
    except Exception as e:
        return render(request, 'officer/one_rca.html', {'trf_id': trf_id})


def create_employee2(request, trf_id):
    po_obj = ProcurementInfo.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/create.html', {'po_obj': po_obj, 'trf_id': trf_id})


def create_employee2_rca(request, trf_id):
    po_obj = RcaProcurementInfo.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/create_rca.html', {'po_obj': po_obj, 'trf_id': trf_id})


def two2(request, trf_id):
    if request.method == 'POST':
        material = request.POST.get('Material')
        specification = request.POST.get('Specification')
        Vehicle_number = request.POST.get('Vehicle_number')
        Driver_name = request.POST.get('Driver_name')
        Date = request.POST.get('Date')
        Submitted_by = request.POST.get('Submitted_by')
        Test_Request_Form_by = request.POST.get('Test_Request_Form_by')
        material_number_list = request.POST.get('material_number_list')
        Allot_no = request.POST.get('Allot_no')
        Material_id = request.POST.get('Material_id')
        Start_date = request.POST.get('Start_date')
        End_Date = request.POST.get('End_Date')

        material_obj = Add_material_nabl(select_material=material, TRF_Id=trf_id,
                                         select_specification=specification, Vehicle_number=Vehicle_number,
                                         Driver_name=Driver_name, Date=Date, Submitted_by=Submitted_by,
                                         Test_Request_Form_by=Test_Request_Form_by,
                                         material_number_list=material_number_list, Allot_no=Allot_no,
                                         Material_id=Material_id, Start_date=Start_date, End_Date=End_Date
                                         )
        material_obj.save()

    trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)

    det_obj = TRF_Details.objects.filter(TRF_Id=trf_id)
    det_obj.update(gatepass_gen=1)

    return render(request, 'officer/one.html', {'employees': trf_obj, 'trf_id': trf_id})


def two2_rca(request, trf_id):
    if request.method == 'POST':
        material = request.POST.get('Material')
        specification = request.POST.get('Specification')
        Vehicle_number = request.POST.get('Vehicle_number')
        Driver_name = request.POST.get('Driver_name')
        Date = request.POST.get('Date')
        Submitted_by = request.POST.get('Submitted_by')
        Test_Request_Form_by = request.POST.get('Test_Request_Form_by')
        material_number_list = request.POST.get('material_number_list')
        Allot_no = request.POST.get('Allot_no')
        Material_id = request.POST.get('Material_id')
        Start_date = request.POST.get('Start_date')
        End_Date = request.POST.get('End_Date')

        material_obj = Add_material_rca(select_material=material, TRF_Id=trf_id,
                                        select_specification=specification, Vehicle_number=Vehicle_number,
                                        Driver_name=Driver_name, Date=Date, Submitted_by=Submitted_by,
                                        Test_Request_Form_by=Test_Request_Form_by,
                                        material_number_list=material_number_list, Allot_no=Allot_no,
                                        Material_id=Material_id, Start_date=Start_date, End_Date=End_Date
                                        )
        material_obj.save()

    trf_obj = Add_material_rca.objects.filter(TRF_Id=trf_id)

    det_obj = Rcatrf_Details.objects.filter(TRF_Id=trf_id)
    det_obj.update(gatepass_gen=1)

    return render(request, 'officer/one_rca.html', {'employees': trf_obj, 'trf_id': trf_id})


def tmqm_sample_recv(request):
    add_material_nabl = Add_material_nabl.objects.all()
    return render(request, 'officer/tmqm_sample_recv.html', {'employees': add_material_nabl})


def tmqm_sample_recv_rca(request):
    add_material_nabl = Add_material_rca.objects.all()
    return render(request, 'officer/tmqm_sample_recv_rca.html', {'employees': add_material_nabl})


def tmqm_sample_recv2(request, trf_id):
    add_material_nabl = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    add_material_nabl.update(sample_received=1)
    txt = str(add_material_nabl[0].material_number_list)
    mat_list = txt.split(",")
    material = add_material_nabl[0].select_material

    date = time.strftime("%d%m%y")

    final_list = []
    for i in range(len(mat_list)):
        if material == "CABLES":
            s_mat = 'CA' + date + mat_list[i]
            final_list.append(s_mat)
        elif material == "DTR":
            s_mat = 'DT' + date + mat_list[i]
            final_list.append(s_mat)
        elif material == "CONDUCTORS":
            s_mat = 'DT' + date + mat_list[i]
            final_list.append(s_mat)

    f_lst = zip(mat_list, final_list)

    sample_obj = sample_code_table.objects.filter(TRF_Id=trf_id)
    if not sample_obj:
        for i in range(len(mat_list)):
            sc_obj = sample_code_table(
                TRF_Id=trf_id, material_serial_number=mat_list[i], sample_code=final_list[i])
            sc_obj.save()
        # po_obj = ProcurementInfo.objects.filter(TRF_Id=trf_id)
        # po_obj.update(po_test_progress=1)

    else:
        pass
    return render(request, 'officer/tmqm_sample_recv2.html',
                  {'employees': add_material_nabl[0], 'user_id': trf_id, 'f_list': f_lst})


def tmqm_sample_recv2_rca(request, trf_id):
    add_material_nabl = Add_material_rca.objects.filter(TRF_Id=trf_id)
    add_material_nabl.update(sample_received=1)
    txt = str(add_material_nabl[0].material_number_list)
    mat_list = txt.split(",")
    material = add_material_nabl[0].select_material

    date = time.strftime("%d%m%y")

    final_list = []
    for i in range(len(mat_list)):
        if material == "CABLES":
            s_mat = 'CA' + date + mat_list[i]
            final_list.append(s_mat)
        elif material == "DTR":
            s_mat = 'DT' + date + mat_list[i]
            final_list.append(s_mat)
        elif material == "CONDUCTORS":
            s_mat = 'DT' + date + mat_list[i]
            final_list.append(s_mat)

    f_lst = zip(mat_list, final_list)

    sample_obj = sample_code_table_rca.objects.filter(TRF_Id=trf_id)
    if not sample_obj:
        for i in range(len(mat_list)):
            sc_obj = sample_code_table_rca(
                TRF_Id=trf_id, material_serial_number=mat_list[i], sample_code=final_list[i])
            sc_obj.save()
        # po_obj = RcaProcurementInfo.objects.filter(TRF_Id=trf_id)
        # po_obj.update(po_test_progress=1)
    else:
        pass
    return render(request, 'officer/tmqm_sample_recv2_rca.html',
                  {'employees': add_material_nabl[0], 'user_id': trf_id, 'f_list': f_lst})


def gp_outward(request, trf_id):
    if request.method == 'POST':
        outpass_date = request.POST.get('outpass_date')
        outpass_driver_name = request.POST.get('outpass_driver_name')
        outpass_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
        outpass_obj.update(outpass_date=outpass_date, outpass_driver_name=outpass_driver_name,
                           outpass_generate_complete=1)

        trf_outpass_obj = TRF_Details.objects.filter(TRF_Id=trf_id)
        trf_outpass_obj.update(outpass_gen=1)

        trf_obj = TRF_Details.objects.all()
        return render(request, 'officer/gp_inward.html', {'trf_obj': trf_obj})

    trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_outward.html', {'employees': trf_obj, 'trf_id': trf_id})


def gp_outward_rca(request, trf_id):
    if request.method == 'POST':
        outpass_date = request.POST.get('outpass_date')
        outpass_driver_name = request.POST.get('outpass_driver_name')
        outpass_obj = Add_material_rca.objects.filter(TRF_Id=trf_id)
        outpass_obj.update(outpass_date=outpass_date, outpass_driver_name=outpass_driver_name,
                           outpass_generate_complete=1)

        trf_outpass_obj = Rcatrf_Details.objects.filter(TRF_Id=trf_id)
        trf_outpass_obj.update(outpass_gen=1)

        trf_obj = Rcatrf_Details.objects.all()
        return render(request, 'officer/gp_inward_rca.html', {'trf_obj': trf_obj})

    trf_obj = Add_material_rca.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_outward_rca.html', {'employees': trf_obj, 'trf_id': trf_id})


def gp_outward_view(request, trf_id):
    trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_outward_view.html', {'employees': trf_obj, 'trf_id': trf_id})


def gp_outward_view_rca(request, trf_id):
    trf_obj = Add_material_rca.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_outward_view_rca.html', {'employees': trf_obj, 'trf_id': trf_id})


def tmqm_sample_reject(request, trf_id):
    trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    sample_obj = sample_code_table.objects.filter(TRF_Id=trf_id)
    officer_obj = teachincal_officer_table.objects.all()

    if request.method == 'POST':
        sc = request.POST.getlist('rejected_sample_code')
        rejection_yes_no = request.POST.getlist('rejection_yes_no')
        rejected_by_officer = request.POST.getlist('rejected_by_officer')
        rejection_remark = request.POST.getlist('rejection_remark')
        rejected_date = request.POST.getlist('rejected_date')
        rejected_vehicle_number = request.POST.getlist(
            'rejected_vehicle_number')

        reject_all_date = request.POST.get('reject_all_date')
        reject_all_by_officer = request.POST.get('reject_all_by_officer')
        reject_all_remark = request.POST.get('reject_all_remark')

        if reject_all_date and reject_all_by_officer and reject_all_remark:
            for i in range(len(sc)):
                data = sample_code_table.objects.filter(sample_code=sc[i])
                data.update(is_rejected=1),
                data.update(rejected_by_officer=reject_all_by_officer)
                data.update(rejected_date=reject_all_date)
                data.update(rejection_remark=reject_all_date)

        else:
            pass

        for i in range(len(sc)):
            data = sample_code_table.objects.filter(sample_code=sc[i])
            if sc[i] and rejection_yes_no[i] and rejected_by_officer[i] and rejection_remark[i] and rejected_date[i] and \
                    rejected_vehicle_number[i]:
                data.update(rejected_sample_code=sc[i], rejection_yes_no=rejection_yes_no[i],
                            rejected_by_officer=rejected_by_officer[i],
                            rejection_remark=rejection_remark[i], rejected_date=rejected_date[i],
                            rejected_vehicle_number=rejected_vehicle_number[i], is_rejected=1)
            else:
                pass

    return render(request, 'officer/tmqm_sample_reject.html',
                  {'trf_id': trf_id, 'trf_obj': trf_obj, 'sample_obj': sample_obj, 'officer_obj': officer_obj})


def tmqm_sample_reject_rca(request, trf_id):
    trf_obj = Add_material_rca.objects.filter(TRF_Id=trf_id)
    sample_obj = sample_code_table_rca.objects.filter(TRF_Id=trf_id)
    officer_obj = teachincal_officer_table_rca.objects.all()

    if request.method == 'POST':
        sc = request.POST.getlist('rejected_sample_code')
        rejection_yes_no = request.POST.getlist('rejection_yes_no')
        rejected_by_officer = request.POST.getlist('rejected_by_officer')
        rejection_remark = request.POST.getlist('rejection_remark')
        rejected_date = request.POST.getlist('rejected_date')
        rejected_vehicle_number = request.POST.getlist('rejected_vehicle_number')

        reject_all_date = request.POST.get('reject_all_date')
        reject_all_by_officer = request.POST.get('reject_all_by_officer')
        reject_all_remark = request.POST.get('reject_all_remark')

        if reject_all_date and reject_all_by_officer and reject_all_remark:
            for i in range(len(sc)):
                data = sample_code_table_rca.objects.filter(sample_code=sc[i])
                data.update(is_rejected=1),
                data.update(rejected_by_officer=reject_all_by_officer)
                data.update(rejected_date=reject_all_date)
                data.update(rejection_remark=reject_all_date)
        else:
            pass

        for i in range(len(sc)):
            data = sample_code_table_rca.objects.filter(sample_code=sc[i])
            if sc[i] and rejection_yes_no[i] and rejected_by_officer[i] and rejection_remark[i] and rejected_date[i] and \
                    rejected_vehicle_number[i]:
                data.update(rejected_sample_code=sc[i], rejection_yes_no=rejection_yes_no[i],
                            rejected_by_officer=rejected_by_officer[i],
                            rejection_remark=rejection_remark[i], rejected_date=rejected_date[i],
                            rejected_vehicle_number=rejected_vehicle_number[i], is_rejected=1)
            else:
                pass

    return render(request, 'officer/tmqm_sample_reject_rca.html',
                  {'trf_id': trf_id, 'trf_obj': trf_obj, 'sample_obj': sample_obj, 'officer_obj': officer_obj})


def tmqm_job_order(request):
    add_material_nabl = Add_material_nabl.objects.all()
    return render(request, 'officer/tmqm_job_order.html', {'employees': add_material_nabl})


def tmqm_job_order_rca(request):
    add_material_nabl = Add_material_rca.objects.all()
    return render(request, 'officer/tmqm_job_order_rca.html', {'employees': add_material_nabl})


def tmqm_job_order2(request, trf_id):
    sample_obj = sample_code_table.objects.filter(TRF_Id=trf_id)
    officer_obj = teachincal_officer_table.objects.all()
    return render(request, 'officer/tmqm_job_order2.html',
                  {'f_list': sample_obj, 'officer_obj': officer_obj, 'trf_id': trf_id})


def tmqm_job_order2_rca(request, trf_id):
    sample_obj = sample_code_table_rca.objects.filter(TRF_Id=trf_id)
    officer_obj = teachincal_officer_table_rca.objects.all()
    return render(request, 'officer/tmqm_job_order2_rca.html',
                  {'f_list': sample_obj, 'officer_obj': officer_obj, 'trf_id': trf_id})


def tmqm_job_order3(request, trf_id):
    add_material_nabl = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    add_material_nabl.update(job_order_complete=1)

    if request.method == 'POST':
        sc = request.POST.getlist('sample_code')
        date = request.POST.getlist('date[]')
        officer = request.POST.getlist('officer')
        for i in range(len(sc)):
            data = sample_code_table.objects.filter(sample_code=sc[i])
            data.update(date=date[i], officer_id=officer[i])
    sc_obj = sample_code_table.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/tmqm_job_order3.html', {'sc_obj': sc_obj, 'trf_id': trf_id})


def tmqm_job_order3_rca(request, trf_id):
    add_material_nabl = Add_material_rca.objects.filter(TRF_Id=trf_id)
    add_material_nabl.update(job_order_complete=1)
    if request.method == 'POST':
        sc = request.POST.getlist('sample_code')
        date = request.POST.getlist('date[]')
        officer = request.POST.getlist('officer')
        for i in range(len(sc)):
            data = sample_code_table_rca.objects.filter(sample_code=sc[i])
            data.update(date=date[i], officer_id=officer[i])
    sc_obj = sample_code_table_rca.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/tmqm_job_order3_rca.html', {'sc_obj': sc_obj, 'trf_id': trf_id})


def ta_base(request):
    return render(request, 'officer/ta_base.html')


def ta_joborder(request):
    sct_obj = sample_code_table.objects.all()
    return render(request, 'officer/ta_joborder.html', {'sct_obj': sct_obj})


def ta_joborder_rca(request):
    sct_obj = sample_code_table_rca.objects.all()
    return render(request, 'officer/ta_joborder_rca.html', {'sct_obj': sct_obj})


def ta_uploadReport(request, trf_id):
    if request.method == "POST":
        ReportFile = request.FILES['myfile']
        nabl_test_obj = Nabl_Test_Report(TRF_Id=trf_id, ReportFile=ReportFile)
        nabl_test_obj.save()

    return render(request, 'officer/ta_uploadReport.html', {'trf_id': trf_id})


def ta_uploadReport_rca(request, trf_id):
    if request.method == "POST":
        ReportFile = request.FILES['myfile']
        nabl_test_obj = Nabl_Test_Report_rca(TRF_Id=trf_id, ReportFile=ReportFile)
        nabl_test_obj.save()
    return render(request, 'officer/ta_uploadReport_rca.html', {'trf_id': trf_id})


import pyodbc
def Report_success(request):
    # cnxn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                    # server='172.16.9.103',
                    # database='TTPGeneric',
                    # uid='sa',
                    # pwd='pejk7UNj',
                    # port='1433'
                    # )
                    
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    server = 'tcp:172.16.9.103' 
    database = 'TTPGeneric' 
    username = 'sa' 
    password = 'pejk7UNj' 
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=no;UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()    
    
    
    cur = cnxn.cursor()
    cur.execute('SELECT * from "AllData_TATTestFreezed"')
    rows = cur.fetchall()

    sample_code_lst = []
    for i in rows:
        reportno = i.ReportNo
        ulrno = i.ULRNo
        manufacturer_wopo = i.Manufacturer_WOPO
        manufacturer = i.Manufacturer
        wo_po = i.WO_PO
        srno = i.srno
        lot = i.lot
        mainid = i.MainID
        maindetid = i.MainDETID
        bulkmain_tfcondition = i.BulkMain_TfCondition
        bulkmain_phase = i.BulkMain_Phase
        bulkmain_windingtype = i.BulkMain_WindingType
        bulkmain_vector = i.BulkMain_Vector
        bulkmain_win_descg1 = i.BulkMain_win_descg1
        bulkmain_win_descg2 = i.BulkMain_win_descg2
        bulkmain_cooling = i.BulkMain_Cooling
        bulkmain_prim_mva = i.BulkMain_Prim_MVA
        bulkmain_sec_mva = i.BulkMain_Sec_MVA
        bulkmain_prim_ratedvol = i.BulkMain_Prim_RatedVol
        bulkmain_sec_ratedvol = i.BulkMain_Sec_RatedVol
        bulkmain_prim_ratedcur = i.BulkMain_Prim_RatedCur
        bulkmain_sec_ratedcur = i.BulkMain_Sec_RatedCur
        bulkmain_prim_conn = i.BulkMain_Prim_Conn
        bulkmain_sec_conn = i.BulkMain_Sec_Conn
        bulkmain_prim_not1 = i.BulkMain_Prim_not1
        bulkmain_prim_not2 = i.BulkMain_Prim_not2
        bulkmain_prim_not3 = i.BulkMain_Prim_not3
        bulkmain_prim_not4 = i.BulkMain_Prim_not4
        bulkmain_sec_not1 = i.BulkMain_Sec_not1
        bulkmain_sec_not2 = i.BulkMain_Sec_not2 
        bulkmain_sec_not3 = i.BulkMain_Sec_not3 
        bulkmain_sec_not4 = i.BulkMain_Sec_not4 
        bulkmain_temp_oil = i.BulkMain_Temp_Oil
        bulkmain_temp_wind = i.BulkMain_Temp_Wind
        bulkmain_windingmaterial = i.BulkMain_WindingMaterial 
        bulkmain_metalval = i.BulkMain_MetalVal 
        bulkmain_refstd = i.BulkMain_refstd 
        bulkmain_jobrating = i.BulkMain_jobrating 
        bulkmain_reftemp = i.BulkMain_RefTemp 
        bulkmain_freq = i.BulkMain_freq
        bulkmain_oilleakage = i.BulkMain_oilleakage
        bulkmain_oilquantity = i.BulkMain_OilQuantity
        bulkmain_total_loss = i.BulkMain_total_loss
        bulkmain_tap_changer = i.BulkMain_tap_changer
        bulkmain_tapon = i.BulkMain_tapon
        bulkmain_variation = i.BulkMain_variation
        bulkmain_volts1 = i.BulkMain_volts1
        bulkmain_volts2 = i.BulkMain_volts2
        bulkmain_persteps = i.BulkMain_persteps
        bulkmain_steps = i.BulkMain_steps
        torder_scheduleoftest = i.TOrder_ScheduleOfTest
        torder_dateofreceipt = i.TOrder_DateOfReceipt
        torder_dateoftestingfrom = i.TOrder_DateOfTestingFrom
        torder_dateoftestingto = i.TOrder_DateOfTestingTo
        torder_dateofissue = i.TOrder_DateOfIssue
        torder_samplecode = i.TOrder_SampleCode
        torder_customernameaddress = i.TOrder_CustomerNameAddress
        torder_note1 = i.TOrder_Note1
        torder_note2 = i.TOrder_Note2
        torder_note3 = i.TOrder_Note3
        torder_note4 = i.TOrder_Note4
        tfooter_1testedbylabel = i.TFooter_1TestedByLabel
        torder_1testedbyname = i.TOrder_1TestedByName
        torder_1testedbydesign = i.TOrder_1TestedByDesign
        tfooter_2checkedbylabel = i.TFooter_2CheckedByLabel
        torder_2checkedbyname = i.TOrder_2CheckedByName
        torder_2checkedbydesign = i.TOrder_2CheckedByDesign
        tfooter_3approvedbylabel = i.TFooter_3ApprovedByLabel
        torder_3approvedbyname = i.TOrder_3ApprovedByName
        torder_3approvedbydesign = i.TOrder_3ApprovedByDesign
        tfooter_4hodlabel = i.TFooter_4HODLabel
        torder_4hodname = i.TOrder_4HODName
        torder_4hoddesign = i.TOrder_4HODDesign
        tfooter_witnessbylabel = i.TFooter_WitnessByLabel
        torder_witnessbyname1 = i.TOrder_WitnessByName1
        torder_witnessbydesign1 = i.TOrder_WitnessByDesign1
        torder_witnessbyname2 = i.TOrder_WitnessByName2
        torder_witnessbydesign2 = i.TOrder_WitnessByDesign2
        torder_witnessbyname3 = i.TOrder_WitnessByName3
        torder_witnessbydesign3 = i.TOrder_WitnessByDesign3
        torder_witnessbyname4 = i.TOrder_WitnessByName4
        torder_witnessbydesign4 = i.TOrder_WitnessByDesign4
        normaltapno = i.NormalTapNo
        totaltapqty = i.TotalTapQty
        wr_lot = i.WR_lot
        wr_testdate = i.WR_testdate
        wr_bulkmain_mwrwindphconn = i.WR_BulkMain_MWRwindphconn
        wr_bulkmain_mwrwindtol = i.WR_BulkMain_MWRWindTol
        wr_bulkmain_hvunit = i.WR_BulkMain_HVUnit
        wr_mwrinputhvu = i.WR_MWRInputHVU
        wr_mwrinputhvv = i.WR_MWRInputHVV
        wr_mwrinputhvw = i.WR_MWRInputHVW
        wr_normaltap_reshvtemp = i.WR_NormalTap_ResHVTemp
        wr_normaltap_reshvu = i.WR_NormalTap_ResHVU
        wr_normaltap_reshvv = i.WR_NormalTap_ResHVV
        wr_normaltap_reshvw = i.WR_NormalTap_ResHVW
        wr_normaltap_reshvavg = i.WR_NormalTap_ResHVavg
        wr_normaltap_reshv75 = i.WR_NormalTap_ResHV75
        wr_bulkmain_lvunit = i.WR_BulkMain_LVUnit
        wr_mwrinputlvu = i.WR_MWRInputLVU
        wr_mwrinputlvv = i.WR_MWRInputLVV
        wr_mwrinputlvw = i.WR_MWRInputLVW
        wr_normaltap_reslvtemp = i.WR_NormalTap_ResLVTemp
        wr_normaltap_reslvu = i.WR_NormalTap_ResLVU
        wr_normaltap_reslvv = i.WR_NormalTap_ResLVV
        wr_normaltap_reslvw = i.WR_NormalTap_ResLVW
        wr_normaltap_reslvavg = i.WR_NormalTap_ResLVavg
        wr_normaltap_reslv75 = i.WR_NormalTap_ResLV75
        wr_result = i.WR_Result
        vr_lot = i.VR_lot
        vr_testdate = i.VR_Testdate
        vr_mratioinputu = i.VR_MRatioInputU
        vr_mratioinputv = i.VR_MRatioInputV
        vr_mratioinputw = i.VR_MRatioInputW
        vr_normaltap_hvrated = i.VR_NormalTap_HVRated
        vr_normaltap_lvrated = i.VR_NormalTap_LVRated
        vr_normaltap_calratio = i.VR_NormalTap_CalRatio
        vr_normaltap_ratiou = i.VR_NormalTap_RatioU
        vr_normaltap_ratiov = i.VR_NormalTap_RatioV
        vr_normaltap_ratiow = i.VR_NormalTap_RatioW
        vr_normaltap_acccritdata = i.VR_NormalTap_AccCritData
        vr_vectordetected = i.VR_VectorDetected
        vr_result = i.VR_Result
        ir_lot = i.IR_lot
        ir_testdate = i.IR_Testdate
        ir_time = i.IR_Time
        ir_temp = i.IR_Temp
        ir_reshve = i.IR_Reshve
        ir_reslve = i.IR_Reslve
        ir_reshvlv = i.IR_Reshvlv
        ir_hve_volt = i.IR_HVE_Volt
        ir_lve_volt = i.IR_LVE_Volt
        ir_hvlv_volt = i.IR_HVLV_Volt
        ir_result = i.IR_Result
        nll_lot = i.NLL_lot
        nll_testdate = i.NLL_Testdate
        nll_bulkmain_nllguar = i.NLL_BulkMain_Nllguar
        nll_normaltap_ptr = i.NLL_NormalTap_ptr
        nll_normaltap_ctr = i.NLL_NormalTap_ctr
        nll_normaltap_frq = i.NLL_NormalTap_frq
        nll_normaltap_vrms = i.NLL_NormalTap_Vrms
        nll_normaltap_vmean = i.NLL_NormalTap_Vmean
        nll_normaltap_i1 = i.NLL_NormalTap_I1
        nll_normaltap_i2 = i.NLL_NormalTap_I2
        nll_normaltap_i3 = i.NLL_NormalTap_I3
        nll_normaltap_iavg = i.NLL_NormalTap_Iavg
        nll_normaltap_w1 = i.NLL_NormalTap_W1
        nll_normaltap_w2 = i.NLL_NormalTap_W2
        nll_normaltap_w3 = i.NLL_NormalTap_W3
        nll_normaltap_pmeasured = i.NLL_NormalTap_Pmeasured
        nll_normaltap_pcorrected = i.NLL_NormalTap_Pcorrected
        nll_result = i.NLL_Result
        ll_lot = i.LL_lot
        ll_testdate = i.LL_Testdate
        ll_bulkmain_llguar50 = i.LL_BulkMain_llguar50
        ll_bulkmain_llguar100 = i.LL_BulkMain_llguar100
        ll_normaltap_ptr = i.LL_NormalTap_ptr
        ll_normaltap_ctr = i.LL_NormalTap_ctr
        ll_normaltap_50per_temp = i.LL_NormalTap_50per_Temp
        ll_normaltap_50per_frq = i.LL_NormalTap_50per_frq
        ll_normaltap_50per_vmeas = i.LL_NormalTap_50per_Vmeas
        ll_normaltap_50per_i1 = i.LL_NormalTap_50per_I1
        ll_normaltap_50per_i2 = i.LL_NormalTap_50per_I2
        ll_normaltap_50per_i3 = i.LL_NormalTap_50per_I3
        ll_normaltap_50per_imeas = i.LL_NormalTap_50per_Imeas
        ll_normaltap_50per_w1 = i.LL_NormalTap_50per_W1
        ll_normaltap_50per_w2 = i.LL_NormalTap_50per_W2
        ll_normaltap_50per_w3 = i.LL_NormalTap_50per_W3
        ll_normaltap_50per_pmeasured = i.LL_NormalTap_50per_Pmeasured
        ll_normaltap_50per_llat75 = i.LL_NormalTap_50per_LLat75
        ll_normaltap_50per_zat75 = i.LL_NormalTap_50per_Zat75
        ll_normaltap_100per_temp = i.LL_NormalTap_100per_Temp
        ll_normaltap_100per_frq = i.LL_NormalTap_100per_frq
        ll_normaltap_100per_vmeas = i.LL_NormalTap_100per_Vmeas
        ll_normaltap_100per_i1 = i.LL_NormalTap_100per_I1
        ll_normaltap_100per_i2 = i.LL_NormalTap_100per_I2
        ll_normaltap_100per_i3 = i.LL_NormalTap_100per_I3
        ll_normaltap_100per_imeas = i.LL_NormalTap_100per_Imeas
        ll_normaltap_100per_w1 = i.LL_NormalTap_100per_W1
        ll_normaltap_100per_w2 = i.LL_NormalTap_100per_W2
        ll_normaltap_100per_w3 = i.LL_NormalTap_100per_W3
        ll_normaltap_100per_pmeasured = i.LL_NormalTap_100per_Pmeasured
        ll_normaltap_100per_llat75 = i.LL_NormalTap_100per_LLat75
        ll_normaltap_100per_zat75 = i.LL_NormalTap_100per_Zat75
        ll_percimpedancevoltreq = i.LL_PercImpedanceVoltReq
        ll_percimpedancevoltobtained = i.LL_PercImpedanceVoltObtained
        ll_percimpedancevoltremark = i.LL_PercImpedanceVoltRemark
        ll_totalloss50perreq = i.LL_TotalLoss50PerReq
        ll_totalloss50perobtained = i.LL_TotalLoss50PerObtained
        ll_totalloss50perremark = i.LL_TotalLoss50PerRemark
        ll_totalloss100perreq = i.LL_TotalLoss100PerReq
        ll_totalloss100perobtained = i.LL_TotalLoss100PerObtained
        ll_totalloss100perremark = i.LL_TotalLoss100PerRemark
        hvt_iovt_lot = i.HVT_IOVT_lot
        hvt_iovt_testdate = i.HVT_IOVT_Testdate
        hvt_iovt_ptr = i.HVT_IOVT_ptr
        hvt_iovtctr = i.HVT_IOVTctr
        hvt_hvdetail = i.HVT_HVDetail
        hvt_lvdetail = i.HVT_LVDetail
        hvt_result = i.HVT_Result
        iovt_hvdetail = i.IOVT_HVDetail
        iovt_result = i.IOVT_Result

        if not nabl_report_data.objects.filter(torder_samplecode=torder_samplecode).exists():
            nrd_obj = nabl_report_data(trf_id = 0, reportno=reportno,ulrno=ulrno,manufacturer_wopo=manufacturer_wopo,manufacturer=manufacturer,
            wo_po=wo_po,srno=srno,lot=lot,mainid=mainid,maindetid=maindetid,bulkmain_tfcondition=bulkmain_tfcondition,
            bulkmain_phase=bulkmain_phase,bulkmain_windingtype=bulkmain_windingtype,bulkmain_vector=bulkmain_vector,
            bulkmain_win_descg1=bulkmain_win_descg1,bulkmain_win_descg2=bulkmain_win_descg2,bulkmain_cooling=bulkmain_cooling,
            bulkmain_prim_mva=bulkmain_prim_mva,bulkmain_sec_mva=bulkmain_sec_mva,bulkmain_prim_ratedvol=bulkmain_prim_ratedvol,
            bulkmain_sec_ratedvol=bulkmain_sec_ratedvol,bulkmain_prim_ratedcur=bulkmain_prim_ratedcur,
            bulkmain_sec_ratedcur=bulkmain_sec_ratedcur,bulkmain_prim_conn=bulkmain_prim_conn,bulkmain_sec_conn=bulkmain_sec_conn,
            bulkmain_prim_not1=bulkmain_prim_not1,bulkmain_prim_not2=bulkmain_prim_not2,bulkmain_prim_not3=bulkmain_prim_not3,
            bulkmain_prim_not4=bulkmain_prim_not4,bulkmain_sec_not1=bulkmain_sec_not1,bulkmain_sec_not2=bulkmain_sec_not2,
            bulkmain_sec_not3=bulkmain_sec_not3,bulkmain_sec_not4=bulkmain_sec_not4,bulkmain_temp_oil=bulkmain_temp_oil,
            bulkmain_temp_wind=bulkmain_temp_wind,bulkmain_windingmaterial=bulkmain_windingmaterial,bulkmain_metalval=bulkmain_metalval,
            bulkmain_refstd=bulkmain_refstd,bulkmain_jobrating=bulkmain_jobrating,bulkmain_reftemp=bulkmain_reftemp,
            bulkmain_freq=bulkmain_freq,bulkmain_oilleakage=bulkmain_oilleakage,bulkmain_oilquantity=bulkmain_oilquantity,
            bulkmain_total_loss=bulkmain_total_loss,bulkmain_tap_changer=bulkmain_tap_changer,bulkmain_tapon=bulkmain_tapon,
            bulkmain_variation=bulkmain_variation,bulkmain_volts1=bulkmain_volts1,bulkmain_volts2=bulkmain_volts2,
            bulkmain_persteps=bulkmain_persteps,bulkmain_steps=bulkmain_steps,torder_scheduleoftest=torder_scheduleoftest,
            torder_dateofreceipt=torder_dateofreceipt,torder_dateoftestingfrom=torder_dateoftestingfrom,
            torder_dateoftestingto=torder_dateoftestingto,torder_dateofissue=torder_dateofissue,torder_samplecode=torder_samplecode,
            torder_customernameaddress=torder_customernameaddress,torder_note1=torder_note1,torder_note2=torder_note2,
            torder_note3=torder_note3,torder_note4=torder_note4,tfooter_1testedbylabel=tfooter_1testedbylabel,
            torder_1testedbyname=torder_1testedbyname,torder_1testedbydesign=torder_1testedbydesign,
            tfooter_2checkedbylabel=tfooter_2checkedbylabel,torder_2checkedbyname=torder_2checkedbyname,
            torder_2checkedbydesign=torder_2checkedbydesign,tfooter_3approvedbylabel=tfooter_3approvedbylabel,
            torder_3approvedbyname=torder_3approvedbyname,torder_3approvedbydesign=torder_3approvedbydesign,
            tfooter_4hodlabel=tfooter_4hodlabel,torder_4hodname=torder_4hodname,torder_4hoddesign=torder_4hoddesign,
            tfooter_witnessbylabel=tfooter_witnessbylabel,torder_witnessbyname1=torder_witnessbyname1,
            torder_witnessbydesign1=torder_witnessbydesign1,torder_witnessbyname2=torder_witnessbyname2,
            torder_witnessbydesign2=torder_witnessbydesign2,torder_witnessbyname3=torder_witnessbyname3,
            torder_witnessbydesign3=torder_witnessbydesign3,torder_witnessbyname4=torder_witnessbyname4,
            torder_witnessbydesign4=torder_witnessbydesign4,normaltapno=normaltapno,totaltapqty=totaltapqty,wr_lot=wr_lot,
            wr_testdate=wr_testdate,wr_bulkmain_mwrwindphconn=wr_bulkmain_mwrwindphconn,wr_bulkmain_mwrwindtol=wr_bulkmain_mwrwindtol,
            wr_bulkmain_hvunit=wr_bulkmain_hvunit,wr_mwrinputhvu=wr_mwrinputhvu,wr_mwrinputhvv=wr_mwrinputhvv,
            wr_mwrinputhvw=wr_mwrinputhvw,wr_normaltap_reshvtemp=wr_normaltap_reshvtemp,wr_normaltap_reshvu=wr_normaltap_reshvu,
            wr_normaltap_reshvv=wr_normaltap_reshvv,wr_normaltap_reshvw=wr_normaltap_reshvw,wr_normaltap_reshvavg=wr_normaltap_reshvavg,
            wr_normaltap_reshv75=wr_normaltap_reshv75,wr_bulkmain_lvunit=wr_bulkmain_lvunit,wr_mwrinputlvu=wr_mwrinputlvu,
            wr_mwrinputlvv=wr_mwrinputlvv,wr_mwrinputlvw=wr_mwrinputlvw,wr_normaltap_reslvtemp=wr_normaltap_reslvtemp,
            wr_normaltap_reslvu=wr_normaltap_reslvu,wr_normaltap_reslvv=wr_normaltap_reslvv,wr_normaltap_reslvw=wr_normaltap_reslvw,
            wr_normaltap_reslvavg=wr_normaltap_reslvavg,wr_normaltap_reslv75=wr_normaltap_reslv75,wr_result=wr_result,
            vr_lot=vr_lot,vr_testdate=vr_testdate,vr_mratioinputu=vr_mratioinputu,vr_mratioinputv=vr_mratioinputv,
            vr_mratioinputw=vr_mratioinputw,vr_normaltap_hvrated=vr_normaltap_hvrated,vr_normaltap_lvrated=vr_normaltap_lvrated,
            vr_normaltap_calratio=vr_normaltap_calratio,vr_normaltap_ratiou=vr_normaltap_ratiou,vr_normaltap_ratiov=vr_normaltap_ratiov,
            vr_normaltap_ratiow=vr_normaltap_ratiow,vr_normaltap_acccritdata=vr_normaltap_acccritdata,
            vr_vectordetected=vr_vectordetected,vr_result=vr_result,ir_lot=ir_lot,ir_testdate=ir_testdate,ir_time=ir_time,
            ir_temp=ir_temp,ir_reshve=ir_reshve,ir_reslve=ir_reslve,ir_reshvlv=ir_reshvlv,ir_hve_volt=ir_hve_volt,
            ir_lve_volt=ir_lve_volt,ir_hvlv_volt=ir_hvlv_volt,ir_result=ir_result,nll_lot=nll_lot,nll_testdate=nll_testdate,
            nll_bulkmain_nllguar=nll_bulkmain_nllguar,nll_normaltap_ptr=nll_normaltap_ptr,nll_normaltap_ctr=nll_normaltap_ctr,
            nll_normaltap_frq=nll_normaltap_frq,nll_normaltap_vrms=nll_normaltap_vrms,nll_normaltap_vmean=nll_normaltap_vmean,
            nll_normaltap_i1=nll_normaltap_i1,nll_normaltap_i2=nll_normaltap_i2,nll_normaltap_i3=nll_normaltap_i3,
            nll_normaltap_iavg=nll_normaltap_iavg,nll_normaltap_w1=nll_normaltap_w1,nll_normaltap_w2=nll_normaltap_w2,
            nll_normaltap_w3=nll_normaltap_w3,nll_normaltap_pmeasured=nll_normaltap_pmeasured,nll_normaltap_pcorrected=nll_normaltap_pcorrected,
            nll_result=nll_result,ll_lot=ll_lot,ll_testdate=ll_testdate,ll_bulkmain_llguar50=ll_bulkmain_llguar50,
            ll_bulkmain_llguar100=ll_bulkmain_llguar100,ll_normaltap_ptr=ll_normaltap_ptr,ll_normaltap_ctr=ll_normaltap_ctr,
            ll_normaltap_50per_temp=ll_normaltap_50per_temp,ll_normaltap_50per_frq=ll_normaltap_50per_frq,
            ll_normaltap_50per_vmeas=ll_normaltap_50per_vmeas,ll_normaltap_50per_i1=ll_normaltap_50per_i1,
            ll_normaltap_50per_i2=ll_normaltap_50per_i2,ll_normaltap_50per_i3=ll_normaltap_50per_i3,
            ll_normaltap_50per_imeas=ll_normaltap_50per_imeas,ll_normaltap_50per_w1=ll_normaltap_50per_w1,
            ll_normaltap_50per_w2=ll_normaltap_50per_w2,ll_normaltap_50per_w3=ll_normaltap_50per_w3,
            ll_normaltap_50per_pmeasured=ll_normaltap_50per_pmeasured,ll_normaltap_50per_llat75=ll_normaltap_50per_llat75,
            ll_normaltap_50per_zat75=ll_normaltap_50per_zat75,ll_normaltap_100per_temp=ll_normaltap_100per_temp,
            ll_normaltap_100per_frq=ll_normaltap_100per_frq,ll_normaltap_100per_vmeas=ll_normaltap_100per_vmeas,
            ll_normaltap_100per_i1=ll_normaltap_100per_i1,ll_normaltap_100per_i2=ll_normaltap_100per_i2,
            ll_normaltap_100per_i3=ll_normaltap_100per_i3,ll_normaltap_100per_imeas=ll_normaltap_100per_imeas,
            ll_normaltap_100per_w1=ll_normaltap_100per_w1,ll_normaltap_100per_w2=ll_normaltap_100per_w2,
            ll_normaltap_100per_w3=ll_normaltap_100per_w3,ll_normaltap_100per_pmeasured=ll_normaltap_100per_pmeasured,
            ll_normaltap_100per_llat75=ll_normaltap_100per_llat75,ll_normaltap_100per_zat75=ll_normaltap_100per_zat75,
            ll_percimpedancevoltreq=ll_percimpedancevoltreq,ll_percimpedancevoltobtained=ll_percimpedancevoltobtained,
            ll_percimpedancevoltremark=ll_percimpedancevoltremark,ll_totalloss50perreq=ll_totalloss50perreq,
            ll_totalloss50perobtained=ll_totalloss50perobtained,ll_totalloss50perremark=ll_totalloss50perremark,
            ll_totalloss100perreq=ll_totalloss100perreq,ll_totalloss100perobtained=ll_totalloss100perobtained,
            ll_totalloss100perremark=ll_totalloss100perremark,hvt_iovt_lot=hvt_iovt_lot,hvt_iovt_testdate=hvt_iovt_testdate,
            hvt_iovt_ptr=hvt_iovt_ptr,hvt_iovtctr=hvt_iovtctr,hvt_hvdetail=hvt_hvdetail,hvt_lvdetail=hvt_lvdetail,
            hvt_result=hvt_result,iovt_hvdetail=iovt_hvdetail,iovt_result=iovt_result)
            nrd_obj.save()
        else:
            pass

        sample_code_lst.append(torder_samplecode)

    if request.method == "POST":
        search = request.POST.get('search')
        return redirect('Report_success_view/'+search )

    return render(request, 'officer/tmqm_report_success.html', {'sample_code_lst': sample_code_lst} )

# import pyodbc
# def Report_success_rca(request):
#     cnxn = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
#                     server='172.16.9.103',
#                     database='TTPGeneric',
#                     uid='sa',
#                     pwd='pejk7UNj',
#                     port='1433'
#                     )
#     cur = cnxn.cursor()
#     cur.execute('SELECT * from "AllData_TATTestFreezed"')
#     rows = cur.fetchall()

#     sample_code_lst = []
#     for i in rows:
#         reportno = i.ReportNo
#         ulrno = i.ULRNo
#         manufacturer_wopo = i.Manufacturer_WOPO
#         manufacturer = i.Manufacturer
#         wo_po = i.WO_PO
#         srno = i.srno
#         lot = i.lot
#         mainid = i.MainID
#         maindetid = i.MainDETID
#         bulkmain_tfcondition = i.BulkMain_TfCondition
#         bulkmain_phase = i.BulkMain_Phase
#         bulkmain_windingtype = i.BulkMain_WindingType
#         bulkmain_vector = i.BulkMain_Vector
#         bulkmain_win_descg1 = i.BulkMain_win_descg1
#         bulkmain_win_descg2 = i.BulkMain_win_descg2
#         bulkmain_cooling = i.BulkMain_Cooling
#         bulkmain_prim_mva = i.BulkMain_Prim_MVA
#         bulkmain_sec_mva = i.BulkMain_Sec_MVA
#         bulkmain_prim_ratedvol = i.BulkMain_Prim_RatedVol
#         bulkmain_sec_ratedvol = i.BulkMain_Sec_RatedVol
#         bulkmain_prim_ratedcur = i.BulkMain_Prim_RatedCur
#         bulkmain_sec_ratedcur = i.BulkMain_Sec_RatedCur
#         bulkmain_prim_conn = i.BulkMain_Prim_Conn
#         bulkmain_sec_conn = i.BulkMain_Sec_Conn
#         bulkmain_prim_not1 = i.BulkMain_Prim_not1
#         bulkmain_prim_not2 = i.BulkMain_Prim_not2
#         bulkmain_prim_not3 = i.BulkMain_Prim_not3
#         bulkmain_prim_not4 = i.BulkMain_Prim_not4
#         bulkmain_sec_not1 = i.BulkMain_Sec_not1
#         bulkmain_sec_not2 = i.BulkMain_Sec_not2 
#         bulkmain_sec_not3 = i.BulkMain_Sec_not3 
#         bulkmain_sec_not4 = i.BulkMain_Sec_not4 
#         bulkmain_temp_oil = i.BulkMain_Temp_Oil
#         bulkmain_temp_wind = i.BulkMain_Temp_Wind
#         bulkmain_windingmaterial = i.BulkMain_WindingMaterial 
#         bulkmain_metalval = i.BulkMain_MetalVal 
#         bulkmain_refstd = i.BulkMain_refstd 
#         bulkmain_jobrating = i.BulkMain_jobrating 
#         bulkmain_reftemp = i.BulkMain_RefTemp 
#         bulkmain_freq = i.BulkMain_freq
#         bulkmain_oilleakage = i.BulkMain_oilleakage
#         bulkmain_oilquantity = i.BulkMain_OilQuantity
#         bulkmain_total_loss = i.BulkMain_total_loss
#         bulkmain_tap_changer = i.BulkMain_tap_changer
#         bulkmain_tapon = i.BulkMain_tapon
#         bulkmain_variation = i.BulkMain_variation
#         bulkmain_volts1 = i.BulkMain_volts1
#         bulkmain_volts2 = i.BulkMain_volts2
#         bulkmain_persteps = i.BulkMain_persteps
#         bulkmain_steps = i.BulkMain_steps
#         torder_scheduleoftest = i.TOrder_ScheduleOfTest
#         torder_dateofreceipt = i.TOrder_DateOfReceipt
#         torder_dateoftestingfrom = i.TOrder_DateOfTestingFrom
#         torder_dateoftestingto = i.TOrder_DateOfTestingTo
#         torder_dateofissue = i.TOrder_DateOfIssue
#         torder_samplecode = i.TOrder_SampleCode
#         torder_customernameaddress = i.TOrder_CustomerNameAddress
#         torder_note1 = i.TOrder_Note1
#         torder_note2 = i.TOrder_Note2
#         torder_note3 = i.TOrder_Note3
#         torder_note4 = i.TOrder_Note4
#         tfooter_1testedbylabel = i.TFooter_1TestedByLabel
#         torder_1testedbyname = i.TOrder_1TestedByName
#         torder_1testedbydesign = i.TOrder_1TestedByDesign
#         tfooter_2checkedbylabel = i.TFooter_2CheckedByLabel
#         torder_2checkedbyname = i.TOrder_2CheckedByName
#         torder_2checkedbydesign = i.TOrder_2CheckedByDesign
#         tfooter_3approvedbylabel = i.TFooter_3ApprovedByLabel
#         torder_3approvedbyname = i.TOrder_3ApprovedByName
#         torder_3approvedbydesign = i.TOrder_3ApprovedByDesign
#         tfooter_4hodlabel = i.TFooter_4HODLabel
#         torder_4hodname = i.TOrder_4HODName
#         torder_4hoddesign = i.TOrder_4HODDesign
#         tfooter_witnessbylabel = i.TFooter_WitnessByLabel
#         torder_witnessbyname1 = i.TOrder_WitnessByName1
#         torder_witnessbydesign1 = i.TOrder_WitnessByDesign1
#         torder_witnessbyname2 = i.TOrder_WitnessByName2
#         torder_witnessbydesign2 = i.TOrder_WitnessByDesign2
#         torder_witnessbyname3 = i.TOrder_WitnessByName3
#         torder_witnessbydesign3 = i.TOrder_WitnessByDesign3
#         torder_witnessbyname4 = i.TOrder_WitnessByName4
#         torder_witnessbydesign4 = i.TOrder_WitnessByDesign4
#         normaltapno = i.NormalTapNo
#         totaltapqty = i.TotalTapQty
#         wr_lot = i.WR_lot
#         wr_testdate = i.WR_testdate
#         wr_bulkmain_mwrwindphconn = i.WR_BulkMain_MWRwindphconn
#         wr_bulkmain_mwrwindtol = i.WR_BulkMain_MWRWindTol
#         wr_bulkmain_hvunit = i.WR_BulkMain_HVUnit
#         wr_mwrinputhvu = i.WR_MWRInputHVU
#         wr_mwrinputhvv = i.WR_MWRInputHVV
#         wr_mwrinputhvw = i.WR_MWRInputHVW
#         wr_normaltap_reshvtemp = i.WR_NormalTap_ResHVTemp
#         wr_normaltap_reshvu = i.WR_NormalTap_ResHVU
#         wr_normaltap_reshvv = i.WR_NormalTap_ResHVV
#         wr_normaltap_reshvw = i.WR_NormalTap_ResHVW
#         wr_normaltap_reshvavg = i.WR_NormalTap_ResHVavg
#         wr_normaltap_reshv75 = i.WR_NormalTap_ResHV75
#         wr_bulkmain_lvunit = i.WR_BulkMain_LVUnit
#         wr_mwrinputlvu = i.WR_MWRInputLVU
#         wr_mwrinputlvv = i.WR_MWRInputLVV
#         wr_mwrinputlvw = i.WR_MWRInputLVW
#         wr_normaltap_reslvtemp = i.WR_NormalTap_ResLVTemp
#         wr_normaltap_reslvu = i.WR_NormalTap_ResLVU
#         wr_normaltap_reslvv = i.WR_NormalTap_ResLVV
#         wr_normaltap_reslvw = i.WR_NormalTap_ResLVW
#         wr_normaltap_reslvavg = i.WR_NormalTap_ResLVavg
#         wr_normaltap_reslv75 = i.WR_NormalTap_ResLV75
#         wr_result = i.WR_Result
#         vr_lot = i.VR_lot
#         vr_testdate = i.VR_Testdate
#         vr_mratioinputu = i.VR_MRatioInputU
#         vr_mratioinputv = i.VR_MRatioInputV
#         vr_mratioinputw = i.VR_MRatioInputW
#         vr_normaltap_hvrated = i.VR_NormalTap_HVRated
#         vr_normaltap_lvrated = i.VR_NormalTap_LVRated
#         vr_normaltap_calratio = i.VR_NormalTap_CalRatio
#         vr_normaltap_ratiou = i.VR_NormalTap_RatioU
#         vr_normaltap_ratiov = i.VR_NormalTap_RatioV
#         vr_normaltap_ratiow = i.VR_NormalTap_RatioW
#         vr_normaltap_acccritdata = i.VR_NormalTap_AccCritData
#         vr_vectordetected = i.VR_VectorDetected
#         vr_result = i.VR_Result
#         ir_lot = i.IR_lot
#         ir_testdate = i.IR_Testdate
#         ir_time = i.IR_Time
#         ir_temp = i.IR_Temp
#         ir_reshve = i.IR_Reshve
#         ir_reslve = i.IR_Reslve
#         ir_reshvlv = i.IR_Reshvlv
#         ir_hve_volt = i.IR_HVE_Volt
#         ir_lve_volt = i.IR_LVE_Volt
#         ir_hvlv_volt = i.IR_HVLV_Volt
#         ir_result = i.IR_Result
#         nll_lot = i.NLL_lot
#         nll_testdate = i.NLL_Testdate
#         nll_bulkmain_nllguar = i.NLL_BulkMain_Nllguar
#         nll_normaltap_ptr = i.NLL_NormalTap_ptr
#         nll_normaltap_ctr = i.NLL_NormalTap_ctr
#         nll_normaltap_frq = i.NLL_NormalTap_frq
#         nll_normaltap_vrms = i.NLL_NormalTap_Vrms
#         nll_normaltap_vmean = i.NLL_NormalTap_Vmean
#         nll_normaltap_i1 = i.NLL_NormalTap_I1
#         nll_normaltap_i2 = i.NLL_NormalTap_I2
#         nll_normaltap_i3 = i.NLL_NormalTap_I3
#         nll_normaltap_iavg = i.NLL_NormalTap_Iavg
#         nll_normaltap_w1 = i.NLL_NormalTap_W1
#         nll_normaltap_w2 = i.NLL_NormalTap_W2
#         nll_normaltap_w3 = i.NLL_NormalTap_W3
#         nll_normaltap_pmeasured = i.NLL_NormalTap_Pmeasured
#         nll_normaltap_pcorrected = i.NLL_NormalTap_Pcorrected
#         nll_result = i.NLL_Result
#         ll_lot = i.LL_lot
#         ll_testdate = i.LL_Testdate
#         ll_bulkmain_llguar50 = i.LL_BulkMain_llguar50
#         ll_bulkmain_llguar100 = i.LL_BulkMain_llguar100
#         ll_normaltap_ptr = i.LL_NormalTap_ptr
#         ll_normaltap_ctr = i.LL_NormalTap_ctr
#         ll_normaltap_50per_temp = i.LL_NormalTap_50per_Temp
#         ll_normaltap_50per_frq = i.LL_NormalTap_50per_frq
#         ll_normaltap_50per_vmeas = i.LL_NormalTap_50per_Vmeas
#         ll_normaltap_50per_i1 = i.LL_NormalTap_50per_I1
#         ll_normaltap_50per_i2 = i.LL_NormalTap_50per_I2
#         ll_normaltap_50per_i3 = i.LL_NormalTap_50per_I3
#         ll_normaltap_50per_imeas = i.LL_NormalTap_50per_Imeas
#         ll_normaltap_50per_w1 = i.LL_NormalTap_50per_W1
#         ll_normaltap_50per_w2 = i.LL_NormalTap_50per_W2
#         ll_normaltap_50per_w3 = i.LL_NormalTap_50per_W3
#         ll_normaltap_50per_pmeasured = i.LL_NormalTap_50per_Pmeasured
#         ll_normaltap_50per_llat75 = i.LL_NormalTap_50per_LLat75
#         ll_normaltap_50per_zat75 = i.LL_NormalTap_50per_Zat75
#         ll_normaltap_100per_temp = i.LL_NormalTap_100per_Temp
#         ll_normaltap_100per_frq = i.LL_NormalTap_100per_frq
#         ll_normaltap_100per_vmeas = i.LL_NormalTap_100per_Vmeas
#         ll_normaltap_100per_i1 = i.LL_NormalTap_100per_I1
#         ll_normaltap_100per_i2 = i.LL_NormalTap_100per_I2
#         ll_normaltap_100per_i3 = i.LL_NormalTap_100per_I3
#         ll_normaltap_100per_imeas = i.LL_NormalTap_100per_Imeas
#         ll_normaltap_100per_w1 = i.LL_NormalTap_100per_W1
#         ll_normaltap_100per_w2 = i.LL_NormalTap_100per_W2
#         ll_normaltap_100per_w3 = i.LL_NormalTap_100per_W3
#         ll_normaltap_100per_pmeasured = i.LL_NormalTap_100per_Pmeasured
#         ll_normaltap_100per_llat75 = i.LL_NormalTap_100per_LLat75
#         ll_normaltap_100per_zat75 = i.LL_NormalTap_100per_Zat75
#         ll_percimpedancevoltreq = i.LL_PercImpedanceVoltReq
#         ll_percimpedancevoltobtained = i.LL_PercImpedanceVoltObtained
#         ll_percimpedancevoltremark = i.LL_PercImpedanceVoltRemark
#         ll_totalloss50perreq = i.LL_TotalLoss50PerReq
#         ll_totalloss50perobtained = i.LL_TotalLoss50PerObtained
#         ll_totalloss50perremark = i.LL_TotalLoss50PerRemark
#         ll_totalloss100perreq = i.LL_TotalLoss100PerReq
#         ll_totalloss100perobtained = i.LL_TotalLoss100PerObtained
#         ll_totalloss100perremark = i.LL_TotalLoss100PerRemark
#         hvt_iovt_lot = i.HVT_IOVT_lot
#         hvt_iovt_testdate = i.HVT_IOVT_Testdate
#         hvt_iovt_ptr = i.HVT_IOVT_ptr
#         hvt_iovtctr = i.HVT_IOVTctr
#         hvt_hvdetail = i.HVT_HVDetail
#         hvt_lvdetail = i.HVT_LVDetail
#         hvt_result = i.HVT_Result
#         iovt_hvdetail = i.IOVT_HVDetail
#         iovt_result = i.IOVT_Result

#         if not nabl_report_data_rca.objects.filter(torder_samplecode=torder_samplecode).exists():
#             nrd_obj = nabl_report_data_rca(trf_id = 0, reportno=reportno,ulrno=ulrno,manufacturer_wopo=manufacturer_wopo,manufacturer=manufacturer,
#             wo_po=wo_po,srno=srno,lot=lot,mainid=mainid,maindetid=maindetid,bulkmain_tfcondition=bulkmain_tfcondition,
#             bulkmain_phase=bulkmain_phase,bulkmain_windingtype=bulkmain_windingtype,bulkmain_vector=bulkmain_vector,
#             bulkmain_win_descg1=bulkmain_win_descg1,bulkmain_win_descg2=bulkmain_win_descg2,bulkmain_cooling=bulkmain_cooling,
#             bulkmain_prim_mva=bulkmain_prim_mva,bulkmain_sec_mva=bulkmain_sec_mva,bulkmain_prim_ratedvol=bulkmain_prim_ratedvol,
#             bulkmain_sec_ratedvol=bulkmain_sec_ratedvol,bulkmain_prim_ratedcur=bulkmain_prim_ratedcur,
#             bulkmain_sec_ratedcur=bulkmain_sec_ratedcur,bulkmain_prim_conn=bulkmain_prim_conn,bulkmain_sec_conn=bulkmain_sec_conn,
#             bulkmain_prim_not1=bulkmain_prim_not1,bulkmain_prim_not2=bulkmain_prim_not2,bulkmain_prim_not3=bulkmain_prim_not3,
#             bulkmain_prim_not4=bulkmain_prim_not4,bulkmain_sec_not1=bulkmain_sec_not1,bulkmain_sec_not2=bulkmain_sec_not2,
#             bulkmain_sec_not3=bulkmain_sec_not3,bulkmain_sec_not4=bulkmain_sec_not4,bulkmain_temp_oil=bulkmain_temp_oil,
#             bulkmain_temp_wind=bulkmain_temp_wind,bulkmain_windingmaterial=bulkmain_windingmaterial,bulkmain_metalval=bulkmain_metalval,
#             bulkmain_refstd=bulkmain_refstd,bulkmain_jobrating=bulkmain_jobrating,bulkmain_reftemp=bulkmain_reftemp,
#             bulkmain_freq=bulkmain_freq,bulkmain_oilleakage=bulkmain_oilleakage,bulkmain_oilquantity=bulkmain_oilquantity,
#             bulkmain_total_loss=bulkmain_total_loss,bulkmain_tap_changer=bulkmain_tap_changer,bulkmain_tapon=bulkmain_tapon,
#             bulkmain_variation=bulkmain_variation,bulkmain_volts1=bulkmain_volts1,bulkmain_volts2=bulkmain_volts2,
#             bulkmain_persteps=bulkmain_persteps,bulkmain_steps=bulkmain_steps,torder_scheduleoftest=torder_scheduleoftest,
#             torder_dateofreceipt=torder_dateofreceipt,torder_dateoftestingfrom=torder_dateoftestingfrom,
#             torder_dateoftestingto=torder_dateoftestingto,torder_dateofissue=torder_dateofissue,torder_samplecode=torder_samplecode,
#             torder_customernameaddress=torder_customernameaddress,torder_note1=torder_note1,torder_note2=torder_note2,
#             torder_note3=torder_note3,torder_note4=torder_note4,tfooter_1testedbylabel=tfooter_1testedbylabel,
#             torder_1testedbyname=torder_1testedbyname,torder_1testedbydesign=torder_1testedbydesign,
#             tfooter_2checkedbylabel=tfooter_2checkedbylabel,torder_2checkedbyname=torder_2checkedbyname,
#             torder_2checkedbydesign=torder_2checkedbydesign,tfooter_3approvedbylabel=tfooter_3approvedbylabel,
#             torder_3approvedbyname=torder_3approvedbyname,torder_3approvedbydesign=torder_3approvedbydesign,
#             tfooter_4hodlabel=tfooter_4hodlabel,torder_4hodname=torder_4hodname,torder_4hoddesign=torder_4hoddesign,
#             tfooter_witnessbylabel=tfooter_witnessbylabel,torder_witnessbyname1=torder_witnessbyname1,
#             torder_witnessbydesign1=torder_witnessbydesign1,torder_witnessbyname2=torder_witnessbyname2,
#             torder_witnessbydesign2=torder_witnessbydesign2,torder_witnessbyname3=torder_witnessbyname3,
#             torder_witnessbydesign3=torder_witnessbydesign3,torder_witnessbyname4=torder_witnessbyname4,
#             torder_witnessbydesign4=torder_witnessbydesign4,normaltapno=normaltapno,totaltapqty=totaltapqty,wr_lot=wr_lot,
#             wr_testdate=wr_testdate,wr_bulkmain_mwrwindphconn=wr_bulkmain_mwrwindphconn,wr_bulkmain_mwrwindtol=wr_bulkmain_mwrwindtol,
#             wr_bulkmain_hvunit=wr_bulkmain_hvunit,wr_mwrinputhvu=wr_mwrinputhvu,wr_mwrinputhvv=wr_mwrinputhvv,
#             wr_mwrinputhvw=wr_mwrinputhvw,wr_normaltap_reshvtemp=wr_normaltap_reshvtemp,wr_normaltap_reshvu=wr_normaltap_reshvu,
#             wr_normaltap_reshvv=wr_normaltap_reshvv,wr_normaltap_reshvw=wr_normaltap_reshvw,wr_normaltap_reshvavg=wr_normaltap_reshvavg,
#             wr_normaltap_reshv75=wr_normaltap_reshv75,wr_bulkmain_lvunit=wr_bulkmain_lvunit,wr_mwrinputlvu=wr_mwrinputlvu,
#             wr_mwrinputlvv=wr_mwrinputlvv,wr_mwrinputlvw=wr_mwrinputlvw,wr_normaltap_reslvtemp=wr_normaltap_reslvtemp,
#             wr_normaltap_reslvu=wr_normaltap_reslvu,wr_normaltap_reslvv=wr_normaltap_reslvv,wr_normaltap_reslvw=wr_normaltap_reslvw,
#             wr_normaltap_reslvavg=wr_normaltap_reslvavg,wr_normaltap_reslv75=wr_normaltap_reslv75,wr_result=wr_result,
#             vr_lot=vr_lot,vr_testdate=vr_testdate,vr_mratioinputu=vr_mratioinputu,vr_mratioinputv=vr_mratioinputv,
#             vr_mratioinputw=vr_mratioinputw,vr_normaltap_hvrated=vr_normaltap_hvrated,vr_normaltap_lvrated=vr_normaltap_lvrated,
#             vr_normaltap_calratio=vr_normaltap_calratio,vr_normaltap_ratiou=vr_normaltap_ratiou,vr_normaltap_ratiov=vr_normaltap_ratiov,
#             vr_normaltap_ratiow=vr_normaltap_ratiow,vr_normaltap_acccritdata=vr_normaltap_acccritdata,
#             vr_vectordetected=vr_vectordetected,vr_result=vr_result,ir_lot=ir_lot,ir_testdate=ir_testdate,ir_time=ir_time,
#             ir_temp=ir_temp,ir_reshve=ir_reshve,ir_reslve=ir_reslve,ir_reshvlv=ir_reshvlv,ir_hve_volt=ir_hve_volt,
#             ir_lve_volt=ir_lve_volt,ir_hvlv_volt=ir_hvlv_volt,ir_result=ir_result,nll_lot=nll_lot,nll_testdate=nll_testdate,
#             nll_bulkmain_nllguar=nll_bulkmain_nllguar,nll_normaltap_ptr=nll_normaltap_ptr,nll_normaltap_ctr=nll_normaltap_ctr,
#             nll_normaltap_frq=nll_normaltap_frq,nll_normaltap_vrms=nll_normaltap_vrms,nll_normaltap_vmean=nll_normaltap_vmean,
#             nll_normaltap_i1=nll_normaltap_i1,nll_normaltap_i2=nll_normaltap_i2,nll_normaltap_i3=nll_normaltap_i3,
#             nll_normaltap_iavg=nll_normaltap_iavg,nll_normaltap_w1=nll_normaltap_w1,nll_normaltap_w2=nll_normaltap_w2,
#             nll_normaltap_w3=nll_normaltap_w3,nll_normaltap_pmeasured=nll_normaltap_pmeasured,nll_normaltap_pcorrected=nll_normaltap_pcorrected,
#             nll_result=nll_result,ll_lot=ll_lot,ll_testdate=ll_testdate,ll_bulkmain_llguar50=ll_bulkmain_llguar50,
#             ll_bulkmain_llguar100=ll_bulkmain_llguar100,ll_normaltap_ptr=ll_normaltap_ptr,ll_normaltap_ctr=ll_normaltap_ctr,
#             ll_normaltap_50per_temp=ll_normaltap_50per_temp,ll_normaltap_50per_frq=ll_normaltap_50per_frq,
#             ll_normaltap_50per_vmeas=ll_normaltap_50per_vmeas,ll_normaltap_50per_i1=ll_normaltap_50per_i1,
#             ll_normaltap_50per_i2=ll_normaltap_50per_i2,ll_normaltap_50per_i3=ll_normaltap_50per_i3,
#             ll_normaltap_50per_imeas=ll_normaltap_50per_imeas,ll_normaltap_50per_w1=ll_normaltap_50per_w1,
#             ll_normaltap_50per_w2=ll_normaltap_50per_w2,ll_normaltap_50per_w3=ll_normaltap_50per_w3,
#             ll_normaltap_50per_pmeasured=ll_normaltap_50per_pmeasured,ll_normaltap_50per_llat75=ll_normaltap_50per_llat75,
#             ll_normaltap_50per_zat75=ll_normaltap_50per_zat75,ll_normaltap_100per_temp=ll_normaltap_100per_temp,
#             ll_normaltap_100per_frq=ll_normaltap_100per_frq,ll_normaltap_100per_vmeas=ll_normaltap_100per_vmeas,
#             ll_normaltap_100per_i1=ll_normaltap_100per_i1,ll_normaltap_100per_i2=ll_normaltap_100per_i2,
#             ll_normaltap_100per_i3=ll_normaltap_100per_i3,ll_normaltap_100per_imeas=ll_normaltap_100per_imeas,
#             ll_normaltap_100per_w1=ll_normaltap_100per_w1,ll_normaltap_100per_w2=ll_normaltap_100per_w2,
#             ll_normaltap_100per_w3=ll_normaltap_100per_w3,ll_normaltap_100per_pmeasured=ll_normaltap_100per_pmeasured,
#             ll_normaltap_100per_llat75=ll_normaltap_100per_llat75,ll_normaltap_100per_zat75=ll_normaltap_100per_zat75,
#             ll_percimpedancevoltreq=ll_percimpedancevoltreq,ll_percimpedancevoltobtained=ll_percimpedancevoltobtained,
#             ll_percimpedancevoltremark=ll_percimpedancevoltremark,ll_totalloss50perreq=ll_totalloss50perreq,
#             ll_totalloss50perobtained=ll_totalloss50perobtained,ll_totalloss50perremark=ll_totalloss50perremark,
#             ll_totalloss100perreq=ll_totalloss100perreq,ll_totalloss100perobtained=ll_totalloss100perobtained,
#             ll_totalloss100perremark=ll_totalloss100perremark,hvt_iovt_lot=hvt_iovt_lot,hvt_iovt_testdate=hvt_iovt_testdate,
#             hvt_iovt_ptr=hvt_iovt_ptr,hvt_iovtctr=hvt_iovtctr,hvt_hvdetail=hvt_hvdetail,hvt_lvdetail=hvt_lvdetail,
#             hvt_result=hvt_result,iovt_hvdetail=iovt_hvdetail,iovt_result=iovt_result)
#             nrd_obj.save()
#         else:
#             pass

#         sample_code_lst.append(torder_samplecode)

#     if request.method == "POST":
#         search = request.POST.get('search')
#         return redirect('Report_success_view_rca/'+search )

#     return render(request, 'officer/tmqm_report_success_rca.html', {'sample_code_lst': sample_code_lst} )


def Report_success_view(request, sc):
    nabl_obj = nabl_report_data.objects.filter(torder_samplecode=sc)
    for i in nabl_obj:
        bulkmain_tfcondition = i.bulkmain_tfcondition

        vr_result = i.vr_result

        nll_result = i.nll_result
        if not nll_result:
            nll_result = "Pass"

        ll_percimpedancevoltremark = i.ll_percimpedancevoltremark
        if not ll_percimpedancevoltremark:
            ll_percimpedancevoltremark = "Pass"

        ll_totalloss50perremark = i.ll_totalloss50perremark
        if not ll_totalloss50perremark:
            ll_totalloss50perremark = "Pass"

        ll_totalloss100perremark = i.ll_totalloss100perremark
        if not ll_totalloss100perremark:
            ll_totalloss100perremark = "Pass"

        hvt_result = i.hvt_result
        if not hvt_result:
            hvt_result = "Pass"

        iovt_result = i.iovt_result
        if not iovt_result:
            iovt_result = "Pass"

        output = ""
        if bulkmain_tfcondition == "Repaired":
            if vr_result == "Pass" and nll_result == "Pass" and ll_percimpedancevoltremark == "Pass" and ll_totalloss100perremark == "Pass" and hvt_result == "Pass" and iovt_result == "Pass": 
                output = "Pass"
            else:
                output = "Fail"
        elif bulkmain_tfcondition == "New":
            if vr_result == "Pass" and nll_result == "Pass" and ll_percimpedancevoltremark == "Pass" and ll_totalloss50perremark == "Pass" and ll_totalloss100perremark == "Pass" and hvt_result == "Pass" and iovt_result == "Pass":
                output = "Pass"
            else:
                output = "Fail"
    return render(request, 'officer/tmqm_report_success_view.html', {'nabl_report_lst': nabl_obj, 'output': output})


def Report_success_view_rca(request, sc):
    nabl_obj = nabl_report_data_rca.objects.filter(torder_samplecode=sc)
    for i in nabl_obj:
        wr_result = i.wr_result
        vr_result = i.vr_result
        ir_result = i.ir_result
        output = ""
        if wr_result == "Pass" and vr_result == "Pass" and ir_result == "Pass":
            output = "Pass"
        else:
            output = "Fail"
    return render(request, 'officer/tmqm_report_success_view_rca.html', {'nabl_report_lst': nabl_obj, 'output': output})


# #total nabl
# def nabl_dgm_qc_total(request):
#     data = User_Registration.objects.filter(Complete_Details=1,
#                                             User_type='NABL') | User_Registration.objects.filter(qc_approval=2,
#                                                                                                  Complete_Details=1,
#                                                                                                  User_type='NABL')
#     return render(request, "officer/nabl_dgm_qc_total.html", {'data': data})

# def vendor_dgm_work_total(request):
#     data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR')
#     approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
#                                                                    User_type='VENDOR').count()
#     pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1,User_type='VENDOR').count()
#     total = approve + pending

#     return render(request, 'officer/vendor_dgm_work_total.html', {'data': data,'total':total})


# def tkc_dgm_work_total(request):
#     data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')
#     return render(request, 'officer/tkc_dgm_work_total.html', {'data': data})

def vendor_dgm_finance_total(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(Complete_Details=1,
                                                User_type='VENDOR') | User_Registration.objects.filter(finance_approval=2,
                                                                                                    Complete_Details=1,
                                                                                                    User_type='VENDOR')
        return render(request, 'officer/dgm_finance_total.html', {'data': data})
    return redirect('/')



#####lok####

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from paywix.payu import Payu

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)
import payu_sdk
import uuid


def payu_demo_registration(request):
    txnid = uuid.uuid1()
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type=request.session['User_type'])
    client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
    param = {"txnid": txnid, "amount": "2360.00", "productinfo": "Registration", "firstname": data.Authorised_person_E,
             "email": data.Email_Id}
    apiHash = payu_sdk.Hasher.generate_hash(param)
    data3 = Payudata_main(User_Id = data,Payu_Status='pending', Txdid=txnid,
                          Productinfo="Registration",
                          Firstname=data.Authorised_person_E, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                          Netamount_Debited='2360.00',user_zone = data.User_zone
                          )
    data3.save()
    return render(request, 'main/payu_checkout_registration.html',
                  {"posted": apiHash, "txnid": txnid, "amount": "2360.00", 'firstname': data.Authorised_person_E,
                   "email": data.Email_Id, "productinfo": "Registration", "phone": data.ContactNo,"user_zone_c":data.User_zone})


from fpdf import FPDF
import os
from payu_sdk.API import paymentAPI
import json
import hashlib
import io
from rest_framework.parsers import JSONParser


@csrf_exempt
def payu_success_registration(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    Hash = data['hash']
    Status = data['status']
    Txn_id = data['txnid']
    Product_info = data['productinfo']
    First_name = data['firstname']
    Last_name = data['lastname']
    Phone_no = data['phone']
    mail = data['email']
    Pgateway_Type = data['PG_TYPE']
    Bankrefnum = data['bank_ref_num']
    Bank_code = data['bankcode']
    if Pgateway_Type == 'NB-PG':
        Nameon_card ='Net banking'
        Card_num = '000000'
    #else:
        #Nameon_card = data['name_on_card']
        #Card_num = data['cardnum']
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    Error = data['field9']
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    date = datetime.datetime.now()
    if Payudata_main.objects.filter(Txdid=Txn_id).exists():
        Payudata = Payudata_main.objects.get(Txdid=Txn_id)
        if Payudata.Productinfo == 'Activation Fee Befour Expired':
            user = User_Registration.objects.filter(ContactNo=Phone_no,User_type='TKC')
            user.update(activation_before_expired = 1,activation=1)
        if Payudata.Productinfo == 'Activation Fee After Expired':
            user = User_Registration.objects.filter(ContactNo=Phone_no,User_type='TKC')
            user.update(activation_after_expired = 1,activation=1)
        
        if Payudata.Productinfo == 'Upgradation Fee':
            user = User_Registration.objects.filter(ContactNo=Phone_no,User_type='TKC')
            user.update(upgrade_payment = 1,upgrade=1)

        if Payudata.Productinfo == 'Registration':
            user = User_Registration.objects.filter(ContactNo=Phone_no).last()
            user.payment = 1
            user.save()
        
        if Payudata.Productinfo == 'Payment For Factory Inspection':
            user = User_Registration.objects.filter(ContactNo=Phone_no,User_type='VENDOR')
            user.update(factory_approval_payment = 1)    
        Payudata.Payu_Moneyid = payu_moneyid
        Payudata.Hash_Id = Hash
        Payudata.Paymentgateway_Type = Pgateway_Type
        Payudata.date = date
        Payudata.Bank_Ref_Num = Bankrefnum
        Payudata.Bankcode = Bank_code
        Payudata.Error = Error
        #Payudata.Name_On_Card = Nameon_card
        #Payudata.Cardnum = Card_num
        Payudata.Payu_Status = Status
        Payudata.save()
    user = User_Registration.objects.filter(ContactNo=Phone_no).last()
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    date = datetime.datetime.now()
    user = User_Registration.objects.filter(ContactNo=Phone_no).last()
    client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
    key = 'GHeH7D'
    salt = 'DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ'
    command = 'verify_payment'
    toHash = {"command": command, "var1": Txn_id}
    apiHash = payu_sdk.Hasher.APIHash(toHash)
    Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
    #url = 'https://test.payu.in/merchant/postservice.php?form=2'
    #r = requests.post(url, data=Poststring)
    url = "https://info.payu.in/merchant/postservice?form=2"
    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    #r = requests.post(url, data=Poststring)
    payload = "key=" + key + "&command=verify_payment&var1=" + Txn_id + "&hash=" + apiHash
    #res = paymentAPI.verifyPayment.verifyPaymentStatusByPayUID(payload)
    res = requests.request("POST", url, data=payload, headers=headers)
    if res.status_code == 200:
        json_data = json.loads(res.text)
        if json_data['status'] == 1:
            transcation_details = json_data['transaction_details']
            transction_data = transcation_details[Txn_id]
            if transction_data['status'] == 'success':
                payu_obj = Payudata_main.objects.get(Txdid=Txn_id)
                if transction_data['productinfo'] == "Activation Fee After Expired":
                    user = User_Registration.objects.get(ContactNo=Phone_no,User_type='TKC')
                    user.activation_after_expired = 1;
                    user.activation = 1;
        
                    user.save()
                    return render(request, 'main/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_reg_seven'})
                elif transction_data['productinfo'] == "Activation Fee Befour Expired":
                    user = User_Registration.objects.get(ContactNo=Phone_no,User_type='TKC')
                    user.activation_before_expired = 1;
                    user.activation = 1;
                    user.save()
                    return render(request, 'main/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
                elif transction_data['productinfo'] == "Registration":
                    Payudata = Payudata_main.objects.get(Txdid=Txn_id)
                    payu_obj.Payu_Status = Status
                    payu_obj.save()
                    user = User_Registration.objects.filter(ContactNo=Phone_no).last()
                    user.payment = 1;
                    user.save()
                    return render(request, 'main/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
                elif transction_data['productinfo'] == "sd deposit":
                    Payudata = Payudata_main.objects.get(Txdid=Txn_id)
                    payu_obj.Payu_Status = 'success'
                    payu_obj.save()
                    user = User_Registration.objects.get(ContactNo=Phone_no,User_type='TKC')
                    user.Complete_Details = 1;
                    user.save()
                    return render(request, 'main/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
                elif transction_data['productinfo'] == "Upgradation Fee":
                    user = User_Registration.objects.get(ContactNo=Phone_no,User_type='TKC')
                    user.upgrade_payment = 1;
                    user.upgrade = 1;
                    user.save()
                    return render(request, 'main/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_upgrade_one'})
                elif transction_data['productinfo'] == "Contractor Upgrade sd":
                    user = User_Registration.objects.get(ContactNo=Phone_no,User_type='TKC')
                    user.work_approval = 0;
                    user.finance_approval = 0;
                    user.qc_approval = 0;
                    user.upgrade_payment = 0;
                    user.upgrade = 0;
                    user.save()
                    return render(request, 'main/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_upgrade_one'})
                elif transction_data['productinfo'] == "Payment For Factory Inspection":
                    Payudata = Payudata_main.objects.get(Txdid=Txn_id)
                    payu_obj.Payu_Status = Status
                    payu_obj.save()
                    user = User_Registration.objects.get(ContactNo=Phone_no,User_type='VENDOR')
                    user.factory_approval_payment = 1;
                    user.save()
                    return render(request, 'main/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/login'})                  
                request.session['Phone_no'] = Phone_no
                
                payment_sms = payu_obj.Netamount_Debited
                payment_for_sms = payu_obj.Productinfo
                zone = user.User_zone
                name_sms = user.CompanyName_E
                sms_date = datetime.datetime.now()
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}   
                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007322352087295618&mobile_number=" + str(
                    mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(payment_sms) + "&v4=" + str(
                    zone) + "&v5=" + str(payment_for_sms) + "&v6=" + str() + "&v7=" + str(sms_date) + "&v8=" + str(Bankrefnum) + "&v9=" + str() 
                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                return render(request, 'main/sucess_pay_registration.html', {'response': response, 'data': payu_obj})
    else:
        attempt_num += 1
        time.sleep(5) 
    request.session['Phone_no'] = Phone_no
    return render(request, 'main/sucess_pay_registration.html', {'response': response, 'data': payu_obj})
    User_Id = user.User_Id
    payu_obj = Payudata_main.objects.get(Txdid=Txn_id)
    user = User_Registration.objects.filter(ContactNo=Phone_no).last()
    user.payment = 1;
    user.save()
    return render(request, 'main/sucess_pay_registration.html',
                  {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
    payu_obj = Payudata_main.objects.latest('User_Id')
    request.session['Phone_no'] = Phone_no
    sms = User_Registration.objects.filter(ContactNo=Phone_no).last()
    mobile = sms.ContactNo
    name_sms = sms.CompanyName_E
    sms_date = datetime.datetime.now()
    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8000"}
    # for server set proxy
    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    
    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(
        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('2360') + "&v4=" + str(
        'Registration') + "&v5=" + str(sms_date) + "&v6=" + str() + "&v7=" + str(sms_date) + "&v8=" + str(Bankrefnum)
    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
    
    sms_template = message_template_log(template_id = '1007156373345234835',date = datetime.datetime.now(),mobile_number = mobile)
    sms_template.save()
    
    txnid = uuid.uuid1()



@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    Hash = data['hash']
    Status = data['status']
    Txn_id = data['txnid']
    Product_info = data['productinfo']
    First_name = data['firstname']
    Last_name = data['lastname']
    Phone_no = data['phone']
    mail = data['email']
    Pgateway_Type = data['PG_TYPE']
    Bankrefnum = data['bank_ref_num']
    Bank_code = data['bankcode']
    if Pgateway_Type == 'NB-PG':
        Nameon_card ='Net banking'
        Card_num = '000000'
    #else:
        #Nameon_card = data['name_on_card']
        #Card_num = data['cardnum']
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    Error = data['field9']
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    date = datetime.datetime.now()
    if Payudata_main.objects.filter(Txdid=Txn_id).exists():
        Payudata = Payudata_main.objects.get(Txdid=Txn_id)
        Payudata.Payu_Moneyid = payu_moneyid
        Payudata.Hash_Id = Hash
        Payudata.Paymentgateway_Type = Pgateway_Type
        Payudata.date = date
        Payudata.Bank_Ref_Num = Bankrefnum
        Payudata.Bankcode = Bank_code
        Payudata.Error = Error
        #Payudata.Name_On_Card = Nameon_card
        #Payudata.Cardnum = Card_num
        Payudata.Payu_Status = Status
        Payudata.save()
    payu_obj = Payudata_main.objects.get(Txdid=Txn_id)
    user = User_Registration.objects.get(ContactNo=Phone_no)
    user.save()
    return render(request, 'main/payment_fail.html', {'response': response, 'data': payu_obj})


def gen_invoice_registration(request):
    user = User_Registration.objects.filter(ContactNo=request.session['Phone_no'])
    user.update(payment=1)
    payu_obj = Payudata_main.objects.latest('User')
    if user[0].User_type == "VENDOR":
        datav = 1
    else:
        datav = 0

    if user[0].User_type == "NABL":
        datan = 1
    else:
        datan = 0
    if user[0].User_type == "TKC":
        datat = 1
    else:
        datat = 0

    user11 = User_Registration.objects.get(ContactNo=request.session['Phone_no'])
    otp = user11.Otp
    request.session['otp'] = otp
    return render(request, 'main/invoice_registration.html',
                  {'data': payu_obj, "user1": datav, "user2": datan, "user3": datat})


# --pending--------------

# def factory_initiate(request):
#     data = User_Registration.objects.filter(factory_approval=0, factory_approval_payment=1, User_type='VENDOR')
#     return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data})

# assigned------------------------

def factory_assigned(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(factory_approval=1, factory_approval_payment=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/vendor_factory_inspection_assined.html', {'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(factory_approval=1, factory_approval_payment=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/vendor_factory_inspection_assined.html', {'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(factory_approval=1, factory_approval_payment=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/vendor_factory_inspection_assined.html', {'data': data})

    return redirect('/')

# def nabl_dgm_qc_approve(request):
#     data = User_Registration.objects.filter(qc_approval=1, Complete_Details=1,
#                                             User_type='NABL') | User_Registration.objects.filter(qc_approval=2,
#                                                                                                  Complete_Details=1,
#                                                                                                  User_type='NABL')
#     return render(request, "officer/nabl_dgm_qc_total.html", {'data': data})


# #----DGMW001 WORK--- --CHANGE BECOUSE OF DASHBOARD SHOW TOTAL VENDOR---------------------------------------------------------------------------------------------

def vendor_dgm_work_total(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/vendor_dgm_work_total.html',{'data': data})


        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/vendor_dgm_work_total.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/vendor_dgm_work_total.html',{'data': data})


    return redirect('/')


# -------------7-04-22

# def tkc_dgm_work_total(request):
#     data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')
#     approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
#                                                User_type='VENDOR').count()
#     pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
#     total = approve + pending
#
#     approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
#                                                    User_type='TKC').count()
#     pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
#                                                    User_type='TKC').count()
#     total_tkc = approve_tkc + pending_tkc
#     return render(request, 'officer/tkc_dgm_work_total.html',
#                   {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
#                    'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
#
#     # return render(request, 'officer/tkc_dgm_work_total.html', {'data': data})
# -----Poornima 8-4-2022
def tkc_dgm_work_total(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',User_zone='WZ')
            return render(request, 'officer/tkc_dgm_work_total.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',User_zone='CZ')
            return render(request, 'officer/tkc_dgm_work_total.html',{'data': data})


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',User_zone='EZ')
            return render(request, 'officer/tkc_dgm_work_total.html',{'data': data})
    return redirect('/')


def vendor_dgm_work_complete(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(work_approval=1, Complete_Details=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/vendor_dgm_work_complete.html',{'data': data})
        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(work_approval=1, Complete_Details=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/vendor_dgm_work_complete.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(work_approval=1, Complete_Details=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/vendor_dgm_work_complete.html',{'data': data})


    return redirect('/')


def vendor_dgm_work_pending(request):
    if request.session.has_key('officer'):

        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR',User_zone='WZ').order_by('Uploaded_Date')       
            return render(request, 'officer/vendor_dgm_work_pending.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR',User_zone='CZ').order_by('Uploaded_Date')    
            return render(request, 'officer/vendor_dgm_work_pending.html',{'data': data})


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR',User_zone='EZ').order_by('Uploaded_Date')     
            return render(request, 'officer/vendor_dgm_work_pending.html',{'data': data})


    return redirect('/')

def vendor_dgm_work_pending_resubmit(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/vendor_dgm_work_pending_resubmit.html',{'data': data})


        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/vendor_dgm_work_pending_resubmit.html',{'data': data})


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/vendor_dgm_work_pending_resubmit.html',{'data': data})
                    
    return redirect('/')
                   


def vendor_dgm_work_pending_resubmitt(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

        approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc

        approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
        total = approve + pending
        return render(request, 'officer/tkc_dgm_work_total.html',
                    {'data': data, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc,
                    'data': data, 'total': total, 'pending': pending, 'approve': approve, })
    return redirect('/')

def tkc_dgm_work_complete(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',work_approval=1,User_zone='WZ') | User_Registration.objects.filter(Complete_Details=1, User_type='TKC',work_approval=0,upgrade_payment=1,User_zone='WZ')         
            return render(request, 'officer/tkc_dgm_work_complete.html',{'data': data })

        if request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',work_approval=1,User_zone='CZ') | User_Registration.objects.filter(Complete_Details=1, User_type='TKC',work_approval=0,upgrade_payment=1,User_zone='CZ')         
            return render(request, 'officer/tkc_dgm_work_complete.html',{'data': data })

        if request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',work_approval=1,User_zone='EZ') | User_Registration.objects.filter(Complete_Details=1, User_type='TKC',work_approval=0,upgrade_payment=1,User_zone='EZ')         
            return render(request, 'officer/tkc_dgm_work_complete.html',{'data': data })

    # return render(request, 'officer/tkc_dgm_work_complete.html', {'data': data})
    return redirect('/')


    # return render(request, 'officer/tkc_dgm_work_complete.html', {'data': data})

def tkc_dgm_work_pending_resubmit(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='TKC',User_zone='WZ')
            return render(request, 'officer/tkc_dgm_work_pending_resubmit.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='TKC',User_zone='CZ')
            return render(request, 'officer/tkc_dgm_work_pending_resubmit.html',{'data': data})
        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='TKC',User_zone='EZ')
            return render(request, 'officer/tkc_dgm_work_pending_resubmit.html',{'data': data})

    return redirect('/')
#     # return render(request, 'officer/tkc_dgm_work_pending_resubmit.html', {'data': data})


# # #----------DGMF001---FINANCE-------------CHANGE BECOUSE OF DASHBOARD SHOW TOTAL VENDOR-----------------------------------------------------------------------


def vendor_dgm_finance_all(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/dgm_finance_total.html',{'data': data})
        
        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/dgm_finance_total.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/dgm_finance_total.html',{'data': data})

    return redirect('/')


def vendor_dgm_finance_complate(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1,User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/dgm_finance_complete.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1,User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/dgm_finance_complete.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1,User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/dgm_finance_complete.html',{'data': data})

    return redirect('/')

def vendor_dgm_finance_pending(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/dgm_finance_pending.html',{'data': data, })

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/dgm_finance_pending.html',{'data': data, })

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/dgm_finance_pending.html',{'data': data, })

    return redirect('/')


def vendor_dgm_finance_pending_rejection_vendor(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/vendor_dgm_finance_pending_rejection_vendor.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/vendor_dgm_finance_pending_rejection_vendor.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/vendor_dgm_finance_pending_rejection_vendor.html',{'data': data})


    return redirect('/')


def dgm_work_pending(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='TKC',User_zone='WZ',officer_create=0).order_by('reg_date')
            return render(request, 'officer/dgm_work_pending.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='TKC',User_zone='CZ',officer_create=0).order_by('reg_date')
            return render(request, 'officer/dgm_work_pending.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='TKC',User_zone='EZ',officer_create=0).order_by('reg_date')
            return render(request, 'officer/dgm_work_pending.html',{'data': data})
    return redirect('/')


#     # return render(request, 'officer/dgm_work_pending.html', {'data': data})

def dgm_finance_all_tkc(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',User_zone='WZ')
            return render(request, 'officer/dgm_finance_all.html',{'data': data})
        
        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',User_zone='CZ')
            return render(request, 'officer/dgm_finance_all.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC',User_zone='EZ')
            return render(request, 'officer/dgm_finance_all.html',{'data': data})

    return redirect('/')

#     # return render(request, 'officer/dgm_finance_all.html', {'data': data})


def dgm_finance_complete_tkc(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1, User_type='TKC',User_zone='WZ') | User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC',upgrade_payment=1,User_zone='WZ')
            return render(request, 'officer/dgm_finance_complete_tkc.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1, User_type='TKC',User_zone='CZ') | User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC',upgrade_payment=1,User_zone='CZ')
            return render(request, 'officer/dgm_finance_complete_tkc.html',{'data': data})


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1, User_type='TKC',User_zone='EZ') | User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC',upgrade_payment=1,User_zone='EZ')
            return render(request, 'officer/dgm_finance_complete_tkc.html',{'data': data})

    return redirect('/')

def vendor_dgm_finance_pending_rejection_tkc(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='TKC',User_zone='WZ')
            return render(request, 'officer/vendor_dgm_finance_pending_rejection_tkc.html',{'data': data,})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='TKC',User_zone='CZ')
            return render(request, 'officer/vendor_dgm_finance_pending_rejection_tkc.html',{'data': data,})


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='TKC',User_zone='EZ')
            return render(request, 'officer/vendor_dgm_finance_pending_rejection_tkc.html',{'data': data,})


    return redirect('/')


def dgm_finance_pending(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC',User_zone='WZ',officer_create=0).order_by('reg_date')
            return render(request, 'officer/dgm_finance_pending.html',{'data': data, })

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC',User_zone='CZ',officer_create=0).order_by('reg_date')
            return render(request, 'officer/dgm_finance_pending.html',{'data': data, })


        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC',User_zone='EZ',officer_create=0).order_by('reg_date')
            return render(request, 'officer/dgm_finance_pending.html',{'data': data, })


    return redirect('/')
# # #CGMQC-------------------REMANING------------------------------------------------------------------


def cgm_total_vendor(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(work_approval=1, finance_approval=1, factory_approval_payment=1,User_type='VENDOR',User_zone='WZ') 
            return render(request, 'officer/total_cgm_vendor.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(work_approval=1, finance_approval=1, factory_approval_payment=1,User_type='VENDOR',User_zone='CZ') 
            return render(request, 'officer/total_cgm_vendor.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(work_approval=1, finance_approval=1, factory_approval_payment=1,User_type='VENDOR',User_zone='EZ') 
            return render(request, 'officer/total_cgm_vendor.html',{'data': data})
    return redirect('/')

#     # return render(request, 'officer/total_cgm_vendor.html', {'data': data})


def cgm_pending_vendor(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='WZ')
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='CZ')
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='EZ')
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})
    return redirect('/')

    # return render(request, 'officer/cgm_pending_vendor.html', {'data': data})
    
    
def cgm_pending_vendor_data(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1,factory_approval=1, User_type='VENDOR',User_zone='WZ').order_by('User_Id')
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1,factory_approval=1, User_type='VENDOR',User_zone='CZ').order_by('User_Id')
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1,factory_approval=1, User_type='VENDOR',User_zone='EZ').order_by('User_Id')
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})
        


def cgm_complete_vendor(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1,factory_approval_payment=1,User_zone='WZ')
            return render(request, 'officer/cgm_complete_vendor.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1,factory_approval_payment=1,User_zone='CZ')
            return  render(request, 'officer/cgm_complete_vendor.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1,factory_approval_payment=1,User_zone='EZ')
            return render(request, 'officer/cgm_complete_vendor.html',{'data': data})

    return redirect('/')


def cgm_total_nabl(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(qc_approval=1, User_type='NABL')

        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(Complete_Details=1, work_approval=1, cgm_approval=0, finance_approval=1,
                                                User_type='VENDOR', factory_approval=1).count()
        total = approve + pending

        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()

        total_nabl = approve_nabl + pending_nabl
        return render(request, 'officer/cgm_total_nabl.html',
                    {'data': data, 'approve': approve, 'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                    'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })
    return redirect('/')
    # return render(request, 'officer/cgm_total_nabl.html', {'data': data})


def cgm_pending_nabl(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, User_type='NABL').order_by('User_Id')

        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').order_by('User_Id').count()
        pending = User_Registration.objects.filter(Complete_Details=1, work_approval=1, cgm_approval=0, finance_approval=1,
                                                User_type='VENDOR', factory_approval=1).order_by('User_Id').count()
        total = approve + pending

        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').order_by('User_Id').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').order_by('User_Id').count()

        total_nabl = approve_nabl + pending_nabl
        return render(request, 'officer/cgm_pending_nabl.html',
                    {'data': data, 'approve': approve, 'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                    'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })
    return redirect('/')

    # return render(request, 'officer/cgm_pending_nabl.html', {'data': data})


def nabl_cgm_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        if data[0].User_type == "NABL":
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            # Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
            # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)
            mat= NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            #BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)

            approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                    User_type='VENDOR').count()
            pending = User_Registration.objects.filter(Complete_Details=1, work_approval=1, cgm_approval=0,
                                                    finance_approval=1,
                                                    User_type='VENDOR', factory_approval=1).count()
            total = approve + pending

            approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                            User_type='NABL').count()
            pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                            User_type='NABL').count()

            total_nabl = approve_nabl + pending_nabl
            return render(request, 'officer/nabl_cgm_evaluate.html',
                        {'data': data[0], 'doc': doc, 'approve': approve, 'pending': pending, 'total': total,
                        'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl, 'total_nabl': total_nabl,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,"mat1" : mat })
    return redirect('/')



def cgm_approved_nabl(request):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(qc_approval=1, cgm_approval=1, User_type='NABL')

        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(Complete_Details=1, work_approval=1, cgm_approval=0, finance_approval=1,
                                                User_type='VENDOR', factory_approval=1).count()
        total = approve + pending

        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()

        total_nabl = approve_nabl + pending_nabl
        return render(request, 'officer/cgm_approve_nabl.html',
                    {'data': data, 'approve': approve, 'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                    'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })

    return redirect('/')
    # return render(request, 'officer/cgm_pending_nabl.html', {'data': data})


# def vendor_cgm_evaluate(request, id):
#     data = User_Registration.objects.filter(User_Id=id)


#     if data[0].User_type == "VENDOR":
#         doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)

#         doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)

#         fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
#         Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
#         tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)

#         return render(request, 'officer/vendor_cgm_evaluate_pending.html',{'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material, 'tech_data': tech_data})

#     doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
#     Factory = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
#     Material = Add_material.objects.filter(user_id=data[0].User_Id)
#     return render(request, 'officer/vendor_wnp_evaluate.html',{'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material})


# def nabl_cgm_evaluate_test(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "NABL":
#         doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
#         # Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
#         # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)
#         return render(request, 'officer/nabl_cgm_evaluate_pending.html',
#                       {'data': data[0], 'doc': doc})


# def vendor_cgm_evaluate2(request, id):
#     data = User_Registration.objects.filter(User_Id=id)

#     if data[0].User_type == "VENDOR":
#         doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)

#         doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)

#         fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
#         Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
#         tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)

#         return render(request, 'officer/vendor_cgm_evaluate_pending2.html',
#                       {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
#                        'tech_data': tech_data})

#     doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
#     Factory = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
#     Material = Add_material.objects.filter(user_id=data[0].User_Id)
#     return render(request, 'officer/vendor_wnp_evaluate.html',
#                   {'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material})


def gp_outward_base(request):
    trf_obj = TRF_Details.objects.all()
    return render(request, 'officer/gp_outward_base.html', {'trf_obj': trf_obj})


def gp_outward(request, trf_id):
    if request.method == 'POST':
        outpass_date = request.POST.get('outpass_date')
        outpass_driver_name = request.POST.get('outpass_driver_name')
        outpass_Vehicle_number = request.POST.get('outpass_Vehicle_number')
        outpass_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
        outpass_obj.update(outpass_date=outpass_date, outpass_driver_name=outpass_driver_name,
                           outpass_Vehicle_number=outpass_Vehicle_number, outpass_generate_complete=1)
        trf_outpass_obj = TRF_Details.objects.filter(TRF_Id=trf_id)
        trf_outpass_obj.update(outpass_gen=1)
        trf_obj = TRF_Details.objects.all()
        return render(request, 'officer/gp_outward_base.html', {'trf_obj': trf_obj})

    trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_outward.html', {'employees': trf_obj, 'trf_id': trf_id})


def gp_outward_view(request, trf_id):
    trf_obj = Add_material_nabl.objects.filter(TRF_Id=trf_id)
    return render(request, 'officer/gp_outward_view.html', {'employees': trf_obj, 'trf_id': trf_id})


# total nabl-------DGM001------------------------------------------

def nabl_dgm_qc_total(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1,User_type='NABL',User_zone='WZ') 
            return render(request, 'officer/nabl_dgm_qc_total.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1,User_type='NABL',User_zone='CZ') 
            return render(request, 'officer/nabl_dgm_qc_total.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1,User_type='NABL',User_zone='EZ') 
            return render(request, 'officer/nabl_dgm_qc_total.html',{'data': data})
                    
    return redirect('/')

def nabl_dgm_qc_approve(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(qc_approval=1, Complete_Details=1, User_type='NABL',User_zone='WZ')
            return render(request, 'officer/nabl_dgm_qc_total.html',{'data': data})
        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(qc_approval=1, Complete_Details=1, User_type='NABL',User_zone='CZ')
            return render(request, 'officer/nabl_dgm_qc_total.html',{'data': data})
        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(qc_approval=1, Complete_Details=1, User_type='NABL',User_zone='EZ')
            return render(request, 'officer/nabl_dgm_qc_total.html',{'data': data})
    return redirect('/')

def nabl_dgm_qc_pending(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(qc_approval=0, Complete_Details=1, User_type='NABL',User_zone='WZ',cgm_approval = 0) 
            return render(request, 'officer/nabl_dgm_qc_pending.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(qc_approval=0, Complete_Details=1, User_type='NABL',User_zone='CZ',cgm_approval = 0) 
            return render(request, 'officer/nabl_dgm_qc_pending.html',{'data': data})
        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(qc_approval=0, Complete_Details=1, User_type='NABL',User_zone='EZ',cgm_approval = 0) 
            return render(request, 'officer/nabl_dgm_qc_pending.html',{'data': data})
    return redirect('/')


def nabl_dgm_nabl_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        if data[0].User_type == "NABL":
            # doc = NABL_Document.objects.filter(user_id=id)
            # doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            approve_nabl = User_Registration.objects.filter(Complete_Details=1, qc_approval=1,
                                                            User_type='NABL').count()

            pending_nabl = User_Registration.objects.filter(qc_approval=0, cgm_approval=0, Complete_Details=1,
                                                            User_type='NABL').count()

            total_nabl = approve_nabl + pending_nabl

            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            return render(request, 'officer/nabl_dgm_qc_pending_evaluate.html',
                        {'data': data[0], 'doc': doc, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                        'total_nabl': total_nabl, })
    return redirect('/')


# def nabl_dgm_qc_evaluate_pending(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "NABL":
#         # doc = NABL_Document.objects.filter(user_id=id)
#         # doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
#         doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
#         return render(request, 'officer/nabl_dgm_qc_evaluate_pending.html',
#                       {'data': data[0], 'doc': doc})


def dgm_work_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                User_type='VENDOR').count()

        pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
        total = approve + pending

        approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc

        if data[0].User_type == "VENDOR":
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id = data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id = data_new)
            Vendor_Material_Details1 = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
            Vendor_Technical_Details1 = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)
            return render(request, 'officer/vendor_dgm_work_evaluate.html',
                        {'data': data[0],'doc':doc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'Vendor_Material_Details':Vendor_Material_Details1,'Vendor_Technical_Details':Vendor_Technical_Details1})

        if data[0].User_type == "TKC":
            if BankDetails.objects.filter(user_id=data[0].ContactNo).exists():

                CompanyData1 = UserCompanyDataMain.objects.get(user_id_id = data_new)
                AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id = data_new)
                bank  = BankDetails.objects.filter(user_id=data[0].ContactNo)
                if (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 0) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  0):
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=0)
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt,'bank':bank[0]})


                elif (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 1) or  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  1):
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)
                    print("zzzzzzzzzzzzzzzzzzzzz")
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt,'bank':bank[0]})

                elif data[0].upgrade_payment == 1 and  data[0].activation_before_expired == 0  and   data[0].activation_after_expired ==  0:
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)
                    up_oyt = TKC_Payment.objects.get(id = data[0].Upgrade_Oyt)
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt,'bank':bank[0],'up_oyt':up_oyt})

                else:
                
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt,'bank':bank[0]})

            else:
                CompanyData1 = UserCompanyDataMain.objects.get(user_id_id = data_new)
                AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id = data_new)
                if (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 0) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  0):
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=0)
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt})


                elif (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 1) or  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  1):
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)
                    print("zzzzzzzzzzzzzzzzzzzzz")
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt})

                elif data[0].upgrade_payment == 1 and  data[0].activation_before_expired == 0  and   data[0].activation_after_expired ==  0:
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    up_oyt = TKC_Payment.objects.get(id = data[0].Upgrade_Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt,'up_oyt':up_oyt})

                else:
                
                    oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                    doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)
                    return render(request, 'officer/dgm_work_evaluate.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData':CompanyData1,'AuthorisedPerson':AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'oyt':oyt})


        return render(request, 'officer/dgm_work_evaluate.html',
                    {'data': data[0], 'total': total, 'pending': pending, 'approve': approve,
                    'approve_tkc': approve_tkc,
                    'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
    return redirect('/')

def dgm_finance_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                User_type='VENDOR').count()

        pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
        total = approve + pending

        approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc
        if data[0].User_type == "VENDOR":
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            Vendor_Material_Details1 = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
            Vendor_Technical_Details1 = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)

            doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            no_preview_path = os.getcwd() + "/media/documents/No_Preview.pdf"

            # doc2 = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            # doc = Vendor_Turnover.objects.filter(user_id=data[0].User_Id)
            doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            no_preview_path = os.getcwd() + "/media/documents/No_Preview.pdf"
            try:
                for i in doc1:
                    if i.Ddocfile.url == "":
                        abc = i.update(Balance_Sheet=no_preview_path)
                        abc.save()
            except Exception as e:
                pass
            return render(request, 'officer/vendor_dgm_finance_evaluate.html',
                      {'doc1': doc1,'doc':doc,'CompanyData':CompanyData1,
                      'AuthorisedPerson':AuthorisedPerson1,
                       'Vendor_Material_Details':Vendor_Material_Details1,
                       'Vendor_Technical_Details':Vendor_Technical_Details1,
                      'data': data[0], 'total': total, 'pending': pending, 'approve': approve,
                       'approve_tkc': approve_tkc,'pending_tkc': pending_tkc, 
                       'total_tkc': total_tkc})

        if data[0].User_type == "TKC":
            if BankDetails.objects.filter(user_id=data[0].ContactNo).exists():
            
                doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
                CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
                oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                bank  = BankDetails.objects.filter(user_id=data[0].ContactNo)
                
                if (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 0) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  0):
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=0)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'bank':bank[0]})

                elif  (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 1) or  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  1):         
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=1)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'bank':bank[0]})

                elif  data[0].upgrade_payment == 1 and  data[0].activation_before_expired == 0 and data[0].activation_after_expired ==  0:
                    up_oyt = TKC_Payment.objects.get(id = data[0].Upgrade_Oyt)       
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=1)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'up_oyt':up_oyt,'bank':bank[0]})

                else:
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=1)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'bank':bank[0]})

            else:
                doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
                CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
                AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
                oyt = TKC_Payment.objects.get(id = data[0].Oyt)
                print("gggggggggggggggggggggggggggg")  
                
                if (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 0) and  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  0):
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=0)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc})

                elif  (data[0].upgrade_payment == 0 and  data[0].activation_before_expired == 1) or  (data[0].upgrade_payment == 0 and  data[0].activation_after_expired ==  1):         
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=1)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,})

                elif  data[0].upgrade_payment == 1 and  data[0].activation_before_expired == 0 and data[0].activation_after_expired ==  0:
                    print("gggggggggggggggggggggggggggg")  
                    up_oyt = TKC_Payment.objects.get(id = data[0].Upgrade_Oyt)       
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=1)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc,'up_oyt':up_oyt})

                else:
                    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
                    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=1)
                    return render(request, 'officer/dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,"oyt":oyt,
                        'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc})

    return redirect('/')


def dgm_finance_view(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
        AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
        oyt = TKC_Payment.objects.get(id = data[0].Oyt)
        doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
        doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2,new_data=0)
        approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                User_type='VENDOR').count()

        pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
        total = approve + pending

        approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc

        return render(request, 'officer/dgm_finance_view.html',
                    {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending, 'approve': approve,
                    'approve_tkc': approve_tkc,'AuthorisedPerson': AuthorisedPerson1,'CompanyData':CompanyData1,
                    'pending_tkc': pending_tkc, 'total_tkc': total_tkc,"oyt":oyt})
    return redirect('/')


# ---------------------12 april------------------------------------------------------------------------------------------------------

def dgm_work_evaluate2(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)

        approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                User_type='VENDOR').count()

        pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
        total = approve + pending

        approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc

        if data[0].User_type == "VENDOR":
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)

            no_preview_path = os.getcwd() + "/media/documents/vendor/work_data/No_Preview.pdf"

            try:
                for i in doc:
                    if i.Ddocfile.url == "":
                        abc = i.update(Ddocfile=no_preview_path)
                        abc.save()
            except Exception as e:
                pass

            return render(request, 'officer/dgm_work_evaluate2.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
    return redirect('/')


def resubmit_finance_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        
        approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
        total = approve + pending

        # data = User_Registration.objects.filter(Complete_Destails=1, User_type='TKC')

        approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc

        if data[0].User_type == "VENDOR":
            # doc2 = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            # doc = Vendor_Turnover.objects.filter(user_id=data[0].User_Id)
            doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            #BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)
            no_preview_path = os.getcwd() + "/media/documents/No_Preview.pdf"

            try:
                for i in doc1:
                    if i.Ddocfile.url == "":
                        abc = i.update(Balance_Sheet=no_preview_path)
                        abc.save()
            except Exception as e:
                pass

            return render(request, 'officer/resubmit_dgm_finance_evaluate.html',
                        {'data': data[0], 'doc1': doc1, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_tkc': approve_tkc,'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
        if data[0].User_type == "TKC":
            doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
            doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
            return render(request, 'officer/tkc_resubmit_dgm_finance_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                        'approve': approve, 'approve_tkc': approve_tkc,
                        'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
    return redirect('/')



def vendor_cgm_evaluate2(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(Complete_Details=1, cgm_approval=0,
                                                User_type='VENDOR', factory_approval=1).count()
        total = approve + pending

        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()
        total_nabl = approve_nabl + pending_nabl

        if data[0].User_type == "VENDOR":
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            #BankDetails1 = BankDetails.objects.filter(user_id=data[0].ContactNo)
            doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
            Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
            tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)
            return render(request, 'officer/vendor_cgm_evaluate_pending2.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
                        'tech_data': tech_data, 'doc': doc, 'Material': Material, 'approve': approve, 'pending': pending,
                        'total': total, 'approve_nabl': approve_nabl,
                        'pending_nabl': pending_nabl, 'total_nabl': total_nabl })

            # return render(request, 'officer/vendor_cgm_evaluate_pending2.html',
            #               {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,'tech_data': tech_data})

        doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
        Factory = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
        Material = Add_material.objects.filter(user_id=data[0].User_Id)
        return render(request, 'officer/vendor_wnp_evaluate.html',
                    {'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material, 'approve': approve,
                    'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                    'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })

    # return render(request, 'officer/vendor_wnp_evaluate.html',{'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material})
    return redirect('/')

    # return render(request, 'officer/vendor_wnp_evaluate.html',{'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material})


def nabl_cgm_evaluate_test(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(Complete_Details=1, cgm_approval=0,
                                                User_type='VENDOR', factory_approval=1).count()
        total = approve + pending

        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()
        total_nabl = approve_nabl + pending_nabl

        CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
        mat= NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)

        if data[0].User_type == "NABL":
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            # Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
            # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)

            return render(request, 'officer/nabl_cgm_evaluate_pending.html',
                        {'data': data[0], 'doc': doc, 'approve': approve, 'pending': pending, 'total': total,
                        'approve_nabl': approve_nabl,'CompanyData': CompanyData1,
                            'AuthorisedPerson': AuthorisedPerson1,"mat1":mat,
                        'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })
    return redirect('/')


def nabl_dgm_qc_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(Complete_Details=1, cgm_approval=0,
                                                User_type='VENDOR', factory_approval=1).count()
        total = approve + pending

        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()
        total_nabl = approve_nabl + pending_nabl
        if data[0].User_type == "NABL":
            # doc = NABL_Document.objects.filter(user_id=id)
            # doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            #BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)
            mat= NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
            return render(request, 'officer/nabl_dgm_qc_evaluate.html',
                        {'data': data[0], 'doc': doc, 'approve': approve, 'pending': pending, 'total': total,
                        'approve_nabl': approve_nabl,'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                         "mat1":mat,
                        'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })

    return redirect('/')

# ----------------------------------------13 april evn---------------------------------------------------

def resubmit_view(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(Complete_Details=1, work_approval=1, cgm_approval=0, finance_approval=1,
                                                User_type='VENDOR').count()
        total = approve + pending

        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()
        approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc
        CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
        AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
        mat= NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)

        if data[0].User_type == "VENDOR":
            
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            BankDetails1 = []
            if  BankDetails.objects.filter(user_id=data[0].ContactNo).exists():
                BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
            
            Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
            tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)
            vendor = User_Registration.objects.get(User_Id=id)
            apprisal = []
            fi_tech = []
            if FI_Appraisal_Details.objects.filter(vendor=vendor).exists():
                apprisal = FI_Appraisal_Details.objects.filter(vendor=vendor).last()
                fi_tech = Factory_Technical_Details.objects.filter(vendor=vendor).last()
            return render(request, 'officer/vendor_resubmit_pending_view.html',
                          {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
                           'tech_data': tech_data, 'total': total, 'approve': approve, 'pending': pending,
                            'CompanyData': CompanyData1,
                           'AuthorisedPerson1': AuthorisedPerson1,
                           'BankDetails': BankDetails1, 'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech})
        if data[0].User_type == "TKC":
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            oyt = TKC_Payment.objects.get(id = data[0].Oyt)
            if data[0].upgrade_payment == 1:
                doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)

                return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                            {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                            'approve_nabl': approve_nabl,'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                            'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                            'total_tkc': total_tkc,'oyt':oyt})

            elif data[0].activation_before_expired == 1 or data[0].activation_after_expired==1:
                doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=1)

                return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                            {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                            'approve_nabl': approve_nabl,'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                            'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                            'total_tkc': total_tkc,'oyt':oyt})

            else:
                doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1,new_data=0)

                return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                            {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                            'approve_nabl': approve_nabl,'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                            'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                            'total_tkc': total_tkc,'oyt':oyt})


        if data[0].User_type == "NABL":
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            return render(request, 'officer/nabl_resubmit_pending_view_work.html',
                        {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                        'approve_nabl': approve_nabl, 'CompanyData': CompanyData1,'mat1':mat,
                        'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                        'total_tkc': total_tkc})

        return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                    {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                    'approve_nabl': approve_nabl,
                    'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                    'total_tkc': total_tkc})
    return redirect('/')

def dgm_work_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = User_Registration.objects.filter(User_Id=id)
            if data[0].User_type == "TKC":
                approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                        User_type='VENDOR').count()
                pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
                total = approve + pending

                approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                            User_type='TKC').count()
                pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                            User_type='TKC').count()
                total_tkc = approve_tkc + pending_tkc

                late = TKC_Document.objects.filter(user_id=data[0].User_Id)
            
                latest = late.latest('new_data')
            
                if latest.new_data == 0:
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,Approval_doc=1,new_data=0)

                elif latest.new_data == 1:
                    doc = TKC_Document.objects.filter(Approval_doc=1, user_id=data[0].User_Id,new_data=1)

                counter = 100
                comment = 0
                nz = 0
                for data in doc:
                    comm = request.POST.get(str(comment))
                    result = request.POST.get(str(counter))
                    if comm != '':
                        data.Primary_remark = comm

                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    data.Primary_verification_Date = datetime.datetime.now()
                    if result == 'OK':
                        data.Primary_verification_Status = 1
                    elif result == 'NOT':
                        nz = 1
                        user = User_Registration.objects.get(User_Id=id)
                        officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        officer_name = officer_table.employ_name
                        offcier_designation = officer_table.designation
                        summary = reject_and_approve_summary(user=user,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=comm,document=data.Ddocfile,document_name=data.Types_of_Docs)
                        summary.save()
                        user.work_approval = 2
                        user.dgm_work_reject_date = datetime.datetime.now()
                        user.save()
                        data.Primary_verification_Status = 2
                        data.Status = 0
                        nameee = data.Types_of_Docs
                        sms = User_Registration.objects.get(User_Id=id)
                        mobile = sms.ContactNo
                        zone = sms.User_zone
                        name_sms = sms.CompanyName_E
                        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                        # for server set proxy
                        # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007768706917984539&mobile_number=" + str(
                                mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                                nameee) + "&v4=" + str('and other') + "&v5=" + str('DGM(works)') + "&v6=" + "MP" + str(zone) + "&v6=" + str(
                                'https://qcportal.mpcz.in/')
                        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                        
                        
                        sms_template = message_template_log(template_id = '1007768706917984539',date = datetime.datetime.now(),mobile_number = mobile)
                        sms_template.save()
                        test = data.Primary_remark_rejection_counter
                        test = test + 1
                        data.Primary_remark_rejection_counter = test
                        if test >= 8:
                            user.final_rejection = 1
                            user.work_approval = -1
                            # send_mail(
                            #     'Approval status of DGM(Works) ',
                            #     'Hello ! Your application is finally rejected by DGM (Works) now.',
                            #     settings.EMAIL_HOST_USER,
                            #     [user.Email_Id],
                            #     fail_silently=False,
                            # )
                        user.save()

                    data.save()
                    counter = counter + 1
                    comment = comment + 1
                data = TKC_Document.objects.filter(
                    user_id=id).filter(Primary_verification_Status=2,Approval_doc=1)
                # if nz == 1:
                #     # send_mail(
                #     #     'Approval status of DGM(Works) ',
                #     #     'Hello ! Your are not approved by DGM (Works)',
                #     #     settings.EMAIL_HOST_USER,
                #     #     [user.Email_Id],
                #     #     fail_silently=False,
                #     # )
                # else:
                #     pass

                if not data:
                    data = User_Registration.objects.get(User_Id=id)
                    officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_name = officer_table.employ_name
                    offcier_designation = officer_table.designation
                    summary = reject_and_approve_summary(user=data,type="APPROVE",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
                    summary.save()
                    data.work_approval = 1
                    data.dgm_work_approved_date = datetime.datetime.now()
                    data.save()
                    if data.finance_approval == 1:
#                         employ_id = request.session['employ_login_id']
                        offcier_data = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
#                         offcier_data = Officer.objects.get(employ_login_id=employ_id)
                        zone = offcier_data.user_zone

                        if zone == 'CZ':
                            gmw = Officer.objects.filter(role='29')
                            for i in gmw:
                                number = i.mobile
                                name = i.employ_name
                                degi = i.designation
                                vname = data.CompanyName_E
                                
                                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}   
                                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007866081784871738&mobile_number=" + str(
                                    number) + "&v1=" + str(name) + "&v2=" + str(degi) + "&v3=" + str(vname) + "&v4=" + str() + "&v5=" + str()
                                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                                
                                sms_template = message_template_log(template_id = '1007866081784871738',date = datetime.datetime.now(),mobile_number = number)
                                sms_template.save()

                        elif zone == 'EZ':
                            gmw = Officer.objects.filter(role='44')
                            for i in gmw:
                                number = i.mobile
                                name = i.employ_name
                                degi = i.designation
                                vname = data.CompanyName_E
                                
                                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}   
                                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007866081784871738&mobile_number=" + str(
                                    number) + "&v1=" + str(name) + "&v2=" + str(degi) + "&v3=" + str(vname) + "&v4=" + str() + "&v5=" + str()
                                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                                sms_template = message_template_log(template_id = '1007866081784871738',date = datetime.datetime.now(),mobile_number = number)
                                sms_template.save()

                        elif zone == 'WZ':
                            gmw = Officer.objects.filter(role='45')
                            for i in gmw:
                                number = i.mobile
                                name = i.employ_name
                                degi = i.designation
                                vname = data.CompanyName_E
                                
                                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}   
                                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007866081784871738&mobile_number=" + str(
                                    number) + "&v1=" + str(name) + "&v2=" + str(degi) + "&v3=" + str(vname) + "&v4=" + str() + "&v5=" + str()
                                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                                
                                sms_template = message_template_log(template_id = '1007866081784871738',date = datetime.datetime.now(),mobile_number = number)
                                sms_template.save()
                                
                    # send_mail(
                        # 'Approval status of DGM(Works) ',
                        # 'Hello ! Your are approved by DGM (Works)',
                        # settings.EMAIL_HOST_USER,
                        # [data.Email_Id],
                        # fail_silently=False,
                    # )

                data = User_Registration.objects.filter(
                    work_approval=0, Complete_Details=1, User_type='TKC')

                return redirect('/dgm_work_pending')

                # return render(request, 'officer/dgm_work_pending.html',
                #               {'data': data, 'doc': doc})
            if data[0].User_type == "VENDOR":
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                user_data = User_Registration.objects.get(User_Id=id)
                doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
                doc1 = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
                doc2 = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)
                counter = 60
                comment = 0
                nn = 0

                list_all2=[]

                for data in doc:
               
                    pstatus = request.POST.get(f'{data.Vendor_Document_Id}')
                    premark = request.POST.get(f'a{data.Vendor_Document_Id}')
                    list_all2.append(pstatus)
                    if pstatus == "2":
                        data.Primary_verification_Status= 2
                        data.Status = 0
                        data.DGM_remark=premark
                        data.save()
                        user_data.work_approval = 2
                        user_data.dgm_work_reject_date = datetime.datetime.now()
                        user_data.save()
                        officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        officer_name = officer_table.employ_name
                        offcier_designation = officer_table.designation
                        summary = reject_and_approve_summary(user=user_data,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=premark,document=data.Ddocfile,document_name=data.Types_of_Docs)
                        summary.save()

                    elif pstatus == "1":
                        data.Primary_verification_Status = 1
                        data.DGM_remark=premark
                        data.save()
                list_all0=[]
                for data1 in doc1:
                    pstatus = request.POST.get(f'{data1.id}')
                    premark = request.POST.get(f'a{data1.id}')
                    list_all0.append(pstatus)
                    if pstatus == "2":
                        
                        data1.Primary_verification_Status= 2
                        data1.DGM_remark=premark
                        data1.Status = 0
                        data1.save()
                        user_data.work_approval = 2
                        user_data.dgm_work_reject_date = datetime.datetime.now()
                        user_data.save()
                        officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        officer_name = officer_table.employ_name
                        offcier_designation = officer_table.designation
                        summary = reject_and_approve_summary(user=user_data,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=premark)
                        summary.save()

                    elif pstatus == "1":
                        data1.Primary_verification_Status = 1
                        data1.Status = 1 
                        data1.DGM_remark=premark
                        data1.save()


                list_all=[]

                for data2 in doc2:

                # value = DI_Material_Offer_Serial_No.objects.get(id=data.id)
                    pstatus = request.POST.get(f'{data2.id}')
                    premark = request.POST.get(f'a{data2.id}')
                    list_all.append(pstatus)
                    if pstatus == "2":
                        
                        data2.Primary_verification_Status= 2
                        data2.DGM_remark=premark
                        data2.Status = 0
                        data2.save()
                        user_data.work_approval = 2
                        user_data.dgm_work_reject_date = datetime.datetime.now()
                        user_data.save()
                        officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        officer_name = officer_table.employ_name
                        offcier_designation = officer_table.designation
                        summary = reject_and_approve_summary(user=user_data,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=premark,document=data2.Document_Doc,document_name=data2.Types_of_Docs)
                        summary.save()

                    elif pstatus == "1":
                        data2.Primary_verification_Status = 1
                        data2.DGM_remark=premark
                        data2.save()
              
                if ("0") not in list_all and ("2") not in list_all and ("0") not in list_all0 and ("2") not in list_all0 and ("0") not in list_all2 and ("2") not in list_all2: 
                    data = User_Registration.objects.get(User_Id=id)
                    officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_name = officer_table.employ_name
                    offcier_designation = officer_table.designation
                    summary = reject_and_approve_summary(user=data,type="APPROVE",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
                    summary.save()
                    data.work_approval = 1
                    data.dgm_work_approved_date = datetime.datetime.now()
                    data.save()
                    # send_mail(
                        # 'Approval status of DGM(Finance) ',
                        # 'Hello ! You are approved by DGM (Finance)',
                        # settings.EMAIL_HOST_USER,
                        # [data.Email_Id],
                        # fail_silently=False,
                    # )
                    if data.finance_approval == 1:
                        # send_mail(
                            # 'Approved Profile ',
                            # 'Hello ! Your profile approved make payment for FI',
                            # settings.EMAIL_HOST_USER,
                            # [data.Email_Id],
                            # fail_silently=False,
                        # )
                        sms = User_Registration.objects.get(User_Id=id)
                        mobile = sms.ContactNo
                        name_sms = sms.CompanyName_E
                        zone = sms.User_zone
                        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                        # for server set proxy
                        # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007807022912614083&mobile_number=" + str(
                            mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                            'https://qcportal.mpcz.in/') + "&v4=" + str('11800') + "&v5=" + str(zone)
                        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

                data = User_Registration.objects.filter(
                    work_approval=0, Complete_Details=1, User_type='VENDOR')
                return redirect('vendor_dgm_work_pending')
        data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='TKC')
        return render(request, 'officer/dgm_work_pending.html',
                    {'data': data, 'total': total, 'approve': approve, 'pending': pending, 'approve_tkc': approve_tkc,
                    'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
    return redirect('/')


def dgm_finance_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = User_Registration.objects.filter(User_Id=id)
            if data[0].User_type == "TKC":
                approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                        User_type='VENDOR').count()
                pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                        User_type='VENDOR').count()
                total = approve + pending

                approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                            User_type='TKC').count()
                pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                            User_type='TKC').count()
                total_tkc = approve_tkc + pending_tkc
                late = TKC_Document.objects.filter(user_id=data[0].User_Id)
            
                latest = late.latest('new_data')
            
                if latest.new_data == 0:
                    doc = TKC_Document.objects.filter(user_id=data[0].User_Id,Approval_doc=2,new_data=0)

                elif latest.new_data == 1:
                    doc = TKC_Document.objects.filter(Approval_doc=2, user_id=data[0].User_Id,new_data=1)

                counter = 100
                comment = 0
                nn = 0
                for data in doc:
                    comm = request.POST.get(str(comment))
                    result = request.POST.get(str(counter))
                    if comm != '':
                        data.Primary_remark = comm

                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    data.Primary_verification_Date = datetime.datetime.now()
                    if result == 'OK':
                        data.Primary_verification_Status = 1
                    elif result == 'NOT':
                        nn = 1
                        user = User_Registration.objects.get(User_Id=id)
                        officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        officer_name = officer_table.employ_name
                        offcier_designation = officer_table.designation
                        summary = reject_and_approve_summary(user=user,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=comm,document=data.Ddocfile,document_name=data.Types_of_Docs)
                        summary.save()
                        user.finance_approval = 2
                        user.dgm_finance_reject_date = datetime.datetime.now()
                        user.save()
                        data.Primary_verification_Status = 2
                        data.Status = 0
                        test = data.Primary_remark_rejection_counter
                        nameee = data.Types_of_Docs
                        sms = User_Registration.objects.get(User_Id=id)
                        mobile = sms.ContactNo
                        zone = sms.User_zone
                        name_sms = sms.CompanyName_E
                        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                        # for server set proxy
                        # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007768706917984539&mobile_number=" + str(
                                mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                                nameee) + "&v4=" + str('and other') + "&v5=" + str('DGM(finance)') + "&v6=" + "MP" + str(zone) + "&v6=" + str(
                                'https://qcportal.mpcz.in/')
                        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                        
                        sms_template = message_template_log(template_id = '1007768706917984539',date = datetime.datetime.now(),mobile_number = mobile)
                        sms_template.save()

                        if test >= 8:
                            user.final_rejection = 1
                            user.finance_approval = -1
                            # send_mail(
                                # 'Approval status of DGM(Finance) ',
                                # 'Hello ! Your application is finally rejected by DGM (Finance) now',
                                # settings.EMAIL_HOST_USER,
                                # [user.Email_Id],
                                # fail_silently=False,
                            # )
                        user.save()
                        test = test + 1
                        data.Primary_remark_rejection_counter = test
                    data.save()
                    counter = counter + 1
                    comment = comment + 1
                data = TKC_Document.objects.filter(
                    user_id=id).filter(Primary_verification_Status=2, Approval_doc=2)
                # if nn == 1:
                #     # send_mail(
                #     #     'Rejection status of DGM(Finance) ',
                #     #     'Hello ! Your application is not approved by DGM (Finance).',
                #     #     settings.EMAIL_HOST_USER,
                #     #     [user.Email_Id],
                #     #     fail_silently=False,
                #     # )
                # else:
                #     pass
                if not data:
                    data = User_Registration.objects.get(User_Id=id)
                    officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_name = officer_table.employ_name
                    offcier_designation = officer_table.designation
                    summary = reject_and_approve_summary(user=data,type="APPROVE",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
                    summary.save()
                    data.finance_approval = 1
                    data.dgm_finance_approved_date = datetime.datetime.now()
                    data.save()
                    # send_mail(
                        # 'Approval status of DGM(Finance) ',
                        # 'Hello ! Your application is approved by DGM (Finance).',
                        # settings.EMAIL_HOST_USER,
                        # [data.Email_Id],
                        # fail_silently=False,
                    # )
                    if data.work_approval == 1:
                        employ_id = request.session['employ_login_id']
                        offcier_data = Officer.objects.get(employ_login_id=employ_id)
                        zone = offcier_data.user_zone
                        o_role = offcier_data.role
                        if zone == 'CZ':
                            gmw = Officer.objects.filter(role='29')
                           
                            for i in gmw:
                                number = i.mobile
                               
                                name = i.employ_name
                                degi = i.designation
                                vname = data.CompanyName_E
                                
                                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}   
                                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007866081784871738&mobile_number=" + str(
                                    number) + "&v1=" + str(name) + "&v2=" + str(degi) + "&v3=" + str(vname) + "&v4=" + str() + "&v5=" + str()
                                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                                
                                sms_template = message_template_log(template_id = '1007866081784871738',date = datetime.datetime.now(),mobile_number = number)
                                sms_template.save()

                        elif zone == 'EZ':
                            gmw = Officer.objects.filter(role=o_role)
                            for i in gmw:
                                number = i.mobile
                                name = i.employ_name
                                degi = i.designation
                                vname = data.CompanyName_E
                                
                                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}   
                                # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007866081784871738&mobile_number=" + str(
                                    number) + "&v1=" + str(name) + "&v2=" + str(degi) + "&v3=" + str(vname) + "&v4=" + str() + "&v5=" + str()
                                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                                
                                sms_template = message_template_log(template_id = '1007866081784871738',date = datetime.datetime.now(),mobile_number = number)
                                sms_template.save()

                        elif zone == 'WZ':
                            gmw = Officer.objects.filter(role=o_role)
                            for i in gmw:
                                number = i.mobile
                                name = i.employ_name
                                degi = i.designation
                                vname = data.CompanyName_E
                                
                                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}   
                                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007866081784871738&mobile_number=" + str(
                                    number) + "&v1=" + str(name) + "&v2=" + str(degi) + "&v3=" + str(vname) + "&v4=" + str() + "&v5=" + str()
                                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                                
                                sms_template = message_template_log(template_id = '1007866081784871738',date = datetime.datetime.now(),mobile_number = number)
                                sms_template.save()

                data = User_Registration.objects.filter(
                    finance_approval=0, Complete_Details=1, User_type='TKC')
                return redirect('/dgm_finance_pending')
            if data[0].User_type == "VENDOR":
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                doc = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
                counter = 100
                comment = 0
                for data in doc:
                    comm = request.POST.get(str(comment))
                    result = request.POST.get(str(counter))
                    if comm != '':
                        data.Primary_remark = comm
                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    data.Primary_verification_Date = datetime.datetime.now()
                    if result == 'OK':
                        data.Primary_verification_Status = 1
                    else:
                        user = User_Registration.objects.get(User_Id=id)
                        officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        officer_name = officer_table.employ_name
                        offcier_designation = officer_table.designation
                        summary = reject_and_approve_summary(user=user,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=comm)
                        summary.save()
                        user.finance_approval = 2
                        user.dgm_finance_reject_date = datetime.datetime.now()
                        data.Primary_verification_Status = 2
                        data.Status = 0
                        nameee = data.document_name
                        sms = User_Registration.objects.get(User_Id=id)
                        mobile = sms.ContactNo
                        zone = sms.User_zone
                        name_sms = sms.CompanyName_E
                        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                        # for server set proxy
                        # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007768706917984539&mobile_number=" + str(
                                mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                                nameee) + "&v4=" + str('and other') + "&v5=" + str('DGM(finance)') + "&v6=" + "MP" + str(zone) + "&v6=" + str(
                                'https://qcportal.mpcz.in/')
                        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                        
                        sms_template = message_template_log(template_id = '1007768706917984539',date = datetime.datetime.now(),mobile_number = mobile)
                        sms_template.save()

                        # send_mail(
                            # 'Rejection status of DGM(Finance) ',
                            # 'Hello ! Your are not approved by DGM (Finance)',
                            # settings.EMAIL_HOST_USER,
                            # [user.Email_Id],
                            # fail_silently=False,
                        # )
                        test = data.Primary_remark_rejection_counter
                        if test >= 8:
                            user.final_rejection = 1
                            user.finance_approval = -1
                            # send_mail(
                                # 'Rejection status of DGM(Finance) ',
                                # 'Hello ! Your application is finally rejected by DGM (Finance) now',
                                # settings.EMAIL_HOST_USER,
                                # [user.Email_Id],
                                # fail_silently=False,
                            # )
                        user.save()
                        test = test + 1
                        data.Primary_remark_rejection_counter = test
                    data.save()
                    counter = counter + 1
                    comment = comment + 1
                data = Vendor_BalanceSheet.objects.filter(
                    user_id=id).filter(Primary_verification_Status=2)
                if not data:
                    data = User_Registration.objects.get(User_Id=id)
                    officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_name = officer_table.employ_name
                    offcier_designation = officer_table.designation
                    summary = reject_and_approve_summary(user=data,type="APPROVE",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
                    summary.save()
                    data.finance_approval = 1
                    data.dgm_finance_approved_date = datetime.datetime.now()
                    data.save()
                    # send_mail(
                        # 'Approval status of DGM(Finance) ',
                        # 'Hello ! You are approved by DGM (Finance)',
                        # settings.EMAIL_HOST_USER,
                        # [data.Email_Id],
                        # fail_silently=False,
                    # )
                    if data.work_approval == 1:
                        # send_mail(
                            # 'Approved Profile ',
                            # 'Hello ! Your profile approved make payment for FI',
                            # settings.EMAIL_HOST_USER,
                            # [data.Email_Id],
                            # fail_silently=False,
                        # )
                        sms = User_Registration.objects.get(User_Id=id)
                        mobile = sms.ContactNo
                        name_sms = sms.CompanyName_E
                        zone = sms.User_zone
                        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                        # for server set proxy
                        # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007807022912614083&mobile_number=" + str(
                            mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                            'https://qcportal.mpcz.in/') + "&v4=" + str('11800') + "&v5=" + str(zone)
                        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                        
                        sms_template = message_template_log(template_id = '1007807022912614083',date = datetime.datetime.now(),mobile_number = mobile)
                        sms_template.save()
                        
                data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR')

                approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                        User_type='VENDOR').count()
                pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                        User_type='VENDOR').count()
                total = approve + pending

                approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                            User_type='TKC').count()
                pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                            User_type='TKC').count()
                total_tkc = approve_tkc + pending_tkc
                return redirect('vendor_dgm_finance_pending')

        data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC')

        approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
        total = approve + pending

        approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                    User_type='TKC').count()
        pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                    User_type='TKC').count()
        total_tkc = approve_tkc + pending_tkc
        return render(request, 'officer/dgm_finance_pending.html',
                    {'data': data, 'total': total, 'approve': approve, 'pending': pending, 'approve_tkc': approve_tkc,
                    'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
    return redirect('/')


def vendor_cgm_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                User_type='VENDOR').count()
        pending = User_Registration.objects.filter(Complete_Details=1, work_approval=1, cgm_approval=0, finance_approval=1,
                                                User_type='VENDOR').count()
        total = approve + pending
        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()

        total_nabl = approve_nabl + pending_nabl
        if data[0].User_type == "VENDOR":
            vendor = User_Registration.objects.get(User_Id=id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            #BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)
            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
#             fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
            fac_image = Vendor_Factory_image.objects.filter(vendor=vendor)
            Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id,Primary_verification_Status=1)
            tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)
            vendor = User_Registration.objects.get(User_Id=id)
            apprisal = []
            fi_tech = []
            if FI_Appraisal_Details.objects.filter(vendor=vendor).exists():
                apprisal = FI_Appraisal_Details.objects.get(vendor=vendor)
                fi_tech = Factory_Technical_Details.objects.filter(vendor=vendor).last()
            return render(request, 'officer/vendor_cgm_evaluate.html',
                        {'data': data[0], 'doc': doc, 'doc1': doc1, 'Material': Material,
                        'tech_data': tech_data, 'total': total, 'approve': approve, 'pending': pending,
                        'approve_nabl': approve_nabl,
                        'pending_nabl': pending_nabl, 'total_nabl': total_nabl, 'CompanyData': CompanyData1,
                        'AuthorisedPerson1': AuthorisedPerson1,
                        #'BankDetails': BankDetails1, 'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech,
                        'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech,
                        'fac_image': fac_image})
        doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
        Factory = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
        Material = Add_material.objects.filter(user_id=data[0].User_Id)
        return render(request, 'officer/vendor_wnp_evaluate.html',
                    {'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material, 'total': total,
                    'approve': approve, 'pending': pending, 'approve_nabl': approve_nabl,
                    'pending_nabl': pending_nabl, 'total_nabl': total_nabl})
    return redirect('/')

def remove_vendor_material(request,id):
    if request.method == 'POST':
        data = Vendor_Material_Details.objects.get(id=id)
        user = data.user_id.User_Id
        data.DGM_remark = request.POST.get('remark_cgm')
        data.Primary_verification_Status = 0
        data.save()
        return redirect('/vendor_cgm_evaluate/' + str(user))
    return render(request, 'officer/vendor_cgm_evaluate.html')





def nabl_dgm_qc_evaluate_pending(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                        User_type='NABL').count()
        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                        User_type='NABL').count()

        total_nabl = approve_nabl + pending_nabl
        if data[0].User_type == "NABL":
            # doc = NABL_Document.objects.filter(user_id=id)
            # doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
            AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
            #BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)
            mat= NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
            
            return render(request, 'officer/nabl_dgm_qc_evaluate_pending.html',
                        {'data': data[0], 'doc': doc, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                        'total_nabl': total_nabl,'CompanyData': CompanyData1, 'AuthorisedPerson': AuthorisedPerson1,
                        "mat1":mat})
    return redirect('/')

def nabl_dgm_qc_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        user_data = User_Registration.objects.get(User_Id=id)
        doc = NABL_Document.objects.filter(user_id=user_data.User_Id)
        if request.method == 'POST':
            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            counter = 60
            comment = 0
            nn = 0
            list_all2=[]
            for data in doc:
                pstatus = request.POST.get(f'{data.id}')
                premark = request.POST.get(f'a{data.id}')
                list_all2.append(pstatus)
                if pstatus == "2":
                    data.Primary_verification_Status= 2
                    data.Status = 0
                    data.Primary_remark=premark
                    data.save()
                    user_data.qc_approval = 2
                    user_data.save()
                    officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                    officer_name = officer_table.employ_name
                    offcier_designation = officer_table.designation
                    summary = reject_and_approve_summary(user=user_data,type="REJECT",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation,remark=premark,document=data.Ddocfile,document_name=data.Types_of_Docs)
                    summary.save()
                elif pstatus == "1":
                    data.Primary_verification_Status = 1
                    data.Primary_remark=premark
                    data.save()
            if ("0") not in list_all2 and ("2") not in list_all2 :
                data = User_Registration.objects.get(User_Id=id)
                data.qc_approval = 1
                data.save()
                officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                officer_name = officer_table.employ_name
                offcier_designation = officer_table.designation
                summary = reject_and_approve_summary(user=user_data,type="APPROVED",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
                summary.save()
              
                data = User_Registration.objects.filter(
                    qc_approval=0, Complete_Details=1, User_type='NABL')
                return render(request, 'officer/nabl_dgm_qc_pending.html',
                            {'data': data })

        data = User_Registration.objects.filter(
            qc_approval=0, Complete_Details=1, User_type='NABL')
        return render(request, 'officer/nabl_dgm_qc_pending.html',
                    {'data': data })

    return redirect('/')

# poornima
def resubmit_cgm(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        if data[0].User_type == "VENDOR":
           CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
        AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
        BankDetails1 = []
        if BankDetails.objects.filter(user_id=data[0].ContactNo).exists():
            BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)
        doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
        doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
        fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
        fac_image = Vendor_Factory_image.objects.filter(Factory=fac[0])
        Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
        tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)
        vendor = User_Registration.objects.get(User_Id=id)
        apprisal = []
        fi_tech = []
        if FI_Appraisal_Details.objects.filter(vendor=vendor).exists():
            apprisal = FI_Appraisal_Details.objects.get(vendor=vendor)
            fi_tech = Factory_Technical_Details.objects.filter(vendor=vendor).last()
        return render(request, 'officer/vendor_cgm_complet_view.html',
                      {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
                       'tech_data': tech_data,
                       'CompanyData': CompanyData1,
                       'AuthorisedPerson1': AuthorisedPerson1,
                       'BankDetails': BankDetails1, 'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech,
                       'fac_image': fac_image})

        if data[0].User_type == "TKC":
            doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1)

            return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                        {'data': data[0], 'doc': doc, })

        if data[0].User_type == "NABL":
            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            return render(request, 'officer/nabl_resubmit_pending_view_work.html',
                        {'data': data[0], 'doc': doc, })

        return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                    {'data': data[0], 'doc': doc})

    return redirect('/')


def upload_basic_details(requests):
    return render(requests, 'upload/upload_basic_details.html')

from django.core.paginator import Paginator
def payment(requests):
    # pay_obj = Payudata_main.objects.all()
    pay_obj = Payudata_main.objects.filter(Payu_Status="success")

    paginator = Paginator(pay_obj, 25) # Show 25 contacts per page.
    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(requests, 'main/payment.html', {'pay_obj':pay_obj, 'page_obj':page_obj})



def Exam(requests):
    total = 7
    ur = 3
    ur_f = 1
    st = 1
    sc = 1
    obc = 2
    data = Exam_Data.objects.all()
    for data in data:
        data.select = 0
        data.save()
    data = Exam_Data.objects.filter(select="0",marks__gte=60,age__lte=40).order_by('-score','-age')[:2]
    for data in data:
        data.select = 1
        data.select_category = 'UR'
        data.save()
    if Exam_Data.objects.filter(select="1",gender = "F" ,marks__gte=60,age__lte=40).exists():
        data = Exam_Data.objects.filter(select="0").order_by('-score','-age')[:1]
        selected = Exam_Data.objects.get(user=data[0].user)
        selected.select = 1
        selected.select_category = 'UR'
        selected.save()
    else:
        data = Exam_Data.objects.filter(select="0",gender = "F" ,marks__gte=60,age__lte=40).order_by('-score','-age')[:1]
        selected = Exam_Data.objects.get(id=data[0].id)
        selected.select = 1
        selected.select_category = 'UR'
        selected.save()
    data = Exam_Data.objects.filter(select="0", category="ST").order_by('-score','-age')[:1]
    for data in data:
        data.select = 1
        data.select_category = 'ST'
        data.save()
    data = Exam_Data.objects.filter(select="0", category="SC").order_by('-score', '-age')[:1]
    for data in data:
        data.select = 1
        data.select_category = 'SC'
        data.save()
    data = Exam_Data.objects.filter(select="0", category="OBC").order_by('-score', '-age')[:2]
    for data in data:
        data.select = 1
        data.select_category = 'OBC'
        data.save()
    data1 = Exam_Data.objects.filter(select="1")
    return render(requests, 'main/exam.html', {'data': data1})


def databaseDB(request):
    usr_obj = User_Registration.objects.filter(User_zone="CZ")
    return render(request, 'main/databaseDB.html', {"usr_obj":usr_obj})

def databaseView(request):
    usr_obj = User_Registration.objects.all()
    return render(request, 'main/databaseView.html', {"usr_obj":usr_obj})

def databaseView2(request, User_Id):
    usr_obj = User_Registration.objects.get(User_Id=User_Id)
    cdmu_obj = UserCompanyDataMain.objects.get(user_id_id=usr_obj)
    ap_obj = AuthorisedPerson.objects.get(user_id_id=usr_obj)
    bnk_obj = BankDetails.objects.get(user_id=usr_obj.ContactNo)
    return render(request, 'main/databaseView2.html', {"usr_obj":usr_obj, "cdmu_obj":cdmu_obj, 
                                                       "ap_obj":ap_obj, "bnk_obj":bnk_obj })



# #Jeevan ERP Integration Code
# def ErpPushViewId(request):
#     usr_obj = User_Registration.objects.all()
#     return render(request, 'main/ERP_push1.html', {'usr_obj':usr_obj})

#Aayush Updated ERP Integration Code
def ErpPushViewId(request):
    usr_obj = User_Registration.objects.filter(User_type='VENDOR',cgm_approval=1,digital_cert_upload=1)
    # print("usr_obj values--->",usr_obj)
    return render(request, 'main/ERP_push1.html', {'usr_obj':usr_obj})


import json
import requests as req
from requests.auth import HTTPBasicAuth
# def ErpPush(request, id):
#     usr_obj = User_Registration.objects.get(User_Id=id)
#     com_obj = UserCompanyDataMain.objects.get(user_id_id=usr_obj)
#     URL = "http://nprodap1.mpcz.in:8004/webservices/rest/qc_portal_register_vendor/register_vendor/"
#     Username = 'QC_EBS_USER';
#     Password = "Welcome123";
#     data = {
#         "register_vendor": {
#             "@xmlns": "http://xmlns.oracle.com/apps/ap/rest/qc_portal_register_vendor/register_vendor/",
#             "RESTHeader": {
#                 "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
#                 "Responsibility": "JAI_PAYABLES",
#                 "RespApplication": "JA",
#                 "SecurityGroup": "STANDARD",
#                 "NLSLanguage": "AMERICAN",
#                 "Org_Id": "82"
#             },
#             "InputParameters": {
#                 "P_PORTAL_VENDOR_NUMBER": id,
#                 "P_VENDOR_NAME": usr_obj.CompanyName_E,
#                 "P_VENDOR_TYPE": "VENDOR",
#                 "P_ENABLED_FLAG": "Y",
#                 "P_PAN_NUMBER": usr_obj.Pancard,
#                 "P_SITES" : {
#                     "P_SITES_ITEM": [
#                         {
#                             "SITE_CODE":com_obj.Company_dist,
#                             "CURRENCY": "INR",
#                             "ADDRESS1": com_obj.Company_add_1,
#                             "ADDRESS2": com_obj.Company_add_2,
#                             "ADDRESS3": '',
#                             "CITY": com_obj.Company_dist,
#                             "STATE": com_obj.Company_state,
#                             "PIN": com_obj.Company_pin_code,
#                             "EMAIL_ADDRESS":usr_obj.Email_Id,
#                             "ENABLED_FLAG": "Y",
#                             "BANK": "",
#                             "IFSC_CODE": "",
#                             "BANK_BRANCH": "",
#                             "BRANCH_ADDRESS": "",
#                             "ACCOUNT_NUMBER": "",
#                             "GST_NUMBER": com_obj.Company_Gst_No,
#                         }
#                     ]
#                 }
#             }
#         }
#     }
#     json_data = json.dumps(data)
#     auth_values = HTTPBasicAuth(Username, Password)
#     headers = {'Content-type': 'application/json'}
    # res = req.post(url=URL, auth=auth_values, headers=headers, data=json_data)
    # if res.status_code == 200:
    #     data = res.json()
    #     response = data['OutputParameters']
    #     print('ccccccccccccccczzzzzzzzzzzzzzzz',response)
        # v_id = response['P_VENDOR_ID']
        # usr_obj.erp_cz_id = v_id
        # usr_obj.save()
    # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    # res = req.post(url='https://prodserv.mpwin.co.in:8070/webservices/rest/QC_PORTAL_REGISTER_VENDOR/register_vendor/', auth=auth_values, headers=headers, data=json_data)
    # if res.status_code == 200:
    #     data = res.json()
    #     response = data['OutputParameters']
    #     P_VENDOR_DETAILS = response['P_VENDOR_DETAILS']
    #     usr_obj.erp_ez_id = response['VENDOR_ID']
    #     usr_obj.erp_cz_id = response['VENDOR_ID']
    #     # usr_obj.save()
    #     print('ttttttttttttttttttttttttttttttttttttttttt',response)
    # usr_obj = User_Registration.objects.all()
    
    # try:
    #     return render(request, 'main/ERP_push1.html', {'usr_obj':usr_obj})
    # except Exception as e:
    #     return render(requests, 'main/ERP_push1.html', {'usr_obj':usr_obj})


#Added By Aayush Joshi
#Pushing Data into ERP based on Discom
def ErpPush(request, id,discom_name=None):
    print("id---->",id)
    print("discom_name------>",discom_name)
    if discom_name == "WZ":
        #pushing data into West Zone ERP
        print("#pushing data into West Zone ERP")
        api_status_flag,is_data_pushed,is_data_failed_pushed,res_data=data_push_in_erp_api_call(request,id=id,discom_name=discom_name)

    if discom_name == "CZ":
        #pushing data into CZ Zone ERP
        print("#pushing data into CZ Zone ERP")
        api_status_flag,is_data_pushed,is_data_failed_pushed,res_data=data_push_in_erp_api_call(request,id=id,discom_name=discom_name)
    
    if discom_name == "EZ":
        #pushing data into EZ Zone ERP
        print("#pushing data into EZ Zone ERP")
        # api_status_flag,is_data_pushed,is_data_failed_pushed,res_data=data_push_in_erp_api_call(request,id=id,discom_name=discom_name)
        return HttpResponse("Sorry But API is Not given AS of Now for Register Vendor API for EZ")
    print("88888888888888888888888888")
    print(f'printing data info:"api_status_flag"{api_status_flag},is_data_pushed:{is_data_pushed},is_data_failed_pushed:{is_data_failed_pushed},res_data:{res_data}')
    print("88888888888888888888888888")
    usr_obj=User_Registration.objects.filter(User_type='VENDOR',cgm_approval=1,digital_cert_upload=1)
    # print("usr_obj-----valueooo->",usr_obj)
    if is_data_pushed and api_status_flag == True:
        print("yuuuuuuuuuuu")
        return render(request, 'main/ERP_push1.html', {'usr_obj':usr_obj})
    
    elif is_data_failed_pushed == True and api_status_flag == True:
        print("fffffiuuuuuuuuuuuuuu")
        usr_obj_one=User_Registration.objects.get(User_Id=id,User_type='VENDOR',cgm_approval=1,digital_cert_upload=1)
        message =messages.info(request, f'Unable to push data into erp as {res_data} of {usr_obj_one.CompanyName_E}')
        return render(request, 'main/ERP_push1.html', {'usr_obj':usr_obj,'message': message})
        # return render(request, 'main/error_page.html')
    elif api_status_flag == False :
        print("fffffiuuuuuuuuuuuuuu")
        return render(request, 'main/error_page.html')


def RCA_ErpPushViewId(request):
    usr_obj = Rca_User_Registration.objects.filter(User_zone= request.session['zone'])
    return render(request, 'main/RCA_ERP_push.html', {'usr_obj':usr_obj})

def RCA_ErpPush(request, id):
    usr_obj = Rca_User_Registration.objects.get(User_Id=id)
    # com_obj = Rca_Vendor_Document.objects.get(user_id=usr_obj.ContactNo)
    URL = "http://nprodap1.mpcz.in:8004/webservices/rest/qc_vendor_registration/register_vendor/"
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
                "P_PORTAL_VENDOR_NUMBER": id,
                "P_VENDOR_NAME": usr_obj.CompanyName_E,
                "P_VENDOR_TYPE": "RCA VENDOR",
                "P_ENABLED_FLAG": "Y",
                "P_PAN_NUMBER": usr_obj.Company_Pan_No,
                "P_SITES" : {
                    "P_SITES_ITEM": [
                        {
                            "SITE_CODE":usr_obj.Company_dist,
                            "CURRENCY": "INR",
                            "ADDRESS1": usr_obj.Company_add_1,
                            "ADDRESS2": usr_obj.Company_add_2,
                            "ADDRESS3": '',
                            "CITY": usr_obj.Company_dist,
                            "STATE": usr_obj.Company_state,
                            "PIN": usr_obj.Company_pin_code,
                            "EMAIL_ADDRESS":usr_obj.Email_Id,
                            "ENABLED_FLAG": "Y",
                            "BANK": "",
                            "IFSC_CODE": "",
                            "BANK_BRANCH": "",
                            "BRANCH_ADDRESS": "",
                            "ACCOUNT_NUMBER": "",
                            "GST_NUMBER": usr_obj.Company_Gst_No,
                        }
                    ]
                }
            }
        }
    }
    json_data = json.dumps(data)
    print('jeevan',json_data)
    auth_values = HTTPBasicAuth(Username, Password)
    headers = {'Content-type': 'application/json'}
    res = req.post(url=URL, auth=auth_values, headers=headers, data=json_data)
    print('res',res)
    if res.status_code == 200:
        print('res')
        data = res.json()
        response = data['OutputParameters']
        vendor = response['P_VENDOR_DETAILS']
        usr_obj.erp_cz_id = vendor['VENDOR_ID']
        usr_obj.erp_cz_number = vendor['VENDOR_NUMBER']
        usr_obj.save()
    usr_obj = Rca_User_Registration.objects.filter(User_zone= request.session['zone'])
    return render(request, 'main/RCA_ERP_push.html', {'usr_obj':usr_obj})





def roof_top_discom(request):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            agency_name = request.POST.get('one')
            auth_p = request.POST.get('two')
            contact = request.POST.get('three')
            email = request.POST.get('four')
            pan = request.POST.get('five')
            gst = request.POST.get('six')
            address = request.POST.get('newone')
            print("gggggggggg",address)
            
            if roof_top_first.objects.filter(pan_card=pan).exists():            
                messages.warning(request, "Pan Card number already exists ")
                return render(request, 'roof/agent_first.html')
            elif roof_top_first.objects.filter(contact=contact).exists():
                messages.warning(request, "Mobile  number already exists ")
                return render(request, 'roof/agent_first.html')

            else:
                save_data = roof_top_first(agency_name=agency_name,address=address,name_of_auth=auth_p,pan_card=pan,contact=contact,email=email,created_by='discom')
                save_data.save()
                id_id = roof_top_first.objects.filter(contact=contact)

                request.session['id_id'] = id_id[0].id
                return redirect('roof_top_upload_discom')
        return render(request,'main/agent.html')

    return redirect('/')



def roof_top_upload_discom(request):
    if request.session.has_key('employ_login_id'):
        
        if request.method == 'POST':
            data = roof_top_first.objects.get(id=request.session['id_id'])
            user_id = data.id
            reg_number = request.POST.get('one')
            v_upload_file_factory2 = request.FILES['two']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='Company Registration No.', Document_Number=reg_number,Ddocfile=v_upload_file_factory2,Status=1)
            data1.save()

         
            number = request.POST.get('three')
            v_upload_file_factory3 = request.FILES['four']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='GST Certificate with  Challan',
                                    Document_Number=number, Status=1,Ddocfile=v_upload_file_factory3)
            data1.save()

            reg_number = request.POST.get('five')
            upload = request.FILES['six']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='Pan Card Details',
                                    Document_Number=reg_number, Ddocfile=upload, Status=1)
            data1.save()



            number = request.POST.get('seven')
            upload = request.FILES['eight']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='A/B class Electrical License Undertaking',
                                    Document_Number=number, Ddocfile=upload, Status=1)
            data1.save()


            
            gst_card_no = request.POST.get('nine')
            document = request.FILES['ten']

            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='Aadhar Card Details',
                                Document_Number=gst_card_no, Ddocfile=document,Status=1)
            data1.save()

            gst_card_no = request.POST.get('eleven')
            document = request.FILES['twelve']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='MSME Registration for Solar System',Document_Number=gst_card_no,
                                Ddocfile=document,Status=1)
            data1.save()


            data = roof_top_first.objects.filter(id=request.session['id_id'])
            data.update(profile_complete=1)
            return render(request,'officer/discom_base.html')
        return render(request, 'main/Agent2.html')

    return redirect('/')




def roof_top_filling_pending_list(request):
    if request.session.has_key('employ_login_id'):
        abc = roof_top_first.objects.filter(profile_complete=0,created_by='discom')
        return render(request,'main/roof_top_form_pending_list.html',{'data':abc})
    return redirect('/')



def roof_top_filling_pending_form(request,id):
    request.session['id_id'] = id
    if request.session.has_key('employ_login_id'):
        if roof_top_first.objects.filter(id=id,profile_complete=0).exists():
            return redirect('/roof_top_upload_discom')
    return redirect('/')



def roof_toop_officer_pending(request):
    if request.session.has_key('officer'):
        if request.session['user_zone'] == 'WZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=0,payment=1,user_zone='WZ')
            return render(request, 'officer/roof_toop_pending_vendor.html', {'data': data})

        elif request.session['user_zone'] == 'CZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=0,payment=1,user_zone='CZ')
            return render(request, 'officer/roof_toop_pending_vendor.html', {'data': data})

        elif request.session['user_zone'] == 'EZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=0,payment=1,user_zone='EZ')
            return render(request, 'officer/roof_toop_pending_vendor.html', {'data': data})

    return redirect('/')
    

def roof_toop_officer_evaluate(request, id):
    data = roof_top_first.objects.filter(id=id)
    doc = roof_top_sec.objects.filter(user_id=data[0].id)
    return render(request, 'officer/roof_toop_officer_evaluate.html',{'abc':doc,'data':data[0]})


def roof_toop_officer_dashboard(request):
    return render(request, 'officer/RoofTop_Viewer_base.html')


def roof_toop_officer_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = roof_top_first.objects.filter(id=id)    
            print("xxxxxxxxxxxxxxx",data)      
            doc = roof_top_sec.objects.filter(user_id=data[0].id)
            print("yyyyyyyyyyyyyyy",doc)
            counter = 100
            comment = 0
            nz = 0
            print("onnnnnnnnneee")
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                print("result",result)
                if comm != '':
                    data.Primary_remark = comm
                
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                data.Primary_verification_Date = datetime.datetime.now()
                if result == 'OK':
                    print("rrrrrrrrrrrrrrrrr")
                    data.Primary_verification_Status = 1
                elif result == 'NOT':
                    print("gggggggggggggggggggggg")
                    nz = 1
                    user = roof_top_first.objects.get(id=id)
                    user.viewer_officer = 2
                    user.save()
                    data.Primary_verification_Status = 2
                    data.Status = 0
                    mobile = user.contact
                    name_sms = user.agency_name
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                        # for server set proxy
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str() + "&v4=" + str() + "&v5=" + str(
                        'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('Roof Top Approver Officer') + "&v9=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1007490758019902962',date = datetime.datetime.now(),mobile_number = mobile)
                    sms_template.save()
                   
                    # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    test = data.Primary_remark_rejection_counter
                    test = test + 1
                    data.Primary_remark_rejection_counter = test
                    if test >= 8:
                        user.final_rejection = 1
                        user.viewer_officer = -1
                        
                    user.save()

                data.save()
                counter = counter + 1
                comment = comment + 1
                data = roof_top_sec.objects.filter(
                    user_id=id).filter(Primary_verification_Status=2)
             

            if not data:
                data = roof_top_first.objects.get(id=id)
                data.viewer_officer = 1
                data.save()
            
            return redirect ('roof_toop_officer_dashboard')







def roof_toop_officer_complete_list(request):
    if request.session.has_key('officer'):

        if request.session['user_zone'] == 'WZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,user_zone='WZ')
            return render(request, 'officer/roof_toop_officer_complete_list.html', {'data': data})

        elif request.session['user_zone'] == 'CZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,user_zone='CZ')
            return render(request, 'officer/roof_toop_officer_complete_list.html', {'data': data})

        elif request.session['user_zone'] == 'EZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,user_zone='EZ')
            return render(request, 'officer/roof_toop_officer_complete_list.html', {'data': data})

    return redirect('/')

def roof_toop_officer_complete_view(request, id):
    data = roof_top_first.objects.filter(id=id)
    doc = roof_top_sec.objects.filter(user_id=data[0].id)
    return render(request, 'officer/roof_toop_officer_complete_view.html',{'abc':doc,'data':data[0]})






 
def roof_toop_approver_officer_pending(request):
    if request.session.has_key('officer'):
        if request.session['user_zone'] == 'WZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,approver_officer=0,user_zone='WZ')
            return render(request, 'officer/roof_toop_approver_officer_pending.html', {'data': data})


        elif request.session['user_zone'] == 'EZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,approver_officer=0,user_zone='EZ')
            return render(request, 'officer/roof_toop_approver_officer_pending.html', {'data': data})

        elif request.session['user_zone'] == 'CZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,approver_officer=0,user_zone='CZ')
            return render(request, 'officer/roof_toop_approver_officer_pending.html', {'data': data})


    return redirect('/')


def roof_toop_approver_officer_evaluate(request, id):
    if request.session.has_key('employ_login_id'):
        data = roof_top_first.objects.filter(id=id)
        doc = roof_top_sec.objects.filter(user_id=data[0].id)
        data = roof_top_first.objects.filter(id=id)
        def generateOTP():
            OTP = ""
            digits = "0123456789"
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            return OTP
        otp = generateOTP()
        return render(request, 'officer/roof_toop_approver_officer_evaluate.html',{'abc':doc,'data':data[0],'otp':otp})

    return redirect('/')


def roof_toop_approver_officer_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'): 
        return render(request, 'officer/roof_toop_approver_officer_evaluate.html')






def roof_toop_approver_complete_list(request):
    if request.session.has_key('officer'):
        if request.session['user_zone'] == 'WZ':
            data = roof_top_first.objects.filter(profile_complete=1,approver_officer=1,user_zone='WZ').order_by('agency_name')
            return render(request, 'officer/roof_toop_approver_complete_list.html', {'data': data})

        elif request.session['user_zone'] == 'CZ':
            data = roof_top_first.objects.filter(profile_complete=1,approver_officer=1,user_zone='CZ').order_by('agency_name')
            return render(request, 'officer/roof_toop_approver_complete_list.html', {'data': data})


        elif request.session['user_zone'] == 'EZ':
            data = roof_top_first.objects.filter(profile_complete=1,approver_officer=1,user_zone='EZ').order_by('agency_name')
            return render(request, 'officer/roof_toop_approver_complete_list.html', {'data': data})


    return redirect('/')

def roof_toop_approver_complete_view(request, id):
    data = roof_top_first.objects.filter(id=id)
    doc = roof_top_sec.objects.filter(user_id=data[0].id)
    return render(request, 'officer/roof_toop_approver_complete_view.html',{'abc':doc,'data':data[0]})






def root_top_otp(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = roof_top_first.objects.filter(id=id)    
            doc = roof_top_sec.objects.filter(user_id=data[0].id)
            counter = 100
            comment = 0
            nz = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                data.Primary_verification_Date = datetime.datetime.now()
                if result == 'OK':
                    data.Primary_verification_Status_approver = 1
                elif result == 'NOT':
                    nz = 1
                    user = roof_top_first.objects.get(id=id)
                    user.approver_officer = 2
                    user.save()
                    data.Primary_verification_Status_approver = 2
                    data.Status = 0
                    mobile = user.contact
                    name_sms = user.agency_name
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                        # for server set proxy
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str() + "&v4=" + str() + "&v5=" + str(
                        'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('Roof Top Approver Officer') + "&v9=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1007490758019902962',date = datetime.datetime.now(),mobile_number = mobile)
                    sms_template.save()
                   
                    # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    test = data.Primary_remark_rejection_counter
                    test = test + 1
                    data.Primary_remark_rejection_counter = test
                    if test >= 8:
                        user.final_rejection = 1
                        user.approver_officer = -1
                        
                    user.save()

                data.save()
                counter = counter + 1
                comment = comment + 1
                data = roof_top_sec.objects.filter(user_id=id).filter(Primary_verification_Status_approver=2)
             

            if not data:
                abc = roof_top_first.objects.filter(id=id)  
                abcd = abc[0].user_type
                # if abcd == 'Empanelled for solar subsidy':
                #     pass  # 18/01/20
                  

                abc = roof_top_first.objects.filter(id=id)   
                reg_date = abc[0].reg_date 
             
                from datetime import datetime as dt
                
                if abcd == 'Empanelled for solar subsidy':
                    from datetime import date
                    from datetime import time
                    from datetime import datetime
                    import datetime
                    final_exp_date = datetime.date(2024, 1, 18)
                else:
                    from dateutil.relativedelta import relativedelta
                    reg_date = datetime.datetime.now()
                    final_exp_date = reg_date + relativedelta(years=2)    
              
                data = roof_top_first.objects.get(id=id)
                data.approver_officer = 1
                data.save()
                officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                officer_mobile = officer.mobile
                def generateOTP():
                    OTP = ""
                    digits = "0123456789"
                    for i in range(6):
                        OTP += digits[math.floor(random.random() * 10)]
                    return OTP
                otp = generateOTP()
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otp) + "&v2=" + str()
                response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
                sms_template.save()


                request.session['certificate_otp'] = otp
                print(otp)
                request.session['officer_mobile'] = officer_mobile
                return render(request, 'roof/roof_top_otp.html', {'id':id})    

            return redirect ('roof_toop_approver_officer_pending')

        return redirect('/')




def root_top_otp2(request,id):
    if request.session.has_key('certificate_otp'):
        if request.method == 'POST':
            otp = request.POST.get('roof_top_otp')
            if request.session['certificate_otp'] == otp:

###################################################################################
                from datetime import datetime
                td = datetime.now()
                current_time = td.strftime("%H:%M:%S")

                import datetime as dt
                dayy = dt.datetime.now().date()
                

                import datetime as dt
                import calendar
                day = dt.datetime.now().date()
                three_year_delta = dt.timedelta(days=1096 if ((day.month >= 3 and calendar.isleap(day.year + 3)) or (day.month < 3 and calendar.isleap(day.year))) else 1095)
                valid_upto = day + three_year_delta
                
                # rm_obj = Role_Master.objects.get(Role_Name='RoofTop_Approver')
                Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
            

                import random
                from datetime import datetime
                s = ""
                list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                t_date = datetime.today().strftime('%Y%m%d')
                if Officer_obj.user_zone == 'CZ':
                    s = s + "CZ" + "S" + t_date + random.choice(list1) + random.choice(list1)

                elif Officer_obj.user_zone == 'WZ':
                    
                    s = s + "WZ" + "S" + t_date + random.choice(list1) + random.choice(list1)

                else:
                    s = s + "EZ" + "S" + t_date + random.choice(list1) + random.choice(list1)

                abc = roof_top_first.objects.filter(id=id)  
                abcd = abc[0].user_type
                m_mobile = abc[0].contact
                cname = abc[0].agency_name

                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}

                # proxyDict = {"http" : "proxy.mpcz.in:8000"}

                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007686693598132208&mobile_number=" + str(
                    m_mobile) + "&v1=" + str(cname) + "&v2=" + str() + "&v3=" + str('Roof Top Solar Vendor') + "&v4=" + str(
                    'https://qcportal.mpcz.in/')
                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1007686693598132208',date = datetime.now(),mobile_number = m_mobile)
                sms_template.save()
                
                abc = roof_top_first.objects.filter(id=id)   
                reg_date = abc[0].reg_date 
                reg_date = datetime.now()
                

                from datetime import datetime as dt
                
                if abcd == 'Empanelled for solar subsidy':
                    import datetime
                    final_exp_date = datetime.date(2024, 1, 18)
                else:
                    from dateutil.relativedelta import relativedelta
                    
                    final_exp_date = reg_date + relativedelta(years=2)    
            

                # if root_top_cert_details.objects.filter(User_Id=id).exists():
                #     return HttpResponse("Certificate for Root-Top Vendor already exists!!!")
                # else:
                roof_top_obj = roof_top_first.objects.get(id=id)
                if Officer_obj.user_zone == 'CZ':
                    rtcd_obj = root_top_cert_details(User_Id=id, agency_name=roof_top_obj.agency_name, address=roof_top_obj.address,
                                                    registration_no=s, User_type="Roof Top Solar Vendor", current_date=dayy,
                                                    current_time=current_time, valid_upto=final_exp_date, Officer_name=Officer_obj.employ_name, 
                                                    Officer_designation=Officer_obj.designation, User_Zone="CZ", otp=otp)
                    rtcd_obj.save()

                    data = roof_top_first.objects.filter(id=id)
                    doc = roof_top_sec.objects.filter(user_id=data[0].id)
                    data = roof_top_first.objects.filter(id=id)
                    data.update(approver_officer = 1,registration_no = s)

                    rtcd_cert_obj = root_top_cert_details.objects.get(User_Id=id)
                    var_show = "1"
                    return render(request, 'officer/roof_top_cert.html', {"rtcd_cert_obj":rtcd_cert_obj, 'var_show':var_show})



                elif Officer_obj.user_zone == 'WZ':
                    rtcd_obj = root_top_cert_details(User_Id=id, agency_name=roof_top_obj.agency_name, address=roof_top_obj.address,
                                                    registration_no=s, User_type="Roof Top Solar Vendor", current_date=dayy,
                                                    current_time=current_time, valid_upto=final_exp_date, Officer_name=Officer_obj.employ_name, 
                                                    Officer_designation=Officer_obj.designation, User_Zone="WZ", otp=otp)
                    rtcd_obj.save()

                    data = roof_top_first.objects.filter(id=id)
                    doc = roof_top_sec.objects.filter(user_id=data[0].id)
                    data = roof_top_first.objects.filter(id=id)
                    data.update(approver_officer = 1,registration_no = s)

                    rtcd_cert_obj = root_top_cert_details.objects.get(User_Id=id)
                    var_show = "1"
                    return render(request, 'officer/roof_top_cert_wz.html', {"rtcd_cert_obj":rtcd_cert_obj, 'var_show':var_show})

                elif Officer_obj.user_zone == 'EZ':
                    print("eeeeeeeeeeeeeeeee")
                    rtcd_obj = root_top_cert_details(User_Id=id, agency_name=roof_top_obj.agency_name, address=roof_top_obj.address,
                                                    registration_no=s, User_type="Roof Top Solar Vendor", current_date=dayy,
                                                    current_time=current_time, valid_upto=final_exp_date, Officer_name=Officer_obj.employ_name, 
                                                    Officer_designation=Officer_obj.designation, User_Zone="EZ", otp=otp)
                    rtcd_obj.save()

                    data = roof_top_first.objects.filter(id=id)
                    doc = roof_top_sec.objects.filter(user_id=data[0].id)
                    data = roof_top_first.objects.filter(id=id)
                    data.update(approver_officer = 1,registration_no = s)

                    rtcd_cert_obj = root_top_cert_details.objects.get(User_Id=id)
                    var_show = "1"
                    return render(request, 'officer/roof_top_cert_ez.html', {"rtcd_cert_obj":rtcd_cert_obj, 'var_show':var_show})
###################################################################################
                # rtcd_cert_obj = root_top_cert_details.objects.get(User_Id=id)
                # return render(request, 'officer/roof_top_cert.html', {'rtcd_cert_obj':rtcd_cert_obj})

    return render(request, 'roof/roof_top_otp.html')


def root_top_otp3(request, registration_no):
    if request.method == "POST":
        filename = request.FILES['certFile']  

        cert_det_obj = root_top_cert_details.objects.get(registration_no=registration_no)
        cert_det_obj.image = filename
        cert_det_obj.save()

        
        rtf_obj = roof_top_first.objects.get(id=cert_det_obj.User_Id)
        rtf_obj.imageCert = filename
        rtf_obj.save()

    return redirect('/roof_toop_approver_complete_list')


def roof_top_cert_show(request, no):
    print("nooooooooooooooooooooooooooooonnnnnnnnnnnnnnnnnnnnooooooooooooooooooooooooooo", no)
    rtcd_cert_obj = root_top_cert_details.objects.get(registration_no=no)
    var_show = ""
    return render(request, 'officer/roof_top_cert.html', {"rtcd_cert_obj":rtcd_cert_obj, 'var_show':var_show})
    
def transaction_history_solar_viewer(request):
    if request.session.has_key('officer'):
        if request.session['user_zone'] == 'CZ':
            payu_count = payment_roof_top.objects.filter(Payu_Status='success')
            return render(request, 'officer/roof_transaction_data_viewer.html', {"posted": payu_count})


        elif request.session['user_zone'] == 'WZ':
            payu_count = payment_roof_top_wz.objects.filter(Payu_Status='success')
            return render(request, 'officer/roof_transaction_data_viewer.html', {"posted": payu_count})

        elif request.session['user_zone'] == 'EZ':
            payu_count = payment_roof_top_ez.objects.filter(Payu_Status='success')
            return render(request, 'officer/roof_transaction_data_viewer.html', {"posted": payu_count})

    return redirect('/')



def transaction_history_solar_Approver(request):
    payu_count = payment_roof_top.objects.filter(Payu_Status='success')
    return render(request, 'officer/roof_transaction_data_approver.html', {"posted": payu_count})
    
    
    
from django.db.models import Q


from datetime import datetime
def all_tkc_field_officer(request):
    search_post = request.GET.get('search')
    c_status = request.GET.get('status')
    
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()
    if search_post =="All" and c_status =="All":
        # all_data = request.POST.get('all')
        data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Authentication_id__isnull=False))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'officer/all_tkc_data.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
    elif search_post =="All" and c_status !="All":
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(Oyt__icontains=c_status))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'officer/all_tkc_data.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
        
    if search_post and c_status !="All":
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(User_zone__icontains=search_post)& Q(Oyt__icontains=c_status))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'officer/all_tkc_data.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
    if search_post and c_status =="All":
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(User_zone__icontains=search_post))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'officer/all_tkc_data.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
    
    if c_status:
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(Oyt__icontains=c_status))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'officer/all_tkc_data.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})

    return render(request, 'officer/all_tkc_data.html', {'today':today})
    

def all_tkc_field_officer_document(request,id):
    data = User_Registration.objects.get(User_Id=id)

    oyt_name = TKC_Payment.objects.get(id = data.Oyt )
    
    doc = TKC_Document.objects.filter(user_id=data.User_Id)
    add_data = UserCompanyDataMain.objects.get(user_id_id=data)
    if BankDetails.objects.filter(user_id=data.ContactNo).exists():
        bank_details = BankDetails.objects.get(user_id=data.ContactNo)
        return render(request, 'officer/all_tkc_field_officer_document.html',{'oyt_name':oyt_name,'data':data,'doc':doc,'add_data':add_data,'bank_details':bank_details})

    else:
        return render(request, 'officer/all_tkc_field_officer_document.html',{'oyt_name':oyt_name,'data':data,'doc':doc,'add_data':add_data})



def all_vendor_field_officer(request):
    search_post = request.GET.get('search')
    if search_post:
        data = User_Registration.objects.filter(Q(User_type='VENDOR',complete_data='1',Complete_Details='1') & Q(CompanyName_E__icontains=search_post))
    else:
        data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',complete_data=1)
    return render(request,'officer/all_vendor_data.html',{'data':data})


def all_vendor_field_officer_document(request,id):
    data = User_Registration.objects.get(User_Id=id)
    doc = Vendor_Document.objects.filter(user_id=data.User_Id)
    fac = Vendor_Factory_Details.objects.filter(user_id=data.User_Id)
    balance = Vendor_BalanceSheet.objects.filter(user_id=data.User_Id)
    material = Vendor_Material_Details.objects.filter(user_id=data.User_Id)   
    add_data = UserCompanyDataMain.objects.get(user_id_id=data)
    if BankDetails.objects.filter(user_id=data.ContactNo).exists():
        bank_details = BankDetails.objects.get(user_id=data.ContactNo)
        return render(request, 'officer/all_vendor_field_officer_document.html',{'data':data,'doc':doc,'add_data':add_data,'bank_details':bank_details,'fac':fac,'balance':balance,'material':material})
    else:
        return render(request, 'officer/all_vendor_field_officer_document.html',{'data':data,'doc':doc,'add_data':add_data,'fac':fac,'balance':balance,'material':material})




def all_nabl_field_officer(request):
    search_post = request.GET.get('search')
    if search_post:
        data = User_Registration.objects.filter(Q(User_type='NABL',complete_data='1',Complete_Details='1') & Q(CompanyName_E__icontains=search_post))
    else:
        data = User_Registration.objects.filter(User_type='NABL',Complete_Details='1',complete_data=1)
    return render(request,'officer/all_nabl_data.html',{'data':data})



def all_nabl_field_officer_document(request,id):
    data = User_Registration.objects.get(User_Id=id)
    doc = NABL_Document.objects.filter(user_id=data.User_Id)
    add_data = UserCompanyDataMain.objects.get(user_id_id=data)
    if BankDetails.objects.filter(user_id=data.ContactNo).exists():
        bank_details = BankDetails.objects.get(user_id=data.ContactNo)
        return render(request, 'officer/all_nabl_field_officer_document.html',{'data':data,'doc':doc,'add_data':add_data,'bank_details':bank_details})
    else:
        return render(request, 'officer/all_nabl_field_officer_document.html',{'data':data,'doc':doc,'add_data':add_data}) 

def demo_test(request):
    mm_obj = Material_Master.objects.all()
    dict_mat = {}
    lst = []
    for i in mm_obj:
        dict_mat['Material_Id'] = i.Material_Id
        dict_mat['Material_Name'] = i.Material_Name
        dict_mat['Material_Type'] = i.Material_Type
        dict_mat['Is_Active'] = i.Is_Active
        dict_mat['++++++++'] = "-----------"
        lst.append(dict_mat)
    print(" :::::::::::::::::::::::::::::::::::::::lst::::::::::::::::::::::::::::::::::::::::::::: ", lst)
    return HttpResponse(lst)


def discom(request):
    if request.session.has_key('employ_login_id'):
        type_data = OwnerShip_Type_Table_Master.objects.all()
        return render(request, 'main/tkc.html',{'type_data':type_data})
    return redirect('/')


def discom_reg1(request):
    if request.session.has_key('employ_login_id'):
        type_data = OwnerShip_Type_Table_Master.objects.all()
        if request.method == 'POST':
            mobile = request.POST.get('mobile')
            data = User_Registration.objects.filter(ContactNo=mobile)
            User_type = request.POST.get('user')
            service_type = request.POST.get('service_type')
            company_name_e = request.POST.get('company_name_e')
            user_type_rec = request.POST.get('user_6')
            name_of_authorized_e = request.POST.get('name_of_authorized_e')
            aadhar = request.POST.get('aadhar')
            email = request.POST.get('email')
            zone = request.POST.get('zone')
            add1 = request.POST.get('add1')
            add2 = request.POST.get('add2')
            add3 = request.POST.get('add3')
            add4 = request.POST.get('add4')
            Company_Fax = request.POST.get('fax')
            Company_Pan_No = request.POST.get('pan')
            Company_Gumastha_No = request.POST.get('reg_no')
            Company_Gst_No = request.POST.get('gst')
            reg_date = request.POST.get('reg_date')
            Company_Address_1 = request.POST.get("add1")
            Company_Address_2 = request.POST.get("add2")
            p_code = request.POST.get("zip")
            state = request.POST.get("add4")
            district = request.POST.get("add3")
            City = request.POST.get("city")
            Office_Address_1 = request.POST.get("add5")
            Office_Address_2 = request.POST.get("add6")
            p_code_2 = request.POST.get("zip2")
            state_2 = request.POST.get("add7")
            district_2 = request.POST.get("add8")
            City_2 = request.POST.get("city2")
            reg_date = date.today()
         

            if Rca_User_Registration.objects.filter(Company_Gst_No=Company_Gst_No,User_zone=zone).exists():
                abc = Rca_User_Registration.objects.filter(Company_Gst_No=Company_Gst_No)
                messages.warning(request, "GST number already exists for ")
                return render(request, 'main/tkc.html',{'data': data,'abc':abc[0]})
            elif Rca_User_Registration.objects.filter(Company_Pan_No=Company_Pan_No,User_zone=zone).exists():
                abc = Rca_User_Registration.objects.filter(Company_Pan_No=Company_Pan_No)
                messages.warning(request, "PAN  number already exists for")
                return render(request, 'main/tkc.html',{'data': data[0],'abc':abc[0]})

            elif Rca_User_Registration.objects.filter(ContactNo=mobile,User_zone=zone).exists():
                messages.warning(request, "Mobile Number already registered")
                return render(request, 'main/tkc.html')
            elif Rca_User_Registration.objects.filter(Email_Id=email,User_zone=zone).exists():
                messages.warning(request, "Email ID already registered")
                return render(request, 'main/tkc.html')    
            else:
                try:
                    user_details = Rca_User_Registration(User_type=User_type, Type_of_business=service_type,
                                                    CompanyName_E=company_name_e, User_zone=zone,
                                                    Authorised_person_E=name_of_authorized_e, ContactNo=mobile,Aadhar=aadhar,
                                                    Email_Id=email,Basic_Details=1,User_code=user_type_rec,Company_Fax=Company_Fax, Company_Pan_No=Company_Pan_No,
                                                Company_Gumastha_No=Company_Gumastha_No, Company_Gst_No=Company_Gst_No,
                                                Registration_Date=reg_date, Company_add_1=Company_Address_1,
                                                Company_add_2=Company_Address_2, Company_pin_code=p_code, Company_state=state,
                                                Company_dist=district, Company_city=City, Company_t_add_1=Office_Address_1,
                                                Company_t_add_2=Office_Address_2, Company_t_pin_code=p_code_2,
                                                Company_t_state=state_2, Company_t_dist=district_2, Company_t_city=City_2)

                    user_details.save()

                except Exception as e:
                    user_details = Rca_User_Registration(User_type=User_type, Type_of_business=service_type,
                                                    CompanyName_E=company_name_e, User_zone=zone,
                                                    Authorised_person_E=name_of_authorized_e, ContactNo=mobile,
                                                    Email_Id=email,Basic_Details=1,User_code=user_type_rec,Company_Fax=Company_Fax, Company_Pan_No=Company_Pan_No,
                                                Company_Gumastha_No=Company_Gumastha_No, Company_Gst_No=Company_Gst_No,
                                                Registration_Date=reg_date, Company_add_1=Company_Address_1,
                                                Company_add_2=Company_Address_2, Company_pin_code=p_code, Company_state=state,
                                                Company_dist=district, Company_city=City, Company_t_add_1=Office_Address_1,
                                                Company_t_add_2=Office_Address_2, Company_t_pin_code=p_code_2,
                                                Company_t_state=state_2, Company_t_dist=district_2, Company_t_city=City_2)

                    user_details.save()

                
                



             
          
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007022255202070533&mobile_number=" + str(
                    mobile) + "&v1=" + str(company_name_e) + "&v2=" + str() + "&v3=" + "MP" + str(zone) + "&v4=" + str(mobile) + "&v5=" + str(
                    'https://qcportal.mpcz.in/')
                response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1007022255202070533',date = datetime.now(),mobile_number = mobile)
                sms_template.save()

                return redirect('discom')

        return render(request,'main/tkc.html',{'type_data':type_data})
                  
    return redirect('/')



def roof_top_discom(request):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            agency_name = request.POST.get('one')
            auth_p = request.POST.get('two')
            contact = request.POST.get('three')
            email = request.POST.get('four')
            pan = request.POST.get('five')
            gst = request.POST.get('six')
            address = request.POST.get('newone')
            print("gggggggggg",address)
            
            if roof_top_first.objects.filter(pan_card=pan).exists():            
                messages.warning(request, "Pan Card number already exists ")
                return render(request, 'roof/agent_first.html')
            elif roof_top_first.objects.filter(contact=contact).exists():
                messages.warning(request, "Mobile  number already exists ")
                return render(request, 'roof/agent_first.html')

            else:
                save_data = roof_top_first(agency_name=agency_name,address=address,name_of_auth=auth_p,pan_card=pan,contact=contact,email=email,created_by='discom')
                save_data.save()
                id_id = roof_top_first.objects.filter(contact=contact)

                request.session['id_id'] = id_id[0].id
                return redirect('roof_top_upload_discom')
        return render(request,'main/agent.html')

    return redirect('/')



def roof_top_upload_discom(request):
    if request.session.has_key('employ_login_id'):
        
        if request.method == 'POST':
            data = roof_top_first.objects.get(id=request.session['id_id'])
            user_id = data.id
            reg_number = request.POST.get('one')
            v_upload_file_factory2 = request.FILES['two']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='Company Registration No.', Document_Number=reg_number,Ddocfile=v_upload_file_factory2,Status=1)
            data1.save()

         
            number = request.POST.get('three')
            v_upload_file_factory3 = request.FILES['four']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='GST Certificate with  Challan',
                                    Document_Number=number, Status=1,Ddocfile=v_upload_file_factory3)
            data1.save()

            reg_number = request.POST.get('five')
            upload = request.FILES['six']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='Pan Card Details',
                                    Document_Number=reg_number, Ddocfile=upload, Status=1)
            data1.save()



            number = request.POST.get('seven')
            upload = request.FILES['eight']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='A/B class Electrical License Undertaking',
                                    Document_Number=number, Ddocfile=upload, Status=1)
            data1.save()


            
            gst_card_no = request.POST.get('nine')
            document = request.FILES['ten']

            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='Aadhar Card Details',
                                Document_Number=gst_card_no, Ddocfile=document,Status=1)
            data1.save()

            gst_card_no = request.POST.get('eleven')
            document = request.FILES['twelve']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='MSME Registration for Solar System',Document_Number=gst_card_no,
                                Ddocfile=document,Status=1)
            data1.save()


            data = roof_top_first.objects.filter(id=request.session['id_id'])
            data.update(profile_complete=1)
            return render(request,'officer/discom_base.html')
        return render(request, 'main/Agent2.html')

    return redirect('/')




def roof_top_filling_pending_list(request):
    if request.session.has_key('employ_login_id'):
        abc = roof_top_first.objects.filter(profile_complete=0)
        return render(request,'main/roof_top_form_pending_list.html',{'data':abc})
    return redirect('/')



def roof_top_filling_pending_form(request,id):
    request.session['id_id'] = id
    if request.session.has_key('employ_login_id'):
        if roof_top_first.objects.filter(id=id,profile_complete=0).exists():
            return redirect('/roof_top_upload_discom')
    return redirect('/')
    

def discom_approved_vendor(request):
    if request.session.has_key('employ_login_id'):
        if request.session['officer'] == 'WZ':
            abc = Rca_User_Registration.objects.filter(User_zone='WZ')
            return render(request, 'officer/discom_approved_vendor.html', {'data': abc})

        elif request.session['officer'] == 'CZ':
            abc = Rca_User_Registration.objects.filter(User_zone='CZ')
            return render(request, 'officer/discom_approved_vendor.html', {'data': abc})

        elif request.session['officer'] == 'EZ':
            abc = Rca_User_Registration.objects.filter(User_zone='EZ')
            return render(request, 'officer/discom_approved_vendor.html', {'data': abc})
   
    return redirect('/')    
    
    
    
def roof_toop_officer_loa(request):
    if request.session.has_key('officer'):
        if request.session['user_zone'] == 'CZ':
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,approver_officer=1,loa=0,user_type='Empanelled for solar subsidy',user_zone='CZ')
        
        elif request.session['user_zone'] == 'EZ':

            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,approver_officer=1,loa=0,user_type='Empanelled for solar subsidy',user_zone='EZ')

        else:
            data = roof_top_first.objects.filter(profile_complete=1,viewer_officer=1,approver_officer=1,loa=0,user_type='Empanelled for solar subsidy',user_zone='WZ')

        if request.method == 'POST':
            user_name = request.POST.get("user_name")
            loa = request.FILES['file']
            annexure = request.FILES['file2']
            vendor_document = request.FILES['file3']
            abc = roof_top_first.objects.get(agency_name=user_name)
            loa_date = date.today()
            abc.loa = 1
            abc.save()
            user_id_abc = abc.id
            if request.session['user_zone'] == 'CZ':
                save_data = roof_top_loa(user_id=user_id_abc,user_name=user_name,loa_file=loa,annexure=annexure,vendor_document=vendor_document,Doc_issue_date=loa_date)
                save_data.save()

            elif request.session['user_zone'] == 'EZ':
                save_data = roof_top_loa_ez(user_id=user_id_abc,user_name=user_name,loa_file=loa,annexure=annexure,vendor_document=vendor_document,Doc_issue_date=loa_date)
                save_data.save()
            elif request.session['user_zone'] == 'WZ':
                save_data = roof_top_loa_wz(user_id=user_id_abc,user_name=user_name,loa_file=loa,annexure=annexure,vendor_document=vendor_document,Doc_issue_date=loa_date)
                save_data.save()

            request.session['user_id_abc'] = user_id_abc
            return redirect ('uploaded_loa')
        return render(request, 'officer/upload_loa_solar.html', {'data': data})

    return redirect('/')


def uploaded_loa(request):
    if request.session.has_key('user_id_abc'):  
        abc = roof_top_loa.objects.filter(user_id = request.session['user_id_abc'])
        abc.update(viewer = 1 )
        return render(request, 'officer/uploded_load_success.html')
    return render(request, 'officer/upload_loa_solar.html')

def all_loa_viewer_view(request):
    if request.session.has_key('officer'):
        if request.session['user_zone'] == 'WZ':
            data = roof_top_loa_wz.objects.all().order_by('user_name')
            return render(request, 'officer/upload_loa_solar_view.html',{'data':data})

        elif request.session['user_zone'] == 'EZ':
            data = roof_top_loa_ez.objects.all().order_by('user_name')
            return render(request, 'officer/upload_loa_solar_view.html',{'data':data})

        if request.session['user_zone'] == 'CZ':
            data = roof_top_loa.objects.all().order_by('user_name')
            return render(request, 'officer/upload_loa_solar_view.html',{'data':data})

    return redirect('/')


def all_pending_loa_for_approvel(request):
    data = roof_top_loa.objects.filter(viewer=1,approver=0)

    return render(request, 'officer/all_pending_loa_for_approvel.html',{'data':data})



def all_pending_loa_for_approvel(request):
    data = roof_top_loa.objects.filter(viewer=1,approver=0)

    return render(request, 'officer/all_pending_loa_for_approvel.html',{'data':data})


def all_pending_loa_for_approvel_evaluate(request,id):
    doc = roof_top_loa.objects.filter(user_id = id)
    doc_id=doc[0].user_id
    data = roof_top_first.objects.filter(id=doc[0].user_id)
    return render(request, 'officer/all_pending_loa_for_approvel_evaluate.html',{'data':data[0],'abc':doc,'doc_id':doc_id})


def all_pending_loa_for_approvel_evaluate_save(request,id):
    doc = roof_top_loa.objects.get(user_id = id)
    
    if request.method == 'POST':
        result=request.GET.get('a')
        print('----------',result)
        print('-----------------hello')
        result =request.POST.get('a')
        print('result',result)
        if result == 'OK':
            
            doc.approver = 1
            doc.remark = request.POST.get("remark")
            doc.signed_loa_file = request.FILES['four']
            doc.save()
            data = roof_top_first.objects.filter(agency_name=doc.user_name)
            #email = data[0].email
            # send_mail(
                # 'LOA Alloted',
                # 'Hello ! You Have assined LOA, kindly login on qcportal',
                # settings.EMAIL_HOST_USER,
                # [email],
                # fail_silently=False,
            # )

            return render(request, 'officer/approved_load_success.html')
    
        elif result == 'NOT':
            doc.approver = 2 
            print("jjjjjjjjjjjjjjj",request.POST.get("remark"))
            doc.remark = request.POST.get("remark")
            doc.save()
            return render(request, 'officer/rejected_loa.html')
        return redirect('/all_pending_loa_for_approvel')
            


    return render(request, 'officer/all_pending_loa_for_approvel_evaluate.html',{'abc':doc})


    



from django.http import FileResponse


def check_loa_otp(request, id, otp):
    otp_check = request.session['otp']
    if request.method == 'POST':
        if otp_check == request.POST.get("officer_otp"):
            doc = roof_top_loa.objects.filter(user_id = id)
            loa = str(doc[0].loa_file)
            # fname = loa #3
            path = os.path.join(settings.MEDIA_ROOT, '' + loa)#4
            response = FileResponse(open(path, 'rb'), content_type="application/pdf")
            response["Content-Disposition"] = "filename={}".format(loa)
            return response


def all_approved_loa_approvel_officer(request):
    data = roof_top_loa.objects.filter(viewer=1).order_by('user_name')
    return render(request, 'officer/all_approved_loa_approvel_officer.html',{'data':data})    
    
    
def loa_resubmit(request,id):
    if request.method == 'POST':
        newloaf = request.FILES['newloafile']
        # main_file =  'roofTopCertificate/' + request.FILES['newloafile']._get_name()
        data = roof_top_loa.objects.get(user_id=id,approver=2)
        data.loa_file = newloaf
        data.approver = 0
        data.save()
        return render(request, 'officer/uploded_load_success.html')
    else:
        return render(request, 'officer/uploded_load_success.html')    
        
        
def non_loa_vendors(request):
    if request.session.has_key('officer'):
        if request.session['user_zone'] == 'WZ':
            data = data = roof_top_first.objects.filter(user_zone='WZ',profile_complete=1,viewer_officer=1,approver_officer=1,user_type='Non Empanelled for solar subsidy')
            return render(request, 'officer/non_loa_vendors.html',{'data':data})   

        elif request.session['user_zone'] == 'EZ':
            data = data = roof_top_first.objects.filter(user_zone='EZ',profile_complete=1,viewer_officer=1,approver_officer=1,user_type='Non Empanelled for solar subsidy')
            return render(request, 'officer/non_loa_vendors.html',{'data':data})   


        elif request.session['user_zone'] == 'CZ':
            data = data = roof_top_first.objects.filter(user_zone='CZ',profile_complete=1,viewer_officer=1,approver_officer=1,user_type='Non Empanelled for solar subsidy')
            return render(request, 'officer/non_loa_vendors.html',{'data':data})   


    return redirect('/')
 


def solar_vendor_bg(request,id):
    doc = roof_top_loa.objects.filter(user_id=id)
    doc_id=doc[0].user_id
    name = doc[0].user_name
    data = roof_top_first.objects.filter(id=doc[0].user_id)
    if request.method == "POST":
        bg_name = request.POST.get('bgbank')
        ifsc = request.POST.get('ifsc')
        bg_no = request.POST.get('bg_no')
        bg_issu_date = request.POST.get('bg_issu_date')
        bg_valid_upto = request.POST.get('bg_valid_upto')
        amount = request.POST.get('amount')
        ac_number = request.POST.get('ac_number')
        bg_image = request.FILES['bg_image']
        bg_gu_file = request.FILES['bg_gu_file']

        bg_data = solar_sd(user_id=doc_id,agency_name=name,bg_name=bg_name,bg_no=bg_no,ifsc=ifsc,issue_date=bg_issu_date,valid_date=bg_valid_upto,amount=amount,account_number=ac_number,bg_document=bg_image,bank_order=bg_gu_file)
        bg_data.save()
        doc.update(bg_status=1)

        return redirect('all_loa_viewer_view')

    return render(request, 'officer/solar_vendor_bg.html',{'data':doc,'first':data,'id':doc_id})


def bg_expiry_status(request):
    data = solar_sd.objects.all()
    return render(request, 'officer/solar_vendor_bg_expiry_details.html',{'data':data})


def bg_expiry_status_approver(request):
    data = solar_sd.objects.all()
    return render(request, 'officer/bg_expiry_status_approver.html',{'data':data})


def tkc_cert_gen(request):
    return render(request, 'officer/tkc_cert_gen.html')

def tkc_cert_gen2(request):
    print("tkc_cert_gen2tkc_cert_gen2tkc_cert_gen2")
    usr_obj = User_Registration.objects.filter(digital_cert_upload = 0,cgm_approval = 1, User_type="TKC", User_zone="CZ")
    return render(request, 'officer/tkc_cert_gen2.html', {'usr_obj':usr_obj})

def tkc_cert_gen3(request, User_Id):
    if request.method == "POST":
        if request.FILES['tkc_cert']:
            filename = request.FILES['tkc_cert']  
            usr_obj = User_Registration.objects.get(User_Id=User_Id)
            UCDM_obj = UserCompanyDataMain.objects.get(user_id_id=usr_obj)

            ###############################################################
            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            current_time = td.strftime("%H:%M:%S")

            
            today = date.today().isoformat()
            
            var_oyt = ""
            if usr_obj.Oyt == '9':
                var_oyt = "TKC"
            elif usr_obj.Oyt == '8':
                var_oyt = "A5"
            elif usr_obj.Oyt == '7':
                var_oyt = "A4"
            elif usr_obj.Oyt == '6':
                var_oyt = "A3"
            elif usr_obj.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif usr_obj.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif usr_obj.Oyt == '1':
                var_oyt = "B"

            exp = TKC_Document.objects.get(user_id=usr_obj.User_Id, Types_of_Docs='Electrical License')
            expi_date = exp.Doc_expiry_date

            cert_obj = certificate_details(User_Id=User_Id,company_name=usr_obj.CompanyName_E,
                Company_add_1=UCDM_obj.Company_add_1, Company_add_2=UCDM_obj.Company_add_2,
                Company_dist=UCDM_obj.Company_dist,Company_state=UCDM_obj.Company_state,
                Company_pin_code=UCDM_obj.Company_pin_code, no=usr_obj.Authentication_id,
                User_type=usr_obj.User_type, vmaterial="",
                day=today, valid_upto="expi_date", employ_name="Anubandh Portal", designation="GM_Works",
                current_time=current_time,tkc_class_contractor=var_oyt, electic_liecense_date=expi_date,
                User_Zone="",nabl_cert_exp="",nabl_cert_number="",image=filename)
            cert_obj.save()
            ###############################################################

            usr_obj.digital_cert_upload=1
            usr_obj.cert_image = filename
            usr_obj.save()
        usr_obj = User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type="TKC")
        return render(request, 'officer/tkc_cert_gen2.html', {'usr_obj':usr_obj})
    else:
        usr_obj = User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type="TKC")
        return render(request, 'officer/tkc_cert_gen2.html', {'usr_obj':usr_obj})    

def all_vendor_dicome_document(request,id):
    data = Rca_User_Registration.objects.get(User_Id=id)
    doc = Rca_Vendor_Document.objects.filter(user_id=data.User_Id)

    if Rca_Vendor_Document.objects.filter(user_id=data.User_Id).exists():
        doc = Rca_Vendor_Document.objects.filter(user_id=data.User_Id)
        return render(request, 'officer/all_vendor_dicome_document.html',{'data':data,'doc':doc})
    else:
        return render(request, 'officer/all_vendor_dicome_document.html',{'data':data})
        
        
        
        
#***********************RCA CGM******************************************************
def rca_pending_cgm(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            rca_pending = Rca_User_Registration.objects.filter(payment=1,cgm_approval=0,factory_approval=1,factory_approval_status=1,User_zone='WZ').order_by('User_Id')
            return render(request, 'officer/rca_pending_cgm.html', {"data": rca_pending})

        elif request.session['officer'] == 'CZ':
            rca_pending = Rca_User_Registration.objects.filter(payment=1,cgm_approval=0,factory_approval=1,factory_approval_status=1,User_zone='CZ').order_by('User_Id')
            return render(request, 'officer/rca_pending_cgm.html', {"data": rca_pending})

        elif request.session['officer'] == 'EZ':
            rca_pending = Rca_User_Registration.objects.filter(payment=1,cgm_approval=0,factory_approval=1,factory_approval_status=1,User_zone='EZ').order_by('User_Id')
            return render(request, 'officer/rca_pending_cgm.html', {"data": rca_pending})
            
    return redirect('/')

# def rca_cgm_evaluate(request, id):
    # data = Rca_User_Registration.objects.filter(User_Id=id)
    # doc = Rca_Vendor_Document.objects.filter(user_id=data[0].User_Id)
    # return render(request, 'officer/rca_cgm_evaluate.html',{'abc':doc,'data':data[0]})



def rca_cgm_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = Rca_User_Registration.objects.filter(User_Id=id)
            doc = Rca_Vendor_Document.objects.filter(user_id=data[0].User_Id)
            usr_obj = Rca_User_Registration.objects.get(User_Id=id)
            comm = request.POST.get(str('remark'))
            doc.CGM_remark = comm
            result = request.POST.get(str('action'))
            data = Rca_User_Registration.objects.get(User_Id=id)
            data.cgm_approval = 1
            data.save()
            # send_mail(
            #     'Approval status of C.G.M ',
            #     'Hello ! Your application is approved by C.G.M',
            #     settings.EMAIL_HOST_USER,
            #     [data.Email_Id],
            #     fail_silently=False,
            # )
            from datetime import date
            User_Zone = usr_obj.User_zone
            User = usr_obj.User_type
            vendor_type = "00"
            nabl_type = "00"
            tkc_type = "00"
            today = date.today()
            date = today.strftime("%m%y")
            list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            s = ""
            if User_Zone == "CZ":
                s = "CZ"
                if User == "VENDOR":
                    s = s + "R" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            if User_Zone == "EZ":
                s = "EZ"
                if User == "VENDOR":
                    s = s + "R" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            if User_Zone == "WZ":
                s = "WZ"
                if User == "VENDOR":
                    s = s + "R" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            data = Rca_User_Registration.objects.filter(User_Id=id)
            company_name = data[0].CompanyName_E
            issue_date = today.strftime("%d/%m/%Y")
            valid_upto = datetime(2024, 1, 11)
            valid_upto = valid_upto.strftime("%d/%m/%Y")
            data11 = Rca_User_Registration.objects.filter(User_Id=id)
            data11.update(Authentication_id=s)
            data11 = Rca_User_Registration.objects.get(User_Id=id)

            sms = Rca_User_Registration.objects.get(User_Id=id)
            mobile = sms.ContactNo
            name_sms = sms.CompanyName_E
            zone = sms.User_zone
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8000"}
            # for server set proxy
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277221739526680&mobile_number=" + str(
                mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('VENDOR') + "&v4=" + "MP" + str(zone) + "&v5=" + str(
                'https://qcportal.mpcz.in/')
            response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1007277221739526680',date = datetime.datetime.now(),mobile_number = mobile)
            sms_template.save()

            # send_mail(
            #     'Approval status of CGM (QC) ',
            #     'Your application is finally approved by CGM(QC) and your registration number is ' + s,
            #     settings.EMAIL_HOST_USER,
            #     [data11.Email_Id],
            #     fail_silently=False,
            # )
            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            officer_mobile = officer.mobile
            print("gggggggggggggggg",officer_mobile)
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otptt = generateOTP()
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
            sms_template.save()

            request.session['otptt'] = otptt
            request.session['officer_mobile'] = officer_mobile

            otp_ofcr = Rca_User_Registration.objects.filter(User_Id=id)
            otp_ofcr.update(Otp=otptt)

            usr_obj = Rca_User_Registration.objects.get(User_Id=id)
            otp = usr_obj.Otp

            return render(request, 'main/offcier_otp_rca.html', {'id': id, 'otp': otp})
                # return render(request, 'vendor/cert2.html', {'td':td,'vmaterial':vmaterial,'data': data[0], 'company_name': company_name, 'no': s, 'd1': valid_upto, 'd2': issue_date})

            
    return redirect('/')






# def uplaod_cert(request, no):
    # usr_obj1 = Rca_User_Registration.objects.get(Authentication_id=no)
    # if request.method == "POST":
        # if request.FILES['digitalCert']:
            # filename = request.FILES['digitalCert']  
            # cert_det_obj = certificate_details_cra.objects.get(no=no)
            # usr_obj = Rca_User_Registration.objects.get(Authentication_id=no)
            # cert_det_obj.image = filename
            # cert_det_obj.save()
            # usr_obj.digital_cert_upload=1
            # usr_obj.cert = filename
            # usr_obj.save()
        # return render(request, 'officer/certificate_submit.html', {'User_type':usr_obj1.User_type})
    # else:
        # return render(request, 'officer/certificate_submit.html', {'User_type':usr_obj1.User_type})



# ************8888regular_rca


# def rca_pending_cgm(request):
    # if request.session.has_key('officer'):
        # rca_pending = Rca_User_Registration.objects.filter(payment=1,cgm_approval=0,provision_fi=0)
        # return render(request, 'officer/rca_pending_cgm.html', {"data": rca_pending})
    # return redirect('/')


def rca_pending_cgm_regular(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            rca_pending = Rca_User_Registration.objects.filter(cgm_approval=0,provision_fi=1,User_zone='WZ').order_by('User_Id')
            return render(request, 'officer/rca_pending_cgm_regular.html', {"data": rca_pending})

        elif request.session['officer'] == 'CZ':
            rca_pending = Rca_User_Registration.objects.filter(cgm_approval=0,provision_fi=1,User_zone='CZ').order_by('User_Id')
            return render(request, 'officer/rca_pending_cgm_regular.html', {"data": rca_pending})

        elif request.session['officer'] == 'EZ':
            rca_pending = Rca_User_Registration.objects.filter(cgm_approval=0,provision_fi=1,User_zone='EZ').order_by('User_Id')
            return render(request, 'officer/rca_pending_cgm_regular.html', {"data": rca_pending})
            
    return redirect('/')


from django.db.models import Q
def cgm_complete_vendor_rca(request):
    print("gggggg",request.session['officer'])
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = Rca_User_Registration.objects.filter(Q(cgm_approval=1,User_zone='WZ',User_code='RCA(New)')|Q(cgm_approval=1,User_zone='WZ',User_code='RCA NEW'))
            return render(request, 'officer/cgm_complete_vendor_rca.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = Rca_User_Registration.objects.filter(Q(cgm_approval=1,User_zone='CZ',User_code='RCA(New)')|Q(cgm_approval=1,User_zone='CZ',User_code='RCA NEW'))
            return render(request, 'officer/cgm_complete_vendor_rca.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = Rca_User_Registration.objects.filter(Q(cgm_approval=1,User_zone='EZ',User_code='RCA(New)')|Q(cgm_approval=1,User_zone='EZ',User_code='RCA NEW'))
            return render(request, 'officer/cgm_complete_vendor_rca.html',{'data': data})

    return redirect('/')


def cgm_complete_vendor_rca_regular(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = Rca_User_Registration.objects.filter(Q(cgm_approval=1,User_zone='WZ',User_code='RCA(Regular)')|Q(cgm_approval=1,User_zone='WZ',User_code='RCA REGULAR'))
            return render(request, 'officer/cgm_complete_vendor_rca_regular.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = Rca_User_Registration.objects.filter(Q(cgm_approval=1,User_zone='CZ',User_code='RCA(Regular)')|Q(cgm_approval=1,User_zone='CZ',User_code='RCA REGULAR'))
            return render(request, 'officer/cgm_complete_vendor_rca_regular.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            print("tttttttttt")
            data = Rca_User_Registration.objects.filter(Q(cgm_approval=1,User_zone='EZ',User_code='RCA(Regular)')|Q(cgm_approval=1,User_zone='EZ',User_code='RCA REGULAR'))
            return render(request, 'officer/cgm_complete_vendor_rca_regular.html',{'data': data})

    return redirect('/')





def rca_cgm_evaluate(request, id):
    data = Rca_User_Registration.objects.filter(User_Id=id)
    data1 = Rca_User_Registration.objects.get(User_Id=id)
    doc = Rca_Vendor_Document.objects.filter(user_id=data[0].User_Id)
    image = RCA_Vendor_Factory_image.objects.filter(Vendor=data1)
    print("ffffff",data)
    return render(request, 'officer/rca_cgm_evaluate.html',{'abc':doc,'data':data[0],'image':image})


def rca_cgm_evaluate_regular(request, id):
    data = Rca_User_Registration.objects.filter(User_Id=id)
    doc = Rca_Vendor_Document.objects.filter(user_id=data[0].User_Id)
    return render(request, 'officer/rca_cgm_evaluate_regular.html',{'abc':doc,'data':data[0]})    



def rca_cgm_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = Rca_User_Registration.objects.filter(User_Id=id)
            doc = Rca_Vendor_Document.objects.filter(user_id=data[0].User_Id)
            usr_obj = Rca_User_Registration.objects.get(User_Id=id)
            comm = request.POST.get(str('remark'))
            doc.CGM_remark = comm
            result = request.POST.get(str('action'))
            data = Rca_User_Registration.objects.get(User_Id=id)
            data.cgm_approval = 1
            data.save()
            # send_mail(
            #     'Approval status of C.G.M ',
            #     'Hello ! Your application is approved by C.G.M',
            #     settings.EMAIL_HOST_USER,
            #     [data.Email_Id],
            #     fail_silently=False,
            # )
            from datetime import date
            User_Zone = usr_obj.User_zone
            User = usr_obj.User_type
            vendor_type = "00"
            nabl_type = "00"
            tkc_type = "00"
            today = date.today()
            date = today.strftime("%m%y")
            list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            s = ""
            if User_Zone == "CZ":
                s = "CZ"
                if User == "VENDOR":
                    s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            if User_Zone == "EZ":
                s = "EZ"
                if User == "VENDOR":
                    s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            if User_Zone == "WZ":
                s = "WZ"
                if User == "VENDOR":
                    s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            data = Rca_User_Registration.objects.filter(User_Id=id)
            company_name = data[0].CompanyName_E
            issue_date = today.strftime("%d/%m/%Y")
            from datetime import datetime
            valid_upto = datetime(2024, 1, 11)
            valid_upto = valid_upto.strftime("%d/%m/%Y")
            data11 = Rca_User_Registration.objects.filter(User_Id=id)
            data11.update(Authentication_id=s)
            data11 = Rca_User_Registration.objects.get(User_Id=id)

            sms = Rca_User_Registration.objects.get(User_Id=id)
            mobile = sms.ContactNo
            name_sms = sms.CompanyName_E
            zone = sms.User_zone
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8000"}
            # for server set proxy
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277221739526680&mobile_number=" + str(
                mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('VENDOR') + "&v4=" + "MP" + str(zone)  + "&v5=" + str(
                'https://qcportal.mpcz.in/')
            response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1007277221739526680',date = datetime.now(),mobile_number = mobile)
            sms_template.save()


            # send_mail(
            #     'Approval status of CGM (QC) ',
            #     'Your application is finally approved by CGM(QC) and your registration number is ' + s,
            #     settings.EMAIL_HOST_USER,
            #     [data11.Email_Id],
            #     fail_silently=False,cert_upload_download_rca
            # )
            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            officer_mobile = officer.mobile
            print("gggggggggggggggg",officer_mobile)
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otptt = generateOTP()
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
            sms_template.save()

            request.session['otptt'] = otptt
            request.session['officer_mobile'] = officer_mobile

            otp_ofcr = Rca_User_Registration.objects.filter(User_Id=id)
            otp_ofcr.update(Otp=otptt)
            cert_upload_download_rca
            usr_obj = Rca_User_Registration.objects.get(User_Id=id)
            otp = usr_obj.Otp

            return render(request, 'main/offcier_otp_rca.html', {'id': id, 'otp': otp})
                # return render(request, 'vendor/cert2.html', {'td':td,'vmaterial':vmaterial,'data': data[0], 'company_name': company_name, 'no': s, 'd1': valid_upto, 'd2': issue_date})

            
    return redirect('/')




def rca_regular_cgm_evaluate_save(request, id):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            data = Rca_User_Registration.objects.filter(User_Id=id)
            doc = Rca_Vendor_Document.objects.filter(user_id=data[0].User_Id)
            usr_obj = Rca_User_Registration.objects.get(User_Id=id)
            comm = request.POST.get(str('remark'))
            doc.CGM_remark = comm
            result = request.POST.get(str('action'))
            data = Rca_User_Registration.objects.get(User_Id=id)
            data.cgm_approval = 1
            data.save()
            # send_mail(
            #     'Approval status of C.G.M ',
            #     'Hello ! Your application is approved by C.G.M',
            #     settings.EMAIL_HOST_USER,
            #     [data.Email_Id],
            #     fail_silently=False,
            # )
            from datetime import date
            User_Zone = usr_obj.User_zone
            User = usr_obj.User_type
            vendor_type = "00"
            nabl_type = "00"
            tkc_type = "00"
            today = date.today()
            date = today.strftime("%m%y")
            list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            s = ""
            if User_Zone == "CZ":
                s = "CZ"
                if User == "VENDOR":
                    s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            if User_Zone == "EZ":
                s = "EZ"
                if User == "VENDOR":
                    s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            if User_Zone == "WZ":
                s = "WZ"
                if User == "VENDOR":
                    s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "NABL":
                    s = s + "N" + nabl_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)
                elif User == "TKC":
                    s = s + "T" + tkc_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                        list1) + random.choice(list1)

            data = Rca_User_Registration.objects.filter(User_Id=id)
            company_name = data[0].CompanyName_E
            issue_date = today.strftime("%d/%m/%Y")
            valid_upto = datetime(2024, 1, 11)
            valid_upto = valid_upto.strftime("%d/%m/%Y")
            data11 = Rca_User_Registration.objects.filter(User_Id=id)
            data11.update(Authentication_id=s)
            data11 = Rca_User_Registration.objects.get(User_Id=id)

            sms = Rca_User_Registration.objects.get(User_Id=id)
            mobile = sms.ContactNo
            name_sms = sms.CompanyName_E
            zone = sms.User_zone
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8000"}
            # for server set proxy
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277221739526680&mobile_number=" + str(
                mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('VENDOR') + "&v4=" + "MP" + str(zone)  + "&v5=" + str(
                'https://qcportal.mpcz.in/')
            response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1007277221739526680',date = datetime.datetime.now(),mobile_number = mobile)
            sms_template.save()

            # send_mail(
            #     'Approval status of CGM (QC) ',
            #     'Your application is finally approved by CGM(QC) and your registration number is ' + s,
            #     settings.EMAIL_HOST_USER,
            #     [data11.Email_Id],
            #     fail_silently=False,
            # )
            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            officer_mobile = officer.mobile
            print("gggggggggggggggg",officer_mobile)
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otptt = generateOTP()
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
            sms_template.save()

            request.session['otptt'] = otptt
            request.session['officer_mobile'] = officer_mobile

            otp_ofcr = Rca_User_Registration.objects.filter(User_Id=id)
            otp_ofcr.update(Otp=otptt)

            usr_obj = Rca_User_Registration.objects.get(User_Id=id)
            otp = usr_obj.Otp

            return render(request, 'main/offcier_otp_rca_regular.html', {'id': id, 'otp': otp})
                # return render(request, 'vendor/cert2.html', {'td':td,'vmaterial':vmaterial,'data': data[0], 'company_name': company_name, 'no': s, 'd1': valid_upto, 'd2': issue_date})

            
    return redirect('/')






def rca_certificate(request, id, otp):
    print("officer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otp")

    if request.method == "POST":
        # try:
        data_usr_obj = Rca_User_Registration.objects.get(User_Id=id)
        User_Zone = data_usr_obj.User_zone

        Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
        cmobile = data_usr_obj.ContactNo
        UCDM_obj = Rca_User_Registration.objects.get(User_Id=id)
        from datetime import date
        from datetime import time
        from datetime import datetime
        import datetime
        td = datetime.datetime.now()
        current_time = td.strftime("%H:%M:%S")
        company_name = data_usr_obj.CompanyName_E
        import datetime as dt
        import calendar
        day = dt.datetime.now().date()
       

        data_usr_obj11 = Rca_User_Registration.objects.filter(User_Id=id)
       
        
        data_usr_obj22 = Rca_User_Registration.objects.get(User_Id=id)

        if certificate_details_cra.objects.filter(User_Id=id).exists():
            return HttpResponse(
                "Certificate already generated. Please login and check the generated certificate on the dashboard")
        else:
            data = Rca_User_Registration.objects.filter(User_Id=id)
            officer_otp = request.POST.get('officer_otp')
            usr_obj = Rca_User_Registration.objects.get(User_Id=id)

            data = Rca_User_Registration.objects.filter(User_Id=id)
            company_name = data[0].CompanyName_E

            data111 = Rca_User_Registration.objects.get(User_Id=id)
            cmobile = data111.ContactNo
          
            from datetime import date
            from datetime import time
            from datetime import datetime
            import datetime
            td = datetime.datetime.now()
            current_time = td.strftime("%H:%M:%S")
            UCDM_obj = Rca_User_Registration.objects.get(User_Id=id)

            import datetime as dt
            import calendar
            day = dt.datetime.now().date()
            three_year_delta = dt.timedelta(days=1096 if ((day.month >= 3 and calendar.isleap(day.year + 3)) or (
                    day.month < 3 and calendar.isleap(day.year))) else 1095)
            valid_upto = day + three_year_delta
            employ_login_id = request.session['employ_login_id']
            Officer_obj = Officer.objects.get(employ_login_id=employ_login_id)
            if officer_otp.strip() == ((usr_obj.Otp).strip()):
                from datetime import date
                User_Zone = usr_obj.User_zone
                User = usr_obj.User_type
                vendor_type = "00"
                nabl_type = "01"
                tkc_type = "02"
                today = date.today()
                date = today.strftime("%m%y")
                list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                s = ""
                expi_date = ""
                tkc_class_contractor = ""
                if User_Zone == "CZ":
                    s = "CZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = Rca_User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                        cert_obj = certificate_details_cra(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_code,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'rca/cert_cz_new.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                    
                if User_Zone == "EZ":
                    s = "EZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = Rca_User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                      
                        cert_obj = certificate_details_cra(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_code,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'rca/cert_ez_new.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                    
                if User_Zone == "WZ":
                    s = "WZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = Rca_User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                       
                        cert_obj = certificate_details_cra(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_code,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'rca/cert_wz_new.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                   
            else:
                return render(request, 'main/offcier_otp_rca.html', {'id': id, 'otp': otp})







def rca_certificate_regular(request, id, otp):
    print("officer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otpofficer_otp")

    if request.method == "POST":
        # try:
        data_usr_obj = Rca_User_Registration.objects.get(User_Id=id)
        User_Zone = data_usr_obj.User_zone

        Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
        cmobile = data_usr_obj.ContactNo
        UCDM_obj = Rca_User_Registration.objects.get(User_Id=id)
        td = datetime.now()
        current_time = td.strftime("%H:%M:%S")
        company_name = data_usr_obj.CompanyName_E
        import datetime as dt
        import calendar
        day = dt.datetime.now().date()
       

        data_usr_obj11 = Rca_User_Registration.objects.filter(User_Id=id)
       
        
        data_usr_obj22 = Rca_User_Registration.objects.get(User_Id=id)

        if certificate_details_cra.objects.filter(User_Id=id).exists():
            return HttpResponse(
                "Certificate already generated. Please login and check the generated certificate on the dashboard")
        else:
            data = Rca_User_Registration.objects.filter(User_Id=id)
            officer_otp = request.POST.get('officer_otp')
            usr_obj = Rca_User_Registration.objects.get(User_Id=id)

            data = Rca_User_Registration.objects.filter(User_Id=id)
            company_name = data[0].CompanyName_E

            data111 = Rca_User_Registration.objects.get(User_Id=id)
            cmobile = data111.ContactNo
          
            td = datetime.now()
            current_time = td.strftime("%H:%M:%S")
            UCDM_obj = Rca_User_Registration.objects.get(User_Id=id)

            import datetime as dt
            import calendar
            day = dt.datetime.now().date()
            three_year_delta = dt.timedelta(days=1096 if ((day.month >= 3 and calendar.isleap(day.year + 3)) or (
                    day.month < 3 and calendar.isleap(day.year))) else 1095)
            valid_upto = day + three_year_delta
            employ_login_id = request.session['employ_login_id']
            Officer_obj = Officer.objects.get(employ_login_id=employ_login_id)
            if officer_otp.strip() == ((usr_obj.Otp).strip()):
                from datetime import date
                User_Zone = usr_obj.User_zone
                User = usr_obj.User_type
                vendor_type = "00"
                nabl_type = "01"
                tkc_type = "02"
                today = date.today()
                date = today.strftime("%m%y")
                list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                s = ""
                expi_date = ""
                tkc_class_contractor = ""
                if User_Zone == "CZ":
                    s = "CZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = Rca_User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                        cert_obj = certificate_details_cra(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_code,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'rca/cert_cz_regular.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                    
                if User_Zone == "EZ":
                    s = "EZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = Rca_User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                      
                        cert_obj = certificate_details_cra(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_code,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'rca/cert_ez_regular.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                    
                if User_Zone == "WZ":
                    s = "WZ"
                    if User == "VENDOR":
                        s = s + "V" + vendor_type + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
                        data11 = Rca_User_Registration.objects.filter(User_Id=id)
                        data11.update(Authentication_id=s)
                        mat_list = []
                       
                        cert_obj = certificate_details_cra(User_Id=id, company_name=company_name,
                                                       Company_add_1=UCDM_obj.Company_add_1,
                                                       Company_add_2=UCDM_obj.Company_add_2,
                                                       Company_dist=UCDM_obj.Company_dist,
                                                       Company_state=UCDM_obj.Company_state,
                                                       Company_pin_code=UCDM_obj.Company_pin_code,
                                                       no=s, User_type=usr_obj.User_code,
                                                       vmaterial=mat_list, day=day, valid_upto=valid_upto,
                                                       employ_name=Officer_obj.employ_name,
                                                       designation=Officer_obj.designation, current_time=current_time,
                                                       User_Zone=User_Zone)
                        cert_obj.save()
                        return render(request, 'rca/cert_wz_regular.html',
                                      {'Officer_obj': Officer_obj, 'usr_obj': usr_obj, 'UCDM_obj': UCDM_obj,
                                       'current_time': current_time, 'data': data[0],
                                       'company_name': company_name, 'no': s, 'day': day, 'valid_upto': valid_upto,
                                       'User_Zone': User_Zone})

                   
            else:
                return render(request, 'main/offcier_otp_rca.html', {'id': id, 'otp': otp})


def factory_initiate_rca(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = Rca_User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone='WZ',provision_fi=0).order_by('User_Id')
            return render(request, 'officer/vendor_factory_inspection_initiate_rca.html', {'data': data})

        elif request.session['officer'] == 'CZ':
            data = Rca_User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone='CZ',provision_fi=0).order_by('User_Id')
            return render(request, 'officer/vendor_factory_inspection_initiate_rca.html', {'data': data})


        elif request.session['officer'] == 'EZ':
            data = Rca_User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone='EZ',provision_fi=0).order_by('User_Id')
            return render(request, 'officer/vendor_factory_inspection_initiate_rca.html', {'data': data})
    return redirect('/')





def factory_inspection_initiate_rca(request, id):
    if request.session.has_key('officer'):
        officer_zone  = request.session['officer']
        data = Rca_User_Registration.objects.get(User_Id=id)
        c_name = data.CompanyName_E
        officer = InspectingOfficerInfo.objects.filter(user_zone=officer_zone)
        if request.method == 'POST':
            officer = request.POST.get('officer')
            officer = InspectingOfficerInfo.objects.get(id=officer)

            mobile = officer.contact_no
            name_sms = officer.officer_name
            oid = officer.officer_employ_id
            pws = officer.officer_password

            date = request.POST.get('date')
            import datetime
            today = datetime.datetime.now()
            data = Rca_User_Registration.objects.get(User_Id=id)
            data1 = RCA_Factory_Inspection_Info(vendor=data, officer=officer, assign_date=today, execution_date=date)
            print("uuuuuu")
            data1.save()
            data.factory_approval_status = 1
            data.save()
            vendor_con = data.ContactNo
            vendor_com = data.CompanyName_E
            zone = data.User_zone
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8000"}
            # for server set proxy
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007254789662546256&mobile_number=" + str(
                            mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(c_name) + "&v4=" + str() + "&v5=" + str(zone) +  "&v6=" + str(date) + "&v7=" + str(oid) + "&v8=" + str(pws) + "&v9=" + str('https://qcportal.mpcz.in/media/apk/FactoryInspection.apk') + "&v10=" + str()
            response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1007254789662546256',date = datetime.datetime.now(),mobile_number = mobile)
            sms_template.save()
            
            

            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007363155209103912&mobile_number=" + str(
                            vendor_con) + "&v1=" + str(vendor_com) + "&v2=" + str() + "&v3=" + str() + "&v4=" + str(date)
            response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1007363155209103912',date = datetime.datetime.now(),mobile_number = vendor_con)
            sms_template.save()
            
            data = Rca_User_Registration.objects.filter(
                factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone=officer_zone)
            return render(request, 'officer/vendor_factory_inspection_initiate_rca.html', {'data': data})
            
        return render(request, 'main/vendor_factory_inspection_rca.html', {'data': data, 'employee': officer})
    return redirect('/')



def factory_assigned_rca(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data1 = RCA_Factory_Inspection_Info.objects.filter(vendor__factory_approval_status=1,vendor__User_zone='WZ')          
            return render(request, 'officer/vendor_factory_inspection_assined_rca.html', {'data1': data1})
           


        elif request.session['officer'] == 'CZ':
            data1 = RCA_Factory_Inspection_Info.objects.filter(vendor__factory_approval_status=1,vendor__User_zone='CZ')
            return render(request, 'officer/vendor_factory_inspection_assined_rca.html', {'data1': data1})
            

        elif request.session['officer'] == 'EZ':
            data1 = RCA_Factory_Inspection_Info.objects.filter(vendor__factory_approval_status=1,vendor__User_zone='EZ')
            return render(request, 'officer/vendor_factory_inspection_assined_rca.html', {'data1': data1})

    return redirect('/')
    
def cert_upload_download_rca(request, id):
    cert_u_obj = certificate_details_cra.objects.get(User_Id=id)
    usr_obj = Rca_User_Registration.objects.get(User_Id=id)
    return render(request, 'rca/cert_all_rca.html', {'cert_u_obj':cert_u_obj, 'usr_obj':usr_obj})


def digital_sign_cert_rca(request, user_type, User_Zone):
    if user_type == "RCA":
        usr_obj = Rca_User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type="VENDOR", User_zone=User_Zone)
        return render(request, 'officer/digital_sign_cert_rca.html', {'usr_obj':usr_obj})
    
def uplaod_cert_rca(request, no):
    usr_obj1 = Rca_User_Registration.objects.get(Authentication_id=no)
    if request.method == "POST":
        if request.FILES['digitalCert']:
            filename = request.FILES['digitalCert']  
            cert_det_obj = certificate_details_cra.objects.get(no=no)
            usr_obj = Rca_User_Registration.objects.get(Authentication_id=no)
            cert_det_obj.image = filename
            cert_det_obj.save()
            usr_obj.digital_cert_upload=1
            usr_obj.cert = filename
            usr_obj.save()
        return render(request, 'officer/certificate_submit_rca.html', {'User_type':usr_obj1.User_type})
    else:
        return render(request, 'officer/certificate_submit_rca.html', {'User_type':usr_obj1.User_type})

def certificate_submit_rca(request, User_type):
    if User_type == "RCA":
        return render(request, 'main/mpeb_base.html')

def factory_assigned_rca_view(request,id):
    if request.session.has_key('officer'):
        data = Rca_User_Registration.objects.get(User_Id=id)
        officer = RCA_Factory_Inspection_Info.objects.filter(vendor=data)
        return render(request,'officer/factory_assigned_rca_view.html',{'officer':officer})
    return redirect('/')

def all_rca_vendor_approved_list(request):
    usr_obj = Rca_User_Registration.objects.filter(digital_cert_upload = '1')
    
    return render(request, 'officer/all_rca_vendor_approved_list.html', {'usr_obj':usr_obj}) 


def all_vendor_approved_list(request):
    usr_obj = User_Registration.objects.filter(User_type='VENDOR',complete_data=1,Complete_Details=1)
    return render(request, 'officer/all_vendor_approved_list.html', {'doc':usr_obj})

def all_vendor_approved_list_documents(request,id):
        usr_obj = User_Registration.objects.get(User_Id= id)
        doc = Vendor_Document.objects.filter(user_id=usr_obj.User_Id)
        CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=usr_obj)
        Vendor_Material_Details1 = Vendor_Material_Details.objects.filter(user_id=usr_obj.User_Id)
        Vendor_Technical_Details1 = Vendor_Technical_Details.objects.filter(user_id=usr_obj.User_Id)

        return render(request, 'officer/all_vendor_approved_list_documents.html', {'data': usr_obj, 'doc': doc, 'CompanyData': CompanyData1,'Vendor_Material_Details': Vendor_Material_Details1,'Vendor_Technical_Details': Vendor_Technical_Details1})



def Add_Factory_Officer(request):
    if request.method == 'POST':
        officer_name = request.POST.get('officer_name')
        contact_no = request.POST.get('officer_contact')
        officer_email = request.POST.get('officer_email')
        officer_employ_id = request.POST.get('officer_id')
        officer_designation = request.POST.get('officer_designation')
        officer_place = request.POST.get('officer_place')
        officer_zone = request.POST.get('officer_zone')
        
        def generateOTP():
            digits = "0123456789"
            OTP = ""
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            return OTP

        otp = generateOTP()

        ins_officer = InspectingOfficerInfo(officer_name=officer_name,contact_no=contact_no,officer_email=officer_email,officer_employ_id=officer_employ_id,officer_designation=officer_designation,officer_password=otp,officer_work='FI',user_zone=officer_zone,officer_address=officer_place)
        ins_officer.save()
        data = Rca_User_Registration.objects.filter(
                factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone=officer_zone)
        return render(request, 'officer/vendor_factory_inspection_initiate_rca.html', {'data': data})
    return render(request, 'officer/add_fi_officer.html')        


# def Anubhand_Entry(request):
    # try:
        # u1_obj = User_Registration.objects.filter(cgm_approval = 1, digital_cert_upload = 0, User_type = 'TKC')
        # lst_already_uploaded = []
        # lst_uploaded = []
        # for user_obj in u1_obj:
            # if certificate_details.objects.filter(User_Id=user_obj.User_Id).exists():
                # lst_already_uploaded.append(user_obj.User_Id)
                # pass
            # else:
                # lst_uploaded.append(user_obj.User_Id)
                # usr_obj = User_Registration.objects.get(User_Id = user_obj.User_Id)
                # UCDM_obj = UserCompanyDataMain.objects.get(user_id = usr_obj.ContactNo)
                
                # from datetime import date
                # from datetime import time
                # from datetime import datetime
                # import datetime
                # td = datetime.datetime.now()
                # current_time = td.strftime("%H:%M:%S")
                # today = date.today()

                # var_oyt = ""
                # if usr_obj.Oyt == '9':
                    # var_oyt = "TKC"
                # elif usr_obj.Oyt == '8':
                    # var_oyt = "A5"
                # elif usr_obj.Oyt == '7':
                    # var_oyt = "A4"
                # elif usr_obj.Oyt == '6':
                    # var_oyt = "A3"
                # elif usr_obj.Oyt == '5':
                    # var_oyt = "A2 (with OYT)"
                # elif usr_obj.Oyt == '3':
                    # var_oyt = "A1 (With OYT)"
                # elif usr_obj.Oyt == '1':
                    # var_oyt = "B"

                # try:
                    # if TKC_Document.objects.filter(user_id=usr_obj.User_Id, Types_of_Docs='ELECTRICAL LICENSE').exists():
                        # exp = TKC_Document.objects.get(user_id=usr_obj.User_Id, Types_of_Docs='ELECTRICAL LICENSE')
                        # expi_date = exp.Doc_expiry_date
                        # cert_obj = certificate_details(User_Id=usr_obj.User_Id,Authorised_person_E= usr_obj.Authorised_person_E,
                            # company_name=usr_obj.CompanyName_E,
                            # Company_add_1=UCDM_obj.Company_add_1, Company_add_2=UCDM_obj.Company_add_2,
                            # Company_dist=UCDM_obj.Company_dist,Company_state=UCDM_obj.Company_state,
                            # Company_pin_code=UCDM_obj.Company_pin_code, no=usr_obj.Authentication_id,
                            # User_type=usr_obj.User_type, vmaterial="[]",
                            # day=today, valid_upto="expi_date", employ_name="Anubandh Portal", designation="GM_Works",
                            # current_time=current_time, tkc_class_contractor=var_oyt, electic_liecense_date=expi_date,
                            # User_Zone=usr_obj.User_zone, nabl_cert_exp="", nabl_cert_number="", image="")
                        # cert_obj.save()
                    # else:
                        # pass
                # except Exception as e:
                    # if TKC_Document.objects.filter(user_id=usr_obj.User_Id, Types_of_Docs='Electrical License').exists():
                        # exp = TKC_Document.objects.get(user_id=usr_obj.User_Id, Types_of_Docs='Electrical License')
                        # expi_date = exp.Doc_expiry_date
                        # cert_obj = certificate_details(User_Id=usr_obj.User_Id,Authorised_person_E= usr_obj.Authorised_person_E,
                            # company_name=usr_obj.CompanyName_E,
                            # Company_add_1=UCDM_obj.Company_add_1, Company_add_2=UCDM_obj.Company_add_2,
                            # Company_dist=UCDM_obj.Company_dist,Company_state=UCDM_obj.Company_state,
                            # Company_pin_code=UCDM_obj.Company_pin_code, no=usr_obj.Authentication_id,
                            # User_type=usr_obj.User_type, vmaterial="[]",
                            # day=today, valid_upto="expi_date", employ_name="Anubandh Portal", designation="GM_Works",
                            # current_time=current_time, tkc_class_contractor=var_oyt, electic_liecense_date=expi_date,
                            # User_Zone=usr_obj.User_zone, nabl_cert_exp="", nabl_cert_number="", image="")
                        # cert_obj.save()
                    # else:
                        # pass
                
        # final_list = ["Currently_uploaded : ", lst_uploaded,"--------" ,"Already_uploaded : ", lst_already_uploaded]
        # return HttpResponse(final_list)
    # except Exception as e:
        # return HttpResponse(e)
        
def Anubhand_Entry(request):
    try:
        u1_obj = User_Registration.objects.filter(cgm_approval = 1, digital_cert_upload = 0, User_type = 'TKC')
        lst_already_uploaded = []
        lst_uploaded = []
        for user_obj in u1_obj:
            if certificate_details.objects.filter(User_Id=user_obj.User_Id).exists():
                c_obj = certificate_details.objects.get(User_Id=user_obj.User_Id)
                c_obj.User_Zone = user_obj.User_zone
                c_obj.Authorised_person_E = user_obj.Authorised_person_E
                c_obj.save()
                lst_already_uploaded.append(user_obj.User_Id)
                pass
            else:
                lst_uploaded.append(user_obj.User_Id)
                usr_obj = User_Registration.objects.get(User_Id = user_obj.User_Id)
                UCDM_obj = UserCompanyDataMain.objects.get(user_id_id = usr_obj)
                
                from datetime import date
                from datetime import time
                from datetime import datetime
                import datetime
                td = datetime.datetime.now()
                current_time = td.strftime("%H:%M:%S")
                today = date.today()

                var_oyt = ""
                if usr_obj.Oyt == '9':
                    var_oyt = "TKC"
                elif usr_obj.Oyt == '8':
                    var_oyt = "A5"
                elif usr_obj.Oyt == '7':
                    var_oyt = "A4"
                elif usr_obj.Oyt == '6':
                    var_oyt = "A3"
                elif usr_obj.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif usr_obj.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif usr_obj.Oyt == '1':
                    var_oyt = "B"

                try:
                    if TKC_Document.objects.filter(user_id=usr_obj.User_Id, Types_of_Docs='Electrical License').exists():
                        exp = TKC_Document.objects.get(user_id=usr_obj.User_Id, Types_of_Docs='Electrical License')
                        expi_date = exp.Doc_expiry_date
                        cert_obj = certificate_details(User_Id=usr_obj.User_Id,Authorised_person_E= usr_obj.Authorised_person_E,
                            company_name=usr_obj.CompanyName_E,
                            Company_add_1=UCDM_obj.Company_add_1, Company_add_2=UCDM_obj.Company_add_2,
                            Company_dist=UCDM_obj.Company_dist,Company_state=UCDM_obj.Company_state,
                            Company_pin_code=UCDM_obj.Company_pin_code, no=usr_obj.Authentication_id,
                            User_type=usr_obj.User_type, vmaterial="[]",
                            day=today, valid_upto="expi_date", employ_name="Anubandh Portal", designation="GM_Works",
                            current_time=current_time, tkc_class_contractor=var_oyt, electic_liecense_date=expi_date,
                            User_Zone=usr_obj.User_zone, nabl_cert_exp="", nabl_cert_number="", image="")
                        cert_obj.save()
                    else:
                        pass
                except Exception as e:
                    if TKC_Document.objects.filter(user_id=usr_obj.User_Id, Types_of_Docs='Electrical License').exists():
                        exp = TKC_Document.objects.get(user_id=usr_obj.User_Id, Types_of_Docs='Electrical License')
                        expi_date = exp.Doc_expiry_date
                        cert_obj = certificate_details(User_Id=usr_obj.User_Id,Authorised_person_E= usr_obj.Authorised_person_E,
                            company_name=usr_obj.CompanyName_E,
                            Company_add_1=UCDM_obj.Company_add_1, Company_add_2=UCDM_obj.Company_add_2,
                            Company_dist=UCDM_obj.Company_dist,Company_state=UCDM_obj.Company_state,
                            Company_pin_code=UCDM_obj.Company_pin_code, no=usr_obj.Authentication_id,
                            User_type=usr_obj.User_type, vmaterial="[]",
                            day=today, valid_upto="expi_date", employ_name="Anubandh Portal", designation="GM_Works",
                            current_time=current_time, tkc_class_contractor=var_oyt, electic_liecense_date=expi_date,
                            User_Zone=usr_obj.User_zone, nabl_cert_exp="", nabl_cert_number="", image="")
                        cert_obj.save()
                    else:
                        pass
                
        final_list = ["Currently_uploaded : ", lst_uploaded,"--------" ,"Already_uploaded : ", lst_already_uploaded]
        return HttpResponse(final_list)
    except Exception as e:
        return HttpResponse(e)        
        
        
from datetime import datetime
def new_status(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Authentication_id__isnull=False)).order_by('CompanyName_E')
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
    to_daaa =datetime.datetime.today()
    return render(request, 'officer/Active_tkc.html', {'data':data,'officer':officer,'contractor':contractor_class,'doc':doc,'to_daaa':to_daaa,'today':today})



import csv
def export_users_csv(request):
  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Contractor.csv"'
    writer = csv.writer(response)
    writer.writerow(['Discom','	Registration_Number','authorised person','contact'])
    data11 = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False))
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License')
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    to_daaa =datetime.datetime.today()
    data = data11.values_list('User_zone','Authentication_id','Authorised_person_E','ContactNo')
    # paginator=Paginator(users ,50)
    # page=request.GET.get('page')
    # users=paginator.get_page(page) 
    for user in data:
        writer.writerow(user)
    return response


def gm_search_by_id(request):
    search_post = request.GET.get('search')
    from datetime import datetime
    import datetime
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    if search_post:
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1) | Q(Authentication_id__isnull=False)) & (Q(Authentication_id__isnull=False)) & (Q(Authentication_id__icontains=search_post) | Q(CompanyName_E__icontains=search_post) | Q(Authorised_person_E__icontains=search_post)))
        contractor_class = TKC_Payment.objects.all()
        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data=0)
        from datetime import date
        from datetime import time
        from datetime import datetime
        import datetime
        to_daaa =datetime.datetime.today()
        return render(request, 'officer/search_gm.html',{'data':data,'contractor':contractor_class,'doc':doc,'to_daaa':to_daaa,'officer':officer})
    return render(request, 'officer/search_gm.html',{'officer':officer})




def dgm_complete_tkc(request):
    if request.session.has_key('employ_login_id'):
        if request.session['officer'] == 'WZ':
            alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0,User_zone='WZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=0,User_zone='WZ') | User_Registration.objects.filter(Complete_Details=1,finance_approval=2,User_zone='WZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=2,User_zone='WZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
    
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/dgm_complete_tkc.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})
        elif request.session['officer'] == 'CZ':
            alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0,User_zone='CZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=0,User_zone='CZ') | User_Registration.objects.filter(Complete_Details=1,finance_approval=2,User_zone='CZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=2,User_zone='CZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
    
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/dgm_complete_tkc.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})

        elif request.session['officer'] == 'EZ':
            alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0,User_zone='EZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=0,User_zone='EZ') | User_Registration.objects.filter(Complete_Details=1,finance_approval=2,User_zone='EZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=2,User_zone='EZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
    
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/dgm_complete_tkc.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})

    return redirect('/')    


def factory_payment_details(request):
    if request.session.has_key('employ_login_id'):
        factory = Factory_Form_Details.objects.filter(status=1)
        return render(request, 'officer/factory_payment_form.html', {'data': factory})
    return redirect('/')   



def all_factory_payment_details_save(request,id):
    doc = Factory_Form_Details.objects.get(id=id)
    user = User_Registration.objects.get(User_Id = doc.vendor.User_Id)
    if request.method == 'POST':
        result=request.GET.get('a')
        result =request.POST.get('a')
        print("result",result)
        if result == 'OK':
            
            doc.status = 2
            doc.remark = request.POST.get("remark")
            doc.save()
            user.factory_approval_payment = 1
            user.factory_waiver = 2
            user.save()
            
            data = Factory_Form_Details.objects.filter(status=1)
          
            return render(request, 'officer/factory_payment_form.html', {'data': data})
    
        elif result == 'NOT':
            doc.status = 3
            doc.remark = request.POST.get("remark")
            doc.save()
            user.factory_waiver = 3
            user.save()
            data = Factory_Form_Details.objects.filter(status=1)
            return render(request, 'officer/factory_payment_form.html', {'data': data})

    return render(request, 'officer/all_pending_loa_for_approvel_evaluate.html',{'abc':doc})


    
def all_factory_payment_material(request,id):
    if request.session.has_key('employ_login_id'):
        doc = Factory_Form_Details.objects.get(id=id)
        user = User_Registration.objects.get(User_Id = doc.vendor.User_Id)
        material = Vendor_Material_Details.objects.filter(user_id=user)
        return render(request, 'officer/factory_payment_material_form.html', {'data': material})

    return redirect('/')




def new_material_vendor_dgm_evaluate(request,id):
    if request.session.has_key('employ_login_id'):
        
        alldata =  User_Registration.objects.filter(User_Id=id)
        data_new =  User_Registration.objects.get(User_Id=id)
        material = Vendor_Material_Details.objects.filter(user_id=alldata[0].User_Id,new_material = 1)
        CompanyData1 = UserCompanyDataMain.objects.get(user_id_id = data_new)
        list_all0=[]
        if request.method == 'POST':
            for data1 in material:
                pstatus = request.POST.get(f'{data1.id}')
                premark = request.POST.get(f'a{data1.id}')
                list_all0.append(pstatus)
                if pstatus == "2":
                    
                    data1.Primary_verification_Status= 2
                    data1.DGM_remark=premark
                    data1.new_material = 2
                    data1.save()
                    data_new.add_material = -1
                    data_new.save()

                elif pstatus == "1":
                    data1.Primary_verification_Status = 1
                    data1.Status = 1
                    data1.DGM_remark=premark
                    data1.save()

            if ("0") not in list_all0 and ("2") not in list_all0: 
                data = User_Registration.objects.get(User_Id=id)
                data.add_material = 4
                data.factory_approval_status = 0
                data.factory_approval = 0
                data.save()

            # if request.method == 'POST':
            #     remark = request.POST.getlist('name_data')

            #     # [material.update(Primary_remark=i) for i in remark]
            #     for i in remark:
            #         material.update(Primary_remark=i)
            #     alldata.update(add_material=3)
                return redirect('/new_material_vendor_dgm')

        return render(request, 'officer/new_material_evaluate_dgm.html', {'data': data_new,'CompanyData':CompanyData1,'material':material})

    return redirect('/')









def new_material_vendor_cgm_evaluate(request,id):
    if request.session.has_key('employ_login_id'):
        
        alldata =  User_Registration.objects.filter(User_Id=id)
        data_new =  User_Registration.objects.get(User_Id=id)
        material = Vendor_Material_Details.objects.filter(user_id=alldata[0].User_Id,Status=1,new_material=1)
        CompanyData1 = UserCompanyDataMain.objects.get(user_id_id = data_new)
        if request.method == 'POST':
            remark = request.POST.getlist('name_data')

            # [material.update(Primary_remark=i) for i in remark]
            for i in remark:
                material.update(Primary_remark=i)
            alldata.update(add_material=4,factory_approval=0,factory_approval_status=0)
            return redirect('/new_material_vendor_cgm')

        return render(request, 'officer/new_material_evaluate_cgm.html', {'data': alldata[0],'material':material,'CompanyData':CompanyData1})

    return redirect('/')    
    
    

def cgm_pending_vendor_new(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='WZ',add_material=4)
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor_new.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='CZ',add_material=4)
            print("yyyyyyyyyyyyyyy",data)
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor_new.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='EZ',add_material=4)
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/cgm_pending_vendor_new.html',{'data': data,'b':fdata})
    return redirect('/')




def vendor_cgm_evaluate_new(request, id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id,Primary_verification_Status=1)
        New_Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id,Status=1,new_material = 1,Primary_verification_Status=1)
        CompanyData1 = UserCompanyDataMain.objects.get(user_id_id = data_new)
        # fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
        fac_image = Vendor_Factory_image.objects.filter(vendor=data_new)
        from datetime import date
        from datetime import time
        from datetime import datetime
        import datetime
        if request.method == 'POST':
            data_new_status = User_Registration.objects.get(User_Id=id)
            vmaterial = Vendor_Material_Details.objects.filter(user_id=data_new_status.User_Id,Primary_verification_Status=1)
            for i in vmaterial:
                i.new_status = 1
                i.save()
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            officer_mobile = officer.mobile
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otptt = generateOTP()
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
            sms_template.save()

            request.session['otptt'] = otptt
            request.session['officer_mobile'] = officer_mobile
            otp_ofcr = User_Registration.objects.filter(User_Id=id)
            otp_ofcr.update(Otp=otptt)

            usr_obj = User_Registration.objects.get(User_Id=id)
            otp = usr_obj.Otp

            return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})
        return render(request, 'officer/vendor_cgm_evaluate_new.html',{'data': data[0],'fac_image':fac_image ,'Material': Material,'New_Material':New_Material,'CompanyData':CompanyData1})
    return redirect('/')


def dgm_finance_complete_status(request):
    if request.session.has_key('employ_login_id'):
        if request.session['officer'] == 'WZ':
            alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0,User_zone='WZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=0,User_zone='WZ') | User_Registration.objects.filter(Complete_Details=1,finance_approval=2,User_zone='WZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=2,User_zone='WZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
    
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/dgm_finance_complete_status.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})
        elif request.session['officer'] == 'CZ':
            alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0,User_zone='CZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=0,User_zone='CZ') | User_Registration.objects.filter(Complete_Details=1,finance_approval=2,User_zone='CZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=2,User_zone='CZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
    
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/dgm_finance_complete_status.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})
        elif request.session['officer'] == 'EZ':
            alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0,User_zone='EZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=0,User_zone='EZ') | User_Registration.objects.filter(Complete_Details=1,finance_approval=2,User_zone='EZ') | User_Registration.objects.filter(Complete_Details=1,work_approval=2,User_zone='EZ')
            contractor_class = TKC_Payment.objects.all()
            doc = TKC_Document.objects.all()
    
            officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
            return render(request, 'officer/dgm_finance_complete_status.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})

    return redirect('/')    



def cgm_qc_complete_status(request):
    if request.session.has_key('employ_login_id'):
        alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0) | User_Registration.objects.filter(Complete_Details=1,work_approval=0) | User_Registration.objects.filter(Complete_Details=1,finance_approval=2) | User_Registration.objects.filter(Complete_Details=1,work_approval=2)
        contractor_class = TKC_Payment.objects.all()
        doc = TKC_Document.objects.all()
   
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        return render(request, 'officer/cgm_qc_complete_status.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})

    return redirect('/')
    
    

from datetime import datetime
def contractor_status_check(request):
    search_post = request.GET.get('search')
    c_status = request.GET.get('status')
    
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()
    if search_post =="All" and c_status =="All":
        # all_data = request.POST.get('all')
        data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1,blacklisted=0,deregister=0)|Q(User_type='TKC',Authentication_id__isnull=False,blacklisted=0,deregister=0))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data=0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'main/all_contractor_details.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
    elif search_post =="All" and c_status !="All":
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(Oyt__icontains=c_status))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data=0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'main/all_contractor_details.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
        
    if search_post and c_status !="All":
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(User_zone__icontains=search_post)& Q(Oyt__icontains=c_status))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data=0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'main/all_contractor_details.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
    if search_post and c_status =="All":
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(User_zone__icontains=search_post))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data=0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'main/all_contractor_details.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
    
    if c_status:
        data = User_Registration.objects.filter((Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False)) & Q(Oyt__icontains=c_status))
        lst_oyt = []
        address = []
        for i in data:
            var_oyt = ""
            if i.Oyt == '9':
                var_oyt = "TKC"
            elif i.Oyt == '8':
                var_oyt = "A5"
            elif i.Oyt == '7':
                var_oyt = "A4"
            elif i.Oyt == '6':
                var_oyt = "A3"
            elif i.Oyt == '5':
                var_oyt = "A2 (with OYT)"
            elif i.Oyt == '3':
                var_oyt = "A1 (With OYT)"
            elif i.Oyt == '1':
                var_oyt = "B"
            lst_oyt.append(var_oyt)
            
        
        for j in data:
            add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
            address.append(add)

        doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data=0)
        to_daaa =datetime.datetime.today()
        final_lst = zip(data,lst_oyt,address)
        return render(request, 'main/all_contractor_details.html', {'data':data,'doc':doc,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})

    return render(request, 'main/all_contractor_details.html', {'today':today})


def authZoneUpdate(request):
    lst_cert_id = []
    c_obj = certificate_details.objects.all()
    for i in c_obj:
        try:
            usr_obj = User_Registration.objects.get(User_Id = i.User_Id)
            cert_obj = certificate_details.objects.get(cert_id = i.cert_id)
            cert_obj.User_Zone = usr_obj.User_zone
            cert_obj.Authorised_person_E  = usr_obj.Authorised_person_E
            cert_obj.save()
            lst_cert_id.append(i.cert_id)
        except Exception as e:
            pass
    return HttpResponse(lst_cert_id)


def rca_cgm_view_complete_vendor(request, id):
    data = Rca_User_Registration.objects.filter(User_Id=id)
    data1 = Rca_User_Registration.objects.get(User_Id=id)
    doc = Rca_Vendor_Document.objects.filter(user_id=data[0].User_Id)
    image = RCA_Vendor_Factory_image.objects.filter(Vendor=data1)
    return render(request, 'officer/rca_cgm_view_complete_vendor.html',{'abc':doc,'data':data[0],'image':image})    



def contractor_deregistered_cgm(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1,deregister=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False,deregister=1)).order_by('CompanyName_E')
    return render(request, 'officer/deregister_tkc_cgm.html', {'data':data,'officer':officer})

def deregister_tkc_dgm_work(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1,deregister=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False,deregister=1)).order_by('CompanyName_E')
    return render(request, 'officer/deregister_tkc_dgm_work.html', {'data':data,'officer':officer})

def deregister_tkc_dgm_finance(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1,deregister=1)|Q(User_type='TKC',Complete_Details='0',cgm_approval=0,complete_data=0,Authentication_id__isnull=False,deregister=1)).order_by('CompanyName_E')
    return render(request, 'officer/deregister_tkc_dgm_finance.html', {'data':data,'officer':officer})
    
from django.db.models import Q

def pending_contractor_filed_officer(request):
    search_post = request.GET.get('search')
    data =User_Registration.objects.filter(Q(User_type='TKC',Complete_Details=1,complete_data=1,Authentication_id__isnull=True) |Q(User_type='TKC',Complete_Details=1,complete_data=1,Authentication_id__isnull=False))

    if search_post:
        data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details=1,complete_data=1,Authentication_id__isnull=True) |Q(User_type='TKC',Complete_Details=1,complete_data=1,Authentication_id__isnull=False) & Q(CompanyName_E=search_post))
        return render(request, 'officer/pending_contractor_filed_officer.html',{'data':data})
    else:
        data =User_Registration.objects.filter(Q(User_type='TKC',Complete_Details=1,complete_data=1,Authentication_id__isnull=True) |Q(User_type='TKC',Complete_Details=1,complete_data=1,Authentication_id__isnull=False))
        return render(request, 'officer/pending_contractor_filed_officer.html',{'data':data})
    return render(request, 'officer/pending_contractor_filed_officer.html',{'data':data})
    
    
    
    
def vendor_factory_status_view_dgm_work(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Q(cgm_approval=0, work_approval=1, finance_approval=1, User_type='VENDOR',User_zone='WZ') |Q(add_material=4,User_type='VENDOR',User_zone='WZ'))
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/vendor_factory_status_view_dgm_work.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Q(cgm_approval=0, work_approval=1, finance_approval=1, User_type='VENDOR',User_zone='CZ') |Q(add_material=4,User_type='VENDOR',User_zone='CZ'))
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/vendor_factory_status_view_dgm_work.html',{'data': data,'b':fdata})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Q(cgm_approval=0, work_approval=1, finance_approval=1, User_type='VENDOR',User_zone='EZ') |Q(add_material=4,User_type='VENDOR',User_zone='EZ'))
            fdata = Factory_Inspection_Info.objects.all()
            return render(request, 'officer/vendor_factory_status_view_dgm_work.html',{'data': data,'b':fdata})
    return redirect('/')
    
    
    
    
def contractor_certificate_dgm_work_view(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1, User_type='TKC',User_zone='WZ')
            return render(request, 'officer/contractor_certificate_dgm_work_view.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1, User_type='TKC',User_zone='CZ')
            return render(request, 'officer/contractor_certificate_dgm_work_view.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1, User_type='TKC',User_zone='EZ')
            return render(request, 'officer/contractor_certificate_dgm_work_view.html',{'data': data})
    return redirect('/')
    
    
    
def new_material_vendor_dgm(request):
    if request.session.has_key('employ_login_id'):
        if request.session['officer'] == 'WZ':
            alldata =  User_Registration.objects.filter(User_type='VENDOR',add_material=2,User_zone='WZ') 
            return render(request, 'officer/new_material_vendor_dgm.html', {'data': alldata})
            
        elif request.session['officer'] == 'CZ':
            alldata =  User_Registration.objects.filter(User_type='VENDOR',add_material=2,User_zone='CZ') 
            return render(request, 'officer/new_material_vendor_dgm.html', {'data': alldata})
            
        elif request.session['officer'] == 'EZ':
            alldata =  User_Registration.objects.filter(User_type='VENDOR',add_material=2,User_zone='EZ') 
            return render(request, 'officer/new_material_vendor_dgm.html', {'data': alldata})
            

    return redirect('/')

    
    

def new_material_vendor_cgm(request):
    if request.session.has_key('employ_login_id'):
        if request.session['officer'] == 'WZ':
            alldata =  User_Registration.objects.filter(User_type='VENDOR',add_material=3,User_zone='WZ').order_by('User_Id') 
            return render(request, 'officer/new_material_vendor_cgm.html', {'data': alldata})
            
        elif request.session['officer'] == 'CZ':
            alldata =  User_Registration.objects.filter(User_type='VENDOR',add_material=3,User_zone='CZ').order_by('User_Id')
            return render(request, 'officer/new_material_vendor_cgm.html', {'data': alldata})
            
        elif request.session['officer'] == 'EZ':
            alldata =  User_Registration.objects.filter(User_type='VENDOR',add_material=3,User_zone='EZ').order_by('User_Id')
            return render(request, 'officer/new_material_vendor_cgm.html', {'data': alldata})
            

    return redirect('/')    
    
    
    
    
def all_wo(request):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])
    wo = TKCWoInfo.objects.filter(Status=1, zone=officer.user_zone)
    return render(request, 'officer/work_order.html',
                  {"officer": officer, 'wo': wo})
    
# def pdi_initiate(request,id):
#     if request.session.has_key('officer'):
#         officer = Officer.objects.get(employ_id=request.session['employ_id'])
#         wo = TKCWoInfo.objects.get(id=id)
#         offer = Offer_Material.objects.filter(TKCVendor__TKCWoInfo=wo, Material_Offer_Submit=1, Status=1)
#         return render(request, 'officer/pdi_factory_inspection_initiate.html', {'data': offer})
#     return redirect('/')



# def pdi_inspection_initiate(request, id):
#     if request.session.has_key('officer'):
#         officer = Officer.objects.get(employ_id=request.session['employ_id'])
#         officer_zone  = request.session['officer']
#         data = Offer_Material.objects.get(id=id)
#         c_name = data.TKCVendor.Vendor.CompanyName_E
#         user_cmpny_data = UserCompanyDataMain.objects.get(user_id_id = data.TKCVendor.Vendor)
#         if request.method == 'POST':
#             try:
#                 another_officer_id  = request.POST.get('another_officer')
#                 another_officer = InspectingOfficerInfo.objects.get(id=another_officer_id)
#                 another_officer_mobile = another_officer.contact_no
#                 anoher_officer_name = another_officer.officer_name
#             except:
#                 another_officer = None
#             officer1 = request.POST.get('officer')
#             officer1 = InspectingOfficerInfo.objects.get(id=officer1)
#             mobile = officer1.contact_no
#             name_sms = officer1.officer_name
#             oid = officer1.officer_employ_id
#             pws = officer1.officer_password
#             date = request.POST.get('date')
#             import datetime
#             today = datetime.datetime.now()
#             data = Offer_Material.objects.get(id=id)
#             data1 = PDI_Inspection_Info(Material=data, officer=officer1, assign_date=today, execution_date=date, another_officer = another_officer)
#             data1.save()
#             data.PDI_Assign = 1
#             data.PDI=PDI_Inspection_Info.objects.latest('id')
#             data.PDI_Assign_At = datetime.datetime.now().date()
#             data.PDI_Assign_By= officer.employ_name
#             data.save()
#             vendor_con = data.TKCVendor.TKCWoInfo.supplier.ContactNo
#             vendor_com = data.TKCVendor.TKCWoInfo.supplier.CompanyName_E
#             vendor_contact_no = data.TKCVendor.Vendor.ContactNo
#             header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#             # proxyDict = {"http" : "proxy.mpcz.in:8000"}
#             # for server set proxy
#             proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
#             url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007826634677201491&mobile_number=" + str(
#                             mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('pre delivery inspection') + "&v4=" + str(c_name) + "&v5=" + str() + "&v6=" + str('Offer number') + "&v7=" + str() + "&v8=" + str(date) + "&v9=" + str(oid) + "&v10=" + str(pws) + "&v11=" + str('https://qcportal.mpcz.in/media/apk/FactoryInspection.apk') + "&v12=" + str()+ "&v13=" + str()
#             response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

#             if another_officer is not None:
#                 url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007637441628723739&mobile_number=" + str(
#                                 another_officer_mobile) + "&v1=" + str(anoher_officer_name) + "&v2=" + str() + "&v3=" + str(c_name) + "&v4=" + str() + "&v5=" + str() + "&v6=" + str() + "&v7=" + str() + "&v8=" + str(date) + "&v9=" + str() + "&v10=" + str() + "&v11=" + str('https://qcportal.mpcz.in/media/apk/FactoryInspection.apk') + "&v12=" + str()
#                 response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

#             else:
#                 pass
            
#             devendra_tiwari_pfc_contact = 9479409277
#             url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007637441628723739&mobile_number=" + str(
#                             devendra_tiwari_pfc_contact) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(c_name) + "&v4=" + str() + "&v5=" + str() + "&v6=" + str() + "&v7=" + str() + "&v8=" + str(date) + "&v9=" + str(oid) + "&v10=" + str(pws) + "&v11=" + str('https://qcportal.mpcz.in/media/apk/FactoryInspection.apk') + "&v12=" + str()
#             response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
            
#             url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007363155209103912&mobile_number=" + str(
#                             vendor_con) + "&v1=" + str(vendor_com) + "&v2=" + str() + "&v3=" + str() + "&v4=" + str(date)
#             response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
#             url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007363155209103912&mobile_number=" + str(
#                             vendor_contact_no) + "&v1=" + str(vendor_com) + "&v2=" + str() + "&v3=" + str() + "&v4=" + str(date)
#             response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            
#             officer = InspectingOfficerInfo.objects.filter(user_zone=officer_zone)
#             offer = Offer_Material.objects.filter(TKCVendor__TKCWoInfo=data.TKCVendor.TKCWoInfo, Material_Offer_Submit=1, Status=1)
#             return render(request, 'officer/pdi_factory_inspection_initiate.html', {'data': offer,"user_cmpny_data":user_cmpny_data})
#         officer = InspectingOfficerInfo.objects.filter(user_zone=officer_zone)
#         return render(request, 'officer/pdi_factory_inspection.html', {'data': data, 'employee': officer,"user_cmpny_data":user_cmpny_data})
#     return redirect('/')



def pdi_assigned(request):
    if request.session.has_key('officer'):
        officer = Officer.objects.get(employ_id=request.session['employ_id'])
        data1 = PDI_Inspection_Info.objects.filter(Material__TKCVendor__TKCWoInfo__zone=officer.user_zone)
        return render(request, 'officer/vendor_factory_inspection_assined_pdi.html', {'data1': data1})
    return redirect('/')
   
   
   
from datetime import datetime
def vendor_status_check(request):
    search_post = request.GET.get('search')
    material = request.GET.get('material')
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()

    if search_post =="All":
        data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',cgm_approval=1,blacklisted=0)
        # for i in data:
        #     # material_name = Vendor_Material_Details.objects.filter(user_id=i,user_id__User_type='VENDOR')

        #     material_name = Vendor_Material_Details.objects.prefetch_related('User_Registration_set').all()


        #     # material_name = User_Registration.objects.prefetch_related('Vendor_Material_Details__set').all()
        #     print("ffffff",material_name)

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
        return render(request, 'main/all_vendor_details.html', {'data':data,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})

    if search_post:
        data = User_Registration.objects.filter(Q(User_type='VENDOR',Complete_Details='1',cgm_approval=1,blacklisted=0) & Q(User_zone__icontains=search_post))
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
        return render(request, 'main/all_vendor_details.html', {'data':data,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
   
    
   
    return render(request, 'main/all_vendor_details.html',{'today':today})


   
   
def vendor_check_material(request,id):
    data = User_Registration.objects.get(User_Id = id)
    material = Vendor_Material_Details.objects.filter(user_id = data,new_status = 1)
    list_data = []
    for i in material:
        list_data.append(i.Material_Name)

    if request.method =="POST":
        get_data_value= request.POST.get('get_data_value')
        value_data = Vendor_Material_Details.objects.filter(user_id = data,Material_Name=get_data_value,new_status=1)
        return render(request, 'main/vendor_all_material.html', {'data':value_data}) 


    return render(request, 'main/view_vendor_material.html', {'data':set(list_data),'id':id})   
    
    

def blacklisted(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1,blacklisted=0,User_zone='WZ',User_type='TKC')
            return render(request, 'officer/blacklisted_con.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, blacklisted=0,User_zone='CZ',User_type='TKC')
            return render(request, 'officer/blacklisted_con.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1,blacklisted=0,User_zone='EZ',User_type='TKC')
            return render(request, 'officer/blacklisted_con.html',{'data': data})
    return redirect('/')




def blacklisted_vendor(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(Complete_Details=1,blacklisted=0,User_zone='WZ',User_type='VENDOR')
            return render(request, 'officer/blacklisted_vendor.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(Complete_Details=1, blacklisted=0,User_zone='CZ',User_type='VENDOR')
            return render(request, 'officer/blacklisted_vendor.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(Complete_Details=1,blacklisted=0,User_zone='EZ',User_type='VENDOR')
            return render(request, 'officer/blacklisted_vendor.html',{'data': data})
    return redirect('/')


def blacklisted_save(request):
    if request.session.has_key('employ_login_id'):
        if request.method == 'POST':
            try:
                name = request.POST.get('vendor_name')
                b_type = request.POST.get('timeperiod')
                days = request.POST.get('date_period')
                order_by = request.POST.get('order_by')
                order = request.FILES['order']

                user_id_get = User_Registration.objects.get(CompanyName_E=name)
                user_id_data = str(user_id_get.User_Id)
                print("type(user_id_data)", type(user_id_data))
                data1 = blacklistedSaved(user=user_id_get,user_type=user_id_get.User_type, CompanyName_E=name, blacklisted_type=b_type, date=days,recommended_by=order_by,recommended_order=order)
                data1.save()
                user_id_get = User_Registration.objects.filter(CompanyName_E=name)
                user_id_get.update(blacklisted=1)
                return redirect('blacklisted')
            except Exception as e:
                name = request.POST.get('vendor_name')
                b_type = request.POST.get('timeperiod') 
                order_by = request.POST.get('order_by')
                order = request.FILES['order']  
                user_id_get = User_Registration.objects.get(CompanyName_E=name)
                user_id_data = user_id_get.User_Id
                data2 = blacklistedSaved(user=user_id_get,user_type=user_id_get.User_type,CompanyName_E=name,blacklisted_type=b_type,recommended_by=order_by,recommended_order=order)
                data2.save()
                user_id_get = User_Registration.objects.filter(CompanyName_E=name)
                user_id_get.update(blacklisted=1)
                return render(request,'officer/dgm_work.html')
        
        return render(request, 'officer/blacklisted_con.html')
    return redirect('/')


# *********************************************************************rohit

def blacklisted_gm(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(blacklisted=1, User_type='TKC',User_zone='WZ')
            return render(request, 'officer/cgm_blacklisted_pending.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(blacklisted=1, User_type='TKC',User_zone='CZ')
            return render(request, 'officer/cgm_blacklisted_pending.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(blacklisted=1, User_type='TKC',User_zone='EZ')
            return render(request, 'officer/cgm_blacklisted_pending.html',{'data': data})
    return redirect('/')

def blacklisted_gm_evaluate(request,id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        doc = blacklistedSaved.objects.get(user=data_new)
        return render(request, 'officer/blacklisted_gm_evaluate.html',{'data': doc,'h':data,'id':id})
    return redirect('/')


def blacklisted_gm_evaluate_save(request,id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        doc = blacklistedSaved.objects.filter(user=data_new)
        if request.method == 'POST':
            dd = request.POST.get('OK')
            if dd == 'OK':
                data = User_Registration.objects.filter(User_Id=id)
                data.update(blacklisted=2,work_approval=0,finance_approval=0,cgm_approval=0,digital_cert_upload=0,complete_data=2,Complete_Details=2)
                return render(request,'officer/cgm_blacklisted_pending.html')
        return render(request, 'officer/blacklisted_gm_evaluate.html',{'data': doc,'h':data})
    return redirect('/')

def blacklisted_gm_all(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(blacklisted=2, User_type='TKC',User_zone='WZ')
            data2 = blacklistedSaved.objects.filter(user_type = 'TKC')
            lst_oyt = []

            address = []
            
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)

            for j in data:
                add = UserCompanyDataMain.objects.get(user_id_id = j)
                address.append(add)
                print("ffffffffffffff",address)

    
            zip_data = zip(data,data2,address,lst_oyt)
            return render(request, 'officer/cgm_blacklisted_all.html',{'data': zip_data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(blacklisted=2, User_type='TKC',User_zone='CZ')
            data2 = blacklistedSaved.objects.filter(user_type = 'TKC')
            lst_oyt = []
            address = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)

            for j in data:
                add = UserCompanyDataMain.objects.get(user_id_id = j)
                address.append(add)
                print("ffffffffffffff",address)


            zip_data = zip(data,data2,address,lst_oyt)
            return render(request, 'officer/cgm_blacklisted_all.html',{'data': zip_data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(blacklisted=2, User_type='TKC',User_zone='EZ')
            data2 = blacklistedSaved.objects.filter(user_type = 'TKC')
            lst_oyt = []
            address = []
            for i in data:
                var_oyt = ""
                if i.Oyt == '9':
                    var_oyt = "TKC"
                elif i.Oyt == '8':
                    var_oyt = "A5"
                elif i.Oyt == '7':
                    var_oyt = "A4"
                elif i.Oyt == '6':
                    var_oyt = "A3"
                elif i.Oyt == '5':
                    var_oyt = "A2 (with OYT)"
                elif i.Oyt == '3':
                    var_oyt = "A1 (With OYT)"
                elif i.Oyt == '1':
                    var_oyt = "B"
                lst_oyt.append(var_oyt)

            for j in data:
                add = UserCompanyDataMain.objects.get(user_id_id = j)
                address.append(add)
                print("ffffffffffffff",address)

            zip_data = zip(data,data2,address,lst_oyt)
            return render(request, 'officer/cgm_blacklisted_all.html',{'data': zip_data})
    return redirect('/')


def blacklisted_gm_view(request,id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        doc = blacklistedSaved.objects.get(user=data_new)
        print("doc",doc)
        return render(request, 'officer/blacklisted_gm_view.html',{'data': doc})
    return redirect('/')




# *****************cgm


def blacklisted_cgm_vendor(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(blacklisted=1, User_type='VENDOR',User_zone='WZ')
            return render(request, 'officer/cgm_blacklisted_vendor_pending.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(blacklisted=1, User_type='VENDOR',User_zone='CZ')
            return render(request, 'officer/cgm_blacklisted_vendor_pending.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(blacklisted=1, User_type='VENDOR',User_zone='EZ')
            return render(request, 'officer/cgm_blacklisted_vendor_pending.html',{'data': data})
    return redirect('/')

def blacklisted_cgm_vendor_evaluate(request,id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        doc = blacklistedSaved.objects.get(user=data_new)
        return render(request, 'officer/blacklisted_cgm_evaluate_vendor_save.html',{'data': doc,'h':data,'id':id})
    return redirect('/')


def blacklisted_cgm_evaluate_vendor_save(request,id):
    if request.session.has_key('employ_login_id'):
        data = User_Registration.objects.filter(User_Id=id)
        data_new = User_Registration.objects.get(User_Id=id)
        doc = blacklistedSaved.objects.filter(user=data_new)
        if request.method == 'POST':
            dd = request.POST.get('OK')
            if dd == 'OK':
                data = User_Registration.objects.filter(User_Id=id)
                data.update(blacklisted=2,work_approval=0,finance_approval=0,cgm_approval=0,digital_cert_upload=0,complete_data=2,Complete_Details=2)
                return render(request,'officer/cgm_blacklisted_vendor_pending.html')
        return render(request, 'officer/blacklisted_cgm_evaluate_vendor_save.html',{'data': doc,'h':data})
    return redirect('/')


def blacklisted_cgm_all(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':

            data = User_Registration.objects.filter(blacklisted=2, User_type='VENDOR',User_zone='WZ')
            #data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
            data = blacklistedSaved.objects.filter(user = data)
            return render(request, 'officer/cgm_blacklisted_all_vendor.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(blacklisted=2, User_type='VENDOR',User_zone='CZ')
            #data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
            data = blacklistedSaved.objects.filter(user = data)
            return render(request, 'officer/cgm_blacklisted_all_vendor.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(blacklisted=2, User_type='VENDOR',User_zone='EZ')
            #data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
            data = blacklistedSaved.objects.filter(user = data)
            return render(request, 'officer/cgm_blacklisted_all_vendor.html',{'data': data})
    return redirect('/')







def blacklisted_gm_work_all(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            data = User_Registration.objects.filter(blacklisted=2,User_zone='WZ')
            data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
            return render(request, 'officer/dgm_work_blacklisted_all.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(blacklisted=2, User_zone='CZ')
            data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
            return render(request, 'officer/dgm_work_blacklisted_all.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(blacklisted=2, User_zone='EZ')
            data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
            return render(request, 'officer/dgm_work_blacklisted_all.html',{'data': data})
    return redirect('/')


def cgm_qc_complete_status_nabl(request):
    if request.session.has_key('employ_login_id'):
        alldata =  User_Registration.objects.filter(Complete_Details=1,qc_approval=0,User_type = 'NABL') | User_Registration.objects.filter(Complete_Details=1,qc_approval='-1',User_type = 'NABL') | User_Registration.objects.filter(Complete_Details=1,qc_approval=1,User_type = 'NABL') | User_Registration.objects.filter(Complete_Details=1,cgm_approval=1,User_type = 'NABL')
   
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        return render(request, 'officer/cgm_qc_complete_status_nabl.html', {'data': alldata})

    return redirect('/')

# def blacklisted_cgm_all(request):
#     if request.session.has_key('officer'):
#         if request.session['officer'] == 'WZ':

#             data = User_Registration.objects.filter(blacklisted=2, User_type='VENDOR',User_zone='WZ')
#             data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
#             return render(request, 'officer/cgm_blacklisted_all_vendor.html',{'data': data})

#         elif request.session['officer'] == 'CZ':
#             data = User_Registration.objects.filter(blacklisted=2, User_type='VENDOR',User_zone='CZ')
#             data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
#             return render(request, 'officer/cgm_blacklisted_all_vendor.html',{'data': data})

#         elif request.session['officer'] == 'EZ':
#             data = User_Registration.objects.filter(blacklisted=2, User_type='VENDOR',User_zone='EZ')
#             data = blacklistedSaved.objects.filter(user__CompanyName_E = data[0].CompanyName_E)
#             return render(request, 'officer/cgm_blacklisted_all_vendor.html',{'data': data})
#     return redirect('/')   


def sopinfo(request):
    return render(request,'main/sopinfo.html')

def officersop(request):
    return render(request,'main/officersop/officersop.html')

def work_order(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')
    
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    

    if officer.Circle != None:
       
        tag_circle_region=Tag_Circle.objects.filter(circle_id=officer.Circle).values()
        print(tag_circle_region,"bhopal id")#Wo of Bhopal region
        
        
        wo_id_list = []
        for each in tag_circle_region:
            work_order=each['wo_no_id']
            wo_id_list.append(work_order)
            

        wo_data = TKCWoInfo.objects.filter(id__in = wo_id_list)
        print(wo_data,"dataaaaaaaaa")
        return render(request, 'officer/pma_wo.html',
                        {"officer": officer, 'wo': wo, 'tkc_wo':wo_data})
    
    
    elif officer.Region != None:       
    
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        
        
        circle_region=Tag_Circle.objects.filter(region_id=officer.Region).values()
        print(circle_region,"bhopal id")#Wo of Bhopal region
        
        
        wo_id_list = []
        for each in circle_region:
            work_order=each['wo_no_id']
            wo_id_list.append(work_order)
            

        wo_data = TKCWoInfo.objects.filter(id__in = wo_id_list)
        print(wo_data,"dataaaaaaaaa")
        return render(request, 'officer/pma_wo.html',
                        {"officer": officer, 'wo': wo, 'tkc_wo':wo_data})
    
    elif officer.Circle and officer.Region == None:
        officer = Officer.objects.get(employ_id=request.session['employ_id'])
           
        wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, zone=officer.user_zone).order_by('-id')    
    return render(request, 'officer/pma_wo.html',
                  {"officer": officer, 'tkc_wo': wo})
        




def get_bank(request,user_id):
    officer = Officer.objects.get(employ_id=request.session['employ_id'])  
    user_data = User_Registration.objects.get(User_Id= user_id)    
    bank_detail=BankDetails.objects.filter(user_id=user_data.ContactNo) 
    print(bank_detail,"bank_dataaaaaaaaaaaaaa")   
    return render(request, 'officer/bank_view.html', {"data": bank_detail})



def get_bg(request,wo_id):
    
    officer = Officer.objects.get(employ_id=request.session['employ_id'])  
    wo = TKCWoInfo.objects.get(id=wo_id)
    
    bg_detail=TKCWoInfo_Bg.objects.filter(TKCWoInfo=wo)
    return render(request, 'officer/bg_view.html', {"data": bg_detail})



def get_pert(request,wo_id):
   
    officer = Officer.objects.get(employ_id=request.session['employ_id'])  
    wo = TKCWoInfo.objects.get(id=wo_id)
    
    
    pert_detail=TKCWoInfo_Pert.objects.filter(TKCWoInfo=wo)
    
    return render(request, 'officer/pert_view.html', {"data": pert_detail})



def get_loc(request,wo_id):
    
   
    officer = Officer.objects.get(employ_id=request.session['employ_id'])  
    wo = TKCWoInfo.objects.get(id=wo_id)
    print(wo,"wooooooooooo")
    
    loc_detail = TKCWoInfo_LOC.objects.filter(TKCWoInfo=wo)
    
    return render(request, 'officer/loc_view.html', {"data": loc_detail})


def get_vendor(request,wo_id):
   
    officer = Officer.objects.get(employ_id=request.session['employ_id'])  
    wo = TKCWoInfo.objects.get(id=wo_id)
    print(wo,"wooooooooooo")
    
    vendor_detail=TKCVendor.objects.filter(TKCWoInfo=wo)
    print(vendor_detail,"--------------")
    return render(request, 'officer/vendor.html', {"data": vendor_detail})



def nabl_status_check(request):
    search_post = request.GET.get('search')
    material = request.GET.get('material')
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()

    if search_post =="All":
        data = User_Registration.objects.filter(User_type='NABL',Complete_Details='1',cgm_approval=1,digital_cert_upload=1)
       

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
        return render(request, 'main/all_nabl_details.html', {'data':data,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})

    if search_post:
        data = User_Registration.objects.filter(Q(User_type='NABL',Complete_Details='1',cgm_approval=1,digital_cert_upload=1) & Q(User_zone__icontains=search_post))
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
        return render(request, 'main/all_nabl_details.html', {'data':data,'to_daaa':to_daaa,'today':today,'final_lst':final_lst})
   
    
   
    return render(request, 'main/all_nabl_details.html',{'today':today})



def nabl_check_material(request,id):
    data = User_Registration.objects.get(User_Id = id)
    material = NABL_Registration_Test.objects.filter(user_id = data.User_Id)
    list_data = []
    for i in material:
        list_data.append(i.Material_Specification_Name)
    return render(request, 'main/view_nabl_material.html', {'data':list_data,'id':id}) 



def remove_vendor_material_new(request,id):
    print("uuuuuuuuoooooooo")
    if request.method == 'POST':
        print("tytytytytytyieiteiueiu")
        data = Vendor_Material_Details.objects.get(id=id)
        user = data.user_id.User_Id
        data.DGM_remark = request.POST.get('remark_cgm')
        data.Primary_verification_Status = 0
        data.Status = 0
        data.save()
        return redirect('/vendor_cgm_evaluate_new/' + str(user))
    return render(request, 'officer/vendor_cgm_evaluate_new.html')


def approved_vendor_list_discom(request):
    data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',cgm_approval=1,digital_cert_upload=1,blacklisted=0)
    lst_oyt = []
    address = []
    for i in data:
        cert = certificate_details.objects.filter(User_Id = i.User_Id).last()
        lst_oyt.append(cert)
    
    for j in data:
        add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
        address.append(add)

    final_lst = zip(data,lst_oyt,address)
    return render(request, 'officer/all_vendor_details_discom.html', {'data':data,'final_lst':final_lst})
   
    
   
def vendor_check_material_discom(request,id):
    data = User_Registration.objects.get(User_Id = id)
    material = Vendor_Material_Details.objects.filter(user_id = data,new_status=1)
    list_data = []
    for i in material:
        list_data.append(i.Material_Name)

    if request.method =="POST":
        get_data_value= request.POST.get('get_data_value')
        value_data = Vendor_Material_Details.objects.filter(user_id = data,Material_Name=get_data_value,new_status=1)
        return render(request, 'officer/vendor_all_material_discom.html', {'data':value_data}) 
    return render(request, 'officer/view_vendor_material_discom.html', {'data':set(list_data),'id':id})   


def vendor_basic_details_discom(request,id):
    data_new = User_Registration.objects.get(User_Id = id)
    CompanyData1 = UserCompanyDataMain.objects.get(user_id_id=data_new)
    AuthorisedPerson1 = AuthorisedPerson.objects.get(user_id_id=data_new)
    #BankDetails1 = BankDetails.objects.get(user_id=data[0].ContactNo)
    doc = Vendor_Document.objects.filter(user_id=data_new.User_Id)
    doc1 = Vendor_BalanceSheet.objects.filter(user_id=data_new.User_Id)
    fac = Vendor_Factory_Details.objects.filter(user_id=data_new.User_Id)
    fac_image = Vendor_Factory_image.objects.filter(Factory=fac[0])
    Material = Vendor_Material_Details.objects.filter(user_id=data_new.User_Id,Primary_verification_Status=1)
    tech_data = Vendor_Technical_Details.objects.filter(user_id=data_new.User_Id)
    vendor = User_Registration.objects.get(User_Id=id)
    apprisal = []
    fi_tech = []
    if FI_Appraisal_Details.objects.filter(vendor=vendor).exists():
        apprisal = FI_Appraisal_Details.objects.get(vendor=vendor)
        fi_tech = Factory_Technical_Details.objects.filter(vendor=vendor).last()
    return render(request, 'officer/vendor_basic_details_discom_user.html',
                {'data': data_new, 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
                'tech_data': tech_data, 
                 'CompanyData': CompanyData1,
                'AuthorisedPerson1': AuthorisedPerson1,
                #'BankDetails': BankDetails1, 'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech,
                'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech,
                'fac_image': fac_image})



from datetime import datetime
def active_inactive_contractor_list_dgm_work(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Authentication_id__isnull=False)).order_by('CompanyName_E')
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
    to_daaa =datetime.datetime.today()
    return render(request, 'officer/active_inactive_contractor_list_dgm_work.html', {'data':data,'officer':officer,'contractor':contractor_class,'doc':doc,'to_daaa':to_daaa,'today':today})

from datetime import datetime
def active_inactive_contractor_list_dgm_finance(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Authentication_id__isnull=False)).order_by('CompanyName_E')
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
    to_daaa =datetime.datetime.today()
    return render(request, 'officer/active_inactive_contractor_list_dgm_finance.html', {'data':data,'officer':officer,'contractor':contractor_class,'doc':doc,'to_daaa':to_daaa,'today':today})


def new_dashboard(request):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC').distinct('user__CompanyName_E')
    
    return render(request, 'officer/new_dashboard_data.html',{'con':contractor})


def new_dashboard_history(request,name):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC',user__CompanyName_E=name).order_by('date')
    return render(request, 'officer/new_dashboard_data_history.html',{'con':contractor})



from datetime import datetime
def active_inactive_contractor_list_auditor(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()
    data = User_Registration.objects.filter(Q(User_type='TKC',Complete_Details='1',complete_data=1,cgm_approval=1)|Q(User_type='TKC',Authentication_id__isnull=False)).order_by('CompanyName_E')
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.filter(Types_of_Docs='Electrical License',new_data = 0)
    to_daaa =datetime.datetime.today()
    return render(request, 'officer/active_inactive_contractor_list_auditor.html', {'data':data,'officer':officer,'contractor':contractor_class,'doc':doc,'to_daaa':to_daaa,'today':today})


def contractor_view_details_auditor(request, id):
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
                return render(request, 'officer/contractor_view_details_auditor.html',
                            {'data': data[0],'officer':officer,'doc': doc, 'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})

            elif doc[0].new_data == 0:
                return render(request, 'officer/contractor_view_details_auditor.html',
                            {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})


    return redirect('/')


def all_vendor_wo_creater(request):
    search_post = request.GET.get('search')
    if search_post:
        data = User_Registration.objects.filter(Q(User_type='VENDOR',complete_data='1',Complete_Details='1') & Q(CompanyName_E__icontains=search_post))
    else:
        data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',complete_data=1)
    return render(request,'officer/all_vendor_data_wo_create.html',{'data':data})


def all_vendor_wo_creater_document(request,id):
    data = User_Registration.objects.get(User_Id=id)
    doc = Vendor_Document.objects.filter(user_id=data.User_Id)
    fac = Vendor_Factory_Details.objects.filter(user_id=data.User_Id)
    balance = Vendor_BalanceSheet.objects.filter(user_id=data.User_Id)
    material = Vendor_Material_Details.objects.filter(user_id=data.User_Id)   
    add_data = UserCompanyDataMain.objects.get(user_id_id=data)
    if BankDetails.objects.filter(user_id=data.ContactNo).exists():
        bank_details = BankDetails.objects.get(user_id=data.ContactNo)
        return render(request, 'officer/all_vendor_document_wo_create.html',{'data':data,'doc':doc,'add_data':add_data,'bank_details':bank_details,'fac':fac,'balance':balance,'material':material})
    else:
        return render(request, 'officer/all_vendor_document_wo_create.html',{'data':data,'doc':doc,'add_data':add_data,'fac':fac,'balance':balance,'material':material})





def all_contractor_wo_creater(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    alldata =  User_Registration.objects.filter(Complete_Details=1,User_type='TKC',complete_data=1)
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.all()
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    return render(request, 'officer/all_contractor_wo_creater.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})




def all_vendor_wo_approver(request):
    search_post = request.GET.get('search')
    if search_post:
        data = User_Registration.objects.filter(Q(User_type='VENDOR',complete_data='1',Complete_Details='1') & Q(CompanyName_E__icontains=search_post))
    else:
        data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',complete_data=1)
    return render(request,'officer/all_vendor_data_wo_approver.html',{'data':data})


def all_vendor_wo_approver_document(request,id):
    data = User_Registration.objects.get(User_Id=id)
    doc = Vendor_Document.objects.filter(user_id=data.User_Id)
    fac = Vendor_Factory_Details.objects.filter(user_id=data.User_Id)
    balance = Vendor_BalanceSheet.objects.filter(user_id=data.User_Id)
    material = Vendor_Material_Details.objects.filter(user_id=data.User_Id)   
    add_data = UserCompanyDataMain.objects.get(user_id_id=data)
    if BankDetails.objects.filter(user_id=data.ContactNo).exists():
        bank_details = BankDetails.objects.get(user_id=data.ContactNo)
        return render(request, 'officer/all_vendor_document_wo_approver.html',{'data':data,'doc':doc,'add_data':add_data,'bank_details':bank_details,'fac':fac,'balance':balance,'material':material})
    else:
        return render(request, 'officer/all_vendor_document_wo_approver.html',{'data':data,'doc':doc,'add_data':add_data,'fac':fac,'balance':balance,'material':material})





def all_contractor_wo_approver(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    alldata =  User_Registration.objects.filter(Complete_Details=1,User_type='TKC',complete_data=1)
    contractor_class = TKC_Payment.objects.all()
    doc = TKC_Document.objects.all()
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    return render(request, 'officer/all_contractor_wo_approver.html', {'data': alldata,'contractor':contractor_class,'doc':doc,'officer':officer})


# PDI new code according to offer(multiple)

def pdi_pending_assign(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    wo_approved = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status=1,PDI_Assign=0,wo__zone=officer_zone,is_pdi_required=True).order_by('offer_no', 'PDI_Assign_At').distinct('offer_no')
    wo=[]
    va=[]
    
    
    # wo_id_list = []
    # for each in wo:
    #     work_order=each.wo_id
    #     wo_id_list.append(work_order)            
    for i in wo_approved:
        offer_approved=offer_material_site_stores.objects.filter(offer_no=i.offer_no)
        # print(len(offer_approved))
        c=0
        for j in offer_approved:
            if j.Material_Offer_Submit_Approved_Status == 1 or j.Material_Offer_Submit_Approved_Status == -1 :
                
                c=c+1
        if len(offer_approved) == c:
            # print("######",i)
            venor_add=UserCompanyDataMain.objects.get(user_id_id=i.TKCVendor.Vendor)
            # print("#####",venor_add.Company_add_1)
            va.append(venor_add)
            wo.append(i)
    wo_id_list = []
    for each in wo:
        work_order=each.wo_id
        wo_id_list.append(work_order)            

    
    return render(request, 'officer/pending_pdi_assign.html',
                  {"officer": officer,'list': wo})




def view_offer(request,offer_no):
    offer=offer_material_site_stores.objects.filter(offer_no=offer_no,Material_Offer_Submit_Approved_Status=1,is_pdi_required=True)
    
    qun_list = []
    total_qun = []
    item_code_list  = []

    for j in offer:
        item_code_list.append(j.wo_material.item_code)

    if(len(set(item_code_list))!=len(item_code_list)):
        new_obj = offer.distinct('wo_material__item_code')
        for i in new_obj:
            offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code =i.wo_material.item_code,Material_Offer_Submit_Approved_Status=1,is_pdi_required=True)
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
    return render(request,'officer/view_offer.html',{"offer":final_data})



def new_pdi_assign(request,offer_no):
    
    offer=offer_material_site_stores.objects.filter(offer_no=offer_no,is_pdi_required=True).distinct('offer_no')   
    wo_id_list = []
    for each in offer:
        work_order=each.wo_id
     
        wo_id_list.append(work_order)
        
    
    wo_data = TKCWoInfo.objects.filter(id__in = wo_id_list) 
 
    address_data=[]
    for each in offer:        
        vendor_id=each.TKCVendor_id
    
        offer_no=each.offer_no
        tkc_vendor=TKCVendor.objects.filter(id=vendor_id)
        for each in tkc_vendor:
            tkc_vendor_id=each.Vendor_id
            user_reg=User_Registration.objects.filter(User_Id=tkc_vendor_id)
            for each in user_reg:
                v_id=each.User_Id
                address_data=UserCompanyDataMain.objects.filter(user_id_id=v_id)
                
    
    wo_id_data = []
    officer_list=[]
    officer_designation=[]
    officer_mobile=[]
    for each in offer:
        work_order=each.wo_id
        wo_id_data.append(work_order)            

    inspecting_officer=InspectingOfficerInfo.objects.all()
   
    material_data = offer_material_site_stores.objects.filter(offer_no=offer_no)
    return render(request,'officer/new_pdi_assign.html',
    {"offer":offer,"inspecting_officer":inspecting_officer,"wo_data":wo_data,"officer_list":officer_list,"officer_designation":officer_designation,"officer_mobile":officer_mobile,"address_data":address_data,"offer_no":offer_no})

def pdi_add_data(request,offer_no):
    login_officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    pdi_offer_data_exist = PDI_Inspection_Info.objects.filter(offer_no = offer_no)
    if len(pdi_offer_data_exist) > 0:
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        officer_zone = officer.Discom.Discom_Code
        pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone).distinct('offer_no')
        vendor_address=[]
        for i in pdi_assign:
            address=UserCompanyDataMain.objects.get(user_id_id=i.Material.TKCVendor.Vendor_id)
            vendor_add=str(address.Company_add_1) + " "+ str(address.Company_add_2)  + " "+str(address.Company_dist) +" " + str(address.Company_state)+ " "+str(address.Company_pin_code)
            vendor_address.append(vendor_add)
        zip_data=zip(pdi_assign,vendor_address)
        return render(request,'officer/all_pdi_assigned.html',{"pdi_assign":zip_data,"msg1":f'you have already assigned the pdi for offer no. {offer_no}'})
       
    wo = offer_material_site_stores.objects.filter(offer_no=offer_no,is_pdi_required=True).distinct('offer_no')
    for j in wo:
        wo_data = TKCWoInfo.objects.get(id = j.wo.id)
    officer=request.POST.get('Officer')
    offc=InspectingOfficerInfo.objects.get(id=officer)
    officer_contact_no = offc.contact_no
    officer_name = offc.officer_name
    officer_login_id = offc.officer_employ_id
    officer_password = offc.officer_password



    from datetime import date
    today = date.today()
   
    inspection_date=request.POST.get('date')
    try:
        officer1=request.POST.get('another_officer')
        offc1=InspectingOfficerInfo.objects.get(id=officer1)   
    except:
        offc1 = None

    offer=offer_material_site_stores.objects.filter(offer_no=offer_no,Material_Offer_Submit_Approved_Status = 1,is_pdi_required = True)

    qun_list = []
    total_qun = []
    item_code_list  = []

    for j in offer:
        item_code_list.append(j.wo_material.item_code)

    if(len(set(item_code_list))!=len(item_code_list)):
        pdi_obj_lst=[]
        new_obj = offer.distinct('wo_material__item_code')
        for i in new_obj:
            offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code =i.wo_material.item_code,Material_Offer_Submit_Approved_Status = 1)
            for k in offer_material:
                qun_list.append(k.quantity)
            qty_sum = sum(qun_list)
            total_qun.append(qty_sum)
            qun_list.clear()
            vendor_add = UserCompanyDataMain.objects.get(user_id_id=i.TKCVendor.Vendor)
            vendor_full_add=str(vendor_add.Company_add_1)+str(vendor_add.Company_add_2)+str(vendor_add.Company_pin_code)+str(vendor_add.Company_dist)+str(vendor_add.Company_state)+str(vendor_add.Company_city)
            tkc_add = UserCompanyDataMain.objects.get(user_id_id=i.supplier)
            pdi_data=PDI_Inspection_Info(officer=offc,another_officer=offc1,tkc_address=tkc_add.Company_add_1,Material=i,inspection_date=inspection_date,offer_no=offer_no,
            offer_date=i.TKCVendor.TKCVendor_Submit_At,wo=wo_data,vendor_address=vendor_full_add,tkc_name=i.supplier.CompanyName_E,vendor_name=i.TKCVendor.Vendor.CompanyName_E,
            material_name=k.wo_material.material_name,item_code=k.wo_material.item_code,quantity = qty_sum,assign_date=today)
            pdi_obj_lst.append(pdi_data)
            pdi_data.save()
            
            for each in offer_material:
                each.PDI_Assign=1
                each.PDI_Assign_By = login_officer.employ_name
                each.PDI_Assign_At = today
                each.PDI =  pdi_data           
                each.save()
            vendor_company = i.TKCVendor.Vendor.CompanyName_E
            vendor_contact = i.TKCVendor.Vendor.ContactNo
            wo_discom = i.wo.zone


        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        offer_string = offer_no
        offer_no_trim = offer_string[-29:]
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007826634677201491&mobile_number=" + str(
                        officer_contact_no) + "&v1=" + str(officer_name) + "&v2=" + str() + "&v3=" + str('pre delivery inspection') + "&v4=" + str(vendor_company) + "&v5=" + str() + "&v6=" + str('offer') + "&v7=" + str(offer_no_trim) + "&v8=" + str(inspection_date) + "&v9=" + str(officer_login_id) + "&v10=" + str(officer_password) + "&v11=" + str('https://shorturl.at/jkyJ8') + "&v12=" + str()+ "&v13=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

        # if another_officer is not None:
        #     url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007637441628723739&mobile_number=" + str(
        #                     another_officer_mobile) + "&v1=" + str(anoher_officer_name) + "&v2=" + str() + "&v3=" + str(c_name) + "&v4=" + str() + "&v5=" + str() + "&v6=" + str() + "&v7=" + str() + "&v8=" + str(date) + "&v9=" + str() + "&v10=" + str() + "&v11=" + str('https://qcportal.mpcz.in/media/apk/FactoryInspection.apk') + "&v12=" + str()
        #     response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

        # else:
        #     pass
        
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007697261728783071&mobile_number=" + str(
                        vendor_contact) + "&v1=" + str(vendor_company) + "&v2=" + str() + "&v3=" + str('materials/items') + "&v4=" + str('offer') + "&v5=" + str(offer_no)+ "&v6=" + str(wo_discom)+ "&v7=" + str(inspection_date)+ "&v8=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

    else:
        pdi_obj_lst=[]
        for j in offer:
            vendor_add = UserCompanyDataMain.objects.get(user_id_id=j.TKCVendor.Vendor)
            vendor_full_add=str(vendor_add.Company_add_1)+str(vendor_add.Company_add_2)+str(vendor_add.Company_pin_code)+str(vendor_add.Company_dist)+str(vendor_add.Company_state)+str(vendor_add.Company_city)
            tkc_add = UserCompanyDataMain.objects.get(user_id_id=j.supplier)
            pdi_data=PDI_Inspection_Info(officer=offc,another_officer=offc1,tkc_address=tkc_add.Company_add_1,Material=j,inspection_date=inspection_date,offer_no=offer_no,
            offer_date=j.TKCVendor.TKCVendor_Submit_At,wo=wo_data,vendor_address=vendor_full_add,tkc_name=j.supplier.CompanyName_E,vendor_name=j.TKCVendor.Vendor.CompanyName_E,
            material_name=j.wo_material.material_name,item_code=j.wo_material.item_code,quantity = j.quantity,assign_date=today)
            pdi_obj_lst.append(pdi_data)
            pdi_data.save()
            j.PDI_Assign=1
            j.PDI_Assign_By = login_officer.employ_name
            j.PDI_Assign_At = today
            j.PDI =  pdi_data           
            j.save()
            vendor_company = j.TKCVendor.Vendor.CompanyName_E
            vendor_contact = j.TKCVendor.Vendor.ContactNo
            wo_discom = j.wo.zone
        

        new_obj = offer
        for i in offer:
            total_qun.append(i.quantity)
        
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        offer_string = offer_no
        offer_no_trim = offer_string[-29:]
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007826634677201491&mobile_number=" + str(
                        officer_contact_no) + "&v1=" + str(officer_name) + "&v2=" + str() + "&v3=" + str('pre delivery inspection') + "&v4=" + str(vendor_company) + "&v5=" + str() + "&v6=" + str('offer') + "&v7=" + str(offer_no_trim) + "&v8=" + str(inspection_date) + "&v9=" + str(officer_login_id) + "&v10=" + str(officer_password) + "&v11=" + str('https://shorturl.at/jkyJ8') + "&v12=" + str()+ "&v13=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

        # if another_officer is not None:
        #     url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007637441628723739&mobile_number=" + str(
        #                     another_officer_mobile) + "&v1=" + str(anoher_officer_name) + "&v2=" + str() + "&v3=" + str(c_name) + "&v4=" + str() + "&v5=" + str() + "&v6=" + str() + "&v7=" + str() + "&v8=" + str(date) + "&v9=" + str() + "&v10=" + str() + "&v11=" + str('https://qcportal.mpcz.in/media/apk/FactoryInspection.apk') + "&v12=" + str()
        #     response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

        # else:
        #     pass
        
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007697261728783071&mobile_number=" + str(
                        vendor_contact) + "&v1=" + str(vendor_company) + "&v2=" + str() + "&v3=" + str('materials/items') + "&v4=" + str('offer') + "&v5=" + str(offer_no)+ "&v6=" + str(wo_discom)+ "&v7=" + str(inspection_date)+ "&v8=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                
    zippedList = zip(new_obj, total_qun)
    pdi_all_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    
    
    
    return render(request,'officer/pdi_index.html',
    {"wo_data":wo_data,"pdi_all_data":pdi_all_data,"wo":wo,"today":today,"officer":offc,"offc1":offc1,"address_data":vendor_add,"zippedList":zippedList,"inspection_date":inspection_date,"offer_no":offer_no})

# reassign for inspecting officer
def update_pdi_assign(request,offer_no):
    offer=offer_material_site_stores.objects.filter(offer_no=offer_no).exclude(is_pdi_required=False).distinct('offer_no')   
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign_1=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=0,Material__PDI_Complete=1,Material__Material_Offer_Submit_Approved_Status=1,offer_no=offer_no)
    if len(pdi_assign_1)>0:
        # pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone).distinct('offer_no')
        messages.warning(request, 'Inspecting officer partial inspection completed')
        return redirect('all_pdi_assigned_data_cgm')
    offer=offer_material_site_stores.objects.filter(offer_no=offer_no).exclude(is_pdi_required=False).distinct('offer_no')   
    wo_id_list = []
    for each in offer:
        work_order=each.wo_id
     
        wo_id_list.append(work_order)
        
    
    wo_data = TKCWoInfo.objects.filter(id__in = wo_id_list) 
 
    address_data=[]
    for each in offer:        
        vendor_id=each.TKCVendor_id
    
        offer_no=each.offer_no
        tkc_vendor=TKCVendor.objects.filter(id=vendor_id)
        for each in tkc_vendor:
            tkc_vendor_id=each.Vendor_id
            user_reg=User_Registration.objects.filter(User_Id=tkc_vendor_id)
            for each in user_reg:
                v_id=each.User_Id
                address_data=UserCompanyDataMain.objects.filter(user_id_id=v_id)
                
    
    wo_id_data = []
    officer_list=[]
    officer_designation=[]
    officer_mobile=[]
    for each in offer:
        work_order=each.wo_id
        wo_id_data.append(work_order)            

    inspecting_officer=InspectingOfficerInfo.objects.all()
   
    # material_data = offer_material_site_stores.objects.filter(offer_no=offer_no)
  
    return render(request,'officer/update_pdi_assign.html',
    {"offer":offer,"inspecting_officer":inspecting_officer,"wo_data":wo_data,"officer_list":officer_list,"officer_designation":officer_designation,"officer_mobile":officer_mobile,"address_data":address_data,"offer_no":offer_no})


# update_data in PDI_Inspection_Info model in main inspecting officer and inspection date

def pdi_update_data(request,offer_no):
    wo = offer_material_site_stores.objects.filter(offer_no=offer_no).exclude(is_pdi_required=False).distinct('offer_no')
    for j in wo:
        wo_data = TKCWoInfo.objects.get(id = j.wo.id)
    officer=request.POST.get('Officer')
    offc=InspectingOfficerInfo.objects.get(id=officer)
    officer_contact_no = offc.contact_no
    officer_name = offc.officer_name
    officer_login_id = offc.officer_employ_id
    officer_password = offc.officer_password



    from datetime import date
    today = date.today()
   
    inspection_date=request.POST.get('date')
    try:
        officer1=request.POST.get('another_officer')
        offc1=InspectingOfficerInfo.objects.get(id=officer1)   
    except:
        offc1 = None

    offer=offer_material_site_stores.objects.filter(offer_no=offer_no,Material_Offer_Submit_Approved_Status = 1).exclude(is_pdi_required=False)

    qun_list = []
    total_qun = []
    item_code_list  = []

    for j in offer:
        item_code_list.append(j.wo_material.item_code)
    
    if(len(set(item_code_list))!=len(item_code_list)):
        

        new_obj = offer.distinct('wo_material__item_code')
        for i in new_obj:
            offer_material = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code =i.wo_material.item_code,Material_Offer_Submit_Approved_Status = 1).exclude(is_pdi_required=False)
            for k in offer_material:
                qun_list.append(k.quantity)
            qty_sum = sum(qun_list)
            total_qun.append(qty_sum)
            qun_list.clear()
            vendor_add = UserCompanyDataMain.objects.get(user_id_id=i.TKCVendor.Vendor)
            vendor_full_add=str(vendor_add.Company_add_1)+str(vendor_add.Company_add_2)+str(vendor_add.Company_pin_code)+str(vendor_add.Company_dist)+str(vendor_add.Company_state)+str(vendor_add.Company_city)
            tkc_add = UserCompanyDataMain.objects.get(user_id_id=i.supplier)
            pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)
            print("#####",pdi_data)
            for p in pdi_data:
                p.officer=offc
                p.another_officer=offc1
                p.inspection_date=inspection_date
                p.assign_date=today
                p.save()
            vendor_company = i.TKCVendor.Vendor.CompanyName_E
            vendor_contact = i.TKCVendor.Vendor.ContactNo
            wo_discom = i.wo.zone


        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        offer_string = offer_no
        offer_no_trim = offer_string[-29:]
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007826634677201491&mobile_number=" + str(
                        officer_contact_no) + "&v1=" + str(officer_name) + "&v2=" + str() + "&v3=" + str('pre delivery inspection') + "&v4=" + str(vendor_company) + "&v5=" + str() + "&v6=" + str('offer') + "&v7=" + str(offer_no_trim) + "&v8=" + str(inspection_date) + "&v9=" + str(officer_login_id) + "&v10=" + str(officer_password) + "&v11=" + str('https://shorturl.at/jkyJ8') + "&v12=" + str()+ "&v13=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007697261728783071&mobile_number=" + str(
                        vendor_contact) + "&v1=" + str(vendor_company) + "&v2=" + str() + "&v3=" + str('materials/items') + "&v4=" + str('offer') + "&v5=" + str(offer_no)+ "&v6=" + str(wo_discom)+ "&v7=" + str(inspection_date)+ "&v8=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
    else:

        for j in offer:
            vendor_add = UserCompanyDataMain.objects.get(user_id_id=j.TKCVendor.Vendor)
            vendor_full_add=str(vendor_add.Company_add_1)+str(vendor_add.Company_add_2)+str(vendor_add.Company_pin_code)+str(vendor_add.Company_dist)+str(vendor_add.Company_state)+str(vendor_add.Company_city)
            tkc_add = UserCompanyDataMain.objects.get(user_id_id=j.supplier)
            pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)
            print("#####",pdi_data)
            for l in pdi_data:
                l.officer=offc
                l.another_officer=offc1
                l.inspection_date=inspection_date
                l.assign_date=today
                l.save()
                
            vendor_company = j.TKCVendor.Vendor.CompanyName_E
            vendor_contact = j.TKCVendor.Vendor.ContactNo
            wo_discom = j.wo.zone

        new_obj = offer
        for i in offer:
            total_qun.append(i.quantity)
        
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        offer_string = offer_no
        offer_no_trim = offer_string[-29:]
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007826634677201491&mobile_number=" + str(
                        officer_contact_no) + "&v1=" + str(officer_name) + "&v2=" + str() + "&v3=" + str('pre delivery inspection') + "&v4=" + str(vendor_company) + "&v5=" + str() + "&v6=" + str('offer') + "&v7=" + str(offer_no_trim) + "&v8=" + str(inspection_date) + "&v9=" + str(officer_login_id) + "&v10=" + str(officer_password) + "&v11=" + str('https://shorturl.at/jkyJ8') + "&v12=" + str()+ "&v13=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

        
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007697261728783071&mobile_number=" + str(
                        vendor_contact) + "&v1=" + str(vendor_company) + "&v2=" + str() + "&v3=" + str('materials/items') + "&v4=" + str('offer') + "&v5=" + str(offer_no)+ "&v6=" + str(wo_discom)+ "&v7=" + str(inspection_date)+ "&v8=" + str('PDI')
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
                
    zippedList = zip(new_obj, total_qun)
    pdi_all_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    
    
    
    return render(request,'officer/pdi_index.html',
    {"wo_data":wo_data,"pdi_all_data":pdi_all_data,"wo":wo,"today":today,"officer":offc,"offc1":offc1,"address_data":vendor_add,"zippedList":zippedList,"inspection_date":inspection_date,"offer_no":offer_no})
    
#pending pdi acceptance 
def pending_pdi_acceptance(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign_1=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=0,Material__PDI_Complete=1,Material__Material_Offer_Submit_Approved_Status=1).distinct('offer_no')
    pdi_assign=[]
    for i in pdi_assign_1:
        offer_approved=offer_material_site_stores.objects.filter(offer_no=i.offer_no,Material_Offer_Submit_Approved_Status=1,is_pdi_required=True)
        print(len(offer_approved))
        c=0
        a=0
        for j in offer_approved:
            if j.Material_Offer_Submit_Approved_Status == 1:
                
                c=c+1
            if j.PDI_Complete == 1:
                a=a+1
            
        
        if a == c:
            pdi_assign.append(i)
        
    return render(request,'officer/pending_pdi_acceptance.html',{"pdi_assign":pdi_assign})


def pending_pdi_acceptance_data(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign_1=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=0,Material__PDI_Complete=1,Material__Material_Offer_Submit_Approved_Status=1,pdi_report__isnull = True).order_by('offer_no', 'offer_date').distinct('offer_no')
    pdi_assign=[]
    for i in pdi_assign_1:
        offer_approved=offer_material_site_stores.objects.filter(offer_no=i.offer_no,Material_Offer_Submit_Approved_Status=1,is_pdi_required=True)
        print(len(offer_approved))
        c=0
        a=0
        for j in offer_approved:
            if j.Material_Offer_Submit_Approved_Status == 1:
                
                c=c+1
            if j.PDI_Complete == 1:
                a=a+1
            
        
        if a == c:
            pdi_assign.append(i)
        
    return render(request,'officer/pending_pdi_acceptance.html',{"pdi_assign":pdi_assign})



def rejected_pdi(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=-1,Material__PDI_Complete=1).distinct('offer_no')
    return render(request,'officer/rejected_pdi.html',{"pdi_assign":pdi_assign})

# show Fake call Pdi's
def fake_call_pdi(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=-2,Material__PDI_Complete=1).distinct('offer_no')
    return render(request,'officer/fakecall_pdi.html',{"pdi_assign":pdi_assign})





def all_pdi_assigned_data(request,offer_no):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__Material_Offer_Submit_Approved_Status = 1).exclude(Material__is_pdi_required=False).distinct('offer_no')
    
    pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)

    if request.method == "POST":
        pdi_file = request.FILES['pdi_report']
        for i in pdi_data:   
            i.letter_report=pdi_file             
            i.save()
    vendor_address=[]
    for i in pdi_assign:
        address=UserCompanyDataMain.objects.get(user_id_id=i.Material.TKCVendor.Vendor_id)
        vendor_add=str(address.Company_add_1) + " "+ str(address.Company_add_2)  + " "+str(address.Company_dist) +" " + str(address.Company_state)+ " "+str(address.Company_pin_code)
        vendor_address.append(vendor_add)
    zip_data=zip(pdi_assign,vendor_address)
    return render(request,'officer/all_pdi_assigned.html',{"pdi_assign":zip_data})

def all_pdi_assigned_data_cgm(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__Material_Offer_Submit_Approved_Status = 1).exclude(Material__is_pdi_required=False).distinct('offer_no')
    vendor_address=[]
    for i in pdi_assign:
        address=UserCompanyDataMain.objects.get(user_id_id=i.Material.TKCVendor.Vendor_id)
        vendor_add=str(address.Company_add_1) + " "+ str(address.Company_add_2)  + " "+str(address.Company_dist) +" " + str(address.Company_state)+ " "+str(address.Company_pin_code)
        vendor_address.append(vendor_add)
    zip_data=zip(pdi_assign,vendor_address)
    return render(request,'officer/all_pdi_assigned.html',{"pdi_assign":zip_data})




def all_pdi_assigned(request,offer_no):# All PDI Assigned
    
    #officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])    
    wo = PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    
    
  
    
    # wo_id_list = []
    # for each in wo:
    #     offer_no=each.offer_no
    #     work_order=each.wo_id
    #     wo_id_list.append(work_order)            

    # wo_data = TKCWoInfo.objects.filter(id__in = wo_id_list)
    # # zippedList = zip(wo, wo_data)   

    # pdi_file = request.FILES['pdi_report']
    # pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)[0]
   
    # pdi_data.pdi_uploaded_document=pdi_file
    
    
    # pdi_data.save()
    pdi_file = request.FILES['pdi_report']                   
    pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    
    for i in pdi_data:   
        i.letter_report=pdi_file   
                         
        i.save()
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,PDI_Complete=1)    
    
    offer_mat_len= len(offer_material)<1 #If this variable true then print validation
   
    return render(request,'officer/pdi_assigned.html',{"list": wo,"offer_mat_len":offer_mat_len})


def pdi_inspection_data(request,item_code,offer_no):
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code=item_code)
    for each in offer_material:
        id=each.id
        flag=each.PDI_Approved_Status
        
    pdi=PDI_Inspection_Info.objects.filter(offer_no=offer_no,item_code=item_code).distinct('offer_no')
    for each in pdi:
        task_id=each.offer_no
        material_id  = each.Material
  
    representative_data=Pdi_Inspection_Representive_data.objects.filter(task__offer_no=task_id)
    pdi_images = PDI_Factory_image.objects.filter(Offer_Material=material_id)
    
    return render(request,'officer/pdi_view.html',{"representative_data":representative_data,"item_code":item_code,"list": offer_material,"pdi":pdi,"flag":flag,"offer_no":offer_no,"pdi_images":pdi_images})
    
def pdi_against_wo(request,offer_no):
    data1 = PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    unique_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    for i in unique_data:
        offer_no=i.offer_no 
    return render(request, 'officer/vendor_factory_inspection_assined_pdi.html', {'data1': data1,'unique_data':unique_data,'offer_no':offer_no})

def submit_button(request,offer_no):
    data1 = PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    for i in data1:
        i.pdi_cgm_status=1
        i.save()
    wo = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status=1).distinct('offer_no')
    return render(request, 'officer/pending_pdi_assign.html',{'list': wo})


def pdi_view(request,id):
    if request.session.has_key('officer'):
        offer = offer_material_site_stores.objects.get(id = id)
        pdi_images = PDI_Factory_image.objects.filter(Offer_Material=offer)
        pdi_representative_data = Pdi_Inspection_Representive_data.objects.filter(task__offer_no =offer.offer_no)
        return render(request, 'officer/pdi_view.html', {'offer': offer,'pdi_images':pdi_images,'representative_data':pdi_representative_data})
    return redirect('/')

    
import datetime
def pdi_accept(request,offer_no):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    # offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,PDI__item_code=item_code)
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no).exclude(is_pdi_required=False)
    pdi=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    for i in offer_material:
        i.PDI_Approved_Status=1
        i.PDI_Approved_At=datetime.datetime.now().date()
        i.PDI_Approved_By = officer.employ_name            
        i.save()
        flag=i.PDI_Approved_Status
        id=i.id
        offer=i.offer_no
    factory_image=PDI_Factory_image.objects.filter(Offer_Material=id) 
    
  
    representative_data=Pdi_Inspection_Representive_data.objects.filter(task__offer_no=offer)
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone).distinct('offer_no')
    vendor_address=[]
    for i in pdi_assign:
        address=UserCompanyDataMain.objects.get(user_id_id=i.Material.TKCVendor.Vendor_id)
        vendor_add=str(address.Company_add_1) + " "+ str(address.Company_add_2)  + " "+str(address.Company_dist) +" " + str(address.Company_state)+ " "+str(address.Company_pin_code)
        vendor_address.append(vendor_add)
    zip_data=zip(pdi_assign,vendor_address)
    return render(request,'officer/all_pdi_assigned.html',{"pdi_assign":zip_data})
    
  
       
    # return render(request,'officer/pdi_view.html',{"list": offer_material,"pdi":pdi,"pdi_images":factory_image,"flag":flag,"offer_no":offer_no,"offer":offer_material,'representative_data':representative_data})
            
   
    
    


def pdi_reject(request,offer_no):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no).exclude(is_pdi_required=False)
    pdi=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')  
    for i in offer_material:
        i.PDI_Approved_Status=-1
        wo_qty=tkc_wo_items_boq.objects.get(id=i.wo_material.id)
        wo_qty.balance_qty=float(wo_qty.balance_qty) + float(i.quantity)
        wo_qty.save()
        i.PDI_Approved_At=datetime.datetime.now().date()
        i.PDI_Approved_By = officer.employ_name            
        i.save()
        flag_value = i.PDI_Approved_Status
        flag=flag_value
        id=i.id
    factory_image=PDI_Factory_image.objects.filter(Offer_Material=id) 
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone).distinct('offer_no')
    vendor_address=[]
    for i in pdi_assign:
        address=UserCompanyDataMain.objects.get(user_id_id=i.Material.TKCVendor.Vendor_id)
        vendor_add=str(address.Company_add_1) + " "+ str(address.Company_add_2)  + " "+str(address.Company_dist) +" " + str(address.Company_state)+ " "+str(address.Company_pin_code)
        vendor_address.append(vendor_add)
    zip_data=zip(pdi_assign,vendor_address)
    return render(request,'officer/all_pdi_assigned.html',{"pdi_assign":zip_data})   
                 
    # return render(request,'officer/pdi_view.html',{"list": offer_material,"pdi":pdi,"factory_image":factory_image,"flag":flag,"offer_no":offer_no,"offer":offer_material})

def fake_call(request,offer_no):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    # offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,PDI__item_code=item_code)
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no).exclude(is_pdi_required=False)
    pdi=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    
    
    import datetime 
    
    for i in offer_material:            
        i.PDI_Approved_Status=-2
        wo_qty=tkc_wo_items_boq.objects.get(id=i.wo_material.id)
        wo_qty.balance_qty=float(wo_qty.balance_qty) + float(i.quantity)
        wo_qty.save()
        i.PDI_Approved_At=datetime.date.today()
        i.PDI_Approved_By = officer.employ_name            
        i.save()
    # for each in offer_material:
    #     flag_value = each.PDI_Approved_Status
    #     flag=flag_value
    #     id=each.id
    #     print(id,"***********************")
    # factory_image=PDI_Factory_image.objects.filter(Offer_Material=id)
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone).distinct('offer_no')
    vendor_address=[]
    for i in pdi_assign:
        address=UserCompanyDataMain.objects.get(user_id_id=i.Material.TKCVendor.Vendor_id)
        vendor_add=str(address.Company_add_1) + " "+ str(address.Company_add_2)  + " "+str(address.Company_dist) +" " + str(address.Company_state)+ " "+str(address.Company_pin_code)
        vendor_address.append(vendor_add)
    zip_data=zip(pdi_assign,vendor_address)
    return render(request,'officer/all_pdi_assigned.html',{"pdi_assign":zip_data})     
                 
    # return render(request,'officer/pdi_view.html',{"list": offer_material,"pdi":pdi,"factory_image":factory_image,"flag":flag,"offer_no":offer_no,"offer":offer_material})


def pdi_officers_add(request,offer_no):
    officer_from = request.POST.get('officer_from')
    officer_name = request.POST.get('officer_name')
    officer_mobile_no = request.POST.get('officer_mobile_no')
    designation = request.POST.get('designation')
    data = pdi_other_officer(offer_no = offer_no, officer_name = officer_name,officer_contact = officer_mobile_no,officer_from = officer_from,officer_designation=designation,created_at = datetime.datetime.now())
    data.save()

    offer=offer_material_site_stores.objects.filter(offer_no=offer_no).distinct('offer_no')   
    wo_id_list = []
    for each in offer:
        work_order=each.wo_id
        wo_id_list.append(work_order)
    wo_data = TKCWoInfo.objects.filter(id__in = wo_id_list) 
    address_data=[]
    for each in offer:        
        vendor_id=each.TKCVendor_id
    
        offer_no=each.offer_no
        tkc_vendor=TKCVendor.objects.filter(id=vendor_id)
        for each in tkc_vendor:
            tkc_vendor_id=each.Vendor_id
            user_reg=User_Registration.objects.filter(User_Id=tkc_vendor_id)
            for each in user_reg:
                v_id=each.User_Id
                address_data=UserCompanyDataMain.objects.filter(user_id_id=v_id)
        
    wo_id_data = []
    officer_list=[]
    officer_designation=[]
    officer_mobile=[]
    for each in offer:
        work_order=each.wo_id
        wo_id_data.append(work_order)            

    inspecting_officer=InspectingOfficerInfo.objects.all()  
    return render(request,'officer/new_pdi_assign.html',
    {"offer":offer,"inspecting_officer":inspecting_officer,"wo_data":wo_data,"officer_list":officer_list,"officer_designation":officer_designation,"officer_mobile":officer_mobile,"address_data":address_data,"offer_no":offer_no})




def pdi(request,offer_no):
    pdi_file = request.FILES['pdi_report']                   
    pdi_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    
    for i in pdi_data:   
        i.pdi_report=pdi_file                       
        i.save()
    ins_officer = InspectingOfficerInfo.objects.get(officer_employ_id=request.session['employ_login_id'])
    officer_id=ins_officer.id
    pdi_data=PDI_Inspection_Info.objects.filter(officer=officer_id).distinct('offer_no')
    return render(request,"officer/inspection_officer.html",{"pdi_data":pdi_data,"officer":ins_officer})


def assigned_officer_pdi(request):
    ins_officer = InspectingOfficerInfo.objects.get(officer_employ_id=request.session['employ_login_id'])
    officer_id=ins_officer.id
    pdi_data=PDI_Inspection_Info.objects.filter(officer=officer_id).distinct('offer_no')
    return render(request, 'officer/inspection_officer.html', {'officer': ins_officer,"pdi_data":pdi_data}) 

def officer_view_inspection(request,offer_no):
    data1 = PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    unique_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,PDI_Approved_Status=1)
    offer_mat_len= len(offer_material)<1
    for i in unique_data:
        offer_no=i.offer_no 
    return render(request, 'officer/officer_view_inspection.html', {'data1': data1,'unique_data':unique_data,"offer_mat_len":offer_mat_len})

    #return render(request,'officer/officer_view_inspection.html',{"view_report":view_report,"unique_data":unique_data})

def inspection_data(request,offer_no,item_code):
    print("123456789")
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code=item_code)
    print(offer_material,"**************************")
    
    for each in offer_material:
        id=each.id
        flag=each.PDI_Approved_Status
        
    
   
    offr_no=offer_no
   
    pdi=PDI_Inspection_Info.objects.filter(offer_no=offer_no,item_code=item_code).distinct('offer_no')
    for each in pdi:
        task_id=each.offer_no
  
    representative_data=Pdi_Inspection_Representive_data.objects.filter(task__offer_no=task_id)

    factory_image=PDI_Factory_image.objects.filter(Offer_Material=id)    
    return render(request,'officer/inspection_data.html',{"representative_data":representative_data,"list": offer_material,"pdi":pdi,"factory_image":factory_image,"flag":flag,"offer_no":offr_no})

def contractor_document_view_wo_approver(request, id):
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
                return render(request, 'officer/contractor_document_view_wo_approver.html',
                            {'data': data[0],'officer':officer,'doc': doc, 'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})

            elif doc[0].new_data == 0:
                return render(request, 'officer/contractor_document_view_wo_approver.html',
                            {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})


    return redirect('/')


def contractor_document_view_wo_creater(request, id):
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
                return render(request, 'officer/contractor_document_view_wo_creater.html',
                            {'data': data[0],'officer':officer,'doc': doc, 'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})

            elif doc[0].new_data == 0:
                return render(request, 'officer/contractor_document_view_wo_creater.html',
                            {'data': data[0], 'doc': doc,'officer':officer ,'doc1': doc1, 'type': type, 'CompanyData': CompanyData1,'AuthorisedPerson1': AuthorisedPerson1})


    return redirect('/')



def wo_creater_view_reject_summary(request):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC').distinct('user__CompanyName_E')
    
    return render(request, 'officer/wo_creater_view_reject_summary_contractor.html',{'con':contractor})


def wo_creater_view_reject_summary_history(request,name):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC',user__CompanyName_E=name).order_by('date')
    payment_check = Payudata_main.objects.filter(User_Id__CompanyName_E=name,Payu_Status = 'success')
    for i in payment_check:     
        for j in contractor:  
            import datetime
            today = datetime.date.today()
            if  j.type == 'APPROVE' and j.officer == 'Shishir Gupta':
                print('jjjjj',j.date)
                print("ffffffffff",i.date)
    
    return render(request, 'officer/wo_creater_view_reject_summary_history.html',{'con':contractor})



def wo_approver_view_reject_summary(request):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC').distinct('user__CompanyName_E')
    
    return render(request, 'officer/wo_approver_view_reject_summary_contractor.html',{'con':contractor})


def wo_approver_view_reject_summary_history(request,name):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC',user__CompanyName_E=name).order_by('date')
    payment_check = Payudata_main.objects.filter(User_Id__CompanyName_E=name,Payu_Status = 'success')
    for i in payment_check:     
        for j in contractor:  
            import datetime
            today = datetime.date.today()
            if  j.type == 'APPROVE' and j.officer == 'Shishir Gupta':
                print('jjjjj',j.date)
    
    return render(request, 'officer/wo_approver_view_reject_summary_history.html',{'con':contractor})


def blacklisted_contractor_wo_creater(request):
    data = User_Registration.objects.filter(blacklisted=2)
    data2 = blacklistedSaved.objects.filter(user_type = 'TKC')\
    
    address = []

    for j in data:
        add = UserCompanyDataMain.objects.get(user_id_id = j)
        address.append(add)
    zip_data = zip(data,data2,address)
    return render(request, 'officer/blacklisted_contractor_wo_creater.html',{'data': zip_data})


def blacklisted_contractor_wo_approver(request):
    data = User_Registration.objects.filter(blacklisted=2)
    data2 = blacklistedSaved.objects.filter(user_type = 'TKC')\
    
    address = []

    for j in data:
        add = UserCompanyDataMain.objects.get(user_id_id = j)
        address.append(add)
    zip_data = zip(data,data2,address)
    return render(request, 'officer/blacklisted_contractor_wo_approver.html',{'data': zip_data})




# ********************************************************* BOQ Code ********************************************************

def pma_verify_boq_list(request):    
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1).order_by('-id')
    return render(request, 'officer/pma_verify_boq_list.html', {'officer': officer, 'wo':wo}) 

def pma_verify_boq(request, wo_id):     
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id']) 
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)    
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)     
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id, circles_name=officer_circle)             
    stored_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)
    wo = TKCWoInfo.objects.filter(id=wo_id)
    recommendation_data = ""    
      
    for i in stored_data:
        try:
            recommendation_data = i.pma_boq_recommendation
            if len(recommendation_data) !=0 :
                recommendation_data = i.pma_boq_recommendation
            else:
                recommendation_data = ""   
        except:
            recommendation_data = ""
         
    if len(stored_data) != 0 :    
        item_code_list = []
        item_dict = {}
        verified_item_qty = {}
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            verified_item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)
            for k in stored_item_data:
                item_qty_list.append(k.circle_quantity)
                verified_item_qty_list.append(k.verified_circle_qty)
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list   
            verified_item_qty[j]=verified_item_qty_list
    else:
        item_dict = 0 
        circle_list = 0       
        verified_item_qty = 0
        
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)     
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)
        
    for i in gm_status_data:
        gm_status = i.gm_status 
    gm_status = 0 
         
    return render(request, 'officer/pma_verify_boq_info.html', {'officer': officer, 'stored_data':stored_data, 'officer_circle':officer_circle, 'gm_status':gm_status, 'recommendation_data':recommendation_data, 'verified_item_qty':verified_item_qty, 'wo':wo, "requested_data":requested_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})  

@csrf_exempt
def pma_save_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)   
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)     
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id, circles_name=officer_circle)             
    stored_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)     
    
    if len(stored_data) != 0 :    
        item_code_list = []
        item_dict = {}
        verified_item_qty = {}
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            verified_item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)
            for k in stored_item_data:
                item_qty_list.append(k.circle_quantity)
                verified_item_qty_list.append(k.verified_circle_qty)
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list   
            verified_item_qty[j]=verified_item_qty_list
    else:
        item_dict = 0
        circle_list = 0
        verified_item_qty = 0
        
    recommendation_data = request.POST.get("recommendations")    
    
    data = tkc_update_boq.objects.filter(wo=wo_id,circles_name=officer_circle).update(pma_boq_recommendation= recommendation_data)
    
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)     
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)
    for i in gm_status_data:
        gm_status = i.gm_status  
        
    data = tkc_update_boq.objects.filter(wo=wo_id)
    for k in data:
        k.Officer_name = officer.employ_name
        k.updated_at = datetime.datetime.now()
        k.save()
    
    return render(request, 'officer/pma_verify_boq_info.html', {'officer': officer, 'stored_data':stored_data, 'officer_circle':officer_circle, 'gm_status':gm_status, 'recommendation_data':recommendation_data, 'verified_item_qty':verified_item_qty, 'wo':wo, "requested_data":requested_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})  

def pma_reject_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])  
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)            
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_instance = TKCWoInfo.objects.get(id=wo_id) 
            
    wo.gm_status= 2
    wo.save()
    
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)
    for i in gm_status_data:
        gm_status = i.gm_status
     
    mgs= "BOQ Quantity has been Rejected"
    return render(request, 'officer/pma_reject_boq.html', {'wo':wo, 'officer_circle':officer_circle, 'gm_status':gm_status,'officer': officer,  'wo':wo, 'mgs':mgs, 'wo_instance':wo_instance})  

@csrf_exempt
def pma_accept_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id']) 
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)     
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id, circles_name=officer_circle)             
    stored_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)  
    wo = TKCWoInfo.objects.filter(id=wo_id)
    for i in stored_data:
        recommendation_data = i.pma_boq_recommendation   
     
    for ver_qty in stored_data:
        if ver_qty.verified_circle_qty == 0:
            items_qty =0
        else:
            items_qty = -1
    if items_qty == 0:
        items_qty = 0
    else:
        items_qty = {}
        for i in stored_data:
            circle_stored_data = tkc_update_boq.objects.filter(wo=wo_id,item_code = i.item_code)
            item_qty_list=[]
            for j in circle_stored_data: 
                item_qty_list.append(j.circle_quantity)
                item_qty_list.append(j.verified_circle_qty) 
                item_qty_list.append(j.gm_verified_circle_qty)       
            items_qty[i.item_code]=item_qty_list 
    
    if len(stored_data) != 0 :    
        item_code_list = []
        item_dict = {}
        verified_item_qty = {}
        gm_verified_item_qty = {}
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            verified_item_qty_list = []
            gm_verified_item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)
            for k in stored_item_data:
                item_qty_list.append(k.circle_quantity)
                verified_item_qty_list.append(k.verified_circle_qty)
                gm_verified_item_qty_list.append(k.gm_verified_circle_qty)
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list   
            verified_item_qty[j]=verified_item_qty_list
            gm_verified_item_qty[j]= gm_verified_item_qty_list
    else:
        item_dict = 0 
        circle_list = 0       
        verified_item_qty = 0
        gm_verified_item_qty = 0  
       
    wo.pma_status= 1
    wo.save()
    
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)
    for i in gm_status_data:
        gm_status = i.gm_status         
    
    data = tkc_update_boq.objects.filter(wo=wo_id)
    for k in data:
        k.Officer_name = officer.employ_name
        k.updated_at = datetime.datetime.now()
        k.save()
              
    return render(request, 'officer/pma_accept_boq.html', {'officer': officer,'stored_data':stored_data, 'officer_circle':officer_circle, 'gm_status':gm_status,'recommendation_data':recommendation_data, 'stored_data':stored_data, 'gm_verified_item_qty':gm_verified_item_qty, 'wo':wo, "requested_data":requested_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})  


# verify boq GM
def gm_verify_boq_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    circle_qty_status  = 0
    stored_data = tkc_update_boq.objects.all()
    for i in stored_data:
        gm_status = i.gm_status
    
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1).order_by('-id')
    return render(request, 'officer/gm_verify_boq_list.html', {'officer': officer, 'gm_status':gm_status, 'wo':wo, 'circle_qty_status':circle_qty_status}) 
    
@csrf_exempt
def gm_verify_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)               
    circles = Tag_Circle.objects.filter(wo_no=wo_id)      
    wo_instance = TKCWoInfo.objects.get(id=wo_id)   
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)     
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id, circles_name=officer_circle)             
    stored_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle).order_by('-id')
    wo = TKCWoInfo.objects.filter(id=wo_id)
    
    if len(stored_data) == 0 : 
        recommendation_data = " "
        pma_remarks = " "
        
    
        
    try:
        
        for i in stored_data:
            recommendation_data = i.gm_boq_recommendation
            try:
                if len(recommendation_data) !=0 :
                    recommendation_data = i.gm_boq_recommendation
                else:
                    recommendation_data = " "
            except: 
                recommendation_data = " " 
    except:
        recommendation_data = " "
    
    
    items_qty = {}
    item_code_list = []    
    for i in stored_data:
        item_code_list.append(i.item_code)
    new_item_code_list = set(item_code_list)
    for j in new_item_code_list:
        gm_circle_list = []
        stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j, circles_name=officer_circle).order_by('-id')        
        for k in stored_item_data:
            gm_circle_list.append(k.gm_verified_circle_qty)            
        items_qty[j] = gm_circle_list 
    
        
    if len(stored_data) != 0 :    
        item_code_list = []
        item_dict = {}        
        for i in stored_data:
            print(i)
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []            
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j).order_by('-id')
            for k in stored_item_data:
                item_qty_list.append(k.circle_quantity)                
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list             
       
    else:
        item_dict = 0
        circle_list = 0
            
    for i in stored_data:
        pma_remarks = i.pma_boq_recommendation      
         
    return render(request, 'officer/gm_verify_boq_info.html', {'officer': officer, 'pma_remarks':pma_remarks, 'recommendation_data':recommendation_data, 'items_qty':items_qty, 'stored_data':stored_data, 'officer_circle':officer_circle, 'wo':wo, "requested_data":requested_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})  


@csrf_exempt
def gm_save_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)         
    circles = Tag_Circle.objects.filter(wo_no=wo_id)      
    wo_instance = TKCWoInfo.objects.filter(id=wo_id)   
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)   
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1)        
    
    stored_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle).order_by("id")
    for i in stored_data:
        i.gm_status = 1
        i.save()      
    
    gm_verified_circle_qty = {}
    item_qty_list=[]
      
    for i in boq_data:   
        item_name = i.item_code
        qty = request.POST.getlist(item_name)            
        item_qty_list.append(qty)
        for req in item_qty_list:
            list1 = []  
            for j in req:                
                data = tkc_update_boq.objects.get(wo=wo, item_code= item_name, circles_name= officer_circle) 
                data.gm_verified_circle_qty = j       
                data.save()                
                list1.append(data.circle_quantity)
                list1.append(float(j))
                gm_verified_circle_qty[item_name] = list1.copy()
                item_qty_list.clear()
                list1.clear()        
   
    items_qty = {}    
    for i in stored_data:
        item_name = i.item_code
        gm_circle_qty = request.POST.getlist(item_name)  
        items_qty[item_name] = gm_circle_qty 
        
    data = tkc_update_boq.objects.filter(wo=wo_id)
    for k in data:
        k.Officer_name = officer.employ_name
        k.updated_at = datetime.datetime.now()
        k.save()     
                
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1).order_by('-id')

    return render(request, 'officer/gm_verify_boq_list.html', {'wo':wo, 'officer':officer, 'items_qty':items_qty, 'stored_data':stored_data})  

@csrf_exempt
def gm_save_remarks(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)         
    circles = Tag_Circle.objects.filter(wo_no=wo_id)      
    wo_instance = TKCWoInfo.objects.filter(id=wo_id)   
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)   
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1)        
    
    stored_data = tkc_update_boq.objects.filter(wo=wo_id, circles_name=officer_circle)       
   
    items_qty = {}    
    for i in stored_data:
        item_name = i.item_code
        gm_circle_qty = request.POST.getlist(item_name)  
        items_qty[item_name] = gm_circle_qty 
    
    recommendation_data = request.POST.get("recommendations")    
    
    data = tkc_update_boq.objects.filter(wo=wo_id,circles_name=officer_circle).update(gm_boq_recommendation= recommendation_data)
          
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1).order_by('-id')

    return render(request, 'officer/gm_verify_boq_list.html', {'wo':wo, 'recommendation_data':recommendation_data, 'officer':officer, 'items_qty':items_qty, 'stored_data':stored_data})  



@csrf_exempt
def gm_verified_boq_data(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)
    wo_instance = TKCWoInfo.objects.get(id=wo_id) 
    stored_data = tkc_update_boq.objects.filter(wo=wo_id,circles_name=officer_circle)  
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1).order_by('-id')
    for i in stored_data:
        recommendation_data = i.gm_boq_recommendation
                 
    return render(request, 'officer/gm_edit_boq_data.html', {'wo':wo, 'recommendation_data':recommendation_data, 'officer': officer, 'wo_instance':wo_instance,'stored_data':stored_data, 'officer_circle':officer_circle,  'wo':wo})  

@csrf_exempt
def gm_save_new_data(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)
    wo_instance = TKCWoInfo.objects.get(id=wo_id) 
    stored_data = tkc_update_boq.objects.filter(wo=wo_id,circles_name=officer_circle)
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id, circles_name=officer_circle) 
   
    for i in requested_data:
        save_data = request.POST.get(i.item_code)    
        if save_data in validators.EMPTY_VALUES:
            save_data = None
        else:
            save_data = float(save_data)                            
        data = tkc_requested_boq_item.objects.get(wo=wo_instance, circle_qty=i.circle_qty, item_code= i.item_code, circles_name= i.circles_name)    
        print(data)
        data.gm_verified_circle_qty = save_data       
        data.save()
        
    for i in stored_data:
        recommendation_data = i.gm_boq_recommendation

    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1).order_by('-id')                
    return render(request, 'officer/gm_verify_boq_list.html', {'wo':wo, 'recommendation_data':recommendation_data, 'officer': officer, 'requested_data':requested_data, 'wo_instance':wo_instance,'stored_data':stored_data, 'officer_circle':officer_circle,  'wo':wo})  

 
def gm_reject_boq(request, wo_id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_circle = Circle_Master.objects.get(id = officer.Circle.id)         
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_instance = TKCWoInfo.objects.get(id=wo_id) 
    stored_circle_data = tkc_update_boq.objects.filter(wo=wo_id,circles_name=officer_circle)
    for i in stored_circle_data:
        i.gm_status = 2
        i.save()
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id)
    for j in gm_status_data:
        circle_qty_status  = j.gm_verified_status    
    
    mgs= "BOQ Quantity has been Rejected"
    return render(request, 'officer/gm_reject_boq.html', {'wo':wo, 'officer': officer,  'wo':wo, 'mgs':mgs, 'wo_instance':wo_instance})  



# ********************************************************* BOQ Code ********************************************************

from datetime import datetime
def tkc_registration(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    User_Zone = officer.user_zone
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.datetime.now()
    if request.method == "POST":
        firm_name = request.POST.get('firm_name')
        pancardno=request.POST.get('pancardno')
        pancardno1=request.FILES['pancardno1']
        gstno=request.POST.get('gstno')
        gstno1  = request.FILES['gstno1']
        gumastano = request.POST.get('gumastano')
        gumastano1 =  request.FILES['gumastano1']
        gumastadate = request.POST.get('gumastadate')
        address1 = request.POST.get('address1')
        address2 =  request.POST.get('address2')
        city = request.POST.get('city')
        district =  request.POST.get('district')
        state = request.POST.get('state')
        pin =  request.POST.get('pin')
        address11 = request.POST.get('address11')
        address22 = request.POST.get('address22')
        city2 = request.POST.get('city2')
        district2 = request.POST.get('district2')
        state2 = request.POST.get('state2')
        pin2 = request.POST.get('pin2')
        username = request.POST.get('username')
        mnumber =  request.POST.get('mnumber')
        emailid = request.POST.get('emailid')
        ownername = request.POST.get('ownername')
        acardnumber = request.POST.get('acardnumber')
        acardnumber1 = request.FILES['acardnumber1']
        mnumber1 = request.POST.get('mnumber1')
        address13 = request.POST.get('address13')
        address33 = request.POST.get('address33')
        city3 = request.POST.get('city3')
        district3 = request.POST.get('district3')
        state3 = request.POST.get('state3')
        pin3 = request.POST.get('pin3')

        licensenumber =  request.POST.get('licensenumber')
        licenseregdate = request.POST.get('licenseregdate')
        licenseexpdate = request.POST.get('licenseexpdate')
        licenseupload = request.FILES['licenseupload']
        contract_award = request.POST.get('contract_award')
        contract_award_file = request.FILES['contract_award_file']


        
        

        if User_Registration.objects.filter(ContactNo=mnumber,User_type='TKC').exists():
            messages.warning(request, "Mobile Number already registered")
            return render(request, 'fqp/wo_creater/register_tkc_contrator.html')


        else:

            user_details = User_Registration(User_type='TKC',CompanyName_E=firm_name, User_zone=User_Zone,
                                                        Authorised_person_E=username, ContactNo=mnumber,Email_Id=emailid,reg_date = today)
            
            user_details.save()
            data_new = User_Registration.objects.get(ContactNo=mnumber,User_type='TKC')
        if UserCompanyDataMain.objects.filter(Company_Pan_No=pancardno).exists() or UserCompanyDataMain.objects.filter(Company_Gst_No=gstno).exists():
            messages.warning(request, "PAN or GST already Exists")
            return render(request, 'fqp/wo_creater/register_tkc_contrator.html')
        else:
            company = UserCompanyDataMain(user_id_id=data_new,user_id=mnumber, CompanyName_E=firm_name,
                                                Company_Contact_No=mnumber,
                                                Company_Pan_No=pancardno,
                                                Company_Gumastha_No=gumastano, Company_Gst_No=gstno,
                                                Registration_Date=gumastadate, Company_add_1=address1,
                                                Company_add_2=address2, Company_pin_code=pin, Company_state=state,
                                                Company_dist=district, Company_city=city, Company_t_add_1=address11,
                                                Company_t_add_2=address22, Company_t_pin_code=pin2,
                                                Company_t_state=state2, Company_t_dist=district2, Company_t_city=city2)


        

            person = AuthorisedPerson(user_id_id = data_new,user_id=mnumber, Authorised_P_Name_E=ownername, 
                                        Authorised_P_Number=mnumber1, Authorised_P_Aadhar_No=acardnumber,
                                        Authorised_P_add_1=address13, Authorised_P_add_2=address33,
                                        Authorised_P_state=state3, Authorised_P_District=district3,
                                        Authorised_P_City=city3, Authorised_P_pin_code=pin3)
            

            data1 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='AADHAR CARD DETAILS',Document_Number=acardnumber, Ddocfile=acardnumber1)
            
            data2 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='GST',Document_Number=gstno, Ddocfile=gstno1)
            
            

            data5 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='Electrical License',
                                Document_Number=licensenumber, Ddocfile=licenseupload, Doc_issue_date=licenseregdate,
                                Doc_expiry_date=licenseexpdate)

            
            try:
                epfnumber = request.POST.get('epfnumber')
                epfupload = request.FILES['epfupload']
                
                data6 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='EPF With Challan',Document_Number=epfnumber, Ddocfile=epfupload)
            

            except Exception as e:
                data6 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='EPF With Challan')


            data11 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='PAN Card Number',Document_Number=pancardno, Ddocfile=pancardno1)


            try:
                esisnumber = request.POST.get('esisnumber')
                esiupload = request.FILES['esiupload']
                
                data7 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='ESIC Registration With Challan',Document_Number=esisnumber, Ddocfile=epfupload)
            
            except Exception as e:

                data7 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='ESIC Registration With Challan')


            data10 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='Gumasta/Firm Registration/DIC/MSME Certificate',Document_Number=gumastano, Ddocfile=gumastano1)
            


            try:
                supnumber = request.POST.get('supnumber')
                supnumner1 = request.FILES['supnumner1']
                data4 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='Declaration of Contractor and Supervisior',Document_Number=supnumber, Ddocfile=supnumner1)

            except Exception as e:
                data4 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='Declaration of Contractor and Supervisior')



            data12 = TKC_Document(user_id=data_new.User_Id, Types_of_Docs='Contract Award No. For Registration As TKC',
                                Document_Number=contract_award, Ddocfile=contract_award_file)

            

            
            if company and person and data1 and data2 and data4 and data5 and data6 and data7 and data10 and data11 and data12:
                person.save()
                company.save()
                data1.save()
                data2.save()
                data4.save()
                data5.save()
                data6.save()
                data7.save()
                data10.save()
                data11.save()
                data12.save()
                data_new.complete_data = 1
                data_new.Complete_Details = 1
                data_new.officer_create = 1
                data_new.Oyt = 9
                data_new.save()

                officer_table = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                officer_name = officer_table.employ_name
                offcier_designation = officer_table.designation
                summary = reject_and_approve_summary(user=data_new,type="Create",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
                summary.save()

                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007022255202070533&mobile_number=" + str(
                    mnumber) + "&v1=" + str(firm_name) + "&v2=" + str() + "&v3=" + "MP" + str(User_Zone) + "&v4=" + str(mnumber) + "&v5=" + str(
                    'https://qcportal.mpcz.in/')
                response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

                sms_template = message_template_log(template_id = '1007022255202070533',date = datetime.datetime.now(),mobile_number = mnumber)
                sms_template.save()
            return redirect('/tkc_registration_view')


    return render(request, 'fqp/wo_creater/register_tkc_contrator.html')


def tkc_registration_view(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            user =  User_Registration.objects.filter(officer_create = 1,User_zone='WZ') or User_Registration.objects.filter(officer_create = 2,User_zone='WZ')
            return render(request, 'fqp/wo_creater/register_tkc_contrator_view.html', {'user': user})  

        elif request.session['officer'] == 'EZ':
            user =  User_Registration.objects.filter(officer_create = 1,User_zone='EZ') or User_Registration.objects.filter(officer_create = 2,User_zone='EZ')
            return render(request, 'fqp/wo_creater/register_tkc_contrator_view.html', {'user': user})  

        elif request.session['officer'] == 'CZ':
            user =  User_Registration.objects.filter(officer_create = 1,User_zone='CZ') or User_Registration.objects.filter(officer_create = 2,User_zone='CZ')
            return render(request, 'fqp/wo_creater/register_tkc_contrator_view.html', {'user': user})  

    return redirect("/")



def tkc_registration_pending_approver(request):
    
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            user =  User_Registration.objects.filter(officer_create = 1,User_zone='WZ')
            return render(request, 'fqp/wo_approver/register_tkc_contrator_pending.html', {'user': user})

        elif request.session['officer'] == 'EZ':
            user =  User_Registration.objects.filter(officer_create = 1,User_zone='EZ')
            return render(request, 'fqp/wo_approver/register_tkc_contrator_pending.html', {'user': user})

        elif request.session['officer'] == 'CZ':
            user =  User_Registration.objects.filter(officer_create = 1,User_zone='CZ')
            return render(request, 'fqp/wo_approver/register_tkc_contrator_pending.html', {'user': user})

    return redirect("/")




def tkc_registration_approver_evaluate(request, id):
    user = User_Registration.objects.get(User_Id = id)
    address = UserCompanyDataMain.objects.get(user_id_id = user)
    auth = AuthorisedPerson.objects.get(user_id_id = user)
    doc = TKC_Document.objects.filter(user_id = user.User_Id,new_data = 1 )
    return render(request, 'fqp/wo_approver/register_tkc_contrator_evaluate.html', {'data': user, 'CompanyData':address, 'auth':auth,'doc':doc})  


import datetime
import calendar
def officer_otp_tkc(request, id, otp):
    data_usr_obj = User_Registration.objects.get(User_Id=id)
    if request.method == "POST":
        from datetime import date
        from datetime import time
        from datetime import datetime
        import datetime   
        data_usr_obj = User_Registration.objects.get(User_Id=id)
        User_Zone = data_usr_obj.User_zone
        date_save = datetime.datetime.now()
        data_usr_obj.date_of_approved = date_save
        data_usr_obj.save
        tkc_obj = 'TKC'
        Officer_obj = Officer.objects.get(mobile=request.session['officer_mobile'])
        cmobile = data_usr_obj.ContactNo
        UCDM_obj = UserCompanyDataMain.objects.get(user_id_id=data_usr_obj)
        officer_table = Officer.objects.get(mobile=request.session['officer_mobile'])
        officer_name = officer_table.employ_name
        offcier_designation = officer_table.designation
        summary = reject_and_approve_summary(user=data_usr_obj,type="APPROVE",date=datetime.datetime.now(),officer=officer_name,officer_designation=offcier_designation)
        summary.save()
        from datetime import date
        from datetime import time
        from datetime import datetime
        import datetime
        td = datetime.datetime.now()
        current_time = td.strftime("%H:%M:%S")
        company_name = data_usr_obj.CompanyName_E
        import calendar
        day = datetime.datetime.now().date()
        exp = TKC_Document.objects.get(user_id=data_usr_obj.User_Id, Types_of_Docs='Electrical License')
        expi_date = exp.Doc_expiry_date
        try:
            cert_det_obj = certificate_details.objects.get(User_Id=id)
            cert_det_obj.update(electic_liecense_date = expi_date)
        except Exception as e:
            pass 
        try:
            cert_det_obj.update(valid_upto = expi_date)
        except Exception as e:
            pass
        try:
            cert_det_obj.update(day = day)
        except Exception as e:
            pass
        try:
            cert_det_obj.update(current_time = current_time)
        except Exception as e:
            pass
        try:
            cert_det_obj.update(User_Zone = User_Zone)
        except Exception as e:
            pass
        try:
            #t1 = str(data_usr_obj.Authentication_id)
            #t2 = "CZC" + t1 
            cert_det_obj.update(no = data_usr_obj.Authentication_id)
        except Exception as e:
            pass
        data_usr_obj11 = User_Registration.objects.filter(User_Id=id)
        data_usr_obj11.update(upgrade = 0)
        data_usr_obj11.update(activation = 0)
        data_usr_obj11.update(digital_cert_upload = 0)
        data_usr_obj11.update(officer_create =  2)    
        data_usr_obj33 = User_Registration.objects.get(User_Id=id)
        data_usr_obj33.cgm_approval = 1 
        data_usr_obj33.save()   
        data_usr_obj22 = User_Registration.objects.get(User_Id=id)   
        usr_obj = User_Registration.objects.get(User_Id=id)  
        mat_list = []
        s = ""
        today = date.today()
        date = today.strftime("%m%y")
        list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if User_Zone == "CZ":
            st = s + User_Zone + 'C' + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
            if usr_obj.Authentication_id:
                st = usr_obj.Authentication_id
            else:    
                data_usr_obj11.update(Authentication_id=st)
                certificate_number = data_usr_obj.Authentication_id       
            if certificate_details.objects.filter(User_Id=id).exists():
                certificate_details_new = certificate_details.objects.filter(User_Id=id)
                certificate_details_new.update(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                    company_name=company_name,
                                                    Company_add_1=UCDM_obj.Company_add_1,
                                                    Company_add_2=UCDM_obj.Company_add_2,
                                                    Company_dist=UCDM_obj.Company_dist,
                                                    Company_state=UCDM_obj.Company_state,
                                                    Company_pin_code=UCDM_obj.Company_pin_code,
                                                    no = usr_obj.Authentication_id, User_type=usr_obj.User_type,
                                                    vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                    employ_name=Officer_obj.employ_name,
                                                    designation=Officer_obj.designation, current_time=current_time,
                                                    tkc_class_contractor=tkc_obj,
                                                    electic_liecense_date=expi_date, User_Zone=User_Zone)
                
            else:
                cert_obj = certificate_details(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                    company_name=company_name,
                                                    Company_add_1=UCDM_obj.Company_add_1,
                                                    Company_add_2=UCDM_obj.Company_add_2,
                                                    Company_dist=UCDM_obj.Company_dist,
                                                    Company_state=UCDM_obj.Company_state,
                                                    Company_pin_code=UCDM_obj.Company_pin_code,
                                                    no = st, User_type=usr_obj.User_type,
                                                    vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                    employ_name=Officer_obj.employ_name,
                                                    designation=Officer_obj.designation, current_time=current_time,
                                                    tkc_class_contractor=tkc_obj,
                                                    electic_liecense_date=expi_date, User_Zone=User_Zone)
                cert_obj.save()
                
            return render(request, 'tkc/tkc_cert_cz_tkc.html',
                                    {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': data_usr_obj22,
                                    'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data_usr_obj22,
                                    'company_name': data_usr_obj22.CompanyName_E, 'no': st, 
                                    'day': day, 'valid_upto': expi_date,
                                    'User_Zone': data_usr_obj22.User_zone})
        elif User_Zone == "EZ":
            st = s + User_Zone + 'C' + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
            if usr_obj.Authentication_id:
                st = usr_obj.Authentication_id
            else:    
                data_usr_obj11.update(Authentication_id=st)
                certificate_number = data_usr_obj.Authentication_id
            if certificate_details.objects.filter(User_Id=id).exists():
                certificate_details_new = certificate_details.objects.filter(User_Id=id)
                certificate_details_new.update(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                    company_name=company_name,
                                                    Company_add_1=UCDM_obj.Company_add_1,
                                                    Company_add_2=UCDM_obj.Company_add_2,
                                                    Company_dist=UCDM_obj.Company_dist,
                                                    Company_state=UCDM_obj.Company_state,
                                                    Company_pin_code=UCDM_obj.Company_pin_code,
                                                    no = usr_obj.Authentication_id, User_type=usr_obj.User_type,
                                                    vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                    employ_name=Officer_obj.employ_name,
                                                    designation=Officer_obj.designation, current_time=current_time,
                                                    tkc_class_contractor=tkc_obj,
                                                    electic_liecense_date=expi_date, User_Zone=User_Zone)
                
            else:
                cert_obj = certificate_details(User_Id=id,Authorised_person_E=usr_obj.Authorised_person_E,
                                                    company_name=company_name,
                                                    Company_add_1=UCDM_obj.Company_add_1,
                                                    Company_add_2=UCDM_obj.Company_add_2,
                                                    Company_dist=UCDM_obj.Company_dist,
                                                    Company_state=UCDM_obj.Company_state,
                                                    Company_pin_code=UCDM_obj.Company_pin_code,
                                                    no = st, User_type=usr_obj.User_type,
                                                    vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                    employ_name=Officer_obj.employ_name,
                                                    designation=Officer_obj.designation, current_time=current_time,
                                                    tkc_class_contractor=tkc_obj,
                                                    electic_liecense_date=expi_date, User_Zone=User_Zone)
                cert_obj.save()
                
            return render(request, 'tkc/tkc_cert_ez_tkc.html',
                                    {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': data_usr_obj22,
                                    'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data_usr_obj22,
                                    'company_name': data_usr_obj22.CompanyName_E, 'no': st, 
                                    'day': day, 'valid_upto': expi_date,
                                    'User_Zone': data_usr_obj22.User_zone})
        elif User_Zone == "WZ":
            st = s + User_Zone + 'C' + date + random.choice(list1) + random.choice(list1) + random.choice(
                            list1) + random.choice(list1)
            if usr_obj.Authentication_id:
                st = usr_obj.Authentication_id
            else:    
                data_usr_obj11.update(Authentication_id=st)
                certificate_number = data_usr_obj.Authentication_id
            if certificate_details.objects.filter(User_Id=id).exists():
                certificate_details_new = certificate_details.objects.filter(User_Id=id)
                certificate_details_new.update(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E,
                                                    company_name=company_name,
                                                    Company_add_1=UCDM_obj.Company_add_1,
                                                    Company_add_2=UCDM_obj.Company_add_2,
                                                    Company_dist=UCDM_obj.Company_dist,
                                                    Company_state=UCDM_obj.Company_state,
                                                    Company_pin_code=UCDM_obj.Company_pin_code,
                                                    no = usr_obj.Authentication_id, User_type=usr_obj.User_type,
                                                    vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                    employ_name=Officer_obj.employ_name,
                                                    designation=Officer_obj.designation, current_time=current_time,
                                                    tkc_class_contractor=tkc_obj,
                                                    electic_liecense_date=expi_date, User_Zone=User_Zone)
                
            else:
                cert_obj = certificate_details(User_Id=id, Authorised_person_E=usr_obj.Authorised_person_E,
                                                    company_name=company_name,
                                                    Company_add_1=UCDM_obj.Company_add_1,
                                                    Company_add_2=UCDM_obj.Company_add_2,
                                                    Company_dist=UCDM_obj.Company_dist,
                                                    Company_state=UCDM_obj.Company_state,
                                                    Company_pin_code=UCDM_obj.Company_pin_code,
                                                    no = st , User_type=usr_obj.User_type,
                                                    vmaterial=mat_list, day=day, valid_upto=expi_date,
                                                    employ_name=Officer_obj.employ_name,
                                                    designation=Officer_obj.designation, current_time=current_time,
                                                    tkc_class_contractor=tkc_obj,
                                                    electic_liecense_date=expi_date, User_Zone=User_Zone)
                cert_obj.save()
                
            return render(request, 'tkc/tkc_cert_wz_tkc.html',
                                    {'Authorised_person_E':usr_obj.Authorised_person_E,'tkc_obj': tkc_obj, 'Officer_obj': Officer_obj, 'usr_obj': data_usr_obj22,
                                    'UCDM_obj': UCDM_obj, 'current_time': current_time, 'data': data_usr_obj22,
                                    'company_name': data_usr_obj22.CompanyName_E, 'no': st, 
                                    'day': day, 'valid_upto': expi_date,
                                    'User_Zone': data_usr_obj22.User_zone})



    return render(request, 'main/officer_otp_new_tkc.html', {'id': id, 'otp': otp,'data_usr_obj':data_usr_obj})    





def uplaod_cert_new_tkc(request, no):
    usr_obj1 = User_Registration.objects.get(Authentication_id=no)
    if request.method == "POST":
        if request.FILES['digitalCert']:
            filename = request.FILES['digitalCert']  
            cert_det_obj = certificate_details.objects.get(no=no)
            usr_obj = User_Registration.objects.get(Authentication_id=no)
            cert_det_obj.image = filename
            cert_det_obj.save()
            usr_obj.digital_cert_upload=1
            usr_obj.cert_image = filename
            usr_obj.save()
        return redirect('/digital_sign_cert_new_tkc/TKC')
    else:
        return redirect('/digital_sign_cert_new_tkc/TKC')



def digital_sign_cert_new_tkc(request, user_type):
    if request.session.has_key('zone'):
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        user_type = 'TKC'
        if request.session['zone'] == 'WZ':
            usr_obj = User_Registration.objects.filter(officer_create=2,digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='WZ')
            return render(request, 'officer/digital_sign_cert_new_tkc.html', {'usr_obj':usr_obj,'officer':officer})
        elif request.session['zone'] == 'CZ':
            usr_obj = User_Registration.objects.filter(officer_create = 2,digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='CZ')
            print("tttttttttttt",usr_obj)
            return render(request, 'officer/digital_sign_cert_new_tkc.html', {'usr_obj':usr_obj,'officer':officer})
        elif request.session['zone'] == 'EZ':
            usr_obj = User_Registration.objects.filter(officer_create=2,digital_cert_upload = 0, cgm_approval = 1, User_type=user_type,User_zone='EZ')
            return render(request, 'officer/digital_sign_cert_new_tkc.html', {'usr_obj':usr_obj,'officer':officer})         
    else:
        return redirect('/')



def cert_upload_download_new_tkc(request, id):
    var_show = "1"
    x1 = [""]
    usr_obj = User_Registration.objects.get(User_Id = id)
    cert_u_obj = certificate_details.objects.get(User_Id=id)
    return render(request, 'officer/certificate_upload_download_new_tkc.html', {'vmat':x1,'cert_u_obj':cert_u_obj, 'var_show':var_show})
       


def tkc_registration_view_approver(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':
            user =  User_Registration.objects.filter(officer_create = 2,digital_cert_upload=1,User_zone='WZ')
            return render(request, 'fqp/wo_approver/register_tkc_approved_list.html', {'user': user})

        elif request.session['officer'] == 'EZ':
            user =  User_Registration.objects.filter(officer_create = 2,digital_cert_upload=1,User_zone='EZ')
            return render(request, 'fqp/wo_approver/register_tkc_approved_list.html', {'user': user}) 

        elif request.session['officer'] == 'CZ':
            user =  User_Registration.objects.filter(officer_create = 2,digital_cert_upload=1,User_zone='CZ')
            return render(request, 'fqp/wo_approver/register_tkc_approved_list.html', {'user': user})  

    return redirect("/")



def contractor_approvel_history_gm_works(request):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC').distinct('user__CompanyName_E')
    return render(request, 'officer/contractor_approvel_history_gm_works.html',{'con':contractor})


def contractor_approvel_history_gm_works_check(request,name):
    contractor = reject_and_approve_summary.objects.filter(user__User_type = 'TKC',user__CompanyName_E=name)
    return render(request, 'officer/contractor_approvel_history_gm_works_check.html',{'con':contractor})



def gm_works_vendor_complete_status(request):
    if request.session.has_key('employ_login_id'):
        alldata =  User_Registration.objects.filter(Complete_Details=1,finance_approval=0,User_type = 'VENDOR') | User_Registration.objects.filter(Complete_Details=1,work_approval=0,User_type = 'VENDOR') | User_Registration.objects.filter(Complete_Details=1,finance_approval=2,User_type = 'VENDOR') | User_Registration.objects.filter(Complete_Details=1,work_approval=2,User_type = 'VENDOR') | User_Registration.objects.filter(Complete_Details=1,work_approval=1,finance_approval=1,cgm_approval = 0,User_type = 'VENDOR')
        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
        return render(request, 'officer/gm_works_vendor_complete_status.html', {'data': alldata,'officer':officer})
    return redirect('/')



#Added by Aayush Joshi:
def data_push_in_erp_api_call(request,id,discom_name):
    print("discom_name",discom_name)
    print("in data_push_in_erp_api_call")
    usr_obj = User_Registration.objects.get(User_Id=id,cgm_approval=1,digital_cert_upload=1)
    com_obj = UserCompanyDataMain.objects.get(user_id_id=usr_obj.User_Id)
    if discom_name == 'WZ':
        URL=const.register_vendor_sit_wz
        data = {
            "register_vendor": {
                "@xmlns": "http://xmlns.oracle.com/apps/ap/rest/QC_PORTAL_REGISTER_VENDOR/register_vendor/",
                "RESTHeader": {
                    "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
                    "Responsibility": "JAI_PAYABLES",
                    "RespApplication": "JA",
                    "SecurityGroup": "STANDARD",
                    "NLSLanguage": "AMERICAN",
                    "Org_Id": "82"
                },
                "InputParameters": {
                    "P_PORTAL_VENDOR_NUMBER": usr_obj.Authentication_id,
                    "P_VENDOR_NAME": usr_obj.CompanyName_E,
                    "P_VENDOR_TYPE": usr_obj.User_type,
                    "P_ENABLED_FLAG": "Y",
                    "P_PAN_NUMBER": com_obj.Company_Pan_No,
                    "P_SITES" : {
                        "P_SITES_ITEM": [
                            {
                                "SITE_CODE":com_obj.Company_dist,
                                "CURRENCY": "INR",
                                "ADDRESS1": com_obj.Company_add_1,
                                "ADDRESS2": com_obj.Company_add_2,
                                "ADDRESS3": '',
                                "CITY": com_obj.Company_dist,
                                "STATE": com_obj.Company_state,
                                "PIN": com_obj.Company_pin_code,
                                "EMAIL_ADDRESS":usr_obj.Email_Id,
                                "ENABLED_FLAG": "Y",
                                "BANK": "",
                                "IFSC_CODE": "",
                                "BANK_BRANCH": "",
                                "BRANCH_ADDRESS": "",
                                "ACCOUNT_NUMBER": "",
                                "GST_NUMBER": com_obj.Company_Gst_No,
                            }
                        ]
                    }
                }
            }
        }
        # print("data----->",data)
    elif discom_name =='CZ':

        URL=const.register_vendor_sit_cz
        data={
        "register_vendor": {
            "@xmlns": "http://xmlns.oracle.com/apps/ap/rest/qc_vendor_registration/register_vendor/",
            "RESTHeader": {
                "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
                "Responsibility": "JAI_PAYABLES",
                "RespApplication": "JA",
                "SecurityGroup": "STANDARD",
                "NLSLanguage": "AMERICAN",
                "Org_Id": "82"
            },
            "InputParameters": {
                "P_PORTAL_VENDOR_NUMBER": usr_obj.Authentication_id,
                "P_VENDOR_NAME": usr_obj.CompanyName_E,
                "P_VENDOR_TYPE": usr_obj.User_type,
                "P_ENABLED_FLAG": "Y",
                "P_PAN_NUMBER": com_obj.Company_Pan_No,
                "PI_SITES": {
                    "PI_SITES_ITEM": [
                        {
                            "SITE_CODE": com_obj.Company_dist,
                            "CURRENCY": "INR",
                            "ADDRESS1": com_obj.Company_add_1,
                            "ADDRESS2": com_obj.Company_add_2,
                            "ADDRESS3": "",
                            "CITY": com_obj.Company_dist,
                            "STATE": com_obj.Company_state,
                            "PIN": com_obj.Company_pin_code,
                            "EMAIL_ADDRESS": usr_obj.Email_Id,
                            "ENABLED_FLAG": "Y",
                            "BANK": "",
                            "IFSC_CODE": "",
                            "BANK_BRANCH": "",
                            "BRANCH_ADDRESS": "",
                            "ACCOUNT_NUMBER": "",
                            "GST_NUMBER": com_obj.Company_Gst_No
                        }
                    ]
                }
            }
        }
    }
    elif discom_name =='EZ':
        # return HttpResponse("Sorry But API is Not given AS of Now for Register Vendor API for EZ")
        #currently storing data of EZ into CZ as EZ API of Register Vendor is Not Available
        URL=const.register_vendor_sit_cz
        data={
        "register_vendor": {
            "@xmlns": "http://xmlns.oracle.com/apps/ap/rest/qc_vendor_registration/register_vendor/",
            "RESTHeader": {
                "xmlns": "http://xmlns.oracle.com/apps/fnd/rest/header",
                "Responsibility": "JAI_PAYABLES",
                "RespApplication": "JA",
                "SecurityGroup": "STANDARD",
                "NLSLanguage": "AMERICAN",
                "Org_Id": "82"
            },
            "InputParameters": {
                "P_PORTAL_VENDOR_NUMBER": usr_obj.Authentication_id,
                "P_VENDOR_NAME": usr_obj.CompanyName_E,
                "P_VENDOR_TYPE": usr_obj.User_type,
                "P_ENABLED_FLAG": "Y",
                "P_PAN_NUMBER": com_obj.Company_Pan_No,
                "PI_SITES": {
                    "PI_SITES_ITEM": [
                        {
                            "SITE_CODE": com_obj.Company_dist,
                            "CURRENCY": "INR",
                            "ADDRESS1": com_obj.Company_add_1,
                            "ADDRESS2": com_obj.Company_add_2,
                            "ADDRESS3": "",
                            "CITY": com_obj.Company_dist,
                            "STATE": com_obj.Company_state,
                            "PIN": com_obj.Company_pin_code,
                            "EMAIL_ADDRESS": usr_obj.Email_Id,
                            "ENABLED_FLAG": "Y",
                            "BANK": "",
                            "IFSC_CODE": "",
                            "BANK_BRANCH": "",
                            "BRANCH_ADDRESS": "",
                            "ACCOUNT_NUMBER": "",
                            "GST_NUMBER": com_obj.Company_Gst_No
                        }
                    ]
                }
            }
        }
    }
    
    json_data = json.dumps(data)
    auth_values = HTTPBasicAuth(const.Username, const.Password)
    
    try:
        #calling API here with all the payload and endpoint details.
        res = req.post(url=URL, auth=auth_values, headers=const.headers, data=json_data)        
        if res.status_code == 200:
            print("code matched")
            error_in_response,bool_val=vendor_data_registration_in_erp(request,res,id)
            if bool_val == False:
                
                #api_status_flag,is_data_pushed,is_data_failed_pushed,res_data
                return True,False,True,error_in_response
            
            elif bool_val == True:
                # api_status_flag,is_data_pushed,is_data_failed_pushed,res_data
                return True,True,False,error_in_response
            
        else:
            # print("in else : api code 400,500,404 etc.")
            error_in_response,bool_val=vendor_data_registration_in_erp(request,res,id)
            # api_status_flag,is_data_pushed,is_data_failed_pushed,res_data
            return True,False,True,error_in_response
        
    except Exception as e:
        error_in_response ="API IS NOT RESPONDING..... "
        # return render(request, 'main/error_page.html')
        # api_status_flag,is_data_pushed,is_data_failed_pushed,res_data
        return False,False,True,error_in_response


def vendor_data_registration_in_erp(request,res,id):
    data = res.json()
    # print("dddddddddd--->",data['OutputParameters'])
    
    if 'ISGServiceFault' in data:
        error_in_response = data['ISGServiceFault']['Message']
        return error_in_response,False

    elif data['OutputParameters']['P_ERRORS'] :
        if data['OutputParameters']['P_ERRORS']['P_ERRORS_ITEM'] !=None:    
            error_in_response=data['OutputParameters']['P_ERRORS']['P_ERRORS_ITEM'][0]['ERROR_MESSAGE']
            return error_in_response,False
    
    else:
        # pushing data in erp. 
        data = res.json()
        response_output_params = data['OutputParameters']
        usr_obj=User_Registration.objects.get(User_Id=id,cgm_approval=1,digital_cert_upload=1)

        try:
            if response_output_params['P_VENDOR_ID']['P_VENDOR_ID_ITEM'][0]['VENDOR_ID']:
                usr_obj.erp_cz_id = response_output_params['P_VENDOR_ID']['P_VENDOR_ID_ITEM'][0]['VENDOR_ID'] 
                usr_obj.is_erp_pushed =True
                usr_obj.save()
        except:
            if response_output_params['P_VENDOR_ID']:
                usr_obj.erp_wz_id = response_output_params['P_VENDOR_ID']    
                usr_obj.is_erp_pushed =True
                usr_obj.save()

        print("-------Data pushed in erp successfully")            
        #"Data pushed in erp successfully"
        return False,True

    
    


def day_wise_count_tkc(request):
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    today = datetime.date.today()
    # contractor = reject_and_approve_summary.objects.filter(Q(user__User_type = 'VENDOR',user__finance_approval=0,user__complete_data=1) | Q(user__complete_data=1,user__User_type = 'VENDOR',user__work_approval=0))
    contractor = User_Registration.objects.filter(Q(User_zone='CZ',User_type = 'VENDOR',finance_approval=0,complete_data=1) | Q(User_zone='CZ',complete_data=1,User_type = 'VENDOR',work_approval=0))
    dgm_days = []

    for j in contractor:
        if not j.reg_date:
            dgm_days.append(4)
        
        else:
            p_days = today-j.reg_date
            dgm_days.append(p_days.days)
    new_data = zip(contractor,dgm_days)
    return render(request, 'officer/day_wise_count_tkc.html',{'con':contractor,'today':today,'new_data':new_data})


def new_dashboard_history_vendor(request,name):
    user_new = User_Registration.objects.get(CompanyName_E=name,User_zone='CZ',User_type = 'VENDOR',complete_data=1)
    contractor = reject_and_approve_summary.objects.filter(user=user_new.User_Id)
    return render(request, 'officer/new_dashboard_data_history_vendor.html',{'con':contractor}) 


def gtp_drawing_auditor_dashboard(request):
    gtp = TKCVendor.objects.filter(TKCWoInfo__zone='CZ').distinct('TKCWoInfo__Contract_Number')
    return render(request, 'officer/new_dashboard_data_gtp_data.html',{'gtp':gtp})


def view_gtp_wo_wise(request,id):
    gtp = TKCVendor.objects.filter(TKCWoInfo__id=id)
    return render(request, 'officer/view_gtp_wo_wise.html',{'gtp':gtp})

def wo_view_cgm(request, id):
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
    Company = UserCompanyDataMain.objects.filter(user_id=wo.supplier.ContactNo)
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

    return render(request, 'officer/wo_view.html',
                  {"officer": officer, 'wo': wo, 'Header': Header, 'Company': Company, 'Time': Time, 'Price': Price,
                   "Advance": Advance, 'Supply_Item': Supply_Item, 'Supply': Supply, 'Install_Item': Install_Item,
                   'Install': Install, 'Major_Item': Major_Item, 'Install': Install, 'Variable_Item': Variable_Item,
                   'Copy_To': Copy_To})



def deregister_cgm_all(request):
    if request.session.has_key('officer'):
        if request.session['officer'] == 'WZ':

            data = User_Registration.objects.filter(User_zone='WZ',deregister=1)
            return render(request, 'officer/cgm_deregister_all_vendor.html',{'data': data})

        elif request.session['officer'] == 'CZ':
            data = User_Registration.objects.filter(User_zone='CZ',deregister=1)
            return render(request, 'officer/cgm_deregister_all_vendor.html',{'data': data})

        elif request.session['officer'] == 'EZ':
            data = User_Registration.objects.filter(User_zone='EZ',deregister=1)
            return render(request, 'officer/cgm_deregister_all_vendor.html',{'data': data})
    return redirect('/')

# factory inspection reassign
def update_FI(request,id):
    data = User_Registration.objects.get(User_Id=id)
    c_add = UserCompanyDataMain.objects.get(user_id_id=data)
    c_name = data.CompanyName_E
    officer = InspectingOfficerInfo.objects.all()
    off=Factory_Inspection_Info.objects.filter(vendor=id)
    fi_data=off[len(off)-1]
    pofficer=fi_data.officer.officer_name
    return render(request, 'officer/update_vendor_factory_inspection.html', {'data': data, 'c_add':c_add,'employee': officer,'pofficer':pofficer}) 

def Update_factory_inspection_initiate(request,id):
    data = User_Registration.objects.get(User_Id=id)
    c_name = data.CompanyName_E
    if request.method == 'POST':
        officer = request.POST.get('officer')
        officer = InspectingOfficerInfo.objects.get(id=officer)

        mobile = officer.contact_no
        name_sms = officer.officer_name
        oid = officer.officer_employ_id
        pws = officer.officer_password

        date = request.POST.get('date')
        cancel_remark=request.POST.get('cancel_remark')
        import datetime
        today = datetime.datetime.now()
        data = User_Registration.objects.get(User_Id=id)
        assign_by_officer = request.session['employ_login_id']
        data1 = Factory_Inspection_Info.objects.filter(vendor=id)
        print(len(data1))
        print(data1)
        FI=data1[len(data1)-1]
        FI_history=Factory_Inspection_Info_history(vendor=data, officer=FI.officer, assign_date=FI.assign_date, execution_date=FI.execution_date,assigned_by = FI.assigned_by,cancel_remark=cancel_remark)
        FI_history.save()
        FI.officer=officer
        FI.vendor=data
        FI.assign_date=today
        FI.assigned_by=assign_by_officer
        FI.execution_date=date
        FI.save()
        vendor_con = data.ContactNo
        vendor_com = data.CompanyName_E
        zone = data.User_zone
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        # for server set proxy
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007254789662546256&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(c_name) + "&v4=" + str() + "&v5=" + str(zone) + "&v6=" + str(date) + "&v7=" + str(oid) + "&v8=" + str(pws) + "&v9=" + str('https://shorturl.at/jkyJ8') + "&v10=" + str()
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007254789662546256',date = datetime.datetime.now(),mobile_number = mobile)
        sms_template.save()
        
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007363155209103912&mobile_number=" + str(
                            vendor_con) + "&v1=" + str(vendor_com) + "&v2=" + str() + "&v3=" + str() + "&v4=" + str(date)
        response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007363155209103912',date = datetime.datetime.now(),mobile_number = vendor_con)
        sms_template.save()

        if request.session.has_key('officer'):
            if request.session['officer'] == 'WZ':
                data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='WZ')
                fdata = Factory_Inspection_Info.objects.all()
                return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})

            elif request.session['officer'] == 'CZ':
                data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='CZ')
                fdata = Factory_Inspection_Info.objects.all()
                return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})

            elif request.session['officer'] == 'EZ':
                data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone='EZ')
                fdata = Factory_Inspection_Info.objects.all()
                return render(request, 'officer/cgm_pending_vendor.html',{'data': data,'b':fdata})
        return redirect('/')
    
def reassign_history(request,id):
    data=Factory_Inspection_Info_history.objects.filter(vendor=id)
    return render(request,'officer/reassign_history.html',{'data': data})


def to_do(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id']) 
    officer_zone = officer.Discom.Discom_Code
    pdi_assign_data = offer_material_site_stores.objects.filter(Material_Offer_Submit_Approved_Status=1,PDI_Assign=0,wo__zone=officer_zone,is_pdi_required=True).distinct('offer_no')
    len_pdi_data = len(pdi_assign_data)
    
    pdi_acceptance_data = PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=officer_zone,Material__PDI_Approved_Status=0,Material__PDI_Complete=1,Material__Material_Offer_Submit_Approved_Status=1, pdi_report__isnull = True).distinct('offer_no')
    len_pdi_acceptance_data = len(pdi_acceptance_data)
    
    factory_inspection_data = User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone=officer.Discom.Discom_Code)
    len_factory_inspection_data = len(factory_inspection_data)
    
    vendor_data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,factory_approval_payment=1,factory_approval=1, User_type='VENDOR',User_zone=officer.Discom.Discom_Code)
    len_vendor_data = len(vendor_data)
    
    new_material_data = User_Registration.objects.filter(work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR',User_zone=officer.Discom.Discom_Code,add_material=4)
    len_new_material_data = len(new_material_data)

    vendor_sign = User_Registration.objects.filter(officer_create=0, digital_cert_upload = 0, cgm_approval = 1, User_type='VENDOR', User_zone=officer.Discom.Discom_Code)
    len_vendor_sign = len(vendor_sign)
    
    vendor_sampling = DI_Areastores.objects.filter(di_master__send_to_cgm=1, zone= officer.Discom.Discom_Code, sampling_flag = 0).distinct('di_master')
    len_vendor_sampling = len(vendor_sampling)
    
    pending_nabl_data = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1, User_type='NABL')
    len_pending_nabl_data = len(pending_nabl_data)
    
    nabl_sign = User_Registration.objects.filter(officer_create=0, digital_cert_upload = 0, cgm_approval = 1, User_type='NABL', User_zone=officer.Discom.Discom_Code)
    len_nabl_sign = len(nabl_sign)
    
    rca_pending_new = Rca_User_Registration.objects.filter(payment=1,cgm_approval=0,factory_approval=1,factory_approval_status=1,User_zone=officer.Discom.Discom_Code)
    len_rca_pending_new = len(rca_pending_new)
    
    rca_pending_data = Rca_User_Registration.objects.filter(cgm_approval=0,provision_fi=1,User_zone=officer.Discom.Discom_Code)
    len_rca_pending_data = len(rca_pending_data)
    
    rca_factory_inspection = Rca_User_Registration.objects.filter(factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR',User_zone=officer.Discom.Discom_Code,provision_fi=0)
    len_rca_factory_inspection = len(rca_factory_inspection)
    
    rca_sign = Rca_User_Registration.objects.filter(digital_cert_upload = 0, cgm_approval = 1, User_type="VENDOR", User_zone = officer.Discom.Discom_Code)
    len_rca_sign = len(rca_sign)

    new_vendor_material =  User_Registration.objects.filter(User_type='VENDOR',add_material=3,User_zone=officer.Discom.Discom_Code) 
    len_new_vendor_material = len(new_vendor_material)
    
    
    print("[[[[[[[]]]]]]]]",len_new_vendor_material) 
                   
    
    return render(request, 'main/to_do.html',{'len_pdi_data' : len_pdi_data, 'len_pdi_acceptance_data' : len_pdi_acceptance_data, 'len_factory_inspection_data' : len_factory_inspection_data,
                                              'len_vendor_data' : len_vendor_data, 'len_new_material_data' : len_new_material_data, 'len_vendor_sign' : len_vendor_sign, 'len_vendor_sampling' : len_vendor_sampling,
                                              'len_pending_nabl_data' : len_pending_nabl_data, 'len_nabl_sign' : len_nabl_sign, 'len_rca_pending_new' : len_rca_pending_new, 'len_rca_pending_data' : len_rca_pending_data,
                                              'len_rca_factory_inspection' : len_rca_factory_inspection, 'len_rca_sign' : len_rca_sign, 'len_new_vendor_material' : len_new_vendor_material})



 # code show inspecting officer List in CGM Side add update and delete by PDM
from django.contrib import messages
def inspecting_off_info(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    data=InspectingOfficerInfo.objects.filter(user_zone=officer_zone)
    region=Region_Master.objects.filter(Discom__Discom_Code=officer_zone) 
    return render(request,'officer/inspecting_officer.html',{'data':data,'region':region})

def add_inspecting_off_info(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    
    if request.method == "POST":
        employ_id=request.POST.get('employee_id')
        employee_name=request.POST.get('employee_name')
        contact=request.POST.get('contact')
        email=request.POST.get('email')
        designation=request.POST.get('designation')
        off_region=request.POST.get('region')
        address=request.POST.get('address')
        data1=InspectingOfficerInfo.objects.filter(contact_no=contact) or InspectingOfficerInfo.objects.filter(officer_employ_id=employ_id)
        if not data1.exists():
            password=employ_id[:3] + contact[-4:-1]
            officer_work="FI"
            inspection_officer=InspectingOfficerInfo(officer_name=employee_name,contact_no=contact,officer_email=email,officer_employ_id=employ_id,officer_designation=designation,officer_password=password,officer_work=officer_work,user_zone=officer_zone,officer_address=address,officer_region=off_region)
            inspection_officer.save()
            messages.success(request,'Inspecting Officer Added Successfully!!')
            return redirect('inspecting_off_info')
            
        else:
            messages.warning(request, 'Mobile no already exist to another Officer')
            return redirect('inspecting_off_info')
    return redirect('inspecting_off_info')
        
def update_inspecting_off_info(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    if request.method == "POST":
        emp_id=request.POST.get('id_value')
        employ_id=request.POST.get('officer_employee')
        employee_name=request.POST.get('employee_name')
        contact=request.POST.get('contact')
        email=request.POST.get('email')
        designation=request.POST.get('designation')
        off_region=request.POST.get('region')
        address=request.POST.get('address')
        data = InspectingOfficerInfo.objects.filter(contact_no=contact).exclude(officer_employ_id=employ_id)
        if not data.exists():
            ins_data=InspectingOfficerInfo.objects.get(id=emp_id)
            ins_data.officer_name=employee_name
            ins_data.contact_no=contact
            ins_data.officer_email=email
            ins_data.officer_employ_id=employ_id
            ins_data.officer_designation=designation
            ins_data.officer_address=address
            ins_data.officer_region=off_region
            ins_data.save()
            messages.success(request,'Inspecting Officer Updated Successfully!!')
            return redirect('inspecting_off_info')
        else:
            data=InspectingOfficerInfo.objects.filter(user_zone=officer_zone)
            region=Region_Master.objects.filter(Discom__Discom_Code=officer_zone)
            messages.warning(request,'Mobile no already exist to another Officer')
            return redirect('inspecting_off_info')
    return redirect('inspecting_off_info')
            

def del_ins_officer(request,pk):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    officer_zone = officer.Discom.Discom_Code
    data=PDI_Inspection_Info.objects.filter(officer=pk) or Factory_Inspection_Info.objects.filter(officer=pk)
    if not data.exists():
        data1=InspectingOfficerInfo.objects.get(id=pk)
        data1.delete()
        messages.success(request,'Inspecting Officer Deleted Successfully!!')
        return redirect('inspecting_off_info')
        
    else:
        messages.warning(request, 'This officer assigned for Pre Delivery Inspection OR Factory Inspection')
        return redirect('inspecting_off_info')
    
        
    
# reject offer by CGM QC in pending PDI before assign
def pending_pdi_reject(request,offer_no):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    offer_material=offer_material_site_stores.objects.filter(offer_no=offer_no,is_pdi_required=True)
    for i in offer_material:
        i.PDI_Assign=-1
        wo_qty=tkc_wo_items_boq.objects.get(id=i.wo_material.id)
        wo_qty.balance_qty=float(wo_qty.balance_qty) + float(i.quantity)
        wo_qty.save()
        i.PDI_Assign_At=datetime.datetime.now().date()
        i.PDI_Assign_By = officer.employ_name            
        i.save()
    return redirect(pdi_pending_assign)  
    
    

