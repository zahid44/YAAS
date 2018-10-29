# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from auction.models import *

class AuctionAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Auction._meta.fields if field.name != "id"]
	list_filter = ('status',)

class BidAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bid._meta.fields if field.name != "id"]

admin.site.register(Profile)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)