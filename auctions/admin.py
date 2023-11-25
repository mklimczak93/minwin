from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Listing, Bid, Comment, Watchlist


# Register your models here.
UserAdmin.fieldsets += ('Watchlist', {'fields': ('watchlist',)}), ('Profile photo', {'fields': ('profile_photo',)}),

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)