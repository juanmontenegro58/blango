from django.urls import path

from blog.api_views import UserDetail, post_list, PostDetail

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("posts/", post_list, name="api_post_list"),
    path("posts/<int:pk>", PostDetail.as_view(), name="api_post_detail"),
    path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
]


urlpatterns = format_suffix_patterns(urlpatterns)