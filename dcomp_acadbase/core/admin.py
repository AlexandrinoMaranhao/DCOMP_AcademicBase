from django.contrib import admin
from .models import User, Monografia, Banca

# Register your models here.
admin.site.register(User)
admin.site.register(Monografia)
admin.site.register(Banca)