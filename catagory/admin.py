from django.contrib import admin
from .import models

# Register your models here.
class CatagotyAdmin(admin.ModelAdmin):
    prepopulated_field={'slug':('name',)}
    list_display=['name','slug']
admin.site.register(models.Catagory,CatagotyAdmin)    



