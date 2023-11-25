from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
import json
from commerce.settings import DATE_INPUT_FORMATS

'''
def jsonfield_default_value():
    #return {"listing_id": 0}
    return [1]
'''

class User(AbstractUser):
    id           = models.AutoField(primary_key=True)
    watchlist    = models.ManyToManyField('auctions.Listing', related_name='watchlist', blank=True)
    #watchlist    = models.TextField(default=jsonfield_default_value) # JSON-serialized (text) version of the list
    #watchlist    = models.JSONField(default=jsonfield_default_value) # JSON-serialized (text) version of the list
    profile_photo = models.ImageField(
        upload_to='user_profiles',
        height_field=None,
        width_field=None,
        default='auctions/static/User01.png'
        )

'''
    #setting list, encoding intp json
    def set_watchlist(self, list):
        self.watchlist = json.dumps(list)
        #return self.watchlist

    #getting the list in list format, decoding from json
    def get_watchlist(self):
        return json.loads(self.watchlist)

    def add_to_watchlist (self, product):
        self.watchlist.append(product)
        return self.watchlist

    def remove_from_watchlist(self, product):
        self.watchlist.remove(product)
        return self.watchlist
'''
'''
class Profile(models.Model):
    id          = models.AutoField(primary_key=True)
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_owner")
    watchlist   = models.ManyToManyField('auctions.Listing', related_name='watchlist', blank=True)


    def add_to_watchlist(self, product):
        self.watchlist.append(product)
        return self.watchlist

    def remove_from_watchlist(self, product):
        self.watchlist.remove(product)
        return self.watchlist
'''

class Listing(models.Model):
    categories=[
        ("CH","chairs"),
        ("CA","cabinets"),
        ("SO","sofas"),
        ("TA","tables"),
        ("DE","decor"),
        ("OT","others")
    ]

    id          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=64)
    description = models.CharField(max_length=280)
    price       = models.DecimalField(max_digits=7, decimal_places=2)
    category    = models.CharField(max_length=10, choices=categories, default="others")
    status      = models.BooleanField(default="True")
    photo       = models.ImageField(
        upload_to='images_uploaded',
        height_field=None,
        width_field=None,
        default='auctions/static/images/01.jpg'
        )
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True)
    date        = models.DateField(default=(2023-10-20))
    bidder      = models.CharField(max_length=64, default="no one has made a bit yet.")


    def __str__(self):
        return f"{self.title}, {self.price}€"

    def change_price(self, new_price):
        if float(new_price)>float(self.price):
            self.price=new_price
        else:
            pass

    def change_bidder(self, new_bidder):
        self.bidder=new_bidder

    def show_categories(self):
        return self.categories

    def show_categories_names(self):
        categories_names=[]
        for i in self.categories:
            categories_names.append(i[1])
        return categories_names


class Bid(models.Model):
    id          = models.AutoField(primary_key=True)
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bidding')
    username    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    bid_amount  = models.DecimalField(max_digits=7, decimal_places=2)


    def __str__(self):
        return f"{self.username} bids {self.bid_amount}€"


class Comment(models.Model):
    id          = models.AutoField(primary_key=True)
    listing     = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing')
    text        = models.CharField(max_length=280)
    created_on  = models.DateField(auto_now_add=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter', null=True)
    upvotes     = models.IntegerField()
    upvoters    = models.ManyToManyField(User, related_name='upvoter', blank=True)


    class Meta:
        #ordering comments by date
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.id} by {self.owner}"

    def add_upvote(self):
        self.upvotes=int(self.upvotes)+1

    def remove_upvote(self):
        self.upvotes=int(self.upvotes)-1


class Watchlist(models.Model):
    id             = models.AutoField(primary_key=True)
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='watchlist_owner', null=True)
    watchlist   = models.ManyToManyField(Listing, related_name='products', blank=True)



    def __str__(self):
        return f"{self.owner}'s watchlist"

'''
    def add(self, product):
        self.my_watchlist.append(product)
        return self.my_watchlist

    def remove(self, product):
        self.my_watchlist.remove(product)
        return self.my_watchlist

'''






