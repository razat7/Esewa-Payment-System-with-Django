from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from .models import *
from django.contrib import messages
import string 
import random
import hmac
import hashlib
import base64
import uuid

#Code Generator
def code_generator():
    length = 4
    pw  = string.ascii_letters+string.digits+string.ascii_uppercase
    gen_pw = ''.join(random.choice(pw)for _ in range(length))
    return gen_pw

#Signature Generator
def generate_signature(key, message):
    key = key.encode('utf-8')
    message = message.encode('utf-8')
 
    hmac_sha256 = hmac.new(key, message, hashlib.sha256)
    digest = hmac_sha256.digest()
 
    #Convert the digest to a Base64-encoded string
    signature = base64.b64encode(digest).decode('utf-8')
 
    return signature

# Create your views here.
def index_views(request):
    data = Product.objects.all()
    context = {'data': data}
    return render(request, "index.html", context)

def order_menu(request, food_id):
    data = Product.objects.get(id = food_id)

    if request.method == "POST":
        data = request.POST

        food_id = data.get("food_id")
        quantity = int(data.get("quantity"))
        customer_name = data.get("customer_name")
        phone = data.get("phone")
        address = data.get("address")

        order = Orders.objects.create(
            ordered_food = Product.objects.get(id = food_id),
            order_code = code_generator(),
            quantity = quantity,            
            customer_name = customer_name,
            phone = phone,
            address = address,
        )
        order.save()
        return redirect('checkout', order_id = order.id)

    context = {'data': data}    
    return render(request, "order_menu.html", context)

def checkout(request, order_id):
    product = Orders.objects.get(id = order_id)

    transaction_uuid = uuid.uuid4()
    tax_amount = 10  
    total_amount = product.price + tax_amount
    secret_key = '8gBm/:&EnhH.1/q'
    data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code=EPAYTEST"
    result = generate_signature(secret_key, data_to_sign)

    context = {
        'product': product,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'transaction_uuid': transaction_uuid,
        'product_delivery_charge': 0,
        'product_service_charge': 0,
        'signature': result,
        
    }
    return render(request, "checkout.html", context)