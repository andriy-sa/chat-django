from django.urls import path

from users import views

app_name = 'users'
urlpatterns = [
    path('list/', views.UsersListAPIView.as_view(), name='list'),
    path('create/', views.UserCreateAPIView.as_view(), name='create'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]
