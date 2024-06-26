from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages


from .models import AuctionsListings, Bids, Category, Comments, User


def index(request):
    # listings=AuctionsListings.objects.all()
    listings=AuctionsListings.objects.filter(active=True)

    return render(request, "auctions/index.html", {'listings':listings})


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
    
def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST.get("image")
        category_id = request.POST.get("category")


        if image == "":
            image= "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/495px-No-Image-Placeholder.svg.png?20200912122019"
        
        # new instance of AuctionsListings
        new_listing = AuctionsListings(
            owner=request.user,  
            title=title,
            description=description,
            price=price,
            photo_url=image
        )

        if category_id:
            category = Category.objects.get(pk=category_id)
            new_listing.category = category

        new_listing.save()
        new_listing.watchlist.add(request.user)

        return HttpResponseRedirect(reverse("index"))
    categories = Category.objects.all()
    return render(request, 'auctions/new.html', {'categories': categories})


def listing(request, pk):
    listing=AuctionsListings.objects.get(pk=pk)
    bid_count = Bids.objects.filter(auction=listing).count()

    is_in_watchlist = listing.watchlist.filter(pk=request.user.pk).exists()
    
    if request.method == "POST":
        if request.user.is_authenticated:
            if is_in_watchlist == False:
                print(f"Listing.pk:{listing.pk}, El user es {request.user.pk}")
                listing.watchlist.add(request.user)
                messages.success(request, f'You have added "{listing.title}" to your watchlist.')
                is_in_watchlist = True
            else:
                listing.watchlist.remove(request.user)
                messages.success(request, f'You have removed "{listing.title}" from your watchlist.')
                is_in_watchlist = False
        else:
            return HttpResponseRedirect(reverse('login'))


    if is_in_watchlist == False:
        is_in_watchlist = "Watch"
    else:
        is_in_watchlist = "Unwatch"

    comments = Comments.objects.filter(auction=listing)
    if not comments.exists():
        comments = False

    if listing.active:
        return render(request, 'auctions/listing.html', {'listing':listing, 'is_in_watchlist': is_in_watchlist,
                                                        'bid_count':bid_count,'comments':comments})
    else:
        if listing.winner.exists():
            winner = listing.winner.get()
        else:
            winner = None  
        return render(request, 'auctions/listing.html', {'listing':listing, 'is_in_watchlist': is_in_watchlist,
                                                        'bid_count':bid_count, 'winner': winner, 'comments':comments})
    
def bid(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            bid_amount = int(request.POST.get("bid_amount"))
            listing=AuctionsListings.objects.get(pk=pk)

            current_price = listing.price
            bid_instance = Bids(auction=listing, price=bid_amount, user=request.user)
            
            if listing.bid == None: # if there are still no bids 
                if bid_amount >= current_price: #
                    listing.price = bid_amount
                    listing.bid = bid_amount
                    listing.save()
                    bid_instance.save() 
                    listing.watchlist.add(request.user)
                    messages.success(request, f'Your bid of ${bid_amount} has been placed successfully.')
                else:
                    messages.error(request, 'Your bid must be greater than or equal to the current price.')
            else:
                if bid_amount > current_price:
                    listing.price = bid_amount
                    listing.bid = bid_amount
                    listing.save()
                    bid_instance.save()
                    listing.watchlist.add(request.user)
                    messages.success(request, f'Your bid of ${bid_amount} has been placed successfully.')
                else:
                    messages.error(request, 'Your bid must be higher than the previous bids.')

            return HttpResponseRedirect(reverse("listing", args=[pk]))
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponseRedirect(reverse("listing", args=[pk]))
    
def close(request, pk):
    if request.method =="POST":
        #Verify if there have been bids 
        listing = AuctionsListings.objects.get(pk=pk)
        listing.active = False
        listing.save()
        if listing.bid != None: # if there were bids
            #the auctions has the price of the highest bid, so de bid thar has the same price and corresponds to that listing is the winner
            bid = Bids.objects.get(auction=listing, price=listing.bid) 
            winner = User.objects.get(pk=bid.user.pk)
            listing.winner.add(winner)
        return HttpResponseRedirect(reverse("listing", args=[pk]))
    else:
        # If someone tries to access this URL via GET, we redirect them to the listing
        return HttpResponseRedirect(reverse("listing", args=[pk]))

def comment(request, pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            listing = AuctionsListings.objects.get(pk=pk)
            if not listing.active:
                messages.error(request, 'This listing is no longer active')
                return HttpResponseRedirect(reverse("listing", args=[pk]))
            else:
                text = request.POST["text"]
                text = text.strip()
                listing = AuctionsListings.objects.get(pk=pk)
                user = request.user

                comment = Comments(auction=listing,user=user,comment=text)
                comment.save()
                return HttpResponseRedirect(reverse("listing", args=[pk]))
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponseRedirect(reverse("listing", args=[pk]))


def watchlist(request):
    listings_in_watchlist = request.user.watchlist.all()
    print(listings_in_watchlist)
    return render(request, 'auctions/watchlist.html',{'listings_in_watchlist':listings_in_watchlist})


def categories(request):
    categories = Category.objects.all()
    return render(request,"auctions/categories.html",{'categories':categories})
    
def category(request,pk):
    category = Category.objects.get(pk=pk)
    listings = AuctionsListings.objects.filter(category=category)
    if not listings.exists():
        listings = False
        return render(request, "auctions/category.html", {'category':category,'listings':listings})
    else:
        active_listings = AuctionsListings.objects.filter(category=category, active=True)
        inactive_listings = AuctionsListings.objects.filter(category=category, active=False)
        if not active_listings.exists():
            active_listings = False
        if not inactive_listings.exists():
            inactive_listings = False

        return render(request, "auctions/category.html", {'category':category,'active_listings':active_listings,
                                                        'inactive_listings':inactive_listings})
    

def closed_listings(request):
    listings=AuctionsListings.objects.filter(active=False)

    return render(request, "auctions/closed.html", {'listings':listings})