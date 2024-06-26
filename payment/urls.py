from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.CheckoutTemplateView.as_view(), name='checkout'),
    path('sslc/status/',views.sslc_status, name='status'),
    path('sslc/complete/<val_id>/<tran_id>/',views.sslc_complete, name='sslc_complete'),
]