from rest_framework import serializers
from vendor.models import *


class Vendor_Financial_Details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_Financial_Details
        fields = "__all__"

