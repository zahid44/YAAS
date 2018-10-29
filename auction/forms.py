from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Max
from auction.models import *
from datetime import *
from decimal import *
import re


class UserForm(forms.ModelForm):

    error_email = {
        'email_exist': _("Email allready exist."),
    }

    error_password = {
        'password_less': _("Password should be more than 6 characters."),
    }

    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'form-control input-lg', 'placeholder': field.label,
                                           'autocomplete': 'off'})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        check = User.objects.filter(email=email)

        if self.instance.email == email:
            return email
        else:
            if len(check) > 0:
                raise forms.ValidationError(
                    _("This email address is already in use. Please supply a different email address."))
            return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise forms.ValidationError(
                _("Password should be more than 6 characters."))
        return password

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('id',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'form-control input-lg', 'placeholder': field.label,
                                           'autocomplete': 'off'})


UserProfileForm = inlineformset_factory(User, Profile, form=ProfileForm, extra=1, can_delete=False)



class AuctionForm(forms.ModelForm):

    class Meta:
        model = Auction
        exclude = ('account', 'slug', 'status', 'winner', 'is_active',)

    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'form-control input-lg', 'placeholder': field.label, 'autocomplete': 'off'})
            if field and field_name == 'expire':
                field.widget.attrs.update({'class': 'form-control input-lg datepicker'})

    def clean_expire(self):
        expire = self.cleaned_data.get("expire").date()
        if expire < (date.today() + timedelta(days=3)):
            raise forms.ValidationError(_("Expire should be 72 hour from now on."))
        return expire


class BidAuction(forms.ModelForm):

    class Meta:
        model = Bid
        exclude = ('id', 'auction', 'bidder',)

    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction', None)
        super(BidAuction, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'class': 'form-control input-lg', 'placeholder': field.label, 'autocomplete': 'off'})

    def clean_bid_price(self):
        qs = Bid.objects.filter(auction = self.auction).aggregate(Max('bid_price'))['bid_price__max']
        if qs is None:
            qs = self.auction.price.amount
        price = self.cleaned_data.get("bid_price")
        # min_price = qs + (self.auction.price.amount * 5) / 100
        min_price = qs + Decimal(0.05)
        if price < min_price:
            raise forms.ValidationError(_("Price should be more than %s." % "{0:.2f}".format(min_price)))
        return price
