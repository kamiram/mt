from django.contrib import admin

from cp.models import Constants


class ConstantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']


admin.site.register(Constants, ConstantsAdmin)

