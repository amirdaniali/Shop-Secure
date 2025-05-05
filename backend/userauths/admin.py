from django.contrib import admin

# Register your models here.
from userauths.models import Profile, User

class UserAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "phone"]
    search_fields = ['full_name','email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["full_name", "gender", "country"]
    search_fields = ['full_name','date','country','state']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)