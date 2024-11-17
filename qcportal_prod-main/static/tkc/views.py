from django.views.decorators.csrf import csrf_exempt
from paywix.payu import Payu
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import *
from tkc.models import *
from tkc.serializer import BalanceSheet_Serializer, TKC_Document_Serializer, TKC_Turnover_Serializer
from datetime import datetime
import datetime
from django.contrib import messages
import json
from django.conf import settings
from django.core.mail import send_mail

import requests


# Create your views here.

def basic(request):
    data = User_Registration.objects.get(Otp=request.session['otp'])
    return render(request, 'tkc/basicinfo.html', {"userdata": data})


def tkc_view_profile(request):
    if request.session.has_key('otp'):
        data11 = User_Registration.objects.filter(Otp=request.session['otp'])
        data = User_Registration.objects.get(Otp=request.session['otp'])
        user_id = data.User_Id
        vendor_document = TKC_Document.objects.filter(user_id=user_id)
        vendor_balance = TKC_Turnover.objects.filter(user_id=user_id)
        abcde = UserCompanyDataMain.objects.get(user_id=data.ContactNo)
        return render(request, 'tkc/tkc_view_profile.html',
                      {"basic": data, 'company': abcde, 'vendor_document': vendor_document,
                       'vendor_balance': vendor_balance})


def update_profile(request):
    data = User_Registration.objects.get(Otp=request.session['otp'])
    userid = data.User_Id
    abcde = UserCompanyDataMain.objects.get(user_id=data.ContactNo)
    if data.profile_update_fee == 1 or data.cgm_approval == 0:
        if request.method == "POST":
            data11 = User_Registration.objects.filter(
                Otp=request.session['otp'])
            abc = UserCompanyDataMain.objects.get(user_id=data.ContactNo)
            data1 = User_Registration.objects.get(Otp=request.session['otp'])
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
            return redirect('complete')
    else:
        return HttpResponse("You have to pay profile update fee")
    return render(request, 'tkc/update_vendor_profile.html', {"basic": data, 'company': abcde})


def tkc_reg_seven(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'])
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

        return render(request, 'tkc/tkc_reg7.html')
    return render(request, 'tkc/tkc_reg7.html')


def tkc_reg_eight(request):
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'])
        data.Experience = request.POST.get('work_experience')
        data.Turnover = request.POST.get('turn_over')
        data.Oyt = request.POST.get('VendorType')
        data.save()
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            data1.page_8 = 1
            data1.save()
        else:
            user = User_Registration_Check_Status(User=data, page_8=1)
            user.save()
        return redirect("tkc_reg_nine")
    payment = TKC_Payment.objects.all()
    return render(request, 'tkc/tkc_reg8.html', {'payment': payment})


def tkc_reg_nine(request):
    if request.method == "POST":
        data = User_Registration.objects.get(Otp=request.session['otp'])
        user_id = data.User_Id
        financial_year = request.POST.get('v_balance_sheet_1')
        if financial_year:
            Amount = request.POST.get('Amount')
            data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                 Status=1)
            data1.save()
        financial_year = request.POST.get('v_balance_sheet_2')
        if financial_year:
            Amount = request.POST.get('Amount2')
            data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                 Status=1)
            data1.save()
        financial_year = request.POST.get('v_balance_sheet_3')
        if financial_year:
            Amount = request.POST.get('Amount3')
            data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                 Status=1, complete_data=1)
            data1.save()
        financial_year = request.POST.get('v_balance_sheet_4')
        if financial_year:
            Amount = request.POST.get('Amount4')
            data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                 Status=2)
            data1.save()
        financial_year = request.POST.get('v_balance_sheet_5')
        if financial_year:
            Amount = request.POST.get('Amount5')
            data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                 Status=2)
            data1.save()
        financial_year = request.POST.get('v_balance_sheet_6')
        if financial_year:
            Amount = request.POST.get('Amount6')
            data1 = TKC_Turnover(user_id=user_id, Financial_year=financial_year, Amount=Amount,
                                 Status=2, complete_data=1)
            data1.save()
        if User_Registration_Check_Status.objects.filter(User=data).exists():
            data1 = User_Registration_Check_Status.objects.get(User=data)
            data1.page_9 = 1
            data1.save()
        else:
            user = User_Registration_Check_Status(User=data, page_9=1)
            user.save()
        return redirect("tkc_reg_ten")
    return render(request, 'tkc/tkc_reg9.html')


def tkc_reg_ten(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'])
        user_id = data.User_Id
        if request.method == "POST":
            data = User_Registration.objects.get(Otp=request.session['otp'])
            user_id = data.User_Id
            office_name = request.POST.get('one')
            aadhar_card_no = request.POST.get('two')
            issu_date = request.POST.get('three')
            document = request.FILES['four']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='AADHAR CARD DETAILS', Issued_office_Name=office_name,
                                 Document_Number=aadhar_card_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Approval_doc=2)
            data1.save()

            office_name = request.POST.get('five')
            gst_card_no = request.POST.get('six')
            issu_date = request.POST.get('seven')
            ex_date = request.POST.get('eight')
            document = request.FILES['nine']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='GST WITH CHALLAN', Issued_office_Name=office_name,
                                 Document_Number=gst_card_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=2)
            data1.save()

            office_name = request.POST.get('ten')
            document_no = request.POST.get('eleven')
            issu_date = request.POST.get('twelve')
            ex_date = request.POST.get('thirteen')
            document = request.FILES['fourteen']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='ITR OF LAST THREE YEAR',
                                 Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=2)
            data1.save()

            office_name = request.POST.get('fifteen')
            document_no = request.POST.get('sixteen')
            issu_date = request.POST.get('seventeen')
            ex_date = request.POST.get('eighteen')
            document = request.FILES['nineteen']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='DETAIL OF CONTRACTOR & SUPERVISOR',
                                 Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=1)
            data1.save()

            office_name = request.POST.get('twentee')
            document_no = request.POST.get('twentee_one')
            issu_date = request.POST.get('twentee_two')
            ex_date = request.POST.get('twentee_three')
            document = request.FILES['twentee_four']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='ELECTRICAL LICENSE',
                                 Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=1)
            data1.save()

            office_name = request.POST.get('twentee_five')
            document_no = request.POST.get('twentee_six')
            issu_date = request.POST.get('twentee_seven')
            ex_date = request.POST.get('twentee_eight')
            document = request.FILES['twentee_nine']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='EPF WITH CHALLAN', Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=2)
            data1.save()

            office_name = request.POST.get('thiety')
            document_no = request.POST.get('thiety_one')
            issu_date = request.POST.get('thiety_two')
            ex_date = request.POST.get('thiety_three')
            document = request.FILES['thiety_four']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='ESIC REGISTRATION WITH CHALLAN',
                                 Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=1)
            data1.save()

            office_name = request.POST.get('thiety_five')
            document_no = request.POST.get('thiety_six')
            issu_date = request.POST.get('thiety_seven')
            ex_date = request.POST.get('thiety_eight')
            document = request.FILES['thiety_nine']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='EXPERIENCE CERTIFICATE FOR LAST 2 YEAR',
                                 Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=1)
            data1.save()

            office_name = request.POST.get('fourty')
            document_no = request.POST.get('fourty_one')
            issu_date = request.POST.get('fourty_two')
            ex_date = request.POST.get('fourty_three')
            document = request.FILES['fourty_four']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='NAME AND REGISTRATION NO OF SUPERVISOR',
                                 Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=1)
            data1.save()

            office_name = request.POST.get('fourty_five')
            document_no = request.POST.get('fourty_six')
            issu_date = request.POST.get('fourty_seven')
            ex_date = request.POST.get('fourty_eight')
            document = request.FILES['fourty_nine']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='NAME OF CONTRACTOR/FIRM AND CLASS',
                                 Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Doc_expiry_date=ex_date, Approval_doc=1)
            data1.save()
            office_name = request.POST.get('fifty')
            document_no = request.POST.get('fifty_one')
            issu_date = request.POST.get('fifty_two')
            document = request.FILES['fifty_three']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='PAN CARD NUMBER', Issued_office_Name=office_name,
                                 Document_Number=document_no, Ddocfile=document, Doc_issue_date=issu_date,
                                 Approval_doc=1)

            document_no = request.POST.get('twenty_four')
            document = request.FILES['twenty_five_90']
            data1 = TKC_Document(user_id=user_id, Types_of_Docs='Electricity bill of Firm /Company Premises',
                                 Document_Number=document_no, Ddocfile=document, Approval_doc=1)
            data1.save()
            if User_Registration_Check_Status.objects.filter(User=data).exists():
                data1 = User_Registration_Check_Status.objects.get(User=data)
                data1.page_10 = 1
                data1.save()
            else:
                user = User_Registration_Check_Status(User=data, page_10=1)
                user.save()

            return redirect("tkc_reg_eleven")
    return render(request, 'tkc/tkc_reg10.html')


def tkc_update(request):
    if request.session.has_key('otp'):

        if TKC_Document.objects.filter(complete_data=1).exists():
            return redirect('tkc_reg_eleven')

        else:
            return redirect('tkc_reg_eight')

    return render(request, 'tkc/tkc_update.html')


def tkc_reg_eleven(request):
    data = User_Registration.objects.get(Otp=request.session['otp'])
    data.Complete_Details = 1
    data.save()
    oyt = data.Oyt
    payment = TKC_Payment.objects.get(id=oyt)
    return render(request, 'tkc/tkc_reg11.html', {'amount': payment})


def tkc_reg_twelve(request):
    return render(request, 'tkc/tkc_reg12.html')


def base(request):
    return render(request, 'tkc/user_base.html')


def message(request):
    return render(request, 'tkc/message.html')


def update_message(request):
    return render(request, 'tkc/message.html')


def activation(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'])
        user_id = data.User_Id
        doc = TKC_Document.objects.filter(user_id=user_id, Types_of_Docs='ELECTRICAL LICENSE')
        data1 = doc[0].Doc_expiry_date - data.Updated_Date.date()
        expiry_date = doc[0].Doc_expiry_date
        registration_date = data.Updated_Date.date()
        return render(request, 'tkc/activation.html', {"userdata": data, "doc": doc[0], "days": data1.days,
                                                       "expiry_date": expiry_date,
                                                       "registration_date": registration_date})


def activation_after_expired(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'])
        data.work_approval = 0
        data.finance_approval = 0
        data.qc_approval = 0
        data.Complete_Details = 0
        data.save()
        user_id = data.User_Id
        doc = TKC_Document.objects.filter(user_id=user_id).delete()
        data1 = User_Registration_Check_Status.objects.get(User=data)
        data1.page_10 = 0
        data1.page_11 = 0
        data1.save()
        redirect(tkc_reg_seven)
    return render(request, 'tkc/basicinfo.html', {"userdata": data})


def activation_before_expired(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'])
        data.work_approval = 0
        data.finance_approval = 0
        data.qc_approval = 0
        data.save()
        user_id = data.User_Id
        doc = TKC_Document.objects.filter(user_id=user_id).delete()
        data1 = User_Registration_Check_Status.objects.get(User=data)
        data1.page_10 = 0
        data1.page_9 = 0
        data1.save()
        redirect(tkc_reg_seven)


def updatedata(request):
    if request.session.has_key('otp'):
        data = User_Registration.objects.get(Otp=request.session['otp'])
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
    data = User_Registration.objects.filter(Otp=request.session['otp'])
    data360 = User_Registration.objects.get(Otp=request.session['otp'])

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
    return render(request, 'main/login')


def rejected_doc(request):
    data = User_Registration.objects.get(Otp=request.session['otp'])
    user_id = data.User_Id
    data = TKC_Document.objects.filter(
        Primary_verification_Status=2, user_id=user_id, Status=0)
    # data1 = NABL_Document.objects.filter(CGM_verification_Status=4, user_id=user_id, Status=0)
    return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})


def rejected_doc_save(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'])
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
    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0)
    if data:
        return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})
    else:
        data1 = User_Registration.objects.get(Otp=request.session['otp'])
        data1.work_approval = 0
        data1.save()
    return render(request, 'tkc/tkc_Base.html', {"data": data})


def rejected_doc_finance_save(request, id):
    data = User_Registration.objects.get(Otp=request.session['otp'])
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
    data = TKC_Document.objects.filter(Primary_verification_Status=2, user_id=user_id, Status=0)
    if data:
        return render(request, 'tkc/rejected_doc_resubmit.html', {"data": data})
    else:
        data1 = User_Registration.objects.get(Otp=request.session['otp'])
        data1.finance_approval = 0
        data1.save()
    return render(request, 'tkc/tkc_Base.html', {"data": data})


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
    data = User_Registration.objects.filter(Otp=request.session['otp'])
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

    user = User_Registration.objects.filter(ContactNo=Phone_no)
    user.update(tkc_payment=1)
    date = datetime.now()

    sms = User_Registration.objects.get(ContactNo=Phone_no)
    mobile = sms.ContactNo
    name_sms = sms.CompanyName_E
    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080"}
    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007277348148394809&mobile_number=" + str(
        mobile) + "&v1=" + str(name_sms) + "&v2=" + str()
    response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

    sms = User_Registration.objects.get(Otp=request.session['otp'])
    mobile = sms.ContactNo
    name_sms = sms.CompanyName_E
    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080"}
    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
    url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007744910864040749&mobile_number=" + str(
        mobile) + "&v1=" + str('DGM') + "&v2=" + str() + "&v3=" + str(name_sms) + "&v4=" + str() + "&v5=" + str(
        'https://qcportal.mpcz.in/')
    response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})

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
    data = User_Registration.objects.get(Otp=request.session['otp'])
    payu_count = Payudata_main.objects.filter(Contact_No=data.ContactNo)
    return render(request, 'tkc/tkc_transation_history.html', {"posted": payu_count})
