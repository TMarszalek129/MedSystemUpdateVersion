from django.contrib import admin
from django.utils.html import format_html
from .models import Patient, Measure, Measurement, Unit

class PatientAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname")

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))
class MeasureAdmin(admin.ModelAdmin):
    list_display = ["measure_name"]
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("id", "patient_id", "measure_id")
class UnitAdmin(admin.ModelAdmin):
    list_display = ["unit_name"]




admin.site.register(Patient, PatientAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Unit, UnitAdmin)
