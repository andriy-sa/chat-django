from django.urls import path

from chat import views

app_name = 'chat'
urlpatterns = [
    path('send_message', views.SendMessageAPIView.as_view(), name='send_message'),
]
