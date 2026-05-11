from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("core.urls")),
    path('fruits/',include("fruit.urls")),
    path('user/', include('users.urls')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)