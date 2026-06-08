from django.db import models
from django.contrib.auth.models import AbstractUser
import re
from django.core.exceptions import ValidationError


# HSN/SAC validation (6 digits)
def validate_hsn(value):
    if not re.match(r'^\d{6}$', value):
        raise ValidationError("HSN/SAC must be 6 digits")


# ---------------- USER ----------------
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# ---------------- ITEM ----------------
class Item(models.Model):
    TYPE_CHOICES = (
        ('GOODS', 'Goods'),
        ('SERVICE', 'Service'),
    )

    TAX_CHOICES = (
        ('TAXABLE', 'Taxable'),
        ('NON_TAXABLE', 'Non Taxable'),
    )

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    hsn_sac = models.CharField(max_length=6, validators=[validate_hsn])
    tax_type = models.CharField(max_length=20, choices=TAX_CHOICES)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# ---------------- INVOICE ----------------
class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


# ---------------- INVOICE ITEM ----------------
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)