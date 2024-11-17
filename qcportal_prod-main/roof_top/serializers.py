from csv import field_size_limit
# from dataclasses import field
from unittest.util import _MAX_LENGTH
from rest_framework import serializers

from rest_framework import serializers
from .models import *



# 1st api loginview--------------------------------

# INSPECTIONLIST 2nd api---------------------------------------------

class SolarUserData(serializers.ModelSerializer):
    class Meta:
        model = roof_top_first
        fields = ('user_type', 'agency_name', 'name_of_auth', 'address', 'contact', 'email','registration_no')

