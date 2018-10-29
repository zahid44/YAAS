from django.db.models import Max
from auction.models import *
from datetime import *

def set_winner():
	qs = Auction.objects.filter(expire__date = date.today(), status = 1)
	for i in qs:
		print(i)
		try:
			bid = Bid.objects.filter(auction = i).annotate(wew=Max('bid_price'))[0]
			i.winner = bid.bidder
			i.status = 2
			i.save()
		except Exception as e:
			print(e)