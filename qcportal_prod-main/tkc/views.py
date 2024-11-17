from django.views.decorators.csrf import csrf_exempt
from paywix.payu import Payu
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from main.models import *
from tkc.models import *
from fqp.models import *
from tkc.serializer import BalanceSheet_Serializer, TKC_Document_Serializer, TKC_Turnover_Serializer, Consumer_bidSerializer,UserSerializer,ConsumerSerializer,UserCompanyDataMainSerializer,Contractor_selectionSerializer,Contractor_selectionSerializerGet,Consumer_bidSerializer2,tkc_paymentSerializer,UserCompanyDataSerializer,CompanyDataMainSerializer
# ,ConsumerSerializer_1
from datetime import datetime as dt,timedelta
import datetime 
from django.contrib import messages
import json
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd
import requests
from rest_framework.views import APIView
from django.db.models import Q
from django.core import validators
from nabl.models import *

from rest_framework import status #by ravindra
from django.http import HttpResponseBadRequest #by ravindra
import schedule #by ravindra
import datetime as dt
import time as t #by ravindra
import threading #by ravindra
from django.http import Http404
# Create your views here.
from main import custom_message as cmsg
def basic(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    
    if data.Authentication_id :
        if data.activation_before_expired == 0 and data.activation_after_expired == 0:
            cert = data.Authentication_id
            exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').last()
            expi_date = exp.Doc_expiry_date
            to_daaa =datetime.datetime.today()
            if data.Oyt is not None:
                oyt_name = TKC_Payment.objects.get(id = data.Oyt )
                name = oyt_name.Name
                print("gggggg",name)
                return render(request, 'tkc/basicinfo.html', {"userdata": data,'con':con,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'oyt':name})
            return render(request, 'tkc/basicinfo.html', {"userdata": data,'cert':cert,'con':con,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa, 'oyt':name})
        else:
            cert = data.Authentication_id
            exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').first()
            expi_date = exp.Doc_expiry_date
            to_daaa =datetime.datetime.today()
            if data.Oyt is not None:
                oyt_name = TKC_Payment.objects.get(id = data.Oyt )
                name = oyt_name.Name
                print("gggggg",name)
                return render(request, 'tkc/basicinfo.html', {"userdata": data,'cert':cert,'con':con,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'oyt':name})
            return render(request, 'tkc/basicinfo.html', {"userdata": data,'cert':cert,'exp':exp,'con':con,'expi_date':expi_date,'to_daaa':to_daaa, 'oyt':name})
            
    else:
        
        if data.Oyt is not None:
            oyt_name = TKC_Payment.objects.get(id = data.Oyt )
            name = oyt_name.Name
            print("gggggg",name)
            return render(request, 'tkc/basicinfo.html', {"userdata": data,'oyt':name})
        return render(request, 'tkc/basicinfo.html', {"userdata": data})
                

    return render(request, 'tkc/basicinfo.html',{"userdata": data,'con':con})


def tkc_view_profile(request):
    if request.session.has_key('otp'):
        data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        vendor_document = TKC_Document.objects.filter(user_id=user_id)
        vendor_balance = TKC_Turnover.objects.filter(user_id=user_id)
        abcde = UserCompanyDataMain.objects.get(user_id_id=data)
        return render(request, 'tkc/tkc_view_profile.html',
                      {"basic": data, 'company': abcde, 'vendor_document': vendor_document,
                       'vendor_balance': vendor_balance})

def update_profile(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    userid = data.User_Id
    abcde = UserCompanyDataMain.objects.get(user_id_id=data)
    if data.profile_update_fee == 1 or data.cgm_approval == 0:
        if request.method == "POST":
            data11 = User_Registration.objects.filter(
                Otp=request.session['otp'],User_type = request.session['User_type'])
            abc = UserCompanyDataMain.objects.get(user_id_id=data)
            data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            data1.Type_of_business = request.POST['two']
            data1.CompanyName_E = request.POST['four']
            data1.Authorised_person_E = request.POST['five']
            data1.ContactNo = request.POST['six']
            data1.Email_Id = request.POST['seven']
            data1.User_zone = request.POST['zero']
            data1.save()
            abc.Company_Pan_No = request.POST['eight']
            abc.Company_Gumastha_No = request.POST['nine']
            abc.Company_Gst_No = request.POST['ten']
            # abc.Registration_Date  = request.POST['eleven']
            abc.Company_Fax = request.POST['twelve']
            # ****
            abc.Company_add_1 = request.POST['thireteen']
            abc.Company_add_2 = request.POST['fourteen']
            abc.Company_pin_code = request.POST['fifteen']
            abc.Company_dist = request.POST['sixteen']
            abc.Company_state = request.POST['seventeen']
            abc.Company_t_add_1 = request.POST['eighteen']
            abc.Company_t_add_2 = request.POST['nineteen']
            abc.Company_t_pin_code = request.POST['twenty']
            abc.Company_t_dist = request.POST['twentyone']
            abc.Company_t_state = request.POST['twentytwo']
            abc.save()
            return redirect('/tkc/basic')
    else:
        return HttpResponse("You have to pay profile update fee")
    if data.Authentication_id :
        if data.activation_before_expired == 0 and data.activation_after_expired == 0:
            abcde = UserCompanyDataMain.objects.get(user_id_id=data)
            cert = data.Authentication_id
            exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').last()
            expi_date = exp.Doc_expiry_date
            to_daaa =datetime.datetime.today()
            return render(request, 'tkc/update_vendor_profile.html', {"basic": data, 'company': abcde,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
        else:
            abcde = UserCompanyDataMain.objects.get(user_id_id=data)
            cert = data.Authentication_id
            exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').first()
            expi_date = exp.Doc_expiry_date
            to_daaa =datetime.datetime.today()
            return render(request, 'tkc/update_vendor_profile.html', {"basic": data, 'company': abcde,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})

    return render(request, 'tkc/update_vendor_profile.html', {"basic": data, 'company': abcde})


def tkc_reg_seven(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)

            # if data1.page_12:
            #     return redirect("vendor_reg_fifteen")

            # if data1.page_11:
            #     return redirect("vendor_reg_twelve")

            if data1.page_10:
                return redirect("tkc_reg_eleven")

            if data1.page_9:
                return redirect("tkc_reg_ten")

            if data1.page_8:
                return redirect("tkc_reg_nine")

        return render(request, 'tkc/tkc_reg7.html',{'con':con})
    return render(request, 'tkc/tkc_reg7.html',{'con':con})


def tkc_reg_eight(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data.Experience = request.POST.get('work_experience')
        data.Turnover = request.POST.get('turn_over')
        data.Oyt = request.POST.get('VendorType')
        data.Upgrade_Oyt = request.POST.get('VendorType')
        print("gggggggggggggggg",data.Oyt)
        data.save()
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            data1.page_8 = 1
            data1.save()
        else:
            user = User_Registration_Check_Status(User=data, page_8=1)
            user.save()
        return redirect("tkc_reg_nine")
    payment = TKC_Payment.objects.filter(~Q(id=9))
    return render(request, 'tkc/tkc_reg8.html', {'payment': payment,'con':con})

def tkc_reg_nine(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        financial_year = request.POST.get('year12')
        Amount = request.POST.get('input_income')
        data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                Status=1)
        data1.save()

        financial_year = request.POST.get('year13')
        Amount = request.POST.get('input_income1')
        data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                Status=1)
        data1.save()

        financial_year = request.POST.get('year14')
        Amount = request.POST.get('input_income2')
        data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                Status=1)
        data1.save()


        
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            data1.page_9 = 1
            data1.save()
        else:
            user = User_Registration_Check_Status(User=data, page_9=1)
            user.save()
        return redirect("tkc_reg_ten")
    return render(request, 'tkc/tkc_reg9.html',{'con':con})

def tkc_reg_ten(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.method == "POST":
        if request.session.has_key('otp'):
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
            if request.method == "POST":
                data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
                user_id = data.User_Id
                

                try:

                    office_name = request.POST.get('five')
                    gst_card_no = request.POST.get('six')
                    issu_date = request.POST.get('seven')
                    ex_date = request.POST.get('eight')
                    document = request.FILES['nine']
                  
                    data2 = TKC_Document(user_id=user_id, Types_of_Docs='GST With Challan', Issued_office_Name=office_name,
                                        Document_Number=gst_card_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Doc_expiry_date=ex_date, Approval_doc=2)
                except Exception as e:
                    office_name = request.POST.get('five')
                    gst_card_no = request.POST.get('six')
                    issu_date = request.POST.get('seven')
                    document = request.FILES['nine']
                    data2 = TKC_Document(user_id=user_id, Types_of_Docs='GST With Challan', Issued_office_Name=office_name,
                                        Document_Number=gst_card_no, Ddocfile=document, Doc_issue_date=issu_date, Approval_doc=2)

               

                try:    

                    office_name = request.POST.get('fifteen')
                    document_no = request.POST.get('sixteen')
                    issu_date = request.POST.get('seventeen')
                    ex_date = request.POST.get('eighteen')
                    document = request.FILES['nineteen']
                    data4 = TKC_Document(user_id=user_id, Types_of_Docs='Declaration of Contractor and Supervisor',
                                        Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Doc_expiry_date=ex_date, Approval_doc=1)

                except Exception as e:
                    office_name = request.POST.get('fifteen')
                    document_no = request.POST.get('sixteen')
                    issu_date = request.POST.get('seventeen')
                    document = request.FILES['nineteen']
                    data4 = TKC_Document(user_id=user_id, Types_of_Docs='Declaration of Contractor and Supervisior',
                                        Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Approval_doc=1)


         
                office_name = request.POST.get('twentee')
                document_no = request.POST.get('twentee_one')
                issu_date = request.POST.get('twentee_two')
                ex_date = request.POST.get('twentee_three')
                document = request.FILES['twentee_four']
                data5 = TKC_Document(user_id=user_id, Types_of_Docs='Electrical License',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=1)

               


                try:

                    office_name = request.POST.get('twentee_five')
                    document_no = request.POST.get('twentee_six')
                    issu_date = request.POST.get('twentee_seven')
                    ex_date = request.POST.get('twentee_eight')
                    document = request.FILES['twentee_nine']
                    data6 = TKC_Document(user_id=user_id, Types_of_Docs='EPF With Challan', Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Doc_expiry_date=ex_date, Approval_doc=2)

                except Exception as e:
                    office_name = request.POST.get('twentee_five')
                    document_no = request.POST.get('twentee_six')
                    issu_date = request.POST.get('twentee_seven')
                    document = request.FILES['twentee_nine']
                    data6 = TKC_Document(user_id=user_id, Types_of_Docs='EPF With Challan', Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Approval_doc=2)



                try:
                    office_name = request.POST.get('thiety')
                    document_no = request.POST.get('thiety_one')
                    issu_date = request.POST.get('thiety_two')
                    ex_date = request.POST.get('thiety_three')
                    document = request.FILES['thiety_four']
                    data7 = TKC_Document(user_id=user_id, Types_of_Docs='ESIC REGISTRATION WITH CHALLAN',
                                        Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Doc_expiry_date=ex_date, Approval_doc=2)

                except Exception as e:

                    office_name = request.POST.get('thiety')
                    document_no = request.POST.get('thiety_one')
                    issu_date = request.POST.get('thiety_two')
                    document = request.FILES['thiety_four']
                    data7 = TKC_Document(user_id=user_id, Types_of_Docs='ESIC Registration With Challan',
                                        Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Approval_doc=2)

                try:  

                    office_name = request.POST.get('thiety_five')
                    document_no = request.POST.get('thiety_six')
                    issu_date = request.POST.get('thiety_seven')
                    ex_date = request.POST.get('thiety_eight')
                    document = request.FILES['thiety_nine']
                    data8 = TKC_Document(user_id=user_id, Types_of_Docs='Experience Certificate',
                                        Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Doc_expiry_date=ex_date, Approval_doc=1)

                except Exception as e:
                    office_name = request.POST.get('thiety_five')
                    document_no = request.POST.get('thiety_six')
                    issu_date = request.POST.get('thiety_seven')
                    document = request.FILES['thiety_nine']
                    data8 = TKC_Document(user_id=user_id, Types_of_Docs='Experience Certificate',
                                        Issued_office_Name=office_name,
                                        Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                        Approval_doc=1)
           




                office_name = request.POST.get('fifty')
                document_no = request.POST.get('fifty_one')
                issu_date = request.POST.get('fifty_two')
                document = request.FILES['fifty_three']
                data11 = TKC_Document(user_id=user_id, Types_of_Docs='PAN Card Number', Issued_office_Name=office_name,
                                     Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                     Approval_doc=1)

                             
                if data2 and data4 and data5 and data6 and data7 and data8  and data11 :
                    data2.save()
                    data4.save()
                    data5.save()
                    data6.save()
                    data7.save()
                    data8.save()
                    data11.save()
                    if User_Registration_Check_Status.objects.filter(User=data).exists():
                        data1 = User_Registration_Check_Status.objects.get(User=data)
                        data1.page_10 = 1
                        data1.save()
                    else:
                        user = User_Registration_Check_Status(User=data, page_10=1)
                        user.save()
            return render(request, 'tkc/tkc_declration.html')
    data = Sample_Document.objects.all()
    return render(request, 'tkc/tkc_reg10.html', {'data': data,'con':con})

def tkc_update(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.session.has_key('otp'):
        if TKC_Document.objects.filter(complete_data=1).exists():
            return redirect('tkc_reg_eleven')
        else:
            return redirect('tkc_reg_eight')
    return render(request, 'tkc/tkc_update.html',{'con':con})


import random
import math
def tkc_reg_eleven(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.method == "POST":
        aa = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        mobile = data.ContactNo
        name_sms = data.CompanyName_E
        def generateOTP():
            OTP = ""
            digits = "0123456789"
            for i in range(6):
                OTP += digits[math.floor(random.random() * 10)]
            return OTP
        otp = generateOTP()
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()

        # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(mobile) + "&v1="+ str(name_sms) + "&v2=" + str()
        response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = mobile)
        sms_template.save()
        # abc = request.POST.get('rca_ven')
        # if abc == 'checked':
        #     aa.update(rca_vendor=1)
        request.session['verify'] = otp
        return redirect("/tkc/vendor_otp_verify")
    return render(request, 'tkc/tkc_reg11.html',{'con':con})

        
from datetime import date
from datetime import time
from datetime import datetime
import datetime
        
def vendor_otp_verify(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.session.has_key('otp'):
        if request.method == "POST":
            otp = request.POST.get('otp')
            if otp == request.session['verify']:
                data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
                data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
                reg_date = datetime.datetime.now().date()
                data11.update(complete_data=1,Complete_Details=1,reg_date=reg_date)
                user_id = data.User_Id
                mobile = data.ContactNo
                name_sms = data.CompanyName_E
                zone = data.User_zone
                
                # send_mail(
                    # 'Your final registration is completed ',
                    # 'Hello thanks for Final registration as a Vendor',
                    # settings.EMAIL_HOST_USER,
                    # [data.Email_Id],
                    # fail_silently=False,
                # )
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007005572119738232&mobile_number=" + str(mobile) + "&v1="+ str(name_sms) + "&v2=" + "MP" + str(zone)
                response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1007005572119738232',date = datetime.datetime.now(),mobile_number = mobile)
                sms_template.save()
                
                officer =  Officer.objects.filter(rank="Deputy General Manager",user_zone=zone)
                
                for i in officer:
                    o_mobile = i.mobile
                    name = i.employ_name
                    rank = i.rank
                    
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007897298975414680&mobile_number=" + str(o_mobile) + "&v1="+ str(name) + "&v2=" + " " + str(rank) + "&v3=" + str(name_sms) + "&v4=" + str()
                    response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                    
                    sms_template = message_template_log(template_id = '1007897298975414680',date = datetime.datetime.now(),mobile_number = o_mobile)
                    sms_template.save()
                    
                
                return redirect('/tkc/basic')
            else:
              
                return render(request, 'tkc/vendor_verify_otp.html',{'con':con})
            
    return render(request, 'tkc/vendor_verify_otp.html',{'con':con})

def tkc_sd_payment(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    oyt = data.Oyt
    payment = TKC_Payment.objects.get(id=oyt)
    txnid = uuid.uuid1()
    client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
    param = {"txnid": txnid, "amount": payment.payment, "productinfo": "sd deposit",
             "firstname": data.Authorised_person_E,
             "email": data.Email_Id}
    apiHash = payu_sdk.Hasher.generate_hash(param)
    data3 = Payudata_main(User_Id=data, Payu_Status='pending', Txdid=txnid,
                          Productinfo="sd deposit",
                          Firstname=data.Authorised_person_E, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                          Netamount_Debited=payment.payment
                          )
    data3.save()
    return render(request, 'main/payu_checkout_registration.html',
                  {"posted": apiHash, "txnid": txnid, "amount": payment.payment, 'firstname': data.Authorised_person_E,
                   "email": data.Email_Id, "productinfo": "sd deposit", "phone": data.ContactNo})


def tkc_reg_twelve(request):
    return render(request, 'tkc/tkc_reg12.html')


def base(request):
    return render(request, 'tkc/user_base.html')



# def declare(request):
#     return render(request, 'tkc/tkc_declration.html')


def message(request):
    return render(request, 'tkc/message.html')


def update_message(request):
    return render(request, 'tkc/message.html')


def activation(request):
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime
    
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id

        con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        
        if data.cgm_approval == 1 and data.blacklisted == 0 :
            doc = TKC_Document.objects.filter(user_id=user_id, Types_of_Docs='Electrical License')
            exp = datetime.datetime.fromordinal(doc[0].Doc_expiry_date.toordinal())
            upd = datetime.datetime.fromordinal(data.Updated_Date.toordinal())

            data1 = exp - upd
            expiry_date = exp
            registration_date = upd
            cert = data.Authentication_id
            if data.activation_before_expired == 0 and data.activation_after_expired == 0:
                exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').last()
                expi_date = exp.Doc_expiry_date
                print("fffffffff",expi_date)
                to_daaa =datetime.datetime.today()
                return render(request, 'tkc/activation.html', {"userdata": data, "doc": doc[0], "days": data1.days,'con':con,
                                                            "expiry_date": expiry_date,
                                                            "registration_date": registration_date,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
            else:
                exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').first()
                expi_date = exp.Doc_expiry_date
                print("fffffffff",expi_date)
                to_daaa =datetime.datetime.today()
                return render(request, 'tkc/activation.html', {"userdata": data, "doc": doc[0], "days": data1.days,'con':con,
                                                            "expiry_date": expiry_date,
                                                            "registration_date": registration_date,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
        else:
            if data.Authentication_id:
                if data.activation_before_expired == 0 and data.activation_after_expired == 0:
                    cert = data.Authentication_id
                    exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').last()
                    expi_date = exp.Doc_expiry_date
                    to_daaa =datetime.datetime.today()
                    return render(request, 'tkc/tkc_review.html',{'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'con':con,})

                else:
                    cert = data.Authentication_id
                    exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').first()
                    expi_date = exp.Doc_expiry_date
                    to_daaa =datetime.datetime.today()
                    return render(request, 'tkc/tkc_review.html',{'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa,'con':con,})

            return render(request, 'tkc/tkc_review.html')

    return redirect('/')




import payu_sdk
import uuid


def activation_after_expired(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        
        user_id = data.User_Id
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            data1.page_10 = 0
            data1.page_11 = 0
            data1.save()
        txnid = uuid.uuid1()
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        param = {"txnid": txnid, "amount": "2360.00", "productinfo": "Activation Fee After Expired",
                 "firstname": data.Authorised_person_E,
                 "email": data.Email_Id}
        apiHash = payu_sdk.Hasher.generate_hash(param)
        data3 = Payudata_main(User_Id=data,Payu_Status='pending', Txdid=txnid,
                          Productinfo="Activation Fee After Expired",
                          Firstname=data.Authorised_person_E, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                          Netamount_Debited='2360.00'
                          )
        data3.save()
        return render(request, 'main/payu_checkout_registration.html',
                      {"posted": apiHash, "txnid": txnid, "amount": "2360.00", 'firstname': data.Authorised_person_E,
                       "email": data.Email_Id, "productinfo": "Activation Fee After Expired", "phone": data.ContactNo})
    return render(request, 'tkc/basicinfo.html', {"userdata": data,'con':con})


def activation_before_expired(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.session.has_key('otp'):
        
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        
        user_id = data.User_Id
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            data1.page_10 = 0
            data1.page_9 = 0
            data1.save()
        txnid = uuid.uuid1()
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        param = {"txnid": txnid, "amount": "590.00", "productinfo": "Activation Fee Befour Expired",
                 "firstname": data.Authorised_person_E,
                 "email": data.Email_Id}
        apiHash = payu_sdk.Hasher.generate_hash(param)
        data3 = Payudata_main(User_Id = data,Payu_Status='pending', Txdid=txnid,
                          Productinfo="Activation Fee Befour Expired",
                          Firstname=data.Authorised_person_E, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                          Netamount_Debited='590.00'
                          )
        data3.save()
        return render(request, 'main/payu_checkout_registration.html',
                      {"posted": apiHash, "txnid": txnid, "amount": "590.00", 'firstname': data.Authorised_person_E,
                       "email": data.Email_Id, "productinfo": "Activation Fee Befour Expired", "phone": data.ContactNo,'con':con})
    return render(request, 'tkc/basicinfo.html', {"userdata": data})


def upgrade(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        
        if data.Authentication_id:
            if data.activation_before_expired == 0 and data.activation_after_expired == 0:
                cert = data.Authentication_id
                exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').last()
                expi_date = exp.Doc_expiry_date
                to_daaa =datetime.datetime.today()

                doc = TKC_Document.objects.filter(user_id=user_id, Types_of_Docs='Electrical License').last()
                exp_date = datetime.datetime.fromordinal(doc.Doc_expiry_date.toordinal())
                upd = datetime.datetime.fromordinal(data.Updated_Date.toordinal())
                print("upd",upd)
                data1 = exp_date - upd
                print("data1",type(data1))
                if exp_date >= upd:
                    if data.cgm_approval == 1 and data.blacklisted == 0 :
                        
                        all_contractor = TKC_Payment.objects.all()
                        contractor = TKC_Payment.objects.get(id=data.Oyt)
                        return render(request, 'tkc/upgrade_tkc_two.html',
                                    {'data': data,'con':con ,'all_contractor': all_contractor, 'contractor': contractor,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
                    else:
                        return render(request, 'tkc/tkc_review.html',{'con':con})
                else:
                    return HttpResponse('Activate First')
            else:
                cert = data.Authentication_id
                exp = TKC_Document.objects.filter(user_id=data.User_Id, Types_of_Docs='Electrical License').first()
                expi_date = exp.Doc_expiry_date
                to_daaa =datetime.datetime.today()

                doc = TKC_Document.objects.filter(user_id=user_id, Types_of_Docs='Electrical License').first()
                exp_date = datetime.datetime.fromordinal(doc.Doc_expiry_date.toordinal())
                upd = datetime.datetime.fromordinal(data.Updated_Date.toordinal())
                print("upd",upd)
                data1 = exp_date - upd
                print("data1",type(data1))
                if exp_date >= upd:
                    if data.cgm_approval == 1 and data.blacklisted == 0 :
                        
                        all_contractor = TKC_Payment.objects.all()
                        contractor = TKC_Payment.objects.get(id=data.Oyt)
                        return render(request, 'tkc/upgrade_tkc_two.html',
                                    {'data': data, 'all_contractor': all_contractor, 'con':con,'contractor': contractor,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
                    else:
                        return render(request, 'tkc/tkc_review.html',{'con':con})
                else:
                    return HttpResponse('Activate First')
        return render(request, 'tkc/tkc_review.html',{'con':con})
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    return render(request, 'tkc/basicinfo.html', {"userdata": data,'con':con})


def updatedata(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_id
        balance_four = TKC_BalanceSheet.objects.filter(
            user_id=user_id).order_by('-id')[3]
        balance_three = TKC_BalanceSheet.objects.filter(
            user_id=user_id).order_by('-id')[2]
        balance_two = TKC_BalanceSheet.objects.filter(
            user_id=user_id).order_by('-id')[1]
        q = TKC_BalanceSheet.objects.filter(user_id=user_id).order_by('-id')[0]
        data_serial = BalanceSheet_Serializer(q)
        d = data_serial.data
        ee2 = json.loads(json.dumps(d))
        ss = ee2['complete_data']

        document1 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[1]
        document2 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[2]
        document3 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[3]
        document4 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[4]
        document5 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[5]
        document6 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[6]
        document7 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[7]
        document8 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[8]
        document9 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[9]
        document10 = TKC_Document.objects.filter(
            user_id=user_id).order_by('-id')[10]

        a = TKC_Document.objects.filter(user_id=user_id).order_by('-id')[0]
        b = TKC_Document_Serializer(a)
        c = b.data
        cc = json.loads(json.dumps(c))
        ccc = cc['complete_data']

        turn_three = TKC_Turnover.objects.filter(
            user_id=user_id).order_by('-id')[2]
        turn_two = TKC_Turnover.objects.filter(
            user_id=user_id).order_by('-id')[1]
        aa = TKC_Turnover.objects.filter(user_id=user_id).order_by('-id')[0]
        bb = TKC_Turnover_Serializer(aa)
        dd = bb.data
        ee = json.loads(json.dumps(dd))
        ff = ee['complete_data']
        if (ss == 1) and (ccc == 1) and (ff == 1):
            if request.method == "POST":
                financial_year = request.POST.get('v_balance_sheet_1')
                Amount = request.POST.get('Amount')
                data1 = TKC_BalanceSheet(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                         Status=1, complete_data=1)
                data1.save()

                financial_year = request.POST.get('v_balance_sheet_2')
                Amount = request.POST.get('Amount2')
                data1 = TKC_BalanceSheet(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                         Status=1, complete_data=1)
                data1.save()

                financial_year = request.POST.get('v_balance_sheet_3')
                Amount = request.POST.get('Amount3')
                data1 = TKC_BalanceSheet(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                         Status=1, complete_data=1)
                data1.save()

                document_no = request.POST.get('number1')
                abcd = request.FILES['file_one']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=abcd)
                data1.save()

                document_no = request.POST.get('number2')
                Ddocfile = request.FILES['file2']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number3')
                Ddocfile = request.FILES['file3']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number4')
                Ddocfile = request.FILES['file4']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number5')
                Ddocfile = request.FILES['file5']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number6')
                Ddocfile = request.FILES['file6']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number7')
                Ddocfile = request.FILES['file7']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number8')
                Ddocfile = request.FILES['file8']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number9')
                Ddocfile = request.FILES['file9']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number10')
                Ddocfile = request.FILES['file10']
                data1 = TKC_Document(user_id=user_id, Document_Number=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()

                document_no = request.POST.get('number11')
                Ddocfile = request.FILES['file11']
                data1 = TKC_Document(user_id=user_id, Issued_office_Name=document_no, Status=1, complete_data=1,
                                     Ddocfile=Ddocfile)
                data1.save()
                return redirect('complete')
            return render(request, '/test',
                          {'one': aa, 'two': turn_two, 'three': turn_three, 'finance': q, 'document0': a,
                           'finance_two': balance_two, 'finance_three': balance_three, 'finance_tour': balance_four,
                           'document1': document1, 'document2': document2, 'document3': document3,
                           'document4': document4, 'document5': document5, 'document6': document6,
                           'document7': document7, 'document8': document8, 'document9': document9,
                           'document10': document10})

        else:
            return render(request, 'tkc/update_message.html')

    return render(request, 'tkc/update.html')


def complete(request):
    data = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    data360 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])

    # send_mail(
    #     'Your final registration is completed ',
    #     'Hello thanks for Final registration as a Contractor',
    #     settings.EMAIL_HOST_USER,
    #     # [data.Email_Id],
    #     [data360.Email_Id],
    #     fail_silently=False,
    # )
    return render(request, 'tkc/test_tkc.html', {'data11': data})


def Logout(request):
    del request.session['otp']
    del request.session['User_type']
    return render(request, 'main/login')


def rejected_doc(request):
    print("print start")
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0).exists():
        data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0)
        late = TKC_Document.objects.filter(user_id=user_id)
        latest = late.latest('new_data')
        if latest.new_data == 0:
            aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,new_data=0) | TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id)
            if aaa.Authentication_id:
                aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
                cert = aaa.Authentication_id
                if aaa.activation_before_expired == 0 and aaa.activation_after_expired == 0:
                    exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').last()
                    expi_date = exp.Doc_expiry_date
                    to_daaa =datetime.datetime.today()
                    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,new_data=0)
                    return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
                else:
                    exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').first()
                    expi_date = exp.Doc_expiry_date
                    to_daaa =datetime.datetime.today()
                    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,new_data=0)
                    return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})          
            return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})

        elif latest.new_data == 1:
            data = TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id)
            if aaa.Authentication_id:
                aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
                cert = aaa.Authentication_id
                if aaa.upgrade_payment == 1:
                    exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').last()
                    expi_date = exp.Doc_expiry_date
                    to_daaa =datetime.datetime.today()
                    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,new_data=1)
                    return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
                elif aaa.activation_after_expired == 1:
                    exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').first()
                    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,new_data=1)
                    expi_date = exp.Doc_expiry_date
                    to_daaa =datetime.datetime.today()
                    return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
                elif aaa.activation_before_expired == 1 :
                    exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').first()
                    expi_date = exp.Doc_expiry_date
                    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,new_data=1)
                    to_daaa =datetime.datetime.today()
                    return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
            return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})
    print("after start")
    if TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,Approver_Status=1).exists():
        print("print one")
        data = TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,Approver_Status=1)
        late = TKC_Document.objects.filter(user_id=user_id)
        latest = late.latest('new_data')
        data = TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,Approver_Status=1)
        if aaa.Authentication_id:
            aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            cert = aaa.Authentication_id
            if aaa.activation_before_expired == 1:
                exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').last()
                expi_date = exp.Doc_expiry_date
                to_daaa =datetime.datetime.today()
                data = TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,new_data=1,Approver_Status=1)
                return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
           
            elif aaa.activation_after_expired == 1:
                print("uuuuuuuuuuuuuuuuuuu")
                exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').last()
                expi_date = exp.Doc_expiry_date
                to_daaa =datetime.datetime.today()
                data = TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,new_data=1,Approver_Status=1)
                print("iiiiiiiiiiiiiiii")
                return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
            elif aaa.upgrade_payment == 1:
                print("print two")
                exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').first()
                expi_date = exp.Doc_expiry_date
                to_daaa =datetime.datetime.today()
                data = TKC_Document.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,new_data=1,Approver_Status=1)
                print("print three",data)
                return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
        return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})

    if data.Authentication_id:
        if data.activation_before_expired == 0 and data.activation_after_expired == 0:
            aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            cert = aaa.Authentication_id
            exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').last()
            expi_date = exp.Doc_expiry_date
            to_daaa =datetime.datetime.today()
            con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])

            return render(request, 'tkc/creater_base.html', {"data": data,'con':con,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})

        else:
            aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            cert = aaa.Authentication_id
            exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').first()
            expi_date = exp.Doc_expiry_date
            to_daaa =datetime.datetime.today()
            con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])

            return render(request, 'tkc/creater_base.html', {"data": data,'con':con,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    return render(request, 'tkc/creater_base.html', {"data": data,'con':con})

def rejected_doc_save(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    sum_data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    data = TKC_Document.objects.filter(id=id, user_id=user_id)
    if request.method == "POST":
        office = request.POST.get('office')
        if office != '':
            data.update(Issued_office_Name=office, Status=1)
        Document_Number = request.POST.get('doc_name')
        if Document_Number != '':
            data.update(Document_Number=Document_Number, Status=1)
        issu_date = request.POST.get('issue_date')
        if issu_date != '':
            data.update(Doc_issue_date=issu_date, Status=1)
        exp_date = request.POST.get('expire_date')
        if exp_date != '':
            data.update(Doc_expiry_date=exp_date, Status=1)
        if len(request.FILES) != 0:
            data = TKC_Document.objects.get(id=id, user_id=user_id)
            upload_file = request.FILES['file']
            data.Ddocfile = upload_file
            data.Status = 1
            data.save()
            print("qqqqqqqqqq")
            summary = reject_and_approve_summary(user=sum_data,type="RESUBMIT",date=datetime.datetime.now(),document_name=data.Types_of_Docs,document=upload_file)
            summary.save()
    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,Approval_doc=1)
    if data:
        return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})
    else:
        data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data1.work_approval = 0
        data1.document_resubmit_date = datetime.datetime.now()
        data1.save()
        con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])

        
    return render(request, 'tkc/creater_base.html', {"data": data,'con':con})


def rejected_doc_finance_save(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    sum_data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    data = TKC_Document.objects.filter(id=id, user_id=user_id)
    if request.method == "POST":
        office = request.POST.get('office')
        if office != '':
            data.update(Issued_office_Name=office, Status=1)
        Document_Number = request.POST.get('doc_name')
        if Document_Number != '':
            data.update(Document_Number=Document_Number, Status=1)
        # issu_date = request.POST.get('issue_date')
        # if issu_date != '':
        #     data.update(Doc_issue_date=issu_date, Status=1)
        # exp_date = request.POST.get('expire_date')
        # if exp_date != '':
        #     data.update(Doc_expiry_date=exp_date, Status=1)
        if len(request.FILES) != 0:
            data = TKC_Document.objects.get(id=id, user_id=user_id)
            upload_file = request.FILES['file']
            data.Ddocfile = upload_file
            data.Status = 1
            data.save()
            print("oooooooooooo")
            summary = reject_and_approve_summary(user=sum_data,type="RESUBMIT",date=datetime.datetime.now(),document_name=data.Types_of_Docs,document=upload_file)
            summary.save()
    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0,Approval_doc=2)
    if data:
        return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})
    else:
        data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data1.finance_approval = 0
        data1.document_resubmit_date = datetime.datetime.now()
        data1.save()
        con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    return render(request, 'tkc/creater_base.html', {"data": data,'con':con})


#######lok####
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


# Create your views here.
# def home(request):
#     # return render(request, 'templates/user_base.html')

#     return render(request, 'main/login.html')


def payu_demo_tkc(request):
    data = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    # data = User_Registration.objects.filter(ContactNo=request.session['uid'])
    firstname = data[0].Authorised_person_E
    e_mail = data[0].Email_Id
    phone = data[0].ContactNo
    vendor_type = data[0].Vendor_type
    oyt = data[0].Oyt
    payment = TKC_Payment.objects.get(id=oyt)
    data1 = {'amount': payment.payment,
             'firstname': firstname,
             'email': e_mail,
             'phone': phone, 'productinfo': 'test',
             'lastname': 'test', 'address1': 'test',
             'address2': 'test', 'city': 'test',
             'state': 'test', 'country': 'test',
             'zipcode': 'tes', 'udf1': '',
             'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
             }

    # txnid = "Create your transaction id"
    data1.update({"txnid": "23456789"})
    payu_data = payu.transaction(**data1)
    return render(request, 'tkc/payu_checkout_tkc.html', {"posted": payu_data})


@csrf_exempt
def payu_success_tkc(request):
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
    payu_moneyid = data['payuMoneyId']
    Netamount = data['net_amount_debit']
    
    from datetime import date
    from datetime import time
    from datetime import datetime
    import datetime

    user = User_Registration.objects.filter(ContactNo=Phone_no,User_type = request.session['User_type'])
    user.update(tkc_payment=1)
    date = datetime.datetime.now()

    sms = User_Registration.objects.get(ContactNo=Phone_no,User_type = request.session['User_type'])
    mobile = sms.ContactNo
    name_sms = sms.CompanyName_E
    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080"}
    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(
        mobile) + "&v1=" + str(name_sms) + "&v2=" + str()
    response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
    
    sms_template = message_template_log(template_id = '1007277348148394809',date = datetime.datetime.now(),mobile_number = mobile)
    sms_template.save()

    sms = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    mobile = sms.ContactNo
    name_sms = sms.CompanyName_E
    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080"}
    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007744910864040749&mobile_number=" + str(
        mobile) + "&v1=" + str('DGM') + "&v2=" + str() + "&v3=" + str(name_sms) + "&v4=" + str() + "&v5=" + str(
        'https://qcportal.mpcz.in/')
    response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
    
    sms_template = message_template_log(template_id = '1007744910864040749',date = datetime.datetime.now(),mobile_number = mobile)
    sms_template.save()

    data3 = Payudata_main(Payu_Moneyid=payu_moneyid, Hash_Id=Hash, Payu_Status=Status, Txdid=Txn_id,
                          Productinfo=Product_info,
                          Firstname=First_name, Lastname=Last_name, Contact_No=Phone_no, Email_Id=mail,
                          Paymentgateway_Type=Pgateway_Type,
                          Bank_Ref_Num=Bankrefnum, Bankcode=Bank_code, Name_On_Card=Nameon_card,
                          Cardnum=Card_num, Netamount_Debited=Netamount,
                          )
    data3.save()

    payu_obj = Payudata_main.objects.latest('id')

    return render(request, 'tkc/sucess_pay_tkc.html', {'response': response, 'data': payu_obj})


# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)


def gen_invoice_first_tkc(request):
    payu_obj = Payudata_main.objects.latest('id')
    return render(request, 'tkc/invoice_first_tkc.html', {'data': payu_obj})



def transaction_history(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    payu_count = Payudata_main.objects.filter(User_Id=data)
    return render(request, 'tkc/tkc_transation_history.html', {"posted": payu_count})


def transaction_history_copy_tkc(request,id):
    payu_count = Payudata_main.objects.get(id=id)
    return render(request, 'tkc/payment_invoice.html', {"data": payu_count})


def upgrade_tkc_one(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        if request.method == "POST":
            if not BankDetails.objects.filter(user_id=data.ContactNo).exists():
                bank_name = request.POST.get('bank_name')
                ifsc = request.POST.get('ifsc')
                ac_holder_name = request.POST.get('ac_holder_name')
                ac_number = request.POST.get('ac_number')
                bank = BankDetails(user_id=data.ContactNo, Bank_name=bank_name, Account_Holder_Name=ac_holder_name,
                                   Account_Number=ac_number, IFSC=ifsc,new_data=1)
                bank.save()
            all_contractor = TKC_Payment.objects.all()
            contractor = TKC_Payment.objects.get(id=data.Oyt)
            return render(request, 'tkc/upgrade_tkc_three.html',
                          {'data': data, 'all_contractor': all_contractor, 'contractor': contractor})
        else:
            return render(request, 'tkc/upgrade_tkc_one.html')
    else:
        return render(request, 'main/mpeb_reg.html')


def upgrade_tkc_two(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        if request.method == "POST":
            data.Upgrade_Oyt = request.POST.get('VendorType')
            data.save()
            txnid = uuid.uuid1()
            if data.upgrade_payment == 1:
                return render(request,'tkc/upgrade_tkc_one.html')
            else:    

                client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
                param = {"txnid": txnid, "amount": "2360.00", "productinfo": "Upgradation Fee",
                        "firstname": data.Authorised_person_E,
                        "email": data.Email_Id}
                apiHash = payu_sdk.Hasher.generate_hash(param)
                data3 = Payudata_main(User_Id = data,Payu_Status='pending', Txdid=txnid,
                          Productinfo="Upgradation Fee",
                          Firstname=data.Authorised_person_E, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                          Netamount_Debited='2360.00'
                          )
                data3.save()
                return render(request, 'main/payu_checkout_registration.html',
                            {"posted": apiHash, "txnid": txnid, "amount": "2360.00", 'firstname': data.Authorised_person_E,
                            "email": data.Email_Id, "productinfo": "Upgradation Fee", "phone": data.ContactNo})
        else:
            return render(request, 'tkc/upgrade_tkc_one.html')
    else:
        return render(request, 'main/mpeb_reg.html')


def upgrade_tkc_three(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        if request.method == "POST":
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
         

            try:

                office_name = request.POST.get('five')
                gst_card_no = request.POST.get('six')
                issu_date = request.POST.get('seven')
                ex_date = request.POST.get('eight')
                document = request.FILES['nine']
             
                data2 = TKC_Document(user_id=user_id, Types_of_Docs='GST With Challan', Issued_office_Name=office_name,
                                    Document_Number=gst_card_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=2,new_data=1)
            except Exception as e:
                print("Exeption is ::::::::::", e)
                office_name = request.POST.get('five')
                gst_card_no = request.POST.get('six')
                issu_date = request.POST.get('seven')
                document = request.FILES['nine']
                data2 = TKC_Document(user_id=user_id, Types_of_Docs='GST With Challan', Issued_office_Name=office_name,
                                    Document_Number=gst_card_no, Ddocfile=document, Doc_issue_date=issu_date, Approval_doc=2,new_data=1)

  

            try:    

                office_name = request.POST.get('fifteen')
                document_no = request.POST.get('sixteen')
                issu_date = request.POST.get('seventeen')
                ex_date = request.POST.get('eighteen')
                document = request.FILES['nineteen']
                data4 = TKC_Document(user_id=user_id, Types_of_Docs='Declaration of Contractor and Supervisior',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=1,new_data=1)

            except Exception as e:
                office_name = request.POST.get('fifteen')
                document_no = request.POST.get('sixteen')
                issu_date = request.POST.get('seventeen')
                document = request.FILES['nineteen']
                data4 = TKC_Document(user_id=user_id, Types_of_Docs='Declaration of Contractor and Supervisior',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=1,new_data=1)


        
            office_name = request.POST.get('twentee')
            document_no = request.POST.get('twentee_one')
            issu_date = request.POST.get('twentee_two')
            ex_date = request.POST.get('twentee_three')
            document = request.FILES['twentee_four']
            data5 = TKC_Document(user_id=user_id, Types_of_Docs='Electrical License',
                                Issued_office_Name=office_name,
                                Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                Doc_expiry_date=ex_date, Approval_doc=1,new_data=1)

            


            try:

                office_name = request.POST.get('twentee_five')
                document_no = request.POST.get('twentee_six')
                issu_date = request.POST.get('twentee_seven')
                ex_date = request.POST.get('twentee_eight')
                document = request.FILES['twentee_nine']
                data6 = TKC_Document(user_id=user_id, Types_of_Docs='EPF With Challan', Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=2,new_data=1)

            except Exception as e:
                office_name = request.POST.get('twentee_five')
                document_no = request.POST.get('twentee_six')
                issu_date = request.POST.get('twentee_seven')
                document = request.FILES['twentee_nine']
                data6 = TKC_Document(user_id=user_id, Types_of_Docs='EPF With Challan', Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=2,new_data=1)



            try:
                office_name = request.POST.get('thiety')
                document_no = request.POST.get('thiety_one')
                issu_date = request.POST.get('thiety_two')
                ex_date = request.POST.get('thiety_three')
                document = request.FILES['thiety_four']
                data7 = TKC_Document(user_id=user_id, Types_of_Docs='ESIC Registration With Challan',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=2,new_data=1)

            except Exception as e:

                office_name = request.POST.get('thiety')
                document_no = request.POST.get('thiety_one')
                issu_date = request.POST.get('thiety_two')
                document = request.FILES['thiety_four']
                data7 = TKC_Document(user_id=user_id, Types_of_Docs='ESIC Registration With Challan',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=2,new_data=1)

            try:  

                office_name = request.POST.get('thiety_five')
                document_no = request.POST.get('thiety_six')
                issu_date = request.POST.get('thiety_seven')
                ex_date = request.POST.get('thiety_eight')
                document = request.FILES['thiety_nine']
                data8 = TKC_Document(user_id=user_id, Types_of_Docs='Experience Certificate',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=1,new_data=1)

            except Exception as e:
                office_name = request.POST.get('thiety_five')
                document_no = request.POST.get('thiety_six')
                issu_date = request.POST.get('thiety_seven')
                document = request.FILES['thiety_nine']
                data8 = TKC_Document(user_id=user_id, Types_of_Docs='Experience Certificate',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=1,new_data=1)


            office_name = request.POST.get('fifty')
            document_no = request.POST.get('fifty_one')
            issu_date = request.POST.get('fifty_two')
            document = request.FILES['fifty_three']
            data11 = TKC_Document(user_id=user_id, Types_of_Docs='PAN Card Number', Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=1,new_data=1)

            
            if data2 and data4 and data5 and data6 and data7 and data8 and data11 :
                data2.save()
                data4.save()
                data5.save()
                data6.save()
                data7.save()
                data8.save()
                data11.save()

                data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
                data.work_approval = 0
                data.finance_approval = 0
                data.cgm_approval = 0
                #data.Authentication_id = ''
                data.upgrade = 1
                data.complete_data = 0
                data.Complete_Details = 0
                data.save()
                today = datetime.datetime.now()
                if data.Upgrade_Oyt == '9':
                    data.officer_create = 1
                    data.reg_date = today
                    data.save()
      
            return redirect('tkc_reg_eleven')
        else:
            return render(request, 'tkc/upgrade_tkc_one.html')
    else:
        return render(request, 'main/mpeb_reg.html')


def upgrade_tkc_four(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data.work_approval = 0
        data.finance_approval = 0
        data.cgm_approval = 0
      
        data.save()
        if request.method == "POST":
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
            payment = TKC_Payment.objects.get(id=data.Upgrade_Oyt)
            payment1 = TKC_Payment.objects.get(id=data.Oyt)
            payment2 = payment.payment - payment1.payment
            txnid = uuid.uuid1()
            client = payu_sdk.payUClient(credes={"key": "7rnFly", "salt": "pjVQAWpA"})
            param = {"txnid": txnid, "amount": payment2, "productinfo": "Contractor Upgrade sd",
                     "firstname": data.Authorised_person_E,
                     "email": data.Email_Id}
            apiHash = payu_sdk.Hasher.generate_hash(param)
            return render(request, 'main/payu_checkout_registration.html',
                          {"posted": apiHash, "txnid": txnid, "amount": payment2,
                           'firstname': data.Authorised_person_E,
                           "email": data.Email_Id, "productinfo": "Contractor Upgrade sd", "phone": data.ContactNo})

        else:
            return render(request, 'tkc/upgrade_tkc_one.html')
    else:
        return render(request, 'main/mpeb_reg.html')


payu = Payu(merchant_key, merchant_salt, surl, furl, mode)
import payu_sdk
import uuid


def payu_demo_registration(request):
    txnid = uuid.uuid1()
    client = payu_sdk.payUClient(credes={"key": "7rnFly", "salt": "pjVQAWpA"})
    param = {"txnid": txnid, "amount": "2360.00", "productinfo": "iPhone", "firstname": "rohit",
             "email": "rohitpatel1790@gmail.com"}
    apiHash = payu_sdk.Hasher.generate_hash(param)
    return render(request, 'main/payu_checkout_registration.html', {"posted": apiHash, "txnid": txnid})

    # For TKC Project Section


def wo(request):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if data1.cgm_approval:
        data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
        return render(request, 'tkc/all_wo.html', {"name": data,'con':con})
    else:
        messages.warning(
            request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"data": data1,'con':con})


def all_wo(request):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/all_wo.html', {"name": data})


def view_wo(request, PO_id):
    procurement = TKCWoInfo.objects.filter(id=PO_id)
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
    return render(request, 'tkc/view_wo.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                   'data': data})


def upload_bg_loc(request):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})


def upload_bg(request, PO_id):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'tkc/upload_bg.html', {"data": data})


def upload_loc(request, PO_id):
    print("LLLLLoooooooCCCCCC")
    data = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'tkc/upload_loc.html', {"data": data})


def upload_bg_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.bg = upload_file
        procurement_obj.save()
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})


def upload_loc_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.loc = upload_file
        procurement_obj.save()
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})


def upload_vendor(request):
    vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    TKC = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    all_vendor = TKCVendor.objects.filter(TKC=TKC)
    return render(request, 'tkc/upload_vendor.html', {"data": data, "vendor": vendor, 'all_vendor': all_vendor})


# def add_vendor(request):
#     if request.method == 'POST':
#         TKC = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
#         v_name = request.POST.get('w_id')
#         id = TKCWoInfo.objects.get(id=v_name)
#         v_id = request.POST.get('v_id')
#         vendor = User_Registration.objects.get(User_Id=v_id)
#         quantity = request.POST.get('quantity')
#         material = request.POST.get('material')
#         data = TKCVendor(TKC=TKC, TKCWoInfo=id, Vendor_id=vendor, material_name=material, quantity=quantity)
#         data.save()
#         vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
#         data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
#         data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#         all_vendor = TKCVendor.objects.filter(TKC=TKC)
#         return render(request, 'tkc/upload_vendor.html', {"data": data, "vendor": vendor, 'all_vendor': all_vendor})


def activation_tkc_three(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        if request.method == "POST":
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
            toc = TKC_Document.objects.filter(user_id=user_id)
            toc.update(Primary_verification_Status=0,Status=0,Primary_remark_rejection_counter=0,Primary_remark='')
         
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
          
            try:

                office_name = request.POST.get('five')
                gst_card_no = request.POST.get('six')
                issu_date = request.POST.get('seven')
                ex_date = request.POST.get('eight')
                document = request.FILES['nine']
               
                data2 = TKC_Document(user_id=user_id, Types_of_Docs='GST With Challan', Issued_office_Name=office_name,
                                    Document_Number=gst_card_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=2,new_data=1)
            except Exception as e:
                print("Exeption is ::::::::::", e)
                office_name = request.POST.get('five')
                gst_card_no = request.POST.get('six')
                issu_date = request.POST.get('seven')
                document = request.FILES['nine']
                data2 = TKC_Document(user_id=user_id, Types_of_Docs='GST With Challan', Issued_office_Name=office_name,
                                    Document_Number=gst_card_no, Ddocfile=document, Doc_issue_date=issu_date, Approval_doc=2,new_data=1)

          
            try:    

                office_name = request.POST.get('fifteen')
                document_no = request.POST.get('sixteen')
                issu_date = request.POST.get('seventeen')
                ex_date = request.POST.get('eighteen')
                document = request.FILES['nineteen']
                data4 = TKC_Document(user_id=user_id, Types_of_Docs='Declaration of Contractor and Supervisior',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=1,new_data=1)

            except Exception as e:
                office_name = request.POST.get('fifteen')
                document_no = request.POST.get('sixteen')
                issu_date = request.POST.get('seventeen')
                document = request.FILES['nineteen']
                data4 = TKC_Document(user_id=user_id, Types_of_Docs='Declaration of Contractor and Supervisior',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=1,new_data=1)


        
            office_name = request.POST.get('twentee')
            document_no = request.POST.get('twentee_one')
            issu_date = request.POST.get('twentee_two')
            ex_date = request.POST.get('twentee_three')
            document = request.FILES['twentee_four']
            data5 = TKC_Document(user_id=user_id, Types_of_Docs='Electrical License',
                                Issued_office_Name=office_name,
                                Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                Doc_expiry_date=ex_date, Approval_doc=1,new_data=1)

            


            try:

                office_name = request.POST.get('twentee_five')
                document_no = request.POST.get('twentee_six')
                issu_date = request.POST.get('twentee_seven')
                ex_date = request.POST.get('twentee_eight')
                document = request.FILES['twentee_nine']
                data6 = TKC_Document(user_id=user_id, Types_of_Docs='EPF With Challan', Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=2,new_data=1)

            except Exception as e:
                office_name = request.POST.get('twentee_five')
                document_no = request.POST.get('twentee_six')
                issu_date = request.POST.get('twentee_seven')
                document = request.FILES['twentee_nine']
                data6 = TKC_Document(user_id=user_id, Types_of_Docs='EPF With Challan', Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=2,new_data=1)



            try:
                office_name = request.POST.get('thiety')
                document_no = request.POST.get('thiety_one')
                issu_date = request.POST.get('thiety_two')
                ex_date = request.POST.get('thiety_three')
                document = request.FILES['thiety_four']
                data7 = TKC_Document(user_id=user_id, Types_of_Docs='ESIC Registration With Challan',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=2,new_data=1)

            except Exception as e:

                office_name = request.POST.get('thiety')
                document_no = request.POST.get('thiety_one')
                issu_date = request.POST.get('thiety_two')
                document = request.FILES['thiety_four']
                data7 = TKC_Document(user_id=user_id, Types_of_Docs='ESIC Registration With Challan',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=2,new_data=1)

            try:  

                office_name = request.POST.get('thiety_five')
                document_no = request.POST.get('thiety_six')
                issu_date = request.POST.get('thiety_seven')
                ex_date = request.POST.get('thiety_eight')
                document = request.FILES['thiety_nine']
                data8 = TKC_Document(user_id=user_id, Types_of_Docs='Experience Certificate',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Doc_expiry_date=ex_date, Approval_doc=1,new_data=1)

            except Exception as e:
                office_name = request.POST.get('thiety_five')
                document_no = request.POST.get('thiety_six')
                issu_date = request.POST.get('thiety_seven')
                document = request.FILES['thiety_nine']
                data8 = TKC_Document(user_id=user_id, Types_of_Docs='Experience Certificate',
                                    Issued_office_Name=office_name,
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=1,new_data=1)
         


            document_no = request.POST.get('fifty_one')
            issu_date = request.POST.get('fifty_two')
            document = request.FILES['fifty_three']
            data11 = TKC_Document(user_id=user_id, Types_of_Docs='PAN Card Number',
                                    Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                    Approval_doc=1,new_data=1)

              
            if  data2 and data4 and data5 and data6 and data7 and data8 and data11 :
                data2.save()
                data4.save()
                data5.save()
                data6.save()
                data7.save()
                data8.save()
                data11.save()

                data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
                data.work_approval = 0
                data.finance_approval = 0
                data.cgm_approval = 0
                data.activation = 1
                #data.Authentication_id = ''
                data.complete_data = 0
                data.Complete_Details = 0
                data.Status = 1
                data.save()
          
            return redirect('tkc_reg_eleven')
        
        return render(request,'tkc/activation_payment_check.html')
    else:
        return render(request, 'main/mpeb_reg.html')



def activation_payment_check(request):
 
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])

        if (data.activation_before_expired == 1 or data.activation_after_expired == 1) and data.cgm_approval == 1:
            payment = TKC_Payment.objects.all()
            if request.method == "POST":
                if not BankDetails.objects.filter(user_id=data.ContactNo).exists():
                    bank_name = request.POST.get('bank_name')
                    ifsc = request.POST.get('ifsc')
                    ac_holder_name = request.POST.get('ac_holder_name')
                    ac_number = request.POST.get('ac_number')
                    bank = BankDetails(user_id=data.ContactNo, Bank_name=bank_name, Account_Holder_Name=ac_holder_name,
                                    Account_Number=ac_number, IFSC=ifsc,new_data=1)
                    bank.save()
                    return redirect('activation_tkc_three')
                all_contractor = TKC_Payment.objects.all()
                contractor = TKC_Payment.objects.get(id=data.Oyt)
                return redirect('activation_tkc_three')
            return render(request,'tkc/activation_bank_details.html')
    
        return redirect('activation')
       
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    return render(request, 'tkc/basicinfo.html', {"userdata": data})


def all_wo(request):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/all_wo.html', {"name": data})


def view_wo(request, PO_id):
    procurement = TKCWoInfo.objects.filter(id=PO_id)
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
    cdatetime = datetime.datetime.now().date()
    data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
    return render(request, 'tkc/view_wo.html',
                  {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
                   'data': data})


def upload_bg_loc(request):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})


def upload_bg(request, PO_id):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'tkc/upload_bg.html', {"data": data})


def upload_loc(request, PO_id):
    data = TKCWoInfo.objects.get(id=PO_id)
    return render(request, 'tkc/upload_loc.html', {"data": data})


def upload_bg_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.bg = upload_file
        procurement_obj.save()
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})


def upload_loc_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.loc = upload_file
        procurement_obj.save()
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})


def upload_vendor(request):
    vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    TKC = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    all_vendor = TKCVendor.objects.filter(TKC=TKC)
    return render(request, 'tkc/upload_vendor.html', {"data": data, "vendor": vendor, 'all_vendor': all_vendor})


# def add_vendor(request):
#     if request.method == 'POST':
#         TKC = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
#         v_name = request.POST.get('w_id')
#         id = TKCWoInfo.objects.get(id=v_name)
#         v_id = request.POST.get('v_id')
#         vendor = User_Registration.objects.get(User_Id=v_id)
#         quantity = request.POST.get('quantity')
#         material = request.POST.get('material')
#         data = TKCVendor(TKC=TKC, TKCWoInfo=id, Vendor_id=vendor, material_name=material, quantity=quantity)
#         data.save()
#         vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
#         data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
#         data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#         all_vendor = TKCVendor.objects.filter(TKC=TKC)
#         return render(request, 'tkc/upload_vendor.html', {"data": data, "vendor": vendor, 'all_vendor': all_vendor})


def rejected_doc_GM_save(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    sum_data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    data = TKC_Document.objects.filter(id=id, user_id=user_id)
    if request.method == "POST":
        office = request.POST.get('office')
        if office != '':
            data.update(Issued_office_Name=office)
        Document_Number = request.POST.get('doc_name')
        if Document_Number != '':
            data.update(Document_Number=Document_Number)
        issu_date = request.POST.get('issue_date')
        if issu_date != '':
            data.update(Doc_issue_date=issu_date)
        exp_date = request.POST.get('expire_date')
        if exp_date != '':
            data.update(Doc_expiry_date=exp_date)
        if len(request.FILES) != 0:
            data = TKC_Document.objects.get(id=id, user_id=user_id)
            upload_file = request.FILES['file']
            data.Ddocfile = upload_file
            data.Approver_Status = 0
            data.save()
            summary = reject_and_approve_summary(user=sum_data,type="RESUBMIT",date=datetime.datetime.now(),document_name=data.Types_of_Docs,document=upload_file)
            summary.save()
            print("yyyyyyyyyyyyyyyyyyyy")
    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id,Approver_Status=1)
    if data:
        return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})
    else:
        data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data1.cgm_approval = 0
        data1.document_resubmit_date = datetime.datetime.now()
        data1.save()
        con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    return render(request, 'tkc/creater_base.html', {"data": data,'con':con})
    
    
def profile_status(request):
    TKC = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if data.Authentication_id:
        aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        cert = aaa.Authentication_id
        exp = TKC_Document.objects.filter(user_id=aaa.User_Id, Types_of_Docs='Electrical License').first()
        expi_date = exp.Doc_expiry_date
        to_daaa =datetime.datetime.today()
        return render(request, 'tkc/base1.html', {"data":data,"data11": TKC,'cert':cert,'exp':exp,'expi_date':expi_date,'to_daaa':to_daaa})

    else:
        return render(request, 'tkc/base1.html', {"data":data,"data11": TKC})    

    


from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from  datetime import date

import json


@api_view(['GET'])
def active_contractors(request):
    response = Response()
    data = User_Registration.objects.filter(User_type = 'TKC',cgm_approval=1)
    list_value = []
    for val in data:
        data_2 = TKC_Document.objects.filter(Types_of_Docs="Electrical License",user_id=val.User_Id,Doc_expiry_date__gte=date.today())
        for a in data_2:


             val_2 = User_Registration.objects.filter(User_type = 'TKC',cgm_approval=1,User_Id=a.user_id)
             for i in val_2:
                 val_3 = UserCompanyDataMain.objects.filter(user_id_id=i)
                 print([i.Company_add_1 for i in val_3 ])
             listt = [{'user_zone':v.User_zone,'company_name':v.CompanyName_E,'email':v.Email_Id,'mobile':v.ContactNo,'authentication_id':v.Authentication_id,'address':f"{i.Company_add_1} {i.Company_add_2}{i.Company_pin_code}{i.Company_dist}{i.Company_state}"}for v in val_2 for i in val_3]
             list_value.append(listt)

    return HttpResponse(json.dumps(list_value), content_type="application/json")
    

# new code
# For TKC Project Section


def wo(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'con': con})
    else:
        messages.warning(
            request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'con': con})


def upload_Bank(request, wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.get(id=wo_id)
    wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
    if BankDetails.objects.filter(user_id=con.ContactNo, Status=1, bank_submit=1).exists():
        messages.add_message(request, messages.INFO, 'Bank Details Already Submitted')
        return render(request, 'wo/all_wo.html', {"wo": wo, 'con': con})
    if request.method == "POST":
        if BankDetails.objects.filter(user_id=con.ContactNo, Bank_name=request.POST.get('Bank_name'),
                                      Account_Holder_Name=request.POST.get('Account_Holder_Name'),
                                      IFSC=request.POST.get('IFSC'),
                                      Account_Number=request.POST.get('Account_Number'),
                                      cancel_check=request.FILES['cancel_check'],
                                      Status=1, bank_submit=1).exists():
            messages.add_message(request, messages.INFO, 'Bank Details Already Submitted')
            wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
            return render(request, 'wo/all_wo.html', {"wo": wo, 'con': con})
        Bank = BankDetails(user_id=con.ContactNo, Bank_name=request.POST.get('Bank_name'),
                           Account_Holder_Name=request.POST.get('Account_Holder_Name'),
                           IFSC=request.POST.get('IFSC'),
                           Account_Number=request.POST.get('Account_Number'),
                           cancel_check=request.FILES['cancel_check'],
                           Status=1, bank_submit=1, submit_at=datetime.datetime.now())
        Bank.save()
        data.Bank = BankDetails.objects.latest('Bank_Id')
        data.save()
        messages.add_message(request, messages.INFO, 'Bank Details Save')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'con': con})
    messages.add_message(request, messages.INFO, 'Data Not Found')
    return render(request, 'wo/upload_Bank.html', {"data": data, 'con': con})


def upload_bg(request, wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        if TKCWoInfo_Bg.objects.filter(TKCWoInfo=supplier, BG_Type=request.POST.get('Type'),
                                       BG_Bank_name=request.POST.get('BG_Bank_name'),
                                       BG_Guarantee_no=request.POST.get('BG_Guarantee_no'),
                                       BG_Issue_Date=request.POST.get('BG_Issue_Date'),
                                       BG_Valid_Date=request.POST.get('BG_Valid_Date'),
                                       BG_Amount=request.POST.get('BG_Amount'),
                                       BG_Copy=request.FILES['BG_Copy'],
                                       Status=1).exists():
            messages.add_message(request, messages.INFO, 'BG Already Submitted')
            wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
            return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
        Bank = TKCWoInfo_Bg(TKCWoInfo=supplier, BG_Type=request.POST.get('Type'),
                            BG_Bank_name=request.POST.get('BG_Bank_name'),
                            BG_Guarantee_no=request.POST.get('BG_Guarantee_no'),
                            BG_Issue_Date=request.POST.get('BG_Issue_Date'),
                            BG_Valid_Date=request.POST.get('BG_Valid_Date'),
                            BG_Amount=request.POST.get('BG_Amount'),
                            BG_Copy=request.FILES['BG_Copy'],
                            Status=1)
        Bank.save()
        messages.add_message(request, messages.INFO, 'BG Submitted')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
    BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=supplier, Status=1)
    Bg_Type = TKCWoInfo_Bg_Type.objects.filter(Status=1)
    return render(request, 'wo/upload_bg.html', {'con': con, 'data': supplier, 'BG': BG, 'Bg_Type': Bg_Type})


def bg_sumit_for_approval(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCWoInfo_Bg.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCWoInfo_Bg.objects.get(id=bg_id, Status=1)
        Advance.BG_Submit = 1
        Advance.save()
    BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=supplier, Status=1)
    Bg_Type = TKCWoInfo_Bg_Type.objects.filter(Status=1)
    return render(request, 'wo/upload_bg.html', {'con': con, 'data': supplier, 'BG': BG, 'Bg_Type': Bg_Type})


def bg_delete(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCWoInfo_Bg.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCWoInfo_Bg.objects.get(id=bg_id, Status=1)
        Advance.Status = -1
        Advance.save()
    BG = TKCWoInfo_Bg.objects.filter(TKCWoInfo=supplier, Status=1)
    Bg_Type = TKCWoInfo_Bg_Type.objects.filter(Status=1)
    return render(request, 'wo/upload_bg.html', {'con': con, 'data': supplier, 'BG': BG, 'Bg_Type': Bg_Type})


def upload_loc(request, wo_id):
    data = TKCWoInfo.objects.get(id=wo_id)
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        if TKCWoInfo_LOC.objects.filter(TKCWoInfo=supplier,LOC_Approved_Status=1).exists():
            messages.add_message(request, messages.INFO, 'LOC Already Submitted')
            wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
            return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
        Bank = TKCWoInfo_LOC(TKCWoInfo=supplier,
                             LOC_No=request.POST.get('LOC_No'),
                             LOC_Amount=request.POST.get('LOC_Amount'),
                             LOC_Issue_Date=request.POST.get('LOC_Issue_Date'),
                             LOC_Valid_Date=request.POST.get('LOC_Valid_Date'),
                             LOC=request.FILES['LOC'],
                             Status=1)
        Bank.save()
        messages.add_message(request, messages.INFO, 'LOC Detail Submitted')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
    LOC = TKCWoInfo_LOC.objects.filter(TKCWoInfo=supplier, Status=1)
    return render(request, 'wo/upload_loc.html', {"data": supplier, 'con': con, 'LOC': LOC})


def loc_sumit_for_approval(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCWoInfo_LOC.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCWoInfo_LOC.objects.get(id=bg_id, Status=1)
        Advance.LOC_Submit = 1
        Advance.save()
    LOC = TKCWoInfo_LOC.objects.filter(TKCWoInfo=supplier, Status=1)
    return render(request, 'wo/upload_loc.html', {'con': con, 'data': supplier, 'LOC': LOC})


def loc_delete(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCWoInfo_LOC.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCWoInfo_LOC.objects.get(id=bg_id, Status=1)
        Advance.Status = -1
        Advance.save()
    LOC = TKCWoInfo_LOC.objects.filter(TKCWoInfo=supplier, Status=1)
    return render(request, 'wo/upload_loc.html', {'con': con, 'data': supplier, 'LOC': LOC})


def upload_pert(request, wo_id):
    data = TKCWoInfo.objects.get(id=wo_id)
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        if TKCWoInfo_Pert.objects.filter(TKCWoInfo=supplier,
                                         Pert=request.FILES['Pert_file'],
                                         Status=1).exists():
            messages.add_message(request, messages.INFO, 'Pet Already Submitted')
            wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
            return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
        Bank = TKCWoInfo_Pert(TKCWoInfo=supplier,
                              Pert=request.FILES['Pert_file'],
                              Status=1)
        Bank.save()
        messages.add_message(request, messages.INFO, 'Pert Submitted')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
    Pert = TKCWoInfo_Pert.objects.filter(TKCWoInfo=supplier, Status=1)
    print('jjjjjjjjjjjjjjjj', Pert)
    return render(request, 'wo/upload_pert.html', {"data": data, 'con': con, 'Pert': Pert})


def pert_sumit_for_approval(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCWoInfo_Pert.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCWoInfo_Pert.objects.get(id=bg_id, Status=1)
        Advance.Pert_Submit = 1
        Advance.save()
    Pert = TKCWoInfo_Pert.objects.filter(TKCWoInfo=supplier, Status=1)
    return render(request, 'wo/upload_pert.html', {"data": supplier, 'con': con, 'Pert': Pert})


def pert_delete(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCWoInfo_Pert.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCWoInfo_Pert.objects.get(id=bg_id, Status=1)
        Advance.Status = -1
        Advance.save()
    Pert = TKCWoInfo_Pert.objects.filter(TKCWoInfo=supplier, Status=1)
    return render(request, 'wo/upload_pert.html', {"data": supplier, 'con': con, 'Pert': Pert})


def upload_mqpdoc(request, wo_id):
    data = TKCWoInfo.objects.get(id=wo_id)
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        if TKC_MqpPlanDocuments.objects.filter(tkcwoinfo=supplier,
                                         mqpdoc=request.FILES['mqpdoc_file'],
                                         status=1).exists():
            messages.add_message(request, messages.INFO, 'Already Mqpdoc Submitted')
            wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
            return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
        Bank = TKC_MqpPlanDocuments(tkcwoinfo=supplier,
                              mqpdoc=request.FILES['mqpdoc_file'],
                                         status=1)
        Bank.save()
        messages.add_message(request, messages.INFO, 'mqpdoc Submitted')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
    mqpdoc = TKC_MqpPlanDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    # print('jjjjjjjjjjjjjjjj', mqpdoc)
    return render(request, 'wo/upload_mqpdoc.html', {"data": data, 'con': con, 'mqpdoc': mqpdoc})


def upload_fqpdoc(request, wo_id):
    data = TKCWoInfo.objects.get(id=wo_id)
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        if TKC_FqpPlanDocuments.objects.filter(tkcwoinfo=supplier,
                                         fqpdoc=request.FILES['fqpdoc_file'],
                                         status=1).exists():
            messages.add_message(request, messages.INFO, 'fqpdoc Already Submitted')
            wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
            return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
        Bank = TKC_FqpPlanDocuments(tkcwoinfo=supplier,
                              fqpdoc=request.FILES['fqpdoc_file'],
                                         status=1)
        Bank.save()
        messages.add_message(request, messages.INFO, 'fqpdoc Submitted')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
    fqpdoc = TKC_FqpPlanDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    # print('jjjjjjjjjjjjjjjj', fqpdoc)
    return render(request, 'wo/upload_fqpdoc.html', {"data": data, 'con': con, 'fqpdoc': fqpdoc})


def mqpdoc_sumit_for_approval(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKC_MqpPlanDocuments.objects.filter(id=bg_id, status=1).exists():
        Advance = TKC_MqpPlanDocuments.objects.get(id=bg_id, status=1)
        Advance.mqpdoc_submit = 1
        Advance.save()
    mqpdoc = TKC_MqpPlanDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    return render(request, 'wo/upload_mqpdoc.html', {"data": supplier, 'con': con, 'mqpdoc': mqpdoc})

    
def fqpdoc_sumit_for_approval(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKC_FqpPlanDocuments.objects.filter(id=bg_id, status=1).exists():
        Advance = TKC_FqpPlanDocuments.objects.get(id=bg_id, status=1)
        Advance.fqpdoc_submit = 1
        Advance.save()
    fqpdoc = TKC_FqpPlanDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    return render(request, 'wo/upload_fqpdoc.html', {"data": supplier, 'con': con, 'fqpdoc': fqpdoc})


def mqpdoc_delete(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKC_MqpPlanDocuments.objects.filter(id=bg_id, status=1).exists():
        Advance = TKC_MqpPlanDocuments.objects.get(id=bg_id, status=1)
        Advance.status = -1
        Advance.save()
    mqpdoc = TKC_MqpPlanDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    return render(request, 'wo/upload_mqpdoc.html', {"data": supplier, 'con': con, 'mqpdoc': mqpdoc})
    


def fqpdoc_delete(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKC_FqpPlanDocuments.objects.filter(id=bg_id, status=1).exists():
        Advance = TKC_FqpPlanDocuments.objects.get(id=bg_id, status=1)
        Advance.status = -1
        Advance.save()
    fqpdoc = TKC_FqpPlanDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    return render(request, 'wo/upload_fqpdoc.html', {"data": supplier, 'con': con, 'fqpdoc': fqpdoc})


def upload_otherdoc(request, wo_id):
    data = TKCWoInfo.objects.get(id=wo_id)
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        if TKCOtherDocuments.objects.filter(tkcwoinfo=supplier,
                                         otherdoc=request.FILES['otherdoc_file'],
                                         status=1).exists():
            messages.add_message(request, messages.INFO, 'Otherdoc Aready Submitted')
            wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
            return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
        Bank = TKCOtherDocuments(tkcwoinfo=supplier,
                              otherdoc=request.FILES['otherdoc_file'],
                                         status=1)
        Bank.save()
        messages.add_message(request, messages.INFO, 'Otherdoc Submitted')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'data': supplier, 'con': con})
    otherdoc = TKCOtherDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    # print('jjjjjjjjjjjjjjjj', otherdoc)
    return render(request, 'wo/upload_OtherDocuments.html', {"data": data, 'con': con, 'otherdoc': otherdoc})


def otherdoc_sumit_for_approval(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCOtherDocuments.objects.filter(id=bg_id, status=1).exists():
        Advance = TKCOtherDocuments.objects.get(id=bg_id, status=1)
        Advance.otherdoc_submit = 1
        Advance.save()
    otherdoc = TKCOtherDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    return render(request, 'wo/upload_OtherDocuments.html', {"data": supplier, 'con': con, 'otherdoc': otherdoc})



def otherdoc_delete(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCOtherDocuments.objects.filter(id=bg_id, status=1).exists():
        Advance = TKCOtherDocuments.objects.get(id=bg_id, status=1)
        Advance.status = -1
        Advance.save()
    otherdoc = TKCOtherDocuments.objects.filter(tkcwoinfo=supplier, status=1)
    return render(request, 'wo/upload_OtherDocuments.html', {"data": supplier, 'con': con, 'otherdoc': otherdoc})


def upload_vendor(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1).exists():
        messages.add_message(request, messages.INFO, 'Record  Found')
    else:
        messages.add_message(request, messages.INFO, 'Record Not Found')
    wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
    return render(request, 'wo/upload_vendor.html', {"wo": wo, 'con': con})


def add_vendor(request, wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id)
    wo_discom = wo.Discom.Discom_Code

    # wo_schedules_list = []
    # wo_schedules = TKCWoInfo_Schedule_Supply.objects.filter(TKCWoInfo = wo)
    # for v in wo_schedules:
    #     wo_schedules_list.append(v)
    # wo_schedule_items = TKCWoInfo_Schedule_Supply_Item.objects.filter(Schedule_Supply__in = wo_schedules_list)
    # list_schedule_supply_item = []
    # for i in wo_schedule_items:
    #     list_schedule_supply_item.append(i)
    # print(list_schedule_supply_item)

    wo_schedule_items = tkc_wo_items_boq.objects.filter(wo = wo)
    list_schedule_supply_item = []
    for i in wo_schedule_items:
        list_schedule_supply_item.append(i)
    

    if request.method == 'POST':
        try:
            other_doc = request.FILES['other_file']
        except:
            other_doc = None
        gtp_file = request.FILES['gtp_file']
        material_id = request.POST.get('vendor')
        material_ins = Vendor_Material_Details.objects.get(id=material_id)
        material_user_id = material_ins.user_id.User_Id
        vendor_ins = User_Registration.objects.get(User_Id=material_user_id)

        vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
        material = Vendor_Material_Details.objects.all()
        wo = TKCWoInfo.objects.get(id=wo_id)
        all_vendor = TKCVendor.objects.filter(TKCWoInfo=wo, Status=1)


        if TKCVendor.objects.filter(TKCWoInfo=wo, Vendor=vendor_ins, Material_id=material_ins, Status=1,TKCVendor_Approved_Status=1).exists():
            return render(request, 'wo/add_vendor.html',
                          {"data": supplier,"wo": wo, 'material': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor,"list_schedule_supply_item":list_schedule_supply_item,"msg":"Selected vendor is already approved for this material","wo_discom":wo_discom})

        if TKCVendor.objects.filter(TKCWoInfo=wo, Vendor=vendor_ins, Material_id=material_ins, Status=1,TKCVendor_Approved_Status=0).exists():
            return render(request, 'wo/add_vendor.html',
                          {"data": supplier,"wo": wo, 'material': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor,"list_schedule_supply_item":list_schedule_supply_item,"msg":"Selected vendor is already in approval process for this material","wo_discom":wo_discom})
        
        data = TKCVendor(TKCWoInfo=wo, Vendor=vendor_ins, Material_id=material_ins, Status=1,vendor_gtp_file= gtp_file,TKCVendor_Submit = 1,TKCVendor_Submit_At = datetime.datetime.now(),vendor_other_docs = other_doc)
        data.save()
        return render(request, 'wo/add_vendor.html',
                      {"wo": wo, 'material': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor,
                       'data': supplier,"list_schedule_supply_item":list_schedule_supply_item,"wo_discom":wo_discom})
    vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
    material = Vendor_Material_Details.objects.all()
    all_vendor = TKCVendor.objects.filter(TKCWoInfo=wo)
    return render(request, 'wo/add_vendor.html',
                  {"data": supplier, 'material': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor,"list_schedule_supply_item":list_schedule_supply_item,"wo_discom":wo_discom})




def tkc_vendor_approval(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCVendor.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCVendor.objects.get(id=bg_id, Status=1)
        Advance.TKCVendor_Submit = 1
        Advance.TKCVendor_Submit_At = datetime.datetime.now()
        Advance.save()
        vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
        material = Vendor_Material_Details.objects.all()
        all_vendor = TKCVendor.objects.filter(TKCWoInfo=supplier, Status=1)
        #messages.add_message(request, messages.INFO, 'Item Deleted')
        return render(request, 'wo/add_vendor.html',
                      {"data": supplier, 'material': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor})
    vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
    material = Vendor_Material_Details.objects.all()
    all_vendor = TKCVendor.objects.filter(TKCWoInfo=supplier, Status=1)
    messages.add_message(request, messages.INFO, 'Item Not Found')
    return render(request, 'wo/add_vendor.html',
                  {"data": supplier, 'material': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor})


def tkc_vendor_delete(request, wo_id, bg_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    supplier = TKCWoInfo.objects.get(id=wo_id)
    if TKCWoInfo_Pert.objects.filter(id=bg_id, Status=1).exists():
        Advance = TKCWoInfo_Pert.objects.get(id=bg_id, Status=1)
        Advance.Status = -1
        Advance.save()
        vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
        material = Vendor_Material_Details.objects.all()
        all_vendor = TKCVendor.objects.filter(TKCWoInfo=supplier, Status=1)
        messages.add_message(request, messages.INFO, 'Item Deleted')
        return render(request, 'wo/add_vendor.html',
                      {"data": supplier, 'material': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor})
    vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
    material = Vendor_Material_Details.objects.all()
    all_vendor = TKCVendor.objects.filter(TKCWoInfo=supplier, Status=1)
    messages.add_message(request, messages.INFO, 'Item Not Found')
    return render(request, 'wo/add_vendor.html',
                  {"data": supplier, 'mater ial': material, 'con': con, 'vendor': vendor, 'all_vendor': all_vendor})


# def all_wo(request):
#     data1 = User_Registration.objects.get(Otp=request.session['otp'])
#     data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#     return render(request, 'tkc/all_wo.html', {"name": data})



def material_offer(request, v_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    Vendor = TKCVendor.objects.get(id=v_id)
    if request.method == "POST":
        if TKCVendor.objects.filter(id=v_id, Status=1).exists():
            Vendor = TKCVendor.objects.get(id=v_id, Status=1)
            date_of_readiness=request.POST.get('date_of_readiness')
            Material = Offer_Material(TKCVendor=Vendor, Quantity=request.POST.get('quantity'), Status=1,readiness_date = date_of_readiness)
            Material.save()
            material_offer = Offer_Material.objects.filter(TKCVendor=Vendor, Status=1)
            return render(request, 'wo/material_offer.html',
                          {"con": con, 'Vendor': Vendor, 'material_offer': material_offer})
    material_offer = Offer_Material.objects.filter(TKCVendor=Vendor, Status=1)
    return render(request, 'wo/material_offer.html',
                  {"con": con, 'Vendor': Vendor, 'material_offer': material_offer})


def upload_item(request, offer_id):
    print(offer_id,"-------------------------------")
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    offer = Offer_Material.objects.get(id=offer_id)
    item = Offer_Material_Item_Code.objects.filter(Offer_Material=offer, Status=1)
    if request.method == "POST":
        print("request done---------------------")
        material_data = request.FILES["file"]
        print(material_data)
        data2 = pd.read_excel(material_data)
        for column in data2:
            no_list = data2[column].values
            item_no_list = list(no_list)

        print(item_no_list)
        print(offer.Quantity,"offer qty")
        print(len(item_no_list),"length of item no.")

#         if offer.Quantity != len(item_no_list):
#             messages.add_message(request, messages.INFO, 'Count of serial number should be equal to offer quantity')
#             return render(request, 'wo/upload_item.html',
#                         {"con": con, 'offer': offer, 'item': item})
            
        
        if len(item_no_list) != len(set(item_no_list)):
            print("same no equal")
            messages.add_message(request, messages.INFO, 'You cannot enter same serial number in excel')
            return render(request, 'wo/upload_item.html',
                        {"con": con, 'offer': offer, 'item': item})
            
        for i in item_no_list:
            offer = Offer_Material.objects.get(id=offer_id, Status=1)
            print(i,"first serial no.")
            if Offer_Material_Item_Code.objects.filter(Offer_Material=offer, Item_Serial_No=str(i),Status=1).exists():       
                print(i,"exist serial no.")
                messages.add_message(request, messages.INFO, 'Item code Already Exists for this Material')
    
            Item_Code = Offer_Material_Item_Code(Offer_Material=offer,
                                                Item_Serial_No=i,
                                                Status=1)
            Item_Code.save()
        messages.add_message(request, messages.INFO, 'Item Save')
        item = Offer_Material_Item_Code.objects.filter(Offer_Material=offer, Status=1)
        return render(request, 'wo/upload_item.html',
                        {"con": con, 'offer': offer, 'item': item})
    
    return render(request, 'wo/upload_item.html',
                  {"con": con, 'offer': offer, 'item': item})


def item_delete(request, offer_id, item_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    offer = Offer_Material.objects.get(id=offer_id)
    if Offer_Material_Item_Code.objects.filter(id=item_id, Status=1).exists():
        Advance = Offer_Material_Item_Code.objects.get(id=item_id, Status=1)
        Advance.Status = -1
        Advance.save()
        messages.add_message(request, messages.INFO, 'Item Deleted')
        item = Offer_Material_Item_Code.objects.filter(Offer_Material=offer, Status=1)
        return render(request, 'wo/upload_item.html',
                      {"con": con, 'offer': offer, 'item': item})
    messages.add_message(request, messages.INFO, 'Item Not Exists')
    item = Offer_Material_Item_Code.objects.filter(Offer_Material=offer, Status=1)
    return render(request, 'wo/upload_item.html',
                  {"con": con, 'offer': offer, 'item': item})


def material_offer_delete(request, v_id, offer_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    Vendor = TKCVendor.objects.get(id=v_id)
    if Offer_Material.objects.filter(id=offer_id, Status=1).exists():
        offer = Offer_Material.objects.get(id=offer_id, Status=1)
        item = Offer_Material_Item_Code.objects.filter(Offer_Material=offer, Status=1)
        for data in item:
            data.Status = -1
            data.save()
        offer.Status = -1
        offer.save()
    material_offer = Offer_Material.objects.filter(TKCVendor=Vendor, Status=1)
    return render(request, 'wo/material_offer.html',
                  {"con": con, 'Vendor': Vendor, 'material_offer': material_offer})


def material_offer_submit(request, v_id, offer_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    Vendor = TKCVendor.objects.get(id=v_id)
    if Offer_Material.objects.filter(id=offer_id, Status=1).exists():
        offer = Offer_Material.objects.get(id=offer_id, Status=1)
#         if Offer_Material_Item_Code.objects.filter(Offer_Material=offer, Status=1).count() == offer.Quantity:
        offer.Material_Offer_Submit = 1
        offer.Material_Offer_Submit_Submit_At = datetime.datetime.now()
        offer.save()
        messages.add_message(request, messages.INFO, 'Offer submit')
#         else:
#             messages.add_message(request, messages.INFO, 'Item Count Less Than To offer Count')
    material_offer = Offer_Material.objects.filter(TKCVendor=Vendor, Status=1)
    return render(request, 'wo/material_offer.html',
                  {"con": con, 'Vendor': Vendor, 'material_offer': material_offer})
                  
                  
import webbrowser


def invoicing(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        if TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1).exists():
            messages.add_message(request, messages.INFO, 'Record Found')
            print('invoicing')
            webbrowser.open('https://www.google.com/')
        else:
            messages.add_message(request, messages.WARNING, 'Record Not Found')
        wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/all_wo.html', {"wo": wo, 'con': con})
    else:
        messages.warning(
            request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"data": data1, 'con': con})


# def view_wo(request, PO_id):
#     procurement = TKCWoInfo.objects.filter(id=PO_id)
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
#     cdatetime = datetime.datetime.now().date()
#     data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
#     return render(request, 'tkc/view_wo.html',
#                   {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
#                    'data': data})


def upload_bg_loc(request):
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'wo/upload_bg_loc.html', {"name": data})


def upload_bg_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.bg = upload_file
        procurement_obj.save()
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})


def upload_loc_save(request, PO_id):
    procurement_obj = TKCWoInfo.objects.get(id=PO_id)
    if len(request.FILES) != 0:
        upload_file = request.FILES['loa_file']
        procurement_obj.loc = upload_file
        procurement_obj.save()
    data1 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
    return render(request, 'tkc/upload_bg_loc.html', {"name": data})

# def all_wo(request):
#     supplier = User_Registration.objects.get(Otp=request.session['otp'])
#     data = TKCWoInfo.objects.filter(supplier=supplier)
#     return render(request, 'wo/all_wo.html', {"name": data})
#
#
# def view_wo(request, PO_id):
#     procurement = TKCWoInfo.objects.filter(id=PO_id)
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     tkc = User_Registration.objects.filter(Authentication_id=procurement[0].tkc_id)
#     cdatetime = datetime.datetime.now().date()
#     data = TKCScheduleInfo.objects.filter(TKCWoInfo=procurement_obj)
#     return render(request, 'tkc/view_wo.html',
#                   {'vendor': tkc[0], "procurement": procurement[0], "date": cdatetime,
#                    'data': data})
#
#
# def upload_bg_loc(request):
#     data1 = User_Registration.objects.get(Otp=request.session['otp'])
#     data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#     return render(request, 'tkc/upload_bg_loc.html', {"name": data})
#
#
# def upload_bg(request, PO_id):
#     data1 = User_Registration.objects.get(Otp=request.session['otp'])
#     data = TKCWoInfo.objects.get(id=PO_id)
#     return render(request, 'tkc/upload_bg.html', {"data": data})
#
#
# def upload_loc(request, PO_id):
#     data = TKCWoInfo.objects.get(id=PO_id)
#     return render(request, 'tkc/upload_loc.html', {"data": data})
#
#
# def upload_bg_save(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     if len(request.FILES) != 0:
#         upload_file = request.FILES['loa_file']
#         procurement_obj.bg = upload_file
#         procurement_obj.save()
#     data1 = User_Registration.objects.get(Otp=request.session['otp'])
#     data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#     return render(request, 'tkc/upload_bg_loc.html', {"name": data})
#
#
# def upload_loc_save(request, PO_id):
#     procurement_obj = TKCWoInfo.objects.get(id=PO_id)
#     if len(request.FILES) != 0:
#         upload_file = request.FILES['loa_file']
#         procurement_obj.loc = upload_file
#         procurement_obj.save()
#     data1 = User_Registration.objects.get(Otp=request.session['otp'])
#     data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#     return render(request, 'tkc/upload_bg_loc.html', {"name": data})
#
#
# def upload_vendor(request):
#     vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
#     data1 = User_Registration.objects.get(Otp=request.session['otp'])
#     data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#     TKC = User_Registration.objects.get(Otp=request.session['otp'])
#     all_vendor = TKCVendor.objects.filter(TKC=TKC)
#     return render(request, 'tkc/upload_vendor.html', {"data": data, "vendor": vendor, 'all_vendor': all_vendor})
#
#
# def add_vendor(request):
#     if request.method == 'POST':
#         TKC = User_Registration.objects.get(Otp=request.session['otp'])
#         v_name = request.POST.get('w_id')
#         id = TKCWoInfo.objects.get(id=v_name)
#         v_id = request.POST.get('v_id')
#         vendor = User_Registration.objects.get(User_Id=v_id)
#         quantity = request.POST.get('quantity')
#         material = request.POST.get('material')
#         data = TKCVendor(TKC=TKC, TKCWoInfo=id, Vendor_id=vendor, material_name=material, quantity=quantity)
#         data.save()
#         vendor = User_Registration.objects.filter(cgm_approval=1, User_type='VENDOR')
#         data1 = User_Registration.objects.get(Otp=request.session['otp'])
#         data = TKCWoInfo.objects.filter(tkc_id=data1.Authentication_id)
#         all_vendor = TKCVendor.objects.filter(TKC=TKC)
#         return render(request, 'tkc/upload_vendor.html', {"data": data, "vendor": vendor, 'all_vendor': all_vendor})


# Fqp Code By jeevan



def invoicing(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        if TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1).exists():
            messages.add_message(request, messages.INFO, 'Record Found')
        else:
            messages.add_message(request, messages.WARNING, 'Record Not Found')
        wo = TKCWoInfo.objects.filter(supplier=supplier, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/invocing.html', {"wo": wo, 'con': con})
    else:
        messages.warning(
            request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"data": data1, 'con': con})
        
        
@api_view(['GET'])
def active_contractors_new(request):
    response = Response()
    data = User_Registration.objects.filter(User_type = 'TKC',cgm_approval=1,blacklisted = 0)
    list_value = []
    for val in data:
        data_2 = TKC_Document.objects.filter(Types_of_Docs="Electrical License",user_id=val.User_Id,Doc_expiry_date__gte=date.today())
        data3 = TKC_Payment.objects.get(id=val.Oyt)
        
        for a in data_2:


             val_2 = User_Registration.objects.filter(User_type = 'TKC',cgm_approval=1,User_Id=a.user_id)
             for v in val_2:
                 val_3 = UserCompanyDataMain.objects.filter(user_id_id=v)
                #  print([i.Company_add_1 for i in val_3 ])
                 for i in val_3:
                     print("opopoppo",data3.Name)
                     data={'user_id':v.User_Id,'user_class':data3.Name ,'user_zone':v.User_zone,'company_name':v.CompanyName_E,'email':v.Email_Id,'mobile':v.ContactNo,'authentication_id':v.Authentication_id,'address':f"{i.Company_add_1} {i.Company_add_2}{i.Company_pin_code}{i.Company_dist}{i.Company_state}"}
            #  listt = [{'user_zone':v.User_zone,'company_name':v.CompanyName_E,'email':v.Email_Id,'mobile':v.ContactNo,'authentication_id':v.Authentication_id,'address':f"{i.Company_add_1} {i.Company_add_2}{i.Company_pin_code}{i.Company_dist}{i.Company_state}"}for v in val_2 for i in val_3]
              
                     list_value.append(data)

    return HttpResponse(json.dumps(list_value), content_type="application/json")



def api_response_data(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    UserId=data.User_Id
    proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
    URL=f"https://rooftop-uat.mpcz.in:8443/deposit_scheme/api/user/vendor/getAllConsumerApplicationByVendor/{UserId}"
    data = requests.get(URL,verify=False,proxies=proxyDict).json()
    if data["list"]:
        created_data = []
        aa = []
        bb = []
        cc = []
        dd = []
        ee = []
        ff = []
        gg = []
        hh = []
        ii = []
        jj = []
        kk = []
        ll = []
        for a in data["list"]:
            one = a["schemeType"]["created"]
            two = a["schemeType"]["schemeTypeName"]
            three = a["consumers"]["consumerName"]
            four = a ["consumers"]["consumerMobileNo"]
            five = a["workType"]["workTypeName"]
            six = a["distributionCenter"]["dcName"]
            seven = a["distributionCenter"]["dcSubdivision"]["subdivisionDivision"]["division"]
            eight = a["distributionCenter"]["dcSubdivision"]["subdivisionDivision"]["divisionCircle"]["circle"]
            nine = a["consumerApplicationNo"]
            ten = a["shortDescriptionOfWork"]
            eleven = a["isRejected"]
            twelve = a["consumerApplicationId"]
            
            aa.append(one)
            bb.append(two)
            cc.append(three)
            dd.append(four)
            ee.append(five)
            ff.append(six)
            gg.append(seven)
            hh.append(eight)
            ii.append(nine)
            jj.append(ten)
            kk.append(eleven)
            ll.append(twelve)
            
        if request.method =="POST":
            ac_data = request.POST.get('ac')
            remark = request.POST.get('remark')
            print("ttttttttt",remark)
            a1 = ac_data.split('|')
            data_id=a1[1]
            data_re = a1[0]
            b2 = int(data_id)
            URL_POST="https://rooftop-uat.mpcz.in:8443/deposit_scheme/api/user/vendor/addConsumerApplicationDetails"
            data= {
                "consumerApplicationId": b2,
                "isRejected": data_re,
                "rejectionRemark": remark
                
            }
            json_data=json.dumps(data)
            headers={'Content-type':'application/json'}
            res = requests.request('POST',url=URL_POST,data=json_data,headers=headers,verify=False)
            return redirect("/tkc/api_response_data")
        final_zip = zip(jj,ii,aa,bb,cc,dd,ee,ff,gg,hh,kk,ll)
        return render(request,'tkc/tkc_apidata.html',{'final_zip':final_zip})
        
    else:
        return render(request,'tkc/tkc_apidata.html')


def tkc_reg_declare(request):
    return render(request, 'tkc/tkc_declration.html')        


def addsitestore(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    discom_data = Discom_Master.objects.all()
    return render(request, 'tkc/tkc_add_site_store.html',{'discom_data':discom_data}) 


def save_tks_site_store(request):
    discom_data = Discom_Master.objects.all()
    division = request.POST.get('division')
    division_obj = Division_Master.objects.get(id = division)
    site_store_add = request.POST.get('sitestore')
    
    rent_copy = request.POST.get('rent_copy')
    electricity_bill = request.POST.get('electricity_bill')
    consumer_no = request.POST.get('consumer_no')
    contact_no = request.POST.get('contact_no')
    autherised = request.POST.get('autherised')
    man_power = request.POST.get('man_power')

    if SiteStore_Master.objects.filter(contact_no = contact_no).exists():
        return render(request, 'tkc/tkc_add_site_store.html',{'discom_data':discom_data,"msg1":"This contact number is already registered in sitestore"})

    
    if SiteStore_Master.objects.filter(contact_no = contact_no).exists():
        return render(request, 'tkc/tkc_add_site_store.html',{'discom_data':discom_data,"msg1":"This contact number is already registered in sitestore"})

    
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    region = Region_Master.objects.filter(Discom__Discom_Code=supplier.User_zone)
    data_save = SiteStore_Master(Division = division_obj,Store_Address = site_store_add,rent_agreement_copy=rent_copy,electricity_bill=electricity_bill,consumer_no=consumer_no,contact_no=contact_no,autherised_person=autherised,man_power=man_power,supplier=supplier,created_at=dt.datetime.now())
    data_save.save()
    return render(request, 'tkc/tkc_add_site_store.html',{'region':region,'msg1': "Site store Address Added Successfully"}) 
    

def all_di(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'])
    con = User_Registration.objects.get(Otp=request.session['otp'])
    if supplier.cgm_approval:
        wo = tkc_di_master.objects.filter(wo__supplier=supplier,di_digital_upload_status=1)
        return render(request, 'wo/all_di.html', {"wo": wo, 'con': con})
    else:
        messages.warning(
            request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'con': con})

    
def view_di_material(request,di_id):
    con = User_Registration.objects.get(Otp=request.session['otp'])
    di_obj = tkc_di_master.objects.get(id=di_id)
    offer_material_data = offer_material_site_stores.objects.filter(tkc_di = di_obj)
    offer_material_dispatch_data = offer_material_site_stores.objects.filter(tkc_di = di_obj,Dispatch_Status = 1)
    if len(offer_material_data) == len(offer_material_dispatch_data):
        dispatch_status = 1
    else:
        dispatch_status = 0

    return render(request, 'wo/view_di.html',
                  {"con": con, 'offer_material_data': offer_material_data,"di_data":di_obj,"dispatch_status":dispatch_status})


def dispatch_all_di_items(request,di_id):
    con = User_Registration.objects.get(Otp=request.session['otp'])
    wo = tkc_di_master.objects.filter(wo__supplier=con,di_digital_upload_status=1)
    di_obj = tkc_di_master.objects.get(id=di_id)
    offer_material_data = offer_material_site_stores.objects.filter(tkc_di = di_obj)
    di_obj.lr_copy_or_rr_and_delivery_challan = request.FILES["lr_copy_or_rr_and_delivery_challan"]
    di_obj.packing_list_of_materials = request.FILES["packing_list_of_materials"]
    di_obj.insurance_policy_certificate = request.FILES["insurance_policy_certificate"]
    di_obj.material_guarantee_certificate = request.FILES["material_guarantee_certificate"]
    di_obj.save()
    
    for i in offer_material_data:
        i.Dispatch_Status = 1
        i.Dispatch_At = datetime.datetime.now()
        i.save()
    return render(request, 'wo/all_di.html', {"wo": wo, 'con': con})
# ,'msg2':"DI Dispatch successfully"
      

# def select_material_sitestore(request,offer_id,di_id,division_id):
#     print(division_id, "-----------------------------------------")
#     con = User_Registration.objects.get(Otp=request.session['otp'])
#     offer_data = Offer_Material.objects.get(id = offer_id)
#     di_obj = tkc_di_master.objects.get(id=di_id)
#     site_store_data = SiteStore_Master.objects.filter(supplier = con)
#     division_obj = Division_Master.objects.get(id = division_id)
#     division_offer_data = offer_material_divisions_data.objects.get(tkc_di = di_obj,wo_material =offer_data, Division = division_obj ) 
#     dispatch_material_data = Wo_Material_Dispatch_details.objects.filter(tkc_di =di_obj,Division =division_obj)
#     qty_list = []
#     for i in dispatch_material_data:
#         qty_list.append(i.quantity)
#     already_dispatch_qty = sum(qty_list)
#     return render(request, 'wo/material_dispatch_sitestore.html',
#                   {"con": con, 'offer': offer_data,"site_store_data":site_store_data,"di_data":di_obj,"dispatch_material_data":dispatch_material_data,"msg1":"You Can't Add Quantity more than offer quantity","already_dispatch_qty":already_dispatch_qty,"division_offer_data":division_offer_data,"division_obj":division_obj})


# def create_di_for_sitestore(request,offer_id,di_id,division_id):
#     con = User_Registration.objects.get(Otp=request.session['otp'])
#     offer_data = Offer_Material.objects.get(id = offer_id)
#     di_obj = tkc_di_master.objects.get(id=di_id)
#     site_store_data = SiteStore_Master.objects.filter(supplier = con)
#     division_obj = Division_Master.objects.get(id = division_id)
#     division_offer_data = offer_material_divisions_data.objects.get(tkc_di = di_obj,wo_material =offer_data, Division = division_obj )
#     dispatch_material_data = Wo_Material_Dispatch_details.objects.filter(tkc_di =di_obj,Division =division_obj)
#     Exist_offer_serial_no = Offer_Material_Item_Code.objects.filter(Offer_Material = offer_data)
#     exist_serial_no_list = []
#     for k in Exist_offer_serial_no:
#         if k.Division == None:
#             exist_serial_no_list.append(k.Item_Serial_No)  
#     print(exist_serial_no_list,"-----------------------------------")  

#     if request.method == "POST":
#         qty = request.POST.get('qty')
#         store = request.POST.get('store')
#         material_data = request.FILES["Serial_Excel"]
#         print(material_data)
#         data2 = pd.read_excel(material_data)
#         for column in data2:
#             no_list = data2[column].values
#             item_no_list = list(no_list)
#             print(item_no_list)

#         if int(qty) != int(len(item_no_list)):
#             print(len(item_no_list))
#             print(qty)
#             return render(request, 'wo/material_dispatch_sitestore.html',
#                     {"con": con, 'offer': offer_data,"site_store_data":site_store_data,"di_data":di_obj,"dispatch_material_data":dispatch_material_data,"msg2":"Quantity you offered for delivery are not equal to entered Serial no.s in Excel","division_offer_data":division_offer_data,"division_obj":division_obj})

#         qty_list = []
#         for i in dispatch_material_data:
#             qty_list.append(i.quantity)

#         if sum(qty_list) >= offer_data.Quantity:
#             return redirect(f'/tkc/select_material_sitestore/{offer_id}/{di_id}/{division_id}')
#         print(item_no_list)
#         print(exist_serial_no_list)
#         check_item =  any(item in item_no_list for item in exist_serial_no_list)
#         if check_item is False:
#             return render(request, 'wo/material_dispatch_sitestore.html',
#                     {"con": con, 'offer': offer_data,"site_store_data":site_store_data,"di_data":di_obj,"dispatch_material_data":dispatch_material_data,
#                     "msg2":"You cannot enter serial numbers other than you entered while offering material and cannot use same serial numbers which are already used for other side store","division_offer_data":division_offer_data,"division_obj":division_obj})

#         data_store = Wo_Material_Dispatch_details(tkc_di =di_obj,wo = di_obj.wo, wo_material = di_obj.wo_material, quantity =qty ,Division = division_obj,
#         supplier =di_obj.wo.supplier,Store_Address = store, created_at = datetime.datetime.now(),delivery_status = 1)
#         data_store.save()
#         for requested_serial_no in item_no_list:
#             store_division_sitesstore = Offer_Material_Item_Code.objects.get(Item_Serial_No = str(requested_serial_no),Offer_Material =offer_data )
#             store_division_sitesstore.Division = division_obj
#             store_division_sitesstore.Store_Address = store
#             store_division_sitesstore.save()
#         return redirect(f'/tkc/select_material_sitestore/{offer_id}/{di_id}/{division_id}')
#     dispatch_material_data = Wo_Material_Dispatch_details.objects.filter(tkc_di =di_obj)
#     return render(request, 'wo/material_dispatch_sitestore.html',
#                     {"con": con, 'offer': offer_data,"site_store_data":site_store_data,"di_data":di_obj,"dispatch_material_data":dispatch_material_data})


def approved_vendor_list(request):
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
    return render(request, 'tkc/all_vendor_details_tkc.html', {'data':data,'to_daaa':to_daaa,'final_lst':final_lst})
   
    
   
def vendor_check_material_tkc(request,id):
    data = User_Registration.objects.get(User_Id = id)
    material = Vendor_Material_Details.objects.filter(user_id = data,Status = 1)
    list_data = []
    for i in material:
        list_data.append(i.Material_Name)

    if request.method =="POST":
        get_data_value= request.POST.get('get_data_value')
        value_data = Vendor_Material_Details.objects.filter(user_id = data,Material_Name=get_data_value)
        return render(request, 'tkc/vendor_all_material_tkc.html', {'data':value_data}) 
    return render(request, 'tkc/view_vendor_material_tkc.html', {'data':set(list_data),'id':id})   




# *************************sitestore
def receving_wo_material(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(Dispatch_Status=1,site_store_fk=store.id).distinct('tkc_di_id')
    return render(request, 'site_store/site_store.html',{'offer': offer_object})

def receving_wo_material_circle(request,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(offer_no=offer)
    return render(request, 'site_store/site_store_circle.html',{'offer': offer_object})

def site_store_item_received(request,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id)
    nsite_list=[]
    for i in offer_object:
        nsite_list.append(i.id)
    
    item_code_table = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,offer__site_store_fk = store.id)
     
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
        return redirect(f"/tkc/site_store_wo_pdi_material_view/{tkc_di_id}/{offer}")
    return render(request, 'site_store/fqp_select_received_material.html', {'data': item_code_table,'tkc_di_id':tkc_di_id,'dataid':offer})



def site_store_item_received_officer(request,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id)
    nsite_list=[]
    for i in offer_object:
        nsite_list.append(i.id)
    
    item_code_table = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,offer__site_store_fk = store.id)
       
    if request.method =="POST":
        for data in item_code_table:
            
            pstatus = request.POST.get(f'{data.id}')
            if pstatus == None:
                
                data.Physical_Status_officer_check = data.Physical_Status_officer_check
                data.save()

            elif pstatus == 1:
                data.Physical_Status_officer_check = data.Physical_Status_officer_check
                data.save()

            elif pstatus == -1:
                data.Physical_Status_officer_check = data.Physical_Status_officer_check
                data.save()

            else:                    
                data.Physical_Status_officer_check = pstatus
                data.save()
        return redirect(f"/tkc/site_store_wo_pdi_material_view_officer/{tkc_di_id}/{offer}")
    return render(request, 'site_store/fqp_select_received_material_officer.html', {'data': item_code_table,'tkc_di_id':tkc_di_id,'dataid':offer})

def site_store_wo_pdi_material_view_officer(request,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id)
    nsite_list=[]
    for i in offer_object:
        nsite_list.append(i.id)
    
    item_code_table = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,offer__site_store_fk = store.id,Physical_Status_officer_check = 2)
       

    #item_code_table = offer_material_serial_number.objects.filter(offer_no=offer_object.offer_no,Physical_Status_officer_check = 2)
    return render(request, 'site_store/fqp_view_serial_number_officer.html', {'data': item_code_table,'tkc_di_id':tkc_di_id,'dataid':offer })
     


# def site_store_wo_pdi_material_view(request,id):
#     offer_object = offer_material_site_stores.objects.get(id=id)
#     item_code_table = offer_material_serial_number.objects.filter(offer=offer_object,Physical_Status = 2)
#     return render(request, 'site_store/fqp_view_serial_number.html', {'data': item_code_table,'dataid':id})
    
# def tkc_site_store_material_received_officer(request,offer):
   
#     if request.method =="POST":

#         Advance = offer_material_site_stores.objects.filter(offer_no=offer).last()
#         serial = offer_material_serial_number.objects.filter(offer=Advance,Physical_Status_officer_check = 2)
#         # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.offer_item.item_name,Offer_status=1,po=material.po,area_store=store_name.Name,area_store_id = material)
#         list_all=[]
       
#         for data in serial:
#             # value = DI_Material_Offer_Serial_No.objects.get(id=data.id)
#             pstatus = request.POST.get(f'{data.id}')
#             premark = request.POST.get(f'a{data.id}')
#             list_all.append(pstatus)
#             if pstatus == "-1":
                
#                 data.Physical_Status_officer_check= -1
#                 data.Status = -1
#                 data.remark=premark
#                 data.save()
        

#             elif pstatus == None:
#                 data.Physical_Status_officer_check = data.Physical_Status
#                 data.Status = data.Status
#                 data.remark = data.remark
#                 data.save()
#                 list_all[-1] = str(data.Physical_Status)

#             elif pstatus == "1":
#                 data.Physical_Status_officer_check = 1
#                 data.Status = 1
#                 data.remark=premark
#                 data.save()
#         list_check = []
#         zero = 0

#         if ("0") not in list_all and ("-1") not in list_all:
#             serial = offer_material_serial_number.objects.filter(offer = Advance)
#             for i in serial:
#                 list_check.append(i.Physical_Status)
#                 if zero not in list_check:
#                     newdata = offer_material_site_stores.objects.filter(offer_no=offer, Status=1)                
#                     newdata.update(Physical_Status_officer = '1')
                
#                 else:
#                     newdata = offer_material_site_stores.objects.filter(offer_no=offer, Status=1)  
#                     newdata.update(Physical_Status_officer = 0)
            
#         else: 
#             newdata = offer_material_site_stores.objects.filter(offer_no=offer, Status=1)                
#             newdata.update(Physical_Status = '-1')
    

#         return redirect('/tkc/receving_wo_material')    
def tkc_site_store_material_received_officer(request,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    if request.method =="POST":
        Advance = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id)
        nsite_list=[]
        for i in Advance:
            nsite_list.append(i.id)
        serial = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,Physical_Status_officer_check = 2)
        list_all=[]
        
        for data in serial:
            # value = DI_Material_Offer_Serial_No.objects.get(id=data.id)
           
            pstatus = request.POST.get(f'{data.id}')
            premark = request.POST.get(f'a{data.id}')
           
            list_all.append(pstatus)
            if pstatus == "-1":
                
                data.Physical_Status_officer_check= -1
                data.Status = -1
                data.remark=premark
                data.save()
        

            elif pstatus == None:
                data.Physical_Status_officer_check = data.Physical_Status
                data.Status = data.Status
                data.remark = data.remark
                data.save()
                list_all[-1] = str(data.Physical_Status)

            elif pstatus == "1":
                data.Physical_Status_officer_check = 1
                data.Status = 1
                data.remark=premark
                data.save()
        
        list_check = []
        zero = 0

        if ("0") not in list_all and ("-1") not in list_all:
            serial = offer_material_serial_number.objects.filter(offer_id__in=nsite_list)
            for i in serial:
                list_check.append(i.Physical_Status)
                if zero not in list_check:
                    newdata = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id, Status=1)                
                    newdata.update(Physical_Status_officer = '1')
                
                else:
                    newdata = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id, Status=1)  
                    newdata.update(Physical_Status_officer = 0)
            
        else: 
            newdata = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id, Status=1)                
            newdata.update(Physical_Status = '-1')
    

        return redirect('/tkc/receving_wo_material')   


    
def gm_circle_view_wo(request):
    if request.session.has_key('circle'):
        c_name = request.session['circle']
        wo_data = offer_material_site_stores.objects.filter(circle__Circle_Name_E = c_name,Physical_Status = 1,officer_assined = 0)    
        print(wo_data)
        return render(request, 'site_store/circle_view_wo.html', {'data': wo_data})
    return redirect('/')    

def gm_circle_assine_officer(request,id):
    if request.session.has_key('circle'):
        c_name = request.session['circle']
        wo_data = offer_material_site_stores.objects.get(id=id)    
        all_query=[]
        if request.method == "POST":
            officer_name = request.POST.get('name')
            officer_designation = request.POST.get('designation')
            mobile_no = request.POST.get('mobile')
            date = request.POST.get('date')
            officer_data = gm_circle_assine_verification_offier(offer_no=wo_data,name=officer_name,designation=officer_designation,mobile=mobile_no,verification_date=date,assine_date=datetime.datetime.now())
            officer_data.save()
            wo_data.officer_assined = 1
            wo_data.save()
            return redirect('/tkc/gm_circle_view_wo')
        return render(request, 'site_store/assine_officer.html', {'data': wo_data})
    return redirect('/')

def gm_circle_assined_officer_details(request):
    if request.session.has_key('circle'):
        c_name = request.session['circle']
        wo_data = gm_circle_assine_verification_offier.objects.filter(offer_no__circle__Circle_Name_E = c_name,offer_no__Physical_Status = 1,offer_no__officer_assined = 1)    
        print("rrererer",wo_data)
        return render(request, 'site_store/gm_circle_assined_officer_details.html', {'data': wo_data})
    return redirect('/')

# def site_store_wo_pdi_material_view(request,offer):
#     offer_object = offer_material_site_stores.objects.filter(offer_no=offer).last()
#     item_code_table = offer_material_serial_number.objects.filter(offer_no=offer_object.offer_no,Physical_Status = 2)
#     item_code_table_count = offer_material_serial_number.objects.filter(offer_no=offer_object.offer_no,Physical_Status = 2,site_store=offer_object.site_store_fk.Store_Address).count()
#     return render(request, 'site_store/fqp_view_serial_number.html', {'data': item_code_table,'dataid':offer,'count':item_code_table_count})
    
    
# def site_store_wo_pdi_material_view(request,tkc_di_id,id):
#     # offer_object = offer_material_site_stores.objects.get(id=id)
#     # item_code_table = offer_material_serial_number.objects.filter(offer=offer_object,Physical_Status = 2)

#     store = SiteStore_Master.objects.get(otp = request.session['otp'])
#     offer_object = offer_material_site_stores.objects.filter(offer_no=id,tkc_di_id=tkc_di_id,site_store_fk=store.id)
#     nsite_list=[]
#     for i in offer_object:
#         nsite_list.append(i.id)
#     item_code_table = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,offer__site_store_fk = store.id,Physical_Status = 2)
#     return render(request, 'site_store/fqp_view_serial_number.html', {'data': item_code_table,'tkc_di_id':tkc_di_id,'dataid':id})
    
def site_store_wo_pdi_material_view(request,tkc_di_id,id):
    # offer_object = offer_material_site_stores.objects.get(id=id)
    # item_code_table = offer_material_serial_number.objects.filter(offer=offer_object,Physical_Status = 2)

    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(offer_no=id,tkc_di_id=tkc_di_id,site_store_fk=store.id)
    nsite_list=[]
    for i in offer_object:
        nsite_list.append(i.id)
    
    item_code_table = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,Physical_Status = 2)
    item_code_table_count = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,Physical_Status = 2).count()
    return render(request, 'site_store/fqp_view_serial_number.html', {'data': item_code_table,'tkc_di_id':tkc_di_id,'dataid':id,'count':item_code_table_count})    

    
# def tkc_site_store_material_drr(request,offer):
#     if request.method =="POST":
#         Advance = offer_material_site_stores.objects.filter(offer_no=offer).last()
#         serial = offer_material_serial_number.objects.filter(offer_no=Advance.offer_no,Physical_Status = 2)
#         # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.offer_item.item_name,Offer_status=1,po=material.po,area_store=store_name.Name,area_store_id = material)
#         list_all=[] 
#         drr_date = request.POST.get('drr_date')
#         challan_no=request.POST.get('challan_no')
#         challan_date=request.POST.get('challan_date')
#         vehicle=request.POST.get('vehicle')
#         quantity=request.POST.get('quantity')

#         data1 = tkc_site_store_drr_info(area_store=Advance, drr_date=drr_date, drr_vehicle=vehicle,drr_challan_no=challan_no,
#                             drr_challan_date=challan_date,drr_quantity=quantity)
#         data1.save()
#         for data in serial:
#             # value = DI_Material_Offer_Serial_No.objects.get(id=data.id)
#             pstatus = request.POST.get(f'{data.id}')
#             premark = request.POST.get(f'a{data.id}')
#             list_all.append(pstatus)
#             if pstatus == "-1":
                
#                 data.Physical_Status= -1
#                 data.Status = -1
#                 data.remark=premark
#                 data.save()
        

#             elif pstatus == None:
#                 data.Physical_Status = data.Physical_Status
#                 data.Status = data.Status
#                 data.remark = data.remark
#                 data.save()
#                 list_all[-1] = str(data.Physical_Status)

#             elif pstatus == "1":
#                 data.Physical_Status = 1
#                 data.Status = 1
#                 data.remark=premark
#                 data.save()
#         list_check = []
#         zero = 0

#         if ("0") not in list_all and ("-1") not in list_all:
#             serial = offer_material_serial_number.objects.filter(offer_no = offer)
#             print("ttttt",serial.count())
#             for i in serial:
#                 list_check.append(i.Physical_Status)
#                 if zero not in list_check:
#                     print("oooooooooo")
#                     newdata = offer_material_site_stores.objects.filter(offer_no=offer, Status=1)
#                     newdata.update(Physical_Status = '1')
#                     print("qqqqqqqqqq")
#                     # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                     # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
#                     # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
#                     # response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                    
#                     # sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
#                     # sms_template.save()

#                 else:
#                     newdata = offer_material_site_stores.objects.filter(offer_no=offer, Status=1)  
#                     newdata.update(Physical_Status = 0)
            
#         else: 
#             newdata = offer_material_site_stores.objects.filter(offer_no=offer, Status=1)                
#             newdata.update(Physical_Status = '-1')
    

#         return redirect('/tkc/receving_wo_material')    
def tkc_site_store_material_drr(request,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    if request.method =="POST":
        Advance1 = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id).last()

        Advance = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id)
        nsite_list=[]
        for i in Advance:
            nsite_list.append(i.id)
        serial = offer_material_serial_number.objects.filter(offer_id__in=nsite_list,Physical_Status = 2)
        # serial = DI_Material_Offer_Serial_No.objects.filter(material=material.offer_item.item_name,Offer_status=1,po=material.po,area_store=store_name.Name,area_store_id = material)
        list_all=[] 
        drr_date = request.POST.get('drr_date')
        challan_no=request.POST.get('challan_no')
        challan_date=request.POST.get('challan_date')
        vehicle=request.POST.get('vehicle')
        quantity=request.POST.get('quantity')

        data1 = tkc_site_store_drr_info(area_store=Advance1, drr_date=drr_date, drr_vehicle=vehicle,drr_challan_no=challan_no,
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
                data.remark=premark
                data.save()
        

            elif pstatus == None:
                data.Physical_Status = data.Physical_Status
                data.Status = data.Status
                data.remark = data.remark
                data.save()
                list_all[-1] = str(data.Physical_Status)

            elif pstatus == "1":
                data.Physical_Status = 1
                data.Status = 1
                data.remark=premark
                data.save()
        list_check = []
        zero = 0

        if ("0") not in list_all and ("-1") not in list_all:
            serial = offer_material_serial_number.objects.filter(offer_id__in=nsite_list)
            print("ttttt",serial.count())
            for i in serial:
                list_check.append(i.Physical_Status)
                if zero not in list_check:
                    print("oooooooooo")
                    newdata = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id, Status=1)
                    newdata.update(Physical_Status = '1')
                    print("qqqqqqqqqq")
                    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(officer_mobile) + "&v1=" + str(otptt) + "&v2=" + str()
                    # response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                    
                    # sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = officer_mobile)
                    # sms_template.save()

                else:
                    newdata = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id, Status=1)  
                    newdata.update(Physical_Status = 0)
            
        else: 
            newdata = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id, Status=1)                
            newdata.update(Physical_Status = '-1')
    

        return redirect('/tkc/receving_wo_material')    
        
def tkc_wo_send_to_cgm(request,tkc_di_id,id):# it is for send to cgm flag not required 
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    di_master = offer_material_site_stores.objects.get(id=id,tkc_di_id=tkc_di_id,site_store_fk=store.id,Status=1,Physical_Status=1)
    di_master.send_to_cgm = 1
    di_master.save()
    return redirect('/tkc/receving_wo_material')



def tkc_wo_sample_list(request):
    officer_zone = request.session['officer']
    sampling = offer_material_site_stores.objects.filter(send_to_cgm=1,wo__zone = officer_zone).distinct('offer_no')
    return render(request, 'officer/wo_sampling.html', {'data1': sampling})


def tkc_wo_sample_sampling(request,offer):
    di_as_obj = offer_material_site_stores.objects.filter(offer_no=offer).last()
    lst_serial_number = []
    di_mosn_obj = offer_material_serial_number.objects.filter(offer_no = di_as_obj.offer_no)
    for i in di_mosn_obj:
        mat_name = i.offer.wo_material.material_name
        item_code_no = i.offer.wo_material.item_code
        if di_as_obj.excel_type == True:
            lst_serial_number.append(i.serial_no)

        elif di_as_obj.excel_type == False:
            lst_serial_number.append(i.batch_no)


    ps_obj = product_sampling.objects.filter(item_code = item_code_no).last()
    if ps_obj.sampling.sample_type == 1:
        sample_percent = ps_obj.sampling.sample_percentage
    else:
        sample_percent  = 10
    length_serial_number =  len(lst_serial_number)
    import random
    random.shuffle(lst_serial_number)

    import math
    random_mat_round_number = math.ceil((length_serial_number * sample_percent ) / 100)
    final_random_sample_mat = lst_serial_number[:random_mat_round_number]
    
    for i in final_random_sample_mat:
        if di_as_obj.excel_type == True:
            obj = offer_material_serial_number.objects.filter(serial_no=i)
            obj.update(is_sampled=1)
        elif di_as_obj.excel_type == False:
            obj = offer_material_serial_number.objects.filter(batch_no=i)
            obj.update(is_sampled=1)

        
        
        di_as_obj_new = offer_material_site_stores.objects.filter(offer_no=offer)
        for i in di_as_obj_new:
            i.sampling = 1
            i.save()
    
    lst_as = []
    lst_mat_name = []
#     for i in final_random_sample_mat:
#         dmosn_obj = offer_material_serial_number.objects.get(serial_no = i)
#         lst_mat_name.append(dmosn_obj.offer.wo_material.material_name)
        
    
#     final_zip = zip(final_random_sample_mat, lst_mat_name)
    final_zip_new = final_random_sample_mat
        
    html = "<html><body>Random Material Ids are %s. </body></html>" % final_random_sample_mat
    return render(request, 'officer/fqp_wo_forward_nabl.html', {'data1': di_as_obj, 'final_zip':final_zip_new})



from nabl.models import *



def nabl_selection(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(Dispatch_Status=1,site_store_fk=store.id,sampling=1).distinct('offer_no')
    return render(request, 'site_store/nabl_pending.html',{'offer': offer_object})

def tkc_wo_select_testing_nabl(request,offer):
    material = offer_material_site_stores.objects.filter(offer_no=offer).last()
    if nistha_nabl_lab_test_material_master.objects.filter(Material_code=material.wo_material.item_code).exists():
        nabl = NABL_Registration_Test.objects.filter(Material_Item_Code= material.wo_material.item_code)
        all_query=[]
        for data in nabl:
            user = User_Registration.objects.filter(CompanyName_E='Nishtha Testing Laboratory') | User_Registration.objects.filter(CompanyName_E='GWALIOR TESTING LABORATORY MPMKVVCL GWALIOR')
            all_query.append(user)

        if request.method == "POST":
            nabl_name = request.POST.get('nabl')
            nabl_number = User_Registration.objects.get(CompanyName_E=request.POST.get('nabl'))
            material_new = offer_material_site_stores.objects.filter(offer_no=offer)
            for i in material_new:
                i.nabl_name = nabl_name
                i.nabl_status = 1
                i.nabl_number = nabl_number.ContactNo
                i.save()
                
            return redirect('/tkc/nabl_selection')
        return render(request, 'site_store/nabl_selection.html', {'data': material,'nabl':all_query})
    else:
#         nabl = NABL_Registration_Test.objects.filter(Material_Item_Code= material.wo_material.item_code)
        nabl = NABL_Registration_Test.objects.filter(Material_Item_Code= material.wo_material.item_code) | NABL_Registration_Test.objects.filter(material_code_ez= material.wo_material.item_code) | NABL_Registration_Test.objects.filter(material_code_wz= material.wo_material.item_code)
        all_query=[]
        for data in nabl:
            user = User_Registration.objects.filter(User_Id=data.user_id)
            all_query.append(user)

        if request.method == "POST":
            nabl_name = request.POST.get('nabl')
            nabl_number = User_Registration.objects.filter(CompanyName_E=request.POST.get('nabl')).last()
            material_new = offer_material_site_stores.objects.filter(offer_no=offer)
            for i in material_new:
                i.nabl_name = nabl_name
                i.nabl_status = 1
                i.nabl_number = nabl_number.ContactNo
                i.save()
                
            return redirect('/tkc/nabl_selection')
        return render(request, 'site_store/nabl_selection.html', {'data': material,'nabl':all_query})


def tkc_nabl_selection_new(request):
    store = SiteStore_Master.objects.filter(otp = request.session['otp']).first()
    print("sop------",store.otp)    
    offer_object = offer_material_site_stores.objects.filter(Dispatch_Status=1,site_store_fk=store.id,sampling=1).exclude(tkc_di_id__isnull=True).distinct('tkc_di_id')
    return render(request, 'site_store/nabl_pending_new.html',{'offer': offer_object,'store':"store"})


# old my new code working  
# def tkc_wo_select_testing_nabl_new(request,tkc_di_id,offer):# created by shubham tripathi for select testing lab detail
#     store = SiteStore_Master.objects.filter(otp = request.session['otp']).first()
#     if store is not None:
#         material = list(offer_material_serial_number.objects.filter(offer__site_store_fk_id=store.id,offer__offer_no=offer,offer__tkc_di_id=tkc_di_id,is_sampled=1,offer__sampling=1).distinct('wo_material').values('wo_material__item_code'))
#         offer_data=offer_material_serial_number.objects.filter(offer__site_store_fk_id=store.id,offer__offer_no=offer,offer__tkc_di_id=tkc_di_id,is_sampled=1,offer__sampling=1).distinct('wo_material')
#         item_code=[]
#         for i in material:
#             item=i["wo_material__item_code"]
#             item_code.append(item)
#         print("-------",item_code)
#         if nistha_nabl_lab_test_material_master.objects.filter(Material_code__in=item_code).exists():
#             nabl = NABL_Registration_Test.objects.filter(Material_Item_Code__in= item_code)
#             all_user=[]
#             for data in nabl:
#                 all_user.append(data.user_id)
#             all_nabl_user = User_Registration.objects.filter(Q(User_Id__in=all_user,CompanyName_E='Nishtha Testing Laboratory') | Q(User_Id__in=all_user,CompanyName_E='GWALIOR TESTING LABORATORY MPMKVVCL GWALIOR')) 

#             if request.method == "POST":
#                 nabl_user_id = request.POST.getlist('nabl_user_id[]')
#                 user_len=range(len(nabl_user_id))
#                 item_id = request.POST.getlist('item_id[]')
#                 item_code = request.POST.getlist('wo_item_code[]')
#                 for i in user_len:
#                     nabl_data = User_Registration.objects.filter(User_Id=nabl_user_id[i]).first()
#                     offer_material_site_stores.objects.filter(offer_no=offer,wo_material_id=item_code[i],tkc_di_id=tkc_di_id,site_store_fk_id=store.id).update(nabl_user_id=nabl_data.User_Id,nabl_status = 1)
#                 return redirect('/tkc/tkc_nabl_selection_new')
#             return render(request, 'site_store/nabl_selection_new.html', {'offer_no':offer,'tkc_di_id':tkc_di_id,'offer_data':offer_data ,'all_nabl_user':all_nabl_user,'store':store})
#         else:
#             print("---2----",item_code)
#             nabl = NABL_Registration_Test.objects.filter(Q(Material_Item_Code__in=item_code) | Q(material_code_ez__in= item_code) | Q(material_code_wz__in= item_code))
#             all_user=[]
#             for data in nabl:
#                 all_user.append(data.user_id)
#             all_nabl_user = (User_Registration.objects.filter(User_Id__in=all_user).distinct('User_Id'))
#             if request.method == "POST":
#                 nabl_user_id = request.POST.getlist('nabl_user_id[]')
#                 user_len=range(len(nabl_user_id))
#                 item_id = request.POST.getlist('item_id[]')
#                 item_code = request.POST.getlist('wo_item_code[]')
#                 for i in user_len:
#                     nabl_data = User_Registration.objects.filter(User_Id=nabl_user_id[i]).first()
#                     offer_material_site_stores.objects.filter(offer_no=offer,wo_material_id=item_code[i],tkc_di_id=tkc_di_id,site_store_fk_id=store.id).update(nabl_status = 1, nabl_user_id=nabl_data.User_Id)
#                 return redirect('/tkc/tkc_nabl_selection_new')
#             return render(request, 'site_store/nabl_selection_new.html', {'offer_no':offer,'tkc_di_id':tkc_di_id,'offer_data':offer_data,'all_nabl_user':all_nabl_user,'store':store})
#     else:
#         return redirect(curl)

# ------------end her code working ------------------------------

def tkc_wo_select_testing_nabl_new(request,tkc_di_id,offer):# created by shubham tripathi for select testing lab detail
    store = SiteStore_Master.objects.filter(otp = request.session['otp']).first()
    if store is not None:
        if request.method == "POST":
            nabl_user_id = request.POST.getlist('nabl_user_id[]')
            print("nabl_user_id----d-----",nabl_user_id)
            user_len=range(len(nabl_user_id))
            
            item_id = request.POST.getlist('item_id[]')
            item_code = request.POST.getlist('wo_item_code[]')
            print("item----d-----",item_code)
            print("user_len----------",user_len)
            for i in user_len:
                c=offer_material_site_stores.objects.filter(offer_no=offer,wo_material_id=item_code[i],tkc_di_id=tkc_di_id,site_store_fk_id=store.id).count()
                print(c,"----------",item_code[i])
                nabl_data = User_Registration.objects.filter(User_Id=nabl_user_id[i]).first()
                offer_material_site_stores.objects.filter(offer_no=offer,wo_material_id=item_code[i],tkc_di_id=tkc_di_id,site_store_fk_id=store.id).update(nabl_user_id=nabl_data.User_Id,nabl_status = 1)
            return redirect('/tkc/tkc_nabl_selection_new')
        else:
            material = list(offer_material_serial_number.objects.filter(offer__site_store_fk_id=store.id,offer__offer_no=offer,offer__tkc_di_id=tkc_di_id,is_sampled=1,offer__sampling=1).distinct('wo_material').values('wo_material__item_code'))
            offer_data=offer_material_serial_number.objects.filter(offer__site_store_fk_id=store.id,offer__offer_no=offer,offer__tkc_di_id=tkc_di_id,is_sampled=1,offer__sampling=1).distinct('wo_material')
            item_code=[]
            for i in material:
                item=i["wo_material__item_code"]
                item_code.append(item)
        
            # if all(nistha_nabl_lab_test_material_master.objects.filter(Material_code=code).exists() for code in item_code_upper):
            if nistha_nabl_lab_test_material_master.objects.filter(Material_code__in=item_code).exists():
                nabl = NABL_Registration_Test.objects.filter(Material_Item_Code__in= item_code)
                all_user=[]
                for data in nabl:
                    all_user.append(data.user_id)
                all_nabl_user = User_Registration.objects.filter(Q(User_Id__in=all_user,CompanyName_E='Nishtha Testing Laboratory') | Q(User_Id__in=all_user,CompanyName_E='GWALIOR TESTING LABORATORY MPMKVVCL GWALIOR')) 
                return render(request, 'site_store/nabl_selection_new.html', {'offer_no':offer,'tkc_di_id':tkc_di_id,'offer_data':offer_data ,'all_nabl_user':all_nabl_user,'store':store})
            else:
                nabl = NABL_Registration_Test.objects.filter(Q(Material_Item_Code__in=item_code) | Q(material_code_ez__in= item_code) | Q(material_code_wz__in= item_code))
                all_user=[]
                for data in nabl:
                    all_user.append(data.user_id)
                all_nabl_user = (User_Registration.objects.filter(User_Id__in=all_user).distinct('User_Id'))

                return render(request, 'site_store/nabl_selection_new.html', {'offer_no':offer,'tkc_di_id':tkc_di_id,'offer_data':offer_data,'all_nabl_user':all_nabl_user,'store':store})
    else:
        return redirect(curl)






def tkc_wo_trf_create(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    di_as_obj = offer_material_site_stores.objects.filter(site_store_fk=store.id,nabl_status=1,sampling=1).distinct('offer_no')

    return render(request, 'site_store/tkc_wo_trf_details.html', {'data1': di_as_obj})

def tkc_wo_trf_create_new(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    di_as_obj = offer_material_site_stores.objects.filter(site_store_fk=store.id,nabl_status=1,sampling=1).distinct('nabl_user_id').exclude(nabl_user_id__isnull=True)
    return render(request, 'site_store/tkc_wo_trf_details_new.html', {'data1': di_as_obj})


def tkc_wo_nabl_gatepass_new(request,offer):
    officer = SiteStore_Master.objects.get(otp = request.session['otp'])
    material = offer_material_site_stores.objects.filter(offer_no=offer).last()
    obj_item = offer_material_serial_number.objects.filter(offer_no = material.offer_no,is_sampled=1)
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
    
        data1 = tkc_wo_nabl_gatepass(offer_number = material,gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                            driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,gate_pass=gatepass,Store_Address=obj_item[0].site_store, 
                            material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh,aname = material.nabl_name)
        data1.save()

        material_new = offer_material_site_stores.objects.filter(offer_no=offer)
        for i in material_new:
            i.nabl_gatepass_status = 1
            i.save()

        return render(request, 'site_store/fqp_wo_nabl_gatepass_print.html', {'data': material,'material':obj_item,'data1':data1})
    
    return render(request, 'site_store/fqp_wo_nabl_gatepass.html', {'data': material,'material':obj_item})


def tkc_wo_nabl_gatepass_new_new(request,nabl_user_id,tkc_di_id,offer_no):# created by shubham tripathi for save gatepass detail
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    if store:
        print("store-----------",store.id)
        offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,site_store_fk=store.id,nabl_status=1,sampling=1,nabl_user_id=nabl_user_id).first()
        offer_1id=offer_data.id
        material = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,site_store_fk=store.id,nabl_status=1,sampling=1,nabl_user_id=nabl_user_id)
        serial_no_item = offer_material_serial_number.objects.filter(offer_id__in = material,is_sampled=1)
        print("seriali_no_item-----------",serial_no_item)
        if request.method == "POST":
            # nabl_name = request.POST.get('nabl_name')
            site_store_address = request.POST.get('site_store_address')
            gp_date = request.POST.get('gatepass_date')
            gp_num=request.POST.get('gatepass_no')
            gatekeep_name=request.POST.get('gk_name')
            veh_no=request.POST.get('vehicle_no')
            driv_name=request.POST.get('driver_name')
            driv_phone=request.POST.get('driver_phone')
            mater_rec_by=request.POST.get('mat_rece_by')
            driver_aadh=request.FILES['driver_aadhar']
            # gatepass = request.FILES['gatepass']
            offer_no = request.POST.get('offer_no')
            print("offer_no------",offer_no)
            offer_id = request.POST.getlist('offer_id[]')
            tkc_di_id = request.POST.get('tkc_di_id')
            print("tkc_di_id=-----------------",tkc_di_id)
            outward_quantity=request.POST.getlist('outward_quantity[]')
            # item_id=request.POST.getlist('item_id[]')
            serial_no_id=request.POST.getlist('serial_no_id[]')
            # outward_quantity_sum = list(map(int, outward_quantity))
            nabl_user_id = request.POST.get('nabl_user_id')
            # tkc_di_id = request.POST.get('tkc_di_id')
            # outward_quantity_sum=sum(outward_quantity_sum)
        
            gatepass_data = tkc_wo_nabl_gatepass(offer_no = offer_no,nabl_user_id=nabl_user_id,site_store_id=store.id,tkc_di_id=tkc_di_id,gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date, 
                                material_rec_by=mater_rec_by,driver_aadhar=driver_aadh,nabl_gatepass=1)
            gatepass_data.save()
            gate_pass_id=gatepass_data.id

            # print("gt dat---------------",gatepass_data)
            serial_no_len = range(len(serial_no_id))
            cd=datetime.date.today()
            print("cd-------------",cd)
            if gatepass_data is not None:
                for i in range(len(serial_no_len)):
                    # print("i-------------",1)
                    offer_material_serial_number.objects.filter(id=serial_no_id[i]).update(site_store_gatepass = gatepass_data.id)
                    offer_material_site_stores.objects.filter(id=offer_id[i],tkc_di_id=tkc_di_id).update(site_store_gatepass = 1)
            
                offer_data = offer_material_serial_number.objects.filter(site_store_gatepass = gatepass_data.id)
                # print(offer_data,"---off----------------gate-",gatepass_data.id)
                return render(request, 'site_store/wo_nabl_gatepass_print_new.html', {'gatepass_data': gatepass_data,'offer_data':offer_data,'current_date':cd})
                # url = reverse('GatepassLetterTKCView',args=[nabl_user_id,tkc_di_id,offer_1id,gate_pass_id])
            
                # return redirect(url) 
                # return redirect(tkc_wo_trf_create)
        return render(request, 'site_store/wo_nabl_gatepass_create_new.html', {'offer_data': offer_data,'serial_no_item':serial_no_item})
    else:
        pass

# def GatepassLetterTKCView(request,nabl_user_id,tkc_di_id,offer_1id,gate_pass_id):
#     store = SiteStore_Master.objects.get(otp = request.session['otp'])
#     gatepass_data=tkc_wo_nabl_gatepass.objects.filter(id=gate_pass_id).first()
#     print("-----------",gatepass_data)
#     offer_data1=offer_material_site_stores.objects.filter(id=offer_1id).first()
#     offer_no=offer_data1.offer_no
#     offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,site_store_fk=store.id,nabl_status=1,sampling=1,nabl_user_id=nabl_user_id).first()
#     material = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,site_store_fk=store.id,nabl_status=1,sampling=1,nabl_user_id=nabl_user_id)
#     serial_no_item = offer_material_serial_number.objects.filter(offer_id__in = material,is_sampled=1)
#     return render(request, 'site_store/tkc_gatepass_letter.html', {'gatepass_data': gatepass_data,'offer_data':serial_no_item,'offer_data1':offer_data})

def tkc_site_store_gatepass_letter_print(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    if store:
        if request.method == "POST":
            gatepass_id=request.POST.get('gate_pass_id')
            # print("gpi--------",gatepass_id)
            tkc_gatepass_data=tkc_wo_nabl_gatepass.objects.get(id=gatepass_id)
            gatepass_file_new = request.FILES['gatepass_file']
            # print("gate_pass_id-------new----------",gate_pass_id)
            # print("gatepass-------new----------",gatepass_file_new)
            tkc_gatepass_data.gate_pass=gatepass_file_new
            tkc_gatepass_data.save()           
            return redirect('tkc_wo_trf_create_new')
        else:
            return redirect('tkc_wo_trf_create_new')
def show_sitestore_gatepass(request,tkc_di_id,offer_no):    
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_obj=offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,site_store_fk=store.id,nabl_status=1,sampling=1,nabl_name__isnull=False).distinct('nabl_name')
    gatepass_detail=tkc_wo_nabl_gatepass_detail.objects.filter(offer__in=offer_obj,tkc_di_id=tkc_di_id,serial_no__gatepass_created_status=True,serial_no__nabl_status=1,serial_no__is_sampled=1)
    return render(request,'site_store/show_sitestore_gatepass.html',{'offer_obj':offer_obj,'gatepass_detail':gatepass_detail})




# def sitestore_view_gatepass(request,tkc_di_id,offer_no):
#     store = SiteStore_Master.objects.filter(otp = request.session['otp']).first()
#     offer_object = offer_material_site_stores.objects.filter(site_store_fk=store.id,sampling=1,offer_no=offer_no,tkc_di_id=tkc_di_id)
#     serial_object = offer_material_site_stores.objects.filter(offer__in=offer_object,gatepass_created_status=True,nabl_status=1,is_sampled=1)
#     gatepass_detail_object = offer_material_site_stores.objects.filter(offer__in=offer_object,serial_no__in=serial_object)
#     return render(request, 'site_store/wo_nabl_gatepass_print.html',{'gatepass_detail_object': gatepass_detail_object,'store':"store"})

def tkc_nabl_gatepass_letter(request,gate_pass_id,nabl_gatepass_id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    gate_pass_detail=tkc_wo_nabl_gatepass_detail.objects.filter(gatepass_id=gate_pass_id)
    if nabl:
        if request.method == "POST":
            nabl_gatepass_data=tkc_wo_nabl_gatepass.objects.filter(id=nabl_gatepass_id).first()
            gatepass = request.FILES['gatepass']
            nabl_gatepass_data.gate_pass=gatepass
            nabl_gatepass_data.save()
            
            return redirect('tkc_nabl_sampling_wo')


def tkc_site_store_view_samled_material(request,offer):
    material = offer_material_site_stores.objects.filter(offer_no=offer).last()
    di_area_store = offer_material_serial_number.objects.filter(offer_no = material.offer_no,is_sampled=1)
    return render(request, 'site_store/tkc_site_store_view_sampled_item.html', {'final_zip':di_area_store})

def tkc_site_store_view_samled_material_new(request,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    if store:
        material = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,sampling=1)
        # print("diare------------------",material)
        di_area_store = offer_material_serial_number.objects.filter(offer_id__in = material,is_sampled=1)
        # print("diare------------------",di_area_store)
        return render(request, 'site_store/tkc_site_store_view_sampled_item_new.html', {'final_zip':di_area_store})
    else:
        return redirect(curl)

def tkc_view_samled_material(request,offer):
    material = offer_material_site_stores.objects.filter(offer_no=offer).last()
    di_area_store = offer_material_serial_number.objects.filter(offer_no = material.offer_no,is_sampled=1)
    return render(request, 'officer/fqp_view_sampled_material.html', {'final_zip':di_area_store})

def tkc_wo_sampled_item(request,offer):
    officer = SiteStore_Master.objects.get(otp = request.session['otp'])
    material = offer_material_site_stores.objects.filter(offer_no=offer).last()
    serial = offer_material_serial_number.objects.filter(offer_no = material.offer_no,is_sampled=1)
    return render(request, 'site_store/sitestore_view_sampled_item.html', {'data': serial,'dataid':id})


def tkc_wo_sampled_item_new(request,nabl_user_id,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    if store:
        material = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id)
        serial = offer_material_serial_number.objects.filter(offer__in= material,is_sampled=1)
        return render(request, 'site_store/sitestore_view_sampled_item_new.html', {'data': serial,'dataid':id})
    else:
        return redirect(curl)        

def tkc_wo_receive_from_nabl(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(accept_from_nabl=1,site_store_fk=store.id).distinct('offer_no')
    return render(request, 'site_store/tkc_wo_nabl_received_details.html', {'data1': offer_object})


def site_store_item_received_from_nabl(request,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(offer_no=offer).last()
    item_code_table = offer_material_serial_number.objects.filter(offer_no=offer_object.offer_no,is_sampled=1)
       
    if request.method =="POST":
        for data in item_code_table:
            
            pstatus = request.POST.get(f'{data.id}')
            if pstatus == None:
                data.Physical_Status_Nabl = data.Physical_Status_Nabl
                data.save()

            elif pstatus == 1:
                data.Physical_Status_Nabl = data.Physical_Status_Nabl
                data.save()

            elif pstatus == -1:
                data.Physical_Status_Nabl = data.Physical_Status_Nabl
                data.save()
            else:                    
                data.Physical_Status_Nabl = pstatus
                data.save()

            offer_object_new = offer_material_site_stores.objects.filter(offer_no=offer)
            for i in offer_object_new:
                i.received_from_nabl = 1
                i.save()
        return redirect(f"/tkc/tkc_wo_receive_from_nabl")
    return render(request, 'site_store/fqp_select_received_material_from_nabl.html', {'data': item_code_table,'dataid':offer})




def tkc_wo_test_request_form_submit(request,offer):
    officer = SiteStore_Master.objects.get(otp = request.session['otp'])
    material = offer_material_site_stores.objects.filter(offer_no=offer).last()
    obj_item = offer_material_serial_number.objects.filter(offer_no = material.offer_no,is_sampled=1)
    gate_pass_number = tkc_wo_nabl_gatepass.objects.filter(offer_number = material)
    if request.method == "POST":
        material = offer_material_site_stores.objects.filter(offer_no=offer).last()
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

        trf_obj = Tkc_Work_Order_Trf_Details(offer_number = material ,TRFAreastore_file=trf_file,
                              customer_Organization_name=customer_Organization_name, 
                              customer_Organization_address=customer_Organization_address,
                              contact_person_name=contact_person_name,
                              contact_person_designation=contact_person_designation, 
                              mobile_no=mobile_no, email_id=email_id, 
                              name_of_sample_product=name_of_sample_product, 
                              customer_ref_gatepass_no=customer_ref_gatepass_no, 
                              dated=dated,  trf_generated = 1,nabl_name = material.nabl_name,nabl_number=material.nabl_number)


        trf_obj.save()
       
        material_new = offer_material_site_stores.objects.filter(offer_no=offer)
        for i in material_new:
            i.trf_status = 1
            i.save()

        list_check = []
        zero = 0

        trf_data = Tkc_Work_Order_Trf_Details.objects.filter(offer_number=material).last()
        material.save()
        return render(request, 'site_store/fqp_wo_test_request_view.html', {'material': material,'trf':trf_data,'gate_pass_number':gate_pass_number[0]})
    return render(request, 'site_store/fqp_wo_test_request_form.html',{'material': material,'gate_pass_number':gate_pass_number[0]})


def outward_gatepass(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offer_object = offer_material_site_stores.objects.filter(site_store_fk=store.id,gatepass=1)
    return render(request,'site_store/reject_di.html',{'offer': offer_object})

    # item_code_table = offer_material_serial_number.objects.filter(offer=offer_object)


def tkc_reject_di_material_view(request,id):
    if request.session.has_key('otp'):
        store = SiteStore_Master.objects.get(otp = request.session['otp'])
        offer_object = offer_material_site_stores.objects.get(id=id)
        serial = offer_material_serial_number.objects.filter(offer=offer_object,Physical_Status='-1',Status='-1')
        return render(request, 'site_store/reject_di_material_view.html', {'data': serial,'dataid':id})
    return redirect('/')


def select_material_for_getpass(request,id):
    if request.session.has_key('otp'):
        store_name =SiteStore_Master.objects.get(otp = request.session['otp'])
        offer_object = offer_material_site_stores.objects.get(id=id)
        serial = offer_material_serial_number.objects.filter(offer=offer_object,Physical_Status='-1',Status='-1')
        if request.method =="POST":
            for data in serial:
                pstatus = request.POST.get(f'{data.id}')
                if pstatus == None:
                    data.accepted = data.accepted
                    data.save()

                elif pstatus == 1:
                    data.accepted = data.accepted
                    data.save()


                else:                    
                    data.accepted = pstatus
                    data.save()
              
            return redirect(f'/tkc/create_wo_gatepass_outward/{id}')

        return render(request, 'site_store/select_material_for_getpass.html', {'data': serial,'dataid':id})
    return redirect('/')




def create_wo_gatepass_outward(request,id):
    if request.session.has_key('otp'):
        store_name =SiteStore_Master.objects.get(otp = request.session['otp'])
        offer_object = offer_material_site_stores.objects.get(id=id)
        reject_item = offer_material_serial_number.objects.filter(offer=offer_object,Physical_Status='-1',Status='-1',accepted=2)

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

            data1 = wo_outward_gatepass(offer=offer_object, gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date,aname = store_name.Store_Address,
                                material_rec_by=mater_rec_by,outward_quantity=quantity,driver_aadhar=driver_aadh)
            data1.save()
            offer_object.gatepass = 1
            offer_object.save()
            gatepass_object = wo_outward_gatepass.objects.latest('id')
            for i in reject_item:
                i.accepted = 1
                i.gatepass = 1
                i.gatepass_number = gatepass_object
                i.save()
            reject_item = offer_material_serial_number.objects.filter(offer=offer_object,Physical_Status='-1',Status='-1',gatepass=1)

            return render(request, 'site_store/po_gatepass_outward_print.html', {'data': offer_object,'material':reject_item,'data1':data1})
        
        return render(request, 'site_store/po_gatepass_outward.html', {'data': offer_object,'material':reject_item})
    return redirect('/')


def outward_gatepass_history(request):
    if request.session.has_key('otp'):
        store_name =SiteStore_Master.objects.get(otp = request.session['otp'])
        di_master = wo_outward_gatepass.objects.filter(offer__site_store = store_name.Store_Address)
        return render(request, 'site_store/gatepass_history.html', {'data': di_master})
    return redirect('/')


def outward_gatepass_view(request,id):
    if request.session.has_key('otp'):
        store_name =SiteStore_Master.objects.get(otp = request.session['otp'])
        data1 = wo_outward_gatepass.objects.get(id=id)
        material = offer_material_serial_number.objects.filter(gatepass_number=data1)
        
        return render(request, 'site_store/po_gatepass_outward_print_new.html', {'data1': data1,'material':material})
        
    return redirect('/')

# def add_officer_details(request,offer):
#     store = SiteStore_Master.objects.get(otp = request.session['otp'])
#     offcer_obj = offer_material_site_stores.objects.filter(offer_no=offer).last()
#     # zone = offcer_obj.wo.zone
#     # print("ffffff",zone)
#     pv_offcer_obj = sitestore_pi_verification.objects.filter(zone = offcer_obj.wo.zone)
#     if request.method == "POST":
#         name = request.POST.get('name')
#         designation=request.POST.get('designation')
#         mobile=request.POST.get('mobile')
#         report=request.FILES['report']
#         officer_from=request.POST.get('officer_from')
#         save_data = pi_verification_offier(site_store=offcer_obj,name=name,designation=designation,officer_from=officer_from,mobile=mobile,report=report)
#         save_data.save()

#         offcer_obj_new = offer_material_site_stores.objects.filter(offer_no=offer)
#         offcer_obj_new.update(officer_checked = 1,report = report,final_check = 1)
#         # offcer_obj.final_check = 1

#         # new_obj = offer_material_site_stores.objects.filter(offer_no = offcer_obj.offer_no)
#         # new_list = []
#         # for i in new_obj:
#         #     new_list.append(i.officer_checked)

#         # if (0) not in new_list and (-1) not in new_list:
#         #     new_obj.update(final_check = 1)
            
#         return redirect('/tkc/receving_wo_material')
#     return render(request,'site_store/pv_officer_form.html',{'dataid':offer,'pv_offcer_obj':pv_offcer_obj})
def add_officer_details(request,tkc_di_id,offer):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    offcer_obj = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id).last()
    #zone = offcer_obj.wo.zone
    #print("fffffhhhhhhhhhhhhhhhhhhhhhf",zone)
    #pv_offcer_obj = sitestore_pi_verification.objects.filter(zone = offcer_obj.wo.zone)
    if request.method == "POST":
        name = request.POST.get('name')
        designation=request.POST.get('designation')
        mobile=request.POST.get('mobile')
        report=request.FILES['report']
        officer_from=request.POST.get('officer_from')
        save_data = pi_verification_offier(site_store=offcer_obj,name=name,designation=designation,officer_from=officer_from,mobile=mobile,report=report)
        save_data.save()

        offcer_obj_new = offer_material_site_stores.objects.filter(offer_no=offer,tkc_di_id=tkc_di_id,site_store_fk=store.id)
        offcer_obj_new.update(officer_checked = 1,report = report,final_check = 1)
        # offcer_obj.final_check = 1

        # new_obj = offer_material_site_stores.objects.filter(offer_no = offcer_obj.offer_no)
        # new_list = []
        # for i in new_obj:
        #     new_list.append(i.officer_checked)

        # if (0) not in new_list and (-1) not in new_list:
        #     new_obj.update(final_check = 1)
            
        return redirect('/tkc/receving_wo_material')
    return render(request,'site_store/pv_officer_form.html',{'dataid':offer,'tkc_di_id':tkc_di_id})

# multiple material offer of  wo from tkc side code start

def all_vendor(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    all_wo = TKCWoInfo.objects.filter(supplier = con,Wo_Approved_Status = 1,Wo_Digital_Upload_Status = 1)
    # all_vendor = TKCVendor.objects.filter(TKCWoInfo__supplier=con, TKCVendor_Approved_Status=1, Status=1)
    return render(request, 'wo/all_vendor.html', {"con": con, 'all_wo': all_wo})


def wo_approve_vendor_list(request, wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    all_approved_vendor = TKCVendor.objects.filter(TKCWoInfo__supplier=con,TKCWoInfo =wo_id , TKCVendor_Approved_Status=1, Status=1).distinct('Vendor')
    return render(request, 'wo/wo_approved_vendor.html', {"con": con, 'all_approved_vendor': all_approved_vendor})


def wo_approve_vendor_material_list(request,wo_id,vendor_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    vendor_data = User_Registration.objects.get(User_Id = vendor_id)
    all_approved_vendor_material = TKCVendor.objects.filter(TKCWoInfo__supplier=con,TKCWoInfo =wo_id ,Vendor = vendor_data, TKCVendor_Approved_Status=1, Status=1)
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    wo_discom = wo_data.Discom.Discom_Code
    return render(request, 'wo/wo_approved_vendor_material.html', {"con": con, 'all_approved_vendor_material': all_approved_vendor_material,"wo_id":wo_id,"vendor_id":vendor_id,"wo_discom":wo_discom})

def wo_approve_vendor_material_list_test(request,wo_id,vendor_id,boq_id,supplier_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    vendor_data = User_Registration.objects.get(User_Id = vendor_id)
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    wo_discom = wo_data.Discom.Discom_Code
    boq_data = tkc_wo_items_boq.objects.get(id = boq_id)
    sitestore_data = SiteStore_Master.objects.filter(supplier = con)
    all_approved_vendor_material = TKCVendor.objects.filter(TKCWoInfo__supplier=con,TKCWoInfo =wo_id ,Vendor = vendor_data, TKCVendor_Approved_Status=1, Status=1)
    new_added_data = offer_material_site_stores.objects.filter(wo = wo_id,TKCVendor__Vendor=vendor_data,supplier = supplier_id,offer_no = None)
    updated_store_data = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data,Material_Offer_Submit_Approved_Status__in = (1,0))
    new_added_data_id_list = []
    for i in new_added_data:
        if i.is_serial_excel_uploaded == False:
            return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"wo_id":wo_id,"updated_store_data":updated_store_data,"vendor_id":vendor_id,"msg1":"please upload the serial no/batch no excel of added material offers"})
        new_added_data_id_list.append(i.id)
    return render(request, 'wo/wo_approved_vendor_material.html', {"con": con, 'all_approved_vendor_material': all_approved_vendor_material,"wo_id":wo_id,"vendor_id":vendor_id,"new_added_data":new_added_data,"new_added_data_id_list":new_added_data_id_list,"wo_discom":wo_discom})


def wo_material_offer_step1(request,wo_id,itemcode,vendor_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    boq_data = tkc_wo_items_boq.objects.get(item_code = itemcode,wo = wo_id)
    sitestore_data = SiteStore_Master.objects.filter(supplier = con) 
    updated_store_data = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data,Material_Offer_Submit_Approved_Status__in = (1,0))
    return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"wo_id":wo_id,"updated_store_data":updated_store_data,"vendor_id":vendor_id})


def save_material_offer_store(request,wo_id,itemcode,vendor_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    boq_data = tkc_wo_items_boq.objects.get(item_code = itemcode,wo = wo_id)
    sitestore_data = SiteStore_Master.objects.filter(supplier = con)
    vendor = User_Registration.objects.get(User_Id =vendor_id )
    wo_discom = wo_data.Discom.Discom_Code
    if wo_discom == 'CZ':
        vendor_material = Vendor_Material_Details.objects.get(user_id = vendor,item_code =itemcode )
    elif wo_discom == 'EZ':
        vendor_material = Vendor_Material_Details.objects.get(user_id = vendor,item_code_ez =itemcode )
    elif wo_discom == 'WZ':
        vendor_material = Vendor_Material_Details.objects.get(user_id = vendor,item_code_wz =itemcode )
    tkc_vendor = TKCVendor.objects.get(TKCWoInfo = wo_data,Vendor = vendor,Material_id = vendor_material,TKCVendor_Approved_Status=1)
    if request.method == "POST":
        store_name = request.POST.get('areastore')
        store_data = SiteStore_Master.objects.get(id = store_name)
        quantity = request.POST.get('qty')
        serial_number_value = request.POST.get('serial_number_value')
        circle_id = request.POST.get('store_circles')
        circle_data = Circle_Master.objects.get(id = circle_id)
        updated_store_data1 = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data,Material_Offer_Submit_Approved_Status__in = (1,0))
        boq_balance_qty = round(float(boq_data.balance_qty),2)
        if float(quantity)>boq_balance_qty:
            return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"wo_id":wo_id,"updated_store_data":updated_store_data1,"msg1":"You can't offer quantity more than balanced quantity","vendor_id":vendor_id})
        data_already_exist = offer_material_site_stores.objects.filter(wo = wo_data,wo_material= boq_data)
#         if len(data_already_exist)>0:
#             return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"wo_id":wo_id,"updated_store_data":updated_store_data1,"msg1":"You have already selected this sitestore for this item","vendor_id":vendor_id})
        data_store = offer_material_site_stores(wo =wo_data,wo_material = boq_data,quantity = float(quantity) ,site_store = store_data.Store_Address,supplier = con,created_at = datetime.datetime.now(),
                                                TKCVendor=tkc_vendor,input_serial_number = serial_number_value,site_store_fk = store_data,Status=1,circle =circle_data,
                                                Material_Offer_Submit = 1,Material_Offer_Submit_Submit_At = datetime.datetime.now())
        data_store.save()
        
        total_qty = boq_data.balance_qty
        
        data_store.balance_quantity = float(total_qty)-float(quantity)
        data_store.save()
        
        boq_data.balance_qty = float(total_qty)-float(quantity)
        boq_data.save()
        updated_store_data = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data,Material_Offer_Submit_Approved_Status__in = (1,0))
        return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"wo_id":wo_id,"updated_store_data":updated_store_data,"vendor_id":vendor_id})


def delete_material_offer_store(request,wo_id,itemcode,id,vendor_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    boq_data = tkc_wo_items_boq.objects.get(item_code = itemcode,wo = wo_id)
    sitestore_data = SiteStore_Master.objects.filter(supplier = con)
    updated_store_data = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data)
    data_exist = offer_material_site_stores.objects.get(id = id)
    data_exist.delete()
    return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id})


def upload_wo_material_serial_no_excel(request,wo_id,itemcode,id,vendor_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    boq_data = tkc_wo_items_boq.objects.get(item_code = itemcode,wo = wo_id)
    sitestore_data = SiteStore_Master.objects.filter(supplier = con)
    updated_store_data = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data,Material_Offer_Submit_Approved_Status__in = (1,0))
    offer_data = offer_material_site_stores.objects.get(id = id)
    input_excel_type = request.POST.get('excel_type')
    if input_excel_type == 'serial_nos':
        serial_excel = request.FILES['sitestore_excel']
        data2 = pd.read_excel(serial_excel)
        for column in data2:
            no_list = data2[column].values
            item_no_list = list(no_list)
        print("list_of_item_codes",item_no_list)

        if int(offer_data.quantity) != len(item_no_list):
            return render(request,'wo/serial_excels_upload_option.html',{"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id,"offer_data":offer_data,"msg1":"Count of serial number should be equal to offer quantity"})
        
            
            
        if len(item_no_list) != len(set(item_no_list)):
            return render(request,'wo/serial_excels_upload_option.html',{"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id,"offer_data":offer_data,"msg1":"You cannot enter same serial number in excel"})
        
        
        for i in item_no_list:
            store_data = offer_material_serial_number(offer = offer_data,wo =wo_data,wo_material =boq_data,site_store =offer_data.site_store,serial_no = i ,created_at = datetime.datetime.now(),offer_no = offer_data.offer_no)
            store_data.save()
        offer_data.is_serial_excel_uploaded = True
        offer_data.excel_type = True
        offer_data.save()

        return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id,"msg1":"Excel uploaded Successfully"})
    
    elif input_excel_type == 'batch_nos':
        serial_excel = request.FILES['sitestore_excel']
        df = pd.read_excel(serial_excel).dropna()
        batch_list = df['batch_no/lot_no/drum_no'].tolist()
        batch_list.pop()
        qty_list = df['total_quantity'].tolist()
        excel_qty_sum = qty_list.pop()
        zipped_list = zip(batch_list,qty_list)
        decimal_format_value = "{:.3f}".format(excel_qty_sum)

        if float(offer_data.quantity) != float(decimal_format_value):
            return render(request,'wo/serial_excels_upload_option.html',{"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id,"offer_data":offer_data,"msg1":"Offered quantity is not equal to batch/lot/drum mentioned quantities"})

        for i,j in zipped_list:
            store_data = offer_material_serial_number(offer = offer_data,wo =wo_data,wo_material =boq_data,site_store =offer_data.site_store,created_at = datetime.datetime.now(),offer_no = offer_data.offer_no,batch_no = i, batch_qty = j)
            store_data.save()
        offer_data.is_serial_excel_uploaded = True
        offer_data.excel_type = False
        offer_data.save()

        return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id,"msg1":"Excel uploaded Successfully"})



def upload_excel_options(request,wo_id,itemcode,id,vendor_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    boq_data = tkc_wo_items_boq.objects.get(item_code = itemcode,wo = wo_id)
    sitestore_data = SiteStore_Master.objects.filter(supplier = con)
    updated_store_data = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data,Material_Offer_Submit_Approved_Status__in = (1,0))
    offer_data = offer_material_site_stores.objects.get(id = id)
    return render(request,'wo/serial_excels_upload_option.html',{"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id,"offer_data":offer_data})


import pandas as pd
import os
def download_batch_demo_excel(request):
    excel_path = os.path.abspath('media/batch_demo_excel.xlsx')
    # file_path = excel_path+"\\media\\demo_excel.xlsx"
    df = pd.read_excel(excel_path)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Material_batch_lot_no.xlsx"'
    df.to_excel(response, index = False)
    return response    




import ast
def offer_material(request,wo_id,vendor_id):
    req_testlist = request.POST.get('req_testlist')
    testlist = ast.literal_eval(req_testlist)
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    vendor_data = User_Registration.objects.get(User_Id = vendor_id)
    all_approved_vendor_material = TKCVendor.objects.filter(TKCWoInfo__supplier=con,TKCWoInfo =wo_id ,Vendor = vendor_data, TKCVendor_Approved_Status=1, Status=1)
    wo_data = TKCWoInfo.objects.get(id = wo_id)
    wo_discom = wo_data.Discom.Discom_Code
    wo_number = wo_data.Contract_Number
    wo_date = wo_data.Contract_Date
    random_no  = random.randint(1001,999999)
    string = str(wo_number)+'-'+str(wo_date)+'-'+ str(random_no)
    offer_num = string.replace("/", "-" )
    if offer_material_site_stores.objects.filter(offer_no = offer_num).exists():
        random_no  = random.randint(999999,999999999)
        string = str(wo_number)+'-'+str(wo_date)+'-'+ str(random_no)
        offer_num = string.replace("/", "-" )   

    if len(testlist) == 0:
        return render(request, 'wo/wo_approved_vendor_material.html', {"con": con, 'all_approved_vendor_material': all_approved_vendor_material,"wo_id":wo_id,"vendor_id":vendor_id,"msg1":"No material available for offer","wo_discom":wo_discom})


    try:
        offer_file = request.FILES['offer_material_file']
        req_readiness_date = request.POST.get('readiness_date')
        inspection_factory_address = request.POST.get('vendor_factory_address')
        
        for i in testlist:
            data_update = offer_material_site_stores.objects.get(id = i)
            serial_item_data =  offer_material_serial_number.objects.filter(offer = data_update)
            for j in serial_item_data:
                j.offer_no = offer_num
                j.save()
            data_update.offer_material_docs = offer_file
            data_update.is_offered = True
            data_update.offer_no = offer_num
            data_update.readiness_date = req_readiness_date
            data_update.vendor_factory_address = inspection_factory_address
            data_update.save()
    except:
        for i in testlist:
            data_update = offer_material_site_stores.objects.get(id = i)
            serial_item_data =  offer_material_serial_number.objects.filter(offer = data_update)
            for j in serial_item_data:
                j.offer_no = offer_num
                j.save()
            data_update.is_offered = True
            data_update.offer_no = offer_num
            data_update.save()
            
       
    return render(request, 'wo/wo_approved_vendor_material.html', {"con": con, 'all_approved_vendor_material': all_approved_vendor_material,"wo_id":wo_id,"vendor_id":vendor_id,"msg1":"Material Offered Successfully","wo_discom":wo_discom})

    

def Discrepancies_found_in_Survey(request,wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = TKCWoInfo.objects.get(id=wo_id)
    if request.method == "POST":
        Discrepancies_found_in_Survey_file = request.FILES['Discrepancies_found_in_Survey']
        data.discrepancies_found_in_Survey_docs = Discrepancies_found_in_Survey_file
        data.save()
        messages.add_message(request, messages.INFO, 'Discrepancies found in Survey Submitted')
        wo = TKCWoInfo.objects.filter(supplier=con, Status=1, Wo_Digital_Upload_Status=1)
        return render(request, 'wo/Discrepancies_found_in_Survey.html', {"wo": wo, 'data': data, 'con': con})
    return render(request, 'wo/Discrepancies_found_in_Survey.html', {"data": data, 'con': con})


def tkc_wo_offred_material_data(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_data = TKCWoInfo.objects.filter(supplier=con,Wo_Approved_Status = 1,Wo_Digital_Upload_Status =1)
    return render (request,'wo/tkc_wo_offered_materials_data.html',{"wo_data":wo_data})
    
    
    
def tkc_offered_materials(request,wo_id):
    wo_obj = TKCWoInfo.objects.get(id=wo_id)
    offer_data = offer_material_site_stores.objects.filter(wo = wo_obj, offer_no__isnull = False)
    return render (request,'wo/tkc_offered_material.html',{"offer_data":offer_data})
    
    
def remove_added_offer_material(request,wo_id,itemcode,vendor_id,offer_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_data = TKCWoInfo.objects.get(id = wo_id) 
    sitestore_data = SiteStore_Master.objects.filter(supplier = con)
    # vendor = User_Registration.objects.get(User_Id =vendor_id )
    # wo_discom = wo_data.Discom.Discom_Code
    offer_data = offer_material_site_stores.objects.get(id = offer_id)
    if offer_data.is_serial_excel_uploaded == True:
        serail_no_data = offer_material_serial_number.objects.filter(offer = offer_data)
        serail_no_data.delete()     
    old_boq_data = tkc_wo_items_boq.objects.get(id = offer_data.wo_material.id)
    old_balance_qty = old_boq_data.balance_qty
    old_boq_data.balance_qty = old_balance_qty + offer_data.quantity
    old_boq_data.save()
    offer_data.delete()
    boq_data = tkc_wo_items_boq.objects.get(item_code = itemcode,wo = wo_id)
    updated_store_data = offer_material_site_stores.objects.filter(wo = wo_data,wo_material = boq_data,Material_Offer_Submit_Approved_Status__in = (1,0))
    return render(request, 'wo/wo_material_offer_step1.html', {"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"wo_id":wo_id,"updated_store_data":updated_store_data,"vendor_id":vendor_id})

    
    
    


def viewsitestore(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    all_store = SiteStore_Master.objects.filter(supplier = con)
    return render (request,'wo/view_site_store.html',{'all_store':all_store})

def tag_sitestore_circle(request,store_id):
    discom_data = Discom_Master.objects.all()
    store_data = SiteStore_Master.objects.get(id = store_id)
    return render (request,'wo/tag_sitestore_circle.html',{'discom_data':discom_data,'store_data':store_data})


def save_sitestore_circle(request,store_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    all_store = SiteStore_Master.objects.filter(supplier = con)
    store_data = SiteStore_Master.objects.get(id = store_id)
    circle_list = request.POST.getlist('Circle_Name')
    for i in circle_list:
        circle_obj = Circle_Master.objects.get(id = i)
        data = sitestore_circle(tkc_sitestore = store_data, circle = circle_obj, circle_name =circle_obj. Circle_Name_E)
        data.save()
    return render (request,'wo/view_site_store.html',{'all_store':all_store,'msg1':"Circle tagged successfully"})


def sitestore_circles(request,store_id):
    store = SiteStore_Master.objects.get(id=store_id)
    all_record = sitestore_circle.objects.filter(tkc_sitestore=store).values()    
    data=list(all_record)   
    return JsonResponse({"data": data})


    


# multiple material offer of  wo from tkc side code end


# ************************************************** BOQ Code **************************************************************

def verify_boq_list(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])    
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1, supplier=con).order_by('-id')
    return render(request, 'wo/verify_boq.html', {'con': con, "wo" : wo})

import itertools
def verify_boq(request, wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])    
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id) 
    wo = TKCWoInfo.objects.get(id=wo_id)   
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id).values()    
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id)
    
    
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1.circle_name)    
    
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
                item_qty_list.append(j.verified_circle_qty)        
            items_qty[i.item_code]=item_qty_list       
   
    if len(stored_data) != 0 :    
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
        items_qty = 0   
        
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id)
    print(gm_status_data)   
    for i in gm_status_data:
        gm_status = i.gm_status        
    
    material = Vendor_Material_Master.objects.all()    
    item_code = Vendor_Material_Specification_Master.objects.all()    
    material_lst = []
    for i in material:
        material_lst.append(i.Material_Name)
        
    item_lst = []
    for j in item_code:
        item_lst.append(j.Material_Item_Code)
        
    data = {}    
    for j,k in zip(material_lst,item_lst):
        data[j]= k     
    
    return render(request, 'wo/verify_boq_info.html', {'con': con, 'data':data, 'requested_data':requested_data, 'gm_status':gm_status, 'circle_list':circle_list, "items_qty":items_qty, "item_dict":item_dict, "circles": circles, "wo" : wo, "wo_instance":wo_instance, "boq_data" : boq_data})


import itertools
@csrf_exempt
def save_verified_boq_data(request,wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])      
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id)    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)    
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id) 

    circle_list= request.POST.getlist("circle_name")
    item_qty_list=[]
    for i in boq_data:   
        item_name = i.item_code
        qty = request.POST.getlist(item_name)        
        item_qty_list.append(qty)
        for req in item_qty_list:        
            for j,k in zip(req,circle_list):
                if j in validators.EMPTY_VALUES:
                    m = None
                else:
                    m = float(j)
                data = tkc_update_boq.objects.get(wo=wo, item_code= item_name, circles_name= k, updated_at=datetime.datetime.now(), created_at=datetime.datetime.now())    
                data.verified_circle_qty = m      
                data.save()
    
    items_qty = {}
    for req in boq_data:
        item_name = req.item_code
        circle_boq_data = request.POST.getlist(item_name)  
        items_qty[item_name] = circle_boq_data    
     
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)   
    
    if len(stored_data) != 0 :    
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
        items_qty = 0
        
    material = Vendor_Material_Master.objects.all()
    item_code = Vendor_Material_Specification_Master.objects.all()
    material_lst = []
    for i in material:
        material_lst.append(i.Material_Name)
        
    item_lst = []
    for j in item_code:
        item_lst.append(j.Material_Item_Code)
        
    data = {}    
    for j,k in zip(material_lst,item_lst):
        data[j]= k
        
    # wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1, supplier=con).order_by('-id')
    return render(request, 'wo/verify_boq_info.html', {'con': con, 'data':data, "items_qty":items_qty, "item_dict":item_dict, "circles": circles, "wo" : wo, "wo_instance":wo_instance, "boq_data" : boq_data})
 

@csrf_exempt
def save_boq_data(request, wo_id):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type']) 
    wo = TKCWoInfo.objects.get(id=wo_id) 
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id) 
    material_name = request.POST.get("material_name")
    item_code = request.POST.get("item_code")
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)    
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id)
    
    wo = TKCWoInfo.objects.get(id=wo_id) 
    
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1) 
       
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)
   
    if len(stored_data) != 0:        
        item_code_list = []
        item_dict = {} 
        items_qty = {}       
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []
            verified_item_qty_list = []
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j)            
            for k in stored_item_data:                
                if k.circle_quantity == None:
                    k.circle_quantity = ''
                item_qty_list.append(k.circle_quantity)
                verified_item_qty_list.append(k.verified_circle_qty)
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list 
            items_qty[j]=verified_item_qty_list
            
    else:
        item_dict = 0
        circle_list = 0 
   
        
    material = Vendor_Material_Master.objects.all()
    item_code = Vendor_Material_Specification_Master.objects.all()
    material_lst = []
    for i in material:
        material_lst.append(i.Material_Name)
        
    item_lst = []
    for j in item_code:
        item_lst.append(j.Material_Item_Code)
        
    data = {}    
    for j,k in zip(material_lst,item_lst):
        data[j]= k
        
    
    item_name = request.POST.get("item_name")    
    split_variable=item_name.split('|')       
    
    item_name = split_variable[0]
    material_name = split_variable[1]
    circle_name = request.POST.get("circle_name")
    circle_qty = request.POST.get("circle_qty")
    if circle_qty in validators.EMPTY_VALUES:
        circle_qty = None
    else:
        circle_qty = float(circle_qty)
    req_data = tkc_requested_boq_item(wo=wo, circle_qty=circle_qty, material_name=material_name, item_code=item_name, circles_name=circle_name, updated_at=datetime.datetime.now(), created_at=datetime.datetime.now())
    req_data.save()           
    exist_data = tkc_requested_boq_item.objects.filter(wo = wo_id)
    
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id)
        
    for i in gm_status_data:
        gm_status = i.gm_status      
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1, supplier=con).order_by('-id')
        
    return render(request, 'wo/verify_boq.html', {'con':con, 'data':data, 'gm_status':gm_status, 'requested_data':requested_data, 'circle_list':circle_list, 'items_qty': items_qty, 'wo':wo, 'data':exist_data, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})

@csrf_exempt
def verify_boq_edit(request,wo_id): 
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type']) 
    wo = TKCWoInfo.objects.get(id=wo_id) 
    wo_instance = TKCWoInfo.objects.get(id=wo_id)      
    circles = Tag_Circle.objects.filter(wo_no=wo_id) 
    material_name = request.POST.get("material_name")
    item_code = request.POST.get("item_code")    
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)    
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id) 
    update_boq_data = tkc_update_boq.objects.filter(wo=wo_id).values()
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1) 
    circle_list= request.POST.getlist("circle_name")
    item_qty_list=[]
    for i in boq_data:   
        item_name = i.item_code
        qty = request.POST.getlist(item_name)
        item_qty_list.append(qty)
        for req in item_qty_list:        
            for j,k in zip(req,circle_list):
                if j in validators.EMPTY_VALUES:
                    m = None
                else:
                    m = float(j)
                data = tkc_update_boq.objects.get(wo=wo, item_code= item_name, circles_name= k)    
                data.verified_circle_qty = m       
                data.save()
                wo.is_verified_boq_added =2
                wo.save()
                
    items_qty = {}
    for req in boq_data:
        item_name = req.item_code
        circle_boq_data = request.POST.getlist(item_name)  
        items_qty[item_name] = circle_boq_data
    
     
    stored_data = tkc_update_boq.objects.filter(wo=wo_id)    
    if len(stored_data) != 0 :    
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
        items_qty = 0
        
    
    zip_dict = zip(item_dict, items_qty)
    print(zip_dict)  
    
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id)
        
    for i in gm_status_data:
        gm_status = i.gm_status  
    
    
    material = Vendor_Material_Master.objects.all()
    item_code = Vendor_Material_Specification_Master.objects.all()
    material_lst = []
    for i in material:
        material_lst.append(i.Material_Name)
        
    item_lst = []
    for j in item_code:
        item_lst.append(j.Material_Item_Code)
        
    data = {}    
    for j,k in zip(material_lst,item_lst):
        data[j]= k        
    
    wo = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1, supplier=con).order_by('-id')
    return render(request,'wo/verify_boq.html', {'con':con, 'data':data, 'gm_status':gm_status, 'circle_list':circle_list, 'update_boq_data':update_boq_data, 'zip_dict':zip_dict, 'wo':wo, "items_qty":items_qty, "item_dict":item_dict, "circles": circles, "wo_instance":wo_instance, "boq_data" : boq_data})


@csrf_exempt
def save_boq_info(request,wo_id, identifier):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type']) 
    wo_instance = TKCWoInfo.objects.get(id=wo_id)     
    circles = Tag_Circle.objects.filter(wo_no=wo_id)
    boq_data = tkc_wo_items_boq.objects.filter(wo=wo_id)
    wo = TKCWoInfo.objects.get(id=wo_id) 
    requested_data = tkc_requested_boq_item.objects.filter(wo=wo_id)
    print("circles", circles) 
    circle_list = []  
    for circle1 in circles:  
        circle_list.append(circle1)
    print("circle_list", circle_list)
    if identifier == 1:
        if tkc_update_boq.objects.filter(wo=wo_id).exists():
            exist_data = tkc_update_boq.objects.filter(wo=wo_id)
            for jj in exist_data:
                jj.verified_circle_qty = 0
                jj.save()
                
    else:
        pass      

    item_qty_list=[]
    for i in boq_data:   
        item_name = i.item_code
        qty = request.POST.getlist(item_name)
        item_qty_list.append(qty)
        for req in item_qty_list:        
            for j,k in zip(req,circle_list):
                if j in validators.EMPTY_VALUES:
                    m = None
                else:
                    m = float(j)
                data = tkc_update_boq.objects.get(wo=wo, item_code= item_name, circles_name= k.circle_name)    
                data.verified_circle_qty = m       
                data.save()
                wo.is_verified_boq_added  = 5
                wo.save()
    
    gm_status_data = tkc_update_boq.objects.filter(wo=wo_id)
        
    for i in gm_status_data:
        gm_status = i.gm_status   
     
    stored_data = tkc_update_boq.objects.filter(wo=wo_id) 
       
    if len(stored_data) != 0:        
        item_code_list = []
        item_dict = {} 
        items_qty = {}       
        for i in stored_data:
            item_code_list.append(i.item_code)
        new_item_code_list = set(item_code_list)
        for j in new_item_code_list:
            circle_list = []
            item_qty_list = []            
            verified_item_qty_list = []           
            stored_item_data = tkc_update_boq.objects.filter(wo=wo_id, item_code=j).order_by('id')            

            for k in stored_item_data:                              
                if k.verified_circle_qty == None:
                    k.verified_circle_qty = ''
                item_qty_list.append(k.circle_quantity)                
                verified_item_qty_list.append(k.verified_circle_qty)
                circle_list.append(k.circles_name)
            item_dict[j]=item_qty_list 
            items_qty[j]=verified_item_qty_list
    else:
        item_dict = 0
        circle_list = 0  
        
    print(":::::::::::::::",items_qty)
       
    material = Vendor_Material_Master.objects.all()
    item_code = Vendor_Material_Specification_Master.objects.all()
    material_lst = []
    for i in material:
        material_lst.append(i.Material_Name)
        
    item_lst = []
    for j in item_code:
        item_lst.append(j.Material_Item_Code)
        
    data = {}    
    for j,k in zip(material_lst,item_lst):
        data[j]= k        
    
    wo_data = TKCWoInfo.objects.filter(Status=1, Wo_Send_To_Approval_Status=1, Wo_Digital_Upload_Status=1, supplier=con).order_by('-id')
    if wo.is_verified_boq_added  == 5:
        wo.is_verified_boq_added = 1
        wo.save()        
        
        return render(request, 'wo/verify_boq.html',{"wo":wo_data})
        
    else:                
        return render(request, 'wo/verify_boq_info.html',  
                    {'con':con, 'wo': wo, 'gm_status':gm_status, 'data':data, 'requested_data':requested_data, 'items_qty':items_qty, "item_dict": item_dict, "boq_data": boq_data, "circles":circles, "wo_instance":wo_instance,"circle_list":circle_list})


# ************************************************** BOQ Code **************************************************************




# --------------------shubham tripathi fqp intimation inspection code start from here---------------
def tkc_circle_list(request):
    region_id = request.GET.get('region_id')
    circle_data = list(Circle_Master.objects.filter(Region_id=region_id).values('id','Circle_Name_E','Circle_Code','Region'))
    return JsonResponse({"circle_Data":circle_data})
# return render(request, 'fqpintimation/tkc_fqpintimate_create.html', {'cm_data':cm_data})


def tkc_division_list(request):
    circle_id = request.GET.get('circle_id')
    division_data = list(Division_Master.objects.filter(Circle_id=circle_id).values('id','Division_Name_E','Division_Code','Circle'))
    return JsonResponse({"division_data":division_data})


def tkc_sub_division_list(request):
    division_id = request.GET.get('division_id')
    subdivision_data = list(Sub_Division_Master.objects.filter(Division_id=division_id).values('id','Sub_Division_Name_E','Sub_Division_Code','Division'))
    return JsonResponse({"subdivision_data":subdivision_data})

def tkc_division_circle_list(request):
    Division_id = request.GET.get('division_id')
    circle_division_data = list(DC_Master.objects.filter(Sub_Division__Division_id=Division_id).values('id','DC_Name_E','DC_Code','Sub_Division'))
    return JsonResponse({"circle_division_data":circle_division_data})





def tkc_fqpintimation(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC":
            wo_data = TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id)
            return render(request, 'fqpintimation/wo_intimation.html', {'supplier': supplier,'wo_data':wo_data})
        else:
            return render(request, 'tkc/creater_base.html', {'supplier': supplier})
    else:
        return render(request, 'tkc/creater_base.html', { 'supplier': supplier})


def tkc_fqpintimation_list(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_id=request.GET.get('woid')
    if supplier.cgm_approval:
        wo_fqpi_data=FqpIntimation.objects.filter(~Q(status=-1),wo_id=wo_id)
        wo_data=TKCWoInfo.objects.filter(id=wo_id)
        return render(request, 'fqpintimation/tkc_intimation_list.html', {'supplier': supplier,'wo_fqpi_data':wo_fqpi_data,'wo_data':wo_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'supplier': supplier})        

    
def tkc_fqpintimation_create(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        if request.method == "POST":
            wo_id = request.POST.get('woid')
            region_id=request.POST.get('region_id')
            circle_id=request.POST.get('circle_id')
            division_id=request.POST.get('division_id')
            work_execution_detail=request.POST.get('work_execution_detail')
            brief_description_of_work=request.POST.get('brief_description_of_work')
            tentative_date_of_execution=request.POST.get('tentative_date_of_execution')
            intimation_remark=request.POST.get('intimation_remark')
            work_execution_milestone_pdf=request.FILES['work_execution_milestone_pdf']
            layout_sld_of_work_execution=request.FILES['layout_sld_of_work_execution']
            estimate_data = FqpIntimation(wo_id=wo_id,region_id=region_id,circle_id=circle_id,division_id=division_id,work_execution_detail=work_execution_detail,brief_description_of_work=brief_description_of_work,work_execution_milestone_pdf=work_execution_milestone_pdf,layout_sld_of_work_execution=layout_sld_of_work_execution,tentative_date_of_execution=tentative_date_of_execution,remark=intimation_remark).save()
            return redirect('tkc_fqpintimation')
        else:
            wo_id = request.GET.get('woid')
            wo_data=TKCWoInfo.objects.filter(id=wo_id)
            rm_data=Region_Master.objects.all()
            cm_data=Circle_Master.objects.all()
            dm_data=Division_Master.objects.all()
            return render(request, 'fqpintimation/tkc_fqpintimate_create.html', {'supplier': supplier,'wo_data':wo_data,'rm_data':rm_data,'cm_data':cm_data,'dm_data':dm_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"supplier": supplier,})

def tkc_fqpintimation_observation_detail(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        fqpintimation_id = request.GET.get('fqpintimation_id')
        int_data=FqpIntimation.objects.filter(id=fqpintimation_id)
        observation_data=FqpIntimation_Observation_Info.objects.filter(fqpintimation_id=fqpintimation_id)
        officer_data=FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id)
        close_inti=FqpIntimation_Observation_Close.objects.filter(fqpintimation_id=fqpintimation_id)
        return render(request, 'fqpintimation/tkc_fqpintimation_observation_detail.html', {'supplier': supplier,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation_data':observation_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"supplier": supplier,})

# ------------------------fqp intimation end here----------------------------------------


#--------------------start of consumer bid functions by ravindra and gaurav-----------------------------#

#POST API FOR TKC_CONSUMER TABLE
# class TKC_ConsumerCreateAPIView(APIView):
#     def post(self, request, format=None):
#         serializer = ConsumerSerializer_1(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def consumer_estimation():    
    url = f'https://dsp.mpcz.in:8888/deposit_scheme/api/consumer/getAllConsumerDetail'
    response = requests.get(url, verify = False, headers = {"User-Agent":'Chrome'}).json()
    
    if response:
        for res in response:
            if TKC_Consumer.objects.filter(consumerApplicationNo = res['CONSUMER_APPLICATION_NUMBER']).exists():pass
            else:
                bid_expiry = datetime.datetime.now() + datetime.timedelta(hours = 72)
                
                con = TKC_Consumer(
                estimate_name = res['ESTIMATE_NAME'],
                kwload= res['KWLOAD'],
                consumer_mobile_no = res['CONSUMER_MOBILE_NO'],
                sgst = res['SGST'],
                consumerApplicationNo = res['CONSUMER_APPLICATION_NUMBER'],
                consumerName = res['CONSUMER_NAME'],
                consumer_email_id = res['CONSUMER_EMAIL_ID'],
                cgst = res['CGST'],
                bid_created = res['ESTIMATE_DATE'],
                approved_by = res['APPROVED_BY'],
                to_char = res["TO_CHAR(SYSDATE,'DD-MON-YYYYHH:MM')"],
                address = res['ADDRESS'],
                schema = res['SCHEMA'],
                kvaload = res['KVALOAD'],
                deposit_amount = res['DEPOSIT_AMOUNT'],
                shortDescriptionOfWork = res['SHORT_DESCRIPTION_OF_WORK'],
                erp_no = res['ERP_NO'],
                supervision_amount = res['SUPERVISION_AMOUNT'],
                bid_expiry=bid_expiry
                )
                con.save()
    else:pass

def place_bid_data(request):
    contractor = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if contractor.Authentication_id is not None and  contractor.Oyt != "9":
        response = TKC_Consumer.objects.all().order_by('-id')
        currenTime = datetime.datetime.now()
        return render(request,'tkc/consumer_estimation.html',{'response':response,'currenTime':currenTime})
     
    else:
        return HttpResponse("You are not eligible for this Bid!!! ") 
    

#  ----ravindra code---------------
# # #scheduler for fun consumer_estimation
def run_continuously(interval=1):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                t.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run
schedule.every(10).seconds.do(consumer_estimation)
stop_run_continuously = run_continuously()
t.sleep(1)        

    
# def contractor_details(request,id):
#     consumer_det = TKC_Consumer.objects.get(consumerApplicationNo = id)
#     data = User_Registration.objects.get(Otp = request.session['otp'], User_type = request.session['User_type'])
#     user_oyt = data.Oyt
#     tkc_payment = TKC_Payment.objects.get(id = user_oyt)
#     user_det = User_Registration.objects.filter(ContactNo = data.ContactNo)[0]   
#     if request.method == "POST":
#          if TKC_Consumer_bid.objects.filter(User_Id = user_det).filter(consumers = consumer_det).exists():pass
#          else:
#             bid_amount = request.POST.get('bid_amount')
    
#             bid = TKC_Consumer_bid(
#                 consumers = consumer_det,
#                 User_Id = user_det,
#                 bid_amount = bid_amount,
#                 contractor_category = tkc_payment.Name        
#             )
#             bid.save()
#             consumer_det.is_bid_submitted = True
#             consumer_det.save()
#     return render(request,'tkc/contractor_details.html',{'i':consumer_det})

def contractor_details(request, id):
    try:
        consumer_det = get_object_or_404(TKC_Consumer, consumerApplicationNo=id)
        data = User_Registration.objects.get(Otp=request.session['otp'], User_type=request.session['User_type'])
        user_oyt = data.Oyt
        tkc_payment = TKC_Payment.objects.get(id=user_oyt)
        user_det = User_Registration.objects.filter(ContactNo=data.ContactNo)[0]

        if request.method == "POST":
            if TKC_Consumer_bid.objects.filter(User_Id=user_det, consumers=consumer_det).exists():
                pass
            else:
                bid_amount = request.POST.get('bid_amount')

                bid = TKC_Consumer_bid(
                    consumers=consumer_det,
                    User_Id=user_det,
                    bid_amount=bid_amount,
                    contractor_category=tkc_payment.Name
                )
               
                bid.save()
                consumer_det.is_bid_submitted = True
                consumer_det.save()

                messages.success(request, 'You have successfully submitted a bid.To see your bid amount go back to contractor details and click on contractor bid details')

    except User_Registration.DoesNotExist:
        raise Http404("User not found")

    except (TKC_Consumer.DoesNotExist, TKC_Payment.DoesNotExist):
        raise Http404("Consumer or payment details not found")

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        
    return render(request, 'tkc/contractor_details.html', {'i': consumer_det})

def Contractor_selectionview2(request,uid):
    response = TKC_ContractorSelections.objects.filter(User_Id = uid)
    contractor_address = UserCompanyDataMain.objects.filter(User_Id = uid)
    return render(request, 'tkc/contractor_selection.html',{'response': response,'ca':contractor_address})

def contractor_status(request):
    con = User_Registration.objects.get(Otp = request.session['otp'],User_type = request.session['User_type'])
    user_id = con.User_Id
    response = TKC_ContractorSelections.objects.filter(User_Id = user_id)
    return render(request, 'tkc/contractor_selection.html',{'response': response})

def contractor_bid_details(request):
    contractors = User_Registration.objects.get(Otp = request.session['otp'], User_type = request.session['User_type'])
    user_id = contractors.User_Id
    consumer_bid = TKC_Consumer_bid.objects.filter(User_Id = user_id)
    active_contractors = User_Registration.objects.filter(User_type = "TKC", cgm_approval = 1, blacklisted = 0, Authentication_id__isnull = False)
    
    lst = []
    for con in consumer_bid:
        lst.append(con.User_Id)
        
    bid_exist = lst.copy() 
     
    bid_data = []     
    for i in active_contractors:
        if i not in lst:
            bid_data.append(i)
            
    lst.extend(bid_data)
    
    return render(request, 'tkc/show_contractor.html',{'contractors':active_contractors,'con_bid':consumer_bid,'extend_data':lst,'bid_exist':bid_exist})

def contractor_display(request):
    consumerBid = TKC_Consumer_bid.objects.all().order_by('bid_amount')
    return render(request,'tkc/contractor_display.html',{'consumerBid':consumerBid}) 

class ConsumerbidView(APIView):
    try:
        def get(self, request):
            queryset = TKC_Consumer_bid.objects.all().order_by('bid_amount')
            
            nuser = []
            for i in queryset:
                nuser.append(i.User_Id)
            # data = User_Registration.objects.filter(~Q(CompanyName_E__in = nuser), User_type = "TKC", cgm_approval = 1, blacklisted = 0, Authentication_id__isnull = False, Basic_Details=1, Complete_Details=1, deregister=1)
            data = User_Registration.objects.filter(
                            Q(~Q(CompanyName_E__in=nuser))|
                            Q(User_type="TKC") |
                            Q(cgm_approval=1) |
                            Q(blacklisted=0) |
                            Q(Authentication_id__isnull=False) |
                            Q(Basic_Details=1) |
                            Q(Complete_Details=1) |
                            Q(deregister=0)
                        )
            list_value = []
            
            for val in data:
                list_value.append(val.User_Id)
            data_2 = TKC_Document.objects.filter(Types_of_Docs = "Electrical License", user_id__in = list_value,
                                                    Doc_expiry_date__gte=date.today(), new_data = 0)
            list_value_2 = []
            for j in data_2:
                list_value_2.append(j.user_id)
            val_3 = UserCompanyDataMain.objects.filter(user_id_id_id__in = list_value_2)
            
            serializer = Consumer_bidSerializer(queryset, many = True)
            not_participated_contractors = UserCompanyDataMainSerializer(val_3, many = True)
            
            return Response({
                'status' : True,
                'message' : 'Applicant & Contractor fetched with GET',
                'participated_contractors': serializer.data,
                'not_participated_contractors': not_participated_contractors.data,
               
            })
            
    except Exception as e:
        print(e)
        
def all_contractors(request):
            contractors = User_Registration.objects.get(Otp = request.session['otp'], User_type = request.session['User_type'])
            user_id = contractors.User_Id
            queryset = TKC_Consumer_bid.objects.filter(User_Id = user_id)     
            
            nuser = []
            for i in queryset:
                nuser.append(i.User_Id)
            # data = User_Registration.objects.filter(~Q(CompanyName_E__in = nuser), User_type = "TKC", cgm_approval = 1, blacklisted = 0, Authentication_id__isnull = False)
            data = User_Registration.objects.filter(
                            Q(~Q(CompanyName_E__in=nuser))|
                            Q(User_type="TKC") |
                            Q(cgm_approval=1) |
                            Q(blacklisted=0) |
                            Q(Authentication_id__isnull=False) |
                            Q(Basic_Details=1) |
                            Q(Complete_Details=1) |
                            Q(deregister=0) |
                            Q(payment=1)
                        )
            list_value = []
            
            for val in data:
                list_value.append(val.User_Id)
            data_2 = TKC_Document.objects.filter(Types_of_Docs = "Electrical License", user_id__in = list_value,
                                                    Doc_expiry_date__gte=date.today(), new_data = 0)
            list_value_2 = []
            for j in data_2:
                list_value_2.append(j.user_id)
            val_3 = UserCompanyDataMain.objects.filter(user_id_id_id__in = list_value_2)
            
            participated = []
            for k in queryset:
                participated.append(k.User_Id)
                
            bid_exist = participated.copy() 
     
            not_participated = []     
            for j in val_3:
                if j not in participated:
                    not_participated.append(j)
                    
            participated.extend(not_participated)
            
            return render(request, 'tkc/show_contractor_new.html',{'con_bid':queryset, 'active_contractors':val_3, 'both':participated, 'bid_exist':bid_exist})   

def consumer_estimation_offline(request):
    response = TKC_Consumer.objects.all()
    return render(request, 'tkc/consumer_estimation_offline.html',{'response':response})
   
class contractorSelectionView(APIView):
        def post(self, request):
            try:
                consumer_application_no_1 = None 
                consumer_name = None
                task_name = None
                if request.data.get('consumers') is None or  request.data.get('consumers') == '':
                    user_id = request.data['User_Id']
                    consumer_application_no_1 = request.data.get('consumerApplicationNo') 
                    consumer_name = request.data.get('consumerName') 
                    task_name = request.data.get('consumerTask') 
                    
                else:     
                    user_id = request.data['User_Id']
                    consumer_id = request.data.get('consumers')
                    consumer_application_no_1 = TKC_Consumer.objects.get(id=consumer_id).consumerApplicationNo
                user_data_check = TKC_Consumer_bid.objects.filter( User_Id = user_id,consumers__consumerApplicationNo = consumer_application_no_1 )
                    
                if len(user_data_check) != 0:
                    serializer = Contractor_selectionSerializer(data = request.data, many = False)
                    
                    if serializer.is_valid():
                        serializer.save()
                        queryset_1 = TKC_Consumer_bid.objects.filter(User_Id = request.data['User_Id'])
                        contractor_serializer_1 = Consumer_bidSerializer2(queryset_1, many = True)
                
                        userdata = UserCompanyDataMain.objects.filter(user_id_id = user_id)
                        userdata = CompanyDataMainSerializer(userdata, many = True)
                        return Response({
                            'status' : True,
                            'message' : 'Contractor details fetched with POST',
                            'contractor_details': serializer.data,
                            'contractor_address':userdata.data,
                            'contractor_selection_bid_details': contractor_serializer_1.data,
                            })
                    
                    return Response({
                        'status' : False,
                        'data' : serializer.errors,             
                    })
                
                else:
                    
                    user_obj = User_Registration.objects.get(User_Id = user_id)
                    can = TKC_Consumer.objects.get(consumerApplicationNo  = consumer_application_no_1)
                    data_present = TKC_bid_not_participated.objects.filter( User_Id = user_obj,consumer_application_no = can.consumerApplicationNo,consumerName = consumer_name,shortDescriptionOfWork=task_name)
                    if len(data_present) == 0:
                        user_data = TKC_bid_not_participated( User_Id = user_obj, consumer_application_no = can.consumerApplicationNo,
                                                      consumerName = consumer_name,shortDescriptionOfWork = task_name)
                        user_data.save()
                    
                    userdata = UserCompanyDataMain.objects.filter(user_id_id = user_id)
                    userdata = CompanyDataMainSerializer(userdata, many = True)
                    
                    return Response({
                        'status' : True,
                        'message' : 'Contractor details fetched with POST',
                        'contractor_address':userdata.data
                        })

            except Exception as e:
                return Response({
                        'status': False,
                        'message': 'Error occurred: {}'.format(str(e))
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
   
def bid_accept(request,id):
    data = TKC_ContractorSelections.objects.get(consumers__consumerApplicationNo = id)
    data.is_participated = True
    data.save()
    return render(request,"tkc/contractor_work_started.html", {'data':data})

def bid_reject(request,id):
    data = TKC_ContractorSelections.objects.get(id = id)
    data.is_participated = False
    data.save()
    return redirect ('/tkc/contractor_selectiondisplay') 

def view_work(request,id):
    data = TKC_ContractorSelections.objects.get(id = id)
    data.is_participated = True
    data.save()
    return redirect ('/tkc/contractor_work_started')

#for those contractor who do not participated in bid & used in bid_not_participated_user page 
def interested(request, id):
    try:
        data = get_object_or_404(TKC_bid_not_participated, id=id)
        data.is_rejected = False
        data.save()

        applicationno = data.consumer_application_no

        data1 = get_object_or_404(User_Registration, Otp=request.session.get('otp'), User_type=request.session.get('User_type'))
        contractorId = data1.User_Id
        isRejected = data.is_rejected

        URL_POST = "https://dsp.mpcz.in:8888/deposit_scheme/api/consumer/qc-portal/acceptanceOfConsumer"
        data = {
            "consumerApplicationNo": applicationno,
            "rejectionRemark": "None",
            "contractorId": contractorId,
            "isRejected": isRejected
        }

        json_data = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        res = requests.request('POST', url=URL_POST, data=json_data, headers=headers, verify=False)

        if res.status_code == 200:
            return redirect(reverse('requested_bid_data'))  
        else:
            return HttpResponseBadRequest("Failed to process the request. Please try again later.")

    except TKC_bid_not_participated.DoesNotExist:
        return HttpResponseBadRequest("Invalid TKC_bid_not_participated ID.")
    except User_Registration.DoesNotExist:
        return HttpResponseBadRequest("Invalid user data.")
    except Exception as e:
        return HttpResponseBadRequest("Error occurred: {}".format(str(e)))

def not_interested(request, id):
    try:
        data = get_object_or_404(TKC_bid_not_participated, id=id)
        data.is_rejected = True
        data.save()

        applicationno = data.consumer_application_no

        data1 = get_object_or_404(User_Registration, Otp=request.session.get('otp'), User_type=request.session.get('User_type'))
        contractorId = data1.User_Id
        isRejected = data.is_rejected

        URL_POST = "https://dsp.mpcz.in:8888/deposit_scheme/api/consumer/qc-portal/acceptanceOfConsumer"
        data = {
            "consumerApplicationNo": applicationno,
            "rejectionRemark": "None",
            "contractorId": contractorId,
            "isRejected": isRejected
        }
        print("data...............",data)
        json_data = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        res = requests.request('POST', url=URL_POST, data=json_data, headers=headers, verify=False)

        if res.status_code == 200:
            return redirect(reverse('requested_bid_data'))  
        else:
            return HttpResponseBadRequest("Failed to process the request. Please try again later.")

    except TKC_bid_not_participated.DoesNotExist:
        return HttpResponseBadRequest("Invalid TKC_bid_not_participated ID.")
    except User_Registration.DoesNotExist:
        return HttpResponseBadRequest("Invalid user data.")
    except Exception as e:
        return HttpResponseBadRequest("Error occurred: {}".format(str(e)))

#for those contractor who not participated in bid
def requested_bid_data(request):
    con = User_Registration.objects.get(Otp = request.session['otp'], User_type = request.session['User_type'])
    user_id = con.User_Id
    user_data = TKC_bid_not_participated.objects.filter(User_Id = user_id)
    return render(request,'tkc/bid_not_participated_user.html',{"user_data":user_data})

def contractor_work_started(request,CAN):
    try:
        con = get_object_or_404(User_Registration, Otp=request.session.get('otp'), User_type=request.session.get('User_type'))
        # con = User_Registration.objects.get(Otp=request.session['otp'], User_type = request.session['User_type'])
        user_id = con.User_Id
        user_data = TKC_contractor_work.objects.filter(User_Id = user_id)
        # cons = TKC_Consumer.objects.get(consumerApplicationNo = CAN)
        cons = get_object_or_404(TKC_Consumer, consumerApplicationNo=CAN)
        
        can = cons.consumerApplicationNo
        appno = can

        UserId = con.User_Id
        contractorId = UserId
        
        if request.method == "POST" :
            # and request.session.get('csrf') != request.POST['csrfmiddlewaretoken']: 
            upload_digi_doc_material = request.FILES.getlist('d')
            select_vendors = request.POST.getlist('Material')
            material_specification = request.POST.getlist('Specification') 
            transformer_serial_num = request.POST.getlist('serial_no')    
            c_work_started = request.POST.get('start_work')
            m_handover_site = request.POST.get('material_handover')
            m_installation_start = request.POST.get('material_installation') 
            m_installation_finished = request.POST.get('material_installation_finished')
            c_work_completed = request.POST.get('work_completed') 

            t_no = []    
            for x in transformer_serial_num:
                t_no.append(x)
                
            v_name = []
            for k in select_vendors:
                ven1 = User_Registration.objects.get(User_Id = k)
                v_name.append(ven1.CompanyName_E)
                
            z = zip(select_vendors, material_specification)
            vm = []
            vt = []
            l = 0
            
            for i,j in z:
                ven1 = User_Registration.objects.get(User_Id = i)
                t = Vendor_Material_Details.objects.get(id = j)
                vm.append(ven1.CompanyName_E)  
                vt.append(t.Material_Specification) 
                
            for y in upload_digi_doc_material:
                print(y)
                
                tkc_cw = TKC_contractor_work(
                        consumers = cons,
                        User_Id = con,
                        vendor = ven1.CompanyName_E,
                        vendor_material_specification = t.Material_Specification,
                        transformer_serial_no = t_no[l],
                        documents_for_material = y,
                        contractor_work_started = c_work_started,
                        material_handover_site = m_handover_site,
                        material_installation_start = m_installation_start,
                        material_installation_finished = m_installation_finished,
                        contractor_work_completed = c_work_completed,
                    )
                tkc_cw.save()
                # request.session['csrf'] = request.POST['csrfmiddlewaretoken']
                l=l+1
                
                URL_POST="https://dsp.mpcz.in:8888/deposit_scheme/api/user/work-status/save"
                data= {
                    "consumerApplicationNumber": str(cons.consumerApplicationNo),
                    "userId": str(contractorId),
                    "vendorName" : str(v_name),
                    "vendorMaterialSpecification" : str(t.Material_Specification),
                    "transformerSerialNo" : str(transformer_serial_num),
                    "conWorkStartedDate" : str(c_work_started),
                    "materialHandoverSiteDate" : str(m_handover_site),
                    "materialInstallStartDate" : str(m_installation_start),
                    "materialInstallFinishDate" : str(m_installation_finished),
                    "conWorkCompleteDate" : str(c_work_completed)
                }
                json_data=json.dumps(data)
                headers={'Content-type':'application/json'}
                res = requests.request('POST',url=URL_POST,data=json_data,headers=headers,verify=False) 
                return redirect('contractor_work_started', CAN=cons.consumerApplicationNo) 
                
        data = TKC_contractor_work.objects.filter(User_Id = user_id).order_by('-id') 
        return render(request,'tkc/contractor_work_started.html',{"user_data1":user_data,"data":data,"cons":cons,"CAN":CAN,"id":id,"appno":appno})  
    
    except User_Registration.DoesNotExist:
        return HttpResponseBadRequest("Invalid user data.")
    except TKC_Consumer.DoesNotExist:
        return HttpResponseBadRequest("Invalid consumer data.")
    except TKC_contractor_work.DoesNotExist:
        return HttpResponseBadRequest("Invalid contractor work data.")
    except Exception as e:
        return HttpResponseBadRequest("Error occurred: {}".format(str(e)))
         
def update_contractor_work(request,pk):
    upload_digi_doc_material = request.FILES['d'] 
    select_vendors = request.POST.get('Material')
    material_specification = request.POST.get('Specification')
    material_specification_1 = Vendor_Material_Details.objects.get(id = material_specification)
    vendor_company_nm = User_Registration.objects.get(User_Id = select_vendors) 
    dtr1 = request.POST.get('dtr')
    ptr1 = request.POST.get('ptr')
    lt1 = request.POST.get('lt')
    ht1 = request.POST.get('ht_11')
    ht3 = request.POST.get('ht_33')
    ht132 = request.POST.get('ht_132')
    transformer_serial_num = request.POST.get('serial_no') 
    contractor_work_started = request.POST.get('start_work')
    material_handover_site = request.POST.get('material_handover')
    material_installation_start = request.POST.get('material_installation')
    material_installation_finished = request.POST.get('material_installation_finished')
    contractor_work_completed = request.POST.get('work_completed')
    contractor_update = TKC_contractor_work.objects.get(id = pk)
    can = contractor_update.consumers.consumerApplicationNo
    appno = can
    
    if contractor_update:
        contractor_update.vendor = vendor_company_nm.CompanyName_E 
        contractor_update.vendor_material_specification = material_specification_1.Material_Specification
        contractor_update.transformer_serial_no = transformer_serial_num
        contractor_update.documents_for_material = upload_digi_doc_material 
        contractor_update.dtr = dtr1
        contractor_update.ptr = ptr1
        contractor_update.lt = lt1
        contractor_update.ht_11kv = ht1
        contractor_update.ht_33kv = ht3
        contractor_update.ht_132kv = ht132
        contractor_update.contractor_work_started = contractor_work_started 
        contractor_update.material_handover_site = material_handover_site
        contractor_update.material_installation_start = material_installation_start
        contractor_update.material_installation_finished = material_installation_finished
        contractor_update.contractor_work_completed = contractor_work_completed
        c_update = contractor_update.save()
    
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    UserId = con.User_Id
    contractorId = UserId
    user_data = TKC_contractor_work.objects.filter(User_Id = UserId)
        
    URL_POST="https://dsp.mpcz.in/deposit_scheme/api/user/work-status/update/"
    data= {
        "consumerApplicationNumber": str(appno),
        "userId": str(contractorId),
        "vendorName" : str(contractor_update.vendor),
        "vendorMaterialSpecification" : str(contractor_update.vendor_material_specification),
        "transformerSerialNo" : str(contractor_update.transformer_serial_no),
        "dtr" : str(contractor_update.dtr),
        "ptr" : str(contractor_update.ptr),
        "lt1" : str(contractor_update.lt),
        "ht11Kv" : str(contractor_update.ht_11kv),
        "ht33Kv" : str(contractor_update.ht_33kv ),
        "ht132Kv" : str(contractor_update.ht_132kv), 
        "conWorkStartedDate" :  str(contractor_update.contractor_work_started) ,
        "materialHandoverSiteDate" : str(contractor_update.material_handover_site),
        "materialInstallStartDate" : str(contractor_update.material_installation_start),
        "materialInstallFinishDate" :  str(contractor_update.material_installation_finished),
        "conWorkCompleteDate" : str(contractor_update.contractor_work_completed)
    }
    print("-------",data)
    json_data = json.dumps(data)
    headers = {'Content-type':'application/json'}
    res = requests.put(url = URL_POST, data = json_data, headers = headers, verify = False)
    messages.success(request, "Contractor Work Progress Updated Successfully")
    return render(request,'tkc/contractor_work_started.html',{"con_update":c_update,"data":user_data}) 
    
def update_contractor_page(request,pk):
    id = pk
    contractor_detail = TKC_contractor_work.objects.get(id = id)
    v = contractor_detail.vendor
    return render(request,'tkc/update_contractor_work.html',{"contractor_detail" : contractor_detail, "id":id})


#-----------------------------------------END OF FUNCTIONS BY RAVINDRA---------------------------------------#
    
# -------------- shubham tripathi code start from here ---------------
from django.db.models import Sum
# from main.views import *
from django.db.models import Count
curl=settings.CURRENT_URL

def tkc_wo_invoice_list(request): 
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC" and supplier.blacklisted == 0 :
            # po_data = Purchase_Order.objects.annotate(total_invoice_ammount=Sum('purchase_order_data__total_invoice_amount')).filter(~Q(status=-1),vendor__User_Id=supplier.User_Id,po_approved_status=1).order_by('-id')
            
            wo_data = TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,Wo_Approved_Status=1).order_by('-id')
            # print(wo_data,"-------------------------",len(wo_data))
            # pomd = PO_Material.objects.values('po').annotate(total_amount=Sum('total_amount'))
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'tkc_invoice/tkc_wo_invoicelist.html', {'supplier': supplier,'wo_data':wo_data,'wo_amt':wo_amt})
        else:
            return redirect('/tkc/basic')
    else:
        return redirect(curl)

def tkc_invoice_list(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    wo_id=request.GET.get('woid')
    # print("wo_id--------------------------",wo_id)
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC" and supplier.blacklisted == 0 :
            if TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,Wo_Approved_Status=1,id=wo_id).exists():
                in_data=Invoice.objects.filter(~Q(status=-1),work_order_id__supplier__User_Id=supplier.User_Id,work_order_id=wo_id).order_by('-id')
                wo_data = TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,Wo_Approved_Status=1,id=wo_id).last()
                wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
                # woamm = TKCWoInfo_Contract_Price.objects.filter(~Q(status=-1),TKCWoInfo_id=wo_id).aggregate(Sum('total_amount'))
                in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
                return render(request, 'tkc_invoice/tkc_invoicelist.html', {'supplier': supplier,'in_data':in_data,"wo_data":wo_data,'in_amount':in_amount,'wo_amt':wo_amt})
            else:
                wo_data=""
                in_data=""
                return render(request, 'tkc_invoice/tkc_invoicelist.html', {'supplier': supplier,'in_data':in_data,"wo_data":wo_data,})
        else:
            return redirect('/tkc/basic')
    else:
        return redirect(curl)

def tkc_invoice_generate(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC" and supplier.blacklisted == 0:
            if request.method =="POST":
                wo_id=request.POST.get('wo_id')
                bg_pdf=request.FILES['bg_pdf']
                invoice_date=request.POST.get('invoice_date')
                invoicetype=request.POST.get('invoicetype')
                invoice_no=request.POST.get('invoice_no')
                invoice_pdf=request.FILES['invoice_pdf']
                bg_acceptance_letter=request.FILES['bg_acceptance_letter']
                invoice_remark=request.POST.get('invoice_remark')
                supporting_document_name=request.POST.get('supporting_document_name')
                invoice_amount_sgst=request.POST.get('invoice_amount_sgst')
                invoice_amount_cgst=request.POST.get('invoice_amount_cgst')
                invoice_amount_withought_taxes=request.POST.get('invoice_amount_withought_taxes')
                total_invoice_amount=request.POST.get('total_invoice_amount')
                # ct=datetime.now()
                # invoice_no = "Po-" + str(int(ct.timestamp()))
                if supporting_document_name is not None and supporting_document_name != "":
                    try:
                        supporting_document=request.FILES['supporting_document']
                        itd=Invoice(user_id=supplier.User_Id,work_order_id=wo_id,order_type="WorkOrder",invoicetype_id=invoicetype,invoice_number=invoice_no,invoice_amount_sgst=invoice_amount_sgst,invoice_amount_cgst=invoice_amount_cgst,invoice_amount_withought_taxes=invoice_amount_withought_taxes,total_invoice_amount=total_invoice_amount,invoice_pdf=invoice_pdf,bg_document=bg_pdf,bg_acceptance_letter=bg_acceptance_letter,invoice_date=invoice_date,remark=invoice_remark,supporting_document_name=supporting_document_name,supporting_document=supporting_document).save()
                        print("shubtam------")
                    except Exception as e:
                        print("---------pass conditnon----------")
                        pass
                else:
                    itd=Invoice(user_id=supplier.User_Id,work_order_id=wo_id,order_type="WorkOrder",invoicetype_id=invoicetype,invoice_number=invoice_no,invoice_amount_sgst=invoice_amount_sgst,invoice_amount_cgst=invoice_amount_cgst,invoice_amount_withought_taxes=invoice_amount_withought_taxes,total_invoice_amount=total_invoice_amount,invoice_pdf=invoice_pdf,bg_document=bg_pdf,bg_acceptance_letter=bg_acceptance_letter,invoice_date=invoice_date,remark=invoice_remark).save()
                    print("tripahti-----------------")
                return redirect(tkc_wo_invoice_list)
            else:
                wo_id=request.GET.get('woid')
                it_data=InvoiceType.objects.filter(~Q(status=-1))
                wo_data = TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,Wo_Approved_Status=1,id=wo_id).last()
                in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
                wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
                # pomd = PO_Material.objects.filter(~Q(status=-1),wo_id=wo_id).aggregate(Sum('total_amount'))
                return render(request, 'tkc_invoice/create_tkc_invoice.html', {'supplier': supplier,"wo_data":wo_data,"it_data":it_data,"in_amount":in_amount,'wo_amt':wo_amt})
        else:
            return redirect('/tkc/basic')
    else:
        return redirect(curl)



#-----------------------TKC MRC by Gaurav Pathak----------------------------------
#------------------TKC MRC GM Circle---------------------
def tkc_mrc_offer_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    lst = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,circle=officer.Circle).distinct('wo__id')    
    return render(request,'tkc/tkc_create_mrc.html',{'data': lst})


def create_mrcview(request):
    # response = create_mrc.objects.all()
    return render(request, "tkc/tkc_create_mrc.html")
    # ,{"response":response}
    


def format_tk_create(request,id):
    offer = offer_material_site_stores.objects.get(id=id)
    
    ss=tkc_site_store_drr_info.objects.filter(area_store=offer)
    sss=tkc_site_store_drr_info.objects.filter(area_store=offer).last()
    
    
    acc_mat=offer_material_serial_number.objects.filter(offer=offer,result=1).count()
    rej_mat=offer_material_serial_number.objects.filter(offer=offer,result=-1).count()
    
    
    if offer.tkc_mrc_initiate == 1:
        pr = create_mrc.objects.latest("id")
        return render(request,"tkc/tkc_mrc_format_create.html",{'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat,'pr':pr})
    
    if request.method == "POST":
        
        ordr_date = request.POST.get('mrc_order_date')
        remark = request.POST.get('remark')
        
        data = create_mrc(offer=offer, date=ordr_date, remark=remark)
        
        data.save()
        offer.tkc_mrc_initiate=1
        offer.save()
        pr = create_mrc.objects.latest("id")
        return render(request,'tkc/tkc_mrc_format_create.html',{'pr':pr,'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat})
  
    
    return render(request,"tkc/tkc_mrc_format_create.html",{'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat})


def tkc_mrc_sign_list(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    tk_mr=offer_material_site_stores.objects.filter(wo_id=id,accept_from_nabl=1,received_from_nabl=1,circle=officer.Circle).order_by("id")
    cr_mr=create_mrc.objects.all()
    return render(request,'tkc/tkc_mrc_sign_list.html',{"data":tk_mr,"cr_mr":cr_mr})
    

def upload_digi_tkc_mrc(request, id):

    if request.method == "POST":

        upload_digi_doc_tkc = request.FILES['digi_pdf_tkc']

        tr = create_mrc.objects.get(id=id)

        tr. digi_sign = upload_digi_doc_tkc
        tr.digi_signflag = 1

        tr.save()
        tr = create_mrc.objects.get(id=id)
        tr1=offer_material_site_stores.objects.get(id=tr.offer.id)
        print(tr1)
        return render(request, 'tkc/upload_digi_tkc.html', {'tr': tr,'offer': tr1})
        # return render(request, 'tkc/tkc_mrc_sign_list.html',{'tr': tr,'tr1': tr1})
        
       
    tr = create_mrc.objects.get(offer=id)
    tr1=offer_material_site_stores.objects.get(id=tr.offer.id)
    print(tr1)
    return render(request, 'tkc/upload_digi_tkc.html', {'tr': tr,'offer': tr1})
  

#-------------------tkc mrc stc------------------------------  
   
def tkc_mrc_offer_list_stc(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    lst = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,site_store_fk__Division__Circle=officer.Circle).distinct('wo__id')    
    y=[]  
    for i in lst:
        j=i.wo.pakage
        pak=works_master.objects.all()
        for p in pak:
            if (j == p) & ((p.id == 7) or (p.id == 8) or (p.id == 9) or (p.id == 10)):
                y.append(i)
    return render(request,'tkc/tkc_create_mrc_stc.html',{'data': y})


def create_mrcview_stc(request):
    # response = create_mrc.objects.all()
    return render(request, "tkc/tkc_create_mrc_stc.html")
    # ,{"response":response}
    
def tkc_mrc_add_offer_stc(request,id):
    # data = offer_material_site_stores.objects.get(id = id)
    if request.method == "POST":
        ro = offer_material_site_stores.objects.get(id=id)
        ordr_date = request.POST.get('mrc_order_date')
        remark = request.POST.get('remark')
        
        data1 = create_mrc(offer=ro, date=ordr_date, remark=remark)
        data1.save()
        ro.tkc_mrc_initiate=1
        ro.save()
        
        pr = create_mrc.objects.latest("id")
        return render(request,'tkc/tkc_mrc_add_offer_stc.html',{'pr':pr})
        
    ro = offer_material_site_stores.objects.get(id=id)
    return render(request,'tkc/tkc_mrc_add_offer_stc.html',{'data': ro})
    


def format_tk_stc(request,id):
    data = create_mrc.objects.get(id=id)
    sid=data.offer.id
    
    off=offer_material_site_stores.objects.get(id=sid)
    ss=tkc_site_store_drr_info.objects.filter(area_store=off)
    sss=tkc_site_store_drr_info.objects.filter(area_store=off).last()
    
    #-------------------------------------------------
    
    did=data.offer.id
    
    com=offer_material_site_stores.objects.get(id=did)
    
    cc=UserCompanyDataMain.objects.filter(user_id_id=com.supplier.pk)
    
    #--------------------------------
    
    # ir=pi_verification_offier.objects.get(site_store=off)
    #print("----------------------",ir)
    
    
    acc_mat=offer_material_serial_number.objects.filter(offer=off,result=1).count()
    rej_mat=offer_material_serial_number.objects.filter(offer=off,result=-1).count()
  
    
    return render(request,"tkc/tkc_mrc_format_stc.html",{'data':data, 'ss':ss,'sss':sss, 'cc':cc,'acc_mat':acc_mat,'rej_mat':rej_mat})


def format_tk_create_stc(request,id):
    offer = offer_material_site_stores.objects.get(id=id)
    
    ss=tkc_site_store_drr_info.objects.filter(area_store=offer)
    sss=tkc_site_store_drr_info.objects.filter(area_store=offer).last()
    
    sampled_qty=offer_material_serial_number.objects.filter(offer=offer,is_sampled=1).count()
    
    acc_mat=offer_material_serial_number.objects.filter(offer=offer,result=1).count()
    rej_mat=offer_material_serial_number.objects.filter(offer=offer,result=-1).count()
    damaged_mat=offer_material_serial_number.objects.filter(offer=offer,Physical_Status_Nabl=-1).count()
    
    pi=pi_verification_offier.objects.get(site_store=offer)
    
    if offer.tkc_mrc_initiate == 1:
        pr = create_mrc.objects.latest("id")
        return render(request,"tkc/tkc_mrc_format_create_stc.html",{'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat,'pr':pr,'sampled_qty':sampled_qty,'damaged_mat':damaged_mat,'pi':pi})

    if request.method == "POST":
        
        ordr_date = request.POST.get('mrc_order_date')
        remark = request.POST.get('remark')
        
        data = create_mrc(offer=offer, date=ordr_date, remark=remark)
        
        data.save()
        offer.tkc_mrc_initiate=1
        offer.save()
        pr = create_mrc.objects.latest("id")
        return render(request,'tkc/tkc_mrc_format_create_stc.html',{'pr':pr,'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat,'sampled_qty':sampled_qty,'damaged_mat':damaged_mat,'pi':pi})
    
    return render(request,"tkc/tkc_mrc_format_create_stc.html",{'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat,'sampled_qty':sampled_qty,'damaged_mat':damaged_mat,'pi':pi})
    


def tkc_mrc_sign_list_stc(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    tk_mr=offer_material_site_stores.objects.filter(wo_id=id,accept_from_nabl=1,received_from_nabl=1,site_store_fk__Division__Circle=officer.Circle).order_by("id")
    y=[]  
    for i in tk_mr:
        j=i.wo.pakage
        pak=works_master.objects.all()
        for p in pak:
            if (j == p) & ((p.id == 7) or (p.id == 8) or (p.id == 9) or (p.id == 10)):
                y.append(i)

    cr_mr=create_mrc.objects.all()
    return render(request,'tkc/tkc_mrc_sign_list_stc.html',{"data":y,"cr_mr":cr_mr})
    

def upload_digi_tkc_mrc_stc(request, id):

    if request.method == "POST":

        upload_digi_doc_tkc = request.FILES['digi_pdf_tkc']

        tr = create_mrc.objects.get(id=id)

        tr. digi_sign = upload_digi_doc_tkc
        tr.digi_signflag = 1

        tr.save()
        return redirect(tkc_mrc_offer_list_stc)
       
       
    tr = create_mrc.objects.get(offer=id)
    tr1=offer_material_site_stores.objects.get(id=tr.offer.id)
    return render(request, 'tkc/upload_digi_tkc_stc.html', {'tr': tr,'offer': tr1})


def tkc_mrc_nabl_report_stc(request,id):
    offer = offer_material_site_stores.objects.get(id=id)

    re=offer_material_serial_number.objects.filter(offer=offer)
    
    return render(request,'tkc/tkc_mrc_nabl_report_stc.html',{'re':re})
    
  
   
#------------------- tkc MRC ONM ----------------------


def tkc_mrc_offer_list_onm(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    lst = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,site_store_fk__Division__Circle=officer.Circle).distinct('wo__id')    
    y=[]  
    for i in lst:
        j=i.wo.pakage
        pak=works_master.objects.all()
        for p in pak:
            if (j == p) & ((p.id == 2) or (p.id == 3) or (p.id == 4) or (p.id == 5) or (p.id == 6)):
                y.append(i)
    
    return render(request,'tkc/tkc_create_mrc_onm.html',{'data': y})


def create_mrcview_onm(request):
    # response = create_mrc.objects.all()
    return render(request, "tkc/tkc_create_mrc_onm.html")
    # ,{"response":response}
    


def format_tk_create_onm(request,id):
    offer = offer_material_site_stores.objects.get(id=id)
    
    ss=tkc_site_store_drr_info.objects.filter(area_store=offer)
    sss=tkc_site_store_drr_info.objects.filter(area_store=offer).last()
    
    sampled_qty=offer_material_serial_number.objects.filter(offer=offer,is_sampled=1).count()
    
    acc_mat=offer_material_serial_number.objects.filter(offer=offer,result=1).count()
    rej_mat=offer_material_serial_number.objects.filter(offer=offer,result=-1).count()
    damaged_mat=offer_material_serial_number.objects.filter(offer=offer,Physical_Status_Nabl=-1).count()
    
    pi=pi_verification_offier.objects.get(site_store=offer)
    
    if offer.tkc_mrc_initiate == 1:
        pr = create_mrc.objects.latest("id")
        return render(request,"tkc/tkc_mrc_format_create_onm.html",{'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat,'pr':pr,'sampled_qty':sampled_qty,'damaged_mat':damaged_mat,'pi':pi})
    
    if request.method == "POST":
        
        ordr_date = request.POST.get('mrc_order_date')
        remark = request.POST.get('remark')
        
        data = create_mrc(offer=offer, date=ordr_date, remark=remark)
        
        data.save()
        offer.tkc_mrc_initiate=1
        offer.save()
        pr = create_mrc.objects.latest("id")
        return render(request,'tkc/tkc_mrc_format_create_onm.html',{'pr':pr,'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat,'sampled_qty':sampled_qty,'damaged_mat':damaged_mat,'pi':pi})
  
    
    return render(request,"tkc/tkc_mrc_format_create_onm.html",{'offer':offer,'ss':ss,'sss':sss,'acc_mat':acc_mat,'rej_mat':rej_mat,'sampled_qty':sampled_qty,'damaged_mat':damaged_mat,'pi':pi})


def tkc_mrc_sign_list_onm(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    tk_mr=offer_material_site_stores.objects.filter(wo_id=id,accept_from_nabl=1,received_from_nabl=1,site_store_fk__Division__Circle=officer.Circle).order_by("id")
    y=[]  
    for i in tk_mr:
        j=i.wo.pakage
        pak=works_master.objects.all()
        for p in pak:
            if (j == p) & ((p.id == 2) or (p.id == 3) or (p.id == 4) or (p.id == 5) or (p.id == 6)):
                y.append(i)
    cr_mr=create_mrc.objects.all()
    return render(request,'tkc/tkc_mrc_sign_list_onm.html',{"data":y,"cr_mr":cr_mr})
    

def upload_digi_tkc_mrc_onm(request, id):

    if request.method == "POST":

        upload_digi_doc_tkc = request.FILES['digi_pdf_tkc']

        tr = create_mrc.objects.get(id=id)

        tr. digi_sign = upload_digi_doc_tkc
        tr.digi_signflag = 1

        tr.save()
        return redirect(tkc_mrc_offer_list_onm)
        
        
       
    tr = create_mrc.objects.get(offer=id)
    tr1=offer_material_site_stores.objects.get(id=tr.offer.id)
    return render(request, 'tkc/upload_digi_tkc_onm.html', {'tr': tr,'offer': tr1})


def tkc_mrc_nabl_report_onm(request,id):
    offer = offer_material_site_stores.objects.get(id=id)
    re=offer_material_serial_number.objects.filter(offer=offer)
    
    return render(request,'tkc/tkc_mrc_nabl_report_stc.html',{'re':re})


#---------------------TKC MRC TKC Dashboard--------------------

def tkc_mrc_offer_list_tkc(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    
    lst = offer_material_site_stores.objects.filter(supplier=supplier,accept_from_nabl=1,received_from_nabl=1).distinct('wo__id')
    return render(request,'tkc/tkc_create_mrc_tkc.html',{'data': lst})


def tkc_mrc_sign_list_tkc(request,id):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    
    tk_mr=offer_material_site_stores.objects.filter(wo_id=id,supplier=supplier,accept_from_nabl=1,received_from_nabl=1).order_by("id")
    
    cr_mr=create_mrc.objects.all()
    return render(request,'tkc/tkc_mrc_sign_list_tkc.html',{"data":tk_mr,"cr_mr":cr_mr})

#---------------------TKC MRC WO Creator Dashboard--------------------

def tkc_mrc_offer_list_wo_creator(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    lst = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('wo__id')
    return render(request,'tkc/tkc_create_mrc_wo_creator.html',{'data': lst})


def tkc_mrc_sign_list_wo_creator(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    tk_mr=offer_material_site_stores.objects.filter(wo_id=id,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).order_by("id")
    cr_mr=create_mrc.objects.all()
    return render(request,'tkc/tkc_mrc_sign_list_wo_creator.html',{"data":tk_mr,"cr_mr":cr_mr})


#---------------------TKC MRC WO approver Dashboard--------------------


def tkc_mrc_offer_list_wo_approver(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    lst = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('wo__id')
    return render(request,'tkc/tkc_create_mrc_wo_approver.html',{'data': lst})


def tkc_mrc_sign_list_wo_approver(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    tk_mr=offer_material_site_stores.objects.filter(wo_id=id,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).order_by("id")
    cr_mr=create_mrc.objects.all()
    return render(request,'tkc/tkc_mrc_sign_list_wo_approver.html',{"data":tk_mr,"cr_mr":cr_mr})


#---------------------TKC MRC sitestore Dashboard--------------------


def tkc_mrc_offer_list_sitestore(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    
    lst = offer_material_site_stores.objects.filter(site_store_fk=store,accept_from_nabl=1,received_from_nabl=1).distinct('wo__id')
    return render(request,'tkc/tkc_create_mrc_sitestore.html',{'data': lst})


def tkc_mrc_sign_list_sitestore(request,id):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    
    tk_mr=offer_material_site_stores.objects.filter(wo_id=id,site_store_fk=store,accept_from_nabl=1,received_from_nabl=1).order_by("id")
    
    cr_mr=create_mrc.objects.all()
    return render(request,'tkc/tkc_mrc_sign_list_sitestore.html',{"data":tk_mr,"cr_mr":cr_mr}) 


#--------------------------DGM STC DI--------------------------------

def tkc_mrc_offer_list_stc_di(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 


    x = offer_material_site_stores.objects.filter(Q(wo__pakage_id__in =[7,8,9,10],accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1)).distinct('wo__supplier__CompanyName_E')
    
    return render(request,'tkc/tkc_create_mrc_stc_di.html',{'data': x})

#     x = offer_material_site_stores.objects.filter(Q(wo__pakage_id__in =[7,8,9,10],accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle=officer.Circle)).distinct('wo__supplier__CompanyName_E')
    
#     return render(request,'tkc/tkc_create_mrc_stc_di.html',{'data': x})


# def tkc_mrc_offer_list_stc_di(request):
#     officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
#     request.session['officer'] = officer.user_zone 

#     x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle=officer.Circle).distinct('wo__supplier__CompanyName_E')
  
#     y=[]  
#     for i in x:
#         j=i.wo.pakage
#         pak=works_master.objects.all()
#         for p in pak:
#             if (j == p) and ((p.id == 7) or (p.id == 8) or (p.id == 9) or (p.id == 10)):
#                 y.append(i)
    
#     return render(request,'tkc/tkc_create_mrc_stc_di.html',{'data': y})


def tkc_mrc_all_di_stc_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    x = offer_material_site_stores.objects.filter(Q(wo__pakage_id__in =[7,8,9,10],wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1)).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_stc_di.html',{'data': x})


def tkc_mrc_sign_list_stc_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
    
    y=[]  
    for i in tk_mr:
        j=i.wo.pakage
        pak=works_master.objects.all()
        for p in pak:
            if (j == p) and ((p.id == 7) or (p.id == 8) or (p.id == 9) or (p.id == 10)):
                y.append(i)
                
    cir=[]
    for i in y:
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_stc_di.html',{"data":cir,"cr_mr":cr_mr})


def format_tk_create_stc_di(request,id):

    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    offer1 = offer_material_site_stores.objects.filter(id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1)
    
    offer=[]
    for i in offer1:
        offer2 = offer_material_site_stores.objects.filter(circle=i.circle,tkc_di__erp_di_number=i.tkc_di.erp_di_number,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1)
    
        for mat in offer2:
            offer.append(mat)
     
    ss1=[]
    for i in offer:
        ss=tkc_site_store_drr_info.objects.filter(area_store=i).order_by("drr_date")
        sss=tkc_site_store_drr_info.objects.filter(area_store=i).last()
        
        if ss:
            ss1.append(ss)
            

    flat_list = []
    for sublist in ss1:
        for num in sublist:
            flat_list.append(num)
   
     
    material_name=[]
    sam_qty=[]
    accepted_mat=[]
    rejected_mat=[]
    dam_mat=[]
    for i in offer:        
        sampled_qty=offer_material_serial_number.objects.filter(offer=i,is_sampled=1).count()
        acc_mat=offer_material_serial_number.objects.filter(offer=i,result=1).count()
        rej_mat=offer_material_serial_number.objects.filter(offer=i,result=-1).count()
        damaged_mat=offer_material_serial_number.objects.filter(offer=i,Physical_Status_Nabl=-1).count()
        material_name.append(i)
        sam_qty.append(sampled_qty)
        accepted_mat.append(acc_mat)
        rejected_mat.append(rej_mat)
        dam_mat.append(damaged_mat)
        
    zip1=zip(material_name,sam_qty,accepted_mat,rejected_mat,dam_mat)
    
    di_num =[]
    for i in offer:
        if i.tkc_di in di_num:
            pass
        else: 
            di_num.append(i.tkc_di)
        
    da=offer[0]
    
    mat_name=[]
    pi_doc=[]
    for i in offer:
        pi=pi_verification_offier.objects.filter(site_store=i)
        for x in pi:           
            mat_name.append(i)
            pi_doc.append(x)
    
    zip2=zip(mat_name,pi_doc)
    
    if da.tkc_mrc_initiate == 1:
        return render(request,"tkc/tkc_mrc_format_create_stc_di.html",{'offer':offer,'ss1':ss1,'ss':ss,'flat_list':flat_list,'sam_qty':sam_qty,'accepted_mat':accepted_mat,'rejected_mat':rejected_mat,'dam_mat':dam_mat,'zip1':zip1,"sss":sss,"da":da,"zip2":zip2 })
        
    if request.method == "POST":
        ordr_date = request.POST.get('mrc_order_date')
        
        remark = request.POST.get('remark')
        
        for i in di_num: 
            
            data = create_mrc.objects.create(tkc_di=i,date=ordr_date, remark=remark)
            
            data.circle=offer1[0].circle
            data.save()
            
        for i in offer:
            i.tkc_mrc_initiate=1
            i.tkc_mrc=data
            
            i.save()
            
            
            
        return render(request,"tkc/tkc_mrc_format_create_stc_di.html",{'offer':offer,'ss1':ss1,'ss':ss,'flat_list':flat_list,'sam_qty':sam_qty,'accepted_mat':accepted_mat,'rejected_mat':rejected_mat,'dam_mat':dam_mat,'zip1':zip1,"sss":sss,"da":da,"zip2":zip2 })
                    
    return render(request,"tkc/tkc_mrc_format_create_stc_di.html",{'offer':offer,'ss1':ss1,'ss':ss,'flat_list':flat_list,'sam_qty':sam_qty,'accepted_mat':accepted_mat,'rejected_mat':rejected_mat,'dam_mat':dam_mat,'zip1':zip1,"sss":sss,"da":da,"zip2":zip2 })

 
def upload_digi_tkc_mrc_stc_di(request, id):

    if request.method == "POST":

        upload_digi_doc_tkc = request.FILES['digi_pdf_tkc']

        tr = create_mrc.objects.get(id=id)

        tr. digi_sign = upload_digi_doc_tkc
        tr.digi_signflag = 1

        tr.save()
        return redirect(tkc_mrc_offer_list_stc_di)
       
       
    tr = create_mrc.objects.get(id=id)
    
    return render(request, 'tkc/upload_digi_tkc_mrc_stc_di.html', {'tr': tr})


def tkc_mrc_nabl_report_stc_di(request,id):
    offer = offer_material_site_stores.objects.get(id=id)

    re=offer_material_serial_number.objects.filter(offer=offer,is_sampled=1)
    
    return render(request,'tkc/tkc_mrc_nabl_report_stc_di.html',{'re':re})

    

#--------------------------TKC MRC ONM DI---------------------------------------

def tkc_mrc_offer_list_onm_di(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 


    x = offer_material_site_stores.objects.filter(Q(wo__pakage_id__in =[2,3,4,5,6],accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division=officer.Division,Physical_Status=1,Physical_Status_officer=1)).distinct('wo__supplier__CompanyName_E')
    
    return render(request,'tkc/tkc_create_mrc_onm_di.html',{'data': x})

#     x = offer_material_site_stores.objects.filter(Q(wo__pakage_id__in =[2,3,4,5,6],accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division=officer.Division)).distinct('wo__supplier__CompanyName_E')
    
#     return render(request,'tkc/tkc_create_mrc_onm_di.html',{'data': x})


# def tkc_mrc_offer_list_onm_di(request):
#     officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
#     request.session['officer'] = officer.user_zone 

#     x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division=officer.Division).distinct('wo__supplier__CompanyName_E')
    
#     y=[]  
#     for i in x:
#         j=i.wo.pakage
#         pak=works_master.objects.all()
#         for p in pak:
#             if (j == p) and ((p.id == 2) or(p.id == 3) or (p.id == 4) or (p.id == 5) or (p.id == 6)):
#                 y.append(i)
    
#     return render(request,'tkc/tkc_create_mrc_onm_di.html',{'data': y})



def tkc_mrc_all_di_onm_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    x = offer_material_site_stores.objects.filter(Q(wo__pakage_id__in =[2,3,4,5,6],wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division=officer.Division,Physical_Status=1,Physical_Status_officer=1)).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_onm_di.html',{'data': x})


def tkc_mrc_sign_list_onm_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division=officer.Division,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
    
    y=[]  
    for i in tk_mr:
        j=i.wo.pakage
        pak=works_master.objects.all()
        for p in pak:
            if (j == p) and ((p.id == 2) or (p.id == 3) or (p.id == 4) or (p.id == 5) or (p.id == 6)):
                y.append(i)
                
    cir=[]
    for i in y:
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_onm_di.html',{"data":cir,"cr_mr":cr_mr})


def format_tk_create_onm_di(request,id):

    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    offer1 = offer_material_site_stores.objects.filter(id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division=officer.Division,Physical_Status=1,Physical_Status_officer=1)
    
    offer=[]
    for i in offer1:
        offer2 = offer_material_site_stores.objects.filter(circle=i.circle,tkc_di__erp_di_number=i.tkc_di.erp_di_number,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division=officer.Division,Physical_Status=1,Physical_Status_officer=1)
    
        for mat in offer2:
            offer.append(mat)
     
    ss1=[]
    for i in offer:
        ss=tkc_site_store_drr_info.objects.filter(area_store=i).order_by("drr_date")
        sss=tkc_site_store_drr_info.objects.filter(area_store=i).last()
        
        if ss:
            ss1.append(ss)

    flat_list = []
    for sublist in ss1:
        for num in sublist:
            flat_list.append(num)
    
    
    material_name=[]
    sam_qty=[]
    accepted_mat=[]
    rejected_mat=[]
    dam_mat=[]
    for i in offer:        
        sampled_qty=offer_material_serial_number.objects.filter(offer=i,is_sampled=1).count()
        acc_mat=offer_material_serial_number.objects.filter(offer=i,result=1).count()
        rej_mat=offer_material_serial_number.objects.filter(offer=i,result=-1).count()
        damaged_mat=offer_material_serial_number.objects.filter(offer=i,Physical_Status_Nabl=-1).count()
        material_name.append(i)
        sam_qty.append(sampled_qty)
        accepted_mat.append(acc_mat)
        rejected_mat.append(rej_mat)
        dam_mat.append(damaged_mat)
        
    zip1=zip(material_name,sam_qty,accepted_mat,rejected_mat,dam_mat)
    
    di_num =[]
    for i in offer:
        if i.tkc_di in di_num:
            pass
        else: 
            di_num.append(i.tkc_di)
        
   
    da=offer[0]
    
    mat_name=[]
    pi_doc=[]
    for i in offer:
        pi=pi_verification_offier.objects.filter(site_store=i)
        for x in pi:           
            mat_name.append(i)
            pi_doc.append(x)
    
    zip2=zip(mat_name,pi_doc)

    
    if da.tkc_mrc_initiate == 1:
        return render(request,"tkc/tkc_mrc_format_create_onm_di.html",{'offer':offer,'ss1':ss1,'ss':ss,'flat_list':flat_list,'sam_qty':sam_qty,'accepted_mat':accepted_mat,'rejected_mat':rejected_mat,'dam_mat':dam_mat,'zip1':zip1,"sss":sss,"da":da,"zip2":zip2 })
        
    if request.method == "POST":
        ordr_date = request.POST.get('mrc_order_date')
        
        remark = request.POST.get('remark')
        
        for i in di_num: 
            
            data = create_mrc.objects.create(tkc_di=i,date=ordr_date, remark=remark)
            
            data.circle=offer1[0].circle
            data.save()
            
        for i in offer:
            i.tkc_mrc_initiate=1
            i.tkc_mrc=data
            
            i.save()        
            
        return render(request,"tkc/tkc_mrc_format_create_onm_di.html",{'offer':offer,'ss1':ss1,'ss':ss,'flat_list':flat_list,'sam_qty':sam_qty,'accepted_mat':accepted_mat,'rejected_mat':rejected_mat,'dam_mat':dam_mat,'zip1':zip1,"sss":sss,"da":da,"zip2":zip2 })
            
        
    return render(request,"tkc/tkc_mrc_format_create_onm_di.html",{'offer':offer,'ss1':ss1,'ss':ss,'flat_list':flat_list,'sam_qty':sam_qty,'accepted_mat':accepted_mat,'rejected_mat':rejected_mat,'dam_mat':dam_mat,'zip1':zip1,"sss":sss,"da":da,"zip2":zip2 })
    
 
def upload_digi_tkc_mrc_onm_di(request, id):

    if request.method == "POST":

        upload_digi_doc_tkc = request.FILES['digi_pdf_tkc']

        tr = create_mrc.objects.get(id=id)

        tr. digi_sign = upload_digi_doc_tkc
        tr.digi_signflag = 1

        tr.save()
        return redirect(tkc_mrc_offer_list_onm_di)
       
       
    tr = create_mrc.objects.get(id=id)
    
    return render(request, 'tkc/upload_digi_tkc_mrc_onm_di.html', {'tr': tr})
 

def tkc_mrc_nabl_report_onm_di(request,id):
    offer = offer_material_site_stores.objects.get(id=id)

    re=offer_material_serial_number.objects.filter(offer=offer,is_sampled=1)
    
    return render(request,'tkc/tkc_mrc_nabl_report_onm_di.html',{'re':re})


#---------------------------- TKC MRC GM Circle-----------------------------------


def tkc_mrc_offer_list_gm_di(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 

    x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/tkc_create_mrc_gm_di.html',{'data': x})


def tkc_mrc_all_di_gm_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    x = offer_material_site_stores.objects.filter(wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_gm_di.html',{'data': x})


def tkc_mrc_sign_list_gm_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,circle=officer.Circle,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_gm_di.html',{"data":cir,"cr_mr":cr_mr})


#---------------------------- TKC MRC TKC Dashboard -----------------------------------


def tkc_mrc_offer_list_tkc_di(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
 
    x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,supplier=supplier,Physical_Status=1,Physical_Status_officer=1).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/tkc_create_mrc_tkc_di.html',{'data': x})


def tkc_mrc_all_di_tkc_di(request,id):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
 
    x = offer_material_site_stores.objects.filter(wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,supplier=supplier,Physical_Status=1,Physical_Status_officer=1).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_tkc_di.html',{'data': x})


def tkc_mrc_sign_list_tkc_di(request,id):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])

    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,supplier=supplier,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_tkc_di.html',{"data":cir,"cr_mr":cr_mr})


#---------------------------- TKC MRC WO Creator Dashboard -----------------------------------


def tkc_mrc_offer_list_wo_creator_di(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,wo__zone=officer.user_zone,Physical_Status=1,Physical_Status_officer=1).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/tkc_create_mrc_wo_creator_di.html',{'data': x})


def tkc_mrc_all_di_wo_creator_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
 
    x = offer_material_site_stores.objects.filter(wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,wo__zone=officer.user_zone,Physical_Status=1,Physical_Status_officer=1).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_wo_creator_di.html',{'data': x})


def tkc_mrc_sign_list_wo_creator_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    

    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,wo__zone=officer.user_zone,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_wo_creator_di.html',{"data":cir,"cr_mr":cr_mr})


#---------------------------- TKC MRC WO Approver Dashboard -----------------------------------


def tkc_mrc_offer_list_wo_approver_di(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,wo__zone=officer.user_zone,Physical_Status=1,Physical_Status_officer=1).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/tkc_create_mrc_wo_approver_di.html',{'data': x})


def tkc_mrc_all_di_wo_approver_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
 
    x = offer_material_site_stores.objects.filter(wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,wo__zone=officer.user_zone,Physical_Status=1,Physical_Status_officer=1).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_wo_approver_di.html',{'data': x})


def tkc_mrc_sign_list_wo_approver_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    

    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,wo__zone=officer.user_zone,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_wo_approver_di.html',{"data":cir,"cr_mr":cr_mr})


#---------------------------- TKC MRC Site Store Dashboard -----------------------------------


def tkc_mrc_offer_list_sitestore_di(request):
    store = SiteStore_Master.objects.get(otp = request.session['otp']) 
    
    x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk=store,Physical_Status=1,Physical_Status_officer=1).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/tkc_create_mrc_sitestore_di.html',{'data': x})


def tkc_mrc_all_di_sitestore_di(request,id):
    store = SiteStore_Master.objects.get(otp = request.session['otp']) 
 
    x = offer_material_site_stores.objects.filter(wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk=store,Physical_Status=1,Physical_Status_officer=1).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_sitestore_di.html',{'data': x})


def tkc_mrc_sign_list_sitestore_di(request,id):
    store = SiteStore_Master.objects.get(otp = request.session['otp'])
    
    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk=store,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_sitestore_di.html',{"data":cir,"cr_mr":cr_mr})


#---------------------------- TKC MRC PMA Dashboard -----------------------------------


def tkc_mrc_offer_list_pma_di(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    x = offer_material_site_stores.objects.filter(accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle__Region__Discom=officer.Discom,Physical_Status=1,Physical_Status_officer=1).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/tkc_create_mrc_pma_di.html',{'data': x})


def tkc_mrc_all_di_pma_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
 
    x = offer_material_site_stores.objects.filter(wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle__Region__Discom=officer.Discom,Physical_Status=1,Physical_Status_officer=1).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_all_di_pma_di.html',{'data': x})


def tkc_mrc_sign_list_pma_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone
    
    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,is_di_created=True,site_store_fk__Division__Circle__Region__Discom=officer.Discom,Physical_Status=1,Physical_Status_officer=1).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign_list_pma_di.html',{"data":cir,"cr_mr":cr_mr})


#-----------------------------TKC MRC by Gaurav Pathak end here----------------------------

def Fake_called(request):
    print("print start")
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    user_zone=data.User_zone
    name=data.CompanyName_E
    # print("user_id:",user_id)
    # print("name:",name)
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=user_zone,Material__PDI_Approved_Status=-2,Material__PDI_Complete=1,tkc_name=name).distinct('offer_no')
    return render(request,'tkc/fake_call_list.html',{"data":pdi_assign}) 

def pdi_details(request,offer_no):
    data1 = PDI_Inspection_Info.objects.filter(offer_no=offer_no)
    unique_data=PDI_Inspection_Info.objects.filter(offer_no=offer_no).distinct('offer_no')
    for i in unique_data:
        offer_no=i.offer_no 
    return render(request, 'tkc/pdi_details.html', {'data1': data1,'unique_data':unique_data,'offer_no':offer_no})

def rejected_offer(request):
    print("print start")
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    user_zone=data.User_zone
    name=data.CompanyName_E
    print("user_id:",user_id)
    print("name:",name)
    pdi_assign=PDI_Inspection_Info.objects.filter(Material__PDI_Assign=1,wo__zone=user_zone,Material__PDI_Approved_Status=-1,Material__PDI_Complete=1,tkc_name=name).distinct('offer_no')
    return render(request,'tkc/rejected_offer.html',{"data":pdi_assign})


#----------shubham tripathi code start from here 11/7/2023----------

# ---------------------tkc new fqp intimation list ---------------------------
def tkc_new_fqpintimation_wo(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC":
            wo_data = TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id).order_by('-id')
            return render(request, 'new_fqpintimation/wo_intimation.html', {'supplier': supplier,'wo_data':wo_data})
        else:
            return render(request, 'tkc/creater_base.html', {'supplier': supplier})
    else:
        return render(request, 'tkc/creater_base.html', { 'supplier': supplier})


def tkc_new_fqpintimation_tasklist(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_id=request.GET.get('woid')
    if supplier.cgm_approval:
        wo_data=TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,id=wo_id).order_by('-id')
        wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id).order_by('-id')
        mil_data = Wo_Task_Milestone.objects.all()
        return render(request, 'new_fqpintimation/tkc_intimation_tasklist.html', {'supplier': supplier,'wo_task_data':wo_task_data,'wo_data':wo_data,'mil_data':mil_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'supplier': supplier})        

    
def tkc_new_fqpintimation_create(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        if request.method == "POST":
            wo_id = request.POST.get('woid')
            wotask_id = request.POST.get('wotask_id')
            wotask_milestone = request.POST.get('wotask_milestone')
            feeder_id = request.POST.get('feeder_id')#  for create intimation unique no
            work_execution_detail=request.POST.get('work_execution_detail')
            brief_description_of_work=request.POST.get('brief_description_of_work')
            intimation_remark=request.POST.get('intimation_remark')
            date_of_execution=request.POST.get('date_of_execution')
            date_of_readines=request.POST.get('date_of_readines')
            date_of_completion=request.POST.get('date_of_completion')
            try:
                work_execution_milestone_image1 = request.FILES['work_execution_milestone_image1']
                work_execution_milestone_image2 = request.FILES['work_execution_milestone_image2']
            except Exception as e:
                pass

            try:
                if wotask_milestone is not None or wotask_milestone != "":
                    tmd = Wo_Task_Milestone.objects.create(milestone_id=wotask_milestone,wo_task_id=wotask_id)            
                    wotask_milestone = tmd.id                    
                intimation_data = New_FqpIntimation(wo_task_id=wotask_id,wotask_milestone_id=wotask_milestone,work_execution_detail=work_execution_detail,brief_description_of_work=brief_description_of_work,work_execution_milestone_image1=work_execution_milestone_image1,work_execution_milestone_image2=work_execution_milestone_image2,date_of_execution=date_of_execution,date_of_readines=date_of_readines,date_of_completion=date_of_completion,intimation_remark=intimation_remark,user_id=supplier.User_Id)
                intimation_data.save()
            except Exception as e:
                pass

            cd=date.today()
            cd = cd.strftime("%d-%m-%Y")
            intimation_unique_no = str(feeder_id)+"/"+str(intimation_data.id)+"/"+str(cd)
            milestone_category_id = request.POST.getlist('milestone_category[]')
            try:
                New_FqpIntimation.objects.filter(id=intimation_data.id).update(intimation_unique_no=intimation_unique_no)# for save unique no 
                for i in milestone_category_id:
                    inti_mile_cat_data= New_FqpIntimation_milestone_category.objects.create(milestone_category_id=i,fqpintimation_id=intimation_data.id)
            except Exception as e:
                pass

            task_data=Wo_Order_Task.objects.filter(id=wotask_id).first()
            if task_data is not None:
                try:
                    ofc=Officer.objects.filter(Q(is_active=True,Region_id=task_data.region_id) & ((Q(role__Role_Name="WO_CREATER") | Q(role__Role_Name="WO_APPROVER")) | 
                    Q(role__Role_Name="GM(CIRCLE)",Circle_id=task_data.circle_id,Division_id__isnull=True,DC_Zone__isnull=True) | 
                    Q(role__Role_Name="DGM_ONM",Circle_id=task_data.circle_id,Division_id=task_data.division_id,DC_Zone_id__isnull=True) | 
                    Q(role__Role_Name="DGM_STC",Circle_id=task_data.circle_id,Division_id__isnull=True,DC_Zone_id__isnull=True) | 
                    (Q(role__Role_Name="PMA",Circle_id=task_data.circle_id) & (Q(Division_id__isnull=True,DC_Zone_id__isnull=True) | Q(Division_id=task_data.division_id,DC_Zone_id=task_data.distribution_center_id) | Q(Division_id=task_data.division_id,DC_Zone_id__isnull=True))) | 
                    Q(role__Role_Name="JE",Circle_id=task_data.circle_id,Division_id=task_data.division_id,DC_Zone=task_data.distribution_center_id)))    
                    # print("ofc---len--------------",len(ofc))
                    template_id = 1007605812683859871 
                    userdata = ofc
                    var1 = " " + str(task_data.gis_feeder_id)+" "
                    var2 = " " + str(task_data.wo.Header.Contract_Description)+ " "
                    otherdata = ""
                    message_type = "FQP Intimation Creation"
                    cmsg.send_message(template_id,userdata,var1,var2,otherdata,message_type)#for send message when intimation created
                except Exception as e:
                    pass
            # New_FqpIntimation_Observation.objects.create(fqpintimation_id = intimation_data.id,tkc_review_remark=tkc_review_remark,tkc_review_status=0)
            # return redirect('tkc_new_fqpintimation_wo')
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            wo_id = request.GET.get('woid')
            wo_taskid = request.GET.get('wotaskid')
            wo_data=TKCWoInfo.objects.filter(id=wo_id,supplier=supplier.User_Id)
            wo_task_data=Wo_Order_Task.objects.filter(wo_id=wo_id,id=wo_taskid)
            # mile_data = Wo_Task_Milestone.objects.filter(wo_task_id = wo_taskid )   #task milestone added by wo creater
            mile_data = Milestone_Main.objects.all() #all milestone
            return render(request, 'new_fqpintimation/tkc_fqpintimate_create.html', {'supplier': supplier,'wo_data':wo_data,'wo_task_data':wo_task_data,'mile_data':mile_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"supplier": supplier,})


def tkc_new_fqpintimation_list(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_id=request.GET.get('woid')
    wotask_id=request.GET.get('wotaskid')
    if supplier.cgm_approval:
        wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id = wotask_id)
        wo_data=TKCWoInfo.objects.filter(id=wo_id)
        fqpinti_mile_cat_data = New_FqpIntimation_milestone_category.objects.all().order_by('-id')
        wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,id=wotask_id)
        return render(request, 'new_fqpintimation/tkc_intimation_list.html', {'supplier': supplier,'wo_fqpi_data':wo_fqpi_data,'wo_data':wo_data,'wo_task_data':wo_task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'supplier': supplier})        



def tkc_new_fqpintimation_observation_detail(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        fqpintimation_id = request.GET.get('fqpintimationid')
        # wo_id = request.GET.get('woid')
        wotask_id = request.GET.get('wotaskid')
        # if fqpintimation_id != "":
        #     int_data=New_FqpIntimation.objects.filter(id=fqpintimation_id)
        # else:
        int_data=New_FqpIntimation.objects.filter(id=fqpintimation_id,wo_task_id=wotask_id,user_id=supplier.User_Id)
        # print("in-------------------",int_data)
        fqpinti_mile_cat_data = New_FqpIntimation_milestone_category.objects.all()
        task_data=Wo_Order_Task.objects.filter(id=wotask_id,wo__supplier__User_Id=supplier.User_Id)
        observation=New_FqpIntimation_Observation.objects.filter(fqpintimation_id=fqpintimation_id)
        observation_data =New_FqpIntimation_Observation_data.objects.filter(observation__fqpintimation_id=fqpintimation_id)
        officer_data=New_FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id)
        close_inti=New_FqpIntimation_Observation_Close.objects.filter(fqpintimation_id=fqpintimation_id)
        return render(request, 'new_fqpintimation/tkc_fqpintimation_observation_detail.html', {'supplier': supplier,'close_inti':close_inti,'int_data':int_data,'officer_data':officer_data,'observation':observation,'observation_data':observation_data,'task_data':task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"supplier": supplier,})

def tkc_new_fqpintimation_observation_review(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        if request.method == "POST":
            # fqpintimation_id = request.POST.get('fqpintimation_id')
            observation_id=request.POST.get('observation_id')
            tkc_review_remark = request.POST.get('tkc_review_remark')
            tkc_review_status=request.POST.get('tkc_review_status')
            tkc_review_date = request.POST.get('tkc_review_date')
            observation_count = request.POST.get('observation_count')
            tkc_review_image = request.FILES['tkc_review_image']

            if int(observation_count) <= 1:
                observation_count = int(observation_count) + 1
                New_FqpIntimation_Observation.objects.filter(id=observation_id).update(observation_count=observation_count)
                a=New_FqpIntimation_Observation_data(observation_id=observation_id,tkc_review_remark=tkc_review_remark,tkc_review_status=tkc_review_status,tkc_review_date=tkc_review_date,tkc_review_image=tkc_review_image)
                a.save()
                
                try:            # for send message when task review send by tkc
                    obj_data = New_FqpIntimation_Observation.objects.filter(id=observation_id).first()
                    task_data = Wo_Order_Task.objects.filter(id=obj_data.fqpintimation_id.wo_task_id).first()
                    if task_data is not None:
                        ofc=Officer.objects.filter(Q(is_active=True,Region_id=task_data.region_id) & ((Q(role__Role_Name="WO_CREATER") | Q(role__Role_Name="WO_APPROVER")) | 
                        Q(role__Role_Name="GM(CIRCLE)",Circle_id=task_data.circle_id,Division_id__isnull=True,DC_Zone__isnull=True) | 
                        Q(role__Role_Name="DGM_ONM",Circle_id=task_data.circle_id,Division_id=task_data.division_id,DC_Zone_id__isnull=True) | 
                        Q(role__Role_Name="DGM_STC",Circle_id=task_data.circle_id,Division_id__isnull=True,DC_Zone_id__isnull=True) | 
                        (Q(role__Role_Name="PMA",Circle_id=task_data.circle_id) & (Q(Division_id__isnull=True,DC_Zone_id__isnull=True) | Q(Division_id=task_data.division_id,DC_Zone_id=task_data.distribution_center_id) | Q(Division_id=task_data.division_id,DC_Zone_id__isnull=True))) | 
                        Q(role__Role_Name="JE",Circle_id=task_data.circle_id,Division_id=task_data.division_id,DC_Zone=task_data.distribution_center_id)))    
                        # print("ofc---len--------------",len(ofc))
                        template_id = 1007959375728863432 
                        userdata = ofc
                        var1 = " " + str(task_data.gis_feeder_id)+" "
                        var2 = " " + str(task_data.wo.Header.Contract_Description)+ " "
                        otherdata = ""
                        message_type = "FQP Intimation Rework"
                        cmsg.send_message(template_id,userdata,var1,var2,otherdata,message_type)#for send message when intimation created
                except Exception as e:
                    pass

            else:
                pass
                print("observation count 2 condtiono-----------")
            # return redirect('tkc_new_fqpintimation_wo')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"supplier": supplier,})


def tkc_fqpintimation_milestone_category_list(request):
    milestone_main_id = request.GET.get('wotask_milestone_id')
    mld = Milestone_Main.objects.filter(id=milestone_main_id).first()
    # mld = Wo_Task_Milestone.objects.filter(id=milestone_main_id).first()
    mile_cat_data = list(Milestone_Main_Category.objects.filter(milestone_main_id=mld.id).values('id','milestone_category_name','milestone_main'))
    return JsonResponse({"mile_cat_data":mile_cat_data})

def tkc_new_fqpintimation_addmilestone_category(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if supplier.cgm_approval:
        # cd=date.today()
        # cd = cd.strftime("%d-%m-%Y")            
        if request.method == "POST":
            fqpintimation_id = request.POST.get('fqpintimationid')
            milestone_category_id = request.POST.getlist('milestone_category[]')
            print(milestone_category_id,"-------",fqpintimation_id,"-----------")
            if fqpintimation_id is not None and milestone_category_id is not None:
                for i in milestone_category_id:
                    inti_mile_cat_data= New_FqpIntimation_milestone_category.objects.create(milestone_category_id=i,fqpintimation_id=fqpintimation_id)
                New_FqpIntimation.objects.filter(id=fqpintimation_id,wo_task_id=wotaskid).update(intimation_status=0)
            # return redirect('tkc_new_fqpintimation_wo')
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            fqpintimation_id = request.GET.get('fqpintimationid')
            wotaskid = request.GET.get('wotaskid')
            inti_data=New_FqpIntimation.objects.filter(id=fqpintimation_id,wo_task_id=wotaskid).first()
            mile_cat_data = Milestone_Main_Category.objects.filter(milestone_main_id = inti_data.wotask_milestone.milestone)
            inti_mile_cat_data = New_FqpIntimation_milestone_category.objects.filter(fqpintimation_id=fqpintimation_id)            
            return render(request, 'new_fqpintimation/add_milestone_category.html', {'supplier': supplier,'inti_data':inti_data,"mile_cat_data":mile_cat_data,'inti_mile_cat_data':inti_mile_cat_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {"supplier": supplier,})

# ------------------------fqp intimation end here----------------------------------------

# to-do list for creator

def mrc_offer_list(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    x = offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, accept_from_nabl=1,received_from_nabl=1,tkc_mrc_initiate=0,wo__zone=officer.user_zone).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/mrc_list.html',{'data': x})


def tkc_mrc_all_di(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
 
    x = offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, wo__supplier__User_Id=id,tkc_mrc_initiate=0,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('tkc_di__erp_di_number')
    print(x)
    return render(request,'tkc/mrc_all_di.html',{'data': x})


# def tkc_mrc_all_di_wo_creator_di(request,id):
#     officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
#     request.session['officer'] = officer.user_zone 
    
 
#     x = offer_material_site_stores.objects.filter(wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('tkc_di__erp_di_number')

#     return render(request,'tkc/tkc_mrc_all_di_wo_creator_di.html',{'data': x})


def tkc_mrc_sign_list(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    

    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, tkc_di_id=di.id,tkc_mrc_initiate=0,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/mrc_sign_list.html',{"data":cir,"cr_mr":cr_mr})


#to do list for approver

def mrc_offer_list_approver(request):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
    x = offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, tkc_mrc_initiate=0,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('wo__supplier__CompanyName_E')
      
    return render(request,'tkc/create_mrc_list.html',{'data': x})


def tkc_mrc_all_di_approver(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    
 
    x = offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, tkc_mrc_initiate=0,wo__supplier__User_Id=id,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('tkc_di__erp_di_number')

    return render(request,'tkc/tkc_mrc_di.html',{'data': x})


def tkc_mrc_sign_list_approver(request,id):
    officer = Officer.objects.get(employ_login_id=request.session['employ_login_id'])
    request.session['officer'] = officer.user_zone 
    

    di=tkc_di_master.objects.get(id=id)

    tk_mr=offer_material_site_stores.objects.filter(tkc_di__erp_di_number__isnull=False, tkc_mrc_initiate=0,tkc_di_id=di.id,accept_from_nabl=1,received_from_nabl=1,wo__zone=officer.user_zone).distinct('circle__Circle_Name_E')
                
    cir=[]
    for i in tk_mr:        
        if i.circle in cir:
            pass
        else:
            cir.append(i)
    
    cr_mr=create_mrc.objects.all()

    return render(request,'tkc/tkc_mrc_sign.html',{"data":cir,"cr_mr":cr_mr})



# to do list for tkc

def tkc_todo_list(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])     
    # user_zone=supplier.User_zone  
    di_data= offer_material_site_stores.objects.filter(supplier=con, Dispatch_Status=0).distinct('tkc_di')
    len_di_data = len(di_data)
      
    invoice_data = Invoice.objects.filter(~Q(status=-1),work_order_id__supplier__User_Id=con.User_Id, status=0)
    len_invoice_data = len(invoice_data)
    
    BG_data = TKCWoInfo_Bg.objects.filter(Status=1, BG_Approved_Status = 0, BG_Submit = 1, TKCWoInfo__supplier=con)
    len_BG_data = len(BG_data)
    
    LOC_data = TKCWoInfo_LOC.objects.filter(Status=1, LOC_Approved_Status = 0, LOC_Submit = 1, TKCWoInfo__supplier=con)
    len_LOC_data = len(LOC_data)
    
    pert_data = TKCWoInfo_Pert.objects.filter(Status=1, Pert_Approved_Status = 0, Pert_Submit = 1, TKCWoInfo__supplier=con)
    len_pert_data = len(pert_data)
    
    mqpdoc = TKC_MqpPlanDocuments.objects.filter(status=1, mqpdoc_approved_status = 0, mqpdoc_submit = 1, tkcwoinfo__supplier=con)
    len_mqpdoc = len(mqpdoc)
    
    fqpdoc = TKC_FqpPlanDocuments.objects.filter(status=1, fqpdoc_approved_status = 0, fqpdoc_submit = 1, tkcwoinfo__supplier=con)
    len_fqpdoc = len(fqpdoc)
    
    otherdoc = TKCOtherDocuments.objects.filter(status=1, otherdoc_approved_status = 0, otherdoc_submit = 1, tkcwoinfo__supplier=con)
    len_otherdoc = len(otherdoc)
    
    print(len_invoice_data)
    
    return render(request, 'tkc/tkc_todo_list.html', {'len_invoice_data':len_invoice_data, 'len_BG_data':len_BG_data, 'len_LOC_data':len_LOC_data,
                                                      'len_pert_data':len_pert_data, 'len_mqpdoc':len_mqpdoc, 'len_fqpdoc':len_fqpdoc, 'len_otherdoc':len_otherdoc})




def all_pending_di(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'])
    con = User_Registration.objects.get(Otp=request.session['otp'])
    if supplier.cgm_approval:
        wo= offer_material_site_stores.objects.filter(supplier=supplier, Dispatch_Status=0).distinct('tkc_di')
        # wo = tkc_di_master.objects.filter(wo__supplier=supplier,di_digital_upload_status=1)
        return render(request, 'wo/all_pending_di_data.html', {"wo": wo, 'con': con})
    else:
        messages.warning(
            request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'con': con})
    
    
def view_di_material(request,di_id):
    con = User_Registration.objects.get(Otp=request.session['otp'])
    di_obj = tkc_di_master.objects.get(id=di_id)
    offer_material_data = offer_material_site_stores.objects.filter(tkc_di = di_obj)
    offer_material_dispatch_data = offer_material_site_stores.objects.filter(tkc_di = di_obj,Dispatch_Status = 1)
    if len(offer_material_data) == len(offer_material_dispatch_data):
        dispatch_status = 1
    else:
        dispatch_status = 0

    return render(request, 'wo/view_di.html',
                  {"con": con, 'offer_material_data': offer_material_data,"di_data":di_obj,"dispatch_status":dispatch_status})
 
    
def pending_invoice_wo_list(request):    
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC" and supplier.blacklisted == 0 :            
            data = Invoice.objects.filter(status=0, order_type = 'WorkOrder', user=supplier).values_list('work_order', flat=True)
            unique_wo_ids = list(set(list(data)))
            wo_data = TKCWoInfo.objects.filter(id__in = unique_wo_ids ,Wo_Approved_Status=1).order_by('-id')
           
            wo_amt = TKCWoInfo_Contract_Price.objects.values('TKCWoInfo').annotate(total_amount=Sum('Amount'))
            return render(request, 'tkc_invoice/invoice_list.html', {'supplier': supplier,'wo_data':wo_data,'wo_amt':wo_amt})
        else:
            return redirect('/tkc/basic')
    else:
        return redirect(curl)
    
    


        
def pending_invoice_list(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    wo_id=request.GET.get('woid')
    # print("wo_id--------------------------",wo_id)
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC" and supplier.blacklisted == 0 :
            if TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,Wo_Approved_Status=1,id=wo_id).exists():
                in_data=Invoice.objects.filter(~Q(status=-1),work_order_id__supplier__User_Id=supplier.User_Id,work_order_id=wo_id, status=0).order_by('-id')
                wo_data = TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,Wo_Approved_Status=1,id=wo_id).last()
                wo_amt = TKCWoInfo_Contract_Price.objects.filter(TKCWoInfo_id=wo_id).aggregate(Sum('Amount'))
                # woamm = TKCWoInfo_Contract_Price.objects.filter(~Q(status=-1),TKCWoInfo_id=wo_id).aggregate(Sum('total_amount'))
                in_amount=Invoice.objects.filter(status=0,dgm_em_status=1,purchase_order_id=wo_id).aggregate(Sum('total_invoice_amount'))
                return render(request, 'tkc_invoice/tkc_invoicelist.html', {'supplier': supplier,'in_data':in_data,"wo_data":wo_data,'in_amount':in_amount,'wo_amt':wo_amt})
            else:
                wo_data=""
                in_data=""
                return render(request, 'tkc_invoice/tkc_invoicelist.html', {'supplier': supplier,'in_data':in_data,"wo_data":wo_data,})
        else:
            return redirect('/tkc/basic')
    else:
        return redirect(curl)
    
    

def pending_upload_bg(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    
    BG = TKCWoInfo_Bg.objects.filter(Status=1, BG_Approved_Status = 0, BG_Submit = 1, TKCWoInfo__supplier=con)
    Bg_Type = TKCWoInfo_Bg_Type.objects.filter(Status=1)
    return render(request, 'wo/pending_upload_bg.html', {'con': con, 'BG': BG, 'Bg_Type': Bg_Type})
    

def pending_upload_loc(request):    
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])  
        
    LOC = TKCWoInfo_LOC.objects.filter(Status=1, LOC_Approved_Status = 0, LOC_Submit = 1, TKCWoInfo__supplier=con)
    return render(request, 'wo/pending_upload_loc.html', {'con': con, 'LOC': LOC})


def pending_upload_pert(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])        
    Pert = TKCWoInfo_Pert.objects.filter(Status=1, Pert_Approved_Status = 0, Pert_Submit = 1, TKCWoInfo__supplier=con)    
    return render(request, 'wo/pending_upload_pert.html', {'con': con, 'Pert': Pert})


def pending_mqpdoc(request):
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
   
    mqpdoc = TKC_MqpPlanDocuments.objects.filter(status=1, mqpdoc_approved_status = 0, mqpdoc_submit = 1, tkcwoinfo__supplier=con)    
    return render(request, 'wo/pending_mqp.html', {'con': con, 'mqpdoc': mqpdoc})


def pending_upload_fqpdoc(request):    
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
   
    fqpdoc = TKC_FqpPlanDocuments.objects.filter(status=1, fqpdoc_approved_status = 0, fqpdoc_submit = 1, tkcwoinfo__supplier=con)
    return render(request, 'wo/pending_fqp.html', {'con': con, 'fqpdoc': fqpdoc})

def pending_otherdoc(request, wo_id):
    data = TKCWoInfo.objects.get(id=wo_id)
    con = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
   
    otherdoc = TKCOtherDocuments.objects.filter(status=1, otherdoc_approved_status = 0, otherdoc_submit = 1, tkcwoinfo__supplier=con)
    return render(request, 'wo/upload_OtherDocuments.html', {'con': con, 'otherdoc': otherdoc})



def new_fqpintimation(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "TKC":
            wo_intimate_data = New_FqpIntimation.objects.filter(intimation_status = 0).values_list('wo_task__wo',flat = True)
            unique_wo_data = set(list(wo_intimate_data))
            wo_data = TKCWoInfo.objects.filter(id__in =unique_wo_data, supplier__User_Id=supplier.User_Id).order_by('-id')
            return render(request, 'new_fqpintimation/new_intimation_data.html', {'supplier': supplier,'wo_data':wo_data})
        else:
            return render(request, 'tkc/creater_base.html', {'supplier': supplier})
    else:
        return render(request, 'tkc/creater_base.html', { 'supplier': supplier})
    
    
    


    
def new_fqpintimation_tasklist(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_id=request.GET.get('woid')
    if supplier.cgm_approval:
        wo_data=TKCWoInfo.objects.filter(supplier__User_Id=supplier.User_Id,id=wo_id).order_by('-id')
        
        intimate_pending_data = New_FqpIntimation.objects.filter(intimation_status = 0,wo_task__wo = wo_id).values_list('wo_task',flat = True)
        intimate_pending_data_unique = set(list(intimate_pending_data))
        wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),id__in = intimate_pending_data_unique,wo_id=wo_id).order_by('-id')
        mil_data = Wo_Task_Milestone.objects.all()
        print(wo_task_data)
        
        return render(request, 'new_fqpintimation/new_intimation_tasklist.html', {'supplier': supplier,'wo_task_data':wo_task_data,'wo_data':wo_data,'mil_data':mil_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'supplier': supplier})  
      
    

def new_fqpintimation_list(request):
    supplier = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    wo_id=request.GET.get('woid')
    wotask_id=request.GET.get('wotaskid')
    if supplier.cgm_approval:
        wo_fqpi_data=New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id = wotask_id, intimation_status=0)
        wo_data=TKCWoInfo.objects.filter(id=wo_id)
        fqpinti_mile_cat_data = New_FqpIntimation_milestone_category.objects.filter(fqpintimation__intimation_status=0).order_by('-id')
        wo_task_data=Wo_Order_Task.objects.filter(~Q(status=-1),wo_id=wo_id,id=wotask_id)
        return render(request, 'new_fqpintimation/tkc_intimation_list.html', {'supplier': supplier,'wo_fqpi_data':wo_fqpi_data,'wo_data':wo_data,'wo_task_data':wo_task_data,'fqpinti_mile_cat_data':fqpinti_mile_cat_data})
    else:
        messages.warning(request, "Your Application is Under Process")
        return render(request, 'tkc/creater_base.html', {'supplier': supplier})   


