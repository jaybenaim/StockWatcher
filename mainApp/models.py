import json
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
import datetime
import uuid


def make_unique_picture_filename(instance, filename):
    return uuid.uuid4().hex[:6] + filename[filename.rfind(".") :]


class Ticker(models.Model):
    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return (
            str(self.symbol)
            + ": $"
            + str(self.price)
            + " - Updated: "
            + str(self.updated_at.strftime("%x %I:%M%p"))
        )

    def is_recent(self):
        updated_on_day = self.updated_at.day

        today = datetime.date.today().day

        return updated_on_day == today

    symbol = models.CharField(max_length=6)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=3, max_digits=9, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TickerWatcher(models.Model):
    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        symbol = self.ticker

        return (
            str(symbol.symbol)
            + ": $"
            + str(symbol.price)
            + ", Min: $"
            + str(self.min_price)
            + " - Max: $"
            + str(self.max_price)
            + f' -- Tickr Updated: {self.ticker.updated_at.strftime("%x %I:%M%p")}'
        )

    def get_user(self):
        return self.user.email

    def get_phone(self):
        profile = Profile.objects.filter(user__email=self.user.email)
        json_profile = json.loads(serializers.serialize("json", profile))[0]

        return json_profile["fields"]["phone"]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, blank=True, null=True)
    min_price = models.DecimalField(decimal_places=3, max_digits=9)
    max_price = models.DecimalField(decimal_places=3, max_digits=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Image(models.Model):
    as_url = models.TextField(max_length=500, blank=True, null=True)
    as_file = models.ImageField(
        blank=True, null=True, upload_to=make_unique_picture_filename
    )

    def __str__(self):
        return self.as_url or "Image missing or is a file"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=30, unique=True, blank=True)
    avatar_url = models.ForeignKey(
        Image, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.display_name
