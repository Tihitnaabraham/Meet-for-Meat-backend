
from django.shortcuts import render
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from users.models import User

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

def payment_list(request):
    payments = Payment.objects.all().order_by('-created_at')
    return render(request, 'payments/payment_list.html', {'payments': payments})

@csrf_exempt
def stk_push_callback(request):
    if request.method == 'POST':
        callback_data = json.loads(request.body)
        print("STK Callback:", callback_data)

        body = callback_data.get("Body", {})
        stk_callback = body.get("stkCallback", {})

        result_code = stk_callback.get("ResultCode")
        result_desc = stk_callback.get("ResultDesc")
        merchant_request_id = stk_callback.get("MerchantRequestID")
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        callback_metadata = stk_callback.get("CallbackMetadata", {})

        amount = None
        phone_number = None
        items = callback_metadata.get("Item", [])
        for item in items:
            if item.get("Name") == "Amount":
                amount = item.get("Value")
            elif item.get("Name") == "PhoneNumber":
                phone_number = item.get("Value")

        payment, created = Payment.objects.update_or_create(
            transaction_id=checkout_request_id,
            defaults={
                "payment_status": "Success" if result_code == 0 else "Failed",
                "amount": amount,
                "payer": User.objects.filter(phone_number=phone_number).first(),
                "result_code": result_code,
                "result_desc": result_desc,
            }
        )
        return HttpResponse('Callback received', status=200)
    return HttpResponse(status=405)

