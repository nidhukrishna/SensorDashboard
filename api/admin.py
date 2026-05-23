from django.contrib import admin

from .models import SensorDataset, ExtractedCycle

admin.site.register(SensorDataset)
admin.site.register(ExtractedCycle)