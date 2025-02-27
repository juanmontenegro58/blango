from django.urls import path, re_path

from blog.api_views import UserDetail, post_list, PostDetail

from rest_framework.urlpatterns import format_suffix_patterns
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os

schema_view = get_schema_view(
    openapi.Info(
        title="Blango API",
        default_version="v1",
        description="API for Blango Blog",
    ),
    url=f"http://localhost:8000/api/v1/",
    public=True,
)

urlpatterns = [
    path("posts/", post_list, name="api_post_list"),
    path("posts/<int:pk>", PostDetail.as_view(), name="api_post_detail"),
    path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
    # re_path(
    #     r"^swagger(?P<format>\.json|\.yaml)$",
    #     schema_view.without_ui(cache_timeout=0),
    #     name="schema-json",
    # ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]


urlpatterns = format_suffix_patterns(urlpatterns)