from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting",views.new,name="new"),
    path("<int:pk>",views.listing, name="listing"),
    path("<int:pk>/bid",views.bid, name="bid"),
    path("<int:pk>/close", views.close, name="close"),
    path("<int:pk>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("<int:pk>/category", views.category, name="category"),
    path("closedlistings", views.closed_listings, name="closed_listings")
]
