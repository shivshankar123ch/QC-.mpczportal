from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.admin import ExportActionMixin

# Register your models here.


# admin.site.register(User_Registration_CA)
admin.site.register(Report_Data)

admin.site.register(Payudata_main1)
admin.site.register(Collection_Agent)
admin.site.register(invoice_data)
admin.site.register(invoice)
admin.site.register(Generated_Invoice)
admin.site.register(Commerical_invoice)
admin.site.register(CA_Deregistration)
admin.site.register(CA_Bank_Update_Req)
# @admin.register(Collection_Agent)
# class Collection_AgentAdmin(ImportExportModelAdmin):
#     list_display = ("Name","Customomer_Id","CUSTOMER_NAME","CUSTOMER_BILL_AMOUNT","CUSTOMER_PAYMENT_DATE","CUSTOMER_PAYMENT_MONTH","CUSTOMER_PAYMENT_YEAR","IS_COMMISSION","COMMISION_AMOUNT","GST_AMOUNT","COLLECTION_AGENT_ID","COLLECTION_AGENT_NAME","CONTRACTOR_ID","IS_PROCESS")


class Collection_AgentResource(resources.ModelResource):

    class Meta:
        model = Collection_Agent

class User_Registration(ExportActionMixin,admin.ModelAdmin):
	list_display=('User_Id','Name','Mobile','Contractor_Id')
admin.site.register(User_Registration_CA,User_Registration)

# from import_export.admin import ImportExportModelAdmin
# from django.contrib import admin

# @admin.register(Collection_Agent)
# class Collection_AgentAdmin(ImportExportModelAdmin):
#     pass
# from import_export.admin import ImportExportModelAdmin
# from django.contrib import admin

# @admin.register(Collection_Agent)
# class Collection_AgentAdmin(ImportExportModelAdmin):
#     pass



# @admin.register(User_Registration_CA)
# class User_Registration_CAAdmin(ImportExportModelAdmin):
#     pass    