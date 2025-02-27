from http import HTTPStatus

from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from blango_auth.models import User
from blog.api.serializers import PostDetailSerializer, PostSerializer, UserSerializer
from blog.models import Post


from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser

from rest_framework import permissions

class ExampleComOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        email = getattr(request.user, "email", "")
        return email.split("@")[-1] == "example.com"
    
class AuthorModifyOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.author

class IsAdminUserForObject(permissions.IsAdminUser):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)

class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@api_view(["GET", "POST"])
def post_list(request, format = None):
    if request.method == "GET":
        posts = Post.objects.all()
        return Response({"data": PostSerializer(posts, many=True).data})
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(
                status=HTTPStatus.CREATED,
                headers={"Location": reverse("api_post_detail", args=(post.pk,))},
            )
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


# @api_view(["GET", "PUT", "DELETE"])
# def post_detail(request, pk, format = None):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response(status=HTTPStatus.NOT_FOUND)

#     if request.method == "GET":
#         return Response(PostSerializer(post).data)
#     elif request.method == "PUT":
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=HTTPStatus.NO_CONTENT)
#         return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
#     elif request.method == "DELETE":
#         post.delete()
#         return Response(status=HTTPStatus.NO_CONTENT)

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthorModifyOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

# class PostDetail(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView,
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer