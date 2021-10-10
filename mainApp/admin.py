from django.contrib import admin

# Register your models here.
from .models import Image, Profile, Ticker, TickerWatcher

admin.site.register(Ticker)
admin.site.register(TickerWatcher)
admin.site.register(Profile)
admin.site.register(Image)
