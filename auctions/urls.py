from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/<int:listing_id>", views.list, name="listing"),
    path("watchlist/<int:user_id>/<int:listing_id>", views.watch, name="watchlist"),
    path("watchlist_remove/<int:user_id>/<int:listing_id>", views.remove_watchlist, name="watchlist_remove"),
    path("create", views.create, name="create"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("upvote/<int:listing_id>/<int:comment_id>", views.change_upvote, name="upvote"),
    path("profile/<int:user_id>/)", views.profile, name="profile"),
    path("watchlist/<int:user_id>", views.view_watch, name="view_watchlist"),
    path("choose_category", views.choose_category, name="choose_category"),
    path("remove_listing/<int:listing_id>", views.remove_listing, name="remove_listing"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)