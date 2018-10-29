from django import template
from auction.models import Bid

register = template.Library()

@register.filter(name='has_group')
def has_group(objects):
	return [i.bidder for i in objects ]
	# try:
	# 	Bid.objects.get(bidder = user)
	# 	return False
	# except:
	# 	return True