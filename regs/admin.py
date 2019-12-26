from django.contrib import admin
from .models import *
# Register your models here.

class RegsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'status']

admin.site.register(Registration, RegsAdmin)
admin.site.register(Contact)

class TokenAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'token', 'role',)
    readonly_fields = ('token',)

admin.site.register(Token, TokenAdmin)
admin.site.register(News)
