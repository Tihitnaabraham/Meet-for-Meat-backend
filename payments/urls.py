from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, payment_list
from . import mpesa_views

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('payment-list/', payment_list, name='payment_list'),
    path('lipa-na-mpesa-online/', mpesa_views.lipa_na_mpesa_online, name='lipa_na_mpesa_online'),
    path('stk-push-callback/', mpesa_views.stk_push_callback, name='stk_push_callback'),
    path('c2b-validation/', mpesa_views.c2b_validation, name='c2b_validation'),
    path('c2b-confirmation/', mpesa_views.c2b_confirmation, name='c2b_confirmation'),
]
