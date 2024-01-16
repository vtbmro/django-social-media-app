from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from . import forms
from .models import Post, User, Follower
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime
import json

# TODO: styling
# Allows users to make posts if they are signed in to the page
def index(request):
    form = forms.PostForm()

    if request.method == "POST":
        form = forms.PostForm(request.POST)
        
        if form.is_valid():
            # Creates the post and saves it into the DB
            newPost = Post.objects.create(user = User.objects.get(id=request.user.id), text_content = form.cleaned_data.get("text_content"), date = datetime.datetime.now())
            newPost.save()
            
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html",{
            "form": form
        })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
# TODO: styling 

# Function displays all posts, ordered by most recent made. 
def all_post(request):
    
    # Displays a page with all the posts made by all user in reverse
    # cronological order
    posts = Post.objects.all().order_by("-date")
    paginator = Paginator(posts, 10)

    # added Pagination
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/all_post.html", {
        "page_obj": page_obj
    })

# TODO: styling 

# Function that display a profile when the name of a user is clicked
def profile_page(request, search_id):
    user = User.objects.get(id = search_id)

    # This two lines get a count of how many people follow this user and how many he follows
    followers = Follower.objects.filter(follows = User.objects.get(id = search_id)).count()
    follows = Follower.objects.filter(follower = User.objects.get(id = search_id)).count()

    # Retrieve posts made by the user for displaying
    posts = Post.objects.filter(user_id = search_id).order_by("-date")

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # If the user clicks on its own profile page do nothing
    if request.user.id == search_id:
        test = ""

    # Else, create a button that allows following and unfollowing
    else:

    # If the user already follows create an unfollow button
        try:
            test = Follower.objects.get(follows=User.objects.get(id = search_id),follower=User.objects.get(id = request.user.id))
            test = "True"

    # If the user doesnt follow the profile-page create a follow button
        except:
            test = "False"

    return render(request, "network/profile_page.html",{
        "profile_user": user,
        "page_obj": page_obj,
        "followers": followers,
        "follows": follows,
        "test": test
    })

# TODO: style follow button

# Function that allows following
def follow(request, search_id):

    # Create an instance of the Follower model
    new_follower = Follower.objects.create(follows = User.objects.get(id = search_id), follower = User.objects.get(id = request.user.id))
    new_follower.save()

    # Redirect to the profile page the user was in
    return redirect(f"http://127.0.0.1:8000/profile_page/{search_id}")


# Function that allows unfollowing
def unfollow(request, search_id):

    # Delete an instance of the Follower model
    delete_follower = Follower.objects.get(follows = User.objects.get(id = search_id), follower = User.objects.get(id = request.user.id))
    delete_follower.delete()

    # Redirect to the profile page the user was in
    return redirect(f"http://127.0.0.1:8000/profile_page/{search_id}")


# TODO: styling

# Function that render posts made by users that the signed user follows

def following(request):
    # Gets all the post made by users that the signed user follows
    list_of_ids = []
    people_user_follows = Follower.objects.filter(follower = request.user.id)
    
    for person in people_user_follows:
        list_of_ids.append(person.follows.id)

# Pagination
    posts = Post.objects.filter(user__in = list_of_ids).order_by("-date")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

# Render following page 
    return render(request, "network/following.html",{
        "posts": posts,
        "page_obj": page_obj
    })

# ALL API's under here (TODO: everything under here is done)
# API that return the content of the message using its ID

@csrf_exempt
@login_required
def edit_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
# Use data from fetch request to update the post with the new text_content
    else: 
        data = json.loads(request.body)

# Prevent user from saving empty posts also handled in the js script
    if data["content"] == "":
        return JsonResponse({"error": "Can't have an empty post"}, status=400)
    else:
        
# Using post id from the fetch request and user id we find the post
        try:
            post = Post.objects.filter(id = int(data["post_id"]), user = request.user)

# Update the post with the new value for content
            post.update(text_content = data["content"])
            return JsonResponse({"message": "Post updated successfully."}, status=201)
        
        except Post.DoesNotExist:
            return JsonResponse({"message": "Post does not exist."}, status=400)


# API that allows liking and unliking a post trough a fetch request
@csrf_exempt
@login_required
def like(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
        
    else:
        data = json.loads(request.body)
        post_id = int(data["post_id"])

# Check if the user liked the post already       
        try:
            # User has already liked the post
            user_already_liked = Post.objects.get(liked_by = request.user, pk=post_id)

            # -1 to likes counter in the Post
            user_already_liked.likes = user_already_liked.likes - 1 
            
            # remove the user from the liked_by list
            user_already_liked.liked_by.remove(request.user.id)

            #Save instance
            user_already_liked.save()

            return JsonResponse({"message": "Post unliked successfully."}, status=201)

            
        except Post.DoesNotExist:
            # User hasnt liked the post
            user_hasnt_liked = Post.objects.get(pk=post_id)

            # +1 to likes counter in the Post
            user_hasnt_liked.likes = user_hasnt_liked.likes + 1
            
            # add the user to liked_by list
            user_hasnt_liked.liked_by.add(request.user)

            #Save instance
            user_hasnt_liked.save()

            return JsonResponse({"message": "Post liked successfully."}, status=201)
        
        
# API that return the amount of likes a post    
@csrf_exempt
@login_required
def like_count(request, post_id):

# Check if request is GET
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
        
    else:
# Using the request we load the post we wanted
        id = int(post_id)

# Return number of likes
        try:
            post = Post.objects.get(pk = id)
            return JsonResponse({"success": f"Likes: {post.likes}"})

# Post not found error handling
        except Post.DoesNotExist:
            return JsonResponse({"error": "POST not found."}, status=400)
        

# API fucntion that check if logged_in user has liked a certain post
@csrf_exempt
@login_required 
def check_liked(request, post_id):

# Check if request is GET
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    
# Check if user liked the post
    else:
        try:
            id = int(post_id)
            post = Post.objects.get(pk = id)
            
            if request.user in post.liked_by.all():
                return JsonResponse({"success":"Liked"}, status=200)
                
            else:
                return JsonResponse({"error":"Not liked"}, status=200)
            
# No post found 
        except Post.DoesNotExist:
            return JsonResponse({"error": "POST not found."}, status=400)