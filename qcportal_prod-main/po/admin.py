from django.contrib import admin
from .models import *


admin.site.register(ProcurementInfo)
admin.site.register(PO_SD)
admin.site.register(PO_Temp_Table)

#####Anupam

admin.site.register(TRF_Details)
admin.site.register(TRF_Test_Details)


# jeevan
admin.site.register(Purchase_Order)
admin.site.register(PO_Material)
admin.site.register(PO_Copy)
admin.site.register(PO_Schedule)
admin.site.register(PO_Material_Offer)



admin.site.register(PO_Material_Offer_Serial_No)
admin.site.register(DI_Master)
admin.site.register(DI_Areastores)
admin.site.register(DI_Material_Offer_Serial_No)


admin.site.register(po_nabl_gatepass)
admin.site.register(PO_TRF_Details)

admin.site.register(sample_code_table_cp)
admin.site.register(po_nabl_gatepass_outward)

# PO MRC
admin.site.register(purchase_mrc_details)
admin.site.register(purchase_mrc_copy)
admin.site.register(purchase_mrc_comment)


