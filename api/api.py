from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from auction.models import *
from api.serializers import *


class SearchAPI(viewsets.ModelViewSet):
	queryset = Auction.objects.all()
	serializer_class = SearchSerializer
	http_method_names = ['get',]

	def get_queryset(self):
		if self.request.GET.get('q'):
			query = Auction.objects.filter(title__icontains = self.request.GET.get('q'))
		else:
			query = Auction.objects.all()
		return query


class BidAPI(viewsets.ModelViewSet):
	queryset = Bid.objects.all()
	serializer_class = BidSerializer
	permission_classes = (IsAuthenticated,)
	http_method_names = ['post',]

	def create(self, request):
		user = Token.objects.get(key=request.META['HTTP_AUTHORIZATION'].split(' ')[1]).user
		request.data['auction'] = Auction.objects.get(id = request.data['auction'])
		request.data['bidder'] = user.profile

		try:
			try:
				Bid.objects.get(bidder = request.data['bidder'], auction = request.data['auction'])
				return Response({'status': 1, 'data': 'Allready bid this'}, status=status.HTTP_200_OK) 
			except:
				Bid.objects.create(**request.data)
				return Response({'status': 1, 'data': 'ok'}, status=status.HTTP_201_CREATED)
		except Exception as err:
			return Response({'status': 0, 'msg': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

