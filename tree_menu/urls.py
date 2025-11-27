from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("page/<path:slug>/", views.page, name="page"),
]
