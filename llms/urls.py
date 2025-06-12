from django.urls import path
from . import views

app_name = "llms"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("llm_calling/", views.llm_call, name="calls"),
    path("message_upload/", views.message_post, name="message_post"),
    path("message/<int:message_id>/", views.get_message, name="message_get")
]