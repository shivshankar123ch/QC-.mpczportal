from django.contrib import admin

from django.contrib import admin

from .models import *
admin.site.register(NABL_Document)
admin.site.register(Product)
admin.site.register(Product_Specification)
admin.site.register(List_Of_Test)
admin.site.register(Product_List_Of_Test)
admin.site.register(Perform_Test_By_NABL)
admin.site.register(NABL_Registration_Test)
admin.site.register(nabl_report_data)


admin.site.register(nabl_report_data_rca)
admin.site.register(sample_test)
admin.site.register(NABL_Perform_Test)