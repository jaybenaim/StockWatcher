"""StockWatcher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http.response import JsonResponse
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from mainApp import views
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/users", views.UserViewSet)
router.register(r"api/groups", views.GroupViewSet)
router.register(r"api/tickers", views.TickerviewSet, basename="tickers")
router.register(r"api/watchers", views.TickerWatcherViewSet)
router.register(r"api/profiles", views.ProfileViewSet)
router.register(r"api/images", views.ImageViewSet)

# router.register(r'api/tickers/recent', views.RecentTickerView)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls"), name="rest_framework"),
    path("admin/", admin.site.urls),
    path("api/stock/", include("mainApp.urls")),
    path("api/status/", views.db_status, name="status"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
