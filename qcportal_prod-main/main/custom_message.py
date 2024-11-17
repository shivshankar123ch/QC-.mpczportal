import datetime

header = {"User-Agent": "Opera/9.80 (X11; Linux x86_64; U; de) Presto/2.2.15 Version/10.00"}
proxyDict = {"http": "proxy.mpcz.in:8080", "https": "proxy.mpcz.in:8080"}
api_url = "https://sms.mpcz.in/api/v1/send-otp"
api_key = "VgsdaQYXmsmVFsUi2Fe4tC7vn"
api_secret_key = "dwGINQswrHtyngc"

def send_message(template_id,userdata,var1,var2,otherdata,message_type):#for send message when intimation created
    if message_type == "FQP Intimation Creation" or message_type == "FQP Intimation Rework":
        try:
            # count=1
            for i in userdata:
                url = str(api_url)+"?app_key="+str(api_key)+"&app_secret="+str(api_secret_key)+"&dlt_template_id="+str(template_id)+"&mobile_number=" + str(i.mobile) + "&v1=" + str(var1) + "&v2=" + str(var2)    
                # print(i.role.Role_Name,"---cou----",count,"url--------",url)
                # count=+1
                sms_template = message_template_log(template_id = str(template_id),date = datetime.datetime.now(),mobile_number = str(i.mobile))
                sms_template.save()
                response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        except Exception as e:
            pass
    elif message_type == "FQP Intimation Review":
        try:
            # count=1
            for i in userdata:
                url = str(api_url)+"?app_key="+str(api_key)+"&app_secret="+str(api_secret_key)+"&dlt_template_id="+str(template_id)+"&mobile_number=" + str(i.ContactNo) + "&v1=" + str(var1) + "&v2=" + str(var2)    
                # print(i.role.Role_Name,"---cou new----",count,"url--------",url)
                # count=+1
                sms_template = message_template_log(template_id = str(template_id),date = datetime.datetime.now(),mobile_number = str(i.ContactNo))
                sms_template.save()
                response = requests.get(url, proxies=proxyDict, headers={'User-Agent': 'Chrome'})
        except Exception as e:
            pass
    else:
        pass
    return 

