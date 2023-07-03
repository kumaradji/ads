from django.contrib import admin
from .models import (Advert, Response, CustomUser)

admin.site.register(Advert)
admin.site.register(Response)
admin.site.register(CustomUser)
