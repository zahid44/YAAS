from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from auction.forms import *
from auction.models import *


def index(request):
	qs = Auction.objects.filter(is_active = True)
	paginator = Paginator(qs, 10)

	page = request.GET.get('page')
	datas = paginator.get_page(page)

	return render(request, 'index.html', {'qs': qs, 'datas': datas, 'page': page})


def signup(request):
	form = UserForm()

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			auth_login(request, user)
			return HttpResponseRedirect('/')

	return render(request, 'signup.html', {'user_form': form})


@login_required
def profile(request):
	q = Profile.objects.get(user = request.user)
	form = UserForm(instance = request.user)
	formset = UserProfileForm(instance = request.user)

	if request.method == 'POST':
		form = UserForm(request.POST, instance = request.user)
		formset = UserProfileForm(request.POST, request.FILES, instance = request.user)
		if form.is_valid():
			form = form.save(commit = False)
			formset = UserProfileForm(request.POST, request.FILES, instance = form)
			if formset.is_valid():
				user = form.save()
				formset.save()
				auth_login(request, user)
				return HttpResponseRedirect('/')

	return render(request, 'profile.html', {'object': q, 'form': form, 'formset': formset})


@login_required
def post_auction(request):
	form = AuctionForm()

	if request.method == 'POST':
		form = AuctionForm(request.POST)
		if form.is_valid():
			form = form.save(commit = False)
			form.account = request.user.profile
			form.save()
			return HttpResponseRedirect('/')

	return render(request, 'post_auction.html', {'form': form})


def auction_detail(request, slug, id):
	q = Auction.objects.get(id = id)
	form = BidAuction()

	if request.method == 'POST':
		form = BidAuction(request.POST, auction = q)
		if form.is_valid():
			form = form.save(commit = False)
			form.auction = q
			form.bidder = request.user.profile
			form.save()
			return HttpResponseRedirect('/post/%s/%s/' % (q.slug, q.id))

	return render(request, 'detail.html', {'q': q, 'form': form})


@login_required
def edit_auction(request, id):
	q = Auction.objects.get(id = id)
	form = AuctionForm(instance = q)

	if request.method == 'POST':
		form = AuctionForm(request.POST, instance = q)
		if form.is_valid():
			form = form.save(commit = False)
			form.account = request.user.profile
			form.save()
			return HttpResponseRedirect('/')

	return render(request, 'post_auction.html', {'form': form})


@login_required
def edit_bid(request, id):

	if request.method == 'POST':
		q = Bid.objects.get(id = id)
		q.price = request.POST.get('price')
		q.save()
		return HttpResponseRedirect('/post/%s/%s' % (q.auction.slug, q.auction.id))


def search(request):
	qs = Auction.objects.filter(title__icontains = request.GET.get('q'), is_active = True)

	paginator = Paginator(qs, 10)

	page = request.GET.get('page')
	datas = paginator.get_page(page)

	return render(request, 'index.html', {'qs': qs, 'datas': datas, 'page': page})
