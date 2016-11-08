from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Article, Subscriber

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class SubscriberInline(admin.StackedInline):
    model = Subscriber
    can_delete = False
    verbose_name_plural = 'subscriber'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (SubscriberInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Article)