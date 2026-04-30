from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register('login', views.loginviewset, basename='login')
router.register('users', views.userviewset, basename='users')
router.register('audio', views.audiouploadviewset, basename='audio')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

