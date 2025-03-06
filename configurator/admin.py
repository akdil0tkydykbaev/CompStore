from django.contrib import admin
from .models import PCConfigurator, Component, PCConfiguration

admin.site.register(PCConfigurator)
admin.site.register(Component)
admin.site.register(PCConfiguration)