from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, re_path, include

from .views import HelloViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("greetings", HelloViewSet, basename="greet")

urlpatterns = router.urls
