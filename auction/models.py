# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Avg

from dateutil import relativedelta
from djmoney.models.fields import MoneyField
from datetime import date, timedelta


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile = models.CharField(max_length=15, blank = True, null = True)
	birthdate = models.DateField(blank=True, null=True)
	photo = models.ImageField(blank=True, null=True, upload_to='profile')
	about = models.TextField(max_length=500, blank=True)

	def __str__(self):
		return self.user.first_name

	def photo_url(self):
		try:
			if self.photo:
				return self.photo
			else:
				return '/static/user.png'
		except:
			return '/static/user.png'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	# print(instance.is_superuser)
	if instance.is_superuser:
		pass
	else:
		if created:
			Profile.objects.create(user=instance)
		instance.profile.save()


class Auction(models.Model):

	STATUS_CHOICE = (
		(1, 'Open'),
		(2, 'Resolve'),
		(3, 'Ban'),
		(4, 'Expire'),
	)

	account = models.ForeignKey(Profile, on_delete=models.CASCADE)
	title = models.CharField(max_length = 50)
	description = models.TextField()
	price = MoneyField(max_digits=14, decimal_places=0, default_currency='EUR', verbose_name = 'Minimum Price')
	is_active = models.BooleanField(default = False)
	created = models.DateTimeField(auto_now_add = True)
	expire = models.DateTimeField(verbose_name = 'Deadline')
	status = models.IntegerField(choices=STATUS_CHOICE, default=1)
	winner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'winner', blank = True, null = True)
	slug = models.SlugField()

	class Meta:
		ordering = ['-created']

	def get_average(self):
		data = self.bid_set.all().aggregate(Avg('bid_price'))['bid_price__avg']
		if not data:
			return 0
		else:
			return data

	def time_left(self):
		time = relativedelta.relativedelta(self.expire, timezone.now())
		if time.days:
			return str(time.days) + ' Days ' + str(time.hours) + ' Hours Left'
		else:
			return str(time.hours) + 'Hours Left'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Auction, self).save(*args, **kwargs)


class Bid(models.Model):
	auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
	bidder = models.ForeignKey(Profile, on_delete=models.CASCADE)
	bid_price = models.DecimalField(max_digits = 14, decimal_places=0)
	note = models.TextField(blank = True, null = True)
	created = models.DateTimeField(auto_now_add = True)

	class Meta:
		ordering = ['-bid_price']

	def get_time(self):
		time = relativedelta.relativedelta(timezone.now(), self.created)
		if time.days:
			return str(time.days) + ' Days ago'
		elif time.hours:
			return str(time.hours) + ' Hours ago'
		else:
			return str(time.minutes) + ' Minutes ago'

	

