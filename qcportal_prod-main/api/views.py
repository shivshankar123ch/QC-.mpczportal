from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import response, decorators, permissions, status
from rest_framework.decorators import api_view, permission_classes
from json import dumps, loads, JSONEncoder, JSONDecoder
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from django.views.generic import View
from . import rest_utils
from vendor.models import *
from main.models import *
from .serializers import *
from api.models import *
from nabl.models import *
from fqp.models import *
from tkc.models import *
import copy
import requests
from django.db.models import Sum

import json
import io

from rca.models import rca_test_rept_power_analyzer

from rest_framework.response import Response #by ravindra
from rest_framework.views import APIView   #by ravindra




#-------- added by shubhamt tripathi new fqpintiamntion login code from mobile------

@csrf_exempt
@api_view(['POST'])
def api_otp_generate_officer(request):
    response = Response()
    mobile = request.POST.get('mobile')
    employ_login_id = request.POST.get('employ_login_id')

    if Officer.objects.filter(mobile=mobile,employ_login_id=employ_login_id).exists():
        def generateOTP():
            OTP = ""
            digits = "123456789"
            for i in range(6):
                OTP += digits[math.floor(random.random() * 9)]
            return OTP
        otp = generateOTP()
        get_data = Officer.objects.filter(mobile=mobile,employ_login_id=employ_login_id)
        for i in get_data:
            mobile = i.mobile
            i.otp = otp
            i.save()
            # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
            response_data = requests.get(url)

            sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.now(),mobile_number = mobile)
            sms_template.save()
            
            response.data = {
                'status': 200,
                'message': 'Your otp has been sent to your registered mobile number',
                'otp': otp,
            }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif employ_login_id == "":
        response.data = {
            'status': 201,
            'message': 'Employee login id is required',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif mobile == "":
        response.data = {
            'status': 201,
            'message': 'Mobile no is required',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Please register your mobile number first before proceeding further',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



@csrf_exempt
@api_view(['POST'])
def api_officer_login(request):
    response = Response()
    mobile = request.POST.get('mobile')
    employ_login_id = request.POST.get('employ_login_id')
    otp = request.POST.get('otp')

    if Officer.objects.filter(mobile=mobile,employ_login_id=employ_login_id).exists():
        officer_data=Officer.objects.get(mobile=mobile,employ_login_id=employ_login_id,otp=otp)
        officer_data=OfficerMainSerializer(officer_data)
        if officer_data is not None: 
            response.data = {
                'status': 200,
                'message': 'You are succefully login your detail',
                'officer': officer_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")

        else:
            response.data = {
                'status': 201,

                'message': 'Otp not match please enter valid otp',
                'officer': officer_data.employ_id
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")

    elif employ_login_id == "":
        response.data = {
            'status': 201,
            'message': 'Employee login id is required',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif mobile == "":
        response.data = {
            'status': 201,
            'message': 'Mobile number is required',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif otp == "":
        response.data = {
            'status': 201,
            'message': 'Mobile OTP is required',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Please register your mobile number first before proceeding further',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

#------------------------------end here--------------------------------------------


# POORNIMA--------LOGIN MODEL SE----------------------------------------------------------------------------------

@api_view(['POST'])
def loginview(request):
    response = Response()

    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')

        if Login.objects.filter(username=name).exists():
            data = Login.objects.get(username=name)
            user_pass = data.password

            if name is None:
                response.data = {
                    'status': 200,
                    'message': 'username is Wrong',

                }
                return response

            elif user_pass == password:
                response.data = {
                    'status': 200,
                    'message': 'successful',

                }
                return response

            elif password is not None:
                response.data = {
                    'status': 201,
                    'message': 'password is Wrong',

                }
                return response

        else:

            response.data = {
                'status': 201,
                'message': 'username password is Wrong',

            }
            return response


# by //officer model----1st------------------LOGIN API ---------------------------------------

# @api_view(['POST'])
# def loginview(request):
#     response = Response()

#     if request.method=="POST":
#         name = request.POST.get('mobile')
#         password = request.POST.get('password')


#         if Officer.objects.filter(mobile=name).exists():
#             data =Officer.objects.get(mobile=name)
#             user_pass = data.password

#             if name is None:
#                 response.data = {
#                     'status' : 200,
#                     'message': 'username is Wrong',

#                 }
#                 return response

#             elif user_pass == password:
#                 response.data = {
#                     'status' : 200,
#                     'message': 'successful',

#                 }
#                 return response

#             elif password is not None:
#                 response.data = {
#                 'status' : 201,
#                 'message': 'password is Wrong',

#                 }
#                 return response


#         else:

#             response.data = {
#                 'status' : 200,
#                 'message': 'successful',

#                 }
#             return response

# ---2nd................................inspectionlist.......................................

@api_view(['GET'])
def inspectionlist(request):
    response = Response()
    data = UserCompanyDataMain.objects.all()
    queryset_serializer = UserCompanyDataMainSerializer(data, many=True)
    sss = queryset_serializer.data

    if len(sss) == 0:
        response.data = {
            'status': 201,
            'message': 'Record not Found',
            'data': queryset_serializer.data,

        }
        return response
    else:
        response.data = {
            'status': 200,
            'message': 'Succesful',
            'data': queryset_serializer.data,

        }
        return response


from rest_framework.views import APIView


class User_Registration_UserCompanyDataMain(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        user = authenticate(username=data["username"], password=data["password"])
        if user:
            usr = User_Registration.objects.filter(factory_approval=1)  # f=1
            uscm = UserCompanyDataMain.objects.all()
            User_Registration_data = User_RegistrationSerializer(usr, many=True)
            UserCompanyDataMain_data = UserCompanyDataMainSerializer(uscm, many=True)
            result_serializer_data = User_Registration_data.data + UserCompanyDataMain_data.data
            return Response(result_serializer_data)


# -----vendor Detail---3rd API------------------------------------------------------------------------------------------

@api_view(['POST'])
def vendordetail(request):
    if request.method == "POST":
        user_id = request.data.get('user_id')
        serializers = VendorDetailSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message': 'Succesful', 'status': '200'}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# -----add_appraisalreport---4TH API-----------view record par-------------------------------------------------------------------------------

@api_view(['POST'])
def add_appraisalreport(request, format=None):
    if request.method == "POST":
        serializers = AppraisalReportSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message': 'Succesful', 'status': '200'}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# ....5th api all Record............................................................................................................

@api_view(['GET'])
def inspectionrecord(request):
    response = Response()
    data = UserCompanyDataMain.objects.all()
    queryset_serializer = UserCompanyDataMainSerializer(data, many=True)
    data2 = VendorDetail.objects.all()
    queryset_serializer2 = VendorDetailSerializer(data2, many=True)
    data3 = AppraisalReport.objects.all()
    queryset_serializer3 = AppraisalReportSerializer(data3, many=True)

    response.data = {
        'UserCompanyDataMain': queryset_serializer.data,
        'VendorDetail': queryset_serializer2.data,
        'AppraisalReport': queryset_serializer3.data
    }
    return response


# ------6th api techniacl recoeds-------------------------------------------------------------------------------------------------

@api_view(['GET'])
def technicaldetail(request):
    response = Response()
    Result = Vendor_Material_Details.objects.all()
    queryset_serializer = Vendor_Material_DetailsSerializer(Result, many=True)

    sss = queryset_serializer.data

    if len(sss) == 0:

        response.data = {
            'status': 201,
            'message': 'Record not Found',
            'Result': queryset_serializer.data,

        }
        return response

    else:
        response.data = {
            'status': 200,
            'message': 'Record fetched successfully',
            'Result': queryset_serializer.data,

        }
        return response


# get send the doc list-------------------------------------------------------------

@api_view(['GET'])
def technicalpost(request):
    response = Response()
    user_id = request.POST.get('user_id')
    data = Vendor_Material_Details.objects.filter(user_id=user_id)

    queryset_serializer = VendorMaterialDetailsSerializer(data, many=True)
    response.data = {
        # 'status' : 200,
        # 'message': 'Record fetched successfully',
        'data': queryset_serializer.data,

    }
    return response


# ----------------------all technical data save-------------

@api_view(['POST'])
def technicaldata(request):
    if request.method == "POST":
        user_id = request.data.get("user_id")
        # material=
        # specfucation
        # linkpdf name
        serializers = VendorMaterialDetailsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'message': 'Succesful', 'status': '200'}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# --------document save---------------------pdf-----------------

@api_view(['POST'])
def Documentsave(request):
    if request.method == "POST":
        serializers = MaterialVerificationSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response({'message': 'Succesful', 'status': '200'}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------------------------------------

@api_view(['POST'])
def materialdetail(request):
    response = Response()

    user_id = request.data.get('user_id')
    data = Add_material.objects.filter(user_id=user_id)
    queryset_serializer = Add_materialSerializer(data, many=True)
    response.data = {
        'status': 200,
        'message': 'Record fetched successfully',
        'data': queryset_serializer.data,

    }
    return response


# -----------------------------------------------VENDOR DETAIL PAGE(TECHNICAL DETAIL PDF)-----------------

@api_view(['POST'])
def plant_machinery(request):
    # if request.method=="POST":
    response = Response()

    user_id = request.data.get('user_id')

    # Types_of_Docs = request.data.get('Types_of_Docs')
    # data=Vendor_Technical_Details.objects.update(user_id=user_id,Types_of_Docs=Types_of_Docs)

    data = Vendor_Technical_Details.objects.filter(user_id=user_id)
    queryset_serializer = Vendor_Technical_DetailsSerializer(data, many=True)
    response.data = {
        'status': 200,
        'message': 'Record fetched successfully',
        'data': queryset_serializer.data,

    }
    return response


# test--------------------------------------------------------------------------------------------------

@api_view(['GET'])
def product(request):
    response = Response()
    # user_id  = request.POST.get('user_id')
    data = Vendor_Material_Details.objects.all()

    queryset_serializer = VendorMaterialDetailsSerializerS(data, many=True)
    response.data = {
        'status': 200,
        'message': 'Record fetched successfully',
        'data': queryset_serializer.data,

    }
    return response


@api_view(['GET'])
def product2(request):
    response = Response()
    # user_id  = request.POST.get('user_id')
    data = Vendor_Material_Details.objects.all()

    queryset_serializer = VendorMaterialDetailsSerializer(data, many=True)
    response.data = {
        'status': 200,
        'message': 'Record fetched successfully',
        'data': queryset_serializer.data,

    }
    return response


# -------------------------------------------------------------------------------------------------

def vendorremark(request):
    response = Response()
    if request.method == "POST":
        hours = request.POST.get('hours')

        Primary_remark = requests.POST.get("Primary_remark")
        aa = Vendor_BalanceSheet.objects.create(Primary_remark=Primary_remark)
        aa.save()

    # -------------------------------------------------------------------------------------------------------

    response.data = {
        'status': 200,
        'message': 'successful',

    }
    return response


# -EXTRA---all vendor list done but not work on server..vendore list all whan f=1,w&P=1.............................................................................................

@api_view(['GET'])
def vendorlist(request):
    response = Response()
    finance_approval = 1
    work_approval = 1
    data = User_Registration.objects.filter(work_approval=1) | User_Registration.objects.filter(finance_approval=1)
    queryset_serializer = User_RegistrationSerializer(data, many=True)

    if data is not None:
        response.data = {
            'status': 200,
            'message': 'successful',
            'data': queryset_serializer.data,

        }
        return response
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': queryset_serializer.data,

        }
        return response


# after schedule show all list......................................................................

e_msg = {'status': 201, 'message': 'Record Not Found', 'Data': []}
s_msg = {'status': 200, 'message': "successful"}


@api_view(['GET'])
def viewscheduledata(request):
    response = Response()

    data = UserCompanyDataMain.objects.all()
    queryset_serializer = UserCompanyDataMainSerializer(data, many=True)
    if data is not None:

        response.data = {
            'status': 200,
            'message': 'successful',
            'data': queryset_serializer.data,

        }
        return response
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': queryset_serializer.data,

        }
        return response


# testing----------vendore list all whan f=1,w&P=1------------------------------------------------------


@api_view(['GET'])
def userlist(request):
    response = Response()
    data = User_Registration.objects.filter(work_approval=1) | User_Registration.objects.filter(finance_approval=1)
    queryset_serializer = User_RegistrationSerializer(data, many=True)
    queryset_serializer_rohit = queryset_serializer.data
    # aaa = json.dumps(queryset_serializer_rohit)
    aaa = json.loads(json.dumps(queryset_serializer_rohit))
    bbb = aaa[0]['CompanyName_E']
    new_data = UserCompanyDataMain.objects.filter(CompanyName_E=bbb)
    new_queryset_serializer = UserCompanyDataMainSerializer(new_data, many=True)

    if data is not None:

        response.data = {
            'status': 200,
            'message': 'successful',
            'data': queryset_serializer.data,

        }
        return response

    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': queryset_serializer.data,

        }
        return response


# ----------------------------------------------------------------------------------------------

# @api_view(['POST'])
# def rating(request):
#     if request.method=="POST":
#         serializers=RatingSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data,status=status.HTTP_201_CREATED)
#         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------------------

# @api_view(['POST'])
# def inspectionrecord(request):
#     if request.method=="POST":
#         serializers=RatingSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data,status=status.HTTP_201_CREATED)
#         return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


# ----fqp------------------------1st---------------------------------------------------------------------

@api_view(['POST'])
def login_fqp(request):
    response = Response()
    if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')

        if Login.objects.filter(username=name).exists():
            data = Login.objects.get(username=name)
            user_pass = data.password

            if name is None:
                response.data = {
                    'status': 200,
                    'message': 'username is Wrong',

                }
                return response

            elif user_pass == password:
                response.data = {
                    'status': 200,
                    'message': 'successful',

                }
                return response

            elif password is not None:
                response.data = {
                    'status': 201,
                    'message': 'password is Wrong',

                }
                return response

        else:

            response.data = {
                'status': 201,
                'message': 'username password is Wrong',

            }
            return response


@api_view(['POST'])
def quality_list(request):
    response = Response()
    officer_id = request.POST.get('officer_id')

    data = FQP_Material.objects.filter(officer_id=officer_id)

    queryset_serializer = FQP_MaterialSerializer(data, many=True)
    if data is not None:

        response.data = {
            'status': 200,
            'message': 'successful',
            'data': queryset_serializer.data,

        }
        return response
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': queryset_serializer.data,

        }
        return response


# --------DTS list -----------------2nd -------------------------------------------------------

@api_view(['POST'])
def DTS_data(request):
    response = Response()
    FQP_Material = request.POST.get('FQP_Material')

    data = FQP_Test.objects.filter(FQP_Material=FQP_Material)

    queryset_serializer = FQP_TestSerializer(data, many=True)
    sss = queryset_serializer.data

    if FQP_Material is None:
        response.data = {
            'status': 201,
            'message': 'FQP_Material_Id is Required',
            'data': queryset_serializer.data,

        }
        return response

    elif len(sss) == 0:

        response.data = {
            'status': 201,
            'message': 'Record not Found',
            'data': queryset_serializer.data,

        }
        return response

    else:

        response.data = {
            'status': 200,
            'message': 'Recoed Found',
            'data': queryset_serializer.data,

        }
        return response


# ---------------------recordsave 3rd-------------------------------------------------

error = {'status': "error"}


@api_view(['POST'])
def DTR_record(request):
    if request.method == "POST":
        serializers = FQP_Test_DataSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    response = Response()
    oid = request.POST.get('officer_employ_id')
    opass = request.POST.get('officer_password')
    data = InspectingOfficerInfo.objects.filter(officer_employ_id=oid, officer_password=opass)
    queryset_serializer = InspectingOfficerInfoSerializer(data, many=True)
    sss = queryset_serializer.data
    if InspectingOfficerInfo.objects.filter(officer_employ_id=oid, officer_password=opass, officer_work='FQP').exists():
        abc = InspectingOfficerInfo.objects.get(officer_employ_id=oid, officer_password=opass, officer_work='FQP')
        aaa = abc.id
        response.data = {

            'status': 200,
            'id': aaa,
            'message': 'Officer found',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


    else:

        response.data = {
            'status': 201,
            'message': 'Recoed not Found',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


# class LoginAPIView(generics.GenericAPIView):
#     serializer_class = FQP_OfficerSerializer

#     def post(self, request):
#         try:
#             data = request.data
#             serializer = self.serializer_class(data=data)
#             if serializer.is_valid():
#                 message = "User Successfully Login"
#                 return rest_utils.build_response(
#                     status.HTTP_200_OK, message, data=serializer.data, errors=None
#                 )
#             else:
#                 return rest_utils.build_response(
#                     status.HTTP_400_BAD_REQUEST,
#                     rest_utils.HTTP_REST_MESSAGES["400"],
#                     data=None,
#                     errors=serializer.errors,
#                 )

#         except Exception as e:
#             message = rest_utils.HTTP_REST_MESSAGES["500"]
#             return rest_utils.build_response(
#                 status.HTTP_500_INTERNAL_SERVER_ERROR, message, data=None, errors=str(e)
#             )


# rohit-----------------------------------------

#
@api_view(['GET'])
def material_specification(request):
    response = Response()
    data = Material_Specification.objects.all()
    queryset_serializer = Material_SpecificationSerializer(data, many=True)
    sss = queryset_serializer.data

    if len(sss) == 0:

        response.data = {
            'status': 201,
            'message': 'Record not Found',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 200,
            'message': 'Succesful',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def material_master(request):
    response = Response()
    data = Vendor_Material_Master.objects.all()
    queryset_serializer = Material_MasterSerializer(data, many=True)
    sss = queryset_serializer.data
    if len(sss) == 0:
        response.data = {
            'status': 201,
            'message': 'Record not Found',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 200,
            'message': 'Succesful',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['GET'])
def material_specification_master(request, id):
    response = Response()
    material = Vendor_Material_Master.objects.get(Material_Id=id)
    data = Vendor_Material_Specification_Master.objects.filter(Material=material, Status=1)
    serial = Material_SpecificationSerializer(data, many=True)
    if Vendor_Material_Specification_Master.objects.filter(Material=material, Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'material_specification': serial.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'material_specification': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def material_is_master(request, id):
    response = Response()
    material = Vendor_Material_Specification_Master.objects.get(Material_Specification_Id=id)
    data = Nabl_Is_Master.objects.filter(Is_Id=material.Is.Is_Id,Status=1)
    serial = IS_Serializer(data, many=True)
    if Nabl_Is_Master.objects.filter(Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'material_specification': serial.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'material_specification': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def material_test_master(request, id):
    response = Response()
    is_data = Nabl_Is_Master.objects.get(Is_Id=id)
    data = Nabl_Acceptance_Test_Master.objects.filter(Is=is_data,Status=1)
    serial = Material_Test(data, many=True)
    if Nabl_Acceptance_Test_Master.objects.filter(Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'material_specification': serial.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'material_specification': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



import json


@api_view(['GET'])
def material_featch(request, id):
    response = Response()
    data = Material_Specification.objects.filter(Material_Id=id)
    serial = Material_SpecificationSerializer(data, many=True)
    response = serial.data
    return HttpResponse(json.dumps(response), content_type="application/json")

@api_view(['GET'])
def material_test_fetch(request, id):
    response = Response()
    data = List_Of_Test.objects.filter(Product_Id = id)
    serial = Material_Test(data, many=True)
    response = serial.data
    return HttpResponse(json.dumps(response), content_type="application/json")





# --------------------jeevan----------------->


import json


@api_view(['POST'])
def no_verification(request):
    response = Response()
    oid = request.POST.get('contact')
    if User_Registration.objects.filter(ContactNo=oid).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Recoed Not Found',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


import math;
import random;

all_otp = [];


@csrf_exempt
@api_view(['POST'])
def otp_generate(request):
    response = Response()
    oid = request.POST.get('contact')
    user_type_check = request.POST.get('user_type')
    if user_type_check=='SITE_STORE':
        print("Site Storeeeee")
        site_data=SiteStore_Master.objects.filter(contact_no=oid)
        for each in site_data:
            if each.otp == None:
                print("yhaaa")
                def generateOTP():
                        OTP = ""
                        digits = "123456789"
                        for i in range(6):
                            OTP += digits[math.floor(random.random() * 9)]
                        return OTP
                otp = generateOTP()
                all_otp.append(otp)
                get_data = SiteStore_Master.objects.filter(contact_no=oid)
                for i in get_data:                   
                    
                    mobile = i.contact_no                    
                    i.otp = otp
                    i.save()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    try:
                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
                        response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                        sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.now(),mobile_number = mobile)
                        sms_template.save()
                    except Exception as e:
                        pass
                    response.data = {
                        'status': 200,
                        'message': 'Your otp has been sent to your registered mobile number',
                        'otp': otp,
                    }
                
                return HttpResponse(json.dumps(response.data), content_type="application/json")
            else:
                def generateOTP():
                        OTP = ""
                        digits = "123456789"
                        for i in range(6):
                            OTP += digits[math.floor(random.random() * 9)]
                        return OTP
                otp = generateOTP()
                all_otp.append(otp)
                get_data = SiteStore_Master.objects.filter(contact_no=oid)
                for i in get_data:                   
                    
                    mobile = i.contact_no                    
                    i.otp = otp
                    i.save()
                    header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
                    proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
                    try:
                        url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
                        response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})            
                        sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.now(),mobile_number = mobile)
                        sms_template.save()
                    except Exception as e:
                        pass
                    response.data = {
                        'status': 200,
                        'message': 'Your otp has been sent to your registered mobile number',
                        'otp': otp,
                    }
                
                return HttpResponse(json.dumps(response.data), content_type="application/json")
    
    if User_Registration.objects.filter(ContactNo=oid,is_cpri_user=True).exists():
        otp_data = User_Registration.objects.get(ContactNo=oid,is_cpri_user=True)
        if otp_data.Otp == None:
            def generateOTP():
                    OTP = ""
                    digits = "123456789"
                    for i in range(6):
                        OTP += digits[math.floor(random.random() * 9)]
                    return OTP
            otp = generateOTP()
            all_otp.append(otp)
            get_data = User_Registration.objects.get(ContactNo=oid)
            mobile = get_data.ContactNo
            get_data.Otp = otp
            get_data.save()
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            try:
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
                response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.datetime.now(),mobile_number = mobile)
                sms_template.save()
            except Exception as e:
                pass            
            
            response.data = {
                'status': 200,
                'message': 'Your Password as otp has been sent to your registered mobile',
                'otp': otp,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Please login with your password',
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        
    if User_Registration.objects.filter(ContactNo=oid,User_type=user_type_check,otp_not_change=1).exists():
        def generateOTP():
            OTP = ""
            digits = "123456789"
            for i in range(6):
                OTP += digits[math.floor(random.random() * 9)]
            return OTP
        otp = generateOTP()
        
        get_data = User_Registration.objects.filter(ContactNo=oid,User_type=user_type_check)
        for i in get_data:
            mobile = i.ContactNo
            
            # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
            # response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
            
            # sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.now(),mobile_number = mobile)
            # sms_template.save()
            
            response.data = {
                'status': 200,
                'message': 'Your otp has been sent to your registered mobile number',
                'otp': otp,
            }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    if User_Registration.objects.filter(ContactNo=oid,User_type=user_type_check).exists():
        def generateOTP():
            OTP = ""
            digits = "123456789"
            for i in range(6):
                OTP += digits[math.floor(random.random() * 9)]
            return OTP
        otp = generateOTP()
        all_otp.append(otp)
        get_data = User_Registration.objects.filter(ContactNo=oid,User_type=user_type_check)
        for i in get_data:
            mobile = i.ContactNo
            i.Otp = otp
            i.save()
            header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
            proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
            try:
                url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1207160939830278103&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
                response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
                
                sms_template = message_template_log(template_id = '1207160939830278103',date = datetime.now(),mobile_number = mobile)
                sms_template.save()
            except Exception as e:
                pass
            response.data = {
                'status': 200,
                'message': 'Your otp has been sent to your registered mobile number',
                'otp': otp,
            }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Please register your mobile number first before proceeding further',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


# <-----------------FI API----------------------->
@api_view(['POST'])
def FI_Login(request):
    response = Response()
    oid = request.POST.get('employ_id')
    opass = request.POST.get('password')
    if InspectingOfficerInfo.objects.filter(officer_employ_id=oid, officer_password=opass, officer_work='FI').exists():
        abc = InspectingOfficerInfo.objects.get(officer_employ_id=oid, officer_password=opass, officer_work='FI')
        officer = InspectingOfficerInfoSerializer(abc)
        task = Factory_Inspection_Info.objects.filter(officer=abc)
        task_data = Factory_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': officer.data,
            # 'task': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FI_Inspection_List(request):
    response = Response()
    eid = request.POST.get('employ_id')
    task_name = request.POST.get('task_name')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if task_name == 'fi':
        if Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
            task = Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=0)
            task_data = Factory_Inspection_InfoSerializer(task, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': task_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:

            response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'data': [],

            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif task_name == 'rca':
        if RCA_Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
            task = RCA_Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=0)
            task_data = RCA_Factory_Inspection_InfoSerializer(task, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': task_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['POST'])
def FI_Inspection_Record(request):
    response = Response()
    eid = request.POST.get('employ_id')
    task_name = request.POST.get('task_name')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if task_name == 'fi':
        if Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
            task = Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=1)
            task_data = Factory_Inspection_InfoSerializer(task, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': task_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'data': [],

            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif task_name == 'rca':
        if RCA_Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
            task = RCA_Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=1)
            task_data = RCA_Factory_Inspection_InfoSerializer(task, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'complete_list': task_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'complete_list': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['POST'])
def FI_Material_List(request):
    response = Response()
    task_id = request.POST.get('task_id')
    if Factory_Inspection_Info.objects.filter(id=task_id).exists():
        task = Factory_Inspection_Info.objects.get(id=task_id)
        material = Vendor_Material_Details.objects.filter(user_id=task.vendor)
        material_data = Vendor_Material_Details_Serializer(material, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': material_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FI_Material_Verify(request):
    response = Response()
    task_id = request.POST.get('task_id')
    doc_id = request.POST.get('doc_id')
    remark = request.POST.get('remark')
    status = request.POST.get('status')
    if Vendor_Material_Details.objects.filter(id=doc_id).exists():
        FI = Vendor_Material_Details.objects.get(id=doc_id)
        FI.Primary_remark = remark
        FI.Primary_verification_Status = status
        FI.response_submitted = 1
        FI.save()
        response.data = {
            'status': 200,
            'message': 'Data Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FI_Inspection_Deny(request):
    response = Response()
    eid = request.POST.get('employ_id')
    task_id = request.POST.get('task_id')
    remark = request.POST.get('remark')
    task_name = request.POST.get('task_name')
    if task_name == 'fi':
        if Factory_Inspection_Info.objects.filter(id=task_id).exists():
            FI = Factory_Inspection_Info.objects.get(id=task_id)
            FI.Is_Active = -1
            FI.deny_reason = remark
            FI.save()
        abc = InspectingOfficerInfo.objects.get(id=eid)
        if Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
            task = Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0)
            task_data = Factory_Inspection_InfoSerializer(task, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': task_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'data': [],

            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif task_name == 'rca':
        if RCA_Factory_Inspection_Info.objects.filter(id=task_id).exists():
            FI = RCA_Factory_Inspection_Info.objects.get(id=task_id)
            FI.Is_Active = -1
            FI.deny_reason = remark
            FI.save()
            FI.vendor.factory_approval_status = 0 ;
            FI.vendor.save()
        abc = InspectingOfficerInfo.objects.get(id=eid)
        if RCA_Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
            task = RCA_Factory_Inspection_Info.objects.filter(officer=abc, Is_Active=0)
            task_data = RCA_Factory_Inspection_InfoSerializer(task, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': task_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'data': [],

            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FI_Document_Verify(request):
    response = Response()
    task_id = request.POST.get('task_id')
    doc_id = request.POST.get('doc_id')
    remark = request.POST.get('remark')
    status = request.POST.get('status')
    if Vendor_Technical_Details.objects.filter(id=doc_id).exists():
        FI = Vendor_Technical_Details.objects.get(id=doc_id)
        FI.Primary_remark = remark
        FI.Primary_verification_Status = status
        FI.response_submitted = 1
        FI.save()
        response.data = {
            'status': 200,
            'message': 'Record Save',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FI_Document_List(request):
    response = Response()
    task_id = request.POST.get('task_id')
    task_name = request.POST.get('task_name')
    if task_name == 'fi':
        if Factory_Inspection_Info.objects.filter(id=task_id).exists():
            task = Factory_Inspection_Info.objects.get(id=task_id)
            material = Vendor_Technical_Details.objects.filter(user_id=task.vendor.User_Id)
            material_data = Vendor_Technical_Document_Serializer(material, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': material_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:

            response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'data': [],

            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    elif task_name == 'rca':
        if RCA_Factory_Inspection_Info.objects.filter(id=task_id).exists():
            task = RCA_Factory_Inspection_Info.objects.get(id=task_id)
            if Rca_Vendor_Document.objects.filter(user_id=task.vendor.User_Id).exists():
                material = Rca_Vendor_Document.objects.filter(user_id=task.vendor.User_Id)
                material_data = RCA_Vendor_Technical_Document_Serializer(material, many=True)
                response.data = {
                    'status': 200,
                    'message': 'Record Found',
                    'document': material_data.data,
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
            else:
                response.data = {
                    'status': 201,
                    'message': 'Record Not Found',
                    'document': [],
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Task Id wrong',
                'data': [],

            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
            

@api_view(['POST'])
def RCA_FI_Document_Response(request):
    response = Response()
    task_id = request.POST.get('task_id')
    # e use for electricity connection
    # e_doc_id = request.POST.get('e_doc_id')
    # e_remark = request.POST.get('e_remark')
    # e_remark = request.POST.get('e_remark')

    # pm use for plant and machines
    # pm_doc_id = request.POST.get('pm_doc_id')
    # pm_remark = request.POST.get('pm_remark')
    # pm_status = request.POST.get('pm_status')

    # te use for testing_equipments
    # te_doc_id = request.POST.get('te_doc_id')
    # te_remark = request.POST.get('te_remark')
    # te_status = request.POST.get('te_status')

    # cc use for calibration_certificate
    # cc_doc_id = request.POST.get('cc_doc_id')
    # cc_remark = request.POST.get('cc_remark')
    # cc_status = request.POST.get('cc_status')

    # image_1 = request.POST.get('image_1')
    # image_2 = request.POST.get('image_2')
    # image_3 = request.POST.get('image_3')

    doc = Rca_Vendor_Document.objects.get(Vendor_Document_Id=request.POST.get('cc_doc_id'))
    doc.Primary_remark = request.POST.get('cc_remark')
    doc.Primary_verification_Status = request.POST.get('cc_status')
    doc.Primary_verification_Date = datetime.now().date()
    doc.save()
    doc = Rca_Vendor_Document.objects.get(Vendor_Document_Id=request.POST.get('te_doc_id'))
    doc.Primary_remark = request.POST.get('te_remark')
    doc.Primary_verification_Status = request.POST.get('te_status')
    doc.Primary_verification_Date = datetime.now().date()
    doc.save()
    doc = Rca_Vendor_Document.objects.get(Vendor_Document_Id=request.POST.get('pm_doc_id'))
    doc.Primary_remark = request.POST.get('pm_remark')
    doc.Primary_verification_Status = request.POST.get('pm_status')
    doc.Primary_verification_Date = datetime.now().date()
    doc.save()
    doc = Rca_Vendor_Document.objects.get(Vendor_Document_Id=request.POST.get('e_doc_id'))
    doc.Primary_remark = request.POST.get('e_remark')
    doc.Primary_verification_Status = request.POST.get('e_status')
    doc.Primary_verification_Date = datetime.now().date()
    doc.save()
    task = RCA_Factory_Inspection_Info.objects.get(id=task_id)
    RCA_Vendor_Factory_image(Vendor=task.vendor, Image=request.FILES['image_1']).save()
    RCA_Vendor_Factory_image(Vendor=task.vendor, Image=request.FILES['image_2']).save()
    RCA_Vendor_Factory_image(Vendor=task.vendor, Image=request.FILES['image_3']).save()
    task.vendor.lat = request.POST.get('lat')
    task.vendor.log = request.POST.get('long')
    task.vendor.factory_approval = 1
    task.vendor.save()
    task.Status = 1
    task.perform_date = datetime.now().date()
    task.save()
    
    user_zone = vendor.User_zone
    user_name = vednor.CompanyName_E
    date = datetime.datetime.now()
    
    
    # header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
    # proxyDict = {"http" : "proxy.mpcz.in:8080","https" : "proxy.mpcz.in:8080"}
    # url = "https://sms.mpcz.in/api/v1/send-otp?app_key=VgsdaQYXmsmVFsUi2Fe4tC7vn&app_secret=dwGINQswrHtyngc&dlt_template_id=1007840595295242797&mobile_number=" + str(mobile) + "&v1=" + str(otp) + "&v2=" + str()
    # response_data = requests.get(url,proxies=proxyDict,headers={'User-Agent': 'Chrome'})
    
    
    if task_id:
        response.data = {
            'status': 200,
            'message': 'Record Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")            


@api_view(['POST'])
def FI_Technical_Details(request):
    response = Response()
    task_id = request.POST.get('task_id')
    consumer_no = request.POST.get('consumer_no')
    sanction = request.POST.get('sanction_id')
    work_load = request.POST.get('work_load')
    load_shading = request.POST.get('load_shading')
    dg_rating = request.POST.get('dg_rating')
    power_backup = request.POST.get('power_backup')
    power_remark = request.POST.get('power_remark')
    plant_machinery = request.POST.get('plant_machinery')
    description = request.POST.get('description')
    latest_machinery = request.POST.get('latest_machinery')
    latest_remark = request.POST.get('latest_remark')
    manufacturing = request.POST.get('manufacturing')
    manufacturing_remark = request.POST.get('manufacturing_remark')
    inspection = request.POST.get('inspection')
    inspection_remark = request.POST.get('inspection_remark')
    sub_stand = request.POST.get('sub_stand')
    sub_stand_remark = request.POST.get('sub_stand_remark')
    assistance = request.POST.get('assistance')
    assistance_remark = request.POST.get('assistance_remark')
    internal_testing = request.POST.get('internal_testing')
    internal_testing_remark = request.POST.get('internal_testing_remark')
    details_testing = request.POST.get('details_testing')
    details_testing_remark = request.POST.get('details_testing_remark')
    vendor = Factory_Inspection_Info.objects.get(id=task_id)
    ftd_obj = Factory_Technical_Details(vendor=vendor.vendor, consumer_no=consumer_no, section_id=sanction, work_load=work_load,
                                        load_shading=load_shading, dg_rating=dg_rating, power_backup=power_backup,
                                        power_remark=power_remark, plant_machinery=plant_machinery, description=description,
                                        latest_machinery=latest_machinery, latest_remark=latest_remark, manufacturing=manufacturing,
                                        manufacturing_remark=manufacturing_remark, inspection=inspection, inspection_remark=inspection_remark,
                                        sub_stand=sub_stand, sub_stand_remark=sub_stand_remark, assistance=assistance,
                                        assistance_remark=assistance_remark, internal_testing=internal_testing,
                                        internal_testing_remark=internal_testing_remark, details_testing=details_testing,
                                        details_testing_remark=details_testing_remark)
    ftd_obj.save()
    if task_id:
        response.data = {
            'status': 200,
            'message': 'Record Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Save',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FI_Factory_Data(request):
    response = Response()
    task_id = request.POST.get('task_id')
    Latitude = request.POST.get('Latitude')
    Longitude = request.POST.get('Longitude')
    image1 = request.FILES['image1']
    image2 = request.FILES['image2']
    image3 = request.FILES['image3']
    type = request.POST.get('type')
    if Factory_Inspection_Info.objects.filter(id=task_id).exists():
        task = Factory_Inspection_Info.objects.get(id=task_id)
        factory = User_Registration.objects.get(User_Id=task.vendor.User_Id)
        task.lattitude = Latitude
        task.longtitude = Longitude
        task.save()
        fac_image = Vendor_Factory_image(vendor=factory,Image=image1)
        fac_image.save()
        fac_image = Vendor_Factory_image(vendor=factory,Image=image2)
        fac_image.save()
        fac_image = Vendor_Factory_image(vendor=factory,Image=image3)
        fac_image.save()
        if type == '4':
            task.Status = 1
        response.data = {
            'status': 200,
            'message': 'Record Save',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['POST'])
def FI_Appraisal(request):
    response = Response()
    task_id = request.POST.get('task_id')
    experience = request.POST.get('experience')
    availability = request.POST.get('availability')
    calibration = request.POST.get('calibration')
    bought = request.POST.get('bought')
    inprocess = request.POST.get('inprocess')
    dispatch = request.POST.get('dispatch')
    overall = request.POST.get('overall')
    control = request.POST.get('control')
    iso = request.POST.get('iso')
    material = request.POST.get('material')
    general = request.POST.get('general')
    packing = request.POST.get('packing')
    incharge = request.POST.get('incharge')
    supervisor = request.POST.get('supervisor')
    controlsystem = request.POST.get('controlsystem')
    qualityofplant = request.POST.get('qualityofplant')
    workshoap = request.POST.get('workshoap')
    sefty = request.POST.get('sefty')
    store = request.POST.get('store')
    faciality = request.POST.get('faciality')
    progress = request.POST.get('progress')
    overallp = request.POST.get('overallp')
    vendor1 = Factory_Inspection_Info.objects.get(id=task_id)
    Factory = FI_Appraisal_Details.objects.all()
    FI = FI_Appraisal_Details(vendor = vendor1.vendor,experience=experience, availability=availability, calibration=calibration,
                             bought=bought, inprocess=inprocess, dispatch=dispatch, overall=overall,
                             control=control, iso=iso, material=material, general=general, packing=packing,
                             incharge=incharge, supervisor=supervisor, controlsystem=controlsystem,
                             qualityofplant=qualityofplant, workshoap=workshoap, sefty=sefty, store=store, faciality=faciality, progress=progress, overallp=overallp)

    FI.save()  
    task = Factory_Inspection_Info.objects.get(id=task_id)
    task.Status = 1
    task.vendor.factory_approval = 1
    task.perform_date = datetime.now().date()
    task.vendor.save()
    task.save()
    if task_id:
        response.data = {
            'status': 200,
            'message': 'Record Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


# <-----------------MQP ----------------------->

@api_view(['POST'])
def MQP_Login(request):
    response = Response()
    oid = request.POST.get('employ_id')
    opass = request.POST.get('password')
    if InspectingOfficerInfo.objects.filter(officer_employ_id=oid, officer_password=opass, officer_work='MQP').exists():
        abc = InspectingOfficerInfo.objects.get(officer_employ_id=oid, officer_password=opass, officer_work='MQP')
        officer = InspectingOfficerInfoSerializer(abc)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': officer.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': {},

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def MQP_Inspection_List(request):
    response = Response()
    eid = request.POST.get('employ_id')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if Material_Inspection_Info.objects.filter(officer=abc).exists():
        task = Material_Inspection_Info.objects.filter(officer=abc)
        task_data = Material_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': {},

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def MQP_Inspection_Deny(request):
    response = Response()
    eid = request.POST.get('employ_id')
    task_id = request.POST.get('task_id')
    remark = request.POST.get('remark')
    if Material_Inspection_Info.objects.filter(id=task_id).exists():
        FI = Material_Inspection_Info.objects.get(id=task_id)
        FI.Is_Active = -1
        FI.deny_reason = remark
        FI.save()
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if Material_Inspection_Info.objects.filter(officer=abc).exists():
        task = Material_Inspection_Info.objects.filter(officer=abc, Is_Active=0)
        task_data = Material_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def MQP_Material_List(request):
    response = Response()
    eid = request.POST.get('task_id')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if Material_Inspection_Info.objects.filter(id=eid).exists():
        MI = Material_Inspection_Info.objects.get(id=eid)
        DI = VendorDispatchItemInfo.objects.filter( dispatch_d = MI.di.id )
        task_data = VendorDispatchItemInfoSerializer(DI, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['POST'])
def MQP_Material_Verify(request):
    response = Response()
    doc_id = request.POST.get('doc_id')
    remark = request.POST.get('remark')
    status = request.POST.get('status')
    if VendorDispatchItemInfo.objects.filter(id=doc_id).exists():
        FI = VendorDispatchItemInfo.objects.get(id=doc_id)
        FI.remark = remark
        FI.status = status
        FI.save()
        response.data = {
            'status': 200,
            'message': 'Record Save',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['POST'])
def MQP_Inspection_Submit(request):
    response = Response()
    task_id = request.POST.get('task_id')
    if Material_Inspection_Info.objects.filter(id=task_id).exists():
        task = Material_Inspection_Info.objects.get(id=task_id)
        task.Status = 1
        task.save()
        response.data = {
            'status': 200,
            'message': 'Record Found',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



# Field Quality process


@api_view(['POST'])
def FQP_Login(request):
    response = Response()
    oid = request.POST.get('employ_id')
    opass = request.POST.get('password')
    if InspectingOfficerInfo.objects.filter(officer_employ_id=oid, officer_password=opass, officer_work='FQP').exists():
        abc = InspectingOfficerInfo.objects.get(officer_employ_id=oid, officer_password=opass, officer_work='FQP')
        officer = InspectingOfficerInfoSerializer(abc)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': officer.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FQP_Inspection_List(request):
    response = Response()
    eid = request.POST.get('employ_id')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if Field_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
        task = Field_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=0)
        task_data = Field_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FQP_Inspection_Deny(request):
    response = Response()
    eid = request.POST.get('employ_id')
    task_id = request.POST.get('task_id')
    remark = request.POST.get('remark')
    if Field_Inspection_Info.objects.filter(id=task_id).exists():
        FI = Field_Inspection_Info.objects.get(id=task_id)
        FI.Is_Active = -1
        FI.deny_reason = remark
        FI.save()
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if Field_Inspection_Info.objects.filter(officer=abc).exists():
        response.data = {
            'status': 200,
            'message': 'Deny Sucessfully',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FQP_Inspection_Record(request):
    response = Response()
    eid = request.POST.get('employ_id')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if Field_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
        task = Field_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=1)
        task_data = Field_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FQP_Test_List(request):
    response = Response()
    task_id = request.POST.get('task_id')
    if Field_Inspection_Info.objects.filter(id=task_id).exists():
        task = Field_Inspection_Info.objects.get(id=task_id)
        test = FQP_Test.objects.all()
        test_data = FQP_Test_Serializer(test, many=True)
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


@api_view(['POST'])
def FQP_Test_Parameter(request):
    response = Response()
    test_id = request.POST.get('test_id')
    if FQP_Test.objects.filter(id=test_id).exists():
        test = FQP_Test.objects.get(id=test_id)
        parameter = FQP_Test_Attributes.objects.filter(FQP_Test = test)
        parameter_data = FQP_Test_Attributes_Serializer(parameter, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': parameter_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def FQP_Test_Result(request):
    response = Response()
    test_id = request.POST.get('parameter_id')
    test = FQP_Test_Attributes.objects.get(id = test_id)
    task_id = request.POST.get('task_id')
    task = Field_Inspection_Info.objects.get(id=task_id)
    remark = request.POST.get('remark')
    status = request.POST.get('status')
    Latitude = request.POST.get('Latitude')
    Longitude = request.POST.get('Longitude')
    upload_file = request.FILES['loa_file']
    data = FQP_Test_Data(Officer=task.officer, user=task.contractor, Test=test, Status=status, Observation=remark,
                         Latitude=Latitude, Longitude=Longitude, Image=upload_file)
    data.save()
    # if len(request.FILES) != 0:
    #     upload_file = request.FILES['loa_file']
    #     vd.Loa = upload_file
    #     vd.save()
    if Field_Inspection_Info.objects.filter(id=task_id).exists():
        response.data = {
            'status': 200,
            'message': 'Record Save',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")




@api_view(['POST'])
def FQP_Inspection_End(request):
    response = Response()
    #eid = request.POST.get('employ_id')
    task_id = request.POST.get('task_id')
    #remark = request.POST.get('remark')
    if Field_Inspection_Info.objects.filter(id=task_id).exists():
        FI = Field_Inspection_Info.objects.get(id=task_id)
        FI.status = 1
        FI.save()
        # task = Field_Inspection_Info.objects.filter(officer=abc, Is_Active=0)
        # task_data = Field_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Save',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def Erp_Test(request):
    response = Response()
    parameter = Erp_Data.objects.filter(status=0)
    parameter_data = Erp_Data_Serializer(parameter, many=True)
    print('ttttttttttttttttttt',parameter_data.data)
    if Erp_Data.objects.filter(status=0).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': parameter_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Save',
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['POST'])
def PO_info(request):
    response = Response()
    po_no = request.POST.get('po_no')
    print('po_no',po_no)
    # Y for active ,N for Not active,ALL for all
    if po_no == 'Y':
        if Store_Info.objects.filter(Is_Active=1).exists():
            stor_data = {'po_no':'1234','nit_no':'hjkkkk/lmn','loa_no':'234333'}
            response.data = {
                'status': 200,
                'message': 'po exists',
                'data':stor_data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 200,
            'message': 'po not exists',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


import requests as req
from requests.auth import HTTPBasicAuth
@api_view(['POST'])
def PO_info1(request):
    response = Response()
    po_no = request.POST.get('po_no')
    # Y for active ,N for Not active,ALL for all
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
                "P_PO_NUMBER": po_no,
                # "P_PAN_CARD": "AAACS7062F"

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
        print('ttttttttttttttttttt',P_PO_RECORD)
        if not P_PO_RECORD :
            P_ERRORS = OutputParameters['P_ERRORS']
            P_ERRORS_ITEM  = P_ERRORS['P_ERRORS_ITEM']
            response.data = {
                'status': 200,
                'message': 'error',
                'data': P_ERRORS_ITEM,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")

        else:
            P_PO_RECORD_ITEM = P_PO_RECORD['P_PO_RECORD_ITEM']
            for data in P_PO_RECORD_ITEM:
                R_HEADERS = data['R_HEADERS']
                po_header = {
                    'po_no': R_HEADERS['PO_NUMBER'],
                    'CREATION_DATE': R_HEADERS['CREATION_DATE'],
                    'SUPPLIER': R_HEADERS['SUPPLIER'],
                    'SUP_ADDRESS': R_HEADERS['SUP_ADDRESS'],
                    'PO_CREATED_BY': R_HEADERS['PO_CREATED_BY'],
                    'PO_STATUS': R_HEADERS['PO_STATUS'],
                   # 'TENDOR_NO': R_HEADERS['PO_PRIFIX'] + R_HEADERS['LEGACY_PO_NUMBER'],
                    'NIT_NUMBER': R_HEADERS['NIT_NUMBER'],
                    'SUB': R_HEADERS['COMMENTS'],


                }
                response.data = {
                    'status': 200,
                    'message': 'success',
                    'data': po_header,
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")




# Location Master


@api_view(['GET'])
def discom_master(request):
    response = Response()
    data = Discom_Master.objects.all()
    queryset_serializer = Discom_MasterSerializer(data, many=True)
    sss = queryset_serializer.data
    if len(sss) == 0:
        response.data = {
            'status': 201,
            'message': 'Record not Found',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def region(request, id):
    response = Response()
    discom = Discom_Master.objects.get(id=id)
    data = Region_Master.objects.filter(Discom=discom)
    serial = Region_MasterSerializer(data, many=True)
    if Region_Master.objects.filter(Discom=discom, Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': serial.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

#------nikhil
@api_view(['GET'])
def vendor_materials(request, item_code):
    print("item_code = ", item_code)
    response = Response()
    if Vendor_Material_Details.objects.filter(item_code=item_code, new_status=1,user_id__blacklisted = 0,user_id__deregister = 0,user_id__cgm_approval= 1).count()!=0:
        data = Vendor_Material_Details.objects.filter(item_code=item_code, new_status=1,user_id__blacklisted = 0,user_id__deregister = 0,user_id__cgm_approval= 1)
    elif Vendor_Material_Details.objects.filter(item_code_ez=item_code, new_status=1,user_id__blacklisted = 0,user_id__deregister = 0,user_id__cgm_approval= 1).count()!=0:
        data = Vendor_Material_Details.objects.filter(item_code_ez=item_code, new_status=1,user_id__blacklisted = 0,user_id__deregister = 0,user_id__cgm_approval= 1)
    elif Vendor_Material_Details.objects.filter(item_code_wz=item_code, new_status=1,user_id__blacklisted = 0,user_id__deregister = 0,user_id__cgm_approval= 1).count()!=0:
        data = Vendor_Material_Details.objects.filter(item_code_wz=item_code, new_status=1,user_id__blacklisted = 0,user_id__deregister = 0,user_id__cgm_approval= 1)
        
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
        
    

    serial = Vendor_Material_Details_Serializer_shubham(data, many=True)
    response.data = {
        'status': 200,
        'message': 'Record Found',
        'data': serial.data,

    }
    return HttpResponse(json.dumps(response.data), content_type="application/json")
    


@api_view(['GET'])
def circle(request, id):
    response = Response()
    region = Region_Master.objects.get(id=id)
    data = Circle_Master.objects.filter(Region=region, Status=1)
    serial = Circle_MasterSerializer(data, many=True)
    if Circle_Master.objects.filter(Region=region, Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': serial.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def division(request, id):
    response = Response()
    circle = Circle_Master.objects.get(id=id)
    data = Division_Master.objects.filter(Circle=circle, Status=1)
    serial = Division_MasterSerializer(data, many=True)
    if Division_Master.objects.filter(Circle=circle, Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': serial.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def sub_division(request, id):
    response = Response()
    division = Division_Master.objects.get(id=id)
    data = Sub_Division_Master.objects.filter(Division=division, Status=1)
    serial = Sub_Division_MasterSerializer(data, many=True)
    if Sub_Division_Master.objects.filter(Division=division, Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': serial.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def dc(request, id):
    response = Response()
    dc = Sub_Division_Master.objects.get(id=id)
    data = DC_Master.objects.filter(Sub_Division=dc, Status=1)
    serial = DC_MasterSerializer(data, many=True)
    if DC_Master.objects.filter(Sub_Division=dc, Status=1).exists():
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': serial.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
        
        
        
# Pre Delivery Inspection


@api_view(['POST'])
def PDI_Login(request):
    response = Response()
    oid = request.POST.get('employ_id')
    opass = request.POST.get('password')
    if InspectingOfficerInfo.objects.filter(officer_employ_id=oid, officer_password=opass, officer_work='PDI').exists():
        abc = InspectingOfficerInfo.objects.get(officer_employ_id=oid, officer_password=opass, officer_work='PDI')
        officer = InspectingOfficerInfoSerializer(abc)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': officer.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def PDI_Inspection_List(request):
    response = Response()
    eid = request.POST.get('employ_id')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if PDI_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=0).exists():
        task = PDI_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=0).distinct('offer_no')
        task_data = PDI_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['POST'])
def PDI_Material_List(request):
    response = Response()
    
    oid = request.POST.get('offer_no')         
    task = PDI_Inspection_Info.objects.filter(offer_no=oid, Is_Active=0)
    if task:
        
        task_data = PDI_Material_InfoSerializer(task, many=True)
            
        response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['POST'])
def PDI_User_Address(request):
    response = Response()
    id = request.POST.get('task_id')
    if PDI_Inspection_Info.objects.filter(id=id).exists():
        task = PDI_Inspection_Info.objects.get(id=id)
        vendor = UserCompanyDataMain.objects.filter(user_id=task.Material.TKCVendor.Vendor.ContactNo)
        vendor = PDI_User_AddressSerializer(vendor, many=True)
        TKC = UserCompanyDataMain.objects.filter(user_id=task.Material.TKCVendor.TKCWoInfo.supplier.ContactNo)
        TKC = PDI_User_AddressSerializer(TKC, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'vendor': vendor.data,
            'Supplier': TKC.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['POST'])
def PDI_Item_Serial(request):
    response = Response()
    offer_no = request.POST.get('offer_no')
    item_code=request.POST.get('item_code')
   
    serial_no_list=[]
    task = offer_material_site_stores.objects.filter(offer_no=offer_no,wo_material__item_code=item_code,Material_Offer_Submit_Approved_Status=1)
    for i in task:        
        serial_no_list.append(i.id)

    serial_data=offer_material_serial_number.objects.filter(offer__in=serial_no_list)    
    serial_nos = []
    serial_batch={}
    sr_list=[]
    
    for each in serial_data: 
        if each.serial_no is not None:
            serial_nos.append(each.serial_no)
        if each.batch_no is not None:
            serial_batch["batch_no."]=each.batch_no
            serial_batch["quantity"]=str(each.batch_qty)
            sr_list.append(serial_batch)
            serial_batch={}
    
    str_list=str(serial_nos)   
    key_list = ["id"]
    n = len(serial_nos)
    res = [{key_list[0]: serial_nos[idx]}
       for idx in range(0, n, 1)] 
   
    if task:        
        
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': res,
            'serial_batch':sr_list
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            'serial_batch':[]

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def PDI_Response(request):
    response = Response()
    id = request.POST.get('offer_no')
    item_code = request.POST.get('item_code')
  
    if PDI_Inspection_Info.objects.filter(offer_no=id,item_code = item_code).exists():

        task = offer_material_site_stores.objects.filter(offer_no=id,wo_material__item_code=item_code)
        pdi_data = PDI_Inspection_Info.objects.get(offer_no=id,item_code = item_code)

        for a in task:
            a.Quantity_Inspected = request.POST.get('quantity_inspected')
            a.Document_Referred = request.POST.get('document_refered')
            a.Test_Witnessed = request.POST.get('test_witness')
            a.Raw_material = request.POST.get('detail_rawmaterial_sample')
            a.Remark = request.POST.get('remark')
            a.Observations = request.POST.get('observation')
            a.Lat = request.POST.get('lat')
            a.Log = request.POST.get('long')
            a.ready_quantity=request.POST.get('ready_quantity')
            a.passed_quantity=request.POST.get('passed_quantity')
            a.failed_quantity=request.POST.get('failed_quantity')
            a.PDI_Complete = 1
            a.PDI = pdi_data            
            a.save()
            

            
            
            PDI_Factory_image(Offer_Material=a, Image=request.FILES['image_1']).save()
            PDI_Factory_image(Offer_Material=a, Image=request.FILES['image_2']).save()
            PDI_Factory_image(Offer_Material=a, Image=request.FILES['image_3']).save()

            # PDI_Factory_image(Offer_Material=a, Image=request.FILES['image_1']).save()
            # PDI_Factory_image(Offer_Material=a, Image=request.FILES['image_2']).save()
            # PDI_Factory_image(Offer_Material=a, Image=request.FILES['image_3']).save()

            

        pdi_data.perform_date = datetime.now().date()
        pdi_data.Status = 1
        pdi_data.save()
        
        if request.POST.get('pdi_report_url') is None or request.POST.get('pdi_report_url') == '':
            pass
        else :
            pdi_report_url = request.POST.get('pdi_report_url')
            def url_ok(pdi_report_url):
                try:
                    proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
                    r = requests.head(pdi_report_url,proxies=proxyDict)
                    return r.status_code == 200
                except:
                    pass
            if url_ok(pdi_report_url)== True:
                pdi_data.pdi_report_url=pdi_report_url
                pdi_data.save()
            else:
                pass
        if request.POST.get('fake_call_remark'):
            pdi_data.fake_call_remark=request.POST.get('fake_call_remark')
            pdi_data.save()
        if request.POST.get('fake_call') == "True":
                pdi_fake=list(PDI_Inspection_Info.objects.filter(offer_no=id).values_list('id', flat=True))
                print(pdi_fake)
                for i in pdi_fake:
                    pdi_propose_fake=PDI_Inspection_Info.objects.get(id=i)
                    pdi_propose_fake.propose_fakecall=True
                    pdi_propose_fake.save()

        response.data = {
                'status': 200,
                'message': 'Record Saved Successfully',
                'data':[],
            }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
                    'status': 201,
                    'message': 'Record Not Found',
                    'data': [],
                }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['POST'])
def PDI_Inspection_Deny(request):
    response = Response()
    eid = request.POST.get('employ_id')
    task_id = request.POST.get('task_id')
    remark = request.POST.get('remark')
    if PDI_Inspection_Info.objects.filter(id=task_id).exists():
        FI = PDI_Inspection_Info.objects.get(id=task_id)
        FI.Is_Active = -1
        FI.deny_reason = remark
        FI.save()
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if PDI_Inspection_Info.objects.filter(officer=abc).exists():
        task = PDI_Inspection_Info.objects.filter(officer=abc, Is_Active=0)
        task_data = PDI_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': 'Not Any Record Found',

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def PDI_Inspection_Record(request):
    response = Response()
    eid = request.POST.get('employ_id')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if PDI_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
        task = PDI_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=1)
        task_data = PDI_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:

        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")        



@api_view(['POST'])
def Tier1_Inspection_Response(request):
    response = Response()
    task_id = request.POST.get('task_id')
    SubTask_id = request.POST.get('SubTask_id')
    list_id = request.POST.get('list_id')
    if Tier1_Inspection_Info.objects.filter(id=task_id).exists():
        if Estimate_Sub_Task.objects.filter(id=SubTask_id).exists():
            if Tier_1_Test_Item_Type_Inspection_List.objects.filter(id=list_id).exists():
                Task = Tier1_Inspection_Info.objects.get(id=task_id)
                SubTask = Estimate_Sub_Task.objects.get(id=SubTask_id)
                Inspection = Tier_1_Test_Item_Type_Inspection_List.objects.get(id=list_id)
                Data = Tier_1_Inspection_Result(Inspection_Info=Task, Sub_Task=SubTask, Inspection=Inspection,
                                                Image=request.FILES['image_1'], Remark=request.POST.get('remark'),
                                                Lat = request.POST.get('lat'), Log = request.POST.get('long'), Short_Coming_Remark = request.POST.get('short_coming_remark'),
                                                Submitted_By=Task.officer.officer_name, Status=0).save()
                response.data = {
                        'status': 200,
                        'message': 'Data Save',
                        'data': [],
                    }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
               
            else:
                response.data = {
                    'status': 201,
                    'message': 'Inspection List Not Found',
                    'data': [],

                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'SubTask Not Found',
                'data': [],

            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:

        response.data = {
            'status': 201,
            'message': 'Task Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


        
# created by shubham tripathi 25/11/2022 for jabalpur discome suggest by yashwant sir 
#  pdi inspection application 
@api_view(['POST'])
def Emb_Measurement_Detail(request):
    response = Response()
    Feeder_id = request.POST.get('feeder_id')
    emb_measurement_data = Emb_Measurement.objects.filter(Feeder_id=Feeder_id, Status=1).first()
    if emb_measurement_data is not None:
        emb_measurement_data = Emb_Measurement.objects.filter(Feeder_id=Feeder_id, Status=1)
        emb_measurement_data = Emb_MeasurementSerializer(emb_measurement_data, many=True)
        response.data = {
            'status': 200,
            'data_status':'ok',
            'message': 'Record Found',
            'data': emb_measurement_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'data_status':'not ok',
            'message': 'Record Not Found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
# ------------------ shubham code end here ------------------------


# -----createcd by shubham tripathi for store representative data ------------------------------------------------------------------------------------------

@api_view(['POST'])
def tier1_inspection_representative(request, format=None):
    if request.method == "POST":
        # user_id = request.data.get('user_id')
        serializers = Tier_1_Inspection_RepresentativeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({ 'status': 200,'message': 'Record Save'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def pdi_inspection_representative(request, format=None):
    if request.method == "POST":
        id = request.POST.get('offer_no')
        serializers = Pdi_Inspection_RepresentativeSerializer(data=request.data)
        if serializers.is_valid():            
                serializers.save()
                return Response({ 'status': 200,'message': 'Record Save'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# -----created by Nikhil Karole for close inspection ------------------------------------------------------------------------------------------


@api_view(['POST'])
def close_pdi_inspection(request, format=None):
    if request.method == "POST":
        id = request.POST.get('offer_no')
        if PDI_Inspection_Info.objects.filter(offer_no=id).exists():
            task = PDI_Inspection_Info.objects.filter(offer_no=id)
            for each in task:
                a= each
                a.Status=1
                a.save()
            return Response({ 'status': 200,'message': 'Record Save'}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def pdi_inspection_representative_list(request, format=None):
    if request.method == "POST":
        id = request.POST.get('task')
        task = Pdi_Inspection_Representive_data.objects.filter(task=id)
        task_data = Pdi_Inspection_RepresentativeSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



# -----createcd by shubham tripathi for store representative data ------------------------------------------------------------------------------------------

@api_view(['POST'])
def tier1_inspection_record(request):
    response = Response()
    eid = request.POST.get('employ_id')
    abc = InspectingOfficerInfo.objects.filter(id=eid).first()
    if abc is not None:
        if Tier1_Inspection_Info.objects.filter(officer=abc.id, Is_Active=0).exists():        
            task = Tier1_Inspection_Info.objects.filter(officer=abc.id, Is_Active=0,Status=1)
            task_data = Tier1_Inspection_InfoSerializer(task, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': task_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Employe id not valid',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

# ------------------ shubham code end here ------------------------

@api_view(['POST'])
def PDI_Inspection_Record(request):
    response = Response()
    eid = request.POST.get('employ_id')
    abc = InspectingOfficerInfo.objects.get(id=eid)
    if PDI_Inspection_Info.objects.filter(officer=abc, Is_Active=0).exists():
        task = PDI_Inspection_Info.objects.filter(officer=abc, Is_Active=0, Status=1)
        task_data = PDI_Inspection_InfoSerializer(task, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': task_data.data,
        }

        
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@csrf_exempt
@api_view(['POST'])
def NablReportData(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = NablDTRReportSerializers(data = pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Data Saved'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type = 'applicaton/json')



@csrf_exempt
def Power_Analyzer(request):
    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = PowerAnalyzerSerializer(data=pythondata)
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data Save'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


# -----createcd by shubham tripathi for store representative data ------------------------------------------------------------------------------------------

@api_view(['GET'])
def api_workorder_list(request):
    response = Response()
    discom = request.GET.get('discom')# add this line for filter record discom wise
    if FqpIntimation.objects.filter(~Q(status=-1),wo__Discom__Discom_Code = discom).exists():
        wo_data = FqpIntimation.objects.filter(~Q(status=-1),wo__Discom__Discom_Code = discom)
        wo_data = FqpIntimation_Serializer(wo_data, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': wo_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
        'status': 201,
        'message': 'Work Order Not Found',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def api_tkcintimation_list(request):
    response = Response()
    discom = request.GET.get('discom')# add this line for filter record discom wise
    if FqpIntimation.objects.filter(~Q(status=-1),wo__Discom__Discom_Code = discom).exists():
        fqp_data = FqpIntimation.objects.filter(~Q(status=-1),wo__Discom__Discom_Code = discom).order_by('-id')
        fqp_data = FqpIntimation_Serializer(fqp_data, many=True)
        response.data = {
            'status': 200,
            'message': 'Record Found',
            'data': fqp_data.data,
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
        'status': 201,
        'message': 'Record Not Found',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    # else:
    #     response.data = {
    #         'status': 201,
    #         'message': 'Work Order Not found',
    #         'data': [],
    #     }
    #     return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def api_tkcintimation_detail(request):
    response = Response()
    wo_id = request.GET.get('wo_id')
    fqpintimation_id = request.GET.get('fqpintimation_id')
    discom = request.GET.get('discom')# add this line for filter record discom wise
    wo_data = FqpIntimation.objects.filter(~Q(status=-1),wo_id=wo_id,wo__Discom__Discom_Code = discom).first()
    if wo_data is not None:
        if FqpIntimation.objects.filter(~Q(status=-1),wo_id=wo_id,id=fqpintimation_id,wo__Discom__Discom_Code = discom).exists():
            fqp_data = FqpIntimation.objects.filter(~Q(status=-1),id=fqpintimation_id,wo_id=wo_id,wo__Discom__Discom_Code = discom)
            fqp_data = FqpIntimation_Serializer(fqp_data, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data':  fqp_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Work Order data not found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['GET'])
def api_fqpmilestone_list(request):
    response = Response()
    wo_id = request.GET.get('wo_id')
    fqpintimation_id = request.GET.get('fqpintimation_id')
    wo_data = FqpIntimation.objects.filter(wo_id=wo_id).first()
    if wo_data is not None:
        if Milestone_Main.objects.filter(~Q(status=-1)).exists():
            ms_data = Milestone_Main.objects.all()
            ms_data = MilestoneMain_Serializer(ms_data, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': ms_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Work Order data not found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['GET'])
def api_fqpmilestone_category_list(request):
    response = Response()
    milestone_id = request.GET.get('milestone_id')
    wo_id = request.GET.get('wo_id')
    fqpintimation_id = request.GET.get('fqpintimation_id')
    # print(milestone_id,"mlid-------------------")
    ms_data = Milestone_Main.objects.filter(id=milestone_id).first()
    if ms_data is not None:
        if Milestone_Main_Category.objects.filter(milestone_main_id=milestone_id).exists():
            msc_data = Milestone_Main_Category.objects.filter(milestone_main_id=milestone_id)
            msc_data = MilestoneMainCategory_Serializer(msc_data, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': msc_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Milestone Not found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['GET'])
def api_fqpmilestone_subcategory_list(request):
    response = Response()
    milestone_id = request.GET.get('milestone_id')
    milestone_category_id = request.GET.get('milestone_category_id')
    msc_data = Milestone_Main_Category.objects.filter(id=milestone_category_id).first()
    if msc_data is not None:
        if Milestone_Main_SubCategory.objects.filter(milestone_main_category_id=milestone_category_id).exists():
            mss_data = Milestone_Main_SubCategory.objects.filter(milestone_main_category_id=milestone_category_id)
            mss_data = MilestoneMainSubcategory_Serializer(mss_data, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': mss_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Milestone category not found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['GET'])
def api_fqpmilestone_subcategory_data_list(request):
    response = Response()
    milestone_id = request.GET.get('milestone_id')
    milestone_category_id = request.GET.get('milestone_category_id')
    milestone_main_subcategory_id = request.GET.get('milestone_main_subcategory_id')
    mss_data = Milestone_Main_SubCategory.objects.filter(id=milestone_main_subcategory_id).first()
    if mss_data is not None:
        if Milestone_Main_SubCategory_Data.objects.filter(milestone_main_subcategory_id=milestone_main_subcategory_id).exists():
            mss_list_data = Milestone_Main_SubCategory_Data.objects.filter(milestone_main_subcategory_id=milestone_main_subcategory_id)
            mss_list_data = MilestoneMainSubcategory_Data_Serializer(mss_list_data, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': mss_list_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Milestone subcategory not found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

@api_view(['POST'])
def api_fqpintimation_observation_info_detail(request):
    serializer = FqpIntimation_Observation_Info_Serializer(data=request.data)
    if serializer.is_valid():
        observation_info = serializer.save()
        serializer_data = serializer.data
        serializer_data['id'] = observation_info.id
        response_data = {
            'message': 'Your fqpintimation observation data successfully saved',
            'status': status.HTTP_200_OK,
            'observation_data': serializer_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_fqpintimation_observation_officer_detail(request):
    serializer = FqpIntimation_Officer_Info_Serializer(data=request.data)
    if serializer.is_valid():
        officer_observation_info = serializer.save()
        serializer_data = serializer.data
        serializer_data['id'] = officer_observation_info.id
        response_data = {
            'message': 'Your fqpintimation observation officers data successfully saved',
            'status': status.HTTP_200_OK,
            'officer_observation_data': serializer_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_fqpintimation_observation_create_data(request):
    serializer = FqpIntimation_Observation_Close_Serializer(data=request.data)
    if serializer.is_valid():
        observation_close_info = serializer.save()
        serializer_data = serializer.data
        serializer_data['id'] = observation_close_info.id
        response_data = {
            'message': 'Your fqpintimation observation close data successfully saved',
            'status': status.HTTP_200_OK,
            'officer_observation_data': serializer_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_fqpintimation_officer_list(request):
    response = Response()
    fqpintimation_id = request.GET.get('fqpintimation_id')
    fqi_data = FqpIntimation.objects.filter(id=fqpintimation_id).first()
    if fqi_data is not None:
        if FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id).exists():
            fqp_data = FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id)
            fqp_data = FqpIntimation_Officer_Info_Serializer(fqp_data, many=True)
            response.data = {
                'status': 200,
                'message': 'Record Found',
                'data': fqp_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 201,
            'message': 'Record Not Found',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 201,
            'message': 'Fqp intimation Not found',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

# ------------------ shubham code end here ------------------------


#----------------------------------START OF VENDOR MATERIAL AND SPECIFICATION API BY RAVINDRA---------------------#

@api_view(['GET'])
def get_vendor(request):
    response = Response()
    data = User_Registration.objects.filter(User_type='VENDOR',Complete_Details='1',cgm_approval=1,digital_cert_upload=1,blacklisted=0)

    queryset_serializer = vendor_master_serial(data, many=True)
    sss = queryset_serializer.data
    if len(sss) == 0:
        response.data = {
            'status': 201,
            'message': 'Record not Found',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
            'status': 200,
            'message': 'Succesful',
            'data': queryset_serializer.data,

        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['GET'])
def get_vendor_material(request, id):
    response = Response()
    material = User_Registration.objects.get(User_Id=id)
    data = Vendor_Material_Details.objects.filter(user_id=material)
    serial = vendor_material_serial(data, many=True)
    # if Vendor_Material_Details.objects.filter(user_id=material).exists():
    response.data = {
        'status': 200,
        'message': 'Record Found',
        'material_specification': serial.data,
    }
    return HttpResponse(json.dumps(response.data), content_type="application/json")
    # else:
    #     response.data = {
    #         'status': 201,
    #         'message': 'Record Not Found',
    #         'material_specification': [],
    #     }
    #     return HttpResponse(json.dumps(response.data), content_type="application/json")
    
    
@api_view(['GET'])
def get_vendor_material_2(request, id):
    response = Response()
    # material = User_Registration.objects.get(User_Id=id)
    data = Vendor_Material_Details.objects.filter(id=id)
    serial = vendor_material_serial_2(data, many=True)
   
    response.data = {
        'status': 200,
        'message': 'Record Found',
        'material_specification': serial.data,
    }
    return HttpResponse(json.dumps(response.data), content_type="application/json")
    # else:
    #     response.data = {
    #         'status': 201,
    #         'message': 'Record Not Found',
    #         'material_specification': [],
    #     }
    #     return HttpResponse(json.dumps(response.data), content_type="application/json")
    
#----------------------------------END OF VENDOR MATERIAL AND SPECIFICATION BY RAVINDRA---------------------------#


#----------------------------------START OF FQP API BY RAVINDRA---------------------------#


class api_check_fqpintimation_status_post(APIView):
    try:
        def post(self, request):
            feederId = request.data['feeder_id']
            # user_data_check = fqp_check_status_save.objects.filter( feeder_id = feederId )
            # user_data_check = list(fqp_check_status.objects.filter( feeder_id = feederId ).values_list('id', flat=True)) #isme m khud se save krta hu
            # data=fqp_check_status.objects.get(id=user_data_check[0])
            try:
                user_data_check = fqp_check_status.objects.get( feeder_id = feederId )
                print(user_data_check)
                
                
                # if len(user_data_check) != 0:
                #     # serializer = fqp_check_status_save_serializer(data = request.data)
                #     serializer = fqp_check_status_save_serializer(data = request.data)
                    
                
                #     if serializer.is_valid():
                #         serializer.save()
                        
                        # queryset_1 = fqp_check_status_save.objects.filter(feeder_id=feederId)
                        # contractor_serializer_1 = fqp_check_status_save_serializer(queryset_1, many = False)
                
                return Response({
                        'status' : True,
                        'message' : 'FQP intimation found of this task',
                        'feeder_id':user_data_check.feeder_id ,
                        'feeder_response':user_data_check.is_accepted,
                        # 'fqp task1': contractor_serializer_1.data,
                        
                        })
            # return HttpResponse(json.dumps(Response), content_type="application/json")
            except:
                return Response({
                            'status' : False,
                            'message' : 'FQP intimation not found of this task',
                            'feeder_response': [],
                            
                            })
                

    except Exception as e:
            print(e)
            
            
   
class api_check_fqpintimation_status_get(APIView):
    
    def get(self, request):
        queryset =fqp_check_status.objects.all()
        if queryset is not None:
            if request.GET.get('search'):
                search = request.GET.get('search')
                queryset = queryset.filter(
                    Q(feeder_id__iexact = search) 
                    # Q(feeder_response__icontains = search) 
                )

            serializer = fqp_check_status_serializer(queryset, many =True)
        
            return Response({
                'status' : True,
                'message' : 'FQP intimation found of this task',
                'data': serializer.data
            })
            
        else:
            return Response({
                'status' : True,
                'message' : 'FQP intimation not found of this task',
                # 'data': serializer.data
            })
            
#----------------------------------END OF FQP API BY RAVINDRA---------------------------#
    
class ListSupport(APIView):
    def get(self,request,format=None):
        response = Response()
        response.data = {
            'status': 200,
            'message': 'Record found',
            'list':{'whatsapp':'+917225812108',
              'contact':'+917225812108',
              'version':'1'},
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    
    
@api_view(['GET'])
def package_master_data(request):
    response = Response()      
    works_data = works_master.objects.all()
    wo_serializer_data = works_master_serializer(works_data,many=True)
    if wo_serializer_data is not None:
        response.data = {
            'status' : 200,
            'mgs' : 'Record Found',
            'wo_data' : wo_serializer_data.data
            }
    else:
        response.data = {
        'status' : 200,
        'mgs' : 'Record Found',
        'wo_data' : []
        } 
    return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def all_contractors_data(request):
    response = Response()      
    user_data = UserCompanyDataMain.objects.filter(user_id_id__User_type = "TKC", user_id_id__cgm_approval = 1)
    wo_serializer_data = UserCompanyDataMain_serializer(user_data, many=True)
    if wo_serializer_data is not None:
        response.data = {
            'status' : 200,
            'mgs' : 'Record Found',
            'wo_data' : wo_serializer_data.data
            }
    else:
        response.data = {
        'status' : 200,
        'mgs' : 'Record Found',
        'wo_data' : []
        } 
    return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def work_order_data(request):
    response = Response()   
    
    wo_data = TKCWoInfo.objects.all()
    
    package_serialize_data = work_order_Serializer(wo_data,many=True)
    # print("package_serialize_data.data--->",len(package_serialize_data.data))
    response.data = {
        'status' : 200,
        'mgs' : 'Record Found',
        'wo_data' : package_serialize_data.data,             
        
    }
    return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['GET'])
def supply_testing_data(request):    
    wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,Wo_Digital_Upload_Status=1)          
    value_data = {} 
    value_data["work_order_data"] = []
    for j in wo_data:
        dict_data = {}
        dict_data["wo_no"] = j.Contract_Number 
        dict_data["TKC"] = j.supplier.CompanyName_E
        dict_data["contract_no"] = j.Contract_Number        
        dict_data["TKC_id"] = j.supplier.User_Id
        dict_data["Discom"] = j.zone         
        dict_data["package_name"] = j.pakage.package_name  
        
       
        material_dict = {'Power Transformer' : [1], "Distribution Transformer" : [2], 'Cables' : [18], "PCC Poles" : [31], 
                         "Conductor" : [14, 15,16, 56], "Capacitor Bank" : [21]}
        
        for k, v in material_dict.items():
            if len(v) == 1:
                for var in v:
                    code_list_cz = []
                    code_list_wz = []
                    code_list_ez = []
                    category_item_code = Vendor_Material_Specification_Master.objects.filter(Material = var)
                    
                    # dict_data["offer_count"] = offer_material_site_stores.objects.filter(wo_material=var.wo_material.material_name, Material_Offer_Submit_Approved_Status=1).distinct("offer_no").count()
                    for var1 in category_item_code:
                        code_list_cz.append(var1.Material_Item_Code)
                        code_list_wz.append(var1.Material_Item_Code_WZ)
                        code_list_ez.append(var1.Material_Item_Code_EZ)
                    
            elif len(v)>1:
                intial = 0
                code_list_cz = []
                code_list_wz = []
                code_list_ez = []
                while intial<len(v):
                    
                    category_item_code = Vendor_Material_Specification_Master.objects.filter(Material = v[intial])
                    intial = intial + 1
                    
                    # dict_data["offer_count"] = offer_material_site_stores.objects.filter(wo_material=var.wo_material.material_name, Material_Offer_Submit_Approved_Status=1).distinct("offer_no").count()
                    for var1 in category_item_code:
                        code_list_cz.append(var1.Material_Item_Code)
                        code_list_wz.append(var1.Material_Item_Code_WZ)
                        code_list_ez.append(var1.Material_Item_Code_EZ)
                
            
                    
                
            material_data = {}
            if j.zone == 'CZ':
                boq_obj_sum = tkc_wo_items_boq.objects.filter(wo=j.id,item_code__in = code_list_cz).aggregate(total=Sum('total_order_qty'))['total']
                data = tkc_wo_items_boq.objects.filter(wo=j.id, item_code__in = code_list_cz)
            elif j.zone == 'WZ':
                boq_obj_sum = tkc_wo_items_boq.objects.filter(wo=j.id,item_code__in = code_list_wz).aggregate(total=Sum('total_order_qty'))['total']
                data = tkc_wo_items_boq.objects.filter(wo=j.id, item_code__in = code_list_wz)
            elif j.zone == 'EZ':
                boq_obj_sum = tkc_wo_items_boq.objects.filter(wo=j.id,item_code__in = code_list_ez).aggregate(total=Sum('total_order_qty'))['total']
                data = tkc_wo_items_boq.objects.filter(wo=j.id, item_code__in = code_list_ez)
            material_data["material boq quantity"] = boq_obj_sum
            
            
            id_list = []  
            for i in data:
                id_list.append(i.id)    
            offer_qty_count = offer_material_site_stores.objects.filter(wo_material__in=id_list, Material_Offer_Submit_Approved_Status=1).aggregate(total=Sum('quantity'))['total']
            mrc_qty_count = offer_material_site_stores.objects.filter(wo_material__in=id_list, Material_Offer_Submit_Approved_Status=1,tkc_mrc_initiate = 1).aggregate(total=Sum('quantity'))['total']

            material_data["material offered quantity"] = offer_qty_count
            material_data["material mrc quantity"] = mrc_qty_count
            dict_data[k]  = material_data
                
        value_data["work_order_data"].append(copy.deepcopy(dict_data))
       
    return Response(value_data)


@api_view(['GET'])
def invoice_data(request):    
    wo_data = TKCWoInfo.objects.filter(Wo_Approved_Status=1,Wo_Digital_Upload_Status=1)      
    value_data = {} 
    value_data["invoice_data"] = []
    for j in wo_data:
        dict_data = {}
        dict_data["wo_no"] = j.Contract_Number 
        dict_data["TKC"] = j.supplier.CompanyName_E
        dict_data["contract_no"] = j.Contract_Number        
        dict_data["TKC_id"] = j.supplier.User_Id
        dict_data["Discom"] = j.zone         
        dict_data["package_name"] = j.pakage.package_name  
        dict_data["erp_wo_no"] = j.erp_wo_no
        data = Invoice.objects.filter(order_type='WorkOrder', work_order=j)
        print(data)
        
        dict_data["No. of Invoice"] = Invoice.objects.filter(order_type='WorkOrder', work_order=j).count()
        dict_data["Amount"] = Invoice.objects.filter(order_type='WorkOrder', work_order=j).aggregate(total=Sum('total_invoice_amount'))['total']
        dict_data["No. of Invoice Rejected by Discom"] = Invoice.objects.filter(order_type='WorkOrder', work_order=j, status=2).count() 
        dict_data["Mobilization Advance"] = Invoice.objects.filter(order_type='WorkOrder', work_order=j, invoicetype__in = [3,4]).aggregate(total=Sum('total_invoice_amount'))['total']   
        dict_data["Material Advance"] = Invoice.objects.filter(order_type='WorkOrder', work_order=j,  invoicetype = 3).aggregate(total=Sum('total_invoice_amount'))['total']   
        dict_data["RA Bill"] = Invoice.objects.filter(order_type='WorkOrder', work_order=j, invoicetype = 8).aggregate(total=Sum('total_invoice_amount'))['total']   

               
        value_data["invoice_data"].append(copy.deepcopy(dict_data))
        
    return Response(value_data)



#-------------- api new fqpintimation data added by shubhamt tripathi-=-------date 11-7-2023---


@api_view(['POST'])
def api_new_fqpintimation_wo_list(request):
    response = Response()
    officer_employ_id = request.POST.get('officer_employ_id')
    if officer_employ_id =="":
        response.data = {
        'status': 401,
        'message': 'Officer employee id is required',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")    
    else:
        officer = Officer.objects.filter(is_active=True,employ_id=officer_employ_id).first()
        if officer is not None and (officer.role.Role_Name == "DGM_STC" or officer.role.Role_Name == "DGM_ONM" or officer.role.Role_Name == "GM(CIRCLE)" or officer.role.Role_Name == "JE" or officer.role.Role_Name == "PMA" or officer.role.Role_Name == "WO_APPROVER" or officer.role.Role_Name == "WO_CREATER" or officer.role.Role_Name == "GM(CIRCLE)"):
            wo_data=""
            if officer.Discom is not None and officer.Region is None and officer.Circle is None and officer.Division is None and officer.DC_Zone_id is None:
                wo_data = New_FqpIntimation.objects.filter(intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id).distinct('wo_task__wo__id')

            elif officer.Discom is not None and officer.Region is not None and officer.Circle is None and officer.Division is None and officer.DC_Zone_id is None:
                wo_data = New_FqpIntimation.objects.filter(intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id).distinct('wo_task__wo__id')

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is None and officer.DC_Zone_id is None:
                if officer.role.Role_Name == "DGM_STC":
                    # wo_data = New_FqpIntimation.objects.filter(intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wotask_milestone__milestone__id__in=[2,3,6]).distinct('wo_task__wo__id')
                    wo_data = New_FqpIntimation.objects.filter(wo_task_id__wo_id__pakage_id__in=[7,8,9,10],intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).distinct('wo_task__wo__id')
                else:
                    wo_data = New_FqpIntimation.objects.filter(intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).distinct('wo_task__wo__id')
                
            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None and officer.DC_Zone_id is None:
                if officer.role.Role_Name == "DGM_ONM":
                    # wo_data = New_FqpIntimation.objects.filter(intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wotask_milestone__milestone__id__in=[1,4,5]).distinct('wo_task__wo__id')
                    wo_data = New_FqpIntimation.objects.filter(wo_task_id__wo_id__pakage_id__in=[2,3,4,5,6],intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id).distinct('wo_task__wo__id')       
                else:
                    wo_data = New_FqpIntimation.objects.filter(intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id).distinct('wo_task__wo__id')       

            elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None and officer.DC_Zone_id is not None:
                wo_data = New_FqpIntimation.objects.filter(intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wo_task__distribution_center_id=officer.DC_Zone_id).distinct('wo_task__wo__id')
            else:
                message="Something is wrong"
                wo_data=""

            if wo_data is not None:
                wo_data = New_FqpIntimation_Workorder_List_Serializer(wo_data, many=True)
                message="Work order list"
                wo_data =wo_data.data
            else:
                message="Work order not Found"
                wo_data=""
            response.data = {
                'status': 200,
                'message': message,
                'data': wo_data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 401,
            'message': 'Please login with right credentials or provide valid officer employee id',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def api_new_fqpintimation_task_list(request):
    response = Response()
    wo_id = request.POST.get('wo_id')# add this line for filter record discom wise
    officer_employ_id = request.POST.get('officer_employ_id')# add this line for filter record discom wise
    wo_task_data=""
    if officer_employ_id =="":
        response.data = {
        'status': 401,
        'message': 'Officer employee id is required',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        officer = Officer.objects.filter(is_active=True,employ_id=officer_employ_id).first()
        if officer is not None and (officer.role.Role_Name == "DGM_STC" or officer.role.Role_Name == "DGM_ONM" or officer.role.Role_Name == "GM(CIRCLE)" or officer.role.Role_Name == "JE" or officer.role.Role_Name == "PMA" or officer.role.Role_Name == "WO_APPROVER" or officer.role.Role_Name == "WO_CREATER" or officer.role.Role_Name == "GM(CIRCLE)"):
            wo_data = TKCWoInfo.objects.filter(id=wo_id).first()
            if wo_id is None:
                message = "Work order id is required"              
            elif wo_data is not None:
                if officer.Discom is not None and officer.Region is None and officer.Circle is None and officer.Division is None and officer.DC_Zone_id is None:
                    wo_task_data = New_FqpIntimation.objects.filter(wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id).order_by('-id')

                elif officer.Discom is not None and officer.Region is not None and officer.Circle is None and officer.Division is None and officer.DC_Zone_id is None:
                    wo_task_data = New_FqpIntimation.objects.filter(wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id).order_by('-id')

                elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is None and officer.DC_Zone_id is None:
                    if officer.role.Role_Name == "DGM_STC":
                        # wo_task_data = New_FqpIntimation.objects.filter(wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wotask_milestone__milestone__id__in=[2,3,6]).order_by('-id')
                        wo_task_data = New_FqpIntimation.objects.filter(wo_task_id__wo_id__pakage_id__in=[7,8,9,10],wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).order_by('-id')
                    else:
                        wo_task_data = New_FqpIntimation.objects.filter(wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).order_by('-id')

                elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None and officer.DC_Zone_id is None:
                    if officer.role.Role_Name == "DGM_ONM":
                        # wo_task_data = New_FqpIntimation.objects.filter(wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wotask_milestone__milestone__id__in=[1,4,5]).order_by('-id')
                        wo_task_data = New_FqpIntimation.objects.filter(wo_task_id__wo_id__pakage_id__in=[2,3,4,5,6],wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id).order_by('-id')
                    else:
                        wo_task_data = New_FqpIntimation.objects.filter(wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id).order_by('-id')                        
                elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None and officer.DC_Zone_id is not None:
                    wo_task_data = New_FqpIntimation.objects.filter(wo_task__wo_id=wo_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wo_task__distribution_center_id=officer.DC_Zone_id).order_by('-id')

                else:
                    message="Something is wrong"
                    wo_task_data=""

                if wo_task_data is not None and wo_task_data != "":
                    wo_task_data = New_FqpIntimation_Task_List_Serializer(wo_task_data, many=True)
                    message="Work order task list"
                    wo_task_data =wo_task_data.data
                else:
                    message="This work order not have any task"
                    wo_task_data=""

            else:
                message="Work order not found"
                wo_task_data=""

            response.data = {
                'status': 200,
                'message': message,
                'wo_task_list': wo_task_data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")

        else:
            response.data = {
            'status': 401,
            'message': 'Please login with right credentials or provide valid officer employee id',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")




@api_view(['POST'])
def api_new_fqpintimation_list(request):
    response = Response()
    wo_id = request.POST.get('wo_id')
    wo_task_id = request.POST.get('wo_task_id')
    officer_employ_id = request.POST.get('officer_employ_id')
    if officer_employ_id =="":
        response.data = {
        'status': 401,
        'message': 'Officer employee id is required',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        officer = Officer.objects.filter(is_active=True,employ_id=officer_employ_id).first()
        if officer is not None and (officer.role.Role_Name == "DGM_STC" or officer.role.Role_Name == "DGM_ONM" or officer.role.Role_Name == "GM(CIRCLE)" or officer.role.Role_Name == "JE" or officer.role.Role_Name == "PMA" or officer.role.Role_Name == "WO_APPROVER" or officer.role.Role_Name == "WO_CREATER" or officer.role.Role_Name == "GM(CIRCLE)"):
            fqp_intimation_data = ""
            wo_task_data = Wo_Order_Task.objects.filter(id=wo_task_id,wo_id=wo_id,region_id=officer.Region_id).first()
            if wo_id is None:
                message = 'Work order id is requiered'
            elif wo_task_id is None:
                message = 'Work order task id is requiered'
            elif wo_task_data is not None:
                if officer.Discom is not None and officer.Region is None and officer.Circle is None and officer.Division is None and officer.DC_Zone_id is None:
                    fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id).order_by('-id')

                elif officer.Discom is not None and officer.Region is not None and officer.Circle is None and officer.Division is None and officer.DC_Zone_id is None:
                    fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id).order_by('-id')

                elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is None and officer.DC_Zone_id is None:
                    if officer.role.Role_Name == "DGM_STC":
                        fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id__wo_id__pakage_id__in=[7,8,9,10],wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).order_by('-id')
                        # fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wotask_milestone__milestone__id__in=[2,3,6]).order_by('-id')
                    else:
                        fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id).order_by('-id')                        

                elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None and officer.DC_Zone_id is None:
                    if officer.role.Role_Name == "DGM_ONM":
                        fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id__wo_id__pakage_id__in=[2,3,4,5,6],wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id).order_by('-id')
                        # fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wotask_milestone__milestone__id__in=[1,4,5]).order_by('-id')
                    else:
                        fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id).order_by('-id')

                elif officer.Discom_id is not None and officer.Region_id is not None and officer.Circle_id is not None and officer.Division_id is not None and officer.DC_Zone_id is not None:
                    fqp_intimation_data = New_FqpIntimation.objects.filter(~Q(status=-1),wo_task_id=wo_task_data.id,intimation_status=0,wo_task__wo__Discom_id=officer.Discom_id,wo_task__region_id=officer.Region_id,wo_task__circle_id=officer.Circle_id,wo_task__division_id=officer.Division_id,wo_task__distribution_center_id=officer.DC_Zone_id).order_by('-id')

                else:
                    message="Something is wrong"
                    fqp_intimation_data=""
            
                if fqp_intimation_data is not None and fqp_intimation_data != "":
                    fqp_intimation_data = New_FqpIntimation_List_Serializer(fqp_intimation_data, many=True)
                    
                    message = 'This is intimation list of task'
                    response.data = {
                    'status': 200,
                    'message': message,
                    'fqp_intimation_list': fqp_intimation_data.data,
                    }
                    return HttpResponse(json.dumps(response.data), content_type="application/json")
                else:
                    fqp_intimation_data = ""
                    message = 'No any intimation found of this task'
            else:
                fqp_intimation_data = ""
                message = 'work order and task record not found'

            response.data = {
            'status': 200,
            'message': message,
            'fqp_intimation_list': fqp_intimation_data.data,
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 401,
            'message': 'Please login with right credentials or provide valid officer employee id',
            'fqp_intimation_list': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")





@api_view(['POST'])
def api_newfqpintimation_milestone_category_list(request):
    response = Response()
    fqpintimation_id = request.POST.get('fqpintimation_id')
    officer_employ_id = request.POST.get('officer_employ_id')
    if officer_employ_id =="":
        response.data = {
        'status': 401,
        'message': 'Officer employee id is required',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")    
    else:
        officer = Officer.objects.filter(is_active=True,employ_id=officer_employ_id).first()
        if officer is not None:
            fqpin_data = New_FqpIntimation.objects.filter(id=fqpintimation_id).first()
            if fqpin_data is not None:
                if New_FqpIntimation_milestone_category.objects.filter(fqpintimation_id=fqpintimation_id).exists():
                    fqp_msc_data = New_FqpIntimation_milestone_category.objects.filter(fqpintimation_id=fqpintimation_id)
                    fqp_msc_data = New_FqpIntimation_Milestone_Category_Serializer(fqp_msc_data, many=True)
                    response.data = {
                        'status': 200,
                        'message': 'Record Found',
                        'data': fqp_msc_data.data,
                    }
                    return HttpResponse(json.dumps(response.data), content_type="application/json")
                else:
                    response.data = {
                        'status': 200,
                        'message': 'Fqp intimation Milestone category not found',
                        'data': [],
                    }
                    return HttpResponse(json.dumps(response.data), content_type="application/json")            

            else:
                response.data = {
                    'status': 201,
                    'message': 'Please provide valid fqp intimation id',
                    'data': [],
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 401,
            'message': 'Please login with right credentials or provide valid officer employee id',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['POST'])
def api_newfqpintimation_milestone_subcategory_list(request):
    response = Response()
    # milestone_id = request.GET.get('milestone_id')
    milestone_category_id = request.POST.get('milestone_category_id')
    officer_employ_id = request.POST.get('officer_employ_id')
    if officer_employ_id =="":
        response.data = {
        'status': 401,
        'message': 'Officer employee id is required',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        officer = Officer.objects.filter(is_active=True,employ_id=officer_employ_id).first()
        if officer is not None:
            msc_data = Milestone_Main_Category.objects.filter(id=milestone_category_id).first()
            if msc_data is not None:
                if Milestone_Main_SubCategory.objects.filter(milestone_main_category_id=milestone_category_id).exists():
                    mss_data = Milestone_Main_SubCategory.objects.filter(milestone_main_category_id=milestone_category_id)
                    mss_data = New_FqpIntimation_MilestoneMainSubcategory_Serializer(mss_data, many=True)
                    response.data = {
                        'status': 200,
                        'message': 'Record Found',
                        'data': mss_data.data,
                    }
                    return HttpResponse(json.dumps(response.data), content_type="application/json")
                else:
                    response.data = {
                    'status': 201,
                    'message': 'Record Not Found',
                    'data': [],
                    }
                    return HttpResponse(json.dumps(response.data), content_type="application/json")
            else:
                response.data = {
                    'status': 201,
                    'message': 'Milestone category not found',
                    'data': [],
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
            'status': 401,
            'message': 'Please login with right credentials or provide valid officer employee id',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")



@api_view(['POST'])
def api_newfqpintimation_milestone_subcategory_data_list(request):
    response = Response()
    # milestone_id = request.POST.get('milestone_id')
    milestone_category_id = request.POST.get('milestone_category_id')
    milestone_main_subcategory_id = request.POST.get('milestone_main_subcategory_id')
    officer_employ_id = request.POST.get('officer_employ_id')
    if officer_employ_id =="":
        response.data = {
        'status': 401,
        'message': 'Officer employee id is required',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        officer = Officer.objects.filter(is_active=True,employ_id=officer_employ_id).first()
        if officer is not None:
            mss_data = Milestone_Main_SubCategory.objects.filter(id=milestone_main_subcategory_id).first()
            if mss_data is not None:
                if Milestone_Main_SubCategory_Data.objects.filter(milestone_main_subcategory_id=milestone_main_subcategory_id).exists():
                    mss_list_data = Milestone_Main_SubCategory_Data.objects.filter(milestone_main_subcategory_id=milestone_main_subcategory_id)
                    mss_list_data = New_FqpIntimation_MilestoneMainSubcategory_Data_Serializer(mss_list_data, many=True)
                    response.data = {
                        'status': 200,
                        'message': 'Record Found',
                        'data': mss_list_data.data,
                    }
                    return HttpResponse(json.dumps(response.data), content_type="application/json")
                else:
                    response.data = {
                    'status': 201,
                    'message': 'Record Not Found',
                    'data': [],
                    }
                    return HttpResponse(json.dumps(response.data), content_type="application/json")
            else:
                response.data = {
                    'status': 201,
                    'message': 'Milestone subcategory not found',
                    'data': [],
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")

        else:
            response.data = {
            'status': 401,
            'message': 'Please login with right credentials or provide valid officer employee id',
            'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['GET'])
def api_newfqpintimation_emb_measurment_status(request):
    response = Response()
    gis_feeder_id = request.GET.get('gis_feeder_id')
    if gis_feeder_id == "" or gis_feeder_id is None:
        response.data = {
            'status': 201,
            'message': 'Gis feeder id / task id is required',
            'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        wo_task_data = Wo_Order_Task.objects.filter(gis_feeder_id=gis_feeder_id).first()
        if wo_task_data is not None:
            if New_FqpIntimation.objects.filter(wo_task_id=wo_task_data.id).exists():
                task_intimation_data = Wo_Order_Task.objects.filter(id=wo_task_data.id)
                task_intimation_data = Emb_Measurement_New_Fqpintimation_Serializer(task_intimation_data, many=True)
                response.data = {
                    'status': 200,
                    'message': 'Record Found',
                    'data': task_intimation_data.data,
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
            else:
                response.data = {
                'status': 201,
                'message': 'No any intimation found',
                'data': [],
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Task data not found',
                'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")


@api_view(['POST'])
def api_newfqpintimation_observation_info_detail_saved(request):
    serializer = New_FqpIntimation_Observation_Serializer(data=request.data)
    if serializer.is_valid():
        observation_info = serializer.save()
        serializer_data = serializer.data
        serializer_data['id'] = observation_info.id
        response_data = {
            'message': 'Your fqpintimation observation data successfully saved',
            'status': status.HTTP_200_OK,
            'observation_detail': serializer_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_new_fqpintimation_observation_officer_detail(request):
    serializer = New_FqpIntimation_Officer_Info_Serializer(data=request.data)
    if serializer.is_valid():
        officer_observation_info = serializer.save()
        serializer_data = serializer.data
        serializer_data['id'] = officer_observation_info.id
        response_data = {
            'message': 'Your fqpintimation observation officers data successfully saved',
            'status': status.HTTP_200_OK,
            'observation_officer_detail': serializer_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_new_fqpintimation_observation_close_data(request):
    serializer = New_FqpIntimation_Observation_Close_Serializer(data=request.data)
    if serializer.is_valid():
        observation_close_info = serializer.save()
        serializer_data = serializer.data
        serializer_data['id'] = observation_close_info.id
        response_data = {
            'message': 'Your fqpintimation observation close data successfully saved',
            'status': status.HTTP_200_OK,
            'officer_observation_close_data': serializer_data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_new_fqpintimation_officer_list(request):
    response = Response()
    fqpintimation_id = request.GET.get('fqpintimation_id')
    officer_employ_id = request.GET.get('officer_employ_id')
    officer = Officer.objects.filter(is_active=True,employ_id=officer_employ_id).first()
    if officer is not None:
        fqi_data = New_FqpIntimation.objects.filter(id=fqpintimation_id).first()
        if fqi_data is not None:
            if New_FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id).exists():
                fqp_data = New_FqpIntimation_Officer_Info.objects.filter(fqpintimation_id=fqpintimation_id)
                fqp_data = New_FqpIntimation_Officer_Info_List_Serializer(fqp_data, many=True)
                response.data = {
                    'status': 200,
                    'message': 'Record Found',
                    'data': fqp_data.data,
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
            else:
                response.data = {
                'status': 201,
                'message': 'Record Not Found',
                'data': [],
                }
                return HttpResponse(json.dumps(response.data), content_type="application/json")
        else:
            response.data = {
                'status': 201,
                'message': 'Fqp intimation Not found',
                'data': [],
            }
            return HttpResponse(json.dumps(response.data), content_type="application/json")
    else:
        response.data = {
        'status': 401,
        'message': 'Please login with right credentials or provide valid officer employee id',
        'data': [],
        }
        return HttpResponse(json.dumps(response.data), content_type="application/json")

# code by PD MISHRA
class getInspectingData(APIView):
    def get(self, request,pk):
        queryset =InspectingOfficerInfo.objects.get(id=pk)
        print("#####",queryset)
        
        serializer = Inspecting_officer(queryset)
        return Response({
            'status' : True,
            'message' : 'data',
            'data': serializer.data
        })    


