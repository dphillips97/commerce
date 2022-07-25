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

    class Category(models.TextChoices):
        CLOTHING = "C", "Clothing"
        ELECTRONICS = "E", "Electronics"
        EVERYTHING = "EE", "Everything Else"

    # Auto-generated
    item_id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True)
    lister_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True)

    # User-generated
    title = models.CharField(max_length=64)

    description = models.TextField()

    image_url = models.URLField(max_length=512, blank=True)
    
    category = models.CharField(max_length=2,
                                choices=Category.choices,
                                blank=True,
                                default=None, 
                                null=True)

    initial_bid = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=1,
                                    validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.item_id}: {self.title} listed by {self.lister_id}. Active={self.active}."

# Create form from model to pass to create_listing page
class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image_url', 'category', 'initial_bid']


class Bid(models.Model):

    item_id = models.IntegerField()

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