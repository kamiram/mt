from django.contrib import admin

from cp.models import EMail


class EMailAdmin(admin.ModelAdmin):
    list_display = ['uid', 'mail_from', 'mail_to', 'sent', 'topic', 'readcount']


admin.site.register(EMail, EMailAdmin)
