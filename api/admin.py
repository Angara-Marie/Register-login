from django.contrib import admin
from django.contrib.auth import get_user_model
from . import models
User = get_user_model()
# Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("first_name" ,"last_name","gender", "email", "password")
# admin.site.register(User,UserAdmin)


# class DetailAdmin(admin.ModelAdmin):
#     list_display = ("customer","income","rent_amount", "electricity_bill", "water_bill", "loan_amount")
# admin.site.register(Detail , DetailAdmin)    


# class IdentificationAdmin(admin.ModelAdmin):
#     list_display = ("customer" ,"location", "id_number")
# admin.site.register(Identification,IdentificationAdmin)