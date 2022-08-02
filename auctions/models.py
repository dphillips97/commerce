from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Listing(models.Model):

    CAT_CHOICES = (
        ("fashion", "Fashion"),
        ("electronics", "Electronics"),
        ("home", "Home"),
        ("toys", "Toys"),
        ("everything_else", "Everything Else"),
    )

    # Auto-generated
    item_id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    lister_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)

    title = models.CharField(max_length=64)

    description = models.TextField()

    image_url = models.URLField(max_length=512, blank=True)
    
    category = models.CharField(max_length=64,
                                choices=CAT_CHOICES,
                                blank=True,
                                default=None, 
                                null=True)

    initial_bid = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=1,
                                    validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.item_id}: {self.title}."

# Create form from model to pass to create_listing page
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'category', 'initial_bid']


class Bid(models.Model):

    item_id = models.ForeignKey(Listing,
                                on_delete=models.CASCADE,
                                to_field="item_id",
                                related_name="bids")
    
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    bid_datetime = models.DateTimeField(auto_now_add=True)

    amount = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=1)

    def __str__(self):
        return f"{self.amount} bid by {self.user_id} for {self.item_id}\n"

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

class Comment(models.Model):

    item_id = models.ForeignKey(Listing,
                                on_delete=models.CASCADE,
                                to_field="item_id",
                                related_name="comment")

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    comment_text = models.TextField()

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

class Watchlist(models.Model):

    item_id = models.ForeignKey(Listing,
                                on_delete=models.CASCADE,
                                to_field="item_id",
                                related_name="watchlist")

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    def __str__(self):
        return f"{self.item_id} added to watchlist of {self.user_id}"

