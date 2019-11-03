from django.db import models
from django.contrib.auth import get_user_model

from model_utils.models import TimeStampedModel
from django.urls import reverse
import uuid
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from decimal import Decimal
from django.urls import reverse


class Company(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30, unique=True)
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE)

    def get_absolute_url(self):
        # return reverse('customer_profile', args=[str(self.uid)])
        return reverse("company-detail", args=[str(self.uid)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class Branch(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=30)
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE)

    def get_absolute_url(self):
        return reverse("company-detail", args=[str(self.company.uid)])

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company", "name"),)


class Material(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE)

    def get_absolute_url(self):
        return reverse("material-list")

    def __str__(self):
        return self.name


class Invoice(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="invoices")
    invoice_number = models.CharField(max_length=20, unique=True)
    print_count = models.PositiveIntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     if not self.invoice_number:
    #         company = self.branch.company
    #         self.invoice_number = "number"
    #         self.invoice_number.save()
    #
    #     super(Invoice, self).save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse("invoice-detail", args=[str(self.uid)])

    def __str__(self):
        return f"{self.branch.name} - {self.invoice_number}"


class InvoiceDetail(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_details")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="invoice_details")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_date = models.DateField()
    output_number = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse("material-order-detail",  args=[str(self.uid)])

    def __str__(self):
        return f"{self.material.name} - {self.invoice.invoice_number}"
