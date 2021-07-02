from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import MyUser,Trainer,Member,Slot,Dietician
class MyUserAdmin(UserAdmin):
    model = MyUser
    list_display = ['username','email','phone','workout']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('phone','workout')}),
    )
admin.site.register(MyUser)
admin.site.register(Trainer)
admin.site.register(Member)
admin.site.register(Slot)
admin.site.register(Dietician)

