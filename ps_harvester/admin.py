from django.contrib import admin
from ps_harvester.models import (HarvestStatus,
                                 HarvestProcess,
                                 HarvestFile,
                                 HarvestWebDirect,
                                 HarvestEntrySpeech,
                                 )

# Register your models here.
admin.site.register(HarvestStatus)
admin.site.register(HarvestProcess)
admin.site.register(HarvestFile)
admin.site.register(HarvestWebDirect)
admin.site.register(HarvestEntrySpeech)
