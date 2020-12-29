from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("lists/new", views.new_list, name="new_list"),
    re_path(r"^lists/(\d+)/$", views.view_list, name="view_list"),
    re_path(r"^lists/(\d+)/add_item$", views.add_item, name="add_item"),
]
