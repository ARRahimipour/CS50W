
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),

    path('new_post', views.new_post, name='new_post'),
    # path('likes_count/<int:post_id>', views.posts_like, name='posts_like'),
    path('edited_post/<int:post_id>', views.edited_post, name='edited_post'),
    path('fol_posts', views.fol_posts, name='fol_posts'),
    path('is_follow/<str:name>', views.is_follow, name='is_follow'),
    path('profile/<str:name>', views.profile, name='profile'),
    path('profile/is_follow/<str:name>', views.is_follow, name='is_follow'),
    path('profile/<str:name>/follow', views.follow, name='follow'),
    path('profile/edited_post/<int:post_id>', views.edited_post, name='edited_post'),
    path('profile/count/<str:name>', views.count, name='count'),
    path('likes/<int:post_id>', views.likes, name='likes'),
    path('profile/likes/<int:post_id>', views.likes, name='likes')


]
