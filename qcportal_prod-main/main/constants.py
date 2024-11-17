#Defining Constants here , which will be using through out the project.

#URLS 
register_vendor_sit_wz = "http://devebs.mpwin.co.in:8040/webservices/rest/qc_portal_register_vendor/register_vendor/"
register_vendor_sit_cz = "http://nprodap1.mpcz.in:8004/webservices/rest/qc_vendor_registration/register_vendor/"
register_vendor_prod_wz = 'https://prodserv.mpwin.co.in:8070/webservices/rest/QC_PORTAL_REGISTER_VENDOR/register_vendor/'
tkc_po_header_api="http://ebssitapp1.mpezerp.com:8001/webservices/rest/xxtkc_turnkey_po_hdr_pkg/get_tkc_po_hdr_details/"


#headers
headers = {'Content-type': 'application/json'}


#User_Type
user_type_vendor='VENDOR'
# user_type_contractor=''

#Authorization for WZ API (SIT)
Username = 'QC_EBS_USER';
Password = "Qc_ebs@23";

#payloads 
#payload for register_vendor_API for Indore(WZ) discomm.
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
            "P_PORTAL_VENDOR_NUMBER": "13333564546",
            "P_VENDOR_NAME": "POIJDBC INDUSTRIES PRIVATE LIMITED",
            "P_VENDOR_TYPE": "VENDOR",
            "P_ENABLED_FLAG": "Y",
            "P_PAN_NUMBER": "ABJCA697GG",
            "P_SITES": {
                "P_SITES_ITEM": [
                    {
                        "SITE_CODE": "Indore",
                        "CURRENCY": "INR",
                        "ADDRESS1": "27-28A, SECTOR-F",
                        "ADDRESS2": "SANWER ROAD INDUSTRIAL AREA ",
                        "ADDRESS3": "",
                        "CITY": "Indore",
                        "STATE": "Madhya Pradesh",
                        "PIN": "452015",
                        "EMAIL_ADDRESS": "devendraparihar@hotmail.com",
                        "ENABLED_FLAG": "Y",
                        "BANK": "",
                        "IFSC_CODE": "",
                        "BANK_BRANCH": "",
                        "BRANCH_ADDRESS": "",
                        "ACCOUNT_NUMBER": "",
                        "GST_NUMBER": "23AAJCA6975G1ZH"
                    }
                ]
            }
        }
    }
}










