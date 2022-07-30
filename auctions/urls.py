from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("item/<str:item_id>", views.see_item, name="see_item"),
    path("categories/<str:category>/", views.index, name="show_cat_items"),
    path("categories/", views.see_categories, name="see_categories"),
    path("create/", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
