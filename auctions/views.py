from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import json
import datetime

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    active_listings=Listing.objects.filter(status=True)

    #formatting
    listing=active_listings[0]
    all_categories=listing.show_categories_names()

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })

def choose_category(request):
    if request.method == "POST":
        #chosen_category_name = request.POST.get('category')
        chosen_category_name = request.POST["category"]
        #reversing the formatting to get the tuple back ('CH', 'chairs')
        listings=Listing.objects.all()
        listing=listings[0]
        all_categories=listing.show_categories()
        #chosen_category_name.replace('"','').replace("'","")
        for i in all_categories:
            if str(chosen_category_name) in i:
                chosen_category=i
                chosen_category=chosen_category[0]

        category_listings=Listing.objects.filter(status=True, category=chosen_category)
        categories=listing.show_categories_names()
        return render(request, "auctions/index.html", {
            "listings": category_listings,
            "categories": categories,
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

def list(request, listing_id):
    listing=Listing.objects.get(id=listing_id)
    comments=Comment.objects.filter(listing=listing_id)

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "comments": comments
    })

def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    else:
        #getting the data
        title       = request.POST['title']
        description = request.POST['description']
        price       = request.POST['price']
        category    = request.POST['category']
        #photod       = request.FILES['photo']
        #photo_saved = photod['photo']
        photod       = request.FILES.get('photo')
        '''
        form = ModelFormWithFileField(request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
        '''
        #photo_saved=photod.save('commerce/media/images_uploaded', 'JPEG')

        owner       = request.user
        date = request.POST['date']
        #creating new listing
        new_listing=Listing(title=title, description=description, price=float(price), category=category, status="True", photo=photod, owner=owner, date=date, bidder="no one has made a bit yet.")
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))

def remove_listing(request, listing_id):
    #deleting listing
    listing=Listing.objects.get(id=listing_id)
    #listing.delete()
    listing.status="False"
    listing.save()

    #returning to index page
    active_listings=Listing.objects.filter(status=True)

    #formatting
    listing=active_listings[0]
    all_categories=listing.show_categories_names()

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })


def watch(request, listing_id, user_id):
    listing         = Listing.objects.get(id=listing_id)

    try:
        current_user    = User.objects.get(id=user_id)
        #profile = Profile.objects.filter(user=current_user).get()
        #their_watchlist = profile.watchlist
        #their_watchlist = current_user.watchlist

        #using class method to get a list
        #their_watchlist = current_user.get_watchlist()
        #their_watchlist = current_user.get_watchlist()
        #skipping default value
        #their_watchlist = their_watchlist[1:]
        #their_watchlist = current_user.watchlist.decoder

        if request.method == "GET":
            return render(request, "auctions/watchlist.html",{
                "watchlist": current_user.watchlist
                })
        else:
            current_user.watchlist.add(listing)
            new_watchlist=current_user.watchlist.all()
            #new_watchlist = current_user.watchlist.append(listing_id)
            #current_user.set_watchlist(new_watchlist)
            #current_user.save()
            #skipping default value
            #new_watchlist = new_watchlist[1:]
            #new_watchlist=their_watchlist.append(listing_id)
            #new_watchlist.set_watchlist()
            #saving the watchlist
            #new_watchlist.encoder
            #current_user.save()

            return render(request, "auctions/watchlist.html",{
                "watchlist": new_watchlist
                })

    except User.DoesNotExist:
        return render(request, "auctions/bid.html", {
                        "listing": listing,
                        "message": "You must be logged in to make a bid."
        })

def remove_watchlist(request, listing_id, user_id):
    listing         = Listing.objects.get(id=listing_id)
    try:
        current_user= User.objects.get(id=user_id)

        if request.method == "GET":
            return render(request, "auctions/watchlist.html",{
                "watchlist": current_user.watchlist
                })
        else:
            current_user.watchlist.remove(listing)
            new_watchlist=current_user.watchlist.all()
            return render(request, "auctions/watchlist.html",{
                "watchlist": new_watchlist
                })

    except User.DoesNotExist:
        return render(request, "auctions/watchlist.html", {
                        "listing": listing,
                        "message": "You must be logged in to see your watchlist."
        })

def view_watch(request, user_id):
    try:
        current_user= User.objects.get(id=user_id)

        if request.method == "GET":
            listings = current_user.watchlist.all()
            watchlist=[]
            for listing in listings:
                watchlist.append(listing)

            #watchlist = current_user.watchlist.values('id')
            #watchlist2=watchlist["id"]

            #for i in watchlist:
                #listings = Listing.objects.filter(id=i)

            return render(request, "auctions/watchlist.html",{
                "watchlist": watchlist
                })

    except User.DoesNotExist:
        return render(request, "auctions/watchlist.html", {
                        "message": "You must be logged in to see your watchlist."
        })

def bid(request, listing_id):
    listing=Listing.objects.get(id=listing_id)

    if request.method == "GET":
        return render(request, "auctions/bid.html",{
            "listing": listing
            })

    else:
        #get current price
        current_price=listing.price
        date=listing.date
        status=listing.status
        #check if product is avaiable:
        if status:
            #allow bidding only if bid bigger then current price
            new_price=request.POST['bid_amount']

            if float(new_price)>float(current_price):
                #overwrite price
                listing.change_price(new_price)
                listing.save()
                #save bid
                if request.user.is_authenticated:
                    bidder = request.user.username
                    listing.change_bidder(bidder)
                    listing.save()
                    return render(request, "auctions/bid.html", {
                        "listing": listing,
                        "message": "You have just placed your bid. The auction will end at:",
                        "date": date
                    })

                else:
                    return render(request, "auctions/bid.html", {
                        "listing": listing,
                        "message": "You must be logged in to make a bid."
                    })

            else:
                return render(request, "auctions/bid.html", {
                    "listing": listing,
                    "message": "The bidding amount must be higher than the current bid."
                })
        else:
            return render(request, "auctions/bid.html", {
                    "listing": listing,
                    "message": "Product not avaiable."
                })


def comment(request, listing_id):
    listing=Listing.objects.get(id=listing_id)

    #getting the data
    text       = request.POST['text']
    created_on = datetime.datetime.now()
    owner      = request.user
    upvotes    = 0
    #saving new comment
    new_comment=Comment(listing=listing, text=text, created_on=created_on, owner=owner, upvotes=int(upvotes))
    new_comment.save()
    #getting all comments with new comment
    comments=Comment.objects.filter(listing=listing_id)

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "comments": comments
        })

def change_upvote(request, comment_id, listing_id):
    user=request.user
    listing=Listing.objects.get(id=listing_id)
    comment=Comment.objects.get(id=comment_id)
    comments=Comment.objects.filter(listing=listing_id)

    #checking if post was already upvoted
    #upvoted=[i for i in comment.upvoters]
    upvoted = comment.upvoters.values('id')

    if user.id in upvoted:
        comment.remove_upvote()
        comment.upvoters.remove(user.id)
        comment.save()
        comments=Comment.objects.filter(listing=listing_id)

    else:
        comment.add_upvote()
        comment.upvoters.add(user.id)
        comment.save()
        comments=Comment.objects.filter(listing=listing_id)

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "comments": comments
        })


def profile(request, user_id):
    user=User.objects.get(id=user_id)
    return render(request, "auctions/profile.html", {
        "user": user
    })
