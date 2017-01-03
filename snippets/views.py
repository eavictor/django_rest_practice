# from django.http import Http404
# from rest_framework import mixins
from rest_framework import generics
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
# from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route


# Create your views here.
"""Class views: ViewSet"""


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides 'list' and 'detail' actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides 'list', 'create', 'retrieve', 'update', and 'destory' actions.

    Additionally we also provide an extra 'highlight' action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


"""Root Endpoint API view"""


# @api_view(["GET"])
# def api_root(request, format=None):
#     return Response({
#         "users": reverse("user-list", request=request, format=format),
#         "snippets": reverse("snippet-list", request=request, format=format)
#     })


"""Class views: Generic"""


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


"""Class Views: Mixin"""


# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     @classmethod
#     def get(cls, request, *args, **kwargs):
#         return cls.list(request, *args, **kwargs)
#
#     @classmethod
#     def post(cls, request, *args, **kwargs):
#         return cls.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     @classmethod
#     def get(cls, request, *args, **kwargs):
#         return cls.retrieve(request, *args, **kwargs)
#
#     @classmethod
#     def put(cls, request, *args, **kwargs):
#         return cls.update(request, *args, **kwargs)
#
#     @classmethod
#     def delete(cls, request, *args, **kwargs):
#         return cls.destroy(request, *args, **kwargs)


"""Method Views"""


# class SnippetList(APIView):
#     """
#     List all code snippets, or create a new snippet
#     """
#     @classmethod
#     def get(cls, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     @classmethod
#     def post(cls, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     @classmethod
#     def get_object(cls, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return None
#
#     @classmethod
#     def get(cls, request, pk, format=None):
#         print(pk)
#         snippet = cls.get_object(pk=pk)
#         serializer = SnippetSerializer(snippet)
#         if snippet is not None:
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     @classmethod
#     def put(cls, request, pk, format=None):
#         data = JSONParser().parse(request)
#         snippet = cls.get_object(pk=pk)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @classmethod
#     def delete(cls, request, pk, format=None):
#         snippet = cls.get_object(pk=pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "POST"])
# def snippet_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == "GET":
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "PUT", "DELETE"])
# def snippet_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(data=None, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid:
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(data=None, status=status.HTTP_404_NOT_FOUND)
#
#     elif request.method == "DELETE":
#         snippet.delete()
#         return Response(data=None, status=status.HTTP_204_NO_CONTENT)
