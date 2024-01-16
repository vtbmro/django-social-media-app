
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_post", views.all_post, name="all_post"),
    path("following", views.following, name="following"),
    path("follow/<int:search_id>", views.follow, name="follow"),
    path("unfollow/<int:search_id>", views.unfollow, name="unfollow"),
    path("profile_page/<int:search_id>", views.profile_page, name="profile_page"),

    # API
    path("like", views.like, name="like"),
    path("like_count/<int:post_id>", views.like_count, name="like_count"),
    path("profile_page/edit_post", views.edit_post, name="edit_post"),
    path("check_liked/<int:post_id>", views.check_liked, name="check_liked")
]