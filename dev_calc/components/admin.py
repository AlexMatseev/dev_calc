from django.contrib import admin

from .models import ComponentDict, PriceComponent, Lots


class PriceComponentAdmin(admin.ModelAdmin):
    list_display = ('component', 'lot_id', 'price')


admin.site.register(ComponentDict)
admin.site.register(PriceComponent, PriceComponentAdmin)
admin.site.register(Lots)