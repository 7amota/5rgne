from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Slider)
admin.site.register(Rate)
admin.site.register(View)
admin.site.register(FavList)

class ItemImages(admin.TabularInline):
    model = Images

class ItemInline(admin.ModelAdmin):
    model = Item
    inlines = [ItemImages]

admin.site.register(Item,ItemInline)



class TripInline(admin.TabularInline):
    model = Trip


class PackageInline(admin.ModelAdmin):
    model = Package
    inlines = [TripInline]


admin.site.register(Package,PackageInline)
admin.site.site_title = "khrgne app"
admin.site.site_header = "khrgne Administration"