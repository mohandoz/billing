from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import TimeStampedModel
from django.urls import reverse
import uuid
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from decimal import Decimal

class Company(TimeStampedModel):
    name = models.CharField(max_length=30)
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE)

    def __str__(self):
        return self.name


class Branch(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=30)
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE)

    def __str__(self):
        return self.name


class Material(TimeStampedModel):
    name = models.CharField(max_length=30)
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE)

    def __str__(self):
        return self.name


class Invoice(TimeStampedModel):
    branch = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invoices")
    # todo it
    invoice_number = models.CharField(max_length=20)
    print_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.branch.name} - {self.invoice_number}"


class InvoiceMaterial(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_materials")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="invoice_materials")
    qtn = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_date = models.DateField()
    output_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.material.name}"
