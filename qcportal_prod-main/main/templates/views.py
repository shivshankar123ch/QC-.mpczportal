from po.models import *
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


# Create your views here.

def home(request):
    return render(request, 'main/login.html')


def user(request):
    if request.method == "POST":
        user = request.POST.get('user')
        if user == 'user':
            return render(request, 'main/main_login.html')
        elif user == 'admin':

            return redirect('mpeb_login')

        elif user == 'registration':

            return redirect('reg')
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
        if User_Registration.objects.filter(ContactNo=mobile_no).exists():
            data = User_Registration.objects.get(ContactNo=mobile_no)
            request.session['mobile_no'] = mobile_no
            request.session['otp'] = otp
            request.session['uid'] = mobile_no

            uid = mobile_no
            uidd = otp
            if data.Otp == otp:
                if data.User_type == "VENDOR":
                    if User_Registration.objects.filter(ContactNo=uid, payment=1, rca_vendor=0):
                        data11 = User_Registration.objects.filter(Otp=uidd)
                        con = User_Registration.objects.get(Otp=uidd)
                        payu_count = Payudata_main.objects.filter(Contact_No=con.ContactNo).count()
                        return render(request, 'vendor/basicinfo.html',
                                      {"userdata": data, 'data11': data11, 'payu_count': payu_count})
                    elif User_Registration.objects.filter(ContactNo=uid, payment=1, rca_vendor=1):
                        data11 = User_Registration.objects.filter(Otp=uidd)
                        return render(request, 'vendor/RCA_vendor_base.html', {"userdata": data, 'data11': data11})
                    elif BankDetails.objects.filter(user_id=uid).exists() and UserCompanyDataMain.objects.filter(
                            user_id=uid).exists() and AuthorisedPerson.objects.filter(user_id=uid).exists():

                        data = BankDetails.objects.filter(user_id=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        data2 = BankDetails.objects.filter(user_id=uid)
                        return render(request, 'main/reg_fifth.html', {'data': data2[0]})
                    elif AuthorisedPerson.objects.filter(
                            user_id=uid).exists() and UserCompanyDataMain.objects.filter(user_id=uid).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        data2 = AuthorisedPerson.objects.filter(
                            user_id=uid)
                        return render(request, 'main/reg_fourth.html',
                                      {'data1': data1[0], 'data': data[0], 'data2': data2[0]})
                    elif UserCompanyDataMain.objects.filter(user_id=uid).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        return render(request, 'main/reg_third.html', {'data1': data1[0], 'data': data[0]})

                    else:
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        return render(request, 'main/reg_second.html', {'data': data[0]})

                elif data.User_type == "TKC":
                    abc = request.session['otp']
                    if User_Registration.objects.filter(ContactNo=uid, payment=1):
                        data11 = User_Registration.objects.filter(Otp=uidd)
                        con = User_Registration.objects.get(Otp=uidd)
                        payu_count = Payudata_main.objects.filter(Contact_No=con.ContactNo).count()
                        return render(request, 'tkc/basicinfo.html',
                                      {"userdata": data, 'abc': abc, 'data11': data11, 'payu_count': payu_count})
                    elif BankDetails.objects.filter(user_id=uid).exists() and UserCompanyDataMain.objects.filter(
                            user_id=uid).exists() and AuthorisedPerson.objects.filter(user_id=uid).exists():
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        data2 = BankDetails.objects.filter(user_id=uid)
                        return render(request, 'main/reg_fifth.html', {'data': data2[0]})
                    elif AuthorisedPerson.objects.filter(
                            user_id=uid).exists() and UserCompanyDataMain.objects.filter(user_id=uid).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        data2 = AuthorisedPerson.objects.filter(
                            user_id=uid)
                        return render(request, 'main/reg_fourth.html',
                                      {'data1': data1[0], 'data': data[0], 'data2': data2[0]})
                    elif UserCompanyDataMain.objects.filter(user_id=uid).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        return render(request, 'main/reg_third.html', {'data1': data1[0], 'data': data[0]})
                    else:
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        return render(request, 'main/reg_second.html', {'data': data[0]})
                else:
                    abc = request.session['otp']
                    if User_Registration.objects.filter(ContactNo=uid, Complete_Details=1):
                        return render(request, 'nabl/basics.html', {"userdata": data})
                    if NABL_Document.objects.filter(
                            user_id=request.session['otp']) and UserCompanyDataMain.objects.filter(
                        user_id=uid).exists():
                        return render(request, 'nabl/user_base.html', {"userdata": data, 'abc': abc})
                    elif BankDetails.objects.filter(user_id=uid).exists():
                        data11 = User_Registration.objects.filter(
                            ContactNo=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        data2 = AuthorisedPerson.objects.filter(
                            user_id=uid)
                        return render(request, 'nabl/basics.html', {"userdata": data})
                        # return render(request, 'nabl/basics.html',
                        #             {'data1': data1[0], 'data': data[0], 'data2': data2[0]})

                    elif AuthorisedPerson.objects.filter(
                            user_id=uid).exists() and UserCompanyDataMain.objects.filter(user_id=uid).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        data2 = AuthorisedPerson.objects.filter(
                            user_id=uid)
                        return render(request, 'main/reg_fourth.html',
                                      {'data1': data1[0], 'data': data[0], 'data2': data2[0]})
                    elif UserCompanyDataMain.objects.filter(user_id=uid).exists():
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
                        data1 = UserCompanyDataMain.objects.filter(
                            user_id=uid)
                        return render(request, 'main/reg_third.html', {'data1': data1[0], 'data': data[0]})
                    else:
                        data = User_Registration.objects.filter(
                            ContactNo=uid)
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

        if User_Registration.objects.filter(ContactNo=mobile).exists():
            messages.warning(request, "Mobile Number already registered")
            return render(request, 'main/reg_first.html',
                          {'one': one, 'two': two, 'three': three, 'four': four, 'five': five, 'six': six,
                           'seven': seven, 'type': type_data})
        elif User_Registration.objects.filter(Email_Id=email).exists():
            messages.warning(request, "Email ID already registered")
            return render(request, 'main/reg_first.html',
                          {'one': one, 'two': two, 'three': three, 'four': four, 'five': five, 'six': six,
                           'seven': seven, 'type': type_data})
        else:

            user_details = User_Registration(User_type=User_type, Type_of_business=service_type,
                                             CompanyName_E=company_name_e, User_zone=zone,
                                             CompanyName_H=company_name_h, Authorised_person_H=name_of_authorized_h,
                                             Authorised_person_E=name_of_authorized_e, ContactNo=mobile, Email_Id=email)

            user_details.save()
            # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # # proxyDict = {"http" : "proxy.mpcz.in:8080"}
            # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007575598720789466&mobile_number=" + str(
            #     mobile) + "&v1=" + str(company_name_e) + "&v2=" + str() + "&v3=" + str(mobile) + "&v4=" + str(
            #     'https://qcportal.mpcz.in/')
            # response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            # send_mail(
            #     'Quality Monitoring Portal-Registration Complete',
            #     'Thank you for your Registration, your user id is your mobile number, please login to portal qcm.mpcz.in for completing the registration process',
            #     settings.EMAIL_HOST_USER,
            #     [email],
            #     fail_silently=False,
            # )

            messages.warning(request, "You are successfully registered")
            data = User_Registration.objects.filter(ContactNo=mobile)
            request.session['uid'] = mobile
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

            # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8000"}
            # # for server set proxy
            # # proxyDict = {"http" : "proxy.mpcz.in:8000","https" : "proxy.mpcz.in:8000"}

            # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007906932005083817&mobile_number=" + str(uid) + "&v1=Application&v2="
            # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})

            data = User_Registration.objects.filter(ContactNo=uid)
            company = UserCompanyDataMain(user_id=uid, CompanyName_E=data[0].CompanyName_E,
                                          CompanyName_H=data[0].CompanyName_H, Company_Contact_No=uid,
                                          Company_Fax=Company_Fax, Company_Pan_No=Company_Pan_No,
                                          Company_Gumastha_No=Company_Gumastha_No, Company_Gst_No=Company_Gst_No,
                                          Registration_Date=reg_date, Company_add_1=Company_Address_1,
                                          Company_add_2=Company_Address_2, Company_pin_code=p_code, Company_state=state,
                                          Company_dist=district, Company_city=City, Company_t_add_1=Office_Address_1,
                                          Company_t_add_2=Office_Address_2, Company_t_pin_code=p_code_2,
                                          Company_t_state=state_2, Company_t_dist=district_2, Company_t_city=City_2)
            company.save()
            data = User_Registration.objects.filter(ContactNo=uid)
            return render(request, 'main/reg_third.html', {'data': data[0]})
    return render(request, 'main/main_login.html')


def reg_third(request):
    if request.session.has_key('uid'):
        uid = request.session['uid']
        data = User_Registration.objects.filter(ContactNo=uid)
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        aadhar = request.POST.get('aadhar')
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
        direct_aadhar = request.POST.get('dir_aadhar')
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

        person = AuthorisedPerson(user_id=uid, Authorised_P_Name_E=data[0].Authorised_person_E,
                                  Authorised_P_Name_H=data[0].Authorised_person_H,
                                  Authorised_P_DOB=dob, Authorised_P_Number=mobile, Authorised_P_Aadhar_No=aadhar,
                                  Authorised_P_add_1=auth_per_addresslin1, Authorised_P_add_2=auth_per_addresslin2,
                                  Authorised_P_state=auth_per_state, Authorised_P_District=auth_per_district,
                                  Authorised_P_City=auth_per_city, Authorised_P_pin_code=auth_per_pincode,
                                  Director_P_Name_E=direct_name, Director_P_Name_H=direct_name_hindi,
                                  Director_P_DOB=direct_dob, Director_P_Number=direct_mobile,
                                  Director_P_Email=direct_email, Director_P_Aadhar_No=direct_aadhar,
                                  Director_P_add_1=direct_addresslin1, Director_P_add_2=direct_addresslin2,
                                  Director_P_pin_code=direct_pincode, Director_P_state=direct_state,
                                  Director_P_District=direct_district, Director_P_City=direct_city

                                  )
        person.save()
        return render(request, 'main/reg_fourth.html', {'user': data[0]})
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
            data = User_Registration.objects.filter(ContactNo=uid)
            if data[0].User_type == "NABL":
                data.update(Basic_Details=1)
                return redirect('login')
            return render(request, 'main/reg_sixth.html', {'c_type': data[0]})
    return render(request, 'main/main_login.html')


def reg_sixth(request):
    if request.session.has_key('uid'):
        uid = request.session['uid']
        data = User_Registration.objects.filter(ContactNo=uid)
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
        if Officer.objects.filter(employ_login_id=employ_login_id).exists():
            def generateOTP():
                digits = "0123456789"
                OTP = ""
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP

            otp = generateOTP()
            rohit = Officer.objects.filter(employ_login_id=employ_login_id)
            rohit.update(otp=otp)
            sms_otp = Officer.objects.get(employ_login_id=employ_login_id)
            sms_number = sms_otp.mobile
            # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # # proxyDict = {"http" : "proxy.mpcz.in:8080"}
            # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(
            #     sms_number) + "&v1=" + str(otp) + "&v2=" + str()
            # response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            request.session['employ_login_id'] = employ_login_id
            request.session['otp'] = otp
            messages.warning(request, otp)
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
                    if officer.mobile == '8357056024':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'officer/dgm_base.html', {'data': officer})
                    elif officer.mobile == '8269860651':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])

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
                    elif officer.mobile == '8744927257':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
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
                        return render(request, 'officer/dgm_finance.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
                    elif officer.mobile == '8786565656':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                                   User_type='VENDOR').count()
                        pending = User_Registration.objects.filter(Complete_Details=1, work_approval=1, cgm_approval=0,
                                                                   finance_approval=1,
                                                                   User_type='VENDOR', factory_approval=1).count()
                        total = approve + pending

                        approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                                        User_type='NABL').count()
                        pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0,
                                                                        Complete_Details=1,
                                                                        User_type='NABL').count()

                        total_nabl = approve_nabl + pending_nabl
                        return render(request, 'main/mpeb_base.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total,
                                       'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                                       'total_nabl': total_nabl, })

                    elif officer.mobile == '6232913171':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'po/procurement_dashboard.html', {'data': officer})
                    elif officer.mobile == '8770091031':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'officer/cgm_procurement.html', {'data': officer})
                    elif officer.mobile == '8888888888':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'po/area_store/areastore_base.html', {'data': officer})

                    elif officer.mobile == '9988776655':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        return render(request, 'po/nabl/dasbordbase.html', {'data': officer})


                    elif officer.mobile == '9876543230':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'rca/RCA_base.html', {'data': officer})

                    elif officer.mobile == '9981393754':
                        officer = Officer.objects.get(
                            employ_login_id=request.session['employ_login_id'])
                        approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                                   User_type='TKC').count()
                        pending = User_Registration.objects.filter(work_approval=1, cgm_approval=0, finance_approval=1,
                                                                   User_type='TKC').count()
                        total = approve + pending
                        return render(request, 'officer/gmwdasbordbase.html',
                                      {'data': officer, 'approve': approve, 'pending': pending, 'total': total})

                    elif officer.mobile == '7000551592':
                        officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
                        return render(request, 'officer/tmqm_base.html', {'data': officer})
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


def work_pending_vendor(request):
    data = User_Registration.objects.filter(work_approval=0)
    return render(request, 'officer/work_pending_vendor.html', {'data': data})


# def cgm_pending_vendor(request):
#     data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,
#                                             factory_approval_payment=1)
#     return render(request, 'officer/cgm_pending_vendor.html', {'data': data})


# def cgm_total_vendor(request):
#     data = User_Registration.objects.filter(work_approval=1, finance_approval=1,factory_approval_payment=1,cgm_approval=0)
#     return render(request, 'officer/total_cgm_vendor.html', {'data': data})


# def cgm_complete_vendor(request):
#     data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1,
#                                             factory_approval_payment=1)
#     return render(request, 'officer/cgm_complete_vendor.html', {'data': data})

# -poornima----------------------------------------------13 april

# def vendor_cgm_evaluate(request, id):
#     data = User_Registration.objects.filter(User_Id=id)

#     if data[0].User_type == "VENDOR":
#         doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)

#         doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)

#         fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
#         Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
#         tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)

#         return render(request, 'officer/vendor_cgm_evaluate.html',
#                       {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
#                        'tech_data': tech_data})

#     doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
#     Factory = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
#     Material = Add_material.objects.filter(user_id=data[0].User_Id)
#     return render(request, 'officer/vendor_wnp_evaluate.html',
#                   {'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material})


def vendor_cgm_evaluate_save(request, id):
    if request.method == 'POST':
        data = User_Registration.objects.filter(User_Id=id)
        doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
        comm = request.POST.get(str('remark'))
        doc.CGM_remark = comm
        result = request.POST.get(str('action'))
        if result == 'OK':
            data = User_Registration.objects.get(User_Id=id)
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
            company_name = data[0].CompanyName_E
            issue_date = today.strftime("%d/%m/%Y")
            valid_upto = datetime(2024, 1, 11)
            valid_upto = valid_upto.strftime("%d/%m/%Y")
            data11 = User_Registration.objects.filter(User_Id=id)
            data11.update(Authentication_id=s)
            data11 = User_Registration.objects.get(User_Id=id)
            vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)

            sms = User_Registration.objects.get(User_Id=id)
            mobile = sms.ContactNo
            name_sms = sms.CompanyName_E
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8000"}
            # for server set proxy
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007686693598132208&mobile_number=" + str(
                mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('VENDOR') + "&v4=" + str(
                'https://qcportal.mpcz.in/')
            response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

            # send_mail(
            #     'Approval status of CGM (QC) ',
            #     'Your application is finally approved by CGM(QC) and your registration number is ' + s,
            #     settings.EMAIL_HOST_USER,
            #     [data11.Email_Id],
            #     fail_silently=False,
            # )
            td = datetime.now()

            otp_ofcr = User_Registration.objects.filter(User_Id=id)
            otp_ofcr.update(Otp='34512')

            usr_obj = User_Registration.objects.get(User_Id=id)
            otp = usr_obj.Otp

            return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})
            # return render(request, 'vendor/cert2.html', {'td':td,'vmaterial':vmaterial,'data': data[0], 'company_name': company_name, 'no': s, 'd1': valid_upto, 'd2': issue_date})

        else:
            data = User_Registration.objects.get(User_Id=id)
            data.cgm_approval = -1
            data.final_rejection = -1
            data.save()
            send_mail(
                'Rejection status of C.G.M (QC) ',
                'Hello ! Your application is finally rejected by C.G.M (QC)',
                settings.EMAIL_HOST_USER,
                [data.Email_Id],
                fail_silently=False,
            )
            data = User_Registration.objects.filter(work_approval=1, finance_approval=1, qc_approval=1, cgm_approval=0)
            return render(request, 'officer/cgm_pending_vendor.html', {'data': data})


def officer_otp(request, id, otp):
    if request.method == "POST":
        officer_otp = request.POST.get('officer_otp')
        usr_obj = User_Registration.objects.get(User_Id=id)

        if officer_otp.strip() == ((usr_obj.Otp).strip()):
            from datetime import date
            User_Zone = usr_obj.User_zone
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
            valid_upto = datetime(2024, 1, 11)
            valid_upto = valid_upto.strftime("%d/%m/%Y")
            data11 = User_Registration.objects.filter(User_Id=id)
            data11.update(Authentication_id=s)
            data11 = User_Registration.objects.get(User_Id=id)
            vmaterial = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
            td = datetime.now()
        else:
            return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})
        return render(request, 'vendor/contactor_cert3.html',
                      {'td': td, 'vmaterial': vmaterial, 'data': data[0], 'company_name': company_name, 'no': s,
                       'd1': valid_upto, 'd2': issue_date, 'User_Zone': User_Zone})
    return render(request, 'main/officer_otp.html', {'id': id, 'otp': otp})


def vendor_cgm_evaluate_save1(request, id):
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
    data = User_Registration.objects.filter(
        factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR')
    return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data})


def factory_inspection_initiate(request, id):
    data = User_Registration.objects.get(User_Id=id)
    officer = InspectingOfficerInfo.objects.all()
    if request.method == 'POST':
        officer = request.POST.get('officer')
        officer = InspectingOfficerInfo.objects.get(id=officer)
        date = request.POST.get('date')
        import datetime
        today = datetime.datetime.now()
        data = User_Registration.objects.get(User_Id=id)
        data1 = Factory_Inspection_Info(vendor=data, officer=officer, assign_date=today, execution_date=date)
        data1.save()
        data.factory_approval_status = 1
        data.save()
        data = User_Registration.objects.filter(
            factory_approval_status=0, factory_approval_payment=1, User_type='VENDOR')
        return render(request, 'officer/vendor_factory_inspection_initiate.html', {'data': data})
    return render(request, 'officer/vendor_factory_inspection.html', {'data': data, 'employee': officer})


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
    data = User_Registration.objects.filter(qc_approval=2, Complete_Details=1,
                                            User_type='NABL')
    return render(request, 'officer/nabl_dgm_work_pending_resubmit.html', {'data': data})

    if data[0].User_type == "TKC":
        doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1)
        return render(request, 'officer/dgm_work_evaluate.html', {'data': data[0], 'doc': doc})
    return render(request, 'officer/dgm_work_evaluate.html', {'data': data[0]})


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
    data = User_Registration.objects.filter(
        finance_approval=2, Complete_Details=1, User_type='VENDOR')
    return render(request, 'officer/vendor_dgm_finance_pending_rejection.html', {'data': data})


def vendor_dgm_finance_total_approved(request):
    data = User_Registration.objects.filter(
        finance_approval=1, Complete_Details=1, User_type='VENDOR')
    return render(request, 'officer/vendor_dgm_finance_total_approved.html', {'data': data})


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


def dgm_qc_evaluate_save(request, id):
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
                data.Primary_verification_Date = datetime.datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status = 1
                else:
                    user = User_Registration.objects.get(User_Id=id)
                    user.qc_approval = 2

                    data.Primary_verification_Status = 2
                    data.Status = 0
                    test = data.Primary_remark_rejection_counter
                    if test >= 3:
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
    material = Vendor_Material_Details.objects.filter(user_id=id)
    data.update(Authentication_id=reg_no)
    td = datetime.now()
    return render(request, 'main/cert_vendor.html', {'td': td, 'no': reg_no, 'data': data[0], 'material': material})


def vendor_cgm_evaluate_view(request, id):
    data = User_Registration.objects.filter(User_Id=id)

    if data[0].User_type == "TKC":
        doc = TKC_Document.objects.filter(user_id=data[0].User_Id)
        doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
        return render(request, 'officer/vendor_cgm_evaluate_view.html',
                      {'data': data[0], 'doc': doc, 'doc1': doc1})


def tkc_total(request):
    data = User_Registration.objects.filter(
        Complete_Details=1, User_type='TKC')
    return render(request, 'officer/tkc_total_vendor.html', {'data': data})


def cgm_rejected_tkc(request):
    data = User_Registration.objects.filter(
        Complete_Details=1, final_rejection=-1, User_type='TKC')
    return render(request, 'officer/cgm_rejected_tkc.html', {'data': data})


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

#             if not data:
#                 data = User_Registration.objects.get(User_Id=id)
#                 data.qc_approval = 1
#                 data.save()

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


def nabl_cgm_evaluate_save(request, id):
    if request.method == 'POST':
        data = User_Registration.objects.filter(User_Id=id)
        doc = NABL_Document.objects.filter(user_id=data[0].User_Id)

        usr_obj = User_Registration.objects.get(User_Id=id)
        print(
            "usr_obj.User_zoneusr_obj.User:::::::::::::::::::::::::::::::::::::_zoneusr_obj.User_zoneusr_obj.User_zone",
            usr_obj.User_zone)

        comm = request.POST.get(str('remark'))
        doc.CGM_remark = comm
        result = request.POST.get(str('action'))
        if result == 'OK':
            data = User_Registration.objects.get(User_Id=id)
            data.cgm_approval = 1
            data.save()
            send_mail(
                'Approval status of CGM(QC) ',
                'Hello ! Your application is approved by CGM (QC).',
                settings.EMAIL_HOST_USER,
                [data.Email_Id],
                fail_silently=False,
            )
            from datetime import date
            User_Zone = usr_obj.User_zone
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
            valid_upto = datetime(2024, 1, 11)
            valid_upto = valid_upto.strftime("%d/%m/%Y")
            data11 = User_Registration.objects.filter(User_Id=id)
            data11.update(Authentication_id=s)
            data11 = User_Registration.objects.get(User_Id=id)
            send_mail(
                'Approval status of CGM (QC) ',
                'Your application is finally approved by CGM(QC) and your registration number is ' + s,
                settings.EMAIL_HOST_USER,
                [data11.Email_Id],
                fail_silently=False,
            )
            return render(request, 'vendor/cert2.html',
                          {'User_Zone': User_Zone, 'data': data[0], 'company_name': company_name, 'no': s,
                           'd1': valid_upto, 'd2': issue_date})

        else:
            data = User_Registration.objects.get(User_Id=id)
            data.cgm_approval = -1
            data.final_rejection = -1
            data.save()
            send_mail(
                'Rejection status of CGM(QC) ',
                'Hello ! Your application is finally rejected by CGM (QC).',
                settings.EMAIL_HOST_USER,
                [data.Email_Id],
                fail_silently=False,
            )
            data = User_Registration.objects.filter(
                qc_approval=1, cgm_approval=0)
            return render(request, 'officer/cgm_pending_nabl.html', {'data': data})


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
    data = User_Registration.objects.filter(
        Complete_Details=1, cgm_approval=0, User_type='TKC')
    return render(request, 'officer/cgm_pending_tkc.html', {'data': data})


def cgm_complete_tkc(request):
    data = User_Registration.objects.filter(
        cgm_approval=1, work_approval=1, finance_approval=1, User_type='TKC')
    return render(request, 'officer/cgm_complete_tkc.html', {'data': data})


def tkc_cgm_evaluate(request, id):
    data = User_Registration.objects.filter(User_Id=id)
    # data.update(cgm_approval=1)
    if data[0].User_type == "TKC":
        doc = TKC_Document.objects.filter(user_id=data[0].User_Id)
        doc1 = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
        return render(request, 'officer/tkc_cgm_evaluate.html',
                      {'data': data[0], 'doc': doc, 'doc1': doc1})


def tkc_cgm_evaluate_save(request, id):
    if request.method == 'POST':
        data = User_Registration.objects.filter(User_Id=id)
        doc = TKC_Document.objects.filter(user_id=data[0].User_Id)

        exp = TKC_Document.objects.get(user_id=data[0].User_Id, Types_of_Docs='ELECTRICAL LICENSE')

        expi_date = exp.Doc_expiry_date

        comm = request.POST.get(str('remark'))
        doc.CGM_remark = comm
        result = request.POST.get(str('action'))
        if result == 'OK':
            data = User_Registration.objects.get(User_Id=id)
            print(
                "data.User_zonedata.User_zonedata.Us:::::::::::::::::::::::::::::::::::::::::::::::er_zonedata.User_zonedata.User_zone",
                data.User_zone)
            data.cgm_approval = 1
            data.save()
            # send_mail(
            #     'Approval status of GM (Works) ',
            #     'Hello ! Your are approved by GM (Works)',
            #     settings.EMAIL_HOST_USER,
            #     [data.Email_Id],
            #     fail_silently=False,
            # )
            from datetime import date
            User_Zone = data.User_zone
            User = "TKC"
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
            valid_upto = expi_date
            data11 = User_Registration.objects.get(User_Id=id)
            data11.Authentication_id = s
            data11.save()
            # send_mail(
            #     'Approval status of GM (works) ',
            #     'Your application is finally approved by GM(Works) and your registration number is ' + s,
            #     settings.EMAIL_HOST_USER,
            #     [data11.Email_Id],
            #     fail_silently=False,
            # )
            td = datetime.now()

            sms = User_Registration.objects.get(User_Id=id)
            mobile = sms.ContactNo
            name_sms = sms.CompanyName_E
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8000"}
            # for server set proxy

            # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            #
            # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007686693598132208&mobile_number=" + str(
            #     mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('TKC') + "&v4=" + str(
            #     'https://qcportal.mpcz.in/')
            # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

            return render(request, 'vendor/cert2.html',
                          {'User_Zone': User_Zone, 'td': td, 'data': data[0], 'company_name': company_name, 'no': s,
                           'd1': valid_upto, 'd2': issue_date})

        else:
            data = User_Registration.objects.get(User_Id=id)
            data.cgm_approval = -1
            data.final_rejection = -1
            data.save()
            send_mail(
                'Rejection status of GM (Works) ',
                'Hello ! Your are finally rejected by GM (Works)',
                settings.EMAIL_HOST_USER,
                [data.Email_Id],
                fail_silently=False,
            )
            data = User_Registration.objects.filter(
                work_approval=1, finance_approval=1, cgm_approval=0)

            return render(request, 'officer/cgm_pending_tkc.html', {'data': data})


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
    print(add_material_nabl)
    print(add_material_nabl[0].material_number_list)
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


# import pyodbc
# def Report_success(request):
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

#         if not nabl_report_data.objects.filter(torder_samplecode=torder_samplecode).exists():
#             nrd_obj = nabl_report_data(trf_id = 0, reportno=reportno,ulrno=ulrno,manufacturer_wopo=manufacturer_wopo,manufacturer=manufacturer,
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
#         return redirect('Report_success_view/'+search )

#     return render(request, 'officer/tmqm_report_success.html', {'sample_code_lst': sample_code_lst} )

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
        wr_result = i.wr_result
        vr_result = i.vr_result
        ir_result = i.ir_result
        output = ""
        if wr_result == "Pass" and vr_result == "Pass" and ir_result == "Pass":
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
    data = User_Registration.objects.filter(Complete_Details=1,
                                            User_type='VENDOR') | User_Registration.objects.filter(finance_approval=2,
                                                                                                   Complete_Details=1,
                                                                                                   User_type='VENDOR')
    return render(request, 'officer/dgm_finance_total.html', {'data': data})


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
    data = User_Registration.objects.get(ContactNo=request.session['uid'])
    client = payu_sdk.payUClient(credes={"key": "7rnFly", "salt": "pjVQAWpA"})
    param = {"txnid": txnid, "amount": "2360.00", "productinfo": "Registration", "firstname":data.Authorised_person_E,
             "email":data.Email_Id}
    apiHash = payu_sdk.Hasher.generate_hash(param)
    return render(request, 'main/payu_checkout_registration.html',
                  {"posted": apiHash, "txnid": txnid, "amount": "2360.00", 'firstname': data.Authorised_person_E,
                   "email": data.Email_Id, "productinfo": "Registration", "phone": data.ContactNo})


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
    Nameon_card = data['name_on_card']
    Card_num = data['cardnum']
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    user = User_Registration.objects.get(ContactNo=Phone_no)
    user.update(payment=1)
    date = datetime.now()
    user = User_Registration.objects.get(ContactNo=Phone_no)
    data3 = Payudata_main(Hash_Id=Hash, Payu_Status=Status, Txdid=Txn_id,
                          Productinfo=Product_info,User_Id=user,
                          Firstname=First_name, Lastname=Last_name, Contact_No=Phone_no, Email_Id=mail,
                          Paymentgateway_Type=Pgateway_Type, date=date,
                          Bank_Ref_Num=Bankrefnum, Bankcode=Bank_code, Name_On_Card=Nameon_card,
                          Cardnum=Card_num, Netamount_Debited=Netamount
                          )
    data3.save()
    client = payu_sdk.payUClient(credes={"key": "7rnFly", "salt": "pjVQAWpA"})
    key = '7rnFly'
    salt = 'pjVQAWpA'
    command = 'verify_payment'
    toHash = {"command": command, "var1": Txn_id}
    apiHash = payu_sdk.Hasher.APIHash(toHash)
    # print('Hash',apiHash)
    # print('Txn_id', apiHash)

    # Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
    # url = 'https://test.payu.in/merchant/postservice.php?form=2'
    # r = requests.post(url, data=Poststring)
    payload = "key=" + key + "&command=verify_payment&var1=" + Txn_id + "&hash=" + apiHash
    # print('Request string:',payload)
    # res = paymentAPI.verifyPayment.verifyPaymentStatusByPayUID(payload)
    # if res.status_code == 200:
    #     json_data = json.loads(res.text)
    #     if json_data['status'] == 1:
    #         transction_details = json_data['transaction_details']
    #         transction_data = transction_details[Txn_id]
    #         if transction_data['status'] == 'success':
    #             payu_obj = Payudata_main.objects.latest('User_Id')
    #             if transction_data['productinfo'] == "Activation after expired":
    #                 user = User_Registration.objects.get(ContactNo=Phone_no)
    #                 user.activation_payment = 1;
    #                 user.save()
    #                 return render(request, 'main/sucess_pay_registration.html',
    #                               {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_reg_seven'})
    #             elif transction_data['productinfo'] == "Activation before expired":
    #                 user = User_Registration.objects.get(ContactNo=Phone_no)
    #                 user.activation_payment = 1;
    #                 user.save()
    #                 return render(request, 'main/sucess_pay_registration.html',
    #                               {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
    #             elif transction_data['productinfo'] == "Registration":
    #                 user = User_Registration.objects.get(ContactNo=Phone_no)
    #                 user.payment = 1;
    #                 user.save()
    #                 return render(request, 'main/sucess_pay_registration.html',
    #                               {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
    #             elif transction_data['productinfo'] == "Contractor Upgrade":
    #                 user = User_Registration.objects.get(ContactNo=Phone_no)
    #                 user.upgrade_payment = 1;
    #                 user.save()
    #                 return render(request, 'main/sucess_pay_registration.html',
    #                               {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_upgrade_one'})
    #             elif transction_data['productinfo'] == "Contractor Upgrade sd":
    #                 user = User_Registration.objects.get(ContactNo=Phone_no)
    #                 user.work_approval = 0;
    #                 user.finance_approval = 0;
    #                 user.qc_approval = 0;
    #                 user.upgrade_payment = 0;
    #                 user.upgrade = 0;
    #                 user.save()
    #                 return render(request, 'main/sucess_pay_registration.html',
    #                               {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_upgrade_one'})

    #             request.session['Phone_no'] = Phone_no
    #             return render(request, 'main/sucess_pay_registration.html', {'response': response, 'data': payu_obj})
    # # else:
    #     attempt_num += 1
    #     # You can probably use a logger to log the error here
    #     time.sleep(5)  # Wait for 5 seconds before re-trying
    # # User_Id=user.User_Id
    payu_obj = Payudata_main.objects.latest('User_Id')
    user = User_Registration.objects.get(ContactNo=Phone_no)
    user.payment = 1;
    user.save()
    return render(request, 'main/sucess_pay_registration.html',
                              {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
    # payu_obj = Payudata_main.objects.latest('User_Id')
    # request.session['Phone_no'] = Phone_no
    # sms = User_Registration.objects.get(ContactNo=Phone_no)
    # mobile = sms.ContactNo
    # name_sms = sms.CompanyName_E
    #
    # sms_date = datetime.now()
    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # # proxyDict = {"http" : "proxy.mpcz.in:8000"}
    # # for server set proxy
    # proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    #
    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(
    #     mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str('2360') + "&v4=" + str(
    #     'Registration') + "&v5=" + str(sms_date) + "&v6=" + str() + "&v7=" + str(sms_date) + "&v8=" + str(Bankrefnum)
    # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
    # txnid = uuid.uuid1()
    client = payu_sdk.payUClient(credes={"key": "7rnFly", "salt": "pjVQAWpA"})
    param = {"txnid": txnid, "amount": "2360.00", "productinfo": "iPhone", "firstname": "rohit",
             "email": "rohitpatel1790@gmail.com"}

    apiHash = payu_sdk.Hasher.generate_hash(param)
    return render(request, 'main/payu_checkout_registration.html', {"posted": apiHash, "txnid": txnid})


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
    Nameon_card = data['name_on_card']
    Card_num = data['cardnum']
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    date = datetime.now()
    data3 = Payudata_main(Payu_Moneyid=payu_moneyid, Hash_Id=Hash, Payu_Status=Status, Txdid=Txn_id,
                          Productinfo=Product_info,
                          Firstname=First_name, Lastname=Last_name, Contact_No=Phone_no, Email_Id=mail,
                          Paymentgateway_Type=Pgateway_Type, date=date,
                          Bank_Ref_Num=Bankrefnum, Bankcode=Bank_code, Name_On_Card=Nameon_card,
                          Cardnum=Card_num, Netamount_Debited=Netamount
                          )
    data3.save()
    payu_obj = Payudata_main.objects.latest('User_Id')
    request.session['Phone_no'] = Phone_no
    return render(request, 'main/payment_fail.html', {'response': response, 'data': payu_obj})


def gen_invoice_registration(request):
    user = User_Registration.objects.filter(ContactNo=request.session['Phone_no'])
    user.update(payment=1)
    payu_obj = Payudata_main.objects.latest('User_Id')
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
    data = User_Registration.objects.filter(factory_approval=1, factory_approval_payment=1, User_type='VENDOR')
    return render(request, 'officer/vendor_factory_inspection_assined.html', {'data': data})


# def nabl_dgm_qc_approve(request):
#     data = User_Registration.objects.filter(qc_approval=1, Complete_Details=1,
#                                             User_type='NABL') | User_Registration.objects.filter(qc_approval=2,
#                                                                                                  Complete_Details=1,
#                                                                                                  User_type='NABL')
#     return render(request, "officer/nabl_dgm_qc_total.html", {'data': data})


# #----DGMW001 WORK--- --CHANGE BECOUSE OF DASHBOARD SHOW TOTAL VENDOR---------------------------------------------------------------------------------------------

def vendor_dgm_work_total(request):
    data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR') | User_Registration.objects.filter(
        work_approval=2, Complete_Details=1, User_type='VENDOR')
    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    # data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc
    return render(request, 'officer/vendor_dgm_work_total.html',
                  {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


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
    data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                               User_type='VENDOR').count()

    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc
    return render(request, 'officer/tkc_dgm_work_total.html',
                  {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def vendor_dgm_work_complete(request):
    data = User_Registration.objects.filter(work_approval=1, Complete_Details=1, User_type='VENDOR')
    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1, User_type='VENDOR').count()
    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    return render(request, 'officer/vendor_dgm_work_complete.html',
                  {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def vendor_dgm_work_pending(request):
    data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR')

    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc
    return render(request, 'officer/vendor_dgm_work_pending.html',
                  {'data': data, 'total': total, 'approve': approve, 'pending': pending, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def vendor_dgm_work_pending_resubmit(request):
    data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='VENDOR')
    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    # data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc
    return render(request, 'officer/vendor_dgm_work_pending_resubmit.html',
                  {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


#     # return render(request, 'officer/vendor_dgm_work_pending_resubmit.html', {'data': data})


def vendor_dgm_work_pending_resubmit(request):
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


def tkc_dgm_work_complete(request):
    # <----------Poornima date 4-8-2022---------->
    data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending
    return render(request, 'officer/tkc_dgm_work_complete.html',
                  {'data': data, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc,
                   'total': total, 'pending': pending, 'approve': approve, })

    # return render(request, 'officer/tkc_dgm_work_complete.html', {'data': data})


def tkc_dgm_work_pending_resubmit(request):
    data = User_Registration.objects.filter(work_approval=2, Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending
    return render(request, 'officer/tkc_dgm_work_pending_resubmit.html',
                  {'data': data, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc,
                   'total': total, 'pending': pending, 'approve': approve, })


#     # return render(request, 'officer/tkc_dgm_work_pending_resubmit.html', {'data': data})


# # #----------DGMF001---FINANCE-------------CHANGE BECOUSE OF DASHBOARD SHOW TOTAL VENDOR-----------------------------------------------------------------------


def vendor_dgm_finance_all(request):
    data = User_Registration.objects.filter(Complete_Details=1, User_type='VENDOR') | User_Registration.objects.filter(
        finance_approval=2,
        Complete_Details=1,
        User_type='VENDOR')

    approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    return render(request, 'officer/dgm_finance_total.html',
                  {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def vendor_dgm_finance_complate(request):
    data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1,
                                            User_type='VENDOR') | User_Registration.objects.filter(finance_approval=2,
                                                                                                   Complete_Details=1,
                                                                                                   User_type='VENDOR')

    approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    # data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc
    return render(request, 'officer/dgm_finance_complete.html',
                  {'data': data, 'approve': approve, 'total': total, 'pending': pending, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


#     # return render(request, 'officer/dgm_finance_complete.html', {'data': data})


def vendor_dgm_finance_pending(request):
    data = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR')
    print(data)

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


def vendor_dgm_finance_pending_rejection_vendor(request):
    data = User_Registration.objects.filter(
        finance_approval=2, Complete_Details=1, User_type='VENDOR')

    approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    # data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    return render(request, 'officer/vendor_dgm_finance_pending_rejection_vendor.html',
                  {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def dgm_work_pending(request):
    data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(work_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending
    return render(request, 'officer/dgm_work_pending.html',
                  {'data': data, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc,
                   'total': total, 'pending': pending, 'approve': approve, })


#     # return render(request, 'officer/dgm_work_pending.html', {'data': data})

def dgm_finance_all_tkc(request):
    data = User_Registration.objects.filter(Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    # data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='VENDOR')

    approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending
    return render(request, 'officer/dgm_finance_all.html',
                  {'data': data, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc,
                   'total': total, 'pending': pending, 'approve': approve})


#     # return render(request, 'officer/dgm_finance_all.html', {'data': data})


def dgm_finance_complete_tkc(request):
    data = User_Registration.objects.filter(finance_approval=1, Complete_Details=1, User_type='TKC')
    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending
    return render(request, 'officer/dgm_finance_complete_tkc.html',
                  {'data': data, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc,
                   'approve': approve, 'total': total, 'pending': pending})


def vendor_dgm_finance_pending_rejection_tkc(request):
    data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    # data = User_Registration.objects.filter(finance_approval=2, Complete_Details=1, User_type='VENDOR')

    approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending
    pending = pending
    return render(request, 'officer/vendor_dgm_finance_pending_rejection_tkc.html',
                  {'data': data, 'total': total, 'pending': pending, 'approve': approve, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def dgm_finance_pending(request):
    data = User_Registration.objects.filter(
        finance_approval=0, Complete_Details=1, User_type='TKC')

    approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                   User_type='TKC').count()
    pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                   User_type='TKC').count()
    total_tkc = approve_tkc + pending_tkc

    approve = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(finance_approval=0, Complete_Details=1, User_type='VENDOR').count()
    total = approve + pending

    return render(request, 'officer/dgm_finance_pending.html',
                  {'data': data, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc, 'total_tkc': total_tkc,
                   'approve': approve, 'total': total, 'pending': pending, })


# # #CGMQC-------------------REMANING------------------------------------------------------------------


def cgm_total_vendor(request):
    data = User_Registration.objects.filter(work_approval=1, finance_approval=1, factory_approval_payment=1,
                                            cgm_approval=0, User_type='VENDOR')
    # data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1,factory_approval_payment=1, User_type='VENDOR')

    approve = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                               User_type='VENDOR').count()
    pending = User_Registration.objects.filter(Complete_Details=1, work_approval=0, cgm_approval=0, finance_approval=0,
                                               User_type='VENDOR', factory_approval=1).count()
    total = approve + pending
    approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                    User_type='NABL').count()
    pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                    User_type='NABL').count()

    total_nabl = approve_nabl + pending_nabl
    return render(request, 'officer/total_cgm_vendor.html',
                  {'data': data, 'approve': approve, 'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                   'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })


#     # return render(request, 'officer/total_cgm_vendor.html', {'data': data})


def cgm_pending_vendor(request):
    data = User_Registration.objects.filter(cgm_approval=0, work_approval=1, finance_approval=1,
                                            factory_approval_payment=1, User_type='VENDOR')
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
    return render(request, 'officer/cgm_pending_vendor.html',
                  {'data': data, 'approve': approve, 'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                   'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })

    # return render(request, 'officer/cgm_pending_vendor.html', {'data': data})


def cgm_complete_vendor(request):
    data = User_Registration.objects.filter(cgm_approval=1, work_approval=1, finance_approval=1,
                                            factory_approval_payment=1)

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
    return render(request, 'officer/cgm_complete_vendor.html',
                  {'data': data, 'approve': approve, 'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                   'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })


#     # return render(request, 'officer/cgm_complete_vendor.html', {'data': data})


def cgm_total_nabl(request):
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

    # return render(request, 'officer/cgm_total_nabl.html', {'data': data})


def cgm_pending_nabl(request):
    data = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, User_type='NABL')

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
    return render(request, 'officer/cgm_pending_nabl.html',
                  {'data': data, 'approve': approve, 'pending': pending, 'total': total, 'approve_nabl': approve_nabl,
                   'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })

    # return render(request, 'officer/cgm_pending_nabl.html', {'data': data})


def nabl_cgm_evaluate(request, id):
    data = User_Registration.objects.filter(User_Id=id)
    if data[0].User_type == "NABL":
        doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
        # Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
        # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)

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
                       'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })


def cgm_approved_nabl(request):
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
    data = User_Registration.objects.filter(Complete_Details=1,
                                            User_type='NABL') | User_Registration.objects.filter(qc_approval=2,
                                                                                                 Complete_Details=1,
                                                                                                 User_type='NABL')

    approve_nabl = User_Registration.objects.filter(Complete_Details=1, qc_approval=1, User_type='NABL').count()

    print(approve_nabl)

    pending_nabl = User_Registration.objects.filter(qc_approval=0, Complete_Details=1,
                                                    User_type='NABL').count()

    total_nabl = approve_nabl + pending_nabl
    return render(request, 'officer/nabl_dgm_qc_total.html',
                  {'data': data, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                   'total_nabl': total_nabl, })


def nabl_dgm_qc_approve(request):
    data = User_Registration.objects.filter(qc_approval=1, Complete_Details=1,
                                            User_type='NABL') | User_Registration.objects.filter(qc_approval=2,
                                                                                                 Complete_Details=1,
                                                                                                 User_type='NABL')

    approve_nabl = User_Registration.objects.filter(Complete_Details=1, qc_approval=1,
                                                    User_type='NABL').count()
    pending_nabl = User_Registration.objects.filter(qc_approval=0, cgm_approval=0, Complete_Details=1,
                                                    User_type='NABL').count()

    total_nabl = approve_nabl + pending_nabl
    return render(request, 'officer/nabl_dgm_qc_total.html',
                  {'data': data, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                   'total_nabl': total_nabl, })


def nabl_dgm_qc_pending(request):
    data = User_Registration.objects.filter(qc_approval=0, Complete_Details=1, User_type='NABL')
    approve_nabl = User_Registration.objects.filter(Complete_Details=1, qc_approval=1,
                                                    User_type='NABL').count()

    pending_nabl = User_Registration.objects.filter(qc_approval=0, cgm_approval=0, Complete_Details=1,
                                                    User_type='NABL').count()

    total_nabl = approve_nabl + pending_nabl
    return render(request, 'officer/nabl_dgm_qc_pending.html',
                  {'data': data, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                   'total_nabl': total_nabl, })


def nabl_dgm_nabl_evaluate(request, id):
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


# def nabl_dgm_qc_evaluate_pending(request, id):
#     data = User_Registration.objects.filter(User_Id=id)
#     if data[0].User_type == "NABL":
#         # doc = NABL_Document.objects.filter(user_id=id)
#         # doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
#         doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
#         return render(request, 'officer/nabl_dgm_qc_evaluate_pending.html',
#                       {'data': data[0], 'doc': doc})


def dgm_work_evaluate(request, id):
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
        return render(request, 'officer/vendor_dgm_work_evaluate.html',
                      {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                       'approve_tkc': approve_tkc,
                       'pending_tkc': pending_tkc, 'total_tkc': total_tkc})

    if data[0].User_type == "TKC":
        doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1)
        return render(request, 'officer/dgm_work_evaluate.html',
                      {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                       'approve_tkc': approve_tkc,
                       'pending_tkc': pending_tkc, 'total_tkc': total_tkc})

    return render(request, 'officer/dgm_work_evaluate.html',
                  {'data': data[0], 'total': total, 'pending': pending, 'approve': approve,
                   'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def dgm_finance_evaluate(request, id):
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
                      {'doc1': doc1, 'data': data[0], 'total': total, 'pending': pending, 'approve': approve,
                       'approve_tkc': approve_tkc,
                       'pending_tkc': pending_tkc, 'total_tkc': total_tkc})

    if data[0].User_type == "TKC":
        doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
        doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)

        return render(request, 'officer/dgm_finance_evaluate.html',
                      {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                       'approve': approve, 'approve_tkc': approve_tkc,
                       'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def dgm_finance_view(request, id):
    data = User_Registration.objects.filter(User_Id=id)
    doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
    doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
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
                   'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


# ---------------------12 april------------------------------------------------------------------------------------------------------

def dgm_work_evaluate2(request, id):
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


def resubmit_finance_evaluate(request, id):
    data = User_Registration.objects.filter(User_Id=id)

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
                       'approve_tkc': approve_tkc,
                       'pending_tkc': pending_tkc, 'total_tkc': total_tkc})
    if data[0].User_type == "TKC":
        doc = TKC_Turnover.objects.filter(user_id=data[0].User_Id)
        doc1 = TKC_Document.objects.filter(user_id=id, Approval_doc=2)
        return render(request, 'officer/tkc_resubmit_dgm_finance_evaluate.html',
                      {'data': data[0], 'doc': doc, 'doc1': doc1, 'total': total, 'pending': pending,
                       'approve': approve, 'approve_tkc': approve_tkc,
                       'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def vendor_cgm_evaluate2(request, id):
    data = User_Registration.objects.filter(User_Id=id)
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

        doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)

        fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
        Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
        tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)
        return render(request, 'officer/vendor_cgm_evaluate_pending2.html',
                      {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
                       'tech_data': tech_data, 'doc': doc, 'Material': Material, 'approve': approve, 'pending': pending,
                       'total': total, 'approve_nabl': approve_nabl,
                       'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })

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


def nabl_cgm_evaluate_test(request, id):
    data = User_Registration.objects.filter(User_Id=id)

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
        doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
        # Test = NABL_Registration_Test.objects.filter(user_id=data[0].User_Id)
        # List_of_Test = NABL_Perform_Test.objects.filter(NABL_Registration_Test_id=Test[0].user_id)

        return render(request, 'officer/nabl_cgm_evaluate_pending.html',
                      {'data': data[0], 'doc': doc, 'approve': approve, 'pending': pending, 'total': total,
                       'approve_nabl': approve_nabl,
                       'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })


def nabl_dgm_qc_evaluate(request, id):
    data = User_Registration.objects.filter(User_Id=id)
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
        return render(request, 'officer/nabl_dgm_qc_evaluate.html',
                      {'data': data[0], 'doc': doc, 'approve': approve, 'pending': pending, 'total': total,
                       'approve_nabl': approve_nabl,
                       'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })


# ----------------------------------------13 april evn---------------------------------------------------

def resubmit_view(request, id):
    data = User_Registration.objects.filter(User_Id=id)

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

        return render(request, 'officer/vendor_resubmit_pending_view.html',
                      {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                       'approve_nabl': approve_nabl,
                       'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                       'total_tkc': total_tkc})

    if data[0].User_type == "TKC":
        doc = TKC_Document.objects.filter(user_id=id, Approval_doc=1)

        return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                      {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                       'approve_nabl': approve_nabl,
                       'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                       'total_tkc': total_tkc})

    if data[0].User_type == "NABL":
        doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
        return render(request, 'officer/nabl_resubmit_pending_view_work.html',
                      {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                       'approve_nabl': approve_nabl,
                       'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                       'total_tkc': total_tkc})

    return render(request, 'officer/tkc_resubmit_pending_view_work.html',
                  {'data': data[0], 'doc': doc, 'total': total, 'pending': pending, 'approve': approve,
                   'approve_nabl': approve_nabl,
                   'pending_nabl': pending_nabl, 'approve_tkc': approve_tkc, 'pending_tkc': pending_tkc,
                   'total_tkc': total_tkc})


def dgm_work_evaluate_save(request, id):
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

            doc = TKC_Document.objects.filter(
                user_id=data[0].User_Id, Approval_doc=1)
            counter = 100
            comment = 0
            nz = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                data.Primary_verification_Date = datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status = 1
                elif result == 'NOT':
                    nz = 1
                    user = User_Registration.objects.get(User_Id=id)
                    user.work_approval = 2
                    user.save()
                    data.Primary_verification_Status = 2
                    data.Status = 0
                    nameee = data.Types_of_Docs
                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    # for server set proxy
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                        nameee) + "&v4=" + str() + "&v5=" + str(
                        'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(works)') + "&v9=" + str(
                        'https://qcportal.mpcz.in/')
                    # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                    test = data.Primary_remark_rejection_counter
                    test = test + 1
                    data.Primary_remark_rejection_counter = test
                    if test >= 3:
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
                user_id=id).filter(Primary_verification_Status=2)
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
                data.work_approval = 1
                data.save()
                send_mail(
                    'Approval status of DGM(Works) ',
                    'Hello ! Your are approved by DGM (Works)',
                    settings.EMAIL_HOST_USER,
                    [data.Email_Id],
                    fail_silently=False,
                )
            data = User_Registration.objects.filter(
                work_approval=0, Complete_Details=1, User_type='TKC')

            return render(request, 'officer/dgm_work_pending.html',
                          {'data': data, 'doc': doc, 'total': total, 'approve': approve, 'pending': pending,
                           'approve_tkc': approve_tkc,
                           'pending_tkc': pending_tkc, 'total_tkc': total_tkc})

            # return render(request, 'officer/dgm_work_pending.html',
            #               {'data': data, 'doc': doc})
        if data[0].User_type == "VENDOR":

            data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR')

            approve = User_Registration.objects.filter(Complete_Details=1, work_approval=1,
                                                       User_type='VENDOR').count()
            pending = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='VENDOR').count()
            total = approve + pending

            approve_tkc = User_Registration.objects.filter(Complete_Details=1, finance_approval=1,
                                                           User_type='TKC').count()
            pending_tkc = User_Registration.objects.filter(finance_approval=0, Complete_Details=1,
                                                           User_type='TKC').count()
            total_tkc = approve_tkc + pending_tkc

            doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
            counter = 100
            comment = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                data.Primary_verification_Date = datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status = 1
                else:
                    user = User_Registration.objects.get(User_Id=id)
                    user.work_approval = 2
                    data.Primary_verification_Status = 2
                    data.Status = 0
                    nameee = data.Types_of_Docs
                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    # for server set proxy
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                        nameee) + "&v4=" + str() + "&v5=" + str(
                        'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(works)') + "&v9=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

                    send_mail(
                        'Approval status of DGM(Works) ',
                        'Hello ! Your are not approved by DGM (Works)',
                        settings.EMAIL_HOST_USER,
                        [user.Email_Id],
                        fail_silently=False,
                    )

                    test = data.Primary_remark_rejection_counter
                    if test >= 3:
                        user.final_rejection = 1
                        user.work_approval = -1
                        send_mail(
                            'Approval status of DGM(Works) ',
                            'Hello ! Your application is finally rejected by DGM (Works) now.',
                            settings.EMAIL_HOST_USER,
                            [user.Email_Id],
                            fail_silently=False,
                        )
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
                data.work_approval = 1
                data.save()
                send_mail(
                    'Approval status of DGM(Works) ',
                    'Hello ! Your are approved by DGM (Works)',
                    settings.EMAIL_HOST_USER,
                    [data.Email_Id],
                    fail_silently=False,
                )
                if data.finance_approval == 1:
                    send_mail(
                        'Approved Profile ',
                        'Hello ! Your profile approved make payment for FI',
                        settings.EMAIL_HOST_USER,
                        [data.Email_Id],
                        fail_silently=False,
                    )
                sms = User_Registration.objects.get(User_Id=id)
                mobile = sms.ContactNo
                name_sms = sms.CompanyName_E
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                # for server set proxy
                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007180239560227172&mobile_number=" + str(
                    mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                    'https://qcportal.mpcz.in/') + "&v4=" + str('10000')
                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

            data = User_Registration.objects.filter(
                work_approval=0, Complete_Details=1, User_type='VENDOR')

            return redirect('vendor_dgm_work_pending')
    data = User_Registration.objects.filter(work_approval=0, Complete_Details=1, User_type='TKC')
    return render(request, 'officer/dgm_work_pending.html',
                  {'data': data, 'total': total, 'approve': approve, 'pending': pending, 'approve_tkc': approve_tkc,
                   'pending_tkc': pending_tkc, 'total_tkc': total_tkc})


def dgm_finance_evaluate_save(request, id):
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
            doc = TKC_Document.objects.filter(
                user_id=data[0].User_Id, Approval_doc=2)
            counter = 100
            comment = 0
            nn = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                data.Primary_verification_Date = datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status = 1
                elif result == 'NOT':
                    nn = 1
                    user = User_Registration.objects.get(User_Id=id)
                    user.finance_approval = 2
                    user.save()
                    data.Primary_verification_Status = 2
                    data.Status = 0
                    test = data.Primary_remark_rejection_counter
                    # nameee = data.document_name
                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    # for server set proxy
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
                    # mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                    # nameee) + "&v4=" + str() + "&v5=" + str(
                    # 'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(finance)') + "&v9=" + str(
                    # 'https://qcportal.mpcz.in/')
                    # response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

                    if test >= 3:
                        user.final_rejection = 1
                        user.finance_approval = -1
                        send_mail(
                            'Approval status of DGM(Finance) ',
                            'Hello ! Your application is finally rejected by DGM (Finance) now',
                            settings.EMAIL_HOST_USER,
                            [user.Email_Id],
                            fail_silently=False,
                        )
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
                data.finance_approval = 1
                data.save()
                send_mail(
                    'Approval status of DGM(Finance) ',
                    'Hello ! Your application is approved by DGM (Finance).',
                    settings.EMAIL_HOST_USER,
                    [data.Email_Id],
                    fail_silently=False,
                )

            data = User_Registration.objects.filter(
                finance_approval=0, Complete_Details=1, User_type='TKC')
            return render(request, 'officer/dgm_finance_pending.html', {'data': data})
        if data[0].User_type == "VENDOR":
            doc = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
            counter = 100
            comment = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                data.Primary_verification_Date = datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status = 1
                else:
                    user = User_Registration.objects.get(User_Id=id)
                    user.finance_approval = 2
                    data.Primary_verification_Status = 2
                    data.Status = 0
                    nameee = data.document_name
                    sms = User_Registration.objects.get(User_Id=id)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                    # for server set proxy
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007490758019902962&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                        nameee) + "&v4=" + str() + "&v5=" + str(
                        'and other') + "&v6=" + str() + "&v7=" + str() + "&v8=" + str('DGM(finance)') + "&v9=" + str(
                        'https://qcportal.mpcz.in/')
                    response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

                    send_mail(
                        'Rejection status of DGM(Finance) ',
                        'Hello ! Your are not approved by DGM (Finance)',
                        settings.EMAIL_HOST_USER,
                        [user.Email_Id],
                        fail_silently=False,
                    )
                    test = data.Primary_remark_rejection_counter
                    if test >= 3:
                        user.final_rejection = 1
                        user.finance_approval = -1
                        send_mail(
                            'Rejection status of DGM(Finance) ',
                            'Hello ! Your application is finally rejected by DGM (Finance) now',
                            settings.EMAIL_HOST_USER,
                            [user.Email_Id],
                            fail_silently=False,
                        )
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
                data.finance_approval = 1
                data.save()
                send_mail(
                    'Approval status of DGM(Finance) ',
                    'Hello ! You are approved by DGM (Finance)',
                    settings.EMAIL_HOST_USER,
                    [data.Email_Id],
                    fail_silently=False,
                )
                if data.work_approval == 1:
                    send_mail(
                        'Approved Profile ',
                        'Hello ! Your profile approved make payment for FI',
                        settings.EMAIL_HOST_USER,
                        [data.Email_Id],
                        fail_silently=False,
                    )
                sms = User_Registration.objects.get(User_Id=id)
                mobile = sms.ContactNo
                name_sms = sms.CompanyName_E
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # proxyDict = {"http" : "proxy.mpcz.in:8000"}
                # for server set proxy
                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}

                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007180239560227172&mobile_number=" + str(
                    mobile) + "&v1=" + str(name_sms) + "&v2=" + str() + "&v3=" + str(
                    'https://qcportal.mpcz.in/') + "&v4=" + str('10000')
                response_data = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
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
            return render(request, 'officer/dgm_finance_pending.html',
                          {'data': data, 'total': total, 'approve': approve, 'pending': pending,
                           'approve_tkc': approve_tkc,
                           'pending_tkc': pending_tkc, 'total_tkc': total_tkc})

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


def vendor_cgm_evaluate(request, id):
    data = User_Registration.objects.filter(User_Id=id)

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
        doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)

        doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)

        fac = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
        Material = Vendor_Material_Details.objects.filter(user_id=data[0].User_Id)
        tech_data = Vendor_Technical_Details.objects.filter(user_id=data[0].User_Id)

        return render(request, 'officer/vendor_cgm_evaluate.html',
                      {'data': data[0], 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
                       'tech_data': tech_data, 'total': total, 'approve': approve, 'pending': pending,
                       'approve_nabl': approve_nabl,
                       'pending_nabl': pending_nabl, 'total_nabl': total_nabl})

    doc = Vendor_Document.objects.filter(user_id=data[0].User_Id)
    Factory = Vendor_Factory_Details.objects.filter(user_id=data[0].User_Id)
    Material = Add_material.objects.filter(user_id=data[0].User_Id)
    return render(request, 'officer/vendor_wnp_evaluate.html',
                  {'data': data, 'doc': doc, 'Factory': Factory, 'Material': Material, 'total': total,
                   'approve': approve, 'pending': pending, 'approve_nabl': approve_nabl,
                   'pending_nabl': pending_nabl, 'total_nabl': total_nabl, })


def nabl_dgm_qc_evaluate_pending(request, id):
    data = User_Registration.objects.filter(User_Id=id)
    approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                    User_type='NABL').count()
    pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                    User_type='NABL').count()

    total_nabl = approve_nabl + pending_nabl
    if data[0].User_type == "NABL":
        # doc = NABL_Document.objects.filter(user_id=id)
        # doc1 = Vendor_BalanceSheet.objects.filter(user_id=data[0].User_Id)
        doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
        return render(request, 'officer/nabl_dgm_qc_evaluate_pending.html',
                      {'data': data[0], 'doc': doc, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                       'total_nabl': total_nabl})


def nabl_dgm_qc_evaluate_save(request, id):
    if request.method == 'POST':
        data = User_Registration.objects.filter(User_Id=id)
        if data[0].User_type == "NABL":
            approve_nabl = User_Registration.objects.filter(Complete_Details=1, cgm_approval=1,
                                                            User_type='NABL').count()
            pending_nabl = User_Registration.objects.filter(qc_approval=1, cgm_approval=0, Complete_Details=1,
                                                            User_type='NABL').count()

            total_nabl = approve_nabl + pending_nabl

            doc = NABL_Document.objects.filter(user_id=data[0].User_Id)
            counter = 100
            comment = 0
            kk = 0
            for data in doc:
                comm = request.POST.get(str(comment))
                result = request.POST.get(str(counter))
                if comm != '':
                    data.Primary_remark = comm
                data.Primary_verification_Date = datetime.now().date()
                if result == 'OK':
                    data.Primary_verification_Status = 1
                else:
                    kk = 1
                    user = User_Registration.objects.get(User_Id=id)
                    user.qc_approval = 2

                    data.Primary_verification_Status = 2
                    data.Status = 0
                    test = data.Primary_remark_rejection_counter
                    if test >= 3:
                        user.final_rejection = 1
                        user.qc_approval = -1
                        send_mail(
                            'Approval status of DGM(QC) ',
                            'Hello ! Your application is finally rejected by DGM (QC) now',
                            settings.EMAIL_HOST_USER,
                            [user.Email_Id],
                            fail_silently=False,
                        )
                    user.save()
                    test = test + 1
                    data.Primary_remark_rejection_counter = test
                data.save()
                counter = counter + 1
                comment = comment + 1
            data = NABL_Document.objects.filter(
                user_id=id).filter(Primary_verification_Status=2)

            if kk == 1:
                send_mail(
                    'Rejection status of DGM(QC) ',
                    'Hello ! Your application is not approved by DGM (QC).',
                    settings.EMAIL_HOST_USER,
                    [user.Email_Id],
                    fail_silently=False,
                )
            else:
                pass

            if not data:
                data = User_Registration.objects.get(User_Id=id)
                data.qc_approval = 1
                data.save()

                send_mail(
                    'Approval status of DGM(QC) ',
                    'Hello ! Your application is approved by DGM (QC).',
                    settings.EMAIL_HOST_USER,
                    [data.Email_Id],
                    fail_silently=False,
                )
            data = User_Registration.objects.filter(
                qc_approval=0, Complete_Details=1, User_type='NABL')
            return render(request, 'officer/nabl_dgm_qc_pending.html',
                          {'data': data, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                           'total_nabl': total_nabl, })

        data = User_Registration.objects.filter(
            qc_approval=0, Complete_Details=1, User_type='NABL')
        return render(request, 'officer/nabl_dgm_qc_pending.html',
                      {'data': data, 'approve_nabl': approve_nabl, 'pending_nabl': pending_nabl,
                       'total_nabl': total_nabl, })
