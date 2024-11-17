from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main.models import *
from nabl.models import *
from nabl.serializers import *
from .models import *
from vendor.models import *
import datetime
import random, math
from django.contrib import messages
import io
from rest_framework.parsers import JSONParser
from api.models import NablDTRReport
from django.db.models import Q
from rca.models import *
from fqp.models import *
from tkc.models import*
import requests
from django.conf import settings
curl=settings.CURRENT_URL
# Create your views here.
def nabl_base(request):
    return render(request, 'nabl/nabl_base.html')


def testNabl(request):
    return render(request, 'nabl/nabl_reg8.html')


def basic(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    return render(request, 'nabl/basics.html', {"userdata": data})


def rejected_doc(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    user_id = data.User_Id
    data = NABL_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0)
    data1 = NABL_Document.objects.filter(CGM_verification_Status=4, user_id=user_id, Status=0)
    return render(request, 'nabl/rejected_doc_resubmit.html', {"data": data, "data1": data1})


def rejected_doc_save(request, id):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    user_id = data.User_Id
    data = NABL_Document.objects.filter(id=id, user_id=user_id)
    if request.method == "POST":
        office = request.POST.get('office')
        if office != '':
            data.update(Issued_office_Name=office, Status=1)
        doc_name = request.POST.get('doc_name')
        if doc_name != '':
            data.update(Document_Name=doc_name, Status=1)
        issu_date = request.POST.get('issue_date')
        if issu_date != '':
            data.update(Doc_issue_date=issu_date, Status=1)
        exp_date = request.POST.get('expire_date')
        if exp_date != '':
            data.update(Doc_expiry_date=exp_date, Status=1)
        if len(request.FILES) != 0:
            data = NABL_Document.objects.get(id=id, user_id=user_id)
            upload_file = request.FILES['file']
            data.Ddocfile = upload_file
            data.Status = 1
            data.Primary_verification_Status = 0
            data.save()
            
    data = NABL_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0)
    if data:
        return render(request, 'nabl/rejected_doc_resubmit.html', {"data": data})

    else:
        data1 = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        data1.qc_approval = 0
        data1.save()
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    return render(request, 'nabl/basics.html', {"userdata": data})



def rejected_doc_cgm_save(request, id):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    user_id = data.User_Id
    data = NABL_Document.objects.filter(id=id, user_id=user_id)
    if request.method == "POST":
        
        office = request.POST.get('office')
        if office != '':
            data.update(Issued_office_Name=office, Status=1)
        doc_name = request.POST.get('doc_name')
        if doc_name != '':
            data.update(Document_Name=doc_name, Status=1)
        issu_date = request.POST.get('issue_date')
        if issu_date != '':
            data.update(Doc_issue_date=issu_date, Status=1)
        exp_date = request.POST.get('expire_date')
        if exp_date != '':
            data.update(Doc_expiry_date=exp_date, Status=1)
        if len(request.FILES) != 0:
            data = NABL_Document.objects.get(id=id, user_id=user_id)
            upload_file = request.FILES['file']
            data.Ddocfile = upload_file
            data.save()
    data = NABL_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0)
    if data:
        return render(request, 'nabl/rejected_doc_resubmit.html', {"data": data})
    data = User_Registration.objects.get(ContactNo=request.session['uid'])
    return render(request, 'nabl/basics.html', {"userdata": data})




def nabl_profile(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    userid = data.User_Id
    abcde = UserCompanyDataMain.objects.get(user_id_id=data)
    nabl_document = NABL_Document.objects.filter(user_id=userid)
    return render(request,'nabl/nabl_profile.html',{"basic": data,'nabl_document':nabl_document,'company': abcde})



def nabl_reg7(request):
    if request.method == "POST":
        data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        data.Experience = request.POST.get('work_experience')
        data.Turnover = request.POST.get('turn_over')
        data.save()
        if User_Registration_Check_Status.objects.filter(User=data).exists():
              data1 = User_Registration_Check_Status.objects.get(User=data)
              data1.page_7 = 1
              data1.save()
        else:
            user = User_Registration_Check_Status(User=data,page_7=1)
            user.save()
        Prod = Product.objects.all()
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            if data1.page_12:
                return redirect("nabl_reg13")
            if data1.page_11:
                return redirect("nabl_reg12")
            if data1.page_9:
                return redirect("nabl_reg10")
            if data1.page_8:
                return redirect("nabl_reg9")
            if data1.page_7:
                return redirect("nabl_reg8")
        return render(request, 'nabl/nabl_reg7.html')
    return render(request, 'nabl/nabl_reg7.html')


def nabl_reg8(request):
    if request.method == "POST":
        data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        user_id = data.User_Id
        office_name = request.POST.get('Accreditation_Certificate_office')
        doc_Name = request.POST.get('Accreditation_Certificate_doc_name')
        doc_Issue_date = request.POST.get('Accreditation_Certificate_issue_date1')
        doc_Expire_date = request.POST.get('Accreditation_Certificate_expire_date')
        acc_cert_file = request.FILES['Accreditation_Certificate_file']

        data1 = NABL_Document(user_id=user_id, Types_of_Docs='NABL Accreditation Certificate',
                              Issued_office_Name=office_name, Document_Name=doc_Name, Doc_issue_date=doc_Issue_date,
                              Doc_expiry_date=doc_Expire_date,
                              Ddocfile=acc_cert_file, Status=1)
        data1.save()

        office_name = request.POST.get('Accreditation_office')
        doc_Name = request.POST.get('Accreditation_doc_name')
        doc_Issue_date = request.POST.get('Accreditation_issue_date')
        doc_Expire_date = request.POST.get('Accreditation_issue_date')
        acc_cert_file = request.FILES['Accreditation_file']
        data2 = NABL_Document(user_id=user_id, Types_of_Docs='NABL Scope of Accreditation',
                              Issued_office_Name=office_name, Document_Name=doc_Name, Doc_issue_date=doc_Issue_date,
                              Doc_expiry_date=doc_Expire_date,
                              Ddocfile=acc_cert_file, Status=1)
        data2.save()

        office_name = request.POST.get('Pan_Card_office')
        doc_Name = request.POST.get('Pan_Card_doc_name')
        doc_Issue_date = request.POST.get('Pan_Card_issue_date')
        doc_Expire_date = request.POST.get('Pan_Card_issue_date')
        acc_cert_file = request.FILES['Pan_Card_file']
        data3 = NABL_Document(user_id=user_id, Types_of_Docs='Pan Card Details', Issued_office_Name=office_name,
                              Document_Name=doc_Name, Doc_issue_date=doc_Issue_date, Doc_expiry_date=doc_Expire_date,
                              Ddocfile=acc_cert_file, Status=1)
        data3.save()

        office_name = request.POST.get('GST_office')
        doc_Name = request.POST.get('GST_doc_name')
        doc_Issue_date = request.POST.get('GST_issue_date')
        doc_Expire_date = request.POST.get('GST_issue_date')
        acc_cert_file = request.FILES['GST_file']
        data4 = NABL_Document(user_id=user_id, Types_of_Docs='GST Registration Certificate',
                              Issued_office_Name=office_name, Document_Name=doc_Name, Doc_issue_date=doc_Issue_date,
                              Doc_expiry_date=doc_Expire_date,
                              Ddocfile=acc_cert_file, Status=1)
        data4.save()

        office_name = request.POST.get('Legal_Entity_office')
        if office_name:
            doc_Name = request.POST.get('Legal_Entity_doc_name')
            doc_Issue_date = request.POST.get('Legal_Entity_issue_date')
            doc_Expire_date = request.POST.get('Legal_Entity_issue_date')
            acc_cert_file = request.FILES['Legal_Entity_file']
            data5 = NABL_Document(user_id=user_id, Types_of_Docs='Legal Entity  Document ',
                                  Issued_office_Name=office_name, Document_Name=doc_Name, Doc_issue_date=doc_Issue_date,
                                  Doc_expiry_date=doc_Expire_date,
                                  Ddocfile=acc_cert_file, Status=1)
            data5.save()

        data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        user_id = data.User_Id
        office_name = request.POST.get('Authorisation_office')
        if office_name:
            doc_Name = request.POST.get('Authorisation_doc_name')
            doc_Issue_date = request.POST.get('Authorisation_issue_date')
            doc_Expire_date = request.POST.get('Authorisation_issue_date')
            acc_cert_file = request.FILES['Authorisation_file']
            data6 = NABL_Document(user_id=user_id, Types_of_Docs='Authorisation Document Details',
                                  Issued_office_Name=office_name, Document_Name=doc_Name, Doc_issue_date=doc_Issue_date,
                                  Doc_expiry_date=doc_Expire_date,
                                  Ddocfile=acc_cert_file, Status=1)
            data6.save()

        data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        user_id = data.User_Id
        office_name = request.POST.get('Aadhar_office')
        if office_name:
            doc_Name = request.POST.get('Aadhar_doc_name')
            doc_Issue_date = request.POST.get('Aadhar_issue_date')
            doc_Expire_date = request.POST.get('Aadhar_issue_date')
            acc_cert_file = request.FILES['Aadhar_file']
            data7 = NABL_Document(user_id=user_id, Types_of_Docs='Aadhar Card of Authorised Person',
                                  Issued_office_Name=office_name, Document_Name=doc_Name, Doc_issue_date=doc_Issue_date,
                                  Doc_expiry_date=doc_Expire_date,
                                  Ddocfile=acc_cert_file, Status=1)
            data7.save()

        Prod = Product.objects.all()
        if User_Registration_Check_Status.objects.filter(User=data).exists():
              data1 = User_Registration_Check_Status.objects.get(User=data)
              data1.page_8 = 1
              data1.save()
        else:
            user = User_Registration_Check_Status(User=data,page_8=1)
            user.save()
        return render(request, 'nabl/nabl_reg9.html', {'product': Prod})
    return render(request, 'nabl/nabl_reg8.html')



def add_material(request):
    if request.method == "POST":
        data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        user_id = data.User_Id
        prdt = request.POST.get('product1')
        matrial_name = Vendor_Material_Master.objects.get(Material_Id=prdt)
        specification = request.POST.get('specification')
        spec = Vendor_Material_Specification_Master.objects.get(Material_Specification_Id=specification)
        list_is = request.POST.get('IsDatas')
        is_name = Nabl_Is_Master.objects.get(Is_Id=list_is)
        created_date = datetime.datetime.now()
        testing = request.POST.getlist('ips')
        if NABL_Registration_Test.objects.filter(user_id=user_id,Material_Name=matrial_name.Material_Name,Material_Specification_Name=spec.Material_Specification_Name).exists():
            messages.warning(request, "Material with this specification already selected")  
            return render(request, 'nabl/matrial.html')    

        else:
        
            for a in testing:
                test_name = Nabl_Acceptance_Test_Master.objects.get(Acceptance_Test_Id = a)

                test_data = NABL_Perform_Test(Material=matrial_name.Material_Name,Test_Name=test_name.Name_Of_Acceptance_Test,user_id=user_id)
                test_data.save()
            data1 = NABL_Registration_Test(user_id=user_id,Material_Name=matrial_name.Material_Name,Material_Item_Code = spec.Material_Item_Code,
                                        Material_Specification_Name=spec.Material_Specification_Name, Material_IS=is_name.IS_Name,
                                        Created_date=created_date, Created_by=user_id, Status=1)

            test_data = NABL_Perform_Test(Material=matrial_name.Material_Name,Test_Name=testing,user_id=user_id)
            data1.save()
        
    

        
        return redirect('nabl_reg9')
    return render(request, 'nabl/matrial.html')


def nabl_reg9(request):
   
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    doc = NABL_Registration_Test.objects.filter(user_id=data.User_Id)
       
    return render(request, 'nabl/nabl_reg9.html',{'data':doc})

def nabl_reg10(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    doc = NABL_Document.objects.filter(user_id=data.User_Id)
    return render(request, 'nabl/nabl_reg10.html',{'data':doc})
   
def nabl_reg11(request):
    aa = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    aa.update(complete_data=1,Complete_Details=1)
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
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
    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()

    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(mobile) + "&v1="+ str(name_sms) + "&v2=" + str()
    # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
    
    
    
    sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = mobile)
    sms_template.save()
    # abc = request.POST.get('rca_ven')
    # if abc == 'checked':
    #     aa.update(rca_vendor=1)
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    if User_Registration_Check_Status.objects.filter(User=data).exists():
        data1 = User_Registration_Check_Status.objects.get(User=data)
        data1.page_11 = 1
        data1.save()
    else:
        user = User_Registration_Check_Status(User=data,page_11=1)
        user.save()
    request.session['otp'] = otp
    return redirect("/nabl/vendor_otp_verify")





from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from datetime import time
from datetime import datetime
import datetime
def vendor_otp_verify(request):
    if request.session.has_key('otp'):
        if request.method == "POST":
            otp = request.POST.get('otp')
            if otp == request.session['otp']:
                
                data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
                data11 = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
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
                # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007005572119738232&mobile_number=" + str(mobile) + "&v1="+ str(name_sms) + "&v2=" + "MP" + str(zone)
                # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1007005572119738232',date = datetime.datetime.now(),mobile_number = mobile)
                sms_template.save()
                
                return redirect('/nabl/basic')
            else:
              
                return render(request, 'nabl/vendor_verify_otp.html')
            
    return render(request, 'nabl/vendor_verify_otp.html')


def nabl_reg12(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    if User_Registration_Check_Status.objects.filter(User=data).exists():
        data1 = User_Registration_Check_Status.objects.get(User=data)
        data1.page_12 = 1
        data1.save()
    else:
        user = User_Registration_Check_Status(User=data,page_12=1)
        user.save()
    def generateOTP():
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]

        return OTP

    otp = generateOTP()
    # all_otp.append(otp)
    # get_data = User_Registration.objects.get(ContactNo=mobile_no)
    # get_data.Otp = otp

    # get_data.save()
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    sms_number = data.ContactNo
    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080"}
    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(
        sms_number) + "&v1=" + str(otp) + "&v2=" + str()
    response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
    
    sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = sms_number)
    sms_template.save()
                
    request.session['otp'] = otp

    messages.warning(request, otp)
    return render(request, 'nabl/nabl_reg12.html')


def nabl_reg13(request):
    sms = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    mobile = sms.ContactNo
    name_sms = sms.CompanyName_E
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    data11 = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    reg_date = datetime.datetime.now().date()
    data11.update(complete_data=1,Complete_Details=1,reg_date=reg_date)
    user_id = data.User_Id
    mobile = data.ContactNo
    name_sms = data.CompanyName_E
    
    send_mail(
        'Your final registration is completed ',
        'Hello thanks for Final registration as a Vendor',
        settings.EMAIL_HOST_USER,
        [data.Email_Id],
        fail_silently=False,
    )
    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(mobile) + "&v1="+ str(name_sms) + "&v2=" + str()
    # response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
  
    sms_template = message_template_log(template_id = '1007277348148394809',date = datetime.datetime.now(),mobile_number = mobile)
    sms_template.save()
   
    return render(request, 'nabl/nabl_reg13.html')


def nabl_reg14(request):
    return render(request, 'nabl/nabl_reg14.html')


def nabl_reg15(request):
    return render(request, 'nabl/nabl_reg15.html')


def nabl_reg16(request):
    return render(request, 'nabl/nabl_reg16.html')


import json


def specification(request, id):
    stu = Product_Specification.objects.filter(Product_id=id)
    ser = Specification_Serializer(stu, many=True)
    main = ser.data
    json_data = json.dumps(main)
    return HttpResponse(json_data, content_type='application/json')


def userlist(request):
    stu = User_Registration.objects.filter(work_approval=1) | User_Registration.objects.filter(finance_approval=1)
    ser = User_RegistrationSerializer(stu, many=True)
    main = ser.data
    json_data = json.dumps(main)
    return HttpResponse(json_data, content_type='application/json')


def test(request, id):
    stu = Product_List_Of_Test.objects.filter(Product_id=id)
    Data = []
    for data in stu:
        Test = {}
        test = List_Of_Test.objects.get(id=data.Test_id)
        Test['id'] = test.id
        Test['name'] = test.Test_Name
        Data.append(Test)
    json_data = json.dumps(Data)
    return HttpResponse(json_data, content_type='application/json')


def product(request):
    Prod = Product.objects.all()
    return render(request, 'product.html', {'product': Prod})


def Test2(request):
    return render(request, 'nabl/nabl_reg8.html')

def Nabl_Profile(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    userid = data.User_Id
    abcde = UserCompanyDataMain.objects.get(user_id_id=data)

    if data.profile_update_fee == 1 or data.cgm_approval == 0:
        if request.method == "POST":
            data11 = User_Registration.objects.filter(
                ContactNo=request.session['uid'],User_type = request.session['User_type'])
            abc = UserCompanyDataMain.objects.get(user_id_id=data)
            data1 = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
            #data1.Type_of_business = request.POST['two']
            #data1.CompanyName_E = request.POST['four']
            #data1.Authorised_person_E = request.POST['five']
            #data1.ContactNo = request.POST['six']
            data1.Email_Id = request.POST['seven']
            data1.User_zone = request.POST['zero']
            data1.save()
            abc.Company_Pan_No = request.POST['eight']
            abc.Company_Gumastha_No = request.POST['nine']
            abc.Company_Gst_No = request.POST['ten']
            # abc.Registration_Date  = request.POST['eleven']
            abc.Company_Fax = request.POST['twelve']
            # **********
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
            return redirect('/nabl/basic')
    else:
        return HttpResponse("You have to pay profile update fee")
    return render(request,'nabl/UpdateNablProfile.html',{"basic": data, 'company': abcde})





from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def AddProduct(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        res = {'msg': 'Data Received'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data, content_type='application/json')
    else:
        res = {'msg': 'Please Send Post Request'}
        return HttpResponse('Please Send Post Request', content_type='application/json')
        
        
def profile_status(request):
    TKC = User_Registration.objects.filter(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    data = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
    if data.Authentication_id:
        aaa = User_Registration.objects.get(ContactNo=request.session['uid'],User_type = request.session['User_type'])
        return render(request, 'nabl/base1.html', {"data11": TKC,'to_daaa':aaa})
    return render(request, 'nabl/base1.html', {"data11": TKC})        


def nabl_trf(request):
    data = User_Registration.objects.get(ContactNo = request.session['uid'])
    amn_obj = Add_material_nabl.objects.filter(User = data, trf_generated=1, gatepass_generated=1, SendMatToNabl=1).order_by('-id')
    lst_failure_per = []
    lst_status = []    
    for i in amn_obj:
        tot = 0
        mat_fail_count = 0
        rejection_criterion = 0
        sc_obj = sample_code_table.objects.filter(Gatepass = i)
        try:
            ro_mat_info_obj = RO_Material_Info.objects.filter(ro = sc_obj[0].ro_id)
            for mt in ro_mat_info_obj:
                qt = mt.quantity
                tot = tot + qt
            mat_fail_count = sample_code_table.objects.filter(ro_id = sc_obj[0].ro_id,result_pass=0, Gatepass = i).count()
            import math
            rejection_criterion = (mat_fail_count / tot) * 100
            lst_failure_per.append(rejection_criterion)
            sample_count = sample_code_table.objects.filter(ro_id = sc_obj[0].ro_id, Gatepass = i).count()
            sample_tested_count = sample_code_table.objects.filter(Q(ro_id = sc_obj[0].ro_id, Gatepass = i) & (Q(result_pass=1)|Q(result_pass=0))).count()
            if rejection_criterion > 5:
                lst_status.append("Lot Rejected")
            elif rejection_criterion <= 5:
                if sample_count == sample_tested_count:
                    lst_status.append("Lot Accepted")
                else:
                    lst_status.append("Pending")
        except Exception as e:
            lst_status.append("Pending")
    final_data = zip(amn_obj, lst_failure_per, lst_status)
    return render(request, 'nabl/nabl_trf.html', { 'amn_obj': amn_obj, 'final_data':final_data})

def nabl_trf_view(request, user_id):
    data = TRF_Details.objects.filter(user_id=user_id)
    data2 = TRF_Test_Details.objects.filter(user_id=user_id)
    return render(request, 'nabl/nabl_trf_view.html', {'data': data[0], 'data2': data2})

def nabl_sample_recv(request, gatepass_id):
    if request.method == 'POST':
        mat_id = request.POST.get('mat_id')
        remark = request.POST.get('remark')
        result = request.POST.get('result')
        rating = request.POST.get('rating')
        
        if request.FILES['myFile']:
            myFile = request.FILES['myFile']

        sc_obj = sample_code_table.objects.get(material_serial_number=mat_id)
        sc_obj.result_pass = result
        sc_obj.save()
        
        amn_obj = Add_material_nabl.objects.get(id=gatepass_id)
        TRF_Details.objects.get(Gatepass=amn_obj)

    amn_obj = Add_material_nabl.objects.get(id=gatepass_id)
    sc_obj = sample_code_table.objects.filter(Gatepass = amn_obj)

    for i in sc_obj:
        try:
            sc_number = sample_code_table.objects.get(id = i.id)
            sc_num = int(sc_number.id)
            length = int(math.log10(sc_num))
            if length == 1:
                sc = "000" + str(sc_num)
            elif length == 2:
                sc = "00" + str(sc_num)
            elif length == 3:
                sc = "0" + str(sc_num)
            else:
                sc = str(sc_num)
                pass
        except Exception as e:
            sc = "0001"
        import time
        current_date = time.strftime("%d%m%y")
        s_mat = 'DT' + str(current_date) + sc
        i.sample_code=s_mat
        i.user_id=amn_obj.User.User_Id
        TRF_obj = TRF_Details.objects.get(Gatepass = amn_obj)
        i.TRF_Id=TRF_obj.TRF_Id
        i.ro_id=amn_obj.roid
        i.gatepass_id=amn_obj.id
        i.company_name=TRF_obj.customer_Organization_name
        i.material_serial_number = i.XMRList
        i.save()

    amn_obj = Add_material_nabl.objects.get(id=gatepass_id)
    sample_obj = sample_code_table.objects.filter(Gatepass = amn_obj, result_pass=None)
    TRF_obj = TRF_Details.objects.get(Gatepass = amn_obj)
    if sample_obj:
        for i in sample_obj:
            if i.phy_rejected == 1:
                amn_obj.SomeSamplePhyRejected = 1
                amn_obj.save()
    else:
        amn_obj.AllSampleReportSubmited = 1
        amn_obj.save()
    return render(request, 'nabl/nabl_sample_recv.html',{'add_material_nabl': amn_obj, 'sc_obj':sample_obj,
                                                         'user_id':amn_obj.User.User_Id, 'TRF_Id':amn_obj.TRF_Id,
                                                         'TRF_obj':TRF_obj})

def nabl_sample_recv2(request, material_serial_number, ro_id, gp_id):
    if request.method == 'POST':
        remark = request.POST.get('remark')
        result = request.POST.get('result')
        myFile = request.FILES['myFile']
        rating = request.POST.get('rating')
    
        sc_obj = sample_code_table.objects.get(material_serial_number=material_serial_number, ro_id=ro_id, Gatepass=gp_id)
        sc_obj.FinalRemark = remark
        sc_obj.result_pass = result
        sc_obj.sampleCode_report = myFile
        sc_obj.material_rating = rating
        sc_obj.report_date = datetime.datetime.now()
        sc_obj.save()
        
        # ****** for single machine reject ******
        ro_mat_xmr_obj = RO_Material_XMR_Info.objects.filter(xmr=material_serial_number, ro=ro_id) # 25-123456-7
        ro_mat_xmr_obj.update(single_reject_nabl_submit = 1)
        for j in ro_mat_xmr_obj:
            if sc_obj.result_pass == "1":
                j.single_reject_by_nabl = 1
                j.save()
            elif sc_obj.result_pass == "0":
                j.single_reject_by_nabl = -1
                j.save()
                ro=j.ro.id
                rel=RO_Info.objects.get(id=ro)
                rel.ro_nabl_mac_rej=1
                rel.random_flag=0
                rel.save()
            else:
                pass
        
        # ****** for lot machine reject ******
        sc_lot_rej_obj = sample_code_table.objects.get(material_serial_number=material_serial_number, ro_id=ro_id, Gatepass=gp_id)
        ro_id = sc_lot_rej_obj.ro_id
        material_rating = sc_lot_rej_obj.CapacityList
        
        ro_info_obj = RO_Info.objects.get(id=ro_id)
        ro_mat_info_obj = RO_Material_Info.objects.filter(ro = ro_info_obj)
        tot=0
        for mt in ro_mat_info_obj:
            qt=mt.quantity
            tot=tot+qt
        
        mat_fail_count= sample_code_table.objects.filter(ro_id=ro_id, result_pass=0, Gatepass=gp_id).count()
        import math
        rejection_criterion = (mat_fail_count / tot) * 100
        if rejection_criterion > 5:
            rel=RO_Info.objects.get(id=ro_info_obj.id)
            rel.ro_nabl_comp_rej=-1
            rel.random_flag = 0
            rel.complete_sampled_by_cgm = 0
            rel.ro_nabl_lot_reject = 1
            rel.save()
            ro_mat_xmr_obj = RO_Material_XMR_Info.objects.filter(ro = ro_info_obj, uneco_status=0)
            for i in ro_mat_xmr_obj:
                i.machine_reject_by_nabl = -1
                i.nachine_reject_nabl_submit = 1
                i.xmr_initial_sampled_flag = 0
                i.ro.random_flag = 0
                i.ro.complete_sampled_by_cgm = 0
                i.ro.ro_nabl_lot_reject = 1
                i.save()
                
        elif rejection_criterion <= 5:
            sc_accept_all_obj = sample_code_table.objects.get(material_serial_number=material_serial_number, ro_id=ro_id, Gatepass=gp_id)
            sampleCountRoWise = sample_code_table.objects.filter(ro_id=sc_accept_all_obj.ro_id, Gatepass=gp_id).count()
            sampleReportUploadedRoWise = sample_code_table.objects.filter((Q(ro_id=sc_accept_all_obj.ro_id, Gatepass=gp_id))
                                                                & (Q(result_pass=1) | Q(result_pass=0) 
                                                                | Q(phy_rejected=1))).count()
            if int(sampleCountRoWise) == int(sampleReportUploadedRoWise):
                rel=RO_Info.objects.get(id=ro_info_obj.id)
                rel.ro_nabl_comp_rej=1
                rel.save()
 
                ro_mat_xmr_obj = RO_Material_XMR_Info.objects.filter(ro=ro_info_obj, uneco_status=0)    
                for i in ro_mat_xmr_obj:
                    i.machine_reject_by_nabl = 1
                    i.nachine_reject_nabl_submit = 1
                    i.save()
            else:
                pass
        else:
            pass
    return redirect("nabl_trf")
    
            
def nabl_sample_reject(request, xmr_number, ro_id, gp_id):
    if request.method == 'POST':
        rejected_by = request.POST.get('rejected_by')
        remark = request.POST.get('remark')
        date = request.POST.get('date')
        phy_accept_reject = request.POST.get('phy_accept_reject')

        if phy_accept_reject == '0' : # 0 == Fail ********* physical reject *********
            data = sample_code_table.objects.filter(material_serial_number=xmr_number, ro_id=ro_id, Gatepass=gp_id)
            data.update(rejected_sample_code=data[0].sample_code),
            data.update(rejection_yes_no="Yes"),
            data.update(phy_rejected=1),
            data.update(officer_id=rejected_by)
            data.update(rejection_remark=remark)
            data.update(rejected_date=date)
            data.update(phy_accepted=0)
            sample_obj = sample_code_table.objects.get(material_serial_number=xmr_number, ro_id=ro_id, Gatepass=gp_id)
            ro=RO_Info.objects.get(id=sample_obj.ro_id)
            ro.random_flag=0
            ro.nabl_manual_rej_flag = 1
            ro.save()
            material=RO_Material_Info.objects.filter(ro=ro,rating=sample_obj.CapacityList)
            for i in material:
                if i.rating=="25KVA":
                    i.mat_rejection_flag=1
                    i.finally_sampled=0
                    i.save()
                elif i.rating=="63KVA":
                    i.mat_rejection_flag=1
                    i.finally_sampled=0
                    i.save()
                elif i.rating=="100KVA":
                    i.mat_rejection_flag=1
                    i.finally_sampled=0
                    i.save()
                elif i.rating=="200KVA":
                    i.mat_rejection_flag=1
                    i.finally_sampled=0
                    i.save()                
            
            xmr_obj=RO_Material_XMR_Info.objects.filter(ro=ro)
            for i in xmr_obj:
                if str(i.xmr) == str(xmr_number):
                    i.ph_reject_by_nabl=-1
                    i.ph_reject_by_submit=1
                    i.save()
                    rel=RO_Info.objects.get(id=ro.id)
                    rel.ro_nabl_sin_rej=1
                    rel.save()
                else:
                    pass
            
        elif phy_accept_reject == '1': # 1 == Pass ********* physical accept *********
            data = sample_code_table.objects.filter(material_serial_number=xmr_number, ro_id=ro_id, Gatepass=gp_id)
            data.update(rejected_sample_code=data[0].sample_code),
            data.update(rejection_yes_no="No"),
            data.update(phy_rejected=0),
            data.update(officer_id=rejected_by)
            data.update(rejection_remark=remark)
            data.update(rejected_date=date)
            data.update(phy_accepted=1)

            sample_obj = sample_code_table.objects.get(material_serial_number=xmr_number, ro_id=ro_id, Gatepass=gp_id)
            ro=RO_Info.objects.get(id=sample_obj.ro_id)
            xmr_obj=RO_Material_XMR_Info.objects.filter(ro=ro)
            for i in xmr_obj:
                if str(i.xmr) == str(xmr_number):
                    i.ph_reject_by_nabl=1
                    i.ph_reject_by_submit=1
                    i.save()
                else:
                    pass
        else:
            pass

        sc_obj = sample_code_table.objects.get(material_serial_number=xmr_number, ro_id=ro_id, Gatepass=gp_id)
        amn_obj = Add_material_nabl.objects.get(id=sc_obj.Gatepass)
        sample_obj = sample_code_table.objects.filter(Gatepass = amn_obj, result_pass=None)
        TRF_obj = TRF_Details.objects.get(Gatepass = amn_obj)
        return render(request, 'nabl/nabl_sample_recv.html',{'add_material_nabl': amn_obj, 'sc_obj':sample_obj,
                                                         'user_id':amn_obj.User.User_Id, 'TRF_Id':amn_obj.TRF_Id,
                                                         'TRF_obj':TRF_obj})
    sample_obj = sample_code_table.objects.get(material_serial_number=xmr_number, ro_id=ro_id, Gatepass=gp_id)
    return render(request, 'nabl/nabl_sample_reject.html',{'sc_obj': sample_obj})


def nabl_out_physical(request):
    usr_obj = User_Registration.objects.get(ContactNo = request.session['uid'])
    sample_obj = sample_code_table.objects.filter((Q(user_id=usr_obj.User_Id) & Q(outward_generated=0)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1))).order_by('-Gatepass')
    if request.method == "POST":
        material_list = request.POST.getlist('material_list')
        XMRList = []
        CapacityList = []
        TypeList = []
        sampleCode_list = []
        RemarkList = []
        ROList = []
        GPList = []
        ro_id = ""
        gp_id = ""
        for i in material_list:
            ss = i.split("/")
            xmr_no = ss[0]
            ro_id = ss[1]
            gp_id = ss[2]
            amn_obj = sample_code_table.objects.get(XMRList=xmr_no, ro_id=ro_id, Gatepass=gp_id)
            XMRList.append(amn_obj.XMRList)
            CapacityList.append(amn_obj.CapacityList)
            TypeList.append(amn_obj.TypeList)
            sampleCode_list.append(amn_obj.sample_code)
            RemarkList.append(amn_obj.RemarkList)
            ROList.append(ro_id)
            GPList.append(gp_id)
        final_zip = zip(XMRList, CapacityList, TypeList, RemarkList, ROList, GPList)
        usr_obj_nabl = User_Registration.objects.filter(User_type="NABL")
        return render(request, 'nabl/GatepassOutwardNabl.html',{'final_zip':final_zip, 'usr_obj_nabl':usr_obj_nabl, 'ro_id':ro_id, 'gp_id':gp_id})
    return render(request, 'nabl/nabl_out.html',{'sc_obj':sample_obj})


def nabl_out_physical_view(request):
    usr_obj = User_Registration.objects.get(ContactNo = request.session['uid'])
    sample_obj = sample_code_table.objects.filter((Q(user_id=usr_obj.User_Id) & Q(outward_generated=1)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1))).order_by('-GatepassOutward')
    return render(request, 'nabl/nabl_out_physical_view.html',{'sc_obj':sample_obj})


def nabl_out_physical_view_gatepass(request, GatepassOutward_id):
    amno_obj = Add_material_nabl_outward.objects.get(id = GatepassOutward_id)    
    sct_obj = sample_code_table.objects.filter(GatepassOutward = amno_obj)
    lst_XMRList = []
    lst_CapacityList = []
    lst_TypeList = []
    lst_RemarkList = []
    for i in sct_obj:
        lst_XMRList.append(i.XMRList)
        lst_CapacityList.append(i.CapacityList)
        lst_TypeList.append(i.TypeList)
        lst_RemarkList.append(i.RemarkList)
    final_data = zip(lst_XMRList, lst_CapacityList, lst_TypeList, lst_RemarkList)
    return render(request, 'nabl/GatepassOutwardNabl2.html', {'material_obj':amno_obj, 'sct_obj':final_data})


def Gatepass_save_nabl(request):
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

        User_Contact_No=request.session['uid']
        usr_obj2 = User_Registration.objects.get(ContactNo = User_Contact_No)

        mat_out_obj = Add_material_nabl_outward(DispatcherNameOfEntity = DispatcherNameOfEntity, LoaOrderNo=LoaOrderNo,
                                        NameOfItem=NameOfItem, LoaOrderDate=LoaOrderDate, DescriptionOfItem=DescriptionOfItem, 
                                        ManufacturerName=ManufacturerName, VehicleNumber=VehicleNumber, 
                                        DINoDate=DINoDate, DriverName=DriverName, DriverContactNo=DriverContactNo,
                                        IssueDate=IssueDate, IssuedTo=IssuedTo, VerifiedBy=VerifiedBy, Gatekeeper=Gatekeeper, 
                                        IssuingAuthority=IssuingAuthority, VerifiedByDesignation=VerifiedByDesignation, 
                                        GatekeeperDesignation=GatekeeperDesignation, 
                                        IssuingAuthorityDesignation=IssuingAuthorityDesignation, ReceiverNameOfEntity=ReceiverNameOfEntity,
                                        ReceiverContactPerson=ReceiverContactPerson, ReceiverDetails=ReceiverDetails, 
                                        ReceiverContact=ReceiverContact, UserOutward=usr_obj2, Zone=usr_obj2.User_zone, 
                                        )
        mat_out_obj.save()

        XMRList = request.POST.getlist("XMRList")
        CapacityList = request.POST.getlist("CapacityList")
        TypeList = request.POST.getlist("TypeList")
        RemarkList = request.POST.getlist("RemarkList")
        ROList = request.POST.getlist("ROList")
        GPList = request.POST.getlist("GPList")

        for i in range(len(XMRList)):
            sct_obj = sample_code_table.objects.get(XMRList = XMRList[i], ro_id=ROList[i], Gatepass=GPList[i])
            sct_obj.GatepassOutward = mat_out_obj
            sct_obj.outward_generated = 1
            sct_obj.save()
        final_zip = zip(XMRList, CapacityList, TypeList, RemarkList)
    return render(request, 'nabl/GatepassOutwardNabl2.html', {'usr_obj2':usr_obj2, 'material_obj':mat_out_obj,
                                                                    'sct_obj':final_zip})

def uplaod_Outwardgatepass(request, gatepass_id):
    amn_obj = Add_material_nabl.objects.all()
    if request.method == "POST":
        if request.FILES['digitalCert']:
            filename = request.FILES['digitalCert']  
            amn_obj2 = Add_material_nabl_outward.objects.get(id=gatepass_id)
            amn_obj2.gatepassAreaStoreOutward_file = filename
            amn_obj2.gatepassOutward_generated = 1
            amn_obj2.save()
        usr_obj = User_Registration.objects.get(ContactNo = request.session['uid'])
        sample_obj = sample_code_table.objects.filter((Q(user_id=usr_obj.User_Id) & Q(outward_generated=0)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1))).order_by('-Gatepass')
        return render(request, 'nabl/nabl_out.html',{'sc_obj':sample_obj})
    return HttpResponse("Go Back on previous page")

def nabl_out_physical2(request):
    if request.method == "POST":
        sampleCode_list = request.POST.getlist('sampleCode_list')
        print("sampleCode_list: ", sampleCode_list)
        material_serial_number_list = request.POST.getlist('material_serial_number_list')
        print("material_serial_number_list: ", material_serial_number_list)
        TRF_Id = request.POST.get('TRF_Id')
        print("TRF_Id: ", TRF_Id)
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
        
        User_Contact_No = request.session['uid']
        data = TRF_Details.objects.get(mobile_no = User_Contact_No)
        
        material_obj = Add_material_nabl(user_id=data.user_id, ro_id=data.ro_id, driver_name=driver_name, 
                                            driver_mobile=driver_mobile,
                                            receiver_name=receiver_name, vehicle_number=vehicle_number,
                                            trnsfrmr_type=trnsfrmr_type, Material_name=Material_name,
                                            manufacturer_name=manufacturer_name, 
                                            rating=rating,order_number=order_number,order_date=order_date,
                                            di_number=di_number,di_date=di_date,xmr_snos=xmr_snos,
                                            send_to_lab=send_to_lab, letter_no=letter_no,date_within=date_within,
                                            out_date=out_date, issue_auth=issue_auth, inspectioner_sign=inspectioner_sign,
                                            receiver_sign=receiver_sign, gatekeeper_sign=gatekeeper_sign
                                            )
        material_obj.save()
        
        for sc in sampleCode_list:
            sct_obj = sample_code_table.objects.filter(sample_code = sc)
            sct_obj.update(outward_driver_name = driver_name)
            sct_obj.update(outward_driver_mobile = driver_mobile)
            sct_obj.update(outward_vehicle_number = vehicle_number)
            sct_obj.update(outward_date = out_date)
            sct_obj.update(outward_pass = 1)

        sample_code_mat_list = zip(sampleCode_list,material_serial_number_list )
        return render(request, 'nabl/nabl_outward.html',{'sample_code_mat_list':sample_code_mat_list, 
                                                        'material_serial_number_list':material_serial_number_list, 
                                                        'driver_name':driver_name, 
                                                        'Vehicle_number':vehicle_number, 'out_date':out_date, 
                                                        'outward_driver_mobile':driver_mobile
                                                        })

    User_Contact_No=request.session['uid']
    
    amn_obj = Add_material_nabl.objects.get(login_number=User_Contact_No)
    sample_obj = sample_code_table.objects.filter(Q(Gatepass=amn_obj) & Q(result_pass=1) | Q(phy_rejected=1))
    print("sample_objsample_objsample_objsample_objsample_objsample_obj:::::", sample_obj)
    return render(request, 'nabl/nabl_out_physical.html',{'sc_obj':sample_obj,'mobile':User_Contact_No})


# def fqp_material_report(request):
#     data = User_Registration.objects.get(ContactNo=request.session['uid'])
#     om_obj = Offer_Material.objects.filter(nabl_number = data.ContactNo, nabl_gatepass = 1, send_to_nabl = 1)
#     list_data=[]
#     for dat in om_obj:
#         dat = fqp_wo_nabl_gatepass.objects.filter(area_store=dat)
#         list_data.append(dat)
#     return render(request, 'nabl/fqp_material_report.html', {'om_obj': om_obj,'list_data':list_data})
def fqp_material_report(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'])
    om_obj = offer_material_site_stores.objects.filter(nabl_number = data.ContactNo, trf_status = 1)
    list_data=[]
    sample_serial_number = []
    for dat in om_obj:
        data = tkc_wo_nabl_gatepass.objects.filter(offer_number = dat.id)
        sampled_qty = offer_material_serial_number.objects.filter(offer = dat.id, is_sampled = 1).count()
        list_data.append(dat)
        sample_serial_number.append(sampled_qty)
    final_zip = zip(list_data, sample_serial_number)
    return render(request, 'nabl/fqp_material_report.html', {'om_obj': om_obj,'list_data':list_data, 'final_zip':final_zip})



# def Offer_Item_Code(request, id):
#     data = Offer_Material_Item_Code.objects.filter(Offer_Material=id, is_sampled=1)
#     data2 = fqp_wo_nabl_gatepass.objects.filter(area_store = id)
#     data3 = Fqp_Work_Order_Trf_Details.objects.filter(area_store_id = id)
#     final_gp_trf = zip(data2, data3)
#     return render(request, 'nabl/fqp_material_report2.html',{'id':id,'data': data, 'final_gp_trf':final_gp_trf})
def Offer_Item_Code(request, id):
    data = offer_material_serial_number.objects.filter(offer = id, is_sampled = 1)
    data2 = tkc_wo_nabl_gatepass.objects.filter(offer_number = id)
    data3 = Tkc_Work_Order_Trf_Details.objects.filter(offer_number = id)
    final_gp_trf = zip(data2, data3)
    return render(request, 'nabl/fqp_material_report2.html',{'id':id,'data': data, 'final_gp_trf':final_gp_trf})



def fqp_nabl_sample_reject(request, id, item_number):
    if request.method == 'POST':
        rejected_by = request.POST.get('rejected_by')
        remark = request.POST.get('remark')
        date = request.POST.get('date')
        phy_accept_reject = request.POST.get('phy_accept_reject')
        data = Offer_Material_Item_Code.objects.get(Offer_Material=id, Item_Serial_No=item_number)
        data.remark = remark
        data.phy_test_date = date
        data.officer_name = rejected_by
        if phy_accept_reject == 0:
            data.nabl_result = -1
        elif phy_accept_reject == 1:
            data.nabl_result = 1
        data.save()

        data2 = Offer_Material.objects.get(id=id)
        data2.send_to_cgm = 1
        data2.nabl_gatepass = 0
        data2.send_to_nabl = 0
        data2.save()

        return HttpResponse("Doneeeeeeeeeee")
    data = Offer_Material_Item_Code.objects.get(Offer_Material=id, Item_Serial_No=item_number)
    return render(request, 'nabl/fqp_nabl_sample_reject.html',{'id':id, 'data': data})
###################################******************PO Sampling Anil**************************######################################

def cp_nabl_trf(request):
    data = User_Registration.objects.get(ContactNo=request.session['uid'])
    
    po_obj = po_nabl_gatepass.objects.filter(Q(Q(area_store__send_to_nabl= 1) | Q(area_store__send_to_nabl= 2)) & (Q(area_store__sampling_flag = 1) | Q(area_store__sampling_flag = 2))).order_by("-id")
    
    return render(request, 'nabl/cp_nabl_trf.html', { 'po_obj': po_obj})


def cp_nabl_trf_view(request, id):
    data = User_Registration.objects.get(ContactNo=request.session['uid'])
    gp_obj = po_nabl_gatepass.objects.get(id=id)
    po_trf_obj = PO_TRF_Details.objects.filter(gatepass_doc=gp_obj).earliest('TRF_Id')
    dias_obj = DI_Areastores.objects.get(id = gp_obj.area_store.id)
    m_sample_code = dias_obj.material_sample_code
    di_master_obj = DI_Master.objects.get(id = dias_obj.di_master.id)
    
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)

    
    di_area_master_ids = [obj.id for obj in di_area_master]
            
    
    dimos_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id__in=di_area_master_ids,as_accepted=1)
    
    outward_qty = dimos_obj.count()
    
    print("outward_qty=================outward_qty========outward_qty",outward_qty)
    
    for i in dimos_obj:
        if sample_code_table_cp.objects.filter(user_id = data, TRF_Id = po_trf_obj.TRF_Id, material_serial_number = i.serial_no, 
                                              Gatepass = gp_obj).exists():
            pass
        else:
            sctc_obj = sample_code_table_cp(user_id = data, TRF_Id = po_trf_obj.TRF_Id, material_serial_number = i.serial_no,
                                            material_name = i.offer.item_name, company_name = dias_obj.po.vendor.CompanyName_E,
                                            Gatepass = gp_obj, sample_code = m_sample_code, di_area_store=dias_obj)
            sctc_obj.save()
    sctcp_obj = sample_code_table_cp.objects.filter(user_id = data, TRF_Id = po_trf_obj.TRF_Id, Gatepass = gp_obj, result_pass = None)
    return render(request, 'nabl/cp_nabl_trf_view.html', {'sctcp_obj':sctcp_obj, 'gp_obj': gp_obj, 'po_trf_obj':po_trf_obj,'outward_qty':outward_qty})
 

def cp_nabl_trf_view2(request, gp_id, trf_id, mat_sr):
    if request.method == 'POST':
        remark = request.POST.get('remark')
        result = request.POST.get('result')
        myFile = request.FILES['myFile']
        rating = request.POST.get('rating')
        sc_obj = sample_code_table_cp.objects.get(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
        sc_obj.FinalRemark = remark
        sc_obj.result_pass = result
        sc_obj.sampleCode_report = myFile
        sc_obj.material_rating = rating
        sc_obj.report_date = datetime.datetime.now()
        sc_obj.save()
        return redirect("cp_nabl_trf")
    return HttpResponse("cp_nabl_trf_view2"+'/'+str(gp_id)+'/'+str(trf_id)+'/'+str(mat_sr))
    

def cp_nabl_sample_reject(request, gp_id, trf_id, mat_sr):
    if request.method == 'POST':
        rejected_by = request.POST.get('rejected_by')
        remark = request.POST.get('remark')
        date = request.POST.get('date')
        phy_accept_reject = request.POST.get('phy_accept_reject')
        if phy_accept_reject == '0' : # 0 == Fail ********* physical reject *********
            data = sample_code_table_cp.objects.filter(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
            data.update(rejected_sample_code=data[0].sample_code),
            data.update(rejection_yes_no="Yes"),
            data.update(phy_rejected=1),
            data.update(officer_id=rejected_by)
            data.update(rejection_remark=remark)
            data.update(rejected_date=date)
            data.update(phy_accepted=0)
        elif phy_accept_reject == '1': # 1 == Pass ********* physical accept *********
            data = sample_code_table_cp.objects.filter(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
            data.update(rejected_sample_code=data[0].sample_code),
            data.update(rejection_yes_no="No"),
            data.update(phy_rejected=0),
            data.update(officer_id=rejected_by)
            data.update(rejection_remark=remark)
            data.update(rejected_date=date)
            data.update(phy_accepted=1)
        else:
            pass
        sc_obj = sample_code_table_cp.objects.filter(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id).earliest('id')
        amn_obj = po_nabl_gatepass.objects.get(id=sc_obj.Gatepass.id)
        sample_obj = sample_code_table_cp.objects.filter(Gatepass = amn_obj, result_pass=None)
        TRF_obj = PO_TRF_Details.objects.filter(gatepass_doc = amn_obj).earliest('TRF_Id')
        return redirect('/nabl/cp_nabl_trf_view/'+ str(gp_id))
    sample_obj = sample_code_table_cp.objects.filter(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id).earliest('TRF_Id')
    return render(request, 'nabl/cp_nabl_sample_reject.html',{'sc_obj': sample_obj})


def cp_nabl_out_physical(request):
    usr_obj = User_Registration.objects.get(ContactNo = request.session['uid'])
    sample_obj = sample_code_table_cp.objects.filter((Q(user_id=usr_obj) & Q(outward_generated=0)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1))).order_by('-Gatepass')
    if request.method == "POST":
        material_list = request.POST.getlist('material_list')
        MatList = []
        CapacityTypeList = []
        RemarkList = []
        trf_id = ""
        gp_id = ""
        for i in material_list:
            ss = i.split("/")
            mat_sr = ss[0]
            trf_id = ss[1]
            gp_id = ss[2]
            amn_obj = sample_code_table_cp.objects.filter(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id).earliest('id')
            MatList.append(amn_obj.material_serial_number)
            CapacityTypeList.append(amn_obj.material_name)
            RemarkList.append(amn_obj.FinalRemark)
        final_zip = zip(MatList, CapacityTypeList, RemarkList)
        usr_obj_nabl = User_Registration.objects.filter(User_type="NABL")
        return render(request, 'nabl/cp_GatepassOutwardNabl.html',{'final_zip':final_zip, 'usr_obj_nabl':usr_obj_nabl, 'trf_id':trf_id, 'gp_id':gp_id})
    return render(request, 'nabl/cp_nabl_out.html',{'sc_obj':sample_obj})


def cp_Gatepass_save_nabl(request, trf_id, gp_id):
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

        User_Contact_No=request.session['uid']
        usr_obj2 = User_Registration.objects.get(ContactNo = User_Contact_No)

        flag = 0
        mat_out_obj = ""
        if po_nabl_gatepass_outward.objects.filter(trfid=trf_id, UserOutward=usr_obj2, Zone=usr_obj2.User_zone).exists():
            flag = 1
        else:
            mat_out_obj = po_nabl_gatepass_outward(DispatcherNameOfEntity = DispatcherNameOfEntity, LoaOrderNo=LoaOrderNo,
                                            NameOfItem=NameOfItem, LoaOrderDate=LoaOrderDate, DescriptionOfItem=DescriptionOfItem, 
                                            ManufacturerName=ManufacturerName, VehicleNumber=VehicleNumber, 
                                            DINoDate=DINoDate, DriverName=DriverName, DriverContactNo=DriverContactNo,
                                            IssueDate=IssueDate, IssuedTo=IssuedTo, VerifiedBy=VerifiedBy, Gatekeeper=Gatekeeper, 
                                            IssuingAuthority=IssuingAuthority, VerifiedByDesignation=VerifiedByDesignation, 
                                            GatekeeperDesignation=GatekeeperDesignation, 
                                            IssuingAuthorityDesignation=IssuingAuthorityDesignation, ReceiverNameOfEntity=ReceiverNameOfEntity,
                                            ReceiverContactPerson=ReceiverContactPerson, ReceiverDetails=ReceiverDetails, 
                                            ReceiverContact=ReceiverContact, UserOutward=usr_obj2, Zone=usr_obj2.User_zone, 
                                            trfid = trf_id, 
                                            )
            mat_out_obj.save()

        MatList = request.POST.getlist("MatList")
        CapacityTypeList = request.POST.getlist("CapacityTypeList")
        RemarkList = request.POST.getlist("RemarkList")
        if flag == 1:
            return HttpResponse("Outward is already generated")
        else:
            for i in MatList:
                sct_obj = sample_code_table_cp.objects.filter(material_serial_number = i, TRF_Id=trf_id, Gatepass=gp_id).earliest('id')
                sct_obj.GatepassOutward = mat_out_obj
                sct_obj.outward_generated = 1
                sct_obj.save()
            final_zip = zip(MatList, CapacityTypeList, RemarkList)
            return render(request, 'nabl/cp_GatepassOutwardNabl2.html', {'usr_obj2':usr_obj2, 'material_obj':mat_out_obj,
                                                                    'final_zip':final_zip})


def cp_uplaod_Outwardgatepass(request, gatepass_id):
    if request.method == "POST":
        if request.FILES['digitalCert']:
            filename = request.FILES['digitalCert']  
            amn_obj2 = po_nabl_gatepass_outward.objects.get(id=gatepass_id)
            amn_obj2.gatepassAreaStoreOutward_file = filename
            amn_obj2.gatepassOutward_generated = 1
            amn_obj2.save()
        usr_obj = User_Registration.objects.get(ContactNo = request.session['uid'])
        sample_obj = sample_code_table_cp.objects.filter((Q(user_id=usr_obj) & Q(outward_generated=0)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1))).order_by('-Gatepass')
        return render(request, 'nabl/cp_nabl_out.html',{'sc_obj':sample_obj})
    return HttpResponse("Go Back on previous page")


def cp_nabl_out_physical_view(request):
    usr_obj = User_Registration.objects.get(ContactNo = request.session['uid'])
    sample_obj = sample_code_table_cp.objects.filter((Q(user_id=usr_obj) & Q(outward_generated=1)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1))).order_by('-GatepassOutward')
    return render(request, 'nabl/cp_nabl_out_physical_view.html',{'sc_obj':sample_obj})


def cp_nabl_result_sampling(request,id):
    
    material = DI_Areastores.objects.get(id=id)
    
    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj)
 
    gatepass_obj = po_nabl_gatepass.objects.get(area_store = material)
    sample_obj = sample_code_table_cp.objects.filter((Q(Gatepass = gatepass_obj)) & (Q(outward_generated=1)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1)))
    sampled_qty = sample_obj.count()
    pass_result = []
    
    reject_result = []
    
    for i in sample_obj:
        pass_result.append(i.result_pass)
        reject_result.append(i.phy_rejected)
    
 
    count_pass = pass_result.count(1)
    
    count_reject = reject_result.count(1)
    
       
    item_code = material.material_sample_code
    
    ps_obj = product_sampling.objects.filter(Q(item_code = item_code) | Q(item_code_ez = item_code) | Q(item_code_wz = item_code))
    
    
    flag = -1
    
    reject_unit = 0
    
    rejection_percentage = 0
    
    sample_count = 0
    
    permision_unit = 0
      
    permision_percent = 0

    for i in ps_obj:
        sample_type = i.sampling.sample_type
        sample_count = i.sampling.sample_unit
        if sample_type == 0:
            reject_unit = i.sampling.rejection_unit
            permision_unit = i.sampling.acceptable_unit
            flag = 0
        elif sample_type == 1:
            rejection_percentage = i.sampling.sample_percentage
            permision_percent = i.sampling.permissible_percentage
            flag = 1
        else:
            print("not matched")
    
    
    rejection_percentage_find = math.ceil(int(sampled_qty * rejection_percentage) / 100)
    
    permision_percentage_find = math.ceil(int(sampled_qty * permision_percent) / 100)
    
    if sample_obj:
        if flag == 0:
            if reject_unit < count_reject:
                for i in di_area_master:
                    i.samp_rejected_flag = 1
                    i.save()
            
            elif permision_unit <= count_pass:
                
                if permision_unit <= count_pass:
                    for i in di_area_master:
                        i.samp_accepted_flag = 1
                        i.save()
                else:
                    for i in di_area_master:
                        i.resampling_flag = 1
                        i.save()

            else:
                print("Nothing workeded flag 0===========Nothing workeded flag 0============Nothing workeded flag 0=======Nothing workeded flag 0::::::::")
            
        elif flag == 1:               
            if rejection_percentage_find <= count_reject:
                for i in di_area_master:
                    i.samp_rejected_flag = 1
                    i.save()
            elif permision_percentage_find <= count_pass:
                if permision_percentage_find <= count_pass:
                    for i in di_area_master:
                        i.samp_accepted_flag = 1
                        i.save()
                else:
                    for i in di_area_master:
                        i.resampling_flag = 1
                        i.save()
            else:
                print("Nothing workeded flag 1===========Nothing workeded flag 1============Nothing workeded flag 1=======Nothing workeded flag 1::::::::")
    else:
        return HttpResponse ("NABL Testing Progress/Pending")
        
    return render(request, 'po/area_store/po_nabl_result.html',{'name':sample_obj})




def cp_nabl_trf_view_resampling(request, id):
    data = User_Registration.objects.get(ContactNo=request.session['uid'])
    gp_obj = po_nabl_gatepass.objects.get(id=id)
    po_trf_obj = PO_TRF_Details.objects.filter(gatepass_doc=gp_obj).latest('TRF_Id')
    

    dias_obj = DI_Areastores.objects.get(id = gp_obj.area_store.id)
    m_sample_code = dias_obj.material_sample_code
    dimos_obj = DI_Material_Offer_Serial_No.objects.filter(area_store_id=dias_obj, as_accepted=2)
    
    outward_qty = dimos_obj.count()
    
    
    for i in dimos_obj:
        if sample_code_table_cp.objects.filter(user_id = data, TRF_Id = po_trf_obj.TRF_Id, material_serial_number = i.serial_no, 
                                              Gatepass = gp_obj).exists():
            pass
        else:
            sctc_obj = sample_code_table_cp(user_id = data, TRF_Id = po_trf_obj.TRF_Id, material_serial_number = i.serial_no,
                                            material_name = i.offer.item_name, company_name = dias_obj.po.vendor.CompanyName_E,
                                            Gatepass = gp_obj, sample_code = m_sample_code)
            sctc_obj.save()
    sctcp_obj = sample_code_table_cp.objects.filter(user_id = data, TRF_Id = po_trf_obj.TRF_Id, Gatepass = gp_obj, result_pass = None)
    return render(request, 'nabl/cp_nabl_trf_view_resampling.html', {'sctcp_obj':sctcp_obj, 'gp_obj': gp_obj, 'po_trf_obj':po_trf_obj,'outward_qty':outward_qty})


def cp_nabl_trf_view2_resampling(request, gp_id, trf_id, mat_sr):
    if request.method == 'POST':
        remark = request.POST.get('remark')
        result = request.POST.get('result')
        myFile = request.FILES['myFile']
        rating = request.POST.get('rating')
        sc_obj = sample_code_table_cp.objects.get(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
        sc_obj.FinalRemark = remark
        sc_obj.result_pass = result
        sc_obj.sampleCode_report = myFile
        sc_obj.material_rating = rating
        sc_obj.report_date = datetime.datetime.now()
        sc_obj.save()
        return redirect("cp_nabl_trf")
    return HttpResponse("cp_nabl_trf_view2_resampling"+'/'+str(gp_id)+'/'+str(trf_id)+'/'+str(mat_sr))


def cp_nabl_sample_reject_resampling(request, gp_id, trf_id, mat_sr):
    if request.method == 'POST':
        rejected_by = request.POST.get('rejected_by')
        remark = request.POST.get('remark')
        date = request.POST.get('date')
        phy_accept_reject = request.POST.get('phy_accept_reject')
        if phy_accept_reject == '0' : # 0 == Fail ********* physical reject *********
            data = sample_code_table_cp.objects.filter(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
            data.update(rejected_sample_code=data[0].sample_code),
            data.update(rejection_yes_no="Yes"),
            data.update(phy_rejected=1),
            data.update(officer_id=rejected_by)
            data.update(rejection_remark=remark)
            data.update(rejected_date=date)
            data.update(phy_accepted=0)
        elif phy_accept_reject == '1': # 1 == Pass ********* physical accept *********
            data = sample_code_table_cp.objects.filter(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
            data.update(rejected_sample_code=data[0].sample_code),
            data.update(rejection_yes_no="No"),
            data.update(phy_rejected=0),
            data.update(officer_id=rejected_by)
            data.update(rejection_remark=remark)
            data.update(rejected_date=date)
            data.update(phy_accepted=1)
        else:
            pass
        sc_obj = sample_code_table_cp.objects.get(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
        amn_obj = po_nabl_gatepass.objects.get(id=sc_obj.Gatepass.id)
        sample_obj = sample_code_table_cp.objects.filter(Gatepass = amn_obj, result_pass=None)
        TRF_obj = PO_TRF_Details.objects.filter(gatepass_doc = amn_obj).latest('TRF_Id')
        return redirect('/nabl/cp_nabl_trf_view_resampling/'+ str(gp_id))
    sample_obj = sample_code_table_cp.objects.get(material_serial_number=mat_sr, TRF_Id=trf_id, Gatepass=gp_id)
    return render(request, 'nabl/cp_nabl_sample_reject_resampling.html',{'sc_obj': sample_obj})


def cp_nabl_result_resampling(request,id):
    material = DI_Areastores.objects.get(id=id)
        
    di_master_obj = DI_Master.objects.get(id = material.di_master.id)
    di_area_master = DI_Areastores.objects.filter(di_master= di_master_obj, sampling_flag=2,resampling_flag=1)    
    
    gatepass_obj = po_nabl_gatepass.objects.get(area_store = material)
    print("gatepass_obj==========gatepass_obj========gatepass_obj::::::::",gatepass_obj)
    sample_obj = sample_code_table_cp.objects.filter((Q(Gatepass = gatepass_obj)) & (Q(outward_generated=2)) & (Q(result_pass=1) | Q(result_pass=0) | Q(phy_rejected=1)))
    print("sample_obj==============sample_obj===========sample_obj:::::::::",sample_obj)
    
    sample_obj_fail = sample_code_table_cp.objects.filter(Gatepass = gatepass_obj, outward_generated=2).exclude(result_pass=1)
    
    sample_obj_fail_count = sample_obj_fail.count() 
    
    sampled_qty = sample_obj.count()
    
    
    sampled_qty = sample_obj.count()
    pass_result = []
    
    reject_result = []
    
    for i in sample_obj:
        pass_result.append(i.result_pass)
        reject_result.append(i.phy_rejected)
    
 
    count_pass = pass_result.count(1)
    
    count_reject = reject_result.count(1)
    
       
    item_code = material.material_sample_code
    
    ps_obj = product_sampling.objects.filter(Q(item_code = item_code) | Q(item_code_ez = item_code) | Q(item_code_wz = item_code))
    
    print("ps_obj==========ps_obj============ps_obj===========ps_obj",ps_obj)
    
    flag = -1
    
    reject_unit = 0
    
    rejection_percentage = 0
    
    sample_count = 0
    
    aceept_unit = 0
      
    accept_percent = 0

    for i in ps_obj:
        sample_type = i.sampling.sample_type
        sample_count = i.sampling.sample_unit
        if sample_type == 0:
            reject_unit = i.sampling.resampling_rejection_unit
            aceept_unit = i.sampling.resampling_acceptable_unit
            flag = 0
        elif sample_type == 1:
            rejection_percentage = i.sampling.resampling_rejection_percentage
            accept_percent = i.sampling.resampling_acceptable_percentage
            flag = 1
        else:
            print("not matched")
    
    
    rejection_percentage_find = math.ceil(int(sampled_qty * rejection_percentage) / 100)
    
    accept_percent_find = math.ceil(int(sampled_qty * accept_percent)/ 100)
    
    if sample_obj:
        print("sample_obj worked===========sample_obj worked============sample_obj worked=======sample_obj worked::::::::")
        # print("samp_rejected_flag=========samp_rejected_flag=========samp_rejected_flag",i.samp_rejected_flag)
        if flag == 0:
            print("flag 0 sample_obj=========flag 0 sample_obj===========flag 0 sample_obj===========flag 0 sample_obj=========flag 0 sample_obj")
            if reject_unit <= sample_obj_fail_count:
                for i in di_area_master:
                    # print("samp_rejected_flag=========samp_rejected_flag=========samp_rejected_flag",i.samp_rejected_flag)
                    i.samp_rejected_flag = 2
                    i.save()
                    print("samp_rejected_flag worked===========samp_rejected_flag worked============samp_rejected_flag worked=======samp_rejected_flag worked::::::::")
            
            elif aceept_unit >= sample_obj_fail_count:
                
                for i in di_area_master:
                    print("samp_accepted_flag=========samp_accepted_flag=========samp_accepted_flag",i.samp_accepted_flag)
                    
                    print("lot Accepted==========lot Accepted============lot Accepted")
                    i.samp_accepted_flag = 2
                    i.save()


            else:
                print("Nothing workeded===========Nothing workeded============Nothing workeded=======Nothing workeded::::::::")
            
        elif flag == 1: 
            print("flag 1 sample_obj=========flag 1 sample_obj===========flag 1 sample_obj===========flag 1 sample_obj=========flag 1 sample_obj")
              
            if rejection_percentage_find <= sample_obj_fail_count:
                for i in di_area_master:
                    i.samp_rejected_flag = 2
                    i.save()
                    print("lot Rejected flag 1==========lot Rejected flag 1============lot Rejected flag 1")
            elif accept_percent_find >= sample_obj_fail_count:

                for i in di_area_master:
                    i.samp_accepted_flag = 2
                    i.save()
                    print("LOT aceept flag 1==========LOT aceept flag 1============LOT aceept flag 1")

            else:
                print("Nothing workeded flag 1===========Nothing workeded flag 1============Nothing workeded flag 1=======Nothing workeded flag 1::::::::")
    else:
        return HttpResponse ("NABL Testing Progress/Pending")
        
    return render(request, 'po/area_store/po_nabl_result_resampling.html',{'name':sample_obj})






#-----------pd mishra work start from here---------------------



def tkc_nabl_sampling_wo(request):
    print("$$$$$$$$",dict(request.session))
    # nabl=User_Registration.objects.filter(otp=request.session['otp'],ContactNo=request.session['uid'],User_type=request.session['User_type'])
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    if nabl:
        wo_data = offer_material_site_stores.objects.filter(nabl_user__CompanyName_E=nabl.CompanyName_E,is_sampling_required=True,send_to_nabl=1,trf_status=1).distinct('wo_id').order_by('-wo_id')
        base_template_name = "nabl/nabl_Base.html"
        return render(request, 'sampling/sampling_wo_list.html', {'base_template_name':base_template_name,'wo_data':wo_data})
    else:
        return redirect(str(curl)+'/')

    
    
def nabl_sampling_offerlist(request,wo_id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    if nabl:
        offer_data = offer_material_site_stores.objects.filter(nabl_user__CompanyName_E=nabl.CompanyName_E,is_sampling_required=True,wo_id=wo_id,send_to_nabl=1,trf_status=1).distinct('tkc_di')
        wo_data = TKCWoInfo.objects.filter(id=wo_id)
        base_template_name = "nabl/nabl_Base.html"
        return render(request, 'sampling/sampling_offerlist.html', {'base_template_name':base_template_name,'wo_data':wo_data,'offer_data':offer_data})
    else:
        return redirect(str(curl)+'/')
    
    
def nabl_sampling_details(request,offer_no,tkc_di_id,item_code):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    if nabl:
        print("##################################")
        sampling_data=offer_material_serial_number.objects.filter(offer_no=offer_no,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1,offer__nabl_user__CompanyName_E=nabl.CompanyName_E,offer__tkc_di_id=tkc_di_id,offer__send_to_nabl=1,offer__trf_status=1,wo_material__item_code=item_code)
        base_template_name = "nabl/nabl_Base.html"
        return render(request, 'sampling/sample_details.html', {'base_template_name':base_template_name,'offer_data':sampling_data})
    else:
        return redirect(str(curl)+'/')
    
def nabl_sampling_receiving(request,id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    if nabl:
        sampling_data=offer_material_serial_number.objects.filter(id=id).update(Physical_Status_Nabl=1)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(str(curl)+'/')
    
def nabl_accept(request,id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    print("$$$$$$$$$$$",request.method)
    if nabl:
        if request.method == 'POST':
            nabl_status=request.POST.get('accept')
            print("###########",nabl_status)
            if nabl_status == 'accept':
                nabl_status=True
            else:
                nabl_status=False
            nabl_remark=request.POST.get('nabl_remark')
            nabl_report=request.FILES['nabl_report']
            nabl_date=datetime.datetime.now()
            sampling_data=offer_material_serial_number.objects.filter(id=id).first()
            sampling_data.nabl_report=nabl_report
            sampling_data.nabl_status=nabl_status
            sampling_data.nabl_date=nabl_date
            sampling_data.nabl_remark=nabl_remark
            sampling_data.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(str(curl)+'/')
    
    
def show_site_store_gate_pass(request,offer_no,tkc_di_id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    if nabl:
        gate_pass_data=offer_material_serial_number.objects.filter(offer__offer_no=offer_no,offer__tkc_di_id=tkc_di_id,offer__nabl_user__CompanyName_E=nabl.CompanyName_E).exclude(site_store_gatepass_id__isnull = True).distinct('site_store_gatepass_id')
        gate_pass_data1=offer_material_serial_number.objects.filter(offer__offer_no=offer_no,offer__tkc_di_id=tkc_di_id,offer__nabl_user__CompanyName_E=nabl.CompanyName_E,nabl_status__isnull=True).exclude(site_store_gatepass_id__isnull = True).distinct('site_store_gatepass_id')
        if gate_pass_data1:
            flag=0
        else:
            flag=1
        base_template_name = "nabl/nabl_Base.html"
        
        return render(request, 'sampling/tkc_gate_pass.html', {'base_template_name':base_template_name,'offer_data':gate_pass_data,'flag':flag})
    else:
        return redirect(str(curl)+'/')
    
def show_tkc_trf(request,offer_no,tkc_di_id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    if nabl:
        trf_data=offer_material_serial_number.objects.filter(offer__offer_no=offer_no,offer__tkc_di_id=tkc_di_id,offer__nabl_user__CompanyName_E=nabl.CompanyName_E,is_sampled=1).distinct('site_store_trf')
        # trf_data=Tkc_Work_Order_Trf_Details.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,nabl_user_id=nabl.User_Id)
        base_template_name = "nabl/nabl_Base.html"
        return render(request, 'sampling/tkc_trf_details.html', {'base_template_name':base_template_name,'offer_data':trf_data})
    else:
        return redirect(str(curl)+'/')

def tkc_nabl_item_details(request,offer_no,tkc_di_id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    if nabl:
        offer1=offer_material_serial_number.objects.filter(offer_no=offer_no,offer__tkc_di_id=tkc_di_id,offer__nabl_user__CompanyName_E=nabl.CompanyName_E,is_sampled=1).first()
        offer=offer_material_serial_number.objects.filter(offer_no=offer_no,offer__tkc_di_id=tkc_di_id,offer__nabl_user__CompanyName_E=nabl.CompanyName_E,is_sampled=1).distinct('wo_material')
        wo_data = TKCWoInfo.objects.filter(id=offer1.wo_id)
        print("=============================",wo_data)
        base_template_name = "nabl/nabl_Base.html"
        return render(request,'sampling/item_details.html',{'offer_data':offer,'base_template_name':base_template_name,'wo_data':wo_data})
    

def tkc_nabl_gate_pass(request,gate_pass_id,offer_no):
    print("##################",gate_pass_id)
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    gate_pass_detail=offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id)
    print("gate_pass_detail",gate_pass_detail)
    gate_pass_data=offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id).first()
    offer_data=offer_material_site_stores.objects.filter(offer_no=offer_no).first()
    
    from django.urls import reverse
    
    if nabl:
        if request.method == "POST":
            nabl_name = request.POST.get('nabl_name')
            gp_date = request.POST.get('gatepass_date')
            gp_num=request.POST.get('gatepass_no')
            gatekeep_name=request.POST.get('gk_name')
            veh_no=request.POST.get('vehicle_no')
            driv_name=request.POST.get('driver_name')
            driv_phone=request.POST.get('driver_phone')
            mater_rec_by=request.POST.get('mat_rece_by')
            
            driver_aadh=request.FILES['driver_aadhar']
        

            offer_no = offer_no
            
            
            gatepass_data = nabl_wo_outward_gatepass(offer_no = offer_no,gatepass_num=gp_num, gatekeeper_name=gatekeep_name,vehicle_no=veh_no,
                                driver_name=driv_name,driver_phone=driv_phone,gatepass_date=gp_date, 
                                material_rec_by=mater_rec_by,driver_aadhar=driver_aadh,nabl_user_id=nabl.User_Id,tkc_di_id=gate_pass_data.offer.tkc_di_id,site_store_id=gate_pass_data.offer.site_store_fk_id)
            gatepass_data.save()
            offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id).update(nabl_outward_gatepass_id=gatepass_data.id)
            
            
            nabl_gatepass_data=gatepass_data.id
            
            
            
            
            
            url = reverse('GatepassLetterView',args=[ nabl_gatepass_data,gate_pass_id])
            
            return redirect(url) 
            
        return render(request,'sampling/nabl_gatepass.html',{'site_store_gate_passdata':gate_pass_detail,'offer_data':offer_data,'gate_pass_data':gate_pass_data,'gate_pass_id':gate_pass_id})



def GatepassLetterView(request,nabl_gatepass_data,gate_pass_id):
    
    
    gate_pass_detail=offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id)
    gate_pass_data=offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id).first()
    gatepass_data=nabl_wo_outward_gatepass.objects.filter(id=nabl_gatepass_data).first()
    
    
    return render(request,'sampling/gatepass_letter.html',{'site_store_gate_passdata':gate_pass_detail,'nabl_gatepass_data':gatepass_data,'gate_pass_data':gate_pass_data,'gate_pass_id':gate_pass_id})
    
                
def tkc_nabl_gatepass_letter(request,gate_pass_id,nabl_gatepass_id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    
    gate_pass_detail=offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id)
    
    
    if nabl:
        if request.method == "POST":
            nabl_gatepass_data=nabl_wo_outward_gatepass.objects.filter(id=nabl_gatepass_id).first()
            gatepass = request.FILES['gatepass']
            nabl_gatepass_data.gatepass_letter=gatepass
            nabl_gatepass_data.save()
            offer_no=nabl_gatepass_data.offer_no
            print("len gate_pass_detail",len(gate_pass_detail))
            
            for i in gate_pass_detail:
                print("tkc_di_id",i.offer.tkc_di_id)
                accept_data=offer_material_serial_number.objects.filter(offer_no=offer_no,offer__tkc_di_id=i.offer.tkc_di_id,wo_material=i.wo_material,is_sampled=1,nabl_status__isnull=True)
                print("accept_data",accept_data)
                if accept_data :
                    pass
                    # return redirect(request.META.get('HTTP_REFERER'))
                else:
                    item_code=i.wo_material.item_code
                    
                    tkc_nabl_sampling_result(request,item_code,gate_pass_id)
            return redirect('tkc_nabl_sampling_wo')
            
            
def tkc_nabl_sampling_result(request,item_code,gate_pass_id):
    nabl=User_Registration.objects.filter(ContactNo=request.session['uid']).first()
    
    gate_pass_data=offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id)
    gate_pass_data1=offer_material_serial_number.objects.filter(site_store_gatepass_id=gate_pass_id).first()
    tkc_di_id=gate_pass_data1.tkc_di_id
    offer_no=gate_pass_data1.offer.offer_no
    offer_data = offer_material_site_stores.objects.filter(offer_no=offer_no,tkc_di_id=tkc_di_id,is_di_created=True,PDI_Assign=1,PDI_Complete=1,PDI_Approved_Status=1,is_sampling_required=True)
    item_code_s_obj=[]
    reject_steel_count=0
    steel_list=[]
    for i in offer_data:
        item_code_s_obj.append(i)
    
    product_data=product_sampling.objects.filter(item_code=item_code).first()
    if product_data is not None  and offer_no is not None:
        # print("product_data",product_data.sampling_id)
        product_sampling_info=Sampling_Info.objects.get(id=product_data.sampling_id)
        # print("product_sampling_info",product_sampling_info)
        offer_s=offer_material_serial_number.objects.filter(offer_no=offer_no,wo_material__item_code=item_code,Physical_Status_officer_check=1,offer__nabl_user__CompanyName_E=nabl.CompanyName_E).first()
        print("icode-----------------",item_code,"os---------",offer_s)

        if product_sampling_info.sample_type == 0:
            if product_sampling_info.name_of_material == "Steel Support/Section":
                sample_data_s=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1))
                reject_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1,nabl_status=False))
                accept_from_nabl_obj=[]
                if reject_data == []:
                    for j in item_code_s_obj:
                        product_data_steel=product_sampling.objects.filter(item_code=j.wo_material.item_code).first()
                        product_data_steel1=Sampling_Info.objects.filter(id=product_data_steel.sampling_id)
                        if product_data_steel1.name_of_material == "Steel Support/Section":
                            accept_from_nabl_obj.append(j)
                        
                    
                print("length sample_data",len(sample_data_s))
                material_name=product_sampling_info.name_of_material
                P_S_I_steel=Sampling_Info.objects.filter(name_of_material=material_name)
                steel_list=steel_list+sample_data_s
                sample_data_s=[]
                reject_steel_count=reject_steel_count+len(reject_data)
                
                
                
                    
            elif offer_s.serial_no == None:
                sample_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1))
                reject_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1,nabl_status=False))
                material_name=product_sampling_info.name_of_material
                P_S_I=Sampling_Info.objects.filter(name_of_material=material_name)
                sample_unit =len(sample_data)
                for i in P_S_I:
                    if sample_unit==i.sample_unit:
                        if len(reject_data)<=i.acceptable_unit:
                            accept_nabl_offer=offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code=item_code)
                            for i in accept_nabl_offer:
                                i.accept_from_nabl=1
                                i.received_from_nabl=1
                                i.save()
                

            else:
                print("###### in if")
                sample_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1))
                reject_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1,nabl_status=False))
                print("length sample_data",len(sample_data))
                material_name=product_sampling_info.name_of_material
                P_S_I=Sampling_Info.objects.filter(name_of_material=material_name)
                sample_unit = len(sample_data)
                for i in P_S_I:
                    if sample_unit==i.sample_unit:
                        if len(reject_data)<=i.acceptable_unit:
                            accept_nabl_offer=offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code=item_code)
                            for i in accept_nabl_offer:
                                i.accept_from_nabl=1
                                i.received_from_nabl=1
                                i.save()
        else:
            sample_data=list(offer_material_serial_number.objects.filter(offer_no=offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status_officer_check=1))
            reject_data=list(offer_material_serial_number.objects.filter(offer_no =offer_no,wo_material__item_code=item_code,is_sampled=1,Physical_Status=1,Physical_Status_officer_check=1,nabl_status=False))
            if len(reject_data)==0:
                accept_nabl_offer=offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code=item_code)
                for i in accept_nabl_offer:
                    i.accept_from_nabl=1
                    i.received_from_nabl=1
                    i.save()
                
        

        if steel_list != []: 
            for i in P_S_I_steel:
                if len(steel_list)== i.sample_unit:
                    if reject_steel_count==0:
                        for i in accept_from_nabl_obj:
                            i.received_from_nabl=1
                            i.accept_from_nabl=1
                            i.save()