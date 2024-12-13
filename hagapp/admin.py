from django.contrib import admin
from hagapp.models import Experiment, SignalData

# Register your models here.
admin.site.register(Experiment),
admin.site.register(SignalData),
