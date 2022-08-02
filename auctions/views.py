from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from auctions.models import Listing, ListingForm, Bid, BidForm, Comment, CommentForm, Watchlist, User

def index(request, category=None):

    if category is not None:
        active_listings = Listing.objects.filter(active=True, category=category)

    else:
        active_listings = Listing.objects.filter(active=True)

    display_bids = {}

    # For each queryset item, find max bid (class Decimal)
    for listing in active_listings:
        
        # Oof this is ugly - clean it up
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

def see_categories(request):

    categories = Listing.CAT_CHOICES

    # Can delete?
    context = {"categories": categories}

    return render(request, "auctions/see_categories.html", context)


def see_item(request, item_id):

    item = Listing.objects.filter(item_id=item_id).first()

    max_bid = Bid.objects.filter(item_id=item_id).order_by("-amount").first()

    comments = Comment.objects.filter(item_id=item_id).all()

    u = User.objects.get(username=request.user)

    # Check if item is watched
    watched_queryset = Watchlist.objects.filter(user_id=u, item_id=item_id)

    # Alter button text based on whether item is watched
    if watched_queryset:
        watch_message = "Remove from watchlist"
    else:
        watch_message = "Add to watchlist"

    if request.method == "GET": 

        # Template will only show these if user is signed in
        bid_form = BidForm()
        comment_form = CommentForm()

        # Should fire every time?
        if item and max_bid:

            return render(request, "auctions/see_item.html", {
                "item_info": item,
                "max_bid": max_bid,
                "bid_form": bid_form,
                "comments": comments,
                "comment_form": comment_form,
                "watch_message": watch_message})

    if request.method == "POST" and 'bid_btn' in request.POST:

        bid_form_post = BidForm(request.POST)

        if bid_form_post.is_valid():

            bid_int = int(bid_form_post.cleaned_data["amount"])

            if (bid_int <= max_bid.amount):

                return render(request, "auctions/see_item.html", {
                    "item_info": item,
                    "max_bid": max_bid,
                    "bid_form": bid_form_post,
                    "message": "Your bid is too low!"
                    })

            else:

                new_bid = Bid(item_id=item, amount=bid_int)

                new_bid.save()

                return HttpResponseRedirect(f"/item/{item.item_id}")

    elif request.POST and 'comment_btn' in request.POST:

        comment_form_post = CommentForm(request.POST)

        if comment_form_post.is_valid():

            new_comment = Comment(item_id=item, 
                user_id=request.user,
                comment_text=comment_form_post.cleaned_data['comment_text'])

            new_comment.save()

            return HttpResponseRedirect(f"/item/{item.item_id}")

    elif request.POST and 'watch-btn' in request.POST:

        # If exists then delete
        if watched_queryset:
            watched_queryset.delete()

        elif not watched_queryset:
            new_watchlist_item = Watchlist(item_id=item,
                user_id=u)
            new_watchlist_item.save()

        return HttpResponseRedirect(f"/item/{item.item_id}")

@login_required()
def see_watchlist(request):

    # Get current user (must pass object)
    u = User.objects.get(username=request.user)
    
    # Get all watched items
    watched_items = Watchlist.objects.filter(user_id=u)

    # Why do I need "item_id_id"?
    # Contains primary key of Parent model
    # Maybe calling everything item_id is mixing stuff up?
    items = [Listing.objects.get(item_id=x.item_id_id) for x in watched_items]

    return render(request, "auctions/see_watchlist.html", {
        "items": items
        })