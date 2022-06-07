from django.contrib import admin
from .models import User, Users_likes, Posts


admin.site.register(User)
admin.site.register(Users_likes)
admin.site.register(Posts)