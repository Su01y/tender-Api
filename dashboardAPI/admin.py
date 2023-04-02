from django.contrib import admin

from .models import Purchases, Participants, Contracts


admin.site.register(Purchases)
admin.site.register(Participants)
admin.site.register(Contracts)
