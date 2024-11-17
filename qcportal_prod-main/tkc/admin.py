from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(TKC_Turnover)
admin.site.register(TKC_BalanceSheet)
admin.site.register(TKC_Document)
admin.site.register(TKC_Payment)
# admin.site.register(Wo_Material_Dispatch_details)
class offermaterialsitestores(admin.ModelAdmin):
    list_display = ('id','offer_no', 'site_store',)
    search_fields = ('id','offer_no','site_store',)
    list_filter = ('wo','supplier','tkc_di','circle',)

admin.site.register(offer_material_site_stores,offermaterialsitestores)

class offermaterialserialnumber(admin.ModelAdmin):
    list_display = ('offer_no', 'site_store',)
    search_fields = ('offer_no','site_store',)
    list_filter = ('offer_no','wo','site_store','serial_no',)

admin.site.register(offer_material_serial_number,offermaterialserialnumber)
admin.site.register(SiteStore_Master)
admin.site.register(TKC_Consumer)
admin.site.register(TKC_Consumer_bid)
admin.site.register(TKC_ContractorSelections)
admin.site.register(TKC_bid_not_participated)
admin.site.register(TKC_contractor_work)
admin.site.register(create_mrc)
admin.site.register(tkc_site_store_drr_info)
admin.site.register(pi_verification_offier)
admin.site.register(Tkc_Work_Order_Trf_Details)
admin.site.register(tkc_wo_nabl_gatepass)
