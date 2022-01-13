from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat-messages", views.chat_messages, name="chat-messages"),
    path("login", views.login, name="login"),
    path("messages", views.messages_api, name="messages"),
    path("register-user", views.register_user, name="register-user")
]