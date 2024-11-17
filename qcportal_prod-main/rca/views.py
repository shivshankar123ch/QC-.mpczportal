from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from django.shortcuts import render
from .models import *
from main.models import *
from django.db.models import Q
from vendor.models import *


def rca_base(request):

    return render(request, 'rca/RCA_base.html')


def create_wo(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    rca_vendor = Rca_User_Registration.objects.filter(cgm_approval=1,digital_cert_upload=1,User_zone=officer.user_zone)
    return render(request, 'rca/create_wo.html', {"vendor": rca_vendor})


def rca_order(request):
    if request.method == "POST":
        vendor_det = request.POST.get('vendor')
        vendor_name = Rca_User_Registration.objects.get(CompanyName_E=vendor_det,cgm_approval=1)
        order = request.POST.get('order')
        dispatch_num = request.POST.get('dispatch_num')
        bid_open_date = request.POST.get('bid_open_date')
        ordr_date = request.POST.get('order_date')
        specific = request.POST.get('specific')
        officer = request.session['officer']
        officer = Officer.objects.get(employ_id= request.session['officer'])
        cell =RCA_Cell.objects.get(Region = officer.Region)
        work_info = WO_Info(rca_cell=cell,vendor_id=vendor_name, tendor_no=order, bid_open_date=bid_open_date, ordr_date=ordr_date,
                            dispatch_no=dispatch_num, wo_specification=specific)
        work_info.save()
        wo = WO_Info.objects.latest('id')
        return render(request, 'rca/add_schedule_wo.html', {'wo': wo})
    vendor_rca = Rca_User_Registration.objects.filter( User_type='VENDOR',cgm_approval=1)
    return render(request, 'rca/RCA_order.html', {'vendor': vendor_rca})


def rca_order_add_schedule(request, id):
    if request.method == "POST":
        sched = request.POST.get("sched_name")
        descip = request.POST.get("sched_desc")
        wo = WO_Info.objects.get(id=id)
        wo_sched = WO_Schedule_Info(schedule_id=wo, schedule_name=sched, description_name=descip)
        wo_sched.save()
        schedule = WO_Schedule_Info.objects.filter(schedule_id=wo)
        return render(request, 'rca/add_schedule_wo.html', {'wo': wo, "schedule": schedule})


def rca_order_add_copy_to(request, id):
    if request.method == "POST":
        sched = request.POST.get("copy")
        wo = WO_Info.objects.get(id=id)
        wo_sched = WO_Copy_Info(wo=wo, copy_name=sched)
        wo_sched.save()
        copy = WO_Copy_Info.objects.filter(wo=wo)
        return render(request, 'rca/rca_order_add_copy_to.html', {'wo': wo, "copy": copy})
    wo = WO_Info.objects.get(id=id)
    copy = WO_Copy_Info.objects.filter(wo=wo)
    return render(request, 'rca/rca_order_add_copy_to.html', {'wo': wo, "copy": copy})


from datetime import date
from fpdf import FPDF
import os


def rca_order_view(request, id):
    vd = WO_Info.objects.get(id=id)
    schedule = WO_Schedule_Info.objects.filter(schedule_id=vd)
    copy = WO_Copy_Info.objects.filter(wo=vd)
    today = date.today()
    # add=Rca_User_Registration.objects.get(User_Id=vd.vendor_id)
    return render(request, 'rca/rca_order_view.html',
                  {'vd': vd, 'copy': copy, 'date': today, 'schedule': schedule})


def rca_all_work_order(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    data = WO_Info.objects.filter(rca_cell=cell).order_by('-id')
    return render(request, 'rca/all_wo.html', {'data': data})


def rca_ro_create(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    data = WO_Info.objects.filter(rca_cell=cell,rca_bg_accept=1).order_by('-id')
    store = Store_Info.objects.filter(Region = officer.Region)
    return render(request, 'rca/RCA_release_order.html',
                  {'vd': data, 'store': store})


def rca_ro_add_material(request):
    if request.method == "POST":
        wo = request.POST.get("wo")
        store = request.POST.get("store")
        officer = Officer.objects.get(employ_id= request.session['officer'])
        order_date=date.today()
        cell =RCA_Cell.objects.get(Region = officer.Region)
        data = RO_Info(rca_cell=cell,wo=WO_Info.objects.get(id=wo), store=Store_Info.objects.get(id=store),ro_order_date=order_date)
        data.save()
        ro = RO_Info.objects.latest("id")
        return render(request, 'rca/RCA_ro_add_material.html', {'ro': ro})


def rca_ro_add_rating(request, id):
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        # rate = request.POST.get("rate")
        rating = request.POST.get("rating")
        description = request.POST.get('description')
        # total_rate = request.POST.get('total')
        ro = RO_Info.objects.get(id=id)
        # data = RO_Material_Info(ro=ro, quantity=quantity, rate=rate, rating=rating, description=description,
        #                         total_rate=total_rate)
        data = RO_Material_Info( ro=ro, quantity=quantity, rating=rating, description=description )
                               
        data.save()
        ro_m = RO_Material_Info.objects.filter(ro=ro)
        ro = RO_Info.objects.get(id=id)
        return render(request, 'rca/RCA_ro_add_material.html', {"ro_m": ro_m, "ro": ro})
    return render(request, 'rca/RCA_ro_add_material.html')


def rca_ro_order_add_schedule(request, id):
    if request.method == "POST":
        sched = request.POST.get("sched_name")
        descip = request.POST.get("sched_desc")
        ro = RO_Info.objects.get(id=id)
        ro_sched = RO_Schedule_Info(ro_id=ro, schedule_name=sched, description_name=descip)
        ro_sched.save()
    ro = RO_Info.objects.get(id=id)
    schedule = RO_Schedule_Info.objects.filter(ro_id=ro)
    return render(request, 'rca/add_schedule_ro.html', {'ro': ro, "schedule": schedule})


def rca_ro_order_add_copy_to(request, id):
    if request.method == "POST":
        sched = request.POST.get("copy")
        ro = RO_Info.objects.get(id=id)
        ro_sched = RO_Copy(ro=ro, copy_name=sched)
        ro_sched.save()
        copy = RO_Copy.objects.filter(ro=ro)
        return render(request, 'rca/rca_ro_order_add_copy_to.html', {'ro': ro, "copy": copy})
    ro = RO_Info.objects.get(id=id)
    copy = RO_Copy.objects.filter(ro=ro)
    return render(request, 'rca/rca_ro_order_add_copy_to.html', {'ro': ro, "copy": copy})


# def rca_ro_view(request, id):
#     vd = RO_Info.objects.get(id=id)
#     schedule = RO_Schedule_Info.objects.filter(ro_id=vd)
#     copy = RO_Copy.objects.filter(ro=vd)
#     ro_m = RO_Material_Info.objects.filter(ro=vd)
#     today = date.today()
#     return render(request, 'rca/RCA_ro_view.html',
#                   {'vd': vd, 'copy': copy, 'date': today, 'schedule': schedule, 'material': ro_m})

def rca_ro_view(request, id):
    vd = RO_Info.objects.get(id=id)
    schedule = RO_Schedule_Info.objects.get(ro_id=vd)
    copy = RO_Copy.objects.filter(ro=vd)
    ro_m = RO_Material_Info.objects.filter(ro=vd)
    return render(request, 'rca/RCA_ro_view.html',
                  {'vd': vd, 'copy1': copy, 'schedule': schedule, 'material': ro_m})


def rca_all_release_order(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    print("kkkkkkkkkkkkk",cell)
    data = RO_Info.objects.filter(rca_cell=cell).order_by("-id")
    # ro_m=RO_Material_Info.objects.all().order_by('-id')
    return render(request, 'rca/all_ro.html', {'data': data})


def all_oil_request(request):
    data = Oil_Request.objects.all()
    return render(request, 'rca/all_oil_request.html', {'data': data})


def oil_request_forward(request, id):
    data = Oil_Request.objects.get(id=id)
    data.rca_forward_to_as = 1
    data.save()
    data = Oil_Request.objects.all()
    return render(request, 'rca/all_oil_request.html', {'data': data})

def oil_request_forward_vendor(request, id):
    data = Oil_Request.objects.get(id=id)
    data.rca_forward_to_vendor = 1
    data.save()
    data = Oil_Request.objects.all()
    return render(request, 'rca/all_oil_request.html', {'data': data})



def RCA_dtr_issued(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    data = RO_Info.objects.filter(rca_cell=cell,digi_flag_ro=1).order_by("-id")
    return render(request,'rca/RCA_dtr_issued.html',{'data': data})

def rca_di_view(request, id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    return render(request, 'rca/rca_di_view.html',
                  {'ro': ro, "material": material, "xmr": xmr})

def rca_as_oil_confirmed(request):
    data = Oil_Request.objects.filter(rca_forward_to_as=1,as_forward_to_rca=1)
    return render(request,'rca/rca_as_oil_confirmed.html',{'data_info': data})

def rca_oilconfir_for_ven(request, id):
    data = Oil_Request.objects.get(id=id)
    data.rca_forward_to_vendor = 1
    data.save()
    data = Oil_Request.objects.all()
    return render(request, 'rca/rca_as_oil_confirmed.html', {'data_info': data})

def RCA_di_issue(request):
    data = RO_Info.objects.all()
    return render(request,'rca/RCA_di_issue.html',{'data': data})

def RCA_di_issue_view(request,id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo=material_offer.objects.filter(ro_id=ro) 
    
    

    return render(request, 'rca/RCA_di_issue_view.html', {'ro': ro, "material": material, "xmr": xmr,'mo':mo})

def RCA_di_issue_accept(request,id):
    data = material_offer.objects.get(id=id)
    data.issue_di = 1
    data.save()
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo=material_offer.objects.filter(id=id) 
    
    
    return render(request, 'rca/RCA_di_issue_view.html', {'ro': ro, "material": material, "xmr": xmr,'mo':mo})


def rca_allotment(request):
    return render(request, 'rca/RCA_allotment.html')


def rca_as(request):
    return render(request, 'rca/RCA_as.html')


def rca_di(request):
    return render(request, 'rca/RCA_di.html')


def rca_inspection_officer_base(request):
    return render(request, 'rca/RCA_inspection_officer_base.html')


def rca_inspection_complete(request):
    return render(request, 'rca/RCA_inspection_complete.html')


def rca_inspection_pending(request):
    return render(request, 'rca/RCA_inspection_pending.html')


def rca_inspection_pending2(request):
    return render(request, 'rca/RCA_inspection_pending2.html')


def rca_vendor_base(request):
    return render(request, 'rca/RCA_vendor_base.html')


def rca_acceptance(request):
    return render(request, 'rca/RCA_acceptance.html')


def rca_release_ack(request):
    return render(request, 'rca/RCA_release_ack.html')


def rca_repair_ue(request):
    return render(request, 'rca/RCA_repair_ue.html')


def rca_to_as(request):
    return render(request, 'rca/RCA_to_as.html')
    
    
import random
import math
import requests
from django.contrib import messages
def rca_login(request):
    if request.method == "POST":
        mobile = request.POST.get('contact')
        zone = request.POST.get('zone')
        if Rca_User_Registration.objects.filter(ContactNo=mobile,User_zone=zone).exists():
            def generateOTP():
                OTP = ""
                digits = "0123456789"
                for i in range(6):
                    OTP += digits[math.floor(random.random() * 10)]
                return OTP
            otp = generateOTP()
            Q = Rca_User_Registration.objects.filter(ContactNo=mobile,User_zone=zone)
            Q.update(Otp=otp)
            request.session['otp_two'] = otp
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
            response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = mobile)
            sms_template.save()
            
            # messages.warning(request, "Mobile number already registered")
            return render(request, 'rca/check_otp.html')

        else:
            messages.warning(request, "Mobile Number Not Register For Selected Discom Zone")
            return render(request, 'rca/rca_login.html')

    return render(request, 'rca/rca_login.html')


def check_otp(request):
    if request.session.has_key('otp_two'):
        r = request.session['otp_two']
        if request.method == "POST":
            otp = request.POST.get('otp')
            if otp == request.session['otp_two']:
                agent = Rca_User_Registration.objects.filter(Otp=request.session['otp_two'])
                request.session['otp_two'] = otp
                dash_data = Rca_User_Registration.objects.get(Otp=otp)
                mobile = dash_data.ContactNo
                return render(request, 'rca/basic_rca.html',{'userdata':dash_data,'mobile':mobile})

            else:
                messages.warning(request, "Otp not matched, Kindly enter valid otp")
                return render(request, 'rca/check_otp.html')

        return render(request, 'rca/check_otp.html')
    return redirect('/')




def upload_docs(request):
    if request.session.has_key('otp_two'):
        if request.method == "POST":
            agent = Rca_User_Registration.objects.filter(Otp=request.session['otp_two'])
            otp = request.session['otp_two'] 
            dash_data = Rca_User_Registration.objects.get(Otp=otp)
            user_id = dash_data.User_Id

            number = request.POST.get('one')
         
            file = request.FILES['four']

            data = Rca_Vendor_Document(user_id=user_id,Types_of_Docs='Electricity Connection of Firm/Company’s Premise(Latest month bill)',Document_Number=number,Ddocfile=file)
            data.save()

            number = request.POST.get('five')
         
            file = request.FILES['eight']

            data = Rca_Vendor_Document(user_id=user_id,Types_of_Docs='List of Plant and Machineries',Document_Number=number,Ddocfile=file)
            data.save()

            number = request.POST.get('nine')
        
            file = request.FILES['twelve']

            data = Rca_Vendor_Document(user_id=user_id,Types_of_Docs='List of Testing Equipment’s',Document_Number=number,Ddocfile=file)
            data.save()

            number = request.POST.get('thrteen')
         
            file = request.FILES['sixteen']

            data = Rca_Vendor_Document(user_id=user_id,Types_of_Docs='Calibration Certificate for Testing Equipment’s',Document_Number=number,Ddocfile=file)
            data.save()

            data = Rca_User_Registration.objects.filter(Otp=request.session['otp_two'])
            data.update(profile_complete=1)

            return redirect('/rca/view_document')

        return render(request, 'rca/rca_documet.html')

    return redirect('/')

    

def view_document(request):
    if request.session.has_key('otp_two'):
        agent = Rca_User_Registration.objects.filter(Otp=request.session['otp_two'])
        otp =request.session['otp_two']
        dash_data = Rca_User_Registration.objects.get(Otp=otp)
        user_id = dash_data.User_Id
        document = Rca_Vendor_Document.objects.filter(user_id=user_id)
        return render(request,'rca/view_document.html',{'document':document})
    return redirect('/')


import payu_sdk
import uuid

def rca_payment(request):
    if request.session.has_key('otp_two'):
        data = Rca_User_Registration.objects.get(Otp=request.session['otp_two'])
        productinfo="RCA Vender Registration and Factory Inspection Fee"
      
        user_id = data.User_Id
        zone = data.User_zone
     
        txnid = uuid.uuid1()
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        param = {"txnid": txnid, "amount": "14160.00", "productinfo": productinfo,
                "firstname": data.Authorised_person_E,
                "email": data.Email_Id}
        apiHash = payu_sdk.Hasher.generate_hash(param)
        data3 = payment_rca(user = data.User_Id,Payu_Status='pending', Txdid=txnid,
                                Productinfo="RCA Vender Registration and Factory Inspection Fee",
                                Firstname=data.Authorised_person_E, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                                Netamount_Debited='14160.00', company_name=data.CompanyName_E
                                )
        data3.save()


        return render(request, 'rca/payu_checkout_registration.html',
                    {"posted": apiHash, "txnid": txnid, "amount": "14160.00", 'firstname': data.Authorised_person_E,
                    "email": data.Email_Id, "productinfo": "RCA Vender Registration and Factory Inspection Fee", "phone": data.ContactNo, "company_name":data.CompanyName_E})



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
import datetime
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
        if payment_rca.objects.filter(Txdid=Txn_id).exists():
            Payudata = payment_rca.objects.get(Txdid=Txn_id)
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
        if payment_rca.objects.filter(Txdid=Txn_id).exists():
            # Card_num = data['cardnum']
            Payudata = payment_rca.objects.get(Txdid=Txn_id)
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
     

    if payment_rca.objects.filter(Txdid=Txn_id).exists():
        data = payment_rca.objects.get(Txdid=Txn_id)
      

        RegNum = "CZ2022"
        nabl_type = "00"
        tkc_type = "00"

        list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        s = ""
        s = s + "V" + RegNum + random.choice(list1) + random.choice(list1) + random.choice(list1) + random.choice(list1)
        Regdatashow = Rca_User_Registration.objects.filter(User_Id=data.user)
        Regdatashow.update(payment=1, factory_approval_payment = 1)
        # if Regdatashow[0].User_code == 'RCA(Regular)':
            # Regdatashow.update(provision_fi=1)
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        key = 'GHeH7D'
        salt = 'DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ'
        command = 'verify_payment'
        toHash = {"command": command, "var1": Txn_id}
        apiHash = payu_sdk.Hasher.APIHash(toHash)
        Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
        #url = 'https://test.payu.in/merchant/postservice.php?form=2'
        proxyDictfd={"https":"proxy.mpcz.in:8080","http":"proxy.mpcz.in:8080"}
        url = "https://info.payu.in/merchant/postservice?form=2"
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
                    payu_obj = payment_rca.objects.get(Txdid=Txn_id)
                    if transction_data['productinfo'] == "RCA Vender Registration and Factory Inspection Fee":
                        # user = payment_rca.objects.get(user=data.user)
                        # user.activation_payment = 1
                        # user.save()
                        return render(request, 'rca/success_rca.html',
                                    {'response': response, 'data': payu_obj})
            
                
                    request.session['Phone_no'] = Phone_no
                    sms = Rca_User_Registration.objects.get(ContactNo=Phone_no)
                    mobile = sms.ContactNo
                    name_sms = sms.CompanyName_E
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

                    return render(request, 'rca/success_rca.html', {'data': payu_obj,'Regdatashow':Regdatashow,})
        else:
            attempt_num += 1
            time.sleep(5)  # Wait for 5 seconds before re-trying

        request.session['Phone_no'] = Phone_no
        return render(request, 'rca/success_rca.html', {'response': response, 'data': payu_obj,'Regdatashow':Regdatashow,})
        User_Id = user.User_Id
        payu_obj = Payudata_main1.objects.get(Txdid=Txn_id)
        user = AllData.objects.get(userid=data.user)
        user.payment = 1
        user.save()
        return render(request, 'rca/success_rca.html',
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



def update_profile(request):
  
    data =Rca_User_Registration.objects.get(Otp=request.session['otp_two'])
    if request.method == "POST":    
        data =Rca_User_Registration.objects.get(Otp=request.session['otp_two'])
        data.Authorised_person_E  = request.POST['one']
        data.CompanyName_E  = request.POST['two']
        data.ContactNo  = request.POST['three']
        data.Email_Id  = request.POST['four']
        data.Company_Gst_No  = request.POST['five']
        data.Company_Pan_No  = request.POST['six']
        data.Aadhar  = request.POST['seven']
        data.Company_Gumastha_No  = request.POST['eight']
        
        data.save()
        return redirect('/rca/rca_basic')
    
    return render(request, 'rca/update_vendor_profile.html',{"basic":data})



def rca_basic(request):
    if request.session.has_key('otp_two'):
        aa = request.session['otp_two']
        dash = Rca_User_Registration.objects.get(Otp=aa)

        return render(request, 'rca/basic_rca.html',{'userdata':dash})
        
        
def payment_dis(request):
    if request.session.has_key('otp_two'):
        return render(request, 'rca/payment_dis.html')

    return redirect('/rca/rca_basic')

def certificate_details(request):
    if request.session.has_key('otp_two'):
        aa = request.session['otp_two']
        dash = Rca_User_Registration.objects.get(Otp=aa)
        if dash.cert:
            dash = Rca_User_Registration.objects.get(Otp=aa)
            return render(request, 'rca/certificate.html',{'userdata':dash})
        else:
            return HttpResponse('Profile Under Review')

    return redirect('/rca/rca_basic')

def rca_ven_bg_order_list(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    data = WO_Info.objects.filter(rca_cell=cell,rca_bg_submitted=1).order_by('-id')
    print("kkkkkkkkkkkkkk",data) 
    return render(request,'rca/rca_ven_bg_order_list.html', {'data': data})
	
def rca_ven_bg_confirm(request,id):
    data=WO_Info.objects.get(id=id,rca_bg_submitted=1)
    if data.rca_bg_accept==1:
        data=WO_Info.objects.get(id=id,rca_bg_submitted=1)
        return render(request,'rca/rca_ven_bg_confirm_save.html',{'data':data})
    elif data.rca_bg_accept==-1:
        data=WO_Info.objects.get(id=id,rca_bg_submitted=1)
        return render(request,'rca/rca_ven_bg_confirm_save.html',{'data':data})
    else:
        if request.method == "POST":
            data = WO_Info.objects.get(id=id,rca_bg_submitted=1)
            rem = request.POST.get("remark")
            data.rca_bg_remark=rem
            data.rca_bg_remark_flag=1
            data.save()
            data = WO_Info.objects.get(id=id,rca_bg_submitted=1)
            if request.POST.get("options1") == "ok":
                bg_accept_letter = request.FILES['bg_acceptance_let']
                data.bg_acceptance_letter=bg_accept_letter
                data.rca_bg_accept=1
                data.rca_bg_remark_flag=0
            elif request.POST.get("options1") == "not_ok":
                data.rca_bg_accept=-1
                data.rca_bg_status=0
            data.save()
            data = WO_Info.objects.get(id=id,rca_bg_submitted=1)
            return render(request,'rca/rca_ven_bg_confirm_save.html',{'data':data})

        data=WO_Info.objects.get(id=id,rca_bg_submitted=1)
        return render(request,'rca/rca_ven_bg_confirm.html',{'data':data})


    data=WO_Info.objects.get(id=id,rca_bg_submitted=1)
    return render(request,'rca/rca_ven_bg_confirm_save.html',{'data':data})


def rca_ven_dtr_dis_order_list(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    # data = RO_Info.objects.filter(rca_cell=cell,digi_flag_ro=1).order_by("-id")
    data = RO_Info.objects.filter(rca_cell=cell,digi_flag_ro=1,ro_ven_dis_flag=1).order_by("-ro_ven_dis_date")
    return render(request,'rca/rca_ven_dtr_dis_order_list.html',{'data': data})
	
def rca_ven_dtr_dis(request, id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro,vendor_send=1)
    material = RO_Material_Info.objects.filter(ro_id=ro)

    mat_list=[]
    xmr_quant=[]

    for mat in material:
        mat_list.append(mat.rating)

        xmr_dis=RO_Material_XMR_Info.objects.filter(material=mat,vendor_send=1).count()
        xmr_quant.append(xmr_dis)

    
    dis_zip=zip(mat_list,xmr_quant)


    report=material_offer.objects.filter(ro=ro)
    
    return render(request, 'rca/rca_ven_dtr_dis.html',
                  {'ro': ro, "material": material, "xmr": xmr,"rep":report,"dispatch":dis_zip})    


def approved_vendor_list_rca_cell(request):
    data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',cgm_approval=1,digital_cert_upload=1,blacklisted=0)
    address = []
 
    for j in data:
        add = UserCompanyDataMain.objects.filter(user_id_id = j).last()
        address.append(add)

    final_lst = zip(data,address)
    return render(request, 'rca/all_vendor_details_rca_cell.html', {'data':data,'final_lst':final_lst})
   
    
   
def vendor_check_material_rca_cell(request,id):
    data = User_Registration.objects.get(User_Id = id)
    material = Vendor_Material_Details.objects.filter(user_id = data)
    list_data = []
    for i in material:
        list_data.append(i.Material_Name)

    if request.method =="POST":
        get_data_value= request.POST.get('get_data_value')
        value_data = Vendor_Material_Details.objects.filter(user_id = data,Material_Name=get_data_value)
        return render(request, 'rca/vendor_all_material_rca_cell.html', {'data':value_data}) 
    return render(request, 'rca/view_vendor_material_rca_cell.html', {'data':set(list_data),'id':id})   

def vendor_basic_details_rca_cell(request,id):
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
    return render(request, 'rca/vendor_basic_details_rca_cell.html',
                {'data': data_new, 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material,
                'tech_data': tech_data, 
                 'CompanyData': CompanyData1,
                'AuthorisedPerson1': AuthorisedPerson1,
                #'BankDetails': BankDetails1, 'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech,
                'tech_data': tech_data, 'apprisal': apprisal, 'fi_tech': fi_tech,
                'fac_image': fac_image})






#.......................... additional bg rca lok code...............................




def add_bg_order_list(request):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    cell =RCA_Cell.objects.get(Region = officer.Region)
    bg_lst=[]
    data = Multiple_Bg.objects.filter(add_bg_submitted=1).order_by('-id')
    for i in data:
        i.wo.rca_cell==cell
        bg_lst.append(i)
    return render(request,'rca/add_bg_order_list.html', {'data': bg_lst})



def additional_bg_confirm(request,id):
    officer = Officer.objects.get(employ_id= request.session['officer'])
    data=Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
    
    if data.add_bg_accept==1:
        data=Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
        return render(request,'rca/add_bg_confirm_save.html',{'data':data})
    elif data.add_bg_accept==-1:
        data=Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
        return render(request,'rca/add_bg_confirm_save.html',{'data':data})
    else:
        if request.method == "POST":
            data = Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
            rem = request.POST.get("remark")
            data.add_bg_remark=rem
            data.add_bg_remark_flag=1
            data.save()
            data = Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
            if request.POST.get("options1") == "ok":
                bg_accept_letter = request.FILES['bg_acceptance_let']
                data.add_bg_acceptance_letter=bg_accept_letter
                data.add_bg_accept=1
                data.add_bg_remark_flag=0
            elif request.POST.get("options1") == "not_ok":
                data.add_bg_accept=-1
                data.add_bg_status=0
            data.save()
            data = Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
            return render(request,'rca/add_bg_confirm_save.html',{'data':data})

        data= Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
        return render(request,'rca/add_bg_confirm.html',{'data':data})


    data= Multiple_Bg.objects.get(id=id,add_bg_submitted=1)
    return render(request,'rca/add_bg_confirm_save.html',{'data':data})
   
    
    
    #............................................................................................
    
    
    
    
    
########################## As_Circle_Officer_Dashboard ##########################

def rca_as_circle_wo(request):
    if request.session.has_key('employ_login_id'):
        officer = Officer.objects.get(employ_id= request.session['officer'])
        wo=WO_Info.objects.filter(rca_cell__Discom=officer.Discom)
        return render(request,'rca/rca_as_circle_wo.html',{'data':wo})     
    return redirect('/')
    
def rca_as_circle_ro(request):
    if request.session.has_key('employ_login_id'):
        officer = Officer.objects.get(employ_id= request.session['officer'])
        ro=RO_Info.objects.filter(rca_cell__Discom=officer.Discom)
        return render(request,'rca/rca_as_circle_ro.html',{'data':ro})
    return redirect('/')


def rca_as_circle_issue(request):
    if request.session.has_key('employ_login_id'):
        officer = Officer.objects.get(employ_id= request.session['officer'])
        ro=RO_Info.objects.filter(rca_cell__Discom=officer.Discom)
        return render(request,'rca/rca_as_circle_issue.html',{'data':ro})
    return redirect('/')
    


def rca_as_circle_inward(request,id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)   
    return render(request,'rca/rca_as_circle_inward.html',{'data': xmr})
