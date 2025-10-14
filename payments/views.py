from django.shortcuts import render
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


def payment_list(request):
    payments = Payment.objects.all().order_by('-created_at')
    return render(request, 'payments/payment_list.html', {'payments': payments})
