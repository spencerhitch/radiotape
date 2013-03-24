from django.contrib import admin
from django.contrib.auth.models import User
from rec.models import *

admin.site.register(Profile)
admin.site.register(Mix)
admin.site.register(Track)
admin.site.register(TrackSound)
admin.site.register(MixComment)