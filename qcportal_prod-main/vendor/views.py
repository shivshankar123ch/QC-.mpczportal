from paywix.payu import Payu
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q
from .forms import EmployeeForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from main.models import *
from django.contrib import messages
from vendor.models import *
from po.models import *
from vendor.serializer import Vendor_Financial_Details_Serializer
import json
import psycopg2
from django.conf import settings
from django.core.mail import send_mail
from rca.models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from datetime import datetime as dtm

# Create your views here.
def base(request):
    return render(request, 'vendor/vendor_base.html')

import cx_Oracle
def snipped(request):
    print("ghhhhhhghghgh")
    
    # cx_Oracle.init_oracle_client(lib_dir=r"\lib\python3.8")
    # comm = cx_Oracle.connect("qc_user/qc_user@172.24.100.146:1525/TEST")
    comm = cx_Oracle.connect('qc_user/qc_user@172.24.100.146:1525/TEST')
    print("ffffffffffffffff",comm)

    cur = comm.cursor()
    cur.execute("SELECT * from qc_user.QC_VENDOR_SITE_MASTER")
    all = cur.fetchall()
    print("aaaaaa",all)
    return HttpResponse(all)

def update_profile(request):
  
    data =User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    userid = data.User_Id
    abcde = UserCompanyDataMain.objects.get(user_id_id=data)
    if data.profile_update_fee == 1 or data.cgm_approval == 0 :
        if request.method == "POST":
            data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
            abc = UserCompanyDataMain.objects.get(user_id_id=data)
            data1 =User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            # data1.Type_of_business=request.POST['two']
            # data1.CompanyName_E=request.POST['four']
            # data1.Authorised_person_E=request.POST['five']
            data1.ContactNo=request.POST['six']
            data1.Email_Id=request.POST['seven']
            # data1.User_zone=request.POST['zero']
            data1.save()
            abc.Company_Pan_No  = request.POST['eight']
            abc.Company_Gumastha_No  = request.POST['nine']
            abc.Company_Gst_No  = request.POST['ten']
            # abc.Registration_Date  = request.POST['eleven']
            abc.Company_Fax  = request.POST['twelve']
            # **********
         
            abc.Company_add_1  = request.POST['thireteen']
            abc.Company_add_2  = request.POST['fourteen']
            abc.Company_pin_code  = request.POST['fifteen']
            abc.Company_dist  = request.POST['sixteen']
            abc.Company_state  = request.POST['seventeen']
            abc.Company_t_add_1  = request.POST['eighteen']
            abc.Company_t_add_2  = request.POST['nineteen']
            abc.Company_t_pin_code  = request.POST['twenty']
            abc.Company_t_dist  = request.POST['twentyone']
            abc.Company_t_state  = request.POST['twentytwo']
            abc.save()
            return redirect('/vendor/basic')
    else:
        return render(request,'vendor/updateProfileStatus.html')
    return render(request, 'vendor/update_vendor_profile.html',{"basic":data,'company':abcde})




def updatedata(request):
    return render(request, 'vendor/update.html')


def message(request):
    return render(request, 'vendor/message.html')


def basic(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    payu_count = Payudata_main.objects.filter(Contact_No=data.ContactNo).count()
    doc = Vendor_Document.objects.filter(user_id=data.User_Id)

    doc1 = Vendor_BalanceSheet.objects.filter(user_id=data.User_Id)

    fac = Vendor_Factory_Details.objects.filter(user_id=data.User_Id)
    Material = Add_material.objects.filter(user_id=data.User_Id)
    
    return render(request, 'vendor/basicinfo.html', {'payu_count':payu_count,'userdata': data, 'doc': doc, 'doc1': doc1, 'factory': fac, 'Material': Material})


def vendor_reg_seven(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)

            if data1.page_12:
                return redirect("vendor_reg_fifteen")

            if data1.page_11:
                return redirect("vendor_reg_twelve")
            
            if data1.page_9:
                return redirect("vendor_reg_eleven")

            if data1.page_10:
                return redirect("employees-list")

            if data1.page_8:
                return redirect("vendor_reg_ten")
              
       
        return render(request, 'vendor/vendor_reg7.html')
    data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    payu_count = Payudata_main.objects.filter(Contact_No=data.ContactNo).count()
    return render(request, 'vendor/vendor_reg7.html',{"userdata": data11[0],'payu_count':payu_count})


def vendor_reg_eight(request):
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data.Experience = request.POST.get('work_experience')
        data.Turnover = request.POST.get('turn_over')
        data.save()
        if User_Registration_Check_Status.objects.filter(User=data).exists():
              data1 = User_Registration_Check_Status.objects.get(User=data)
              data1.page_8 = 1
              data1.save()
        else:
            user = User_Registration_Check_Status(User=data,page_8=1)
            user.save()
        return redirect("vendor_reg_ten")
    return render(request, 'vendor/vendor_reg8.html')


def vendor_reg_nine(request):
    if request.method == "POST":
        return redirect("vendor_reg_ten")
    return render(request, 'vendor/vendor_reg9.html')


def vendor_reg_ten(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    pan_details = UserCompanyDataMain.objects.get(user_id_id = data.User_Id)
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        pan_details = UserCompanyDataMain.objects.get(user_id_id = data.User_Id)

        try:

            reg_number = request.POST.get('one')
            issu_date = request.POST.get('two')
            # end_date = request.POST.get('three')
            v_upload_file_factory2 = request.FILES['todays']
            data1 = Vendor_Document(user_id=user_id, Types_of_Docs='NSIC/MSME/DIC REGISTRATION', Document_Number=reg_number,
                                    Doc_issue_date=issu_date, Ddocfile=v_upload_file_factory2,
                                    Status=1,Primary_verification_Status=3)
            data1.save()

        except Exception as e:
            pass

        # name = request.POST.get('four')
        # number = request.POST.get('five')
        # issu_date = request.POST.get('six')
        # v_upload_file_factory3 = request.FILES['new']
        # data1 = Vendor_Document(user_id=user_id, Types_of_Docs='AADHAR CARD(Proprietor/Director/Partner/Authorised Person)', Name_on_Document=name,
        #                         Document_Number=number, Status=1,Ddocfile=v_upload_file_factory3,
        #                         Doc_issue_date=issu_date)
        # data1.save()

        try:
            reg_number = request.POST.get('seven')
            end_date = datetime.now()
            upload = request.FILES['hello']
            data1 = Vendor_Document(user_id=user_id, Types_of_Docs='PROOF OF FIRM/COMPANY/ENTITY REGISTRATION',
                                    Document_Number=reg_number, Ddocfile=upload,
                                    Doc_expiry_date=end_date, Status=1)
            data1.save()
        except Exception as e:
            reg_number = request.POST.get('seven')
            upload = request.FILES['hello']
            data1 = Vendor_Document(user_id=user_id, Types_of_Docs='PROOF OF FIRM/COMPANY/ENTITY REGISTRATION',
                                    Document_Number=reg_number, Ddocfile=upload,
                                    Status=1)
            data1.save()


        name = request.POST.get('ten')
        number = request.POST.get('eleven')

        # try:
        #     upload = request.FILES['twelve']
        #     data1 = Vendor_Document(user_id=user_id, Types_of_Docs='FATHER AADHAR CARD DETAILS', Name_on_Document=name,
        #                             Document_Number=number, Ddocfile=upload, Status=1)
        #     data1.save()
        # except Exception as e:
        #     data1 = Vendor_Document(user_id=user_id, Types_of_Docs='FATHER ADHAAR CARD', Name_on_Document=name,
        #                             Document_Number=number, Status=1)
        #     data1.save()
        try:
            number = request.POST.get('sixteen')
            # upload = request.FILES['seventeen']
            
            data1 = Vendor_Document(user_id=user_id, Types_of_Docs='FACTORY LICENSE NUMBER DETAILS', Document_Number=number,
                                    Status=1)
            data1.save()

        except Exception as e:
            pass
        # try:
        #     land = request.POST.get('nineteen')
        #     working_shift = request.POST.get('twenty')
        #     area_of_factroy = request.POST.get('twenty_one')
        #     capacity = request.POST.get('twenty_two')
        #     firm_photo = request.POST.get('twenty_three')
        #     data1 = Vendor_Factory_Details(user_id=user_id, Area_of_land=land, No_of_Shifts=working_shift,
        #                                 Area_built_up=area_of_factroy, Production_Capacity=capacity, Ddocfile=firm_photo,
        #                                 Status=1)
        #     data1.save()
        # except Exception as e:
        #     firm_photo = request.POST.get('twenty_three')
        #     data1 = Vendor_Factory_Details(user_id=user_id, Ddocfile=firm_photo,Status=1)
        #     data1.save()
        
        if User_Registration_Check_Status.objects.filter(User=data).exists():
              data1 = User_Registration_Check_Status.objects.get(User=data)
              data1.page_10 = 1
              data1.save()
        else:
            user = User_Registration_Check_Status(User=data,page_10=1)
            user.save()

        return redirect('employees-list')
    return render(request, 'vendor/vendor_reg10.html',{'pan_details':pan_details})
def vendor_reg_eleven(request):
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        # material = request.POST.get('one')
        # material_specification = request.POST.get('two')
        # tests_reports = request.FILES['three']
        # gtp_and_drawing = request.FILES['four']
        # other_file = request.FILES['five']
        # data1 = Vendor_Material_Details(user_id=user_id, Material_Name=material,
        #                                 Material_Specification=material_specification,
        #                                 Material_Test_Doc=tests_reports, Material_GTP_Doc=gtp_and_drawing,
        #                                 Material_Other_Doc=other_file, Status=1)
        # data1.save()

        # office_name = request.POST.get('six')
        # number = request.POST.get('seven')
        upload = request.FILES['eight']
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='PRIVIOUS SUPPLY ORDER COPIES/COMPLETION CERTIFICATE REQUIRED',
                                         Document_Doc=upload, Status=1)

        data1.save()

        upload = request.FILES['nine']
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='LIST OF PLANTS and MACHINERIES',
                                         Document_Doc=upload, Status=1,Primary_verification_Status=3)
        data1.save()

        upload = request.FILES['ten']
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='LIST OF TESTING EQUIPMENT',
                                         Document_Doc=upload, Status=1,Primary_verification_Status=3)
        data1.save()

        upload = request.FILES['eleven']
        
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='CALIBRATION CERTIFICATE FOR ALL TESTING EQUIPMENT(shall be cross verify during factory inspection',
                                         Document_Doc=upload, Status=1)
        data1.save()

      

        number = request.POST.get('fourteen')
        try:
            upload = request.FILES['fifteen']
            data1 = Vendor_Technical_Details(
                user_id=user_id, Document_Number=number, Types_of_Docs='BIS LICENCE', Document_Doc=upload, Status=1,Primary_verification_Status=3)
            data1.save()
        except Exception as e:
            data1 = Vendor_Technical_Details(Types_of_Docs='BIS LICENCE',
                user_id=user_id, Status=1,Primary_verification_Status=3)
            data1.save()

        number = request.POST.get('eighteen')
        upload = request.FILES['nineteen']
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='INTERNAL QUALITY PLAN OF VENDOR FIRM',
                                         Document_Doc=upload, Document_Number=number, Status=1,Primary_verification_Status=3)
        data1.save()

        number = request.POST.get('twenty')
        upload = request.FILES['twenty_one']
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='SOURCE OF SUPPLY OF RAW MATERIAL WITH ADDRESS',
                                         Document_Doc=upload, Document_Number=number, Status=1,Primary_verification_Status=3)
        data1.save()

        number = request.POST.get('twenty_two')
        upload = request.FILES['twenty_three']
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs=' LIST OF ITEMS HOLDING ISO 9001 CERTIFICATE',
                                         Document_Doc=upload, Document_Number=number, Status=1,Primary_verification_Status=3)
        data1.save()


        number = request.POST.get('twenty_four')
        upload = request.FILES['twenty_five_90']
        data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='Electricity bill of Firm or Company Premises',
                                         Document_Doc=upload, Document_Number=number, Status=1, complete_data=1,Primary_verification_Status=3)
        data1.save()

        # number = request.POST.get('Twenty_six')
        # upload = request.FILES['twenty_five_file']
        # data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='Undertaking regarding debarring from the DISCOM of MP',
        #                                  Document_Doc=upload, Document_Number=number, Status=1, complete_data=1)
        # data1.save()




        # upload = request.FILES['Twenty_seven']
        # data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='Undertaking regarding debarring from the DISCOM of MP',
        #                                  Document_Doc=upload, Status=1, complete_data=1)
        # data1.save()


        # upload = request.FILES['twenty_five_901']
        # data1 = Vendor_Technical_Details(user_id=user_id, Types_of_Docs='Declaration with regard to the Ex-employee of MP DISCOMS and regarding their relatives',
        #                                  Document_Doc=upload, Status=1, complete_data=1)
        # data1.save()







        if User_Registration_Check_Status.objects.filter(User=data).exists():
              data1 = User_Registration_Check_Status.objects.get(User=data)
              data1.page_11 = 1
              data1.save()
        else:
            user = User_Registration_Check_Status(User=data,page_11=1)
            user.save()

        return redirect('vendor_reg_twelve')
    return render(request, 'vendor/vendor_reg11.html')


def vendor_reg_twelve(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    pan_details = UserCompanyDataMain.objects.get(user_id_id = data.User_Id)
    print("ggggggggg",pan_details.Company_Pan_No)
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id

    
        upload_four = request.FILES['four']
        data2 = Vendor_BalanceSheet(user_id=user_id, document_name='BALANCE SHEET DETAILS/ PROFIT-LOSS STATEMENT (CA Certified)', Balance_Sheet=upload_four,
                                    Status=1)
        data2.save()

        # upload_five = request.FILES['five']
        # data3 = Vendor_BalanceSheet(user_id=user_id, document_name='PREVIOUS LAST THREE YEARS TAX RETURN', Balance_Sheet=upload_five,
        #                             Status=1)
        # data3.save()
        name = request.POST.get('thirteen')
        number = request.POST.get('fourteen')
#         issu_date = datetime.datetime.now()
        upload = request.FILES['sixteen']
        data1 = Vendor_Document(user_id=user_id, Types_of_Docs='PAN CARD DETAILS', Name_on_Document=name,
                                Document_Number=number,
                                Ddocfile=upload, Status=1)
        data1.save()
        name = request.POST.get('twenty')

        number = request.POST.get('twenty_one')
        upload = request.FILES['twenty_two']
        data1 = Vendor_BalanceSheet(user_id=user_id, document_name='ACTIVE GST NO. (ALONG WITH COPY OF CURRENT PAID CHALLAN AND ITS RECEIPT)',

                                    Balance_Sheet=upload, Status=1)
        data1.save()
        finance = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
      


        if User_Registration.objects.filter(Otp=request.session['otp'],by_discom='1',User_type = request.session['User_type']).exists():
            user_id = User_Registration.objects.filter(Otp=request.session['otp'],by_discom='1',User_type = request.session['User_type'])
          
            user_id.update(payment=1)
            user_id.update(work_approval=1)
            user_id.update(finance_approval=1)



        if User_Registration_Check_Status.objects.filter(User=data).exists():
              data1 = User_Registration_Check_Status.objects.get(User=data)
              data1.page_12 = 1
              data1.save()
        else:
            user = User_Registration_Check_Status(User=data,page_12=1)
            user.save()

        return redirect("vendor_reg_fifteen")
    return render(request, 'vendor/vendor_reg12.html',{'data':data,'pan_details':pan_details})


def vendor_reg_thirteen(request):
    return render(request, 'vendor/vendor_reg13.html')


def vendor_reg_fourteen(request):
    return render(request, 'vendor/vendor_reg14.html')


# def vendor_reg_fifteen(request):
#     return render(request, 'vendor/vendor_reg15.html')



#-----------lokendra

import math
import random

def vendor_reg_fifteen(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
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
        if data.add_material == 1:
            data.add_material = 2
            data.save()
        request.session['verify'] = otp
        return redirect("/vendor/vendor_otp_verify")
    return render(request, 'vendor/vendor_reg15.html',{'data':data})



def vendor_otp_verify(request):
    if request.session.has_key('otp'):
        if request.method == "POST":
            otp = request.POST.get('otp')
            if otp == request.session['verify']:
                data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
                data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
                reg_date = datetime.datetime.now()
                data11.update(complete_data=1,Complete_Details=1,reg_date=reg_date)
                user_id = data.User_Id
                mobile = data.ContactNo
                name_sms = data.CompanyName_E
                zone = data.User_zone
                
                # send_mail(
                #     'Your final registration is completed ',
                #     'Hello thanks for Final registration as a Vendor',
                #     settings.EMAIL_HOST_USER,
                #     [data.Email_Id],
                #     fail_silently=False,
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
                    
                    sms_template = message_template_log(template_id = '1007897298975414680',date = datetime.datetime.now(),mobile_number = mobile)
                    sms_template.save()
                    if data.add_material == 1:
                        data.add_material = 2
                        data.save()                    
                
                return redirect('/vendor/basic')
            else:
              
                return render(request, 'vendor/vendor_verify_otp.html')
            
    return render(request, 'vendor/vendor_verify_otp.html')

def vendor_reg_sixteen(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        mobile = data.ContactNo
        name_sms = data.Authorised_person_E
        data1 = Vendor_Financial_Details(user_id=user_id, complete_data=1)
        data1.save()
        send_mail(
            'Your final registration is completed ',
            'Hello thanks for Final registration as a Vendor',
            settings.EMAIL_HOST_USER,
            [data.Email_Id],
            fail_silently=False,
        )
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(mobile) + "&v1="+ str(company_name_e) + "&v2=" + str()
        response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1007277348148394809',date = datetime.datetime.now(),mobile_number = mobile)
        sms_template.save()

        return render(request, 'vendor/regtest.html', {'data': data11})
    return render(request, 'vendor/vendor_reg16.html')

def LeasingPerson(request):
    
        # data = User_Registration.objects.get(Otp=request.session['otp'])
    aa = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    abc = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if abc.cgm_approval == 1:
        if request.method == "POST":
            name = request.POST.get('nameData')
            designation = request.POST.get('designation')
            dob = request.POST.get('dob')
            firm_name = request.POST.get('firm_name')
            number = request.POST.get('number')
            email = request.POST.get('email')
            photo = request.FILES['photo']

            lp = LeasingPerson(vendor_id=abc.User_Id,name=name,designation=designation,dob=dob,firm=firm_name,mobile=number,email=email,photo=photo)
            lp.save()
            return render(request, 'vendor/leasingPerson.html')

    else:
        return render(request, 'vendor/verification_pending_leasing.html')

            
    return render(request, 'vendor/leasingPerson.html')




def add_material(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    if data.cgm_approval == 1 and data.add_material == 0:
        return render(request, 'vendor/add_material_instuction.html')

    elif data.add_material == 1:
        return redirect("/vendor/vednor_new_material")

    else:
        return render(request, 'vendor/profile_under_process.html')


def employees_list(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    add_material = Vendor_Material_Details.objects.filter(user_id=user_id)
    if request.method == "POST":
        return redirect('two')
    data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    payu_count = Payudata_main.objects.filter(Contact_No=data.ContactNo).count()
    return render(request, 'vendor/one.html', {'userdata': data11[0],'payu_count':payu_count,'employees': add_material,})

def two(request):
    mm = Material_Master.objects.all()
   
    if request.method == 'POST':
        try:
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
            material = request.POST.get('Material')
            matrial_name = Vendor_Material_Master.objects.get(Material_Id=material)
            specification = request.POST.get('Specification')
            spec = Vendor_Material_Specification_Master.objects.get(Material_Specification_Id=specification)
            capacity = request.POST.get('capacity')
            unit = request.POST.get('unit')
            # others = request.FILES['others']

            if Vendor_Material_Details.objects.filter(user_id=data, Material_Name=matrial_name.Material_Name,Material_Specification=spec.Material_Specification_Name).exists():
                messages.warning(request, "Material with this specification already selected")  
                return render(request, 'vendor/two.html')  
            else:
                material_obj = Vendor_Material_Details(user_id=data, Material_Name=matrial_name.Material_Name,item_code = spec.Material_Item_Code,
                                            Material_Specification=spec.Material_Specification_Name,item_code_ez=spec.Material_Item_Code_EZ,item_code_wz=spec.Material_Item_Code_WZ,
                                            Material_Test_Doc=type_test_report, Material_GTP_Doc=gtp_and_drawing, Material_Other_Doc=others,Status=1
                                            )
                material_obj.save()

        except Exception as e:
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
            material = request.POST.get('Material')
            matrial_name = Vendor_Material_Master.objects.get(Material_Id=material)
            specification = request.POST.get('Specification')
            spec = Vendor_Material_Specification_Master.objects.get(Material_Specification_Id=specification)
            capacity = request.POST.get('capacity')
            unit = request.POST.get('unit')
            if Vendor_Material_Details.objects.filter(user_id=data, Material_Name=matrial_name.Material_Name,Material_Specification=spec.Material_Specification_Name).exists():
                messages.warning(request, "Material with this specification already selected")  
                return render(request, 'vendor/two.html') 
            else:
                material_obj = Vendor_Material_Details(user_id=data, Material_Name=matrial_name.Material_Name,item_code = spec.Material_Item_Code,
                                            Material_Specification=spec.Material_Specification_Name,item_code_ez=spec.Material_Item_Code_WZ,item_code_wz=spec.Material_Item_Code_EZ,
                                            Status=1,per_month_capacity=capacity,material_unit=unit
                                            )
                material_obj.save()

        return redirect('employees-list')
    return render(request, 'vendor/two.html',{'mm':mm} )



# ********************************************************working officer*************************

def vendor_wnp_base(request):
    work = Vendor_Financial_Details.objects.filter(complete_data=1).count()
    work_one = Vendor_Technical_Details.objects.filter(complete_data=1).count()
    total = work + work_one
    return render(request, 'vendor/vendor_wnp_base.html', {"pending": work, "com": work_one, "total": total})


def Working_data(request):
    finance = Vendor_fiance_officer.objects.filter(fiance_approve=1)
    return render(request, 'vendor/working_data.html', {"data": finance})


def vendor_wnp_evaluate(request):
    data = Vendor_Financial_Details.objects.filter(all_complete_data=1)
    return render(request, 'vendor/vendor_wnp_evaluate.html', {'data': data})


def vendor_wnp_approval(request, V_id):
    finance = Vendor_Financial_Details.objects.filter(id=V_id)
    finance.update(all_complete_data=0)
    v_serail = Vendor_Financial_Details_Serializer(finance, many=True)
    final = v_serail.data
    ee = json.loads(json.dumps(final))
    userid = ee[0]['user_id']
    finance_data_save = Vendor_fiance_officer(user_id=userid, fiance_approve=1)
    finance_data_save.save()
    return render(request, 'vendor/vendor_wnp_approval.html', {'data': finance[0]})


def test(request):
    return render(request, 'vendor/regtest.html')


def changepwd(request):
    if request.method == "POST":
        res = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        current = request.POST["old_password"]
        newpass = request.POST["new_password"]

        if res.ContactNo == request.POST["old_password"]:
            res.ContactNo = request.POST["new_password"]
            res.ContactNo = request.POST["confirm_password"]
            if request.POST["new_password"] == request.POST["confirm_password"]:
                res.save()
                return render(request, 'vendor/change_pass_r_vai.html', {"msg": "Password Changed successfully"})

            else:
                return render(request, 'vendor/change_pass_r_vai.html',
                              {"msg": "New password and confirm password are not match"})
        else:
            return render(request, 'vendor/change_pass_r_vai.html', {"msg": "current password is not match"})

    return render(request, 'vendor/change_pass_r_vai.html')


# ********************************************************vendor Po *************************
def procurement_Previous_PO(request):
    data = ProcurementInfo.objects.all()
    return render(request, 'PO/procurement_di_list.html', {"data": data})



def vendor_purchase(request):
    res = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = ProcurementInfo.objects.filter(di_status=1, User_code=res.User_Id)
    return render(request, 'vendor/vendor_purchase_order.html', {"data": data})


def procurement_Dispatch(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(dispatch_status=1)
    return render(request, 'vendor/vendor_purchase_order.html', {"data": data})


def vendor_view_di(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    vd = VendorDispatchInfo.objects.filter(po_id=po_id)

    store = LocalStoreInventory.objects.filter(po_id=po_id)
    return render(request, 'vendor/vendor_view_di.html',  {"data": data[0], 'offer': vd, 'store': store})


def vendor_purchase_B(request):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    idd = user.User_Id
    data = Purchase_Order.objects.filter(vendor=user, po_approved_status=1)
    return render(request, 'vendor/vendor_purchase_order_list.html', {"data": data})



def vendor_gtp_approval(request):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    idd = user.User_Id
    data = Purchase_Order.objects.filter(gtp_status=1, gtp_approved=0,po_approved_status=1,vendor=user)
    return render(request, 'po/procurement_gtp_approval.html', {"data": data})



def view_po_details(request, id):
    data1 = Purchase_Order.objects.filter(id=id)
    for v in data1:
        if BankDetails.objects.filter(po_no=v).exists():

            bg = BankDetails.objects.select_related('po_no').get(po_no=v)
            print("bbbbbbbbb",bg)
            for i in data1:
                if PO_SD.objects.filter(po_no=v).exists():
                    sd = PO_SD.objects.select_related('po_no').get(po_no=v)
                    return render(request, 'vendor/vendor_po_details_view.html', {"data": data1,'bg':bg,'sd':sd})
                else:
                    return render(request, 'vendor/vendor_po_details_view.html', {"data": data1,'bg':bg})
        else:
            return render(request, 'vendor/vendor_po_details_view.html', {"data": data1})
    return render(request, 'vendor/vendor_po_details_view.html', {'data1':data1})


def vendor_gtp_approved(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(gtp_approved=1)
    data = ProcurementInfo.objects.filter(
        bg_status=1, bg_approved=0, gtp_approved=0)
    return render(request, 'po/procurement_gtp_approval.html', {"data": data})


def vendor_bg_approval(request):
    data = ProcurementInfo.objects.filter(bg_status=1, bg_approved=0)
    return render(request, 'po/procurement_bg_approval.html', {"data": data})


def vendor_bg_approved(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(bg_approved=1)
    data = ProcurementInfo.objects.filter(bg_status=1, bg_approved=0)
    return render(request, 'po/procurement_bg_approval.html', {"data": data})


def vendor_ins_approval(request):
    data = ProcurementInfo.objects.filter(
        bg_status=1, bg_approved=1, vendor_offer=1)
    return render(request, 'po/procurement_ins_approval.html', {"data": data})


def vendor_ins_approved(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    data.update(offer_approved=1)
    data = ProcurementInfo.objects.filter(
        bg_status=1, bg_approved=1, offer_approved=0)
    return render(request, 'po/procurement_ins_approval.html', {"data": data})


def vendor_dispatch_GTP(request, po_id):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    idd = user.User_Id
    data = Purchase_Order.objects.filter(vendor=user,gtp_status=0, po_approved_status=1)
    # print("ttttttttttttttttttttt")
    # data = ProcurementInfo.objects.filter(id=po_id)
    return render(request, 'vendor/gtp.html', {"data": data[0]})


def vendor_dispatch_GTP_Save(request, po_id):
    if request.method == "POST":
        mobile_no = request.session['mobile_no']
        user = User_Registration.objects.get(ContactNo=mobile_no)
        gtp = request.FILES['gtp']
        data = Purchase_Order.objects.get(id=po_id)
        data.gtp_status = 1
        data.gtp_approved = 0
        data.Po_GTP = gtp
        data.save()
        mobile_no = request.session['mobile_no']
        user = User_Registration.objects.get(ContactNo=mobile_no)
        data = Purchase_Order.objects.filter(vendor=user, po_approved_status=1)
        
        return render(request, 'vendor/vendor_purchase_order_list.html', {"data": data})



def vendor_dispatch_SD(request, po_id):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    idd = user.User_Id
    data = Purchase_Order.objects.filter(id = po_id, vendor=user,bg_status=0, po_approved_status=1)
    return render(request, 'vendor/bgdetails.html', {"data": data[0]})



def vendor_dispatch_SD_Save(request, po_id):

    if request.method == "POST":
        mobile_no = request.session['mobile_no']
        user = User_Registration.objects.get(ContactNo=mobile_no)
        res = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        reg_code = res.CompanyName_E
        bgbank = request.POST.get('bgbank')
        bg_no = request.POST.get('bg_no')
        bg_issu_date = request.POST.get('bg_issu_date')
        bg_valid_upto = request.POST.get('bg_valid_upto')
        amount = request.POST.get('amount')
        file = request.FILES['file']
      
        data = Purchase_Order.objects.get(id=po_id)
        po_sd = PO_SD(po_no=data, bg_name=bgbank, bg_no=bg_no, issue_date=bg_issu_date, valid_date=bg_valid_upto,
                      amount=amount,file=file)
        po_sd.save()
        data.bg_status = 1
        data.bg_approved = 0
        data.save()
        data = Purchase_Order.objects.filter(vendor=user, po_approved_status=1)
        return render(request, 'vendor/vendor_purchase_order_list.html', {"data": data})



def vendor_dispatch_BD(request, po_id):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    idd = user.User_Id
    data = Purchase_Order.objects.filter(id = po_id, vendor=user,bank_details=0, po_approved_status=1)
    return render(request, 'vendor/bankdetails.html', {"data": data[0]})


def vendor_dispatch_BD_Save(request, po_id):

    if request.method == "POST":
        mobile_no = request.session['mobile_no']
        user = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        res = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        reg_code = res.CompanyName_E
        bank = request.POST.get('bankname')
        ifsc = request.POST.get('ifsc')
        ac_number = request.POST.get('account')
        ac_holder = request.POST.get('account_holder')
        file = request.FILES['file']
        data = Purchase_Order.objects.get(id=po_id)
        po_sd = BankDetails(po_no=data, Bank_name=bank, Account_Holder_Name=ac_holder, Account_Number=ac_number, IFSC=ifsc,file=file)
        po_sd.save()
        data.bank_details = 1
        data.bank_details_approved = 0
        data.save()
        data = Purchase_Order.objects.filter(vendor=user, po_approved_status=1)
        return render(request, 'vendor/vendor_purchase_order_list.html', {"data": data})


def vendor_dispatch_Open(request):
    
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    idd = user.User_Id
    data = Purchase_Order.objects.filter(vendor=user,bg_approved=1, po_approver=1)
    return render(request, 'vendor/vendor_generate_di1.html', {"data": data})



def vendor_dispatch_B(request, po_id):
    data = Purchase_Order.objects.filter(id=po_id)
    data.update(bg_status=1)
    return render(request, 'vendor/vendor_generate_di1.html', {"data": data})


# def vendor_dispatch_B2(request, po_id):
    # if request.method == "POST":
        # quantity = int(request.POST.get('quantity'))
        # data = Purchase_Order.objects.filter(id=po_id)
        # return render(request, 'vendor/vendor_generate_di2.html',
                      # {"data": data[0], "quantity": range(quantity), "quantity1": quantity})
    # data = Purchase_Order.objects.filter(id=po_id)
    # return render(request, 'vendor/vendor_generate_di.html', {"data": data[0]})

def vendor_dispatch_B3(request, po_id, quantity):
    if request.method == "POST":
        officer = InspectingOfficerInfo.objects.all().order_by('?')[:1]
        lab = User_Registration.objects.filter(
            User_type='NABL').order_by('?')[:1]
        po_id =Purchase_Order.objects.get(id=po_id)
        lab1 = User_Registration.objects.get(User_Id=lab[0].User_Id)
        vdi = VendorDispatchInfo(po_id=po_id, inspecting_officer_id=officer[0].id, item_quantity=quantity,
                                 lab_name=lab1)
        vdi.save()
        vd = VendorDispatchInfo.objects.latest('id')
        for data in range(quantity):
            serial_no = request.POST.get(str(data))
            vdi = VendorDispatchItemInfo(
                dispatch_d=vd.id, serial_number=serial_no)
            vdi.save()
        data = Purchase_Order.objects.filter(id=po_id.id)
        data.update(vendor_offer=1)
        dispatch_info = VendorDispatchItemInfo.objects.filter(dispatch_d=vd.id)
        return render(request, 'vendor/vendor_generate_di3.html',
                      {"data": data[0], "quantity": range(quantity), "quantity1": quantity,
                       "dispatch_info": dispatch_info, 'offer': vd})
    data = ProcurementInfo.objects.filter(id=po_id)
    return render(request, 'vendor/vendor_generate_di.html', {"data": data[0]})


def vendor_procurement_status(request, po_id):
    data = ProcurementInfo.objects.filter(id=po_id)
    cdatetime = datetime.now().date()
    return render(request, 'vendor/vendor_po_status.html', {"data": data[0], "date": cdatetime})


# def employees_list(request):
#     data = User_Registration.objects.get(Otp=request.session['otp'])
#     user_id = data.User_Id
#     add_material = Add_material.objects.filter(user_id=user_id)
#     return render(request, 'vendor/list.html', {'employees': add_material})


def create_employee(request):
    form = EmployeeForm()

    if request.method == 'POST':
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        user_name = data.CompanyName_E

        intaial_data = {
            'user_id': user_id,
            'user_name': user_name
        }
        # form = EmployeeForm(initial=intaial_data)

        form = EmployeeForm(request.POST, request.FILES, initial=intaial_data)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user_id = user_id
            dweet.emp_name = user_name
            dweet.save()
            # dd = Employee(user_id=user_id,emp_name=user_name)
            # dd.save()
            return redirect('employees-list')

    context = {
        'form': form,
    }
    return render(request, 'vendor/create.html', context)


def edit_employee(request, pk):
    employee = Add_material.objects.get(id=pk)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees-list')

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'vendor/edit.html', context)


def delete_employee(request, pk):
    employee = Add_material.objects.get(id=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employees-list')

    context = {
        'employee': employee,
    }
    return render(request, 'vendor/delete.html', context)


import payu_sdk
import uuid

def vendor_factory_pay(request, id):
    if request.method == 'POST':
        txnid = uuid.uuid1()
        data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        param = {"txnid": txnid, "amount": "11800.00", "productinfo": "Payment For Factory Inspection",
                "firstname": data.Authorised_person_E,"userzone":'CZ',
                "email": data.Email_Id}
        apiHash = payu_sdk.Hasher.generate_hash(param)
        data3 = Payudata_main(User_Id=data, Payu_Status='pending', Txdid=txnid,
                            Productinfo="Payment For Factory Inspection",
                            Firstname=data.Authorised_person_E, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                            Netamount_Debited='11800.00',user_zone = data.User_zone
                            )
        data3.save()
        return render(request, 'main/payu_checkout_registration.html',
                    {"posted": apiHash, "txnid": txnid, "amount": "11800.00", 'firstname': data.Authorised_person_E,
                    "email": data.Email_Id, "productinfo": "Payment For Factory Inspection", "phone": data.ContactNo,"user_zone_c":data.User_zone})



def vendor_factory_payment(request, id):
    if request.method == 'POST':
        data = User_Registration.objects.get(User_Id=id)
        data.factory_approval_payment = 1
        data.save()
        data = User_Registration.objects.filter(
            work_approval=1, finance_approval=1, User_type='VENDOR')
        return render(request, 'officer/vendor_dgm_qc_pending.html', {'data': data})


def rejected_doc(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    data = Vendor_Document.objects.filter(
        Primary_verification_Status=2, user_id=user_id, Status=0)
    data1 = Vendor_BalanceSheet.objects.filter(
        Primary_verification_Status=2, user_id=user_id, Status=0)

    data2 = Vendor_Technical_Details.objects.filter(Primary_verification_Status=2,
        user_id=user_id)

    data111 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])

    data3 = Vendor_Material_Details.objects.filter(Primary_verification_Status=2,
        user_id=data111)

    print("ttttttt",data3)

    data11 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    payu_count = Payudata_main.objects.filter(Contact_No=data11.ContactNo).count()
    return render(request, 'vendor/rejected_doc_resubmit.html', {"userdata": data11,'payu_count':payu_count,"data": data, "data1": data1,"data2":data2,"data3":data3})




def vendor_view_profile(request):
    if request.session.has_key('otp'):
        data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
        
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        user_id = data.User_Id
        vendor_document = Vendor_Document.objects.filter(user_id=user_id)
        vendor_balance = Vendor_BalanceSheet.objects.filter(user_id=user_id)
        vendor_tech= Vendor_Technical_Details.objects.filter(user_id=user_id)
        abcde = UserCompanyDataMain.objects.get(user_id_id=data)
        return render(request, 'vendor/vendor_view_profile.html',{"basic":data,'company':abcde,'vendor_document':vendor_document,'vendor_balance':vendor_balance,'vendor_tech':vendor_tech})
    return render(request, 'vendor/base1.html')

def rejected_doc_save(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    if data.work_approval == 0 and data.finance_approval == 2:
        data.finance_approval = 0
        data.save()

    elif data.work_approval == 1 and data.finance_approval == 2:
        data.finance_approval = 0
        data.save()
    elif data.work_approval == 2 and data.finance_approval == 1:
        data.work_approval = 0
        data.save()
    elif data.work_approval == 2 and data.finance_approval == 0:
        data.work_approval = 0
        data.save()
    data = Vendor_Document.objects.filter(
        Vendor_Document_Id=id, user_id=user_id)
    data1 = Vendor_BalanceSheet.objects.filter(
        user_id=user_id, Vendor_Document_Id=id)

    data2 = Vendor_Technical_Details.objects.filter(
        user_id=user_id, id=id)

    data111 = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data3 = Vendor_Material_Details.objects.filter(user_id=data111, id=id)
    data_reject_approve_sum = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    


        
    if request.method == "POST":
        office = request.POST.get('office')
        
        Document_Number = request.POST.get('doc_name')
        if Document_Number != '':
            data.update(Document_Number=Document_Number, Status=1)
        issu_date = request.POST.get('issue_date')
        if issu_date != '':
            data.update(Doc_issue_date=issu_date, Status=1)
        exp_date = request.POST.get('expire_date')
        if exp_date != '':
            data.update(Doc_expiry_date=exp_date, Status=1)
        if data:
            if len(request.FILES) != 0:
                data = Vendor_Document.objects.get(
                    Vendor_Document_Id=id, user_id=user_id)
                upload_file = request.FILES['file']
                data.Ddocfile = upload_file
                data.Primary_verification_Status = 0
                data.Status = 1
                
                data.save()
                data2 = User_Registration.objects.get(
                    ContactNo=request.session['uid'],User_type = request.session['User_type'])
                user_id = data2.User_Id
                data2.work_approval = 0
                data2.document_resubmit_date = datetime.datetime.now()
                data2.save()
                data = Vendor_Document.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data1 = Vendor_BalanceSheet.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data2 = Vendor_Technical_Details.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data3 = Vendor_Material_Details.objects.filter(user_id=data111,Primary_verification_Status=2)
                summary = reject_and_approve_summary(user=data_reject_approve_sum,type="RESUBMIT",date=datetime.datetime.now())
                summary.save()
                return render(request, 'vendor/rejected_doc_resubmit.html', {"data": data, "data1": data1,'data2':data2,'data3':data3})
        if data1:
            if len(request.FILES) != 0:
                data1 = Vendor_BalanceSheet.objects.get(Vendor_Document_Id=id)
                upload_file = request.FILES['file2']
                data1.Balance_Sheet = upload_file
                data1.Status = 1
                data1.Primary_verification_Status = 0
                data1.save()
                data = User_Registration.objects.get(
                    ContactNo=request.session['uid'],User_type = request.session['User_type'])
                user_id = data.User_Id
                data.finance_approval = 0
                data.document_resubmit_date = datetime.datetime.now()
                data.save()
                data = Vendor_Document.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data1 = Vendor_BalanceSheet.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)

                data2 = Vendor_Technical_Details.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data3 = Vendor_Material_Details.objects.filter(user_id=data111,Primary_verification_Status=2)
                summary = reject_and_approve_summary(user=data_reject_approve_sum,type="RESUBMIT",date=datetime.datetime.now())
                summary.save()
                return render(request, 'vendor/rejected_doc_resubmit.html', {"data": data, "data1": data1,'data2':data2,'data3':data3})


        if data2:
            if len(request.FILES) != 0:
                data1 = Vendor_Technical_Details.objects.get(id=id)
                upload_file = request.FILES['file3']
                data1.Document_Doc = upload_file
                data1.Status = 1
                data1.Primary_verification_Status = 0
                data1.save()
                data = User_Registration.objects.get(
                    ContactNo=request.session['uid'],User_type = request.session['User_type'])
                user_id = data.User_Id
                data.work_approval = 0
                data.document_resubmit_date = datetime.datetime.now()
                data.save()
                data = Vendor_Document.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data1 = Vendor_BalanceSheet.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)

                data2 = Vendor_Technical_Details.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data3 = Vendor_Material_Details.objects.filter(user_id=data111,Primary_verification_Status=2)
                summary = reject_and_approve_summary(user=data_reject_approve_sum,type="RESUBMIT",date=datetime.datetime.now())
                summary.save()
                return render(request, 'vendor/rejected_doc_resubmit.html', {"data": data, "data1": data1,'data2':data2,'data3':data3})


        if data3:
            if len(request.FILES) != 0:
                data1 = Vendor_Material_Details.objects.get(id=id)
                upload_file1 = request.FILES['file4']
                upload_file2 = request.FILES['file5']
                upload_file3 = request.FILES['file6']
                data1.Material_Test_Doc = upload_file1
                data1.Material_GTP_Doc = upload_file2
                data1.Material_Other_Doc = upload_file3

                data1.Primary_verification_Status = 0
                data1.save()
                data = User_Registration.objects.get(
                    ContactNo=request.session['uid'],User_type = request.session['User_type'])
                user_id = data.User_Id
                data.work_approval = 0
                data.document_resubmit_date = datetime.datetime.now()
                data.save()
                data = Vendor_Document.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data1 = Vendor_BalanceSheet.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)

                data2 = Vendor_Technical_Details.objects.filter(
                    Primary_verification_Status=2, user_id=user_id, Status=0)
                data3 = Vendor_Material_Details.objects.filter(user_id=data111,Primary_verification_Status=2)
                summary = reject_and_approve_summary(user=data_reject_approve_sum,type="RESUBMIT",date=datetime.datetime.now())
                summary.save()
                return render(request, 'vendor/rejected_doc_resubmit.html', {"data": data, "data1": data1,'data2':data2,'data3':data3})
    return render(request, 'vendor/base1.html', {"data": data, 'data1': data1,'data2':data2,'data3':data3,'data3':data3})




# payu_config = settings.PAYU_CONFIG
# merchant_key = payu_config.get('merchant_key')
# merchant_salt = payu_config.get('merchant_salt')
# surl = payu_config.get('success_url')
# furl = payu_config.get('failure_url')
# mode = payu_config.get('mode')

# payu = Payu(merchant_key, merchant_salt, surl, furl, mode)


# def payu_demo_one(request):
#     # mail=request.data.get('Email_Id')

#     # data=User_Registration.objects.get(mail=Email_Id).exists()

#     data = {'amount': '10000',
#             'firstname': 'renjith',
#             'email': 'renjithsraj@gmail.com',
#             'phone': '9746272610', 'productinfo': 'test',
#             'lastname': 'test', 'address1': 'test',
#             'address2': 'test', 'city': 'test',
#             'state': 'test', 'country': 'test',
#             'zipcode': 'tes', 'udf1': '',
#             'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
#             }

#     # txnid = "Create your transaction id"
#     data.update({"txnid": "23456789"})
#     payu_data = payu.transaction(**data)

#     payu_data['surl'] = '/vendor/success_fi'
#     return render(request, 'vendor/payu_checkout.html', {"posted": payu_data})


# # Payu success return page
# @csrf_exempt
# def payu_success(request):
#     data = {k: v[0] for k, v in dict(request.POST).items()}
#     response = payu.verify_transaction(data)
#     return redirect(request, 'vendor/sucess_pay_vendor.html')


# # Payu failure page
# @csrf_exempt
# def payu_failure(request):
#     data = {k: v[0] for k, v in dict(request.POST).items()}
#     response = payu.verify_transaction(data)
#     return JsonResponse(response)


# def success_reg_new(request):
#     return render(request, 'vendor/sucess_pay.html')


# def gen_invoice_fi(request):
#     return render(request, 'vendor/gen_invoice_fi.html')


# ##########

# def payu_demo_two(request):
#     # mail=request.data.get('Email_Id')

#     # data=User_Registration.objects.get(mail=Email_Id).exists()
#     data1 = User_Registration.objects.filter(Otp=request.session['otp'])
#     firstname = data1[0].Authorised_person_E
#     e_mail = data1[0].Email_Id
#     phone = data1[0].ContactNo

#     data = {'amount': '2000',
#             'firstname': firstname,
#             'email': e_mail,
#             'phone': phone, 'productinfo': 'test',
#             'lastname': 'test', 'address1': 'test',
#             'address2': 'test', 'city': 'test',
#             'state': 'test', 'country': 'test',
#             'zipcode': 'tes', 'udf1': '',
#             'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
#             }

#     # txnid = "Create your transaction id"
#     data.update({"txnid": "23456789"})
#     payu_data = payu.transaction(**data)

#     payu_data['surl'] = '/vendor/success_fi'
#     return render(request, 'vendor/payu_checkout.html', {"posted": payu_data})


def transaction_history(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    payu_count = Payudata_main.objects.filter(User_Id=data)
    return render(request, 'vendor/transation_history.html', {"posted": payu_count})



def transaction_history_copy(request,id):
    payu_count = Payudata_main.objects.get(id=id)
    return render(request, 'vendor/invoice_first.html', {"data": payu_count})
# # @api_view(['GET', 'POST'])
# # def snippet_list(request):

# #     if request.method == 'GET':
# #         con = psycopg2.connect(database="MQP", user="postgres", password="postgres", host="172.24.200.22", port="5432")
# #         cur =  con.cursor()
# #         cur.execute('SELECT "Material_Name" from "Material_Master"')
# #         cur2 = con.cursor()
# #         # cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Material_Acceptance_Test_Master'")
# #         # cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Material_Specification'")
# #         # cur.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Material_Master'")


# #         cur2.execute('SELECT "Material_Type" from "Material_Specification"')
# #         test_keys = cur.fetchall()
# #         test_values = cur2.fetchall()
# #         res = {}
# #         for key in test_keys:
# #             for value in test_values:
# #                 res[key] = value
# #                 test_values.remove(value)
# #                 break


# #         print ("Resultant dictionary is : " +  str(res))
# #         return Response(res)




###########updated payu lok########

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from paywix.payu import Payu

payu_config = settings.PAYU_CONFIG1
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

payu1 = Payu(merchant_key, merchant_salt, surl, furl, mode)





# def payu_demo_one(request):
#     # mail=request.data.get('Email_Id')


#     # data=User_Regi21 '9746272610', 'productinfo': 'test',
#             'lastname': 'test', 'address1': 'test',
#             'address2': 'test', 'city': 'test',
#             'state': 'test', 'country': 'test',
#             'zipcode': 'tes', 'udf1': '',
#             'udf2': 21quest, 'vendor/payu_checkout.html', {"posted": payu_data})


# # Payu success return page
# @csrf_exempt
# def payu_success(request):
#     data = {k: v[0] for k, v in dict(request.POST).items()}
#     response = payu.verify_transaction(data)
#     return redirect(request,'vendor/sucess_pay_vendor.html')


# # Payu failure page
# @csrf_exempt
# def payu_failure(request):
#     data = {k: v[0] for k, v in dict(request.POST).items()}
#     response = payu.verify_transaction(data)
#     return JsonResponse(response)


# def success_reg_new(request):
#     return render(request, 'vendor/sucess_pay.html')



# def gen_invoice_fi(request):
#     return render(request, 'vendor/gen_invoice_fi.html')

def payu_demo_factoryinspection(request):

    # data = User_Registration.objects.filter(Otp=request.session['otp'])
    data = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    firstname = data[0].Authorised_person_E
    e_mail = data[0].Email_Id
    phone = data[0].ContactNo
    data1 = {'amount': '10000',
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
    payu_data = payu1.transaction(**data1)
    return render(request, 'vendor/payu_checkout_factoryinspection.html', {"posted": payu_data})


# Payu success return page
@csrf_exempt
def payu_success_factoryinspection(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu1.verify_transaction(data)

    Hash=data['hash']
    Status=data['status']
    Txn_id=data['txnid']
    Product_info=data['productinfo']
    First_name=data['firstname']
    Last_name=data['lastname']
    Phone_no=data['phone']
    mail=data['email']
    Pgateway_Type=data['PG_TYPE']
    Bankrefnum=data['bank_ref_num']
    Bank_code=data['bankcode']
    Nameon_card=data['name_on_card']
    Card_num=data['cardnum']
    payu_moneyid=data['payuMoneyId']
    Netamount=data['net_amount_debit']
    

    
    

    data3 = Payudata_main( Payu_Moneyid=payu_moneyid,Hash_Id=Hash, Payu_Status=Status, Txdid=Txn_id, Productinfo=Product_info,
                         Firstname=First_name, Lastname=Last_name, Contact_No=Phone_no, Email_Id=mail,
                         Paymentgateway_Type=Pgateway_Type,
                         Bank_Ref_Num=Bankrefnum, Bankcode=Bank_code, Name_On_Card=Nameon_card,
                         Cardnum=Card_num, Netamount_Debited=Netamount,
                        )
    data3.save()

    payu_obj = Payudata_main.objects.latest('id')
    

    return render(request, 'vendor/sucess_pay_factoryinspection.html', {'response': response,'data': payu_obj})


# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu1.verify_transaction(data)
    return JsonResponse(response)


def gen_invoice_factoryinspection(request):
    payu_obj = Payudata_main.objects.latest('id')
    return render(request, 'vendor/invoice_factoryinspection.html',{'data': payu_obj})







#########

# def payu_demo_two(request):
#     # mail=request.data.get('Email_Id')


#     # data=User_Registration.objects.get(mail=Email_Id).exists()
#     data1 = User_Registration.objects.filter(Otp=request.session['otp'])
#     firstname = data1[0].Authorised_person_E
#     e_mail = data1[0].Email_Id
#     phone = data1[0].ContactNo

#     data = {'amount': '2000',
#             'firstname': firstname,
#             'email': e_mail,
#             'phone': phone, 'productinfo': 'test',
#             'lastname': 'test', 'address1': 'test',
#             'address2': 'test', 'city': 'test',
#             'state': 'test', 'country': 'test',
#             'zipcode': 'tes', 'udf1': '',
#             'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
#             }

#     # txnid = "Create your transaction id"
#     data.update({"txnid": "23456789"})
#     payu_data = payu.transaction(**data)

#     payu_data['surl']='/vendor/success_fi'
#     return render(request, 'vendor/payu_checkout.html', {"posted": payu_data})

payu_config = settings.PAYU_CONFIG2
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

payu2 = Payu(merchant_key, merchant_salt, surl, furl, mode)


import payu_sdk
import uuid

def payu_demo_vendormaterial(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        print(data)
        firstname = data.Authorised_person_E
        e_mail = data.Email_Id

        phone = data.ContactNo
        productinfo = 'Add Material'
     
        txnid = uuid.uuid1()
        keys = "GHeH7D"
        salt = "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"
        amount= 11800.00
        client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        param = {"txnid": txnid, "amount":amount, "productinfo": productinfo,
                "firstname": data.Authorised_person_H,
                "email": data.Email_Id}
        apiHash = payu_sdk.Hasher.generate_hash(param)
        data3 = Payudata_main(User_Id=data,Payu_Status='pending', Txdid=txnid,
                                Productinfo=productinfo,
                                Firstname=data.Authorised_person_H, Contact_No=data.ContactNo, Email_Id=data.Email_Id,
                                Netamount_Debited='11800.00'
                                )
        data3.save()
        return render(request, 'vendor/payu_checkout_vendormaterial.html',
                    {"posted": apiHash, "txnid": txnid, "amount": amount, 'firstname': data.Authorised_person_H,
                    "email": data.Email_Id, "productinfo": productinfo, "phone": data.ContactNo,"keys":keys,"salt":salt})


from fpdf import FPDF
import os
from payu_sdk.API import paymentAPI
import json
import hashlib
import io
from rest_framework.parsers import JSONParser


@csrf_exempt
def payu_success_vendormaterial(request):
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
    # if Pgateway_Type == 'NB-PG':
    #     Nameon_card ='Net banking'
    #     Card_num = '000000'
  
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    Error = data['field9']
    date = datetime.datetime.now()
    if Payudata_main.objects.filter(Txdid=Txn_id).exists():
        Payudata = Payudata_main.objects.get(Txdid=Txn_id)
        if Payudata.Productinfo == 'Activation Fee Befour Expired':
            user = User_Registration.objects.filter(ContactNo=Phone_no,User_type = "VENDOR")
            user.update(activation_before_expired = 1,activation=1)
      
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
    user = User_Registration.objects.filter(ContactNo=Phone_no,User_type = "VENDOR")
    date = datetime.datetime.now()
    user = User_Registration.objects.filter(ContactNo=Phone_no,User_type = "VENDOR")
    client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
    key = 'GHeH7D'
    salt = 'DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ'
    command = 'verify_payment'
    toHash = {"command": command, "var1": Txn_id}
    apiHash = payu_sdk.Hasher.APIHash(toHash)
    Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
    #url = 'https://test.payu.in/merchant/postservice.php?form=2'
    url = "https://info.payu.in/merchant/postservice?form=2"
    proxyDictfd={"https":"proxy.mpcz.in:8080","http":"proxy.mpcz.in:8080"}
    response = requests.get(url,proxies=proxyDictfd)
    #r = requests.post(url, data=Poststring)
    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    payload = "key=" + key + "&command=verify_payment&var1=" + Txn_id + "&hash=" + apiHash
    # res = requests.request("POST", url, data=payload, headers=headers)
    res = requests.request("POST", url,proxies=proxyDictfd, data=payload, headers=headers)

    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
    user = User_Registration.objects.get(ContactNo=Phone_no,User_type = "VENDOR")
    user.add_material= 1
    user.save()
    if res.status_code == 200:
        json_data = json.loads(res.text)
        if json_data['status'] == 1:
            transcation_details = json_data['transaction_details']
            transction_data = transcation_details[Txn_id]
            if transction_data['status'] == 'success':
                payu_obj = Payudata_main.objects.get(Txdid=Txn_id)
                if transction_data['productinfo'] == "Activation Fee After Expired":
                    user = User_Registration.objects.get(ContactNo=Phone_no,User_type = "VENDOR")
                    user.add_material= 1
                    user.save()
                    return render(request, 'vendor/sucess_pay_vendormaterial.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_reg_seven'})

    
    else:
        attempt_num += 1
        time.sleep(5) 
    request.session['Phone_no'] = Phone_no
    return render(request, 'vendor/sucess_pay_vendormaterial.html',
                                  {'response': response, 'data': payu_obj, 'url': 'tkc/tkc_reg_seven'})

    User_Id = user.User_Id
    payu_obj = Payudata_main.objects.get(Txdid=Txn_id)
    user = User_Registration.objects.get(ContactNo=Phone_no,User_type = "VENDOR")
    user.payment = 1;
    user.save()
    return render(request, 'main/sucess_pay_registration.html',
                  {'response': response, 'data': payu_obj, 'url': 'tkc/login'})
    payu_obj = Payudata_main.objects.latest('User_Id')
    request.session['Phone_no'] = Phone_no
    sms = User_Registration.objects.get(ContactNo=Phone_no,User_type = "VENDOR")
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
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu2.verify_transaction(data)
    return JsonResponse(response)

# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu2.verify_transaction(data)
    return JsonResponse(response)


def gen_invoice_vendormaterial(request):
    data = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    data.update(add_material=1)
    payu_obj = Payudata_main.objects.latest('id')
    return render(request, 'vendor/invoice_vendormaterial.html',{'data': payu_obj})




payu_config = settings.PAYU_CONFIG3
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

payu3 = Payu(merchant_key, merchant_salt, surl, furl, mode)




def payu_demo_vendorprofile(request):

    # data = User_Registration.objects.filter(Otp=request.session['otp'])
    data = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    firstname = data[0].Authorised_person_E
    e_mail = data[0].Email_Id
    phone = data[0].ContactNo
    data1 = {'amount': '2000',
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
    payu_data = payu3.transaction(**data1)
    return render(request, 'vendor/payu_checkout_vendorprofile.html', {"posted": payu_data})


@csrf_exempt
def payu_success_vendorprofile(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu3.verify_transaction(data)

    Hash=data['hash']
    Status=data['status']
    Txn_id=data['txnid']
    Product_info=data['productinfo']
    First_name=data['firstname']
    Last_name=data['lastname']
    Phone_no=data['phone']
    mail=data['email']
    Pgateway_Type=data['PG_TYPE']
    Bankrefnum=data['bank_ref_num']
    Bank_code=data['bankcode']
    Nameon_card=data['name_on_card']
    Card_num=data['cardnum']
    payu_moneyid=data['payuMoneyId']
    Netamount=data['net_amount_debit']
    

    
    

    data3 = Payudata_main( Payu_Moneyid=payu_moneyid,Hash_Id=Hash, Payu_Status=Status, Txdid=Txn_id, Productinfo=Product_info,
                         Firstname=First_name, Lastname=Last_name, Contact_No=Phone_no, Email_Id=mail,
                         Paymentgateway_Type=Pgateway_Type,
                         Bank_Ref_Num=Bankrefnum, Bankcode=Bank_code, Name_On_Card=Nameon_card,
                         Cardnum=Card_num, Netamount_Debited=Netamount,
                        )
    data3.save()

    payu_obj = Payudata_main.objects.latest('id')
    

    return render(request, 'vendor/sucess_pay_vendorprofile.html', {'response': response,'data': payu_obj})


# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu3.verify_transaction(data)
    return JsonResponse(response)


def gen_invoice_vendorprofile(request):
    data = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    data.update(profile_update_fee=1)
    payu_obj = Payudata_main.objects.latest('id')

    return render(request, 'vendor/invoice_vendorprofile.html',{'data': payu_obj})

#---------lokendra


#####################lok#####

def RCA_vendor_order(request):
    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1)
    # data = WO_Info.objects.all()
    return render(request, 'vendor/RCA_vendor_order_list.html', {"data": data})


def RCA_vendor_order_submit(request, id):
    print("kkkkkkkkkkkkkk", id)
    wo_ack = WO_Info.objects.filter(id=id)
    wo_ack.update(wo_ack=1)
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    data = WO_Info.objects.filter(vendor_id=user.User_Id)

    data1 = WO_Material_Info.objects.filter(wo_id=user.User_Id)
    return render(request, 'vendor/RCA_vendor_order_list.html', {"data": data, "data1": data1})


from datetime import date


def rca_order_view(request, id):
    vd = WO_Info.objects.get(id=id)
    schedule = WO_Schedule_Info.objects.filter(schedule_id=vd)
    copy = WO_Copy_Info.objects.filter(wo=vd)
    today = date.today()
    return render(request, 'vendor/rca/view_wo.html',
                  {'vd': vd, 'copy': copy, 'date': today, 'schedule': schedule})


from datetime import date





def RCA_vendor_release_order(request):
   
    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1,rca_bg_accept=1)
    return render(request, 'vendor/RCA_vendor_release_order_list.html',
                  {"data": data})



def rca_release_order_view(request, id):
    vd = RO_Info.objects.get(id=id)
    schedule = RO_Schedule_Info.objects.get(ro_id=vd)
    
    copy = RO_Copy.objects.filter(ro=vd)
    ro_m = RO_Material_Info.objects.filter(ro=vd)
    today = date.today()
    
    return render(request, 'vendor/rca/view_ro.html',
                           {'vd': vd, 'copy': copy, 'date': today, 'schedule': schedule, 'material': ro_m})



def RCA_release_order_submit(request, id):
    # wo = WO_Info.objects.filter(id=id)
    ro_ack = RO_Info.objects.get(id=id)
    ro_ack.ven_ack = 1
    ro_ack.save()
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    data = WO_Info.objects.filter(vendor_id=user.User_Id)

    data1 = RO_Info.objects.all()
    return render(request, 'vendor/RCA_vendor_release_order_list.html', {"data": data, "redata": data1})


# def rca_release_order_view(request):
#     mobile_no = request.session['mobile_no']
#     user = User_Registration.objects.get(ContactNo=mobile_no)
#     data = WO_Info.objects.filter(vendor_id=user.User_Id)
#     return render(request, 'vendor/RCA_vendor_order_list.html', {"data": data})


def RCA_vendor_dtr_list(request, id):
    vd = WO_Info.objects.get(id=id)
    data = RO_Info.objects.filter(wo=vd.id)
    return render(request, 'vendor/RCA_vendor_dtr_list.html', {'data': data})


def rca_di_view(request, id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    return render(request, 'vendor/RCA_di_view.html',
                  {'ro': ro, "material": material, "xmr": xmr})



def oil_request(request):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    data = RO_Info.objects.all()
    return render(request, 'vendor/rca/oil_request.html', {"data": data})


def oil_request1(request, id):
    mobile_no = request.session['mobile_no']
    user = User_Registration.objects.get(ContactNo=mobile_no)
    data = WO_Info.objects.filter(vendor_id=user.User_Id)
    if request.method == 'POST':
        ro = RO_Info.objects.get(id=id)
        quantity = request.POST.get('quantity')
        oil = Oil_Request(ro=ro,v_request_quantity=quantity)
        oil.save()
        data = RO_Info.objects.all()
        return render(request, 'vendor/rca/oil_request.html', {"data": data})
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    return render(request, 'vendor/rca/oil_request1.html',
                  {'ro': ro, "material": material, "xmr": xmr})

from datetime import datetime
def rca_oil_confirmed(request):
    data = Oil_Request.objects.filter(rca_forward_to_as=1,as_forward_to_rca=1,rca_forward_to_vendor=1)   
    return render(request,'vendor/RCA_oil_confirmed.html',{'data_info': data})

# def 

def repaired_dtr_by_vendor(request):
    # mobile_no = request.session['mobile_no']
    # user = User_Registration.objects.get(ContactNo=mobile_no,rca_vendor=1)
    # data = WO_Info.objects.filter(vendor_id=user.User_Id)

    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1,rca_bg_accept=1)
    return render(request, 'vendor/repaired_dtr_by_vendor.html', {'data': data})

# def repaired_dtr_by_vendor_view(request, id):
#     if request.method == "POST":
#         quantity_dtr_repair = request.POST.get("quantity")
        
#         # mo_capacit = request.POST.get("mo")

#         ro = RO_Info.objects.get(id=id)
#         combined_xmr_report = request.FILES['all_xmr_file']
#         abc = request.POST.getlist('xmr_det')
#         for data in abc:
#             test = RO_Material_XMR_Info.objects.get(id=data)
#             test.vendor_send = 1
#             test.xmr_ven_dispatch_date=date.today()
#             # test.vendor_submitted = 1
#             test.physical_status = 0
#             test.as_accepted = 0
#             test.pa_result = 0
#             test.pa_result_submitted = 0
#             test.pa_report_flag = 0
#             test.xmr_rej_gp_flag = 0
#             test.xmr_rej_gp_submitted = 0
#             test.as_issue_mat = 0
#             test.single_reject_by_nabl=0
#             test.machine_reject_by_nabl=0
#             test.ph_reject_by_nabl=0
#             test.save()

#         unecono = request.POST.getlist('uneco')
#         for data1 in unecono:
#             test1 = RO_Material_XMR_Info.objects.get(id=data1)
#             test1.uneco_status = 1
#             test1.save()
#         # data1 = material_offer.objects.get(id=id)

#         # data1 = material_offer.objects.get(id=id)

        
#         data2 = material_offer(ro=ro,all_xmr_rprt=combined_xmr_report, quanity_offered=quantity_dtr_repair)
#         data2.save()



#         ro = RO_Info.objects.get(id=id)
        
#         xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,xmr_rej_gp_flag=1, vendor_send=0) | Q(ro=ro,as_issue_mat=1, vendor_send=0))
#         material = RO_Material_Info.objects.filter(ro_id=ro)
#         # xmr2 = RO_Material_XMR_Info.objects.filter(ro=ro, physical_status=-1)

#         return render(request, 'vendor/repaired_dtr_by_vendor_view.html',
#                         {'ro': ro, "material": material, "xmr": xmr})

#     ro = RO_Info.objects.get(id=id)
#     xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,xmr_rej_gp_flag=1, vendor_send=0) | Q(ro=ro,as_issue_mat=1, vendor_send=0))
#     # xmr2 = RO_Material_XMR_Info.objects.filter(ro=ro, physical_status=-1)
#     material = RO_Material_Info.objects.filter(ro_id=ro)
#     return render(request, 'vendor/repaired_dtr_by_vendor_view.html',
#                   {'ro': ro, "material": material, "xmr": xmr})




# def repaired_dtr_by_vendor_view(request, id):
#     if request.method == "POST":
#         quantity_dtr_repair = request.POST.get("quantity")

#         ro = RO_Info.objects.get(id=id)
#         combined_xmr_report = request.FILES['all_xmr_file']
#         abc = request.POST.getlist('xmr_det')
#         for data in abc:
#             test = RO_Material_XMR_Info.objects.get(id=data)
#             test.vendor_send = 1
#             test.physical_status = 0
#             test.as_accepted = 0
#             test.pa_result = 0
#             test.pa_result_submitted = 0
#             test.pa_report_flag = 0
#             test.xmr_rej_gp_flag = 0
#             test.xmr_rej_gp_submitted = 0
#             test.as_issue_mat = 0
#             test.single_reject_by_nabl=0
#             test.machine_reject_by_nabl=0
#             test.ph_reject_by_nabl=0
#             test.save()

#         unecono = request.POST.getlist('uneco')
#         for data1 in unecono:
#             test1 = RO_Material_XMR_Info.objects.get(id=data1)
#             test1.uneco_status = 1
#             test1.save()

        
#         data2 = material_offer(ro=ro,all_xmr_rprt=combined_xmr_report, quanity_offered=quantity_dtr_repair)
#         data2.save()


#         ro = RO_Info.objects.get(id=id)
#         dis=ro.rca_cell.Discom
#         reg=ro.rca_cell.Region
       
#         officer=Officer.objects.all()
#         for i in officer:
#             if i.Discom==dis and i.Region==reg and i.role.Role_Name =='RCA(Cell)':

#                 sms_number=i.mobile
#                 off=i.employ_name
#                 ro = RO_Info.objects.get(id=id)
#                 ven=ro.wo.vendor_id.CompanyName_E
#                 xmr="DTR dispatch information"
#                 rel="Release"
#                 rel_num="RO00"+str(ro.id)
               

#                 header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                 proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
#                 url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007143029691256383&mobile_number=" + str(sms_number) + "&v1=" + str(off) + "&v2=" + str(ven) + "&v3=" + str() + "&v4=" + str(xmr) + "&v5=" + str(rel) + "&v6=" + str(rel_num)
#                 response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
#                 sms_template = message_template_log(template_id = '1007143029691256383',date = datetime.now(),mobile_number = sms_number)
#                 sms_template.save()
		
#         officer=Officer.objects.all()
#         for i in officer:
#             if i.Discom==dis and i.Region==reg and i.role.Role_Name =='GM(Store)':
#                 as_of=AreaStore_Officer.objects.all()
#                 for j in as_of:
#                     ro = RO_Info.objects.get(id=id)
#                     if j.Officer==i and j.AreaStore==ro.store:

#                         sms_number=i.mobile
#                         off=i.employ_name
#                         ro = RO_Info.objects.get(id=id)
#                         ven=ro.wo.vendor_id.CompanyName_E
#                         xmr="DTR dispatch information"
#                         rel="Release"
#                         rel_num="RO00"+str(ro.id)
                    
#                         header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
#                         proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
#                         url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007143029691256383&mobile_number=" + str(sms_number) + "&v1=" + str(off) + "&v2=" + str(ven) + "&v3=" + str() + "&v4=" + str(xmr) + "&v5=" + str(rel) + "&v6=" + str(rel_num)

#                         response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
#                         sms_template = message_template_log(template_id = '1007143029691256383',date = datetime.now(),mobile_number = sms_number)
#                         sms_template.save()


#         ro = RO_Info.objects.get(id=id)
#         xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,xmr_rej_gp_flag=1, vendor_send=0) | Q(ro=ro,as_issue_mat=1, vendor_send=0))
#         material = RO_Material_Info.objects.filter(ro_id=ro)
#         return render(request, 'vendor/repaired_dtr_by_vendor_view.html',
#                         {'ro': ro, "material": material, "xmr": xmr})

#     ro = RO_Info.objects.get(id=id)
#     xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,xmr_rej_gp_flag=1, vendor_send=0) | Q(ro=ro,as_issue_mat=1, vendor_send=0))
#     material = RO_Material_Info.objects.filter(ro_id=ro)
#     return render(request, 'vendor/repaired_dtr_by_vendor_view.html',
#                   {'ro': ro, "material": material, "xmr": xmr})



def repaired_dtr_by_vendor_view(request, id):
    if request.method == "POST":
        quantity_dtr_repair = request.POST.get("quantity")

        ro = RO_Info.objects.get(id=id)
        combined_xmr_report = request.FILES['all_xmr_file']
        abc = request.POST.getlist('xmr_det')
        for data in abc:
            test = RO_Material_XMR_Info.objects.get(id=data)
            test.vendor_send = 1
            test.xmr_ven_dispatch_date=date.today()
            test.physical_status = 0
            test.as_accepted = 0
            test.pa_result = 0
            test.pa_result_submitted = 0
            test.pa_report_flag = 0
            test.xmr_rej_gp_flag = 0
            test.xmr_rej_gp_submitted = 0
            test.as_issue_mat = 0
            test.single_reject_by_nabl=0
            test.machine_reject_by_nabl=0
            test.ph_reject_by_nabl=0
            test.save()
            ro = RO_Info.objects.get(id=id)
            ro.ro_ven_dis_flag=1
            ro.ro_ven_dis_date=date.today()
            ro.save()

        unecono = request.POST.getlist('uneco')
        for data1 in unecono:
            test1 = RO_Material_XMR_Info.objects.get(id=data1)
            test1.uneco_status = 1
            test1.save()

        
        data2 = material_offer(ro=ro,all_xmr_rprt=combined_xmr_report, quanity_offered=quantity_dtr_repair)
        data2.save()


        ro = RO_Info.objects.get(id=id)
        dis=ro.rca_cell.Discom
        reg=ro.rca_cell.Region
       
        officer=Officer.objects.all()
        for i in officer:
            if i.Discom==dis and i.Region==reg and i.role.Role_Name =='RCA(Cell)':

                sms_number=i.mobile
                off=i.employ_name
                ro = RO_Info.objects.get(id=id)
                ven=ro.wo.vendor_id.CompanyName_E
                xmr="DTR dispatch information"
                rel="Release"
                rel_num="RO00"+str(ro.id)
               

                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007143029691256383&mobile_number=" + str(sms_number) + "&v1=" + str(off) + "&v2=" + str(ven) + "&v3=" + str() + "&v4=" + str(xmr) + "&v5=" + str(rel) + "&v6=" + str(rel_num)
                response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                sms_template = message_template_log(template_id = '1007143029691256383',date = datetime.datetime.now(),mobile_number = sms_number)
                sms_template.save()
		
        officer=Officer.objects.all()
        for i in officer:
            if i.Discom==dis and i.Region==reg and i.role.Role_Name =='GM(Store)':
                as_of=AreaStore_Officer.objects.all()
                for j in as_of:
                    ro = RO_Info.objects.get(id=id)
                    if j.Officer==i and j.AreaStore==ro.store:

                        sms_number=i.mobile
                        off=i.employ_name
                        ro = RO_Info.objects.get(id=id)
                        ven=ro.wo.vendor_id.CompanyName_E
                        xmr="DTR dispatch information"
                        rel="Release"
                        rel_num="RO00"+str(ro.id)
                    
                        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007143029691256383&mobile_number=" + str(sms_number) + "&v1=" + str(off) + "&v2=" + str(ven) + "&v3=" + str() + "&v4=" + str(xmr) + "&v5=" + str(rel) + "&v6=" + str(rel_num)

                        response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                        sms_template = message_template_log(template_id = '1007143029691256383',date = datetime.datetime.now(),mobile_number = sms_number)
                        sms_template.save()


        ro = RO_Info.objects.get(id=id)
        xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,xmr_rej_gp_flag=1, vendor_send=0) | Q(ro=ro,as_issue_mat=1, vendor_send=0))
        material = RO_Material_Info.objects.filter(ro_id=ro)
        return render(request, 'vendor/repaired_dtr_by_vendor_view.html',
                        {'ro': ro, "material": material, "xmr": xmr})

    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(Q(ro=ro,xmr_rej_gp_flag=1, vendor_send=0) | Q(ro=ro,as_issue_mat=1, vendor_send=0))
    material = RO_Material_Info.objects.filter(ro_id=ro)
    return render(request, 'vendor/repaired_dtr_by_vendor_view.html',
                  {'ro': ro, "material": material, "xmr": xmr})




                  
# def rca_repaired_capacity_view(request,id):
#     ro = RO_Info.objects.get(id=id)
#     xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
#     material = RO_Material_Info.objects.filter(ro_id=ro)
#     mo=material_offer.objects.filter(ro_id=ro) 
#     return render(request,'vendor/rca_repaired_capacity_view.html',{'ro': ro, "material": material, "xmr": xmr,'mo':mo})

def rca_di_issue(request):
    data = RO_Info.objects.all()
    return render(request,'vendor/rca_di_issue.html',{'data': data})

def rca_ven_di_issue_view(request,id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    mo=material_offer.objects.filter(ro_id=ro) 
    return render(request, 'vendor/rca_ven_di_issue_view.html', {'ro': ro, "material": material, "xmr": xmr,'mo':mo})


def rca_all_dispatch_instruction(request):
    mo=material_offer.objects.all()
    return render(request,'vendor/rca_all_dispatch_instruction.html',{"data_info":mo})


def vendor_matria_view(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id

    if Vendor_Material_Details.objects.filter(user_id=user_id).exists():
        m_data = Vendor_Material_Details.objects.filter(user_id=user_id)
        return render(request,'vendor/material_data.html',{'m_data':m_data})

    else:
        return HttpResponse("Not Have any material")


def Material_Delete(request,id):
    Vendor_Material_Details.objects.filter(id=id).delete()
    return redirect('/vendor/new')        

def rca_bg_order_list(request):
    # mobile_no = request.session['mobile_no']
    # user = User_Registration.objects.get(ContactNo=mobile_no,rca_vendor=1)
    # data = WO_Info.objects.filter(
    #     vendor_id=user.User_Id, digi_flag=1).order_by("-id")


    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1).order_by("-id")
    return render(request, 'vendor/rca_bg_order_list.html', {"data": data})
	
def rca_ven_bg_save(request, id):
    data = WO_Info.objects.get(id=id)
    if data.rca_bg_status == 1:
        data = WO_Info.objects.get(id=id)
        return render(request, 'vendor/rca_bg_submit_saved.html', {"data": data})
    else:

        if request.method == "POST":
            bgbank = request.POST.get('bgbank')
            account_owner_name=request.POST.get('acc_holder_name')
            ac_number = request.POST.get('account_no')
            ifsc = request.POST.get('ifsc')
            bg_no = request.POST.get('bg_no')
            amount = request.POST.get('amount')
            bg_issu_date = request.POST.get('bg_issu_date')
            bg_valid_upto = request.POST.get('bg_valid_upto')
            bg_claim_date=request.POST.get('claim_date')
            upload_bg = request.FILES['bg_upload']
            data = WO_Info.objects.get(id=id,digi_flag=1)
            data.bg_bank = bgbank
            data.Account_Holder_Name=account_owner_name
            data.bg_no = bg_no
            data.issue_date = bg_issu_date
            data.valid_date = bg_valid_upto
            data.claim_date = bg_claim_date
            data.amount = amount
            data.ac_number = ac_number
            data.ifsc = ifsc
            data.rca_bg_upload= upload_bg
            data.rca_bg_status = 1
            data.rca_bg_submitted = 1
            data.rca_bg_accept = 0
            data.rca_bg_remark_flag = 0
            data.save()
            data = WO_Info.objects.get(id=id, rca_bg_status=1, digi_flag=1)
            return render(request, 'vendor/rca_bg_submit_saved.html', {"data": data})
        data = WO_Info.objects.get(id=id, rca_bg_status=0, digi_flag=1)
        return render(request, 'vendor/rca_bg_submit.html', {"data": data})


def rca_vendor_bg_accept_list(request):
    # mobile_no = request.session['mobile_no']
    # user = User_Registration.objects.get(ContactNo=mobile_no,rca_vendor=1)
    # data = WO_Info.objects.filter(
    #     vendor_id=user.User_Id, digi_flag=1,rca_bg_accept=1).order_by("-id")

    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1,rca_bg_accept=1).order_by("-id")
    return render(request, 'vendor/rca_vendor_bg_accept_list.html', {"data": data})
    
    
def rca_ven_bg_acceptance_details(request,id):
    data = WO_Info.objects.get(id=id,rca_bg_accept=1)
    return render(request, 'vendor/rca_ven_bg_acceptance_details.html',{"data":data})

def RCA_vendor_release_list(request, id):
    vd = WO_Info.objects.get(id=id)
    rd = RO_Info.objects.filter(wo=vd.id,digi_flag_ro=1)
    return render(request, 'vendor/RCA_vendor_release_list.html', {"data": rd})

def RCA_vendor_dtr_order_list(request):

    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1,rca_bg_accept=1)
    return render(request, 'vendor/RCA_vendor_dtr_order_list.html',
                  {"data": data})    
    
def repaired_dtr_by_vendor_release_list(request, id):
    vd = WO_Info.objects.get(id=id)
    data = RO_Info.objects.filter(wo=vd.id)
    return render(request, 'vendor/repaired_dtr_by_vendor_release_list.html', {'data': data})    



# meeting Code


def vendor_matria_view(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    if Vendor_Material_Details.objects.filter(user_id=user_id).exists():
        m_data = Vendor_Material_Details.objects.filter(user_id=user_id)
        return render(request,'vendor/material_data.html',{'m_data':m_data})
    else:
        return HttpResponse("Not Have any material")






def PO_Material_View(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data1  = Purchase_Order.objects.filter(vendor=data,po_send_to_approval_status = 1,po_approved_status = 1)
    return render(request, 'vendor/po_material_offer.html', {"data": data1})


def view_po_material(request,id):
    po = Purchase_Order.objects.get(id=id)
    Material = PO_Material.objects.filter(po=po)
    return render(request,'vendor/offer_material_view.html',{'Material':Material})


def single_material_offer(request,id):
    offer = PO_Material.objects.get(id=id)
    return render(request,'vendor/vendor_generate_di.html',{'data':offer})

#---------------------------------------view offered Material--------------------------------------------
def po_view_offered(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data1  = Purchase_Order.objects.filter(vendor=data,po_send_to_approval_status = 1,po_approved_status = 1)
    # material = PO_Material.objects.filter(po=data1)
    return render(request, 'vendor/po_offered_view.html', {"data":data1})

def po_view_offered_material(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    # data1  = Purchase_Order.objects.filter(vendor=data,po_send_to_approval_status = 1,po_approved_status = 1)
    # material = PO_Material.objects.filter(po=data1)
    offered = PO_Material_Offer.objects.filter(po__vendor=data, po__id=id, po__po_approved_status = 1).order_by('-id')
    return render(request, 'vendor/po_offered_material_view.html', {"material":offered})
 
def view_offered_details(request, id):
    # data = Purchase_Order.objects.filter(id=po_id)
    offered = PO_Material_Offer.objects.get(id = id)
    material_data = PO_Material.objects.get(id = offered.material.id)
    dispatch_info = PO_Material_Offer_Serial_No.objects.filter(offer=offered.id)
    return render(request, 'vendor/material_offered_details.html', {"dispatch_info": dispatch_info, 'offer': offered, 'material_data': material_data})
#-------------------------------------------------end-------------------------------------------------------------------------------------------------------

def vendor_dispatch_B2(request, po_id):
    offer = PO_Material.objects.get(id=po_id)
    if request.method == "POST":
        quantity = (request.POST.get('quantity'))
        request.session['quantity'] = quantity
        data = Purchase_Order.objects.filter(id=po_id)
        offer = PO_Material.objects.get(id=po_id)
        if float(quantity)>(offer.remaining_qty):
            return render(request, 'vendor/vendor_generate_di.html', {"data": offer, "msg": "You can't offer quantity more than remaining quantity"})
        return render(request, 'vendor/vendor_generate_di2.html',
                      {"quantity1": quantity,"offer":offer})
    data = Purchase_Order.objects.filter(id=po_id)
    return render(request, 'vendor/vendor_generate_di.html', {"data": offer})



def vendor_offer_xmr_save(request, po_id):
    if request.method == "POST":
        quantity = request.session['quantity']
        routine_report_file = request.FILES['file']
        readiness_date=request.POST.get('readiness_date')
        input_serial_no=request.POST.get('input_serial_no')
        data = PO_Material.objects.get(id=po_id)
        
        # data.Offer = 1
        # data.save()
        total_qty = data.Quantity
        po_exist_data = PO_Material_Offer.objects.filter(po = data.po, material =data , item_code = data.item_code, status=1).order_by('id')
        if len(po_exist_data)>0:
            if len(po_exist_data) > 1:
                i = po_exist_data.last()
                dis_qty = i.dispatch_qty
                dispatch_quantity = float(dis_qty)+float(quantity)

                rem_qty = i.remaining_qty
                remaining_qty =+ rem_qty
                remaining_quantity = float(remaining_qty)-float(quantity)
            else:
                i = po_exist_data
                for j in i:
                    dis_qty = j.dispatch_qty
                    dispatch_quantity =float (dis_qty)+float(quantity)

                    rem_qty = j.remaining_qty
                    remaining_qty =+ rem_qty
                    remaining_quantity = float(remaining_qty)-float(quantity)        

        else:
            dispatch_quantity = quantity
            remaining_quantity = float(total_qty)-float(quantity)

        
        data.remaining_qty =remaining_quantity
        data.dispatch_qty = dispatch_quantity
        data.save()
        if remaining_quantity == 0:
            data.Offer = 1
            data.save()

        Material_Offer = PO_Material_Offer(po=data.po,material = data, Offer_Quantity = (quantity), status=1, total_quantity = total_qty,
        item_name = data.specification,dispatch_qty =  dispatch_quantity ,remaining_qty= remaining_quantity, item_code = data.item_code,routine_report_file = routine_report_file,  input_serial_no=input_serial_no, readiness_date=readiness_date, date = dtm.now())
        Material_Offer.save()
     
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data1  = Purchase_Order.objects.filter(vendor=data, po_approved_status = 1)
        return render(request, 'vendor/po_material_offer.html', {"data": data1, "msg1":'Material offered successfully'})
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data1  = Purchase_Order.objects.filter(vendor=data, po_approved_status = 1)
    return render(request, 'vendor/po_material_offer.html', {"data": data1})

    
def Dispatch_item(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    data1  = DI_Master.objects.filter(vendor=data,vendor_deliverable_status=False,di_approved_status=1).order_by('-id')
    return render(request, 'vendor/dispatch_item.html', {"data": data1})
    
def view_di_material(request,id,erp_di_no):
    di_update_data1 = DI_Master.objects.get(id=id)
    po_data= Purchase_Order.objects.get(id=di_update_data1.po.id)
    Material = DI_Areastores.objects.filter(po=po_data,status=False,p_varification=False, di_master__erp_di_number = erp_di_no)
    return render(request,'vendor/offer_di_material_view.html',{'Material':Material, 'erp_di_no':erp_di_no})
    
    
def Enter_serial(request,id):
    offer = DI_Areastores.objects.get(id=id)
    return render(request,'vendor/vendor_serial.html',{'data':offer})
    
def vendor_dispatch_di_new(request, id):
    if request.method == "POST":
        offer = DI_Areastores.objects.get(id=id)
        # quantity = int(request.POST.get('quantity'))
        quantity =  offer.deliverable_qty
        request.session['quantity'] = float(quantity)
        # data = Purchase_Order.objects.filter(id=po_id)
        return render(request, 'vendor/vendor_generate_di_new.html',
                      {"quantity": float(quantity), "quantity1": quantity,"data":offer})
    data = DI_Areastores.objects.get(id=id)
    return render(request, 'vendor/vendor_serial.html', {"data": data})
    

def vendor_offer_di_save(request, id):
    data1 = DI_Areastores.objects.get(id=id)
    input_excel_type = request.POST.get('excel_type')
    if input_excel_type == 'serial_nos':
        quantity = request.session['quantity'] 
        material_data = request.FILES["myfile"]
        data2 = pd.read_excel(material_data)
        for column in data2:
            no_list = data2[column].values
            item_no_list = list(no_list)

        if quantity != len(item_no_list):
            return render(request, 'vendor/vendor_generate_di_new.html',
                      {"msg2": "Count of serial number should be equal to offer quantity","quantity": range(quantity), "quantity1": quantity,"data":data1})
        
        if len(item_no_list) != len(set(item_no_list)):
            return render(request, 'vendor/vendor_generate_di_new.html',
                      {"msg2": "You cannot enter same serial number in excel","quantity": range(quantity), "quantity1": quantity,"data":data1})

        data1.status = True
        data1.delivered_status = True
        # data1.di_master.vendor_deliverable_status = True
        data1.save()
        for data in item_no_list:
            try:
                data_new = data.replace('/','-')
            except:
                data_new = data
            Offer_Serial_No = DI_Material_Offer_Serial_No(area_store_id=data1,po=data1.po,offer = PO_Material_Offer.objects.latest('id'),serial_no=data_new,area_store=data1.areastore,Offer_status=1,material=data1.offer_item.material.specification,status=1)
            Offer_Serial_No.save()
        data = User_Registration.objects.get(Otp=request.session['otp'])
        data1  = DI_Master.objects.filter(vendor=data,vendor_deliverable_status=False,di_approved_status=1).order_by('-id')
        return render(request, 'vendor/dispatch_item.html', {"data": data1,"msg2": "Material Dispatch requested Succefully"})

    elif input_excel_type == 'batch_nos':
        serial_excel = request.FILES['myfile']
        df = pd.read_excel(serial_excel)
        batch_list = df['batch_no/lot_no/drum_no'].tolist()
        qty_list = df['total_quantity'].tolist()
        zipped_list = zip(batch_list,qty_list)

        # if int(offer_data.quantity) != sum(qty_list):
        #     return render(request,'wo/serial_excels_upload_option.html',{"con": con, 'boq_data': boq_data,"sitestore_data":sitestore_data,"updated_store_data":updated_store_data,"wo_id":wo_id,"vendor_id":vendor_id,"offer_data":offer_data,"msg1":"Offered quantity is not equal to batch/lot/drum mentioned quantities"})
        for i,j in zipped_list:
            Offer_Serial_No = DI_Material_Offer_Serial_No(area_store_id=data1,po=data1.po,offer = PO_Material_Offer.objects.latest('id'), area_store=data1.areastore,Offer_status=1,material=data1.offer_item.material.specification,status=1,batch_no = i, batch_qty = j)
            Offer_Serial_No.save()
        data1.status = True
        data1.delivered_status = True
        # data1.di_master.vendor_deliverable_status = True
        data1.save()

        data = User_Registration.objects.get(Otp=request.session['otp'])
        data1  = DI_Master.objects.filter(vendor=data,vendor_deliverable_status=False,di_approved_status=1).order_by('-id')
        return render(request, 'vendor/dispatch_item.html', {"data": data1,"msg2": "Material Dispatch requested Succefully"})


#------------------------------------------po resubmit item at areastore------------------------------------
def view_di_material_reject(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    #data1  = DI_Master.objects.filter(vendor=data,vendor_deliverable_status=False,di_approved_status=1)
    Material = DI_Areastores.objects.filter(po__vendor=data,status=False, p_varification=True, gatepass=1 )
    return render(request,'vendor/offer_di_material_view_reject.html',{"data":Material })

def view_di_material_resubmit(request,id):
    di_update_data1 = DI_Master.objects.get(id=id)
    po_data= Purchase_Order.objects.get(id=di_update_data1.po.id)
    Material = DI_Areastores.objects.filter(di_master_id=id,po=po_data,status=False,p_varification=True)
    #Material = DI_Areastores.objects.filter(po=po_data,status=False,p_varification=True)
    return render(request,'vendor/offer_di_material_view_resubmit.html',{'Material':Material,'dataid':id})


def view_di_material_resubmit_save(request,id,erp_di_no):
    di_update_data1 = DI_Areastores.objects.get(id=id)
    po_data= Purchase_Order.objects.get(id=di_update_data1.po.id)
    Material = DI_Areastores.objects.filter(po=po_data,status=False,p_varification=True)
    Offer_Serial_No = DI_Material_Offer_Serial_No.objects.filter(area_store_id__di_master__erp_di_number=erp_di_no,po=po_data, p_status='-1', accepted=1)
    #Offer_Serial_No = DI_Material_Offer_Serial_No.objects.filter(po=po_data, p_status='-1',accepted=1)
    
    if request.method == 'POST':
        for data in Offer_Serial_No:
            newdata = DI_Areastores.objects.get(id=id)
            # newdata.status = True
            # newdata.p_varification = False
            # newdata.gatepass = 0
            # newdata.save()

            pstatus = request.POST.get(f'{data.id}')
            data.serial_no=pstatus
            data.p_status=0
            data.gatepass = 0
            data.accepted = 0
            data.received_material = 0
            data.save()
            
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        data1 = DI_Areastores.objects.filter(di_master__erp_di_number=erp_di_no,status=False, p_varification=True, gatepass=1 )
        #data1  = DI_Master.objects.filter(vendor=data,vendor_deliverable_status=False,di_approved_status=1)
        return render(request,'vendor/offer_di_material_view_reject.html',{"data": data1})
            
    return render(request,'vendor/offer_di_material_view_resubmit_item.html',{'Offer_Serial_No':Offer_Serial_No,'dataid':id,'erp_di_no':erp_di_no})
#----------------------------------------------------------------end----------------------------------------------------------------

#------------------------------------------PO NABL Rejected Items-------------------------------------------
def nabl_di_material_reject(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    di = DI_Master.objects.filter(po__vendor=data, nabl_status=-1)
    return render(request,'vendor/nabl_di_material_view_reject.html',{"data": di})

def lot_rejected_gatepass_info(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    areastore = DI_Areastores.objects.get(id=id)
    # di = DI_Master.objects.get()
    Material = DI_Areastores.objects.filter(po__vendor=data,samp_rejected_flag=1, send_to_gm=2, gatepass=2, id=id)
    gatepass = DI_nabl_rejected_gatepass.objects.filter(area_store__po__vendor=data,area_store__id = areastore.id).last()
    return render(request,'vendor/lot_rejected_gatepass.html',{'gatepass':gatepass, 'Material':Material})

def nabl_reject_di_areastore(request,id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    di_update_data1 = DI_Master.objects.get(id=id)
    po_data= Purchase_Order.objects.get(id=di_update_data1.po.id)
    Material = DI_Areastores.objects.filter(po__vendor=data,samp_rejected_flag=1, send_to_gm=2, gatepass=2, po=po_data, di_master__id=di_update_data1.id)
    return render(request,'vendor/nabl_rejected_di_area_view.html',{'Material':Material})

def nabl_di_material_reject_view(request,id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    material = DI_Areastores.objects.get(id=id)
    reject_serial = DI_Material_Offer_Serial_No.objects.filter(po__vendor=data,area_store_id__samp_rejected_flag=1,area_store_id=material.id, material=material.offer_item.item_name)
    return render(request, 'vendor/nabl_reject_di_material_view.html', {'data': reject_serial,'dataid':id, 'material':material})
#-------------------------------------------------------end------------------------------------------------------------

def profile_status(request):
    TKC = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if data.Authentication_id:
        aaa = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        cert = aaa.Authentication_id
        to_daaa =datetime.datetime.now()
        return render(request, 'vendor/profile_status.html', {"data11": TKC,'cert':cert,'to_daaa':to_daaa})

    else:
        return render(request, 'vendor/profile_status.html', {"data11": TKC})  




# **********************************

def factory_payment_form(request):
    res = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    if Factory_Form_Details.objects.filter(vendor=res,status=1).exists():
        return HttpResponse("Details Unser Review")
    elif Factory_Form_Details.objects.filter(vendor=res,status=3).exists():
        fd = Factory_Form_Details.objects.get(vendor=res,status=3)
        if request.method == "POST":
            res = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            date = request.POST.get('date')
            file = request.FILES['file']
            po_sd = Factory_Form_Details(vendor=res, date=date, report=file,status=1)
            po_sd.save()
            res.factory_waiver = 1
            res.save()
            return redirect('/vendor/basic')
        
        return render(request, 'vendor/factory_payment_form.html',{'res':res,'fd':fd})
    else:
        if request.method == "POST":
            res = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            date = request.POST.get('date')
            file = request.FILES['file']
            po_sd = Factory_Form_Details(vendor=res, date=date, report=file,status=1)
            po_sd.save()
            res.factory_waiver = 1
            res.save()
            return redirect('/vendor/basic')
        return render(request, 'vendor/factory_payment_form.html',{'res':res})
        
        
        
    
def vednor_new_material(request):
    
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    user_id = data.User_Id
    add_material = Vendor_Material_Details.objects.filter(user_id=user_id)
    if request.method == "POST":
        return redirect('new_material_data')
    data11 = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])

    request.session['otp'] = data.Otp
    return render(request, 'vendor/vendor_new_material.html', {'userdata': data11[0],'employees': add_material})





def new_material_data(request):
    mm = Material_Master.objects.all()
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
   
    if request.method == 'POST':
        try:
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
            material = request.POST.get('Material')
            matrial_name = Vendor_Material_Master.objects.get(Material_Id=material)
            specification = request.POST.get('Specification')
            spec = Vendor_Material_Specification_Master.objects.get(Material_Specification_Id=specification)
            capacity = request.POST.get('capacity')
            unit = request.POST.get('unit')

            if Vendor_Material_Details.objects.filter(user_id=data, Material_Name=matrial_name.Material_Name,Material_Specification=spec.Material_Specification_Name).exists():
                messages.warning(request, "Material with this specification already selected")  
                return render(request, 'vendor/new_material_data.html')  
            else:
                material_obj = Vendor_Material_Details(user_id=data, Material_Name=matrial_name.Material_Name,
                                            Material_Specification=spec.Material_Specification_Name,item_code_ez=spec.Material_Item_Code_WZ,item_code_wz=spec.Material_Item_Code_EZ,
                                            new_material = 1,per_month_capacity=capacity,material_unit=unit
                                            )
                material_obj.save()

        except Exception as e:
            data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
            user_id = data.User_Id
            material = request.POST.get('Material')
            matrial_name = Vendor_Material_Master.objects.get(Material_Id=material)
            specification = request.POST.get('Specification')
            spec = Vendor_Material_Specification_Master.objects.get(Material_Specification_Id=specification)
            capacity = request.POST.get('capacity')
            unit = request.POST.get('unit')
            if Vendor_Material_Details.objects.filter(user_id=data, Material_Name=matrial_name.Material_Name,Material_Specification=spec.Material_Specification_Name).exists():
                messages.warning(request, "Material with this specification already selected")  
                return render(request, 'vendor/new_material_data.html') 
            else:
                material_obj = Vendor_Material_Details(user_id=data, Material_Name=matrial_name.Material_Name,
                                            Material_Specification=spec.Material_Specification_Name,item_code_ez=spec.Material_Item_Code_WZ,item_code_wz=spec.Material_Item_Code_EZ,
                                            new_material = 1,per_month_capacity=capacity,material_unit=unit
                                            )
                material_obj.save()

        return redirect('vednor_new_material')
    return render(request, 'vendor/new_material_data.html',{'mm':mm,'data':data} )
    

def delete_reject_material_delete(request, id):
    vendor = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type'])
    employee = Vendor_Material_Details.objects.get(id=id)
    if request.method == 'POST':
        employee.delete()
        vendor.update(work_approval=0)
        return redirect('/vendor/rejected_doc')

    context = {
        'employee': employee,
    }
    return render(request, 'vendor/reject_doc_resubmit.html', {'employee':employee})	
	

def material_submit(request):
    data_new = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
    
    if Vendor_Material_Details.objects.filter(user_id = data_new.User_Id).exists():
        data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            data1.page_9 = 1
            data1.save()
        else:
            user = User_Registration_Check_Status(User=data,page_9=1)
            user.save()
        return redirect('/vendor/vendor_reg_eleven')

    else:
        messages.warning(
        request, "Kindly add atleast 1 material")
        return redirect('/vendor/new')   


import pandas as pd
import os
def download_demo_excel(request):
    excel_path = os.path.abspath('media/demo_excel.xlsx')
    # file_path = excel_path+"\\media\\demo_excel.xlsx"
    df = pd.read_excel(excel_path)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Material_serial_no.xlsx"'
    df.to_excel(response, index = False)
    return response    

def rejected_new_material(request):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
   
    data3 = Vendor_Material_Details.objects.filter(user_id=data,Primary_verification_Status=2,
        new_material=2)
    return render(request, 'vendor/rejected_new_material.html', {"data": data,"data3":data3})




def rejected_new_material_save(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'],User_type = request.session['User_type'])
        
    if request.method == "POST":
       
        data1 = Vendor_Material_Details.objects.get(id=id)
        upload_file1 = request.FILES['file4']
        upload_file2 = request.FILES['file5']
        upload_file3 = request.FILES['file6']
        data1.Material_Test_Doc = upload_file1
        data1.Material_GTP_Doc = upload_file2
        data1.Material_Other_Doc = upload_file3

        data1.Primary_verification_Status = 0
        data1.new_material = 1
        data1.save()
        data = User_Registration.objects.get(
            ContactNo=request.session['uid'],User_type = request.session['User_type'])
        user_id = data.User_Id
        data.add_material = 2
        data.save()
        
        data3 = Vendor_Material_Details.objects.filter(user_id=data,Primary_verification_Status=2,new_material = 2)
        return render(request, 'vendor/rejected_new_material.html', {"data": data,'data3':data3})
    return render(request, 'vendor/base1.html', {"data": data})

######### dtr status

def rca_ven_pass_order_list(request):
    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id).order_by("-id")
    return render(request, 'vendor/rca_ven_pass_order_list.html', {'data': data})


def rca_ven_pass_release_list(request,id):
    vd = WO_Info.objects.get(id=id)
    data = RO_Info.objects.filter(wo=vd.id)
    return render(request, 'vendor/rca_ven_pass_release_list.html', {'data': data})



def rca_ven_pass_dtr_list(request,id):
    ro = RO_Info.objects.get(id=id)
    xmr = RO_Material_XMR_Info.objects.filter(ro=ro)
    material = RO_Material_Info.objects.filter(ro_id=ro)
    return render(request, 'vendor/rca_ven_pass_dtr_list.html',{'xmr_t': xmr,'material':material})



# -------------- shubham tripathi code start from here ---------------
from django.db.models import Sum
from main.views import *
from django.db.models import Count
curl=settings.CURRENT_URL

def vendor_po_invoice_list(request): 
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "VENDOR" and supplier.blacklisted == 0 :
            # if Purchase_Order.objects.filter(~Q(status=-1),vendor__User_Id=supplier.User_Id,po_approved_status=1).exists():
            po_data = Purchase_Order.objects.annotate(total_invoice_ammount=Sum('purchase_order_data__total_invoice_amount')).filter(~Q(status=-1),vendor__User_Id=supplier.User_Id,po_approved_status=1).order_by('-id')
            pomd = PO_Material.objects.values('po').annotate(total_amount=Sum('total_amount'))
            return render(request, 'vendor_invoice/vendor_po_invoicelist.html', {'supplier': supplier,'po_data':po_data,'pomd':pomd})
        else:
            return redirect('/vendor/basic')
    else:
        return redirect(curl)

def vendor_invoice_list(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    po_id=request.GET.get('poid')
    print("po_id--------------------------",po_id)
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "VENDOR" and supplier.blacklisted == 0 :
            if Purchase_Order.objects.filter(~Q(status=-1),vendor_id__User_Id=supplier.User_Id,po_approved_status=1,id=po_id).exists():
                in_data=Invoice.objects.filter(~Q(status=-1),purchase_order_id__vendor__User_Id=supplier.User_Id,purchase_order_id=po_id).order_by('-id')
                po_data = Purchase_Order.objects.filter(~Q(status=-1),vendor__User_Id=supplier.User_Id,po_approved_status=1,id=po_id).last()
                pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
                in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
                return render(request, 'vendor_invoice/vendor_invoicelist.html', {'supplier': supplier,'in_data':in_data,"po_data":po_data,'pomd':pomd,'in_amount':in_amount})
            else:
                po_data=""
                in_data=""
                return render(request, 'vendor_invoice/vendor_invoicelist.html', {'supplier': supplier,'in_data':in_data,"po_data":po_data,})
        else:
            return redirect('/vendor/basic')
    else:
        return redirect(curl)

def vendor_invoice_generate(request):
    supplier = User_Registration.objects.filter(Otp=request.session['otp'],User_type = request.session['User_type']).last()
    if supplier is not None:
        if supplier.cgm_approval==1 and supplier.User_type == "VENDOR" and supplier.blacklisted == 0:
            if request.method =="POST":
                po_id=request.POST.get('po_id')
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
                        itd=Invoice(user_id=supplier.User_Id,purchase_order_id=po_id,invoicetype_id=invoicetype,invoice_number=invoice_no,invoice_amount_sgst=invoice_amount_sgst,invoice_amount_cgst=invoice_amount_cgst,invoice_amount_withought_taxes=invoice_amount_withought_taxes,total_invoice_amount=total_invoice_amount,invoice_pdf=invoice_pdf,bg_document=bg_pdf,bg_acceptance_letter=bg_acceptance_letter,invoice_date=invoice_date,remark=invoice_remark,supporting_document_name=supporting_document_name,supporting_document=supporting_document).save()
                    except Exception as e:
                        pass
                else:
                    itd=Invoice(user_id=supplier.User_Id,purchase_order_id=po_id,invoicetype_id=invoicetype,invoice_number=invoice_no,invoice_amount_sgst=invoice_amount_sgst,invoice_amount_cgst=invoice_amount_cgst,invoice_amount_withought_taxes=invoice_amount_withought_taxes,total_invoice_amount=total_invoice_amount,invoice_pdf=invoice_pdf,bg_document=bg_pdf,bg_acceptance_letter=bg_acceptance_letter,invoice_date=invoice_date,remark=invoice_remark).save()
                return redirect(vendor_po_invoice_list)
            else:
                po_id=request.GET.get('poid')
                it_data=InvoiceType.objects.filter(~Q(status=-1))
                po_data = Purchase_Order.objects.filter(~Q(status=-1),vendor__User_Id=supplier.User_Id,po_approved_status=1,id=po_id).last()
                in_amount=Invoice.objects.filter(status=1,dgm_em_status=1,purchase_order_id=po_id).aggregate(Sum('total_invoice_amount'))
                pomd = PO_Material.objects.filter(~Q(status=-1),po_id=po_id).aggregate(Sum('total_amount'))
                return render(request, 'vendor_invoice/create_vendor_invoice.html', {'supplier': supplier,"po_data":po_data,"it_data":it_data,'pomd':pomd,"in_amount":in_amount})
        else:
            return redirect('/vendor/basic')
    else:
        return redirect(curl)




###### Multiple BG RCA #####

  
    
def add_bg(request):
    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1,rca_bg_accept=1).order_by("-id")
    return render(request, 'vendor/additional_bg_order_list.html',{"data": data})


def add_bg_save(request,id):
    data = WO_Info.objects.get(id=id,rca_bg_status=1,rca_bg_accept=1)
    if request.method == "POST":
        bgbank = request.POST.get('bgbank')
        account_owner_name=request.POST.get('acc_holder_name')
        ac_number = request.POST.get('account_no')
        ifsc = request.POST.get('ifsc')
        bg_no = request.POST.get('bg_no')
        amount = request.POST.get('amount')
        bg_issu_date = request.POST.get('bg_issu_date')
        bg_valid_upto = request.POST.get('bg_valid_upto')
        bg_claim_date=request.POST.get('claim_date')
        upload_bg = request.FILES['bg_upload']
        mul_bg = Multiple_Bg( wo=WO_Info.objects.get(id=id,rca_bg_status=1),add_bg_bank=bgbank,add_bg_no=bg_no,add_amount=amount,
                                add_ac_number=ac_number,add_ifsc=ifsc,add_Account_Holder_Name=account_owner_name,add_bg_upload=upload_bg,
                                add_issue_date=bg_issu_date,add_valid_date=bg_valid_upto,add_claim_date=bg_claim_date)
        
        mul_bg.save()
        mul_bg = Multiple_Bg.objects.latest("id")
        mul_bg.add_bg_status = 1
        mul_bg.add_bg_submitted = 1
        mul_bg.save()
    

        return render(request,'vendor/add_bg_save.html',{"data": data,"mul_bg":mul_bg})
    data = WO_Info.objects.get(id=id, rca_bg_status=1, digi_flag=1)
    bg=Multiple_Bg.objects.filter(wo=data)
    return render(request, 'vendor/add_bg.html', {"data": data,'bg':bg})





# def add_bg_accept_list(request):
#     otp_det = request.session['otp_two']
#     user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
#     # wo = WO_Info.objects.filter(vendor_id=user.User_Id, digi_flag=1,rca_bg_accept=1).order_by("-id")
#     data = Multiple_Bg.objects.filter(Q(add_bg_accept=1) | Q(add_bg_accept=-1)).order_by("-id")
#     lst=[]
#     for i in data:
#         i.wo.vendor_id==user.User_Id
#         lst.append(i)
    
#     return render(request, 'vendor/add_bg_accept_list.html', {"data": lst})



def add_bg_accept_list(request):
    otp_det = request.session['otp_two']
    user = Rca_User_Registration.objects.get(Otp=otp_det,cgm_approval=1)
    data = Multiple_Bg.objects.all().order_by("-id")
    lst=[]
    for i in data:
        i.wo.vendor_id==user.User_Id
        lst.append(i)
    
    return render(request, 'vendor/add_bg_accept_list.html', {"data": lst})



# def add_bg_acceptance_details(request,id):
#     data = Multiple_Bg.objects.get(id=id)
   
    
#     if data.add_bg_accept==-1:
#         data = Multiple_Bg.objects.get(id=id)
#         return render(request, 'vendor/add_bg_resubmit.html',{"data":data})
    
#     elif data.add_bg_accept==1:
#         data = Multiple_Bg.objects.get(id=id)
#         return render(request, 'vendor/add_bg_acceptance_details.html',{"data":data})
    
#     data = Multiple_Bg.objects.get(id=id)
    
#     return render(request, 'vendor/add_bg_acceptance_details.html',{"data":data})


def add_bg_acceptance_details(request,id):
    data = Multiple_Bg.objects.get(id=id)
    
    if data.add_bg_accept==-1:
        data = Multiple_Bg.objects.get(id=id)
        return render(request, 'vendor/add_bg_resubmit.html',{"data":data})
    
    elif data.add_bg_accept==1:
        data = Multiple_Bg.objects.get(id=id)
        return render(request, 'vendor/add_bg_acceptance_details.html',{"data":data})
    
    elif data.add_bg_accept==0:
        data = Multiple_Bg.objects.get(id=id)
        return render(request, 'vendor/add_bg_acceptance_details.html',{"data":data})
    
    data = Multiple_Bg.objects.get(id=id)
    
    return render(request, 'vendor/add_bg_acceptance_details.html',{"data":data})


def add_bg_resubmit_save(request,id):
    data = Multiple_Bg.objects.get(id=id)
    if request.method == "POST":
        bgbank = request.POST.get('bgbank')
        account_owner_name=request.POST.get('acc_holder_name')
        ac_number = request.POST.get('account_no')
        ifsc = request.POST.get('ifsc')
        bg_no = request.POST.get('bg_no')
        amount = request.POST.get('amount')
        bg_issu_date = request.POST.get('bg_issu_date')
        bg_valid_upto = request.POST.get('bg_valid_upto')
        bg_claim_date=request.POST.get('claim_date')
        upload_bg = request.FILES['bg_upload']
        
        data = Multiple_Bg.objects.get(id=id)
        data.add_bg_bank=bgbank
        data.add_bg_no=bg_no
        data.add_amount=amount
        data.add_ac_number=ac_number
        data.add_ifsc=ifsc
        data.add_Account_Holder_Name=account_owner_name
        data.add_bg_upload=upload_bg
        data.add_issue_date=bg_issu_date
        data.add_valid_date=bg_valid_upto
        data.add_claim_date=bg_claim_date 
        data.add_bg_status = 1
        data.add_bg_submitted = 1
        data.add_bg_accept=0
        data.save()
        data = Multiple_Bg.objects.get(id=id)
        return render(request, 'vendor/add_bg_resubmit_save.html',{"data":data})
    

