from django.contrib import admin
from .models import STOCK,LINK,HIST,TEXTARTIC

# Register your models here.
admin.site.register(STOCK)
admin.site.register(LINK)
admin.site.register(HIST)
admin.site.register(TEXTARTIC)