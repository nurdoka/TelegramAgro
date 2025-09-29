from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.submit_message, name="submit_message"),
    path("monitor/", views.monitor_messages, name="monitor_messages"),
    path("mine/", views.my_messages, name="my_messages"),
]
