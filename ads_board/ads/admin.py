from django.contrib import admin
from .models import (Advert, Response, Category, CustomUser)

admin.site.register(Advert)
admin.site.register(Response)
admin.site.register(Category)
admin.site.register(CustomUser)
