from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from andy_app.utils import CustomListAPIView, CustomPagination
from users.models import User
from users.serializers import LoginSerializer, UserCreateSerializer, UserSerializer, UsersListReqSerializer


class UsersListAPIView(CustomListAPIView):
    request_serializer_class = UsersListReqSerializer
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = (permissions.IsAuthenticated,)
    model = User

    def get_queryset(self):
        q = self.request_serializer_data.get('q')
        country = self.request_serializer_data.get('country')
        gender = self.request_serializer_data.get('gender')

        queryset = self.model.objects.all()
        if q:
            queryset = queryset.filter(Q(username__icontains=q) | Q(email__icontains=q))
        if country:
            queryset = queryset.filter(country=country)
        if gender:
            queryset = queryset.filter(gender=gender)

        return queryset


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'token': serializer.context['user'].token}, status=status.HTTP_200_OK)
