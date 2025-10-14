import requests
import base64
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Payment


def get_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    return response_data.get("access_token")

@csrf_exempt
def lipa_na_mpesa_online(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    data = json.loads(request.body)
    phone_number = data.get('phone')
    amount = data.get('amount')
    if not phone_number or not amount:
        return JsonResponse({'error': 'Phone number and amount required'}, status=400)

    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        (settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_STK_CALLBACK_URL,
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }

    response = requests.post(api_url, headers=headers, json=payload)
    return JsonResponse(response.json())


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
            if item.get("Name") == "PhoneNumber":
                phone_number = item.get("Value")

        payment, created = Payment.objects.update_or_create(
            transaction_id=checkout_request_id,
            defaults={
                "phone_number": phone_number,
                "amount": amount,
                "status": "Success" if result_code == 0 else "Failed",
                "result_code": result_code,
                "result_desc": result_desc,
            }
        )
        return HttpResponse('Callback received', status=200)
    return HttpResponse(status=405)


@csrf_exempt
def c2b_validation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        response = {"ResultCode": 0, "ResultDesc": "Accepted"}
        return JsonResponse(response)
    return HttpResponse(status=405)


@csrf_exempt
def c2b_confirmation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("C2B Confirmation:", data) 
        return HttpResponse("Received", status=200)
    return HttpResponse(status=405)
