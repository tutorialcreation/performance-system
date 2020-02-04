from django.contrib import admin
from pams_system.models.levels import *
from pams_system.models.maps import *
from pams_system.models.kpis import *

# Register your models here.
admin.site.register(Level)
admin.site.register(InputData)
admin.site.register(MapType)
admin.site.register(MapList)
admin.site.register(KpiType)
admin.site.register(KPIWeightings)
admin.site.register(KpiGroups)
admin.site.register(KpiMembership)