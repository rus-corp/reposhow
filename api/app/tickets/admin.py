from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Ticket

admin.site.register(Ticket, MPTTModelAdmin)