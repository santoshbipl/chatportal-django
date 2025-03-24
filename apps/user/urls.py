from django.urls import path
from apps.user.views import UserView, LoginApiView, SignupApiView, SingleUser, SearchApiView

urlpatterns = [
    path('users', UserView.as_view(), name='userList'),
    path('login', LoginApiView.as_view(), name='login'),
    path('signup', SignupApiView.as_view(), name='signup'),
    path('get-user', SingleUser.as_view(), name="single_user"),
    path('search', SearchApiView.as_view(), name="search_user"),


]
