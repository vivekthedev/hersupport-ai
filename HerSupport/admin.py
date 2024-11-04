from django.contrib import admin

from .models import Biomarker, CustomUser, History

admin.site.register(CustomUser)
admin.site.register(Biomarker)
admin.site.register(History)
