import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  


from .models import *

# -------------------------- login - regiser block ---------------------------------------

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

# -------------------------- index block ---------------------------------------


def index(request):

        posts1 = Post.objects.all()
        print(posts1)
        posts1 = posts1.order_by("-date")

        # paginator starts
        paginator = Paginator(posts1, 10)

        page = request.GET.get('page')  
        try:  
            posts = paginator.page(page)  
        except PageNotAnInteger:  
            # Если страница не является целым числом, поставим первую страницу  
            posts = paginator.page(1)  
        except EmptyPage:  
            # Если страница больше максимальной, доставить последнюю страницу результатов  
            posts = paginator.page(paginator.num_pages)  

        # print(f'posts = {posts}')
        # ppp = []
        # for post in posts:
        #     # print(f'post.likes {post.likes.count()}')
            
        #     # print(post.serialize())
        #     post.serialize()
        #     # print((post.serialize())[text])
        #     ppp.append(post.serialize())
        # print(ppp)
        if request.user.is_authenticated:
            liked_posts = request.user.user_likes.all()
        else:
            liked_posts = []        

        return render(request, "network/index.html", {
                "posts": posts,
                "liked_posts": liked_posts
            })


# @csrf_exempt
# @login_required
# def posts_like(request, post_id):
#         post = Post.objects.get(pk = post_id)
#         # print(post)
#         user = User.objects.get(pk = request.user.id)
#         # print(user)
#         if user in post.likes.all():
#             # print('like')
#             return JsonResponse({'isliked': True})
#         else:
#             # print('no')
#             return JsonResponse({'isliked': False})


# -------------------------------------- profile --------------------------------------------

def profile(request, name):
    # print(f'profile name= {name}')
    user = User.objects.get(username = name)
    print(user)

    if request.user.is_authenticated:
        liked_posts = request.user.user_likes.all()
        # print(liked_posts)
    else:
        liked_posts = []

    obj = Post.objects.filter(author = user.id)
    obj = obj.order_by('-date')

    paginator = Paginator(obj, 10)

    page = request.GET.get('page')  
    try:  
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        # Если страница не является целым числом, поставим первую страницу  
        posts = paginator.page(1)  
    except EmptyPage:  
        # Если страница больше максимальной, доставить последнюю страницу результатов  
        posts = paginator.page(paginator.num_pages)  
    
    # posts = []
    # for post in obj:
    #     serialized_post = post.serialize()
    #     posts.append(serialized_post)
    #     print(post) 
    #     if post in liked_posts:
    #         print(f'post.id {post.id}')         

    followers = user.followers.count()
    following = user.following.count()
    return render(request, 'network/profile.html', {
        "posts": posts,
        "liked_posts": liked_posts,
        'username1': user,
        'followers_count': followers,
        'following_count': following
        # 'followers': user.followers
    })


@login_required
def fol_posts(request):
    user = request.user
    posts = []
    print(f'request.user.following.all()= {request.user.following.all()}')


    for user in request.user.following.all():
        print(user)
        posts1 = Post.objects.filter(author = user)
        # posts1 = posts.order_by("-date")
        # posts1.sort(key=id)
        print(Post.objects.filter(author = user))
        for post in posts1:
            print(post.serialize())
            # post.serialize()
            posts.append(post.serialize())
    # print(posts)
    # print("testtesttest")
    # print(posts.sort(key=id.id))    
    # posts.order_by("-date")
    print(sorted(posts, key= lambda k: k['id'], reverse= True))
    posts = sorted(posts, key= lambda k: k['id'], reverse= True)
    liked_posts=[]
    if request.user.is_authenticated:
        liked_posts1 = request.user.user_likes.all()
        for post in liked_posts1:
            print(post.serialize())
            # post.serialize()
            liked_posts.append(post.serialize())

    else:
        liked_posts = []
    print(liked_posts)
    paginator = Paginator(posts, 10)

    page = request.GET.get('page')  
    try:  
        posts = paginator.page(page)  
    except PageNotAnInteger:  
        # Если страница не является целым числом, поставим первую страницу  
        posts = paginator.page(1)  
    except EmptyPage:  
        # Если страница больше максимальной, доставить последнюю страницу результатов  
        posts = paginator.page(paginator.num_pages) 

    return render(request, 'network/fol_posts.html', {
        "posts": posts,
        "liked_posts": liked_posts,
        'username1': user
        # 'followers': user.followers
    })


@csrf_exempt
@login_required
def new_post(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    # print(f'data={data}')
    
    # Get contents of email
    subject = data.get("subject", "")

    print(f'str(request.user)={str(request.user)}')
    post = Post(
        author = request.user,
        text = subject
    )
    post.save()
    print(post)

    return JsonResponse({"message": "Post saved successfully."}, status=201)




def is_follow(request, name):
    print("is_follow")
    user = request.user
    print(user)
    profile = User.objects.get(username = name)
    print(profile)
    if user in profile.followers.all():
        print(user in profile.followers.all())
        return JsonResponse({'status': True})
    else:
        print(f'rrrrrr {user in profile.followers.all()}')
        return JsonResponse({'status': False})


@csrf_exempt
@login_required
def follow(request, name):
    receiver = User.objects.get(username = name)
    print(receiver)
    if request.method == 'PUT':
        data = json.loads(request.body)

        if data.get('follow') == True:
            f_set = receiver.followers
            # print(f_set)
            f_set.add(request.user)
            receiver.save()
            follower = request.user
            follower.following.add(receiver)
            follower.save()
            return JsonResponse({'status': 'success'}, status=204)
            
        elif data.get('follow') == False:
            f_set = receiver.followers
            follower_inst = receiver.followers.get(pk=request.user.id)
            f_set.remove(follower_inst)
            receiver.save()
            follower = request.user
            following_set = follower.following
            following_inst = follower.following.get(username= name)
            following_set.remove(following_inst)
            follower.save()
            return HttpResponse(status=204)

        else:
            return JsonResponse({'error': 'Invalid body, use read=true or false'})
    else:
        return JsonResponse({'error': 'Invalid request method, use PUT'})


def count(request, name):
    profile = User.objects.get(username = name)
    followers = profile.followers.count()
    following = profile.following.count()
    print({'followers': followers, 'following': following})
    return JsonResponse({'followers': followers, 'following': following})


# ------------------------------------ likes -----------------------------
@csrf_exempt
@login_required

def likes(request, post_id):

    data = json.loads(request.body)
    print(data)
    post = Post.objects.get(pk = post_id)
    print(post)
    # likes = post.likes
    # print(f'likes= {likes}')
    user = request.user
    print(user.id)
    print(user.user_likes.all())

    if request.method == 'POST':
        
        if data.get('like') == True:
            print("like true")
                 
            post.likes.add(user)
            post.save
            # print(post.likes)
            return HttpResponse(status=200)

        else:
            print("like false")
            # print(post.likes + 1)
           
            post.likes.remove(post.likes.get(pk = user.id))
            post.save()
            # print(post.likes)
            return HttpResponse(status=200)
    else:        
        return HttpResponseRedirect(reverse("index"))          


@csrf_exempt
@login_required
def edited_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = Post.objects.get(pk = post_id)

        post_data = json.loads(request.body)
        print(post_data)
        post_text = post_data.get('new_post_content')
        post.text = post_text
        print(post_text)
        post.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseRedirect(reverse('index'))
