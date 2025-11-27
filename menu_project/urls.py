from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tree_menu.urls")),
    path("demo/", TemplateView.as_view(template_name="demo.html"), name="demo"),
]
