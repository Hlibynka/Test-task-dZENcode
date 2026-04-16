from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, get_captcha

router = DefaultRouter()
router.register(r'', CommentViewSet, basename='comment')

urlpatterns = [
    path('get-captcha/', get_captcha, name='get_captcha'),
    path('', include(router.urls)),
]