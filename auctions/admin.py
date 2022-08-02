from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watchlist

class UserAdmin(admin.ModelAdmin):
	pass

class ListingAdmin(admin.ModelAdmin):
	list_display = ("item_id", "title", "description", "lister_id", "category")

class BidAdmin(admin.ModelAdmin):
	list_display = ("item_id", "user_id", "bid_datetime", "amount")

class CommentAdmin(admin.ModelAdmin):
	list_display = ("item_id", "user_id", "comment_text")

class WatchlistAdmin(admin.ModelAdmin):
	list_display = ("item_id", "user_id")


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
