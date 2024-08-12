from django.contrib import admin
from .models import CustomUser, OtpToken
from django.contrib.auth.admin import UserAdmin


admin.site.site_header="Admin Login"
admin.site.site_title=" Stego-Admin Area"
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2')}
#          ),
#     )
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'profile_image')}  # Add 'profile_image' to the fields
         ),
    )



class OtpTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "otp_code")


admin.site.register(OtpToken, OtpTokenAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
    

