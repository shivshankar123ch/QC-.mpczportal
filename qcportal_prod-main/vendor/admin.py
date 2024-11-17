from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Vendor_Document)
admin.site.register(Vendor_Factory_Details)
admin.site.register(Vendor_Financial_Details)
admin.site.register(Vendor_Technical_Details)
admin.site.register(Vendor_Factory_image)
admin.site.register(Vendor_Material_Details)
admin.site.register(Vendor_Turnover)
admin.site.register(Vendor_BalanceSheet)

admin.site.register(Vendor_fiance_officer)
admin.site.register(Add_material)
admin.site.register(Material_Master)


admin.site.register(Material_Specification)
admin.site.register(area_store_officer)

admin.site.register(Factory_Technical_Details)
admin.site.register(FI_Appraisal_Details)
admin.site.register(Factory_Form_Details)

