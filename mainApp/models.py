from django.core import serializers
from django.db import models
from django.contrib.auth.models import User
import datetime
class Ticker(models.Model):
  class Meta:
   ordering = ['-updated_at']

  def __str__(self):
    return str(self.symbol) + ': $' + str(self.price) + ' - Updated: ' + str(self.updated_at.strftime("%x %I:%M%p"))

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
   ordering = ['-updated_at']

  def __str__(self):
    symbol = self.ticker

    return  str(symbol.symbol) + ': $' + str(symbol.price) + ', Min: $' + str(self.min_price) + ' - Max: $' + str(self.max_price) + f' -- Tickr Updated: {self.ticker.updated_at.strftime("%x %I:%M%p")}'

  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE, blank=True, null=True)
  min_price = models.DecimalField(decimal_places=3, max_digits=9)
  max_price = models.DecimalField(decimal_places=3, max_digits=9)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
