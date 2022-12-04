from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from price.models import Price, UserPrice, PriceFeature, PriceFeaturePrice


class PriceFeatureInline(admin.TabularInline):
    model = PriceFeaturePrice


class PriceAdmin(ModelAdmin):
    list_display = ['title', 'price', ]
    inlines = [
        PriceFeatureInline,
    ]

admin.site.register(Price, PriceAdmin)


class PriceFeatureAdmin(ModelAdmin):
    list_display = ['code', 'title', ]
    list_display_links = ['code', 'title', ]
    pass


admin.site.register(PriceFeature, PriceFeatureAdmin)


class UserAdminWPrice(ModelAdmin):
    # list_display = ('email', 'username', 'is_active', 'is_superuser', 'is_staff', )
    pass


admin.site.register(UserPrice, UserAdminWPrice)


class UserAdminExt(UserAdmin):
    list_display = ['email', 'username', 'price', 'is_active', 'is_superuser', 'is_staff', ]
    list_display_links = ['email', 'username', 'price', ]
    def price(self, obj):
        userprice = obj.userprice.last()
        return userprice.price.title if userprice else ''


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdminExt)

