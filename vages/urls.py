from django.contrib import admin
from django.urls import path,include
from .import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("store.urls", namespace='store')),
    path('',include("user_authentication.urls", namespace='user_authentication')),
    path('accounts/', include('allauth.urls')),  # Allauth URL pattern
    path('',include("cart.urls", namespace='cart')),
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)