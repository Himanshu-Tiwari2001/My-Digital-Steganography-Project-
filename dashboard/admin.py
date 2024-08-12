from django.contrib import admin
from dashboard.models import Image,UserActivity
# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
 list_display = ['id', 'photo',]
 
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    search_fields = ('user__username', 'activity_type')

admin.site.register(UserActivity, UserActivityAdmin)