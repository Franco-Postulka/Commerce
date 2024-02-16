from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages


from .models import AuctionsListings, Bids, Category, User


def index(request):
    listings=AuctionsListings.objects.all()

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
        
        # Crear una nueva instancia de AuctionsListings
        new_listing = AuctionsListings(
            owner=request.user,  # Asígnalo al usuario actual
            title=title,
            description=description,
            price=price,
            photo_url=image
        )

        if category_id:
            # Convertir el ID de la categoría a una instancia de Category
            category = Category.objects.get(pk=category_id)
            new_listing.category = category

        new_listing.save()

        return HttpResponseRedirect(reverse("index"))
    categories = Category.objects.all()
    return render(request, 'auctions/new.html', {'categories': categories})


def listing(request, pk):
    listing=AuctionsListings.objects.get(pk=pk)
    bid_count = Bids.objects.filter(auction=listing).count()

    is_in_watchlist = listing.watchlist.filter(pk=request.user.pk).exists()

    if request.method == "POST":
        if is_in_watchlist == False:
            listing.watchlist.add(listing.pk,request.user.pk)
            messages.success(request, f'You have added "{listing.title}" to your watchlist.')
            is_in_watchlist = True
        else:
            listing.watchlist.remove(listing.pk, request.user.pk)
            messages.success(request, f'You have removed "{listing.title}" from your watchlist.')
            is_in_watchlist = False

    if is_in_watchlist == False:
        is_in_watchlist = "Watch"
    else:
        is_in_watchlist = "Unwatch"
    
    return render(request, 'auctions/listing.html', {'listing':listing, 'is_in_watchlist': is_in_watchlist,
                                                    'bid_count':bid_count})

def bid(request, pk):
    if request.method == "POST":
        bid_amount = int(request.POST.get("bid_amount"))
        listing=AuctionsListings.objects.get(pk=pk)

        current_price = listing.price
        bid_instance = Bids(auction=listing, price=bid_amount, user=request.user)
        
        if listing.bid == None:
            if bid_amount >= current_price:
                listing.price = bid_amount
                listing.bid = bid_amount
                listing.save()
                bid_instance.save() 
                messages.success(request, f'Your bid of ${bid_amount} has been placed successfully.')
            else:
                messages.error(request, 'Your bid must be greater than or equal to the current price.')
        else:
            if bid_amount > current_price:
                listing.price = bid_amount
                listing.bid = bid_amount
                listing.save()
                bid_instance.save()
                messages.success(request, f'Your bid of ${bid_amount} has been placed successfully.')
            else:
                messages.error(request, 'Your bid must be higher than the previous bids.')

        return HttpResponseRedirect(reverse("listing", args=[pk]))
    else:
        # Si alguien intenta acceder a esta URL a través de GET, los redireccionamos al listado
        return HttpResponseRedirect(reverse("listing", args=[pk]))
    
def close(request, pk):
    if request.method =="POST":
        #Verificar si hubieron bids
        listing = AuctionsListings.objects.get(pk=pk)
        listing.active = False
        listing.save()
        if listing.bid != None:
            #Ver quien es el ganador
            bid = Bids.objects.get(auction=listing)
            if listing.bid == bid.price:
                winner = User.objects.get(pk=bid.user.pk)
    return render(request,"auctions/part.html",{"winner":winner})
        #renderizar el nombre del ganador para todos los usuarios
        #Renderizar que es el ganador al ganador 
