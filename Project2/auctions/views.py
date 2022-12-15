from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import datetime

from .models import *


def index(request):
    return render(
        request, "auctions/index.html", {"listings": AuctionListing.objects.all()}
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )
        image = request.POST["image_URL"]
        # Attempt to create new user
        try:
            if image:
                print(f"\m\m\m\m\n\n\n\n\n{image}")
                user = User.objects.create_user(
                    username=username, email=email, password=password, image=image
                )
                user.save()
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    categories = Category.objects.all()

    if request.method == "POST":

        title = request.POST["title"]
        if title == "":
            return render(
                request,
                "auctions/createListing.html",
                {"categories": categories, "message": "Please input a title."},
            )
        description = request.POST["description"]
        try:
            start_bid = float(request.POST["start_bid"])
        except ValueError:
            return render(
                request,
                "auctions/createListing.html",
                {"categories": categories, "message": "Please input a starting bid."},
            )
        if start_bid < 0:
            return render(
                request,
                "auctions/createListing.html",
                {
                    "categories": categories,
                    "message": "Starting Bid Should be positive!",
                },
            )
        try:
            category = Category.objects.get(pk=int(request.POST["category"]))
        except:
            return render(
                request,
                "auctions/createListing.html",
                {"categories": categories, "message": "You should precise a category!"},
            )

        image = request.POST["image_URL"]

        listing = AuctionListing.objects.create(
            title=title,
            category_id=int(request.POST["category"]),
            image=image,
            description=description,
            user=request.user,
        )
        initial_bid = Bid.objects.create(bid_value=start_bid, listing=listing)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(
            request, "auctions/createListing.html", {"categories": categories}
        )


def listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    try:
        is_watchlist = bool(
            listing.watched_item
            and listing.watched_item.all().filter(user=request.user)
        )
    except TypeError:
        is_watchlist = False
    if listing:
        if request.user.id == listing.user.id:
            return render(
                request,
                "auctions/listing.html",
                {"listing": listing, "ïs_owner": True},
            )

        return render(
            request,
            "auctions/listing.html",
            {
                "listing": listing,
                "is_watchlist": is_watchlist,
                "message": request.COOKIES.get("message"),
            },
        )
    else:
        pass


# TODO: If the bid doesn’t meet those criteria, the user should be presented with an error.
@login_required(login_url="/login/")
def bid(request, id):

    if request.method == "POST":

        listing = AuctionListing.objects.get(pk=id)
        response = redirect("listing", listing_id=id)
        try:
            bid_value = float(request.POST["bid-value"])
        except ValueError:
            response.set_cookie(
                "message", "Please imput something before submiting the bid", max_age=3
            )
            return response
        if bid_value > listing.current_price():
            response.set_cookie("message", "Your bid was accepted", max_age=3)
            Bid.objects.create(bid_value=bid_value, listing=listing, user=request.user)
        else:
            response.set_cookie(
                "message", "Your bid should be higher than the current bid", max_age=3
            )

        return response

    else:
        return redirect("index")


@login_required
def close(request, id):
    listing = AuctionListing.objects.get(pk=id)
    # these extra conditions can be deleted but just to make sure this is secure I added it
    if request.method == "POST" and listing and request.user.id == listing.user.id:
        winner_user = listing.bid_listing.last().user
        if winner_user == None:
            # TODO: I have to display an error (There is no bid)
            pass
        listing.date_sold = datetime.datetime.now()
        listing.winner = winner_user

        listing.save()

        return redirect("index")
    return redirect("listing", listing_id=id)


@login_required(login_url="/login/")
def watchlist(request):
    list_listing = [p.listings for p in request.user.user_watching.all()]
    return render(request, "auctions/watchlist.html", {"listings": list_listing},)


@login_required(login_url="/login/")
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        Watchlist.objects.create(user=request.user, listings=listing)
        return redirect("listing", listing_id=listing_id)
    return redirect("index")


@login_required(login_url="/login/")
def delete_watchlist(request, listing_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        item_to_delete = Watchlist.objects.get(listings=listing, user=request.user)
        item_to_delete.delete()
        return redirect("watchlist")


def category_list(request):
    return render(
        request, "auctions/category.html", {"categories": Category.objects.all()}
    )


def search_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = category.auction_category.all()
    return render(request, "auctions/index.html", {"listings": listings})


@login_required(login_url="/login/")
def comment(request, listing_id):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_id)
        comment_content = request.POST["comment"]
        owner = request.user
        Comment.objects.create(
            user=owner, auction_listing=listing, comment=comment_content
        )
        return redirect("listing", listing_id=listing_id)
