# from asyncio.windows_events import NULL
# from gc import is_finalized
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import *
from main.models import *
import requests
from .resources import Collection_AgentResource
from tablib import Dataset
import math;
import random;
from datetime import date
from datetime import datetime
import datetime
import requests as req
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse


def generateOTP():
            OTPCA = ""
            digits = "0123456789"
            for i in range(6):
                OTPCA += digits[math.floor(random.random() * 10)]
            print(OTPCA)
            return OTPCA

# Create your views here.




def login(request):
    if request.method == "POST":
        oid = request.POST.get('mobile')
        request.session['oid']=oid
        if User_Registration_CA.objects.filter(Mobile=oid,Is_Enable = False).exists():
            return render(request, 'CA/index.html',{"msg":"Unable to login Your account is disable. For help contact administrator!!"})

        if User_Registration_CA.objects.filter(Mobile=oid,Payment_Status=1).exists():
            otp = generateOTP()
            Q = User_Registration_CA.objects.filter(Mobile=oid,Payment_Status=1)
            Q.update(Otp=otp)
            request.session['otp12'] = otp
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(request.session['oid']) + "&v1=" + str(otp) + "&v2=" + str()
            response = requests.get(url,proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = oid)
            sms_template.save()
                    
                    
                    
            return redirect('/ca/otp_verify')


        elif User_Registration_CA.objects.filter(Mobile=oid,Payment_Status=0).exists():
            not_register_user = User_Registration_CA.objects.get(Mobile=oid)
            if not_register_user.Aadhar is None:
                data = User_Registration_CA.objects.filter(Mobile=oid)
                otp = generateOTP()      
                data.update(Otp=otp)
                header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(request.session['oid']) + "&v1=" + str(otp) + "&v2=" + str()
                response = requests.get(url,proxies=proxyDict, headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = oid)
                sms_template.save()

                request.session['otp1'] = otp
                return redirect('/ca/otp_verify')

            data = User_Registration_CA.objects.filter(Mobile=oid)
            otp = generateOTP()      
            data.update(Otp=otp)
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(request.session['oid']) + "&v1=" + str(otp) + "&v2=" + str()
            response = requests.get(url,proxies=proxyDict, headers={'User-Agent': 'Chrome'})
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = oid)
            sms_template.save()

            request.session['otp11'] = otp
            return redirect('/ca/otp_verify')
                            
        else:    
            otp = generateOTP()
            ca_data = User_Registration_CA(Mobile=oid,Otp=otp)
            ca_data.save()
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(request.session['oid']) + "&v1=" + str(otp) + "&v2=" + str()
            response = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = oid)
            sms_template.save()
        
            request.session['otp'] = otp
            return redirect('/ca/otp_verify')
    return render(request, 'CA/index.html')



def otp_verify(request):
    if request.session.has_key('otp12'):
        r = request.session['otp12']
        otp = request.POST.get('otp')
        if request.method == "POST":
            if User_Registration_CA.objects.filter(Otp=otp,Payment_Status=1).exists():
                if otp == r:
                    agent = User_Registration_CA.objects.filter(Otp=otp)
                    request.session['otp'] = otp
                    return render(request, 'CA/ca_dashboard.html',{'data1':agent[0]})


    if request.session.has_key('otp11'):
        r = request.session['otp11']
        otp = request.POST.get('otp')
        if request.method == "POST":
            if User_Registration_CA.objects.filter(Otp=otp,Payment_Status=0).exists():
                if otp == r:
                    agent = User_Registration_CA.objects.get(Otp=otp)
                    mobile = agent.Mobile
                    request.session['oid']=mobile
                    request.session['xyz'] = otp
                    request.session['otp'] = otp
                    return payment(request)

    if request.session.has_key('otp1'):
        f = request.session['otp1']
        otp = request.POST.get('otp')
        if request.method == "POST":
            if User_Registration_CA.objects.filter(Otp=otp,Payment_Status=0).exists():
                if otp == f:
                    agent = User_Registration_CA.objects.get(Otp=otp)
                    mobile = agent.Mobile
                    request.session['xyz'] = otp
                    request.session['otp'] = otp
                    return render(request, 'CA/reg.html',{'mobile':mobile})


                
    if request.session.has_key('otp'):
        if request.method == "POST":
            s = request.session['otp']
            otp = request.POST.get('otp')
            if otp == s:
                dash = User_Registration_CA.objects.get(Otp=otp)
                mobile = dash.Mobile
                request.session['Mobile'] = mobile
                request.session['otp'] = otp
                request.session['xyz'] = otp
                return render(request, 'CA/reg.html',{'mobile':mobile})

            else:
                messages.warning(request, "Otp not matched, Kindly enter valid otp")
                return render(request, 'CA/otp_verify.html')


    return render(request, 'CA/otp_verify.html')



def regca(request):
    if request.session.has_key('xyz'):
    
        if request.method == "POST":
            
            mobile = request.POST.get('mobile')
            name = request.POST.get('name')
            
            fname = request.POST.get('fname')
            aadhar =request.POST.get('aadhar')
            email = request.POST.get('email')
            print(email)
            pan = request.POST.get('pan')
            gst = request.POST.get('gst')
            bill = request.POST.get('bill')
            dob = request.POST.get('dob')
            print(dob)
            gender=request.POST.get('gender')
            print(gender,"-------------")
            
            banlk_name = request.POST.get('bank_name')
            account_holder_name = request.POST.get('ac_holder_name')
            account_number = request.POST.get('ac_number')
            ifsc_number = request.POST.get('ifsc')
            re_ac_number = request.POST.get('re_ac_number')
            energy_image=request.FILES['bill_twenty']
            file_name = default_storage.save(energy_image.name, energy_image)
          
            pan_image = request.FILES['twenty_two']
            file_name = default_storage.save(pan_image.name, pan_image)
         
            gst_image = request.FILES.get('twenty',None)
            file_name = default_storage.save(gst_image.name, gst_image)
          
            add1 = request.POST.get('add1')
            add2 = request.POST.get('add2')
            pincode = request.POST.get('zip')            
            add3 = request.POST.get('add3')           
            add4 = request.POST.get('add4')            
            city = request.POST.get('city')            
            district=request.POST.get('district')
           
           
            ContractorId = ""
            digits = "0123456789"
            not_register_user = User_Registration_CA.objects.get(Mobile=mobile)
            for i in range(4):
                ContractorId += digits[math.floor(random.random() * 10)]
            if User_Registration_CA.objects.filter(Mobile=mobile).exists():
                if not_register_user.Aadhar is not None: 
                    messages.warning(request, "Mobile Number already registered")
                    return render(request, 'CA/reg.html')
            if User_Registration_CA.objects.filter(Email_Id=email).exists():
                if not_register_user.Aadhar is not None:
                    messages.warning(request, "Email ID already registered")
                    return render(request, 'CA/reg.html')
            elif User_Registration_CA.objects.filter(Contractor_Id=ContractorId).exists():
                if not_register_user.Aadhar is not None:
                    messages.warning(request, "Contractor ID already registered Fill Again")
                    return render(request, 'CA/reg.html') 
            else:
                
                user_details = User_Registration_CA.objects.filter(Otp=request.session['xyz'])
                
                
                user_details.update(Contractor_Id=ContractorId,Collection_Agent_Name=name,Gst_Confirm=gst,Gender=gender,Dob=dob,Enery_bill_image=energy_image,Pan_Card_Image=pan_image,Gst_Image=gst_image,Name=name, Father_name=fname,
                                                    Aadhar=aadhar, Pan=pan,
                                                    Enery_bill=bill, Gst=gst,
                                                    Email_Id=email, Mobile=mobile,Bank_name=banlk_name, Account_Holder_Name=account_holder_name,Account_Number=account_number, IFSC=ifsc_number,
                                                    Add1=add1,Add2=add2,State=add4,Pincode=pincode,City=city,District=district, Add_Date = datetime.datetime.now(),payment_date = datetime.datetime.now())
               
                messages.warning(request, "You are successfully registered")
                return redirect('/ca/payment')

    return render(request, 'CA/reg.html')

def detail_by_pincode(request,pincode_number):    
    all_record = Pin_Code_Table_Master.objects.filter(Pincode_number=pincode_number).values()    
    data=list(all_record)
    # print(data,"Pincode1111")
   
    #return render(request, 'CA/reg.html',{'data':data})
    return JsonResponse({"data": data})
#----------dashboard--------------------------------------------------------------------------
 


def basic(request):
    userdata = User_Registration_CA.objects.get(Otp=request.session['otp'])

    return render(request, 'CA/basicinfo.html', {'userdata':userdata})


# CA0001
def ae_dashboard(request):
    if request.session.has_key('otp'):
        return render(request, 'CA/ae_dashboard.html')
    return render(request, 'CA/index.html')



#CAM001

def commercial(request):

    if request.session.has_key('otp'):
        return render(request, 'CA/commercial_sales.html')

    return render(request, 'CA/mpeb_reg.html')

#CAF001

def finance(request):

    if request.session.has_key('otp'):
        return render(request, 'CA/fi_dashborad.html')

    return render(request, 'CA/mpeb_reg.html')


#--------------adminagent----------------------------------------------------------------

def agents_details(request):
    all_agent = User_Registration_CA.objects.all()
    return render(request,'CA/agent_details.html',{'data1':all_agent})


def agents_all_details(request,id):
    all_agent = User_Registration_CA.objects.filter(User_Id=id)
    data =  User_Registration_CA.objects.get(User_Id=id)
    con = data.Mobile
    request.session['con'] = con
    return render(request,'CA/agent_all_details.html',{'data1':all_agent})


def agents_upload_detail(request):
    if request.session.has_key('con'):
        all_agent = User_Registration_CA.objects.filter(Mobile=request.session['con'])
        CA_NAME =  request.POST.get('CA_NAME')
        GENDER =  request.POST.get('GENDER')
        COLL_AGENT_NAME =  request.POST.get('COLL_AGENT_NAME')
        mobile = request.session['con']
        SIGN_STATUS =  request.POST.get('SIGN_STATUS')
        IVRS_NO =  request.POST.get('IVRS_NO')
        REFERENCE_NO =  request.POST.get('REFERENCE_NO')
        CONTRACTOR_ID =  request.POST.get('CONTRACTOR_ID')

        data = All_Collection_Agent(Mobile=mobile,CA_NAME=CA_NAME,GENDER=GENDER,COLL_AGENT_NAME=COLL_AGENT_NAME,SIGN_STATUS=SIGN_STATUS,IVRS_NO=IVRS_NO,REFERENCE_NO=REFERENCE_NO,CONTRACTOR_ID=CONTRACTOR_ID)
       
        data.save()
        return render(request,'CA/agents_upload_detail.html',{'data1': all_agent})
    return render(request,'CA/agents_upload_detail.html')
        
    

def agents_details_ae(request):
    all_agent = User_Registration_CA.objects.filter(Is_Approved=0)
    return render(request,'CA/agents_details_ae.html',{'data1':all_agent})


def agents_report(request,id):
    all_agent = User_Registration_CA.objects.filter(User_Id=id)
    return render(request,'CA/agents_details_ae.html',{'data1':all_agent})


def agents_all_details_ae(request,id):
    all_agent = User_Registration_CA.objects.filter(User_Id=id)
    if request.method == "POST":
        user = request.POST.get('user')
        if user == 'Accept':
            all_agent = User_Registration_CA.objects.filter(User_Id=id)
            all_agent.update(Is_Approved=1)
            return redirect('agents_details_ae')
        elif user == 'Reject':
            all_agent = User_Registration_CA.objects.filter(User_Id=id)
            all_agent.update(Is_Approved=-1)
            return redirect('agents_details_ae')
    return render(request,'CA/agent_all_details_ae.html',{'data1':all_agent})



def approved_agents_details_ae(request):
    all_agent = User_Registration_CA.objects.filter(Is_Approved=1)
    return render(request,'CA/approved_agents_details_ae.html',{'data1':all_agent})



def reject_agents_details_ae(request):
    all_agent = User_Registration_CA.objects.filter(Is_Approved=-1)
    return render(request,'CA/reject_agents_details_ae.html',{'data1':all_agent})



def transaction_upload(request):
    if request.session.has_key('otp'):
        if request.method == "POST":
            # Collection_Agent_Resource = Collection_AgentResource()
            dataset = Dataset()
            new_agent = request.FILES['File1']

            # if not new_agent.name.endwith('xlms'):
            #     messages.info(request,'wrong')
            #     return render(request,'CA/transaction_upload.html')

            important = dataset.load(new_agent.read(),format='xlsx')
            for data in important:
              
                value = Collection_Agent(
                    Name=data[0],
                    Customomer_Id=data[1],
                    Customer_name=data[2],
                    Customer_bill_amount=data[3],
                    Customer_payment_date=data[4],
                    Customer_payment_month=data[5],
                    Customer_payment_year=data[6],
                    Month=data[7],
                    Is_commission=data[8],
                    commission_amount=data[9],
                    Gst_ammount=data[10],
                    Collection_agent_id=data[11],
                    Collection_agent_Name=data[12],
                    Contractor_id=data[13],
                    Is_process=data[14],
                    Is_Gst=data[15]
                )
                value.save()

        return render(request,'CA/transaction_upload.html')
    return render(request,'CA/transaction_upload.html')

    # return render(request, 'CA/otp_verify.html')

def uploaded_data(request):
    if 'search' in request.GET:
        search = request.GET['search']
        data = Collection_Agent.objects.filter(Customer_payment_month__icontains=search).order_by('Customer_payment_date')
    else:
        data = Collection_Agent.objects.all().order_by('Customer_payment_date')
    return render(request,'CA/view_uploaded_data.html',{'data':data})


def all_collectionagent(request):
    paginate_by = 25
    model = Collection_Agent
    all_agent = Collection_Agent.objects.all()
    paginator = Paginator(all_agent, 25) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'CA/view_all_data.html', {'data1':page_obj})



# def all_collectionagent(request):
#     if request.session.has_key('otp'):
#         paginate_by = 25
#         model = Collection_Agent
#         a = User_Registration_CA.objects.get(Otp=request.session['otp'])
#         b = a.Mobile
#         all_agent = Collection_Agent.objects.filter(Collection_agent_id=b)

#         #all_agent = Collection_Agent.objects.filter(Collection_agent_id=request.session['con'])
        
#         print(all_agent)
#         paginator = Paginator(all_agent, 25) # Show 25 contacts per page.

#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page('page_number')
#         search_post = request.GET.get('search')
#         if search_post:
#             page_obj = Collection_Agent.objects.filter(Q(Collection_agent_id__icontains=search_post) & Q(Customer_payment_month__icontains=search_post))
#         else:
#             page_obj = Collection_Agent.objects.all()

#         return render(request,'CA/all_collection_agentdata.html', {'data1':page_obj})
#     else:
#         return render(request,'CA/all_collection_agentdata.html', {'data1':page_obj})

        
#         # return render(request, 'CA/otp_verify.html')



def all_collection_agentdata(request):
    if request.session.has_key('otp'):
        paginate_by = 25
        model = Collection_Agent
        a = User_Registration_CA.objects.get(Otp=request.session['otp'])
        b = a.Mobile
        all_agent = Collection_Agent.objects.filter(Collection_agent_id=b)


        #all_agent = Collection_Agent.objects.filter(Collection_agent_id=request.session['con'])
       
        paginator = Paginator(all_agent, 25) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request,'CA/all_collection_agentdata.html', {'data1':page_obj})

    return render(request, 'CA/otp_verify.html')



def logout(request):
    del request.session['otp']
    return redirect('/')

#--------------collectionagent-------------------------------------------------------------------


def agents_details_ce(request):
    if request.session.has_key('otp'):
        paginate_by = 25
        model = Collection_Agent
        user_data = User_Registration_CA.objects.get(Otp=request.session['otp'])
      
        Contractorid = user_data.Contractor_Id
        all_agent = Collection_Agent.objects.filter(Contractor_id=Contractorid)
    
   
        paginator = Paginator(all_agent, 25) # Show 25

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        # search_post = request.GET.get('search')
        # if search_post:
        #     page_obj = Collection_Agent.objects.filter(Q(Collection_agent_id=b)&(Q(Collection_agent_id__icontains=search_post) & Q(Customer_payment_month__icontains=search_post)))
        # else:
        #     page_obj = Collection_Agent.objects.filter(Collection_agent_id=b)


        return render(request,'CA/all_collection_agentdata.html', {'data1':page_obj,'user_data':user_data})
    else:
        return render(request, 'CA/otp_verify.html')


###agents_details_ce_pending
# if 'search' in request.GET:
#         search = request.GET['search']
#         data = Collection_Agent.objects.filter(Customer_payment_month__icontains=search)

def agent_search(request):
    if request.session.has_key('otp'):
        user_data = User_Registration_CA.objects.get(Otp=request.session['otp'])
        return render(request,'CA/agent_search.html',{'user_data':user_data})
    else:
        return render(request, 'CA/otp_verify.html')


def agents_details_ce_pending(request):
 
    if request.session.has_key('otp'):
        if 'Date_value' in request.GET:
            search = request.GET['Date_value']
            print(type(search))
            user_data = User_Registration_CA.objects.get(Otp=request.session['otp'])
            Contractorid = user_data.Contractor_Id
            all_agent = Collection_Agent.objects.filter(Month=search,Contractor_id=Contractorid,Month__icontains=search,invoce=0)
        
        else:
            # user_data = User_Registration_CA.objects.get(Otp=request.session['otp'])
            # Contractorid = user_data.Contractor_Id
            # all_agent = Collection_Agent.objects.filter(Contractor_id=Contractorid,invoce=0)
            return render(request,'CA/agents_details_ce_pending.html')  
        return render(request,'CA/agents_details_ce_pending.html', {'data1':all_agent,'user_data':user_data})

    return render(request, 'CA/otp_verify.html')


def agents_details_otp(request):
    if request.method == "POST":
        val_list1 = request.POST.getlist('checkbox')
        request.session['val_list1']=val_list1
        def generateOTP():
            OTPCA = ""
            digits = "0123456789"
            for i in range(6):
                OTPCA += digits[math.floor(random.random() * 10)]
            return OTPCA
        otpAcca = generateOTP()
        print(otpAcca)
        data_show = User_Registration_CA.objects.get(Otp=request.session['otp'])
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(data_show.Mobile) + "&v1=" + str(otpAcca) + "&v2=" + str()
        response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = data_show.Mobile)
        sms_template.save()
        request.session['otpAcca']=otpAcca

    return render(request,'CA/agents_details_otp.html',{'otpAcca':request.session['otpAcca']})


import datetime

def gen_invoice_ca(request):
    if request.session.has_key('otp'):
        if request.method == "POST":
            otpdata=request.POST.get('otp')
            if otpdata==request.session['otpAcca']:
                user_data = User_Registration_CA.objects.get(Otp=request.session['otp'])
                Contractorid = user_data.Contractor_Id
                if Collection_Agent.objects.filter(invoce=0,Contractor_id=Contractorid):
                    User_Zone = "CZ"
                    User = "VENDOR"
                    invoice = "MPEB"
                    list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    s = ""
                    s = s + invoice+User_Zone + random.choice(list1) + random.choice(list1) + random.choice(list1) + random.choice(list1)
                   
                    val = request.session['val_list1']
                    sum_of_commison=0
                    data2 = []
                    coun_data=0
                    gst_sum=0.0

                    for a_id in val:
                        all_agent = Collection_Agent.objects.filter(id=a_id)
                        for data in all_agent:
                            data.invoce=1
                            data.Invoice_Number=s
                            # data.Agent_log=user_data
                            data.save()
                            Month = data.Month
                            coun_data+=1
                            gst_sum+=round(float(data.Gst_ammount),2)

                            sum_of_commison+=int(data.commission_amount)
                            # coun_data = Collection_Agent.objects.filter(id=a_id,invoce=1).count()
                            data1 = Collection_Agent.objects.filter(id=a_id,invoce=1)
                            data2.append(data1)
                    # print(User_Registration_CA.objects.get(Otp=request.session['otp'],Gst__isnull=True))
                    if user_data.Gst:
                        Commission_Amount=sum_of_commison
                        gst_sum1=round(gst_sum,2)
                        Cgst=round(gst_sum/2,2)
                        Sgst=round(gst_sum/2,2)
                        Grand_Total = round(sum_of_commison+Cgst+Sgst,2)
                        today = datetime.datetime.now()
                        Contractor_Id=user_data.Contractor_Id
                        Invoice_Number=s
                        Agent_log=user_data
                        Name=user_data.Name
                        Father_name=user_data.Father_name
                        Aadhar=user_data.Aadhar
                        Pan=user_data.Pan
                        Email_Id=user_data.Email_Id
                        Mobile=user_data.Mobile
                        Bank_name=user_data.Bank_name
                        Account_Holder_Name=user_data.Account_Holder_Name
                        Account_Number=user_data.Account_Number
                        IFSC=user_data.IFSC
                        Add1=user_data.Add1
                        Add2=user_data.Add2
                        State=user_data.State
                        Pincode=user_data.Pincode
                        City=user_data.City
                        District=user_data.District
                        Payable_Amount=Grand_Total
                        alldata=Generated_Invoice(Total_Invoices=coun_data,Payable_Amount=Payable_Amount,Service_Date=Month,Agent_log=Agent_log,Invoice_Number=Invoice_Number,Commission_Amount=Commission_Amount,Cgst=Cgst,Sgst=Sgst,Created_Date=today,
                            Contractor_Id=Contractor_Id,Name=Name,Father_name=Father_name,Aadhar=Aadhar,Pan=Pan,Email_Id=Email_Id,
                            Mobile=Mobile,Bank_name=Bank_name,Account_Holder_Name=Account_Holder_Name,Account_Number=Account_Number,
                            IFSC=IFSC,Add1=Add1,Add2=Add2,State=State,Pincode=Pincode,City=City,District=District)
                        alldata.save()

                        return render(request,'CA/generate_mrc.html',{'Month':Month,'s':s,'Grand_Total':Grand_Total,'gst_sum':gst_sum1,'sum_of_commison':sum_of_commison,'data2':data2,'user_data':user_data,'coun_data':coun_data,'today':today})
                    else:
                        Commission_Amount=sum_of_commison
                        Grand_Total = round(sum_of_commison,2)
                        today = datetime.datetime.now()
                        Contractor_Id=user_data.Contractor_Id
                        Invoice_Number=s
                        Agent_log=user_data
                        Name=user_data.Name
                        Father_name=user_data.Father_name
                        Aadhar=user_data.Aadhar
                        Pan=user_data.Pan
                        Email_Id=user_data.Email_Id
                        Mobile=user_data.Mobile
                        Bank_name=user_data.Bank_name
                        Account_Holder_Name=user_data.Account_Holder_Name
                        Account_Number=user_data.Account_Number
                        IFSC=user_data.IFSC
                        Add1=user_data.Add1
                        Add2=user_data.Add2
                        State=user_data.State
                        Pincode=user_data.Pincode
                        City=user_data.City
                        District=user_data.District
                        Payable_Amount=Grand_Total
                        alldata=Generated_Invoice(Total_Invoices=coun_data,Payable_Amount=Payable_Amount,Service_Date=Month,Agent_log=Agent_log,Invoice_Number=Invoice_Number,Commission_Amount=Commission_Amount,Created_Date=today,
                            Contractor_Id=Contractor_Id,Name=Name,Father_name=Father_name,Aadhar=Aadhar,Pan=Pan,Email_Id=Email_Id,
                            Mobile=Mobile,Bank_name=Bank_name,Account_Holder_Name=Account_Holder_Name,Account_Number=Account_Number,
                            IFSC=IFSC,Add1=Add1,Add2=Add2,State=State,Pincode=Pincode,City=City,District=District)
                        alldata.save()

                        return render(request,'CA/generate_mrc.html',{'Month':Month,'s':s,'Grand_Total':Grand_Total,'sum_of_commison':sum_of_commison,'data2':data2,'user_data':user_data,'coun_data':coun_data,'today':today})

                else:
                    return redirect('/ca/agents_details_ce_pending')
            else:
                return render(request,'CA/agents_details_otp.html')
        else:
            return redirect('/ca/agent_search')

    else:
        return render(request, 'CA/otp_verify.html')



def commerical_ce_pending(request):
    if request.session.has_key('otp'):
        all_Invoice = Generated_Invoice.objects.filter(Commercial_Flag=0)
      
        
        return render(request,'CA/commerical_ce_pending.html', {'data1':all_Invoice})

    return render(request, 'CA/otp_verify.html')

def commerical_invoice_ca_otp(request):
    if request.method=="POST":
        val_list = request.POST.getlist('checkbox')
        request.session['val_list']=val_list
        def generateOTP():
            OTPCA = ""
            digits = "0123456789"
            for i in range(6):
                OTPCA += digits[math.floor(random.random() * 10)]
            return OTPCA
        otpca = generateOTP()
        data = Officer.objects.get(employ_login_id='commercial')
        print(data.mobile)
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(data.mobile) + "&v1=" + str(otpca) + "&v2=" + str()
        response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        
        sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = data.mobile)
        sms_template.save()
        
        request.session['otpca']=otpca
    return render(request,'CA/commerical_invoice_ca_otp.html',{'otpca':request.session['otpca']})


def commerical_invoice_ca(request):
    if request.session.has_key('otp'):
        if request.method=="POST":
            otp_data = request.POST.get('otp')
            today = datetime.datetime.now()
            
            if otp_data==request.session['otpca']:
                val = request.session['val_list']
                # val = request.POST.getlist('checkbox')
                Generated_list = []
                total_invoice = 0
                total_gst = 0.0
                total_Sgst = 0.0
                total_Commission_Amount = 0.0
                all_total = 0.0
                Reference_No=""
                digits = "0123456789"
                for i in range(7):
                    Reference_No += digits[math.floor(random.random() * 10)]

                for v_id in val:
                    print(v_id)
                    Generated_Invoice_Data = Generated_Invoice.objects.filter(id=v_id,Commercial_Flag=0)
                    Generated_list.append(Generated_Invoice_Data)
                    total_invoice+=1
                    for data in Generated_Invoice_Data:
                        data.Commercial_Flag=1
                        data.Reference_No=Reference_No
                        data.save()



                        total_gst+=float(data.Cgst)
                        total_Sgst+=float(data.Sgst)
                        total_Commission_Amount+=float(data.Commission_Amount)
                for a in Generated_list:
                    for b in a:
                        a=b.Invoice_Number
               
                all_total=round(total_Commission_Amount+total_gst+total_Sgst,2)
                gst_sgst =round(total_gst+total_Sgst,2)
                for data in Generated_list:
                    for data_list in data:
                        ContractorId=data_list.Contractor_Id
                Cm_invoice=Commerical_invoice(Reference_No=Reference_No,Invoice_number=a,Total_Commision=total_Commission_Amount,Total_Invoices=total_invoice,Total_Payable_Amount=all_total,Contractor_Id=ContractorId,Created_Date=today)
                Cm_invoice.save()
                return render(request,'CA/commerical_invoice_ca.html',{'gst_sgst':gst_sgst,'all_total':all_total,'all_total':all_total,'total_Commission_Amount':total_Commission_Amount,'total_Sgst':total_Sgst,'total_gst':total_gst,'total_invoice':total_invoice,'Generated_list':Generated_list,'today':today})
            else:
                return render(request,'CA/commerical_invoice_ca_otp.html')
        else:
            return render(request,'CA/commerical_invoice_ca.html')
    else:
        return render(request, 'CA/otp_verify.html')

def Cash_Voucher_list(request):
    Cash_Voucher=Commerical_invoice.objects.all()
    return render(request,'CA/Cash_Voucher_list.html',{'Cash_Voucher':Cash_Voucher})



def Cash_Voucher(request,id):
    Cash_Voucher=Commerical_invoice.objects.get(id=id)

    return render(request,'CA/Cash_Voucher.html',{'Cash_Voucher':Cash_Voucher})

def fi_Cash_Voucher(request,id):
    Cash_Voucher=Commerical_invoice.objects.get(id=id)
    return render(request,'CA/fi_Cash_Voucher.html',{'Cash_Voucher':Cash_Voucher})



def commerical_invoice(request,id):
    
    all_agent = invoice.objects.filter(id=id,commercial=0)

    name = all_agent[0].invoice_user_reg.Name
    address  = all_agent[0].invoice_user_reg.Add1

    Pincode = all_agent[0].invoice_user_reg.Add1
    bank_name = all_agent[0].invoice_user_reg.Bank_name
    Account_Holder_Name = all_agent[0].invoice_user_reg.Account_Holder_Name
    Account_Number = all_agent[0].invoice_user_reg.Account_Number
    IFSC =  all_agent[0].invoice_user_reg.IFSC
    email =  all_agent[0].invoice_user_reg.Email_Id



    commission_amount = all_agent[0].commission_amount
    date = all_agent[0].date
    gst_amount = all_agent[0].gst_amount
    total = commission_amount + gst_amount
    date = all_agent[0].date
    bill_amount = all_agent[0].bill_amount
    d = all_agent[0].id
    Gst =  all_agent[0].invoice_user_reg.Gst
    Mobile =  all_agent[0].invoice_user_reg.Mobile
    date = all_agent[0].date
    data123=all_agent[0].id
    def generateOTP():
        OTP = ""
        digits = "0123456789"
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP
    otp = generateOTP()
    request.session['otp'] = otp
    all_agent = invoice.objects.filter(id=id,commercial=0)
    all_agent.update(otp = otp)
    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(oid) + "&v1=" + str(otp) + "&v2=" + str()
    # response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
    # request.session['otp'] = otp


    
    return render(request,'CA/commerical_invoice.html', {'data1':all_agent,'data123':data123,'name':name,'address':address,'Pincode':Pincode,'commission_amount':commission_amount,'gst_amount':gst_amount,'total':total,
                                                        'bank_name':bank_name,'Account_Holder_Name':Account_Holder_Name,'Account_Number':Account_Number,'IFSC':IFSC,
                                                        'bill_amount':bill_amount,'date':date,'d':d,'email':email,'Gst':Gst,'Mobile':Mobile,'date':date})





def commerical_invoice2(request,title):
    Invoice_sum = Commerical_invoice.objects.get(Reference_No=title)
    Generated_In = Generated_Invoice.objects.filter(Reference_No=title)
    gst_list = []
    for i in Generated_In:
        gst_list.append(i.Cgst)
        gst_list.append(i.Sgst)
    gst_sum = sum(gst_list)
    # all_agent = Generated_Invoice.objects.get(Commercial_Flag=1,Invoice_Number=title)
    # data_count = Collection_Agent.objects.filter(Invoice_Number=title).count()
    # data_cou = Collection_Agent.objects.filter(Invoice_Number=title)
    
    # all_agent = invoice.objects.filter(id=id,commercial=1).count()
    # agent = invoice.objects.filter(id=id,commercial=1)
   
    # gst = agent[0].gst_amount
    # commission = agent[0].commission_amount
    # gst = agent[0].gst_amount
    # total = gst+commission
   
 
    return render(request,'CA/final_invoice.html',{'Invoice_sum':Invoice_sum,'Generated_Invoice':Generated_In,"gst_sum":gst_sum})


    
    # return render(request,'CA/commerical_invoice2.html',{'data':all_agent,'gst_amount':gst_amount,'commission_amount':commission_amount})



def commerical_approve_save(request,id):
    all_agent = invoice.objects.filter(id=id,commercial=0)
    
    

    return render(request,'CA/commerical_invoice.html', {'data1':all_agent})



def commerical_approved(request):
    all_agent1 = Generated_Invoice.objects.filter(Commercial_Flag=1)
    all_agent = Commerical_invoice.objects.all()

    return render(request,'CA/commerical_approved.html', {'data1':all_agent})


def invoice_otp(request):
    all_agent = request.session['otp']
    aaaa = invoice.objects.get(otp = all_agent)
    if request.method == "POST":
        abc = request.POST.get('otp')
        if abc == aaaa.otp:
            
            all_agent = invoice.objects.filter(otp = abc)
            all_agent.update(commercial=1)
            # pcv_data = invoice.objects.filter(commercial=1)
            commission_amount = all_agent[0].commission_amount
            gst_amount = all_agent[0].gst_amount
            total =  gst_amount+commission_amount
            Bank_name = all_agent[0].invoice_user_reg.Bank_name
            name = all_agent[0].invoice_user_reg.Name
            Reference_No = all_agent[0].invoice_user_reg.Reference_No
            City = all_agent[0].invoice_user_reg.City
            d = all_agent[0].id
            date = all_agent[0].date




            return render(request,'CA/pcv_invoice.html',{'commission_amount':commission_amount,'Bank_name':Bank_name,'name':name,'Reference_No':Reference_No,'City':City,'total':total,'d':d,'date':date})

            # return HttpResponse('verified by commericial')
        else:
            return render(request,'CA/invoice_otp.html')

    return render(request,'CA/invoice_otp.html')



def pcv_invoice(request):
    Cash_Voucher=Commerical_invoice.objects.all()
    return render(request,'CA/pcv_invoice.html',{'Cash_Voucher':Cash_Voucher})

 

 

def finance_details_pending(request):
    if request.session.has_key('otp'):
        finance_data = Commerical_invoice.objects.all()
      
        
        return render(request,'CA/finance_details_pending.html', {'data1':finance_data})

    return render(request, 'CA/otp_verify.html')

        


def finance_invoice(request,title):
    Invoice_sum = Commerical_invoice.objects.get(Reference_No=title)
    Generated_In = Generated_Invoice.objects.filter(Reference_No=title)


    
    return render(request,'CA/finance_invoice.html',{'Invoice_sum':Invoice_sum,'Generated_Invoice':Generated_In})





def finance_invoice_otp(request):
    all_agent = request.session['otp']
    aaaa = invoice.objects.get(otp = all_agent)
    if request.method == "POST":
        abc = request.POST.get('otp')
        if abc == aaaa.otp:
            
            all_agent = invoice.objects.filter(otp = abc)
            all_agent.update(finance=1)
            # # pcv_data = invoice.objects.filter(commercial=1)
            # print('-----------',all_agent)
            # commission_amount = all_agent[0].commission_amount
            # print(commission_amount)
            # gst_amount = all_agent[0].commission_amount
            # total =  gst_amount+commission_amount
            # print(total)
            # Bank_name = all_agent[0].invoice_user_reg.Bank_name
            # name = all_agent[0].invoice_user_reg.Name
            # Reference_No = all_agent[0].invoice_user_reg.Reference_No
            # City = all_agent[0].invoice_user_reg.City
            # d = all_agent[0].id
            # date = all_agent[0].date




            #return render(request,'CA/pcv_invoice.html',{'commission_amount':commission_amount,'Bank_name':Bank_name,'name':name,'Reference_No':Reference_No,'City':City,'total':total,'d':d,'date':date})

            return HttpResponse('verified by commericial')
        else:
            return render(request,'CA/finance_invoice_otp.html')

    return render(request,'CA/finance_invoice_otp.html')

def ca_invoice(request):
    if request.session.has_key('otp'):
        user_data = User_Registration_CA.objects.get(Otp=request.session['otp'])
        data=Generated_Invoice.objects.filter(Agent_log=user_data)
        return render(request,'CA/ca_invoice.html',{'data':data,'user_data':user_data})
    else:
        return render(request, 'CA/otp_verify.html')


def ca_invoice_details(request,title):
    data=Generated_Invoice.objects.get(Invoice_Number=title)
    gen = Collection_Agent.objects.filter(Invoice_Number=title)

    return render(request,'CA/ca_invoice_details.html',{'data':data,'gen':gen})

def finance_approve_save(request,id):
    all_agent = invoice.objects.filter(id=id,finance=0)
    


    return render(request,'CA/finance_invoice.html', {'data1':all_agent})





  


def commerical_details_save(request,id):
    
    if request.session.has_key('otp'):
        a = User_Registration_CA.objects.get(Otp=request.session['otp'])
        b = a.Mobile
        all_agent = Collection_Agent.objects.filter(invoce=1)

        # abc = request.session['var'] 
        # print("ggggggggg",abc)
        if b == a.Mobile:
            all_agent.update(invoce=2)
            agent = User_Registration_CA.objects.filter(Otp=request.session['otp'])
            abc = Collection_Agent.objects.filter(Collection_agent_id=b)
            adding = Collection_Agent.objects.filter(Collection_agent_id=b)
            g = adding[0].Gst_ammount
            q = adding[0].commission_amount 
            z = adding[0].Customer_bill_amount
            p = q+g




            Customer_bill_amount = adding[0].Customer_bill_amount
            Customer_bill_amountByTwo = float(z) / 2

            commission_amount=adding[0].commission_amount
            # commission_amountByTwo = float(commission_amount) / 2
            commission_amountByTwo = float(q) / 2

 
            Gst_ammount=adding[0].Gst_ammount
            Gst_ammountByTwo = float(g) / 2
            

            # Customer_bill_amountByTwo=float(Customer_bill_amountByTwo+z)
            # print('Customer_bill_amountByTwoCustomer_bill_amountByTwo',Customer_bill_amountByTwo)

           
            
            return render(request,'CA/generate_mrc1.html', {'z':z,'q':q,'g':g,'data1':all_agent,'data':agent[0],'a':abc[0],'add':p})

        return render(request,'CA/commerical_details_save.html', {'data1':all_agent})
    else:
        return render(request, 'CA/otp_verify.html')


def commerical_pending(request):

    newdata = invoice.objects.filter(commercial=1)
   

    invoice12 = invoice.objects.latest('id')


    transaction = Collection_Agent.objects.filter(invoce_no = invoice12.id)
   

    data = Collection_Agent.objects.filter(invoce=1)
    data.invoce_no=invoice12.id

    total = invoice12.commission_amount + invoice12.gst_amount + invoice12.gst_amount
    return render(request,'CA/commerical_invoice.html',{'data':invoice12,'total':round(total,2),'transaction':transaction})

        
    #return render(request,'CA/commerical_invoice.html',{'data':data})    



def finance_pending(request):

    newdata = invoice.objects.filter(finance=1)
    invoice12 = invoice.objects.latest('id')
  

    transaction = Collection_Agent.objects.filter(invoce_no = invoice12.id)
   
    data = Collection_Agent.objects.filter(invoce=1)
    data.invoce_no=invoice12.id

    total = invoice12.commission_amount + invoice12.gst_amount + invoice12.gst_amount
    return render(request,'CA/commerical_invoice.html',{'data':invoice12,'total':round(total,2),'transaction':transaction})

        
    #return render(request,'CA/commerical_invoice.html',{'data':data})    






# def gen_invoice_ca(request):
#     print('gggggggggggggg')
#     if request.session.has_key('otp'):
        

#         print('fffffffff',request.session['otp'])
#         if request.method == "POST":   
#             var = request.POST.getlist("vehicle1")
#             commission_amount = 0.0
#             bill_amount = 0.0
#             gst_amount = 0.0
#             total = 0.0
         
#             for i in var:
#                 data = Collection_Agent.objects.get(Customer_bill_amount=i)
#                 commission_amount = commission_amount +float(data.commission_amount)
#                 bill_amount = bill_amount + float(data.Customer_bill_amount)
#                 gst_amount = gst_amount + float(data.Gst_ammount)/2
#                 print('***********',gst_amount)
                
              
#                 data.invoce=1
#                 data.save()
#             user = User_Registration_CA.objects.get(Otp=request.session['otp'])
#             invoice1 = invoice(invoice_user_reg=user,commission_amount=commission_amount,
#                                 bill_amount=bill_amount,gst_amount=gst_amount)
                                        
#             invoice1.save()
#             invoice12 = invoice.objects.latest('id')
#             transaction = Collection_Agent.objects.filter(invoce_no = invoice12.id)
#             for i in var:
#                 data = Collection_Agent.objects.get(Customer_bill_amount=i)
#                 data.invoce_no=invoice12.id
#                 data.save()
#             total = invoice12.commission_amount + invoice12.gst_amount + invoice12.gst_amount
#             return render(request,'CA/generate_mrc.html',{'data':invoice12,'total':round(total,2),'transaction':transaction,'user':user})

#     else:
#         return render(request,'CA/generate_mrc.html')


def all_commerical_pending(request):
   
    if request.session.has_key('otp'):
      
        if request.method == "POST":
           
            var = request.POST.getlist("vehicle1")
            c = 0
            r = 0
            p = 0
            for i in var:
               
                data = Collection_Agent.objects.get(Customer_bill_amount=i)
              
                data.invoce=1
                data.save()
                
                adding = Collection_Agent.objects.get(Customer_bill_amount=i)
                c1 = float(adding.commission_amount)
                r1 = float(adding.Gst_ammount)
                c = float(c + c1)
                
                r = r + r1
               

                f = float(adding.commission_amount)
                j = float(adding.Gst_ammount)
                q = f + j

              
                p = float(c+r+r)
               
                s = float(p/2)
                k = float(r/2)

              

                a = User_Registration_CA.objects.filter(Otp=request.session['otp'])
                
                
                # b = agent.Mobile
                abc = Collection_Agent.objects.filter(invoce=1)
                Contractor_id = adding.Contractor_id
                Customer_bill_amount = adding.Customer_bill_amount
                Customer_bill_amountByTwo = float(Customer_bill_amount) / 2
                
                commission_amount=adding.commission_amount
                
                # commission_amountByTwo = float(commission_amount) / 2
                commission_amountByTwo = float(c) / 2

               
                Gst_ammount=adding.Gst_ammount
                Gst_ammountByTwo = float(Gst_ammount) / 2
              
                

                Customer_bill_amountByTwo=float(Customer_bill_amountByTwo+p)
               
                

                new = invoice_data

            #return render(request,'CA/generate_mrc1.html',{'Contractor_id':Contractor_id,'Customer_bill_amount':Customer_bill_amount,'commission_amount':commission_amount,'Gst_ammount':Gst_ammount,'commission_amountByTwo':commission_amount,'Gst_ammountByTwo':Gst_ammountByTwo,'Customer_bill_amountByTwo':Customer_bill_amountByTwo,'s':s,'k':k})

       
        return render(request,'CA/generate_mrc1.html')
    else:
        return render(request,'CA/generate_mrc1.html')



def agents_details_ce_pending_save(request,id):
    
    if request.session.has_key('otp'):
   
        a = User_Registration_CA.objects.get(Otp=request.session['otp'])
        b = a.Mobile
   
        all_agent = Collection_Agent.objects.filter(Collection_agent_id=b,invoce=1)
   
        abc = request.session['var'] 
   
        if b == a.Mobile:
            all_agent.update(invoce=2)
            agent = User_Registration_CA.objects.filter(Otp=request.session['otp'])
            abc = Collection_Agent.objects.filter(Collection_agent_id=b,invoce=1)

            adding = Collection_Agent.objects.filter(Collection_agent_id=b,invoce=1)
            q = adding[0].commission_amount
            r = adding[0].Is_Gst
            p = q+r
            # s = adding[0].Gst_ammount
            # par = s/2
            
            return render(request,'CA/generate_mrc.html', {'data1':all_agent,'data':agent[0],'a':abc[0],'add':p})

        return render(request,'CA/agents_details_ce_pending_save.html', {'data1':all_agent})
    else:
        return render(request, 'CA/otp_verify.html')

    return render(request, 'CA/otp_verify.html')



def summary(request):
    a = User_Registration_CA.objects.filter(Otp=request.session['otp'])
    adding = Collection_Agent.objects.filter(invoce=1)
    # commission_amount = adding[0].commission_amount
    abc = Collection_Agent.objects.filter(invoce=3)
    for a in abc:
        i = a.invoce
        d = a.Gst_ammount

       
       
        invoce = float(a.invoce)
        commission_amount = float(a.commission_amount)
        

        t = float(invoce * commission_amount)
       
        Gst_ammount = float(a.Gst_ammount)
        g = float(invoce * Gst_ammount )
       
        total = float(t+g)
       
        h = float(Gst_ammount/2)
       
        new = float(g+t)
       
    return render(request,'CA/summary.html', {'new':new,'d':d,'data':a,'data1':adding,'commission_amount':commission_amount,'invoce':invoce,'t':t,'g':g,'total':total,'i':i,'h':h})                                


def agents_details_ce_approved(request):
    if request.session.has_key('otp'):
        paginate_by = 25
        model = Collection_Agent
        user_data= User_Registration_CA.objects.get(Otp=request.session['otp'])
        Contractorid= user_data.Contractor_Id
        all_agent = Collection_Agent.objects.filter(Contractor_id=Contractorid,invoce=1)

        #all_agent = Collection_Agent.objects.filter(Collection_agent_id=request.session['con'])
        paginator = Paginator(all_agent, 25) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number) 

        return render(request,'CA/agents_details_ce_approved.html', {'data1':page_obj,'user_data':user_data})

    return render(request, 'CA/otp_verify.html')



def transaction_viewdata(request):
    all_agent = User_Registration_CA.objects.filter(Is_Approved=1)
    return render(request,'CA/transaction_viewdata.html')



#--------------commericial agent------------------------------------------------------------------


def all_commercial(request):
   
    if request.session.has_key('otp'):

        all_agent = Collection_Agent.objects.filter(invoce=1)
        return render(request,'CA/all_commercial.html', {'data1':all_agent})

    return render(request, 'CA/otp_verify.html')




def all_commercial_save(request,id):
    
    if request.session.has_key('otp'):
        
        a = User_Registration_CA.objects.get(Otp=request.session['otp'])
        b = a.Mobile
      
        all_agent = Collection_Agent.objects.filter(Collection_agent_id=b,invoce=1)
        abc = request.session['var'] 
       
        if b == a.Mobile:   
            
            all_agent.update(invoce=2)
            agent = User_Registration_CA.objects.filter(Otp=request.session['otp'])
            abc = Collection_Agent.objects.filter(Collection_agent_id=b)
            adding = Collection_Agent.objects.filter(Collection_agent_id=b)
            q = adding[0].Customer_bill_amount
            r = adding[0].commission_amount
            p = q+r
            
            
            return render(request,'CA/generate_mrc1.html', {'data1':all_agent,'data':agent,'a':abc[0],'add':p})
            #return render(request,'CA/generate_mrc.html')

        return render(request,'CA/agents_details_ce_pending_save.html', {'data1':all_agent})
    else:
        return render(request, 'CA/otp_verify.html')

    return render(request, 'CA/otp_verify.html')





def Generate_deregister_invoice(request):
    if request.session.has_key('otp'):
        agent = User_Registration_CA.objects.get(Otp=request.session['otp'])
        data = User_Registration_CA.objects.filter(Payment_Status=3)
        ta = data.update(Payment_Status=0)
      
        m = agent.Mobile
        n = agent.Name

        

        return render(request, 'CA/Generate_deregister_invoice.html',{'m':m,'n':n,'a':agent})
    return redirect('/ca/fa_dergisterd')




#-------------------------------------------------niche ka shi h -------------------
# def all_commercial_save(request,id):
    
#     if request.session.has_key('otp'):
#         print('saveeeeeee')
      
#         a = Officer.objects.get(otp=request.session['otp'])
#         b = a.mobile
#         print('b',b)
#         all_agent = Collection_Agent.objects.filter(invoce=1)
        
#         abc = request.session['var'] 
#         print("ggggggggg",abc)
#         if b == a.mobile:
#             print('okkkkkkkkkkkkk')
#             all_agall_commercial_save
#             agent = User_Registration_CA.objects.filter(Otp=request.session['otp'])
#             abc = Collection_Agent.objects.filter(invoce=1)

#             adding = Collection_Agent.objects.filter(Collection_agent_id=b)
#             q = adding[0].commission_amount
#             r = adding[0].Is_Gst
#             p = q+r
            
#             return render(request,'CA/generate_mrc.html', {'data1':all_agent,'data':agent[0],'a':abc[0],'add':p})

#         return render(request,'CA/all_commercial_save.html', {'data1':all_agent})
#     else:
#         return render(request, 'CA/otp_verify.html')

#     return render(request, 'CA/otp_verify.html')

# def all_commercial_save(request,id):
    
#     if request.session.has_key('otp'):
#         print('saveeeeeee')
      
#         a = User_Registration_CA.objects.get(Otp=request.session['otp'])
#         b = a.Mobile
#         print('b',b)
#         all_agent = Collection_Agent.objects.filter(Collection_agent_id=b,invoce=1)
        
#         abc = request.session['var'] 
#         print("ggggggggg",abc)
#         if b == a.Mobile:
#             print('okkkkkkkkkkkkk')
#             all_agent.update(invoce=2)
#             agent = User_Registration_CA.objects.filter(Otp=request.session['otp'])
#             abc = Collection_Agent.objects.filter(Collection_agent_id=b)
#             adding = Collection_Agent.objects.filter(Collection_agent_id=b)
#             q = adding[0].commission_amount
#             r = adding[0].Is_Gst
#             p = q+r
            
#             return render(request,'CA/generate_mrc.html', {'data1':all_agent,'data':agent[0],'a':abc[0],'add':p})

#         return render(request,'CA/all_commercial_save.html', {'data1':all_agent})
#     else:
#         return render(request, 'CA/otp_verify.html')

#     return render(request, 'CA/otp_verify.html')



def pcv_generate(request):
    if request.session.has_key('otp'):
        abc = User_Registration_CA.objects.get(Otp=request.session['otp'])
        b = abc.Mobile

        all_agent = Collection_Agent.objects.filter(Collection_agent_id=b)

  
        return render(request,'CA/pcv_generate1.html',{'data1':all_agent,'data':abc})

    return render(request, 'CA/otp_verify.html')

      
#--------------finance agent------------------------------------------------------------------


def finance_details(request):
    agent = User_Registration_CA.objects.all()
    return render(request,'CA/finance_details.html',{'data1':agent})


def finance_details_fi(request):
    all_agent = Collection_Agent.objects.filter(invoce='2')

    # all_agent = Collection_Agent.objects.filter(invoce=1)
    return render(request,'CA/finance_details_fi.html',{'data1':all_agent})


def finance_details_save(request,id):
    
    if request.session.has_key('otp'):
      
        a = User_Registration_CA.objects.get(Otp=request.session['otp'])
        b = a.Mobile
        all_agent = Collection_Agent.objects.filter(invoce=2)
        # abc = request.session['var'] 
        # print("ggggggggg",abc)
        if b == a.Mobile:
            all_agent.update(invoce=3)
            agent = User_Registration_CA.objects.filter(Otp=request.session['otp'])
            abc = Collection_Agent.objects.filter(Collection_agent_id=b)
            adding = Collection_Agent.objects.filter(Collection_agent_id=b)
            g = adding[0].Gst_ammount
            q = adding[0].commission_amount
            r = adding[0].Is_Gst
            z = adding[0].Customer_bill_amount
            p = q+g 


            Customer_bill_amount = adding[0].Customer_bill_amount
            Customer_bill_amountByTwo = float(z) / 2
            
            commission_amount=adding[0].commission_amount
          
            # commission_amountByTwo = float(commission_amount) / 2
            commission_amountByTwo = float(q) / 2


            Gst_ammount=adding[0].Gst_ammount
            Gst_ammountByTwo = float(g) / 2

            # Customer_bill_amountByTwo=float(Customer_bill_amountByTwo+z)
            # print('Customer_bill_amountByTwoCustomer_bill_amountByTwo',Customer_bill_amountByTwo)

           
            
            return render(request,'CA/generate_mrc2.html', {'z':z,'q':q,'g':g,'data1':all_agent,'data':agent[0],'a':abc[0],'add':p})

        return render(request,'CA/finance_pending_save.html', {'data1':all_agent})
    else:
        return render(request, 'CA/otp_verify.html')
            


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




import payu_sdk
from paywix.payu import Payu
import uuid

def payment(request):
    if request.session.has_key('xyz'):
        
        a = User_Registration_CA.objects.get(Mobile=request.session['oid'])
        b = a.Mobile
        n = a.Name
        e = a.Email_Id
        txind = uuid.uuid1()
        client = payu_sdk.payUClient(credes={"key":"GHeH7D","salt":"DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
        param = {"txnid":txind,"amount":"1000.00","productinfo":"Portal Fees","firstname":n,"email":e}
        apiHash = payu_sdk.Hasher.generate_hash(param)
        data3 = Payudata_main1(user = a.Contractor_Id,Payu_Status='pending', Txdid=txind,
            Productinfo="Portal Fees",
            Firstname=a.Name, Contact_No=a.Mobile, Email_Id=a.Email_Id,
            Netamount_Debited='1000.00')
        data3.save()

        return render(request, 'CA/payment.html',{"posted":apiHash,"txnid":txind,"b":b,"n":n,"e":e})
    else:
        return redirect('/ca/login')



# 4012 0010 3714 1112
@csrf_exempt
def payu_success_registration(request):
    # return render(request, 'CA/sucess_pay_registration.html')

    data = {k: v[0] for k, v in dict(request.POST).items()}
    #response = payment.verify_transaction(data)
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
    request.session['Phone_no'] = Phone_no
    print('this is phone number ',request.session['Phone_no'])
    if Pgateway_Type == 'NB-PG':
        if Payudata_main1.objects.filter(Txdid=Txn_id).exists():
            Payudata = Payudata_main1.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            Payudata.Name_On_Card =  'Not Available'
            Payudata.Cardnum =  'Not Available'
            Payudata.Payu_Status=Status
            Payudata.save()
    else:
        if Payudata_main1.objects.filter(Txdid=Txn_id).exists():
            # Nameon_card = data['name_on_card']
            #Card_num = data['cardnum']
            Payudata = Payudata_main1.objects.get(Txdid=Txn_id)
            Payudata.Payu_Moneyid = payu_moneyid
            Payudata.Hash_Id = Hash
            Payudata.Paymentgateway_Type = Pgateway_Type
            # Payudata.date = date
            Payudata.Bank_Ref_Num = Bankrefnum
            Payudata.Bankcode = Bank_code
            # Payudata.Name_On_Card = Nameon_card
            #Payudata.Cardnum = Card_num
            Payudata.Payu_Status=Status
            Payudata.save()
   

    list1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    RegNum = "CZ2022"
    s = ""
    s = s + "V" + RegNum + random.choice(list1) + random.choice(list1) + random.choice(list1) + random.choice(list1)
    # model = user_registration_ca.objects.filter(mobile=phone_no)
    # model.update(payment_status=1)
    # model.update(RegistractionNumber=s)
    Regdatashow = User_Registration_CA.objects.filter(Mobile=Phone_no)
    # date = datetime.now()
    user = User_Registration_CA.objects.get(Mobile=Phone_no)
    client = payu_sdk.payUClient(credes={"key": "GHeH7D", "salt": "DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ"})
    key = 'GHeH7D'
    salt = 'DB2Y4tlzdBqPjFBiES3r5pf4c6JPQCtJ'
    command = 'verify_payment'
    toHash = {"command": command, "var1": Txn_id}
    apiHash = payu_sdk.Hasher.APIHash(toHash)
    Poststring = "key=" + key + "&command=" + command + "&hash=" + apiHash + "&var1=" + Txn_id;
    #url = 'https://test.payu.in/merchant/postservice.php?form=2'
    proxyDictfd={"https":"proxy.mpcz.in:8080","http":"proxy.mpcz.in:8080"}
    # response = requests.get(url,proxies=proxyDictfd)
    #r = requests.post(url, data=Poststring)
    url = "https://info.payu.in/merchant/postservice?form=2"
    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    payload = "key=" + key + "&command=verify_payment&var1=" + Txn_id + "&hash=" + apiHash
    #res = requests.request("POST", url,proxies=proxyDictfd, data=payload, headers=headers)
    res = requests.request("POST",url,data=payload, headers=headers)
    user = User_Registration_CA.objects.get(Mobile=Phone_no)
    user.Payment_Status=1
    user.Security_Deposit = 1000
    user.Is_Enable=1
    user.save()
    RegNum = "CZ2022"
    if user.Gst:
        gst_no = user.Gst
    else:
        gst_no = "null"
    URL =  "https://resources.mpcz.in:8888/NscAgr/api/user/registerUser"
    api_data={"collectionAgentId":user.Contractor_Id,
    "collectionAgentIdEnc":"12s34SD",
    "collectionAgentName":user.Name,
    "gender":"null",
    "mobileNo": user.Mobile,
    "emailId": user.Email_Id,
    "address": user.Add1,
    "city": user.City,
    "pin": user.Pincode,
    "State": user.State,
    "panNo": user.Pan,
    "panFilePath":" ",
    "bankName": user.Bank_name,
    "ifscCode": user.IFSC,
    "accountHolderName": user.Account_Holder_Name,
    "accountNo": user.Account_Number,
    "consumerName":"xyz-user",
    "tarrifCode":"LV1.2",
    "dcCode":"2294317",
    "ivrsAddress":"OLD ITARSI,ITARSI S C NO 3117",
    "aadharNo":user.Aadhar,
    "ivrsNo":"N2435654",
    "dobStr":"23-11-1997",
    "contractorId":user.Contractor_Id,
    "gstNumber":gst_no,
    "gstNumberConfirmation":gst_no
    }
    json_data = json.dumps(api_data)
    headers = {'content-type':'application/json'}
    res_api = req.request('POST',url=URL,data=json_data,headers=headers,verify=False)
    

    if res.status_code == 200:
        json_data = json.loads(res.text)
        if json_data['status'] == 1:
            transcation_details = json_data['transaction_details']
            transction_data = transcation_details[Txn_id]
            if transction_data['status'] == 'success':
                payu_obj = Payudata_main1.objects.filter(Txdid=Txn_id)
                if transction_data['productinfo'] == "Registration":

                    return render(request, 'CA/sucess_pay_registration.html',
                                  {'response': response, 'data': payu_obj})
           
                request.session['Phone_no'] = Phone_no
                return render(request, 'CA/sucess_pay_registration.html', {'data': payu_obj,'Regdatashow':Regdatashow,})
    else:
        attempt_num += 1
        time.sleep(5)  # Wait for 5 seconds before re-trying

    request.session['Phone_no'] = Phone_no
    print('this is session',request.session['Phone_no'])
    return render(request, 'CA/sucess_pay_registration.html', {'response': response, 'data': payu_obj,'Regdatashow':Regdatashow,})


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
    # Nameon_card = data['name_on_card']
    Card_num = data['cardnum']
    payu_moneyid = data['mihpayid']
    Netamount = data['net_amount_debit']
    # date = datetime.now()
    if Payudata_main1.objects.filter(Txdid=Txn_id).exists():
        Payudata = Payudata_main1.objects.get(Txdid=Txn_id)
        Payudata.Payu_Moneyid = payu_moneyid
        Payudata.Hash_Id = Hash
        Payudata.Paymentgateway_Type = Pgateway_Type
        # Payudata.date = date
        Payudata.Bank_Ref_Num = Bankrefnum
        Payudata.Bankcode = Bank_code
        # Payudata.Name_On_Card = Nameon_card
        Payudata.Cardnum = Card_num
        Payudata.Payu_Status = 'Failure'
        Payudata.save()
    payu_obj = Payudata_main1.objects.get(Txdid=Txn_id)
    # user = AllData.objects.get(MobileNumber=Phone_no)
    # user.save()
    
    return render(request, 'CA/payment_fail.html')

def payment_invoice(request):
    data=User_Registration_CA.objects.get(Mobile=request.session['Phone_no'])
    created_date = datetime.datetime.now()
    return render(request,'CA/payment_invoice_page.html',{'data':data,'created_date':created_date})



def ca_deregistered(request):
    if request.session.has_key('otp'):
        otpdata=request.session['otp']
        user_data = User_Registration_CA.objects.get(Otp=otpdata)
        return render(request, 'CA/deregistered.html', {'user_data':user_data})


def ca_deregistered_request(request):
    if request.session.has_key('otp'):
        otpdata=request.session['otp']
        user_data = User_Registration_CA.objects.get(Otp=otpdata)
        ContractorId = user_data.Contractor_Id
        data_exist = CA_Deregistration.objects.filter(agent_id = user_data.User_Id,is_deregister = True)
        if data_exist:
            return render(request, 'CA/deregistered_exist.html', {'user_data':user_data})

        pending_invoice = Collection_Agent.objects.filter(Contractor_id = ContractorId)
        if pending_invoice:
            for i in pending_invoice:
                if i.invoce == 0:
                    return render(request, 'CA/pending_invoice_exist.html', {'user_data':user_data})
        
        s = random.randint(100,10000)
        invoice_data = CA_Deregistration(agent_id_id = user_data.User_Id ,Contractor_Id = ContractorId,Invoice_Number = s, Deposit_amount = user_data.Security_Deposit, Email_Id = user_data.Email_Id,
        Mobile = user_data.Mobile ,Bank_name = user_data.Bank_name,Account_Holder_Name = user_data.Account_Holder_Name,  Account_Number =user_data.Account_Number,
        IFSC = user_data.IFSC,Name = user_data.Name, Father_name = user_data.Father_name, Aadhar = user_data.Aadhar, Pan = user_data.Pan, Add1 =  user_data.Add1,
        Add2 = user_data.Add2, State = user_data.State, Pincode = user_data.Pincode, City = user_data.City, District = user_data.District, gst_no = user_data.Gst,is_deregister = True )
        invoice_data.save()
        user_data.Security_Deposit = 0
        user_data.Is_Enable = False
        user_data.save()
        return render(request, 'CA/deregistered_success.html')


def ca_report(request):
    return render(request, 'CA/reports.html')


def deregistration_requests(request):
    deregister_Invoice = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = False, is_deregister = True)
    return render(request, 'CA/deregistration_requests.html', {'data1':deregister_Invoice})


def view_deregistered_data(request,id):
    deregister_Invoice_data = CA_Deregistration.objects.get(id=id)
    return render(request, 'CA/deregister_data_view.html', {'data1':deregister_Invoice_data})


def ca_deregister_rq_approve(request):
    if request.method=="POST":
        id_list = request.POST.getlist('checkbox')
        request.session['id_list']=id_list
        otpca = generateOTP()
        data = Officer.objects.get(employ_login_id='commercial')
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(data.mobile) + "&v1=" + str(otpca) + "&v2=" + str()
        response = requests.get(url, proxies=proxyDict,headers={'User-Agent': 'Chrome'})
        sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = data.mobile)
        sms_template.save()
        
        request.session['otpca']= otpca
    return render(request,'CA/deregister_cash_voucher_otp_verify.html',{'otpca':request.session['otpca']})


def deregistration_cash_voucher(request):
    if request.session.has_key('otp'):
        if request.method=="POST":
            otp_data = request.POST.get('otp')
            today = datetime.datetime.now()
            
            if otp_data==request.session['otpca']:
                val = request.session['id_list']

                for v_id in val:
                    Reference_No=""
                    digits = "0123456789"
                    Reference_No = random.randint(1000000,999999999)
                    deregister_Invoice_Data = CA_Deregistration.objects.filter(id=v_id,Commercial_Flag=1)
                    dereg_count_row = CA_Deregistration.objects.all()
                    a = dereg_count_row.count()
                    voucher_no = "RFB"+ str(1000+a)
                    if deregister_Invoice_Data:
                        deregister_Invoice_Data.update(Finance_Flag = True,Reference_No = Reference_No,voucher_code = voucher_no, updated_date = datetime.datetime.now())
                    updated_data  = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = False ,is_security_refund = False)
                return render(request, 'CA/deregister_request_submit.html',{"success_msg": "receipt generated successfully", 'data1':updated_data})

            else:
                return render(request,'CA/deregister_cash_voucher_otp_verify.html',{"msg": "Invalid OTP"})

        
def deregistration_receipt(request):
    deregister_receipt = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = True,is_security_refund = False)
    return render(request, 'CA/deregister_receipt.html', {'data1':deregister_receipt})


def deregister_cash_voucher_list(request):
    deregister_voucher = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = True, is_security_refund = False)
    return render(request,'CA/deregister_cash_voucher_list.html',{'Cash_Voucher':deregister_voucher})



def deregister_cash_Voucher(request,id):
    deregister_cash_Voucher=CA_Deregistration.objects.get(id=id)

    return render(request,'CA/deregister_cash_voucher.html',{'Cash_Voucher':deregister_cash_Voucher})

    
def finance_cash_voucher_list(request):
    deregister_voucher = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = True, is_security_refund = False,is_deregister = True)
    return render(request,'CA/finance_deregister_voucher_list.html',{'Cash_Voucher':deregister_voucher})



def finance_deregister_cash_Voucher(request,id):
    deregister_cash_Voucher=CA_Deregistration.objects.get(id=id)

    return render(request,'CA/finance_deregister_voucher.html',{'Cash_Voucher':deregister_cash_Voucher})



def ca_security_refund(request):
    if request.session.has_key('otp'):
        otpdata=request.session['otp']
        user_data = User_Registration_CA.objects.get(Otp=otpdata)
        amnt = user_data.Security_Deposit
        if amnt == 0:
            user_data.Security_Deposit = 0
        else:
            user_data.Security_Deposit = amnt-1000
        return render(request, 'CA/security_refund.html', {'user_data':user_data})


def ca_security_refund_req(request):
    if request.session.has_key('otp'):
        otpdata=request.session['otp']
        user_data = User_Registration_CA.objects.get(Otp=otpdata)
        ContractorId = user_data.Contractor_Id
        deregister_data_exist = CA_Deregistration.objects.filter(agent_id = user_data.User_Id, is_deregister = True)
        if user_data.Security_Deposit == 0:
            return render(request, 'CA/security_refund_exist.html', {'user_data':user_data,"message2": "Your SD amount is 0, can't request for security refund or deregistreation !!"})
        if deregister_data_exist:
            return render(request, 'CA/security_refund_exist.html', {'user_data':user_data,"message1": "You have already requested for deregistration !!"})
        data_exist = CA_Deregistration.objects.filter(agent_id = user_data.User_Id, is_security_refund = True)
        if data_exist:
            return render(request, 'CA/security_refund_exist.html', {'user_data':user_data,"message2": "You have already requested for Security Refund !!"})
        s = random.randint(100,10000)
        amnt = user_data.Security_Deposit
        if amnt == 0:
            user_data.Security_Deposit = 0
        else:
            user_data.Security_Deposit = amnt-1000
        invoice_data = CA_Deregistration(agent_id_id = user_data.User_Id ,Contractor_Id = ContractorId,Invoice_Number = s, Deposit_amount = user_data.Security_Deposit, Email_Id = user_data.Email_Id,
        Mobile = user_data.Mobile ,Bank_name = user_data.Bank_name,Account_Holder_Name = user_data.Account_Holder_Name,  Account_Number =user_data.Account_Number,
        IFSC = user_data.IFSC,Name = user_data.Name, Father_name = user_data.Father_name, Aadhar = user_data.Aadhar, Pan = user_data.Pan, Add1 =  user_data.Add1,
        Add2 = user_data.Add2, State = user_data.State, Pincode = user_data.Pincode, City = user_data.City, District = user_data.District, gst_no = user_data.Gst, is_security_refund = True,Commercial_Flag = True )
        invoice_data.save()
        user_data.Security_Deposit = 1000
        user_data.save()
        return render(request, 'CA/security_refund_success.html')




def security_refund_requests(request):
    deregister_Invoice = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = False, is_security_refund = True)
    return render(request, 'CA/security_refund_requests.html', {'data1':deregister_Invoice})

def view_security_refund_data(request,data_id):
    deregister_Invoice_data = CA_Deregistration.objects.get(id=data_id)
    return render(request, 'CA/security_refund_data_view.html', {'data1':deregister_Invoice_data})


def ca_security_refund_rq_approve(request):
    if request.method=="POST":
        id_list = request.POST.getlist('checkbox')
        request.session['id_list']=id_list
        otpca = generateOTP()
        data = Officer.objects.get(employ_login_id='commercial')
        header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
        proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" +str(data.mobile) + "&v1=" + str(otpca) + "&v2=" + str()
        response = requests.get(url,proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = data.mobile)
        sms_template.save()
        
        request.session['otpca']= otpca
    return render(request,'CA/security_refund_otp_verify.html',{'otpca':request.session['otpca']})


def security_refund_cash_voucher(request):
    if request.session.has_key('otp'):
        if request.method=="POST":
            otp_data = request.POST.get('otp')
            today = datetime.datetime.now()
            
            if otp_data==request.session['otpca']:
                val = request.session['id_list']

                for v_id in val:
                    Reference_No=""
                    digits = "0123456789"
                    Reference_No = random.randint(1000000,999999999)
                    deregister_Invoice_Data = CA_Deregistration.objects.filter(id=v_id,Commercial_Flag=1,is_security_refund = True)
                    dereg_count_row = CA_Deregistration.objects.all()
                    a = dereg_count_row.count()
                    voucher_no = "RFB"+ str(1000+a)
                    if deregister_Invoice_Data:
                        deregister_Invoice_Data.update(Finance_Flag = True,Reference_No = Reference_No,voucher_code = voucher_no, updated_date = datetime.datetime.now())
                    updated_data  = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = False,is_security_refund = True )
                return render(request, 'CA/security_refund_requests.html',{"success_msg": "receipt for security refund generated successfully", 'data1':updated_data})

            else:
                return render(request,'CA/security_refund_otp_verify.html',{"msg": "Invalid OTP"})

        
def security_refund_receipt(request):
    sd_receipt = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = True, is_security_refund = True)
    return render(request, 'CA/security_refund_receipt_list.html', {'data1':sd_receipt})


def security_refund_cash_Voucher(request,id):
    deregister_cash_Voucher=CA_Deregistration.objects.get(id=id)

    return render(request,'CA/security_refund_cash_voucher.html',{'Cash_Voucher':deregister_cash_Voucher})

    
def security_refund_cash_voucher_list(request):
    deregister_voucher = CA_Deregistration.objects.filter(Commercial_Flag=True,Finance_Flag = True, is_security_refund = True)
    return render(request,'CA/finance_security_refund_list.html',{'Cash_Voucher':deregister_voucher})


def finance_security_refund_cash_Voucher(request,id):
    deregister_cash_Voucher=CA_Deregistration.objects.get(id=id)

    return render(request,'CA/finance_security_refund_voucher.html',{'Cash_Voucher':deregister_cash_Voucher})

from django.db import connection


def ca_txn_report(request):
    query = '''select
    "Contractor_id" "AGENT_ID",
    "Name" "COLL_AGENT_NAME", 
    TO_CHAR(to_date("Month",'YYYY-MM'),'MON-YY') "BILL_MON", 
    COUNT(*) AS "TRANS_COUNT",
    SUM(CAST(commission_amount AS INTEGER)) AS "TOT_COMMISION",
    sum(CASE WHEN "invoce"=1 then 1 else 0 end) "INVOICE_GENERATED"
    FROM public."CA_collection_agent"  
    WHERE "Is_commission" ='Yes'
    GROUP BY 
    "Name", 
    "Contractor_id", 
    "Month"'''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/ca_txn_report_data.html',{'data':row})
    

from CA.forms import CABankImageForm
from CA.models import CA_Bank_Update_Req  
  
def ca_bank_update(request): 
    otpdata=request.session['otp']
    user_data = User_Registration_CA.objects.get(Otp=otpdata)
    bank_req_reject =  CA_Bank_Update_Req.objects.filter(agent_id_id = user_data.User_Id, is_rejected = True) 
    if len(bank_req_reject)>0:
        bank_req =  CA_Bank_Update_Req.objects.get(agent_id_id = user_data.User_Id, is_rejected = True)
        if bank_req:
            if bank_req.reject_remark == None:
                pass
            else:
                msg = f"Your Previously bank update request is rejected by commercial section !!.  " + "Reason :- "+ bank_req.reject_remark
                return render(request, 'CA/data.html', {'msg1': msg})
    if request.method == 'POST':
        data_present = CA_Bank_Update_Req.objects.all()
        if data_present:
            exist_data = CA_Bank_Update_Req.objects.filter(agent_id_id = user_data.User_Id)
            if len(exist_data)>0:
                if exist_data:
                    return render(request, 'CA/data.html', {'msg1':"You have already requested for bank details update !!"})
        form = CABankImageForm(request.POST, request.FILES)  
        if form.is_valid():
            bank_name = form.cleaned_data.get('bank_name')
            account_Holder_Name = form.cleaned_data.get('account_Holder_Name')
            account_Number = form.cleaned_data.get('account_Number')
            ifsc = form.cleaned_data.get('ifsc')
            passbook_image = form.cleaned_data.get('passbook_image')

            bank_data = CA_Bank_Update_Req(agent_id_id =user_data.User_Id, bank_name=bank_name,  account_Holder_Name=account_Holder_Name,account_Number=account_Number,
            ifsc = ifsc,passbook_image = passbook_image,is_new_details = True,contractor_id = user_data.Contractor_Id,agent_name = user_data.Name)
            bank_data.save()
              
            return render(request, 'CA/data.html', {'msg1':"We have received your request for bank details update !!"})  
    else:  
        form = CABankImageForm()  
  
    return render(request, 'CA/bank_update_form.html', {'form': form})  


def bank_change_requests(request):
    bank_change_data = CA_Bank_Update_Req.objects.filter(is_new_details = True)
    return render(request, 'CA/commercial_bank_change_data.html', {'data1': bank_change_data})

def view_bank_passbook_data(request,id,agent_id):
    new_bank_data = CA_Bank_Update_Req.objects.get(id = id)
    old_bank_data = User_Registration_CA.objects.get(User_Id=agent_id)

    return render(request, 'CA/bank_data_view.html', {'old_bank_data': old_bank_data, 'new_bank_data': new_bank_data})

    
def ca_bank_approved(request,agent_id,new_data_id):
    bank_old_data = User_Registration_CA.objects.get(User_Id=agent_id)
    bank_new_data = CA_Bank_Update_Req.objects.get(id = new_data_id)
    officer_data = Officer.objects.get(employ_login_id = 'commercial')

    bank_old_history_save = CA_Bank_Update_Req(agent_id_id =agent_id, bank_name=bank_old_data.Bank_name,  account_Holder_Name=bank_old_data.Account_Holder_Name,account_Number=bank_old_data.Account_Number,
        ifsc = bank_old_data.IFSC,is_new_details = False,approved_person_id = 'commercial',approved_by =officer_data.mobile )
    bank_old_history_save.save()

    bank_new_data.is_approved = True
    bank_new_data.save()

    bank_old_data.Account_Holder_Name = bank_new_data.account_Holder_Name
    bank_old_data.Account_Number = bank_new_data.account_Number
    bank_old_data.Bank_name = bank_new_data.bank_name
    bank_old_data.IFSC = bank_new_data.ifsc
    bank_old_data.save()

    updated_bank_change_data = CA_Bank_Update_Req.objects.all()
    return render(request, 'CA/commercial_bank_change_data.html', {'data1': updated_bank_change_data, 'message':"Bank details approved"})  


def ca_bank_reject(request,agent_id,new_data_id):
    updated_bank_change_data = CA_Bank_Update_Req.objects.all()
    bank_new_data = CA_Bank_Update_Req.objects.get(id = new_data_id)
    remark = request.POST.get('reject_remark')
    bank_new_data.is_rejected = True
    bank_new_data.reject_remark = remark
    bank_new_data.save()
    return render(request, 'CA/commercial_bank_change_data.html', {'data1': updated_bank_change_data, 'message':"Bank details rejected"})  
    
    
    
def all_ca_list(request):
    query = '''select *
    FROM public."CA_user_registration_ca"  
    WHERE "Is_Enable" =True and "Payment_Status" = 1'''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/ca_all_agent_list.html',{'data':row})


def ca_total_deregister(request):
    query = '''select *
    FROM public."CA_ca_deregistration"  
    WHERE "is_deregister" =True '''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/ca_all_deregistered_list.html',{'data':row})


def ca_total_security_refund(request):
    query = '''select *
    FROM public."CA_ca_deregistration"  
    WHERE "is_security_refund" =True '''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/ca_all_SD_list.html',{'data':row})

def bank_change_requests_IT(request):
    bank_change_data = CA_Bank_Update_Req.objects.filter(is_new_details = True,is_approved = False)
    return render(request, 'CA/IT_bank_change_data.html', {'data1': bank_change_data})


def view_bank_passbook_data_IT(request,id,agent_id):
    new_bank_data = CA_Bank_Update_Req.objects.get(id = id)
    old_bank_data = User_Registration_CA.objects.get(User_Id=agent_id)

    return render(request, 'CA/IT_bank_data_view.html', {'old_bank_data': old_bank_data, 'new_bank_data': new_bank_data})


def commercial_ca_reports(request):
    return render(request, 'CA/commercial_reports.html')

def commercial_ca_txn_report(request):
    query = '''select
    "Contractor_id" "AGENT_ID",
    "Name" "COLL_AGENT_NAME", 
    TO_CHAR(to_date("Month",'YYYY-MM'),'MON-YY') "BILL_MON", 
    COUNT(*) AS "TRANS_COUNT",
    SUM(CAST(commission_amount AS INTEGER)) AS "TOT_COMMISION",
    sum(CASE WHEN "invoce"=1 then 1 else 0 end) "INVOICE_GENERATED"
    FROM public."CA_collection_agent"  
    WHERE "Is_commission" ='Yes'
    GROUP BY 
    "Name", 
    "Contractor_id", 
    "Month"'''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/commercial_ca_txn_report_data.html',{'data':row})


def commercial_all_ca_list(request):
    query = '''select *
    FROM public."CA_user_registration_ca"  
    WHERE "Is_Enable" =True and "Payment_Status" = 1'''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/commercial_ca_all_agent_list.html',{'data':row})


def commercial_ca_total_deregister(request):
    query = '''select *
    FROM public."CA_ca_deregistration"  
    WHERE "is_deregister" =True '''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/commercial_ca_all_deregistered_list.html',{'data':row})


def commercial_ca_total_security_refund(request):
    query = '''select *
    FROM public."CA_ca_deregistration"  
    WHERE "is_security_refund" =True '''
    cursor = connection.cursor()
    cursor.execute(query)
    row = cursor.fetchall()
    return render(request,'CA/commercial_ca_all_SD_list.html',{'data':row})

def commercial_bank_change_requests_IT(request):
    bank_change_data = CA_Bank_Update_Req.objects.filter(is_new_details = True,is_approved = False)
    return render(request, 'CA/commercial_IT_bank_change_data.html', {'data1': bank_change_data})


def commercial_view_bank_passbook_data_IT(request,id,agent_id):
    new_bank_data = CA_Bank_Update_Req.objects.get(id = id)
    old_bank_data = User_Registration_CA.objects.get(User_Id=agent_id)

    return render(request, 'CA/commercial_IT_bank_data_view.html', {'old_bank_data': old_bank_data, 'new_bank_data': new_bank_data})


def detail_by_pincode(request,pincode_number):    
    all_record = Pin_Code_Table_Master.objects.filter(Pincode_number=pincode_number).values()    
    data=list(all_record)
    print(data,"Pincode1111")
    return JsonResponse({"data": data})    
