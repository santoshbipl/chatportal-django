from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import *
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.user.models import User
from rest_framework import status
from apps.post.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.user.serializers import (
    UserSerializer, LoginSerializer, SignupSerializer
)
from django.db.models import Q


class UserView(ListAPIView):
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        excludeUsersArr = []
        try:
            excludeUsers = self.request.query_params.get('exclude')
            if excludeUsers:
                userIds = excludeUsers.split(',')
                for userId in userIds:
                    excludeUsersArr.append(int(userId))
        except:
            return []
        return super().get_queryset().exclude(id__in=excludeUsersArr).exclude(username='admin')


class SingleUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = get_user_id(self.request)
        user = User.objects.filter(id=user_id).first()

        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_200_OK)


class SearchApiView(ListAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response(UserSerializer(User.objects.filter(Q(username__icontains=request.data['query']) | Q(first_name__icontains=request.data['query'])).exclude(username='admin'), many=True).data, status=status.HTTP_200_OK)


class LoginApiView(TokenObtainPairView):
    
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer


class SignupApiView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = SignupSerializer
