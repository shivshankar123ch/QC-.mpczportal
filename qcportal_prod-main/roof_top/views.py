import django
from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
# Create your views here.
from main.models import *

import requests
from datetime import datetime
import datetime


def transaction_history_solar(request):
    data = roof_top_first.objects.get(otp=request.session['otp_two'])
    payu_count = payment_roof_top.objects.filter(Contact_No=data.contact,Payu_Status='success')
    return render(request, 'roof/roof_transaction_data.html', {"posted": payu_count})



def roof_top_one(request):
    if request.session.has_key('otp_one'):
        if request.method == 'POST':
            user_type = request.POST.get('user_type')
            agency_name = request.POST.get('one')
            auth_p = request.POST.get('two')
            contact = request.POST.get('three')
            email = request.POST.get('four')
            pan = request.POST.get('five')
            gst = request.POST.get('six')
            address = request.POST.get('address')
            zone = request.POST.get('user')

            reg_date = datetime.datetime.today()
            print('gst',gst)

            print('xxxxxxxxxxxx',address)
            
            if roof_top_first.objects.filter(pan_card=pan,user_zone=zone).exists():            
                messages.warning(request, "Pan Card number already exists ")
                return render(request, 'roof/agent_first.html')
        
            else:
                user_details = roof_top_first.objects.filter(otp=request.session['otp_one'])
                user_details.update(user_zone=zone,user_type=user_type,agency_name=agency_name,gst=gst,address=address,name_of_auth=auth_p,pan_card=pan,email=email,created_by='user',basic_details=1,reg_date=reg_date)
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007575598720789466&mobile_number=" + str(
                    contact) + "&v1=" + str(agency_name) + "&v2=" + str() + "&v3=" + str(contact) + "&v4=" + str(
                    'https://qcportal.mpcz.in/')
                response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1007575598720789466',date = datetime.datetime.now(),mobile_number = contact)
                sms_template.save()
                    
                    
                messages.warning(request, "You are successfully registered")
                return render(request,'main/index.html')

    return redirect('/')


import random
import math
import requests
# def login_reg(request):
#     if request.method == "POST":
#         oid = request.POST.get('contact')
#         if roof_top_first.objects.filter(contact=oid).exists():
#             data = roof_top_first.objects.filter(contact=oid)
#             def generateOTP():
#                 OTP = ""
#                 digits = "0123456789"
#                 for i in range(6):
#                     OTP += digits[math.floor(random.random() * 10)]
#                 return OTP
#             otp = generateOTP()
#             data.update(otp=otp)
#             header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#             proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
#             url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(oid) + "&v1=" + str(otp) + "&v2=" + str()
#             response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
#             request.session['otp'] = otp
#             return redirect('check_otp')

#         else:

#             messages.warning(request, "Mobile  number not exist kindly register first ")
#             return render(request, 'roof/index.html')
        
#     return render(request, 'roof/index.html')




# def check_otp(request):
#     print("ggggggjjjjjjjjjj")
#     if request.session.has_key('otp'):
#         if request.method == "POST":
#             otp = request.POST.get('otp')
#             print("fffffffff")
#             if otp == request.session['otp']:
#                 print("gggggggggggg")
#                 dash = roof_top_first.objects.get(otp=otp)
#                 mobile = dash.contact
#                 dash_data = roof_top_first.objects.get(contact=mobile)
#                 print("tttttttttttt")
#                 return render(request, 'roof/agent_Basic.html',{'userdata':dash_data})

#             else:
#                 messages.warning(request, "Otp not matched, Kindly enter valid otp")
#                 return render(request, 'roof/otp_verify.html')

#         return render(request, 'roof/otp_verify.html')
#     return render(request, 'roof/otp_verify.html')






def login_reg(request):
    if request.method == "POST":
        oid = request.POST.get('contact')
        zone = request.POST.get('zone')
        if roof_top_first.objects.filter(contact=oid,basic_details=1,user_zone=zone).exists():
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otp = generateOTP()
            Q = roof_top_first.objects.filter(contact=oid,user_zone=zone)
            Q.update(otp=otp)
            request.session['otp_two'] = otp
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(oid) + "&v1=" + str(otp) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = oid)
            sms_template.save()
            
            
            return redirect('/roof_top/check_otp')

        elif roof_top_first.objects.filter(contact=oid,basic_details=0,user_zone=zone).exists():
            data = roof_top_first.objects.filter(contact=oid)
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otp = generateOTP()
            # ca_data = roof_top_first(contact=oid,otp=otp)
            # ca_data.save()
            abc = roof_top_first.objects.filter(contact=oid,user_zone=zone)
            abc.update(otp=otp)
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(oid) + "&v1=" + str(otp) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = oid)
            sms_template.save()
            
            request.session['otp_one'] = otp
        
            return redirect('/roof_top/check_otp')

                            
        else:    
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otp = generateOTP()
            ca_data = roof_top_first(contact=oid,otp=otp,user_zone=zone)
            ca_data.save()
            
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(oid) + "&v1=" + str(otp) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = oid)
            sms_template.save()
            # send_mail(
            #     'Quality Monitoring Portal-Registration Complete',
            #     'Thank you for your Registration, your user id is your mobile number, please login to portal qcportal.mpcz.in',
            #     settings.EMAIL_HOST_USER,
            #     [email],
            #     fail_silently=False,
            # )
            request.session['otp_one'] = otp
            return redirect('/roof_top/check_otp')
    return render(request, 'roof/index.html')





def check_otp(request):
    if request.session.has_key('otp_two'):
        r = request.session['otp_two']
        # print(otp)
        print("gggggg")
        if request.method == "POST":
            otp = request.POST.get('otp')
            if otp == request.session['otp_two']:
                agent = roof_top_first.objects.filter(otp=request.session['otp_two'])
                request.session['otp_two'] = otp
                dash_data = roof_top_first.objects.get(otp=otp)
                mobile = dash_data.contact
                return render(request, 'roof/agent_Basic.html',{'userdata':dash_data,'mobile':mobile})

            else:
                messages.warning(request, "Otp not matched, Kindly enter valid otp")
                return render(request, 'roof/otp_verify.html')

    if request.session.has_key('otp_one'):
        print("xxxxxxxxx")
        if request.method == "POST":
            print("yyyyyyyyyy")
            otp = request.POST.get('otp')
            if otp == request.session['otp_one']:
                print("zzzzzzzzzzz")
                dash = roof_top_first.objects.get(otp=otp)
                mobile = dash.contact
                request.session['otp_one'] = otp
                request.session['Mobile'] = mobile
                # return redirect('reg')
                return render(request, 'roof/agent_first.html',{'mobile':mobile})

            else:
                messages.warning(request, "Otp not matched, Kindly enter valid otp")
                return render(request, 'roof/otp_verify.html')

    return render(request, 'roof/otp_verify.html')   
                    
    



def agent_base_rooftop(request):
    if request.session.has_key('otp_two'):
        aa = request.session['otp_two']
        dash = roof_top_first.objects.get(otp=aa)
        zone = aa.user_zone
        if zone=='CZ':
            rtcd_obj = root_top_cert_details.objects.get(id = dash.id)
            return render(request, 'roof/agentBase.html',{'userdata':dash, 'rtcd_obj':rtcd_obj})

        elif zone=='EZ':
            rtcd_obj = root_top_cert_details_ez.objects.get(id = dash.id)
            return render(request, 'roof/agentBase.html',{'userdata':dash, 'rtcd_obj':rtcd_obj})

        else:
            rtcd_obj = root_top_cert_details_wz.objects.get(id = dash.id)
            return render(request, 'roof/agentBase.html',{'userdata':dash, 'rtcd_obj':rtcd_obj})



def agent_certiticate(request):
    if request.session.has_key('otp_two'):
        aa = request.session['otp_two']
        dash = roof_top_first.objects.get(otp=aa)
        zone = aa.user_zone
        if zone=='CZ':
            rtcd_obj = root_top_cert_details.objects.get(id = dash.id)
            return render(request, 'roof/agentBase.html',{'userdata':dash, 'rtcd_obj':rtcd_obj})

        elif zone=='EZ':
            rtcd_obj = root_top_cert_details_ez.objects.get(id = dash.id)
            return render(request, 'roof/agentBase.html',{'userdata':dash, 'rtcd_obj':rtcd_obj})

        else:
            rtcd_obj = root_top_cert_details_wz.objects.get(id = dash.id)
            return render(request, 'roof/agentBase.html',{'userdata':dash, 'rtcd_obj':rtcd_obj})

def agent_basic(request):
    if request.session.has_key('otp_two'):
        aa = request.session['otp_two']
        dash = roof_top_first.objects.get(otp=aa)

        return render(request, 'roof/agent_Basic.html',{'userdata':dash})


def roof_top_upload(request):
    if request.session.has_key('otp_two'):
        if request.method == 'POST':
            data = roof_top_first.objects.get(otp=request.session['otp_two'])
            user_id = data.id
            zone = data.user_zone
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
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='A/B class Electrical License or Undertaking Document',
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


            document = request.FILES['sixteen']
            data1 = roof_top_sec(user_id=user_id, Types_of_Docs='Non Blacklisted Affidavit',
                                Ddocfile=document,Status=1)
            data1.save()


            data = roof_top_first.objects.filter(otp=request.session['otp_two'])
            data.update(profile_complete=1)
            return redirect('view_document')

           
        return render(request, 'roof/Agent2.html')
    
    


def view_document(request):
    if request.session.has_key('otp_two'):
        aa = roof_top_first.objects.get(otp=request.session['otp_two'])
        user_id = aa.id
        zone = aa.user_zone
        data = roof_top_sec.objects.filter(user_id=user_id)
        return render(request,'roof/view_document.html',{'data':data,'userdata':aa})

    return render(request,'roof/view_document.html')





def profile(request):
    if request.session.has_key('otp_two'):
        aa = roof_top_first.objects.get(otp=request.session['otp_two'])
        user_id = aa.id
        zone = aa.user_zone
        data = roof_top_sec.objects.filter(user_id=user_id)
        return render(request,'roof/vendor_view_profile.html',{'doc':data,'userdata':aa})

       

def rejected_doc(request):
    aaa = roof_top_first.objects.get(otp=request.session['otp_two'])
    user_id = aaa.id
    zone = aaa.user_zone
    data = roof_top_sec.objects.filter(Primary_verification_Status=2, user_id=user_id,Status=0) | roof_top_sec.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,Status=0)
    return render(request, 'roof/rejected_doc_resubmit.html', {"data": data,'userdata':aaa})


def rejected_doc_save(request, id):
    data = roof_top_first.objects.get(otp=request.session['otp_two'])
    user_id = data.id
    zone = data.user_zone
    data = roof_top_sec.objects.filter(id=id, user_id=user_id)
    if request.method == "POST":
        office = request.POST.get('office')
        if office != '':
            data.update(Issued_office_Name=office, Status=1)
        Document_Number = request.POST.get('doc_name')
        if Document_Number != '':
            data.update(Document_Number=Document_Number, Status=1)
    
    
        if len(request.FILES) != 0:
            data = roof_top_sec.objects.get(id=id, user_id=user_id)
            upload_file = request.FILES['file']
            data.Ddocfile = upload_file
            data.Status = 1
            data.save()

    if roof_top_sec.objects.filter(Primary_verification_Status=2, user_id=user_id,Status=0):
        
        return redirect('agent_basic')
    else:
            data1 = roof_top_first.objects.get(otp=request.session['otp_two'])
            data1.viewer_officer = 0
            data1.save()
    
    return render(request, 'roof/agentBase.html', {"data": data})

    




def rejected_doc_save_approver(request, id):
    data = roof_top_first.objects.get(otp=request.session['otp_two'])
    user_id = data.id
    zone = data.user_zone
    data = roof_top_sec.objects.filter(id=id, user_id=user_id)
    if request.method == "POST":
        office = request.POST.get('office')
        if office != '':
            data.update(Issued_office_Name=office, Status=1)
        Document_Number = request.POST.get('doc_name')
        if Document_Number != '':
            data.update(Document_Number=Document_Number, Status=1)
    
    
        if len(request.FILES) != 0:
            data = roof_top_sec.objects.get(id=id, user_id=user_id)
            upload_file = request.FILES['file']
            data.Ddocfile = upload_file
            data.Status = 1
            data.save()


    if roof_top_sec.objects.filter(Primary_verification_Status_approver=2, user_id=user_id,Status=0):
        
        return redirect('agent_basic')
    else:
        data1 = roof_top_first.objects.get(otp=request.session['otp_two'])
        data1.approver_officer = 0
        data1.save()

    
    return render(request, 'roof/agentBase.html', {"data": data})

        


import payu_sdk
import uuid

def roof_top_payment(request):
    if request.session.has_key('otp_two'):
        data = roof_top_first.objects.get(otp=request.session['otp_two'])
        productinfo="RoofTop Registration Fee"
      
        user_id = data.id
        zone = data.user_zone
        if zone=='CZ':
     
            txnid = uuid.uuid1()
            client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
            param = {"txnid": txnid, "amount": "2360.00", "productinfo": productinfo,
                    "firstname": data.name_of_auth,
                    "email": data.email}
            apiHash = payu_sdk.Hasher.generate_hash(param)
            data3 = payment_roof_top(user = data.id,Payu_Status='pending', Txdid=txnid,
                                    Productinfo="Registration",
                                    Firstname=data.name_of_auth, Contact_No=data.contact, Email_Id=data.email,
                                    Netamount_Debited='2360.00'
                                    )
            data3.save()


            return render(request, 'roof/payu_checkout_registration.html',
                        {"posted": apiHash, "txnid": txnid, "amount": "2360.00", 'firstname': data.name_of_auth,
                        "email": data.email, "productinfo": "RoofTop Registration Fee", "phone": data.contact})

        elif zone=='EZ':
            txnid = uuid.uuid1()
            client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
            param = {"txnid": txnid, "amount": "2360.00", "productinfo": productinfo,
                    "firstname": data.name_of_auth,
                    "email": data.email}
            apiHash = payu_sdk.Hasher.generate_hash(param)
            data3 = payment_roof_top(user = data.id,Payu_Status='pending', Txdid=txnid,
                                    Productinfo="Registration",
                                    Firstname=data.name_of_auth, Contact_No=data.contact, Email_Id=data.email,
                                    Netamount_Debited='2360.00'
                                    )
            data3.save()


            return render(request, 'roof/payu_checkout_registration.html',
                        {"posted": apiHash, "txnid": txnid, "amount": "2360.00", 'firstname': data.name_of_auth,
                        "email": data.email, "productinfo": "RoofTop Registration Fee", "phone": data.contact})

        else:
            txnid = uuid.uuid1()
            client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
            param = {"txnid": txnid, "amount": "2360.00", "productinfo": productinfo,
                    "firstname": data.name_of_auth,
                    "email": data.email}
            apiHash = payu_sdk.Hasher.generate_hash(param)
            data3 = payment_roof_top(user = data.id,Payu_Status='pending', Txdid=txnid,
                                    Productinfo="Registration",
                                    Firstname=data.name_of_auth, Contact_No=data.contact, Email_Id=data.email,
                                    Netamount_Debited='2360.00'
                                    )
            data3.save()


            return render(request, 'roof/payu_checkout_registration.html',
                        {"posted": apiHash, "txnid": txnid, "amount": "2360.00", 'firstname': data.name_of_auth,
                        "email": data.email, "productinfo": "RoofTop Registration Fee", "phone": data.contact})
    return render(request, 'roof/agent_Basic.html',{'userdata':data})





from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF
from paywix.payu import Payu
import os
from payu_sdk.API import paymentAPI
import json
import hashlib
import io
from rest_framework.parsers import JSONParser
import payu_sdk
import requests
@csrf_exempt
def payu_success_registration(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}

    #response = payu.verify_transaction(data)
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
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    date_for_sms = datetime.datetime.today()
    if Pgateway_Type == 'NB-PG':
        if payment_roof_top.objects.filter(Txdid=Txn_id).exists():
            Payudata = payment_roof_top.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            Payudata.Name_On_Card =  'Not Available'
            # Payudata.Cardnum =  'Not Available'
            Payudata.Payu_Status=Status
            Payudata.date = datetime.datetime.today()
            Payudata.save()

        elif payment_roof_top.objects.filter(Txdid=Txn_id).exists():
            Payudata = payment_roof_top.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            Payudata.Name_On_Card =  'Not Available'
            # Payudata.Cardnum =  'Not Available'
            Payudata.Payu_Status=Status
            Payudata.date = datetime.datetime.today()
            Payudata.save()

        elif payment_roof_top.objects.filter(Txdid=Txn_id).exists():
            Payudata = payment_roof_top.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            Payudata.Name_On_Card =  'Not Available'
            # Payudata.Cardnum =  'Not Available'
            Payudata.Payu_Status=Status
            Payudata.date = datetime.datetime.today()
            Payudata.save()
    else:
        if payment_roof_top.objects.filter(Txdid=Txn_id).exists():
            # Card_num = data['cardnum']
            Payudata = payment_roof_top.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            # Payudata.Cardnum = Card_num
            Payudata.Payu_Status=Status
            Payudata.date = datetime.datetime.today()
            Payudata.save()
        elif payment_roof_top.objects.filter(Txdid=Txn_id).exists():
            Payudata = payment_roof_top.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            # Payudata.Cardnum = Card_num
            Payudata.Payu_Status=Status
            Payudata.date = datetime.datetime.today()
            Payudata.save()

        elif payment_roof_top.objects.filter(Txdid=Txn_id).exists():
            Payudata = payment_roof_top.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            # Payudata.Cardnum = Card_num
            Payudata.Payu_Status=Status
            Payudata.date = datetime.datetime.today()
            Payudata.save()

    if payment_roof_top.objects.filter(Txdid=Txn_id).exists():
        data = payment_roof_top.objects.get(Txdid=Txn_id)
        user = roof_top_first.objects.get(id=data.user)
        user.user_code_uni=data.Txdid
        user.save()

        RegNum = "CZ2022"
        nabl_type = "00"
        tkc_type = "00"

        list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        s = ""
        s = s + "V" + RegNum + random.choice(list1) + random.choice(list1) + random.choice(list1) + random.choice(list1)
        model = roof_top_first.objects.filter(id=data.user)
        model.update(payment=1)
        Regdatashow = roof_top_first.objects.filter(id=data.user)
        # date = datetime.now()
        user = roof_top_first.objects.get(id=data.user)
        aaaa = roof_top_first.objects.filter(id=data.user)
        aaaa.update(payment=1)
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        key = 'GHeH7D'
        salt = 'DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ'
        command = 'verify_payment'
        toHash = {"command": command, "var1": Txn_id}
        apiHash = payu_sdk.Hasher.APIHash(toHash)
        Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
        #url = 'https://test.payu.in/merchant/postservice.php?form=2'
        proxyDictfd={"https":"proxy.mpcz.in:8080","http":"proxy.mpcz.in:8080"}
        response = requests.get(url,proxies=proxyDictfd)
        #r = requests.post(url, data=Poststring)
        url = "https://info.payu.in/merchant/postservice?form=2"
        headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        payload = "key=" + key + "&command=verify_payment&var1=" + Txn_id + "&hash=" + apiHash
        # res = requests.request("POST", url, data=payload, headers=headers)
        res = requests.request("POST", url,proxies=proxyDictfd, data=payload, headers=headers)

        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(Phone_no) + "&v1="+ str() + "&v2=" + str()
        response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007277348148394809',date = datetime.datetime.now(),mobile_number = Phone_no)
        sms_template.save()

        if res.status_code == 200:
            json_data = json.loads(res.text)
            if json_data['status'] == 1:
                transcation_details = json_data['transaction_details']
                transction_data = transcation_details[Txn_id]
                if transction_data['status'] == 'success':
                    payu_obj = payment_roof_top.objects.get(Txdid=Txn_id)
                    if transction_data['productinfo'] == "Registration":
                        user = roof_top_first.objects.get(userid=data.user)
                        user.activation_payment = 1
                        user.save()
                        return render(request, 'roof/payu_success.html',
                                    {'response': response, 'data': payu_obj})
            
                
                    request.session['Phone_no'] = Phone_no
                    sms = roof_top_first.objects.get(contact=Phone_no)
                    mobile = sms.contact
                    name_sms = sms.agency_name
                    sms_date = datetime.datetime.today()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str(name_sms) + "&v3=" + str('2360') + "&v4=" + str(
                        'Registration') + "&v5=" + str('Registration') + "&v6=" + str(sms_date) + "&v7=" + str(Bankrefnum)
                    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(Phone_no) + "&v1="+ str(First_name) + "&v2=" + str( ) +  "&v3=" + str('2360') +  "&v4=" + str('Solar Vendor Registration') +  "&v5=" + str( ) + "&v6=" + str(date_for_sms) + "&v7=" + str(Txn_id) 
                    # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})

                    return render(request, 'roof/payu_success.html', {'data': payu_obj,'Regdatashow':Regdatashow,})
        else:
            attempt_num += 1
            time.sleep(5)  # Wait for 5 seconds before re-trying

        request.session['Phone_no'] = Phone_no
        return render(request, 'roof/payu_success.html', {'response': response, 'data': payu_obj,'Regdatashow':Regdatashow,})
        User_Id = user.User_Id
        payu_obj = Payudata_main1.objects.get(Txdid=Txn_id)
        user = AllData.objects.get(userid=data.user)
        user.payment = 1
        user.save()
        return render(request, 'roof/payu_success.html',
                    {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
        payu_obj = Payudata_main1.objects.latest('User_Id')
        request.session['Phone_no'] = Phone_no
        sms = AllData.objects.get(userid=data.user)
        mobile = sms.ContactNo
        name_sms = sms.CompanyName_E
        sms_date = datetime.now()
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
    elif payment_roof_top.objects.filter(Txdid=Txn_id).exists():
        data = payment_roof_top.objects.get(Txdid=Txn_id)
        user = roof_top_first.objects.get(id=data.user)
        user.user_code_uni=data.Txdid
        user.save()

        RegNum = "CZ2022"
        nabl_type = "00"
        tkc_type = "00"

        list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        s = ""
        s = s + "V" + RegNum + random.choice(list1) + random.choice(list1) + random.choice(list1) + random.choice(list1)
        model = roof_top_first.objects.filter(id=data.user)
        model.update(payment=1)
        Regdatashow = roof_top_first.objects.filter(id=data.user)
        # date = datetime.now()
        user = roof_top_first.objects.get(id=data.user)
        aaaa = roof_top_first.objects.filter(id=data.user)
        aaaa.update(payment=1)
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        key = 'GHeH7D'
        salt = 'DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ'
        command = 'verify_payment'
        toHash = {"command": command, "var1": Txn_id}
        apiHash = payu_sdk.Hasher.APIHash(toHash)
        Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
        url = 'https://test.payu.in/merchant/postservice.php?form=2'
        proxyDictfd={"https":"proxy.mpcz.in:8080","http":"proxy.mpcz.in:8080"}
        response = requests.get(url,proxies=proxyDictfd)
        #r = requests.post(url, data=Poststring)
        #url = "https://info.payu.in/merchant/postservice?form=2"
        headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        payload = "key=" + key + "&command=verify_payment&var1=" + Txn_id + "&hash=" + apiHash
        # res = requests.request("POST", url, data=payload, headers=headers)
        res = requests.request("POST", url,proxies=proxyDictfd, data=payload, headers=headers)

        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(Phone_no) + "&v1="+ str() + "&v2=" + str()
        response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007277348148394809',date = datetime.datetime.now(),mobile_number = Phone_no)
        sms_template.save()
        

        if res.status_code == 200:
            json_data = json.loads(res.text)
            if json_data['status'] == 1:
                transcation_details = json_data['transaction_details']
                transction_data = transcation_details[Txn_id]
                if transction_data['status'] == 'success':
                    payu_obj = payment_roof_top.objects.get(Txdid=Txn_id)
                    if transction_data['productinfo'] == "Registration":
                        user = roof_top_first.objects.get(userid=data.user)
                        user.activation_payment = 1
                        user.save()
                        return render(request, 'roof/payu_success.html',
                                    {'response': response, 'data': payu_obj})
            
                
                    request.session['Phone_no'] = Phone_no
                    sms = roof_top_first.objects.get(contact=Phone_no)
                    mobile = sms.contact
                    name_sms = sms.agency_name
                    sms_date = datetime.datetime.today()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str(name_sms) + "&v3=" + str('2360') + "&v4=" + str(
                        'Registration') + "&v5=" + str('Registration') + "&v6=" + str(sms_date) + "&v7=" + str(Bankrefnum)
                    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(Phone_no) + "&v1="+ str(First_name) + "&v2=" + str( ) +  "&v3=" + str('2360') +  "&v4=" + str('Solar Vendor Registration') +  "&v5=" + str( ) + "&v6=" + str(date_for_sms) + "&v7=" + str(Txn_id) 
                    # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})

                    return render(request, 'roof/payu_success.html', {'data': payu_obj,'Regdatashow':Regdatashow,})
        else:
            attempt_num += 1
            time.sleep(5)  # Wait for 5 seconds before re-trying

        request.session['Phone_no'] = Phone_no
        return render(request, 'roof/payu_success.html', {'response': response, 'data': payu_obj,'Regdatashow':Regdatashow,})
        User_Id = user.User_Id
        payu_obj = Payudata_main1.objects.get(Txdid=Txn_id)
        user = AllData.objects.get(userid=data.user)
        user.payment = 1
        user.save()
        return render(request, 'roof/payu_success.html',
                    {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
        payu_obj = Payudata_main1.objects.latest('User_Id')
        request.session['Phone_no'] = Phone_no
        sms = AllData.objects.get(userid=data.user)
        mobile = sms.ContactNo
        name_sms = sms.CompanyName_E
        sms_date = datetime.now()
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
    elif payment_roof_top.objects.filter(Txdid=Txn_id).exists():
        data = payment_roof_top.objects.get(Txdid=Txn_id)
        user = roof_top_first.objects.get(id=data.user)
        user.user_code_uni=data.Txdid
        user.save()

        RegNum = "CZ2022"
        nabl_type = "00"
        tkc_type = "00"

        list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        s = ""
        s = s + "V" + RegNum + random.choice(list1) + random.choice(list1) + random.choice(list1) + random.choice(list1)
        model = roof_top_first.objects.filter(id=data.user)
        model.update(payment=1)
        Regdatashow = roof_top_first.objects.filter(id=data.user)
        # date = datetime.now()
        user = roof_top_first.objects.get(id=data.user)
        aaaa = roof_top_first.objects.filter(id=data.user)
        aaaa.update(payment=1)
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        key = 'GHeH7D'
        salt = 'DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ'
        command = 'verify_payment'
        toHash = {"command": command, "var1": Txn_id}
        apiHash = payu_sdk.Hasher.APIHash(toHash)
        Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
        url = 'https://test.payu.in/merchant/postservice.php?form=2'
        proxyDictfd={"https":"proxy.mpcz.in:8080","http":"proxy.mpcz.in:8080"}
        response = requests.get(url,proxies=proxyDictfd)
        #r = requests.post(url, data=Poststring)
        #url = "https://info.payu.in/merchant/postservice?form=2"
        headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        payload = "key=" + key + "&command=verify_payment&var1=" + Txn_id + "&hash=" + apiHash
        # res = requests.request("POST", url, data=payload, headers=headers)
        res = requests.request("POST", url,proxies=proxyDictfd, data=payload, headers=headers)

        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(Phone_no) + "&v1="+ str() + "&v2=" + str()
        response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007277348148394809',date = datetime.datetime.now(),mobile_number = Phone_no)
        sms_template.save()

        if res.status_code == 200:
            json_data = json.loads(res.text)
            if json_data['status'] == 1:
                transcation_details = json_data['transaction_details']
                transction_data = transcation_details[Txn_id]
                if transction_data['status'] == 'success':
                    payu_obj = payment_roof_top.objects.get(Txdid=Txn_id)
                    if transction_data['productinfo'] == "Registration":
                        user = roof_top_first.objects.get(userid=data.user)
                        user.activation_payment = 1
                        user.save()
                        return render(request, 'roof/payu_success.html',
                                    {'response': response, 'data': payu_obj})
            
                
                    request.session['Phone_no'] = Phone_no
                    sms = roof_top_first.objects.get(contact=Phone_no)
                    mobile = sms.contact
                    name_sms = sms.agency_name
                    sms_date = datetime.datetime.today()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(
                        mobile) + "&v1=" + str(name_sms) + "&v2=" + str(name_sms) + "&v3=" + str('2360') + "&v4=" + str(
                        'Registration') + "&v5=" + str('Registration') + "&v6=" + str(sms_date) + "&v7=" + str(Bankrefnum)
                    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007156373345234835&mobile_number=" + str(Phone_no) + "&v1="+ str(First_name) + "&v2=" + str( ) +  "&v3=" + str('2360') +  "&v4=" + str('Solar Vendor Registration') +  "&v5=" + str( ) + "&v6=" + str(date_for_sms) + "&v7=" + str(Txn_id) 
                    # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})

                    return render(request, 'roof/payu_success.html', {'data': payu_obj,'Regdatashow':Regdatashow,})
        else:
            attempt_num += 1
            time.sleep(5)  # Wait for 5 seconds before re-trying

        request.session['Phone_no'] = Phone_no
        return render(request, 'roof/payu_success.html', {'response': response, 'data': payu_obj,'Regdatashow':Regdatashow,})
        User_Id = user.User_Id
        payu_obj = Payudata_main1.objects.get(Txdid=Txn_id)
        user = AllData.objects.get(userid=data.user)
        user.payment = 1
        user.save()
        return render(request, 'roof/payu_success.html',
                    {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
        payu_obj = Payudata_main1.objects.latest('User_Id')
        request.session['Phone_no'] = Phone_no
        sms = AllData.objects.get(userid=data.user)
        mobile = sms.ContactNo
        name_sms = sms.CompanyName_E
        sms_date = datetime.now()
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
        

import datetime
@csrf_exempt
def payu_failure1(request):
    from datetime import date

    data = {k: v[0] for k, v in dict(request.POST).items()}
    # response = payu.verify_transaction(data)
 
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
    # Card_num = data['cardnum']
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    # date = datetime.now()
    if payment_roof_top.objects.filter(Txdid=Txn_id).exists():
        Payudata = payment_roof_top.objects.get(Txdid=Txn_id)
        Payudata.Payu_Moneyid = payu_moneyid
        Payudata.Hash_Id = Hash
        Payudata.Paymentgateway_Type = Pgateway_Type
        # Payudata.date = date
        Payudata.Bank_Ref_Num = Bankrefnum
        Payudata.Bankcode = Bank_code
        Payudata.date = datetime.datetime.today()
        # Payudata.Cardnum = Card_num
        Payudata.Payu_Status = 'Failure'
        Payudata.save()
    payu_obj = payment_roof_top.objects.get(Txdid=Txn_id)
    # user = payment_roof_top.objects.get(Contact_No=Phone_no)
    payu_obj.save()
   
    return render(request, 'roof/payment_fail.html', {'data': payu_obj})



def update_profile(request):
  
    data =roof_top_first.objects.get(otp=request.session['otp_two'])
    if request.method == "POST":    
        data =roof_top_first.objects.get(otp=request.session['otp_two'])
        data.user_type  = request.POST['one']
        data.agency_name  = request.POST['two']
        data.name_of_auth  = request.POST['three']
        data.address  = request.POST['four']
        data.gst  = request.POST['five']
        data.pan_card  = request.POST['six']
        data.email  = request.POST['seven']
        data.contact  = request.POST['eight']
        data.user_type  = request.POST['user_type']
        
        data.save()
        return redirect('agent_basic')
    
    return render(request, 'roof/update_vendor_profile.html',{"basic":data})


def view_loa(request):
    if request.session.has_key('otp_two'):
        aa = roof_top_first.objects.get(otp=request.session['otp_two'])
        user_id = aa.id
        zone = aa.user_zone
        if zone=='CZ':
            if roof_top_loa.objects.filter(user_id=user_id,approver=1).exists():
                loa = roof_top_loa.objects.filter(user_id=user_id,approver=1)
                return render(request,'roof/view_loa_vendor.html',{'data':loa})
            else:
                return render(request,'roof/not_uploaded_loa.html')

        elif zone=='EZ':
            if roof_top_loa_ez.objects.filter(user_id=user_id,approver=1).exists():
                loa = roof_top_loa_ez.objects.filter(user_id=user_id,approver=1)
                return render(request,'roof/view_loa_vendor.html',{'data':loa})
            else:
                return render(request,'roof/not_uploaded_loa.html')

        else:
            if roof_top_loa_wz.objects.filter(user_id=user_id,approver=1).exists():
                loa = roof_top_loa_wz.objects.filter(user_id=user_id,approver=1)
                return render(request,'roof/view_loa_vendor.html',{'data':loa})
            else:
                return render(request,'roof/not_uploaded_loa.html')


            
    return redirect('/')


from django.db.models import Count
def zone_wise(request):
    data_CZ = roof_top_first.objects.filter(user_zone='CZ').count()
    data_EZ = roof_top_first.objects.filter(user_zone='EZ').count()
    data_WZ = roof_top_first.objects.filter(user_zone='WZ').count()
    Sum = data_CZ+data_EZ+data_WZ
    print('CZ---------',data_CZ)
    print('EZ---------',data_EZ)
    print('WZ---------',data_WZ)
    print('sum--------',Sum)
    # data_CZ = roof_top_first.objects.all().annotate(count('user_zone',distinct=True))
    # data_CZ = roof_top_first.objects.values('user_zone').distinct().count()



    # data_CZ = roof_top_first.objects.values('user_zone').annotate(the_count=Count('user_zone'))
    # for a in data_CZ:
    #     print(a.get('user_zone'))
    #     print(a.get('the_count'))



    return HttpResponse('hello')


# ************************8api********************
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from django.http import HttpResponse
@api_view(['GET'])
def solar_vendor_all_list(request):
    response = Response()
    data = roof_top_first.objects.filter(approver_officer = '1',user_zone='CZ')
    serial = SolarUserData(data, many=True)
    response = serial.data
    return HttpResponse(json.dumps(response), content_type="application/json")



@api_view(['POST'])
def get_data_from_registration_no(request):
    response = Response()
    reg_no = request.POST.get('registration_no')
    if roof_top_first.objects.filter(registration_no=reg_no).exists():
        task = roof_top_first.objects.filter(registration_no=reg_no)
        test_data = SolarUserData(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': test_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")