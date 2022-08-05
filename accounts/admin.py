from django.contrib import admin
from .models import *

class Custom_userAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser', 'is_active']
    search_fields = ['username']
admin.site.register(Custom_user, Custom_userAdmin)

class User_infoAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_full_name']
    search_fields = ['user__username']


    @admin.display(description='userName')
    def get_username(self, instance):
        return instance.user.username
    
    @admin.display(description='fullName')
    def get_full_name(self, instance):
        return f'{instance.first_name} {instance.last_name}'
        
admin.site.register(User_info, User_infoAdmin)

admin.site.register(Slider)