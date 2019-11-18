from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view, authentication_classes, action
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from itboard.models import Post, Image
from itboard.serializers import PostSerializer, ImageSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({"error": "Please provide both username and password"},
                        status=HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": f"User with name \'{username}\' already exists"},
                        status=HTTP_400_BAD_REQUEST)

    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()

    return Response(status=HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Invalid credentials'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=request.user)
    user = {
        'id': request.user.id,
        'username': request.user.username
    }

    return Response({
        'user': user,
        'token': token.key
    }, status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def logout(request):
    if not request.user.is_authenticated:
        return Response({'error': 'Invalid credentials'},
                        status=HTTP_404_NOT_FOUND)

    request.user.auth_token.delete()
    return Response(status=HTTP_200_OK)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=True, methods=['post'])
    def upload_image(self, request):
        try:
            file = request.data['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')

        post_id = request.data['post']
        post = get_object_or_404(Post, pk=post_id)
        image = Image.objects.create(file=file, post=post)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
