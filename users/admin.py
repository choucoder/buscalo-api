from django.contrib import admin
from .models import User, UserVerification


admin.register(User)
admin.register(UserVerification)