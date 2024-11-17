# This file is intended for defining payload bodies for APIs of all Discoms. 
# The payload for each API should be categorized under the appropriate Discom.


'''
API_endpoint:"http://devebs.mpwin.co.in:8040/webservices/rest/qc_portal_register_vendor/register_vendor/"
DISCOM_NAME:'Indore'
ZONE:WZ
API FOR MODULE:TKC
API FOR ENVIRONMENT:SIT/TEST
'''

payload_register_vendor_wz_sit={
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
            "P_PORTAL_VENDOR_NUMBER": "",
            "P_VENDOR_NAME": "",
            "P_VENDOR_TYPE": "",
            "P_ENABLED_FLAG": "Y",
            "P_PAN_NUMBER": "",
            "P_SITES": {
                "P_SITES_ITEM": [
                    {
                        "SITE_CODE": "",
                        "CURRENCY": "",
                        "ADDRESS1": "",
                        "ADDRESS2": "",
                        "ADDRESS3": "",
                        "CITY": "",
                        "STATE": "",
                        "PIN": "",
                        "EMAIL_ADDRESS": "",
                        "ENABLED_FLAG": "Y",
                        "BANK": "",
                        "IFSC_CODE": "",
                        "BANK_BRANCH": "",
                        "BRANCH_ADDRESS": "",
                        "ACCOUNT_NUMBER": "",
                        "GST_NUMBER": ""
                    }
                ]
            }
        }
    }
}

##########################################################################################################




