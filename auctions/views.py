from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listing, ListingForm, Bid, BidForm

from .models import User


def index(request, cat_filter=None):

    if cat_filter:
        active_listings = Listing.objects.filter(active=True).filter(cat_filter)

    else:
        active_listings = Listing.objects.filter(active=True)

    display_bids = {}

    # For each queryset item, find max bid (class Decimal)
    for listing in active_listings:
        
        try:
            bids = Bid.objects.filter(item_id=listing.item_id)
            max_bid = bids.order_by('-amount').first().amount
            max_bid_format = "${:.2f}".format(max_bid)
            display_bids[listing.item_id] = max_bid_format

        except:
            display_bids[listing.item_id] = "No bids"

    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "display_bids": display_bids
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "GET":
        
        listing_form = ListingForm()

        return render(request, "auctions/create_listing.html", {
            "form": listing_form
            })

    if request.method == "POST":

        listing_form = ListingForm(request.POST)

        if listing_form.is_valid():

            # save method should return complete object            
            complete_listing = listing_form.save()

            # Update bid value in Bid table
            initial_bid_entry = Bid(item_id=complete_listing.item_id,
                                    amount=complete_listing.initial_bid)
            
            initial_bid_entry.save()

            return HttpResponseRedirect(reverse("index"))

        else:

            # Return partially complete ListingForm
            return render(request, "auctions/create_listing.html", {
                "form": listing_form
                })

