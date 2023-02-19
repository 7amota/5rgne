from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Slider)
admin.site.register(Item)
admin.site.register(Rate)
admin.site.register(View)
admin.site.register(FavList)

admin.site.site_title = "khrgne app"
admin.site.site_header = "khrgne Administration"