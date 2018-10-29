from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from auction.models import *


class SearchSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Auction
		fields = '__all__'



class BidSerializer(serializers.ModelSerializer):

	class Meta:
		model = Bid
		exclude = '__all__'