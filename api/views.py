from django.http import JsonResponse
import json
import re
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from .models import User, Item, Invoice, InvoiceItem


# ---------------- SAFE JSON PARSER ----------------

def get_json_data(request):
    try:
        return json.loads(request.body)
    except:
        return None


# ---------------- REGISTER ----------------

@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"})

    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON data"})

    if User.objects.filter(username=data['username']).exists():
        return JsonResponse({"error": "Username exists"})

    if User.objects.filter(email=data['email']).exists():
        return JsonResponse({"error": "Email exists"})

    if not re.match(r'^[6-9]\d{9}$', data['phone']):
        return JsonResponse({"error": "Invalid phone number"})

    User.objects.create_user(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        phone=data['phone'],
        name=data['name']
    )

    return JsonResponse({"message": "Registered. Wait for admin approval"})


# ---------------- LOGIN ----------------

@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"})

    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON data"})

    user = authenticate(
        username=data['username'],
        password=data['password']
    )

    if user:
        if not user.is_approved:
            return JsonResponse({"error": "User not approved"})
        return JsonResponse({"message": "Login success", "user_id": user.id})

    return JsonResponse({"error": "Invalid credentials"})


# ---------------- ADD ITEM ----------------

@csrf_exempt
def add_item(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"})

    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON data"})

    if not re.match(r'^\d{6}$', data['hsn_sac']):
        return JsonResponse({"error": "HSN/SAC must be 6 digits"})

    Item.objects.create(
        name=data['name'],
        type=data['type'],
        hsn_sac=data['hsn_sac'],
        tax_type=data['tax_type'],
        price=data['price'],
        user_id=data['user_id']
    )

    return JsonResponse({"message": "Item added"})


# ---------------- GET ITEMS ----------------

@csrf_exempt
def get_items(request):
    items = list(Item.objects.values())
    return JsonResponse(items, safe=False)


# ---------------- DELETE ITEM ----------------

@csrf_exempt
def delete_item(request, id):
    Item.objects.filter(id=id).delete()
    return JsonResponse({"message": "Item deleted"})


# ---------------- CREATE INVOICE ----------------

@csrf_exempt
def create_invoice(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"})

    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON data"})

    invoice = Invoice.objects.create(
        user_id=data['user_id'],
        customer_name=data['customer_name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address']
    )

    for i in data['items']:
        InvoiceItem.objects.create(
            invoice=invoice,
            item_id=i['item_id'],
            quantity=i['quantity']
        )

    return JsonResponse({"message": "Invoice created"})


# ---------------- GET INVOICES ----------------

@csrf_exempt
def get_invoices(request):
    invoices = list(Invoice.objects.values())
    return JsonResponse(invoices, safe=False)


# ---------------- DELETE INVOICE ----------------

# @csrf_exempt
# def delete_invoice(request, id):
#     Invoice.objects.filter(id=id).delete()
#     return JsonResponse({"message": "Invoice deleted"})

@csrf_exempt
def delete_invoice(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Only DELETE allowed"})

    data = get_json_data(request)

    if not data or "user_id" not in data:
        return JsonResponse({"error": "User required"})

    try:
        invoice = Invoice.objects.get(id=id)

        # ✅ ONLY OWNER CAN DELETE
        if invoice.user_id != data["user_id"]:
            return JsonResponse({"error": "Not allowed"})

        invoice.delete()
        return JsonResponse({"message": "Invoice deleted"})

    except:
        return JsonResponse({"error": "Invoice not found"})