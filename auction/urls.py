"""auction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from auction import views
from api import api

router = routers.DefaultRouter()
router.register(prefix=r'search', viewset=api.SearchAPI, base_name='search')
router.register(prefix=r'bid', viewset=api.BidAPI, base_name='bid')

urlpatterns = [
    path('api/', include(router.urls)),
	path('', views.index, name='index'),
	path('login/', LoginView.as_view(template_name='login.html'), name="login"),
	path('logout/', LogoutView.as_view(next_page='/'), name="logout"),
	path('signup/', views.signup, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('post-auction/', views.post_auction, name="post_auction"),
    path('edit-auction/<int:id>/', views.edit_auction, name="edit_auction"),
    path('post/<slug:slug>/<int:id>/', views.auction_detail, name='auction_detail'),
    path('edit-bid/<int:id>/', views.edit_bid, name="edit_bid"),
    path('search/', views.search, name="search"),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
