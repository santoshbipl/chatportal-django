from django.urls import path
from . import views 


urlpatterns = [
    path('feed/', views.PostListCreateApiView.as_view(), name="blog_home"),
    path('create/post/', views.PostListCreateApiView.as_view(), name="create_post"),
    path('post/like/', views.LikeApiView.as_view(), name="like_post"),
    path('post/delete/', views.DeletePost.as_view(), name="delete_post"),
]   