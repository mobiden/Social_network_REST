from django.urls import path
from .view import SignUp, LoginUser, PostCreation, PostLike, UserRetrieveUpdateAPIView

app_name = 'my_so_net'

urlpatterns = [
    path('user/signup/', SignUp.as_view(), name='signup'),
    path('user/login/', LoginUser.as_view(), name='login'),
    path('post/creation/', PostCreation.as_view(), name="post_creation"),
    path('post/like/', PostLike.as_view(), name='post_like'),
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='retrieve_updateUser'),

]