from django.contrib import admin
from .models import Brand, Cap, Stock, Price, Order, Link, DetailPhoto, OrderDetail


class DetailPhotoInline(admin.TabularInline):
    model = DetailPhoto


class PriceInline(admin.TabularInline):
    model = Price


class CapAdmin(admin.ModelAdmin):
    inlines = [
        DetailPhotoInline,
        PriceInline,
    ]
    list_display = ['id', 'name', 'is_active', 'cover_image']


admin.site.register(Brand)
admin.site.register(Cap, CapAdmin)
admin.site.register(Stock)
admin.site.register(Price)
admin.site.register(DetailPhoto)
admin.site.register(Order)
admin.site.register(Link)
admin.site.register(OrderDetail)
