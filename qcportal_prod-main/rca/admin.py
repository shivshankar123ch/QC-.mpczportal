from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(WO_Info)
admin.site.register(WO_Schedule_Info)
admin.site.register(WO_Copy_Info)
admin.site.register(RO_Info)
admin.site.register(RO_Material_Info)
admin.site.register(RO_Schedule_Info)
admin.site.register(RO_Copy)

class ROMaterialXMRInfoAdmin(admin.ModelAdmin):
    list_display = ('xmr', 'xmr_initial_sampled_flag', 'xmr_second_sampled_flag',)
    search_fields = ('xmr','ro',)
    list_filter = ('ro','xmr_sampled_flag',)

admin.site.register(RO_Material_XMR_Info, ROMaterialXMRInfoAdmin)

#admin.site.register(Oil_Request)
#admin.site.register(di_dtr)
admin.site.register(material_offer)


admin.site.register(RcaProcurementInfo)
admin.site.register(Rcatrf_Details)
admin.site.register(Rca_TRF_Test_Details)
admin.site.register(Rca_User_Registration)
admin.site.register(payment_rca)
admin.site.register(Rca_Vendor_Document)
admin.site.register(RCA_Vendor_Factory_image)
admin.site.register(certificate_details_cra)
admin.site.register(drr_info)
admin.site.register(rca_gatepass)
admin.site.register(power_analyser_newdesign)
admin.site.register(power_analyser_level1)
admin.site.register(power_analyser_level2)
admin.site.register(as_issue_gatepass)
admin.site.register(rca_mrc_details)
admin.site.register(rca_mrc_copy)
admin.site.register(rca_mrc_comment)
admin.site.register(as_nablpass_gatepass)
admin.site.register(rca_test_rept_power_analyzer)
admin.site.register(Pa_report)
admin.site.register(as_nabllotpass_gp)
admin.site.register(power_analyser_nonstar_newdesign)


admin.site.register(partial_mrc_details)
admin.site.register(partial_mrc_copy)
admin.site.register(partial_mrc_comment)
