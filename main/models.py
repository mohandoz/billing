from django.db import models
from django.contrib.auth import get_user_model

from model_utils.models import TimeStampedModel
import uuid
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import *
from decimal import Decimal
from django.urls import reverse
from django.db import IntegrityError


class Company(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30, unique=True, verbose_name="اسم الشركة")
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE, verbose_name="الحالة")

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
    name = models.CharField(max_length=30, verbose_name="اسم الفرع")
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE, verbose_name="الحالة")

    def get_absolute_url(self):
        return reverse("company-detail", args=[str(self.company.uid)])

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (("company", "name"),)


class Material(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30,  verbose_name="اسم المادة")
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE, verbose_name="الحالة")

    def get_absolute_url(self):
        return reverse("material-list")

    def __str__(self):
        return self.name


class Invoice(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="invoices")
    invoice_number = models.CharField(max_length=20, blank=True,unique=True,  verbose_name="رقم الفاتورة")
    print_count = models.PositiveIntegerField(default=0,  verbose_name="عداد الطباعة")
    status = models.PositiveIntegerField(choices=STATUS_CHOICE, default=ACTIVE, verbose_name="الحالة")


    def save(self, *args, **kwargs):
        if not self.invoice_number:
            success = False
            branch_invoice_count = self.branch.invoices.all().count()
            while not success:
                try:
                    company_id = self.branch.company.id
                    branch_id = self.branch.id

                    now = datetime.datetime.now()
                    year = now.year
                    month = now.month
                    day = now.day

                    self.invoice_number = f"{year}{month}{day}{company_id}{branch_id}{branch_invoice_count}"

                    success = True
                except IntegrityError:
                    branch_invoice_count += 1



        super(Invoice, self).save(*args, **kwargs)



    def get_absolute_url(self):
        return reverse("invoice-detail", args=[str(self.uid)])

    def __str__(self):
        return f"{self.branch.name} - {self.invoice_number}"


class InvoiceDetail(TimeStampedModel):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_details")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="invoice_details")
    quantity = models.PositiveIntegerField(verbose_name="الكمية")
    price = models.DecimalField(max_digits=6, decimal_places=2,  verbose_name="السعر")
    total = models.DecimalField(max_digits=6, decimal_places=2, blank=True,  verbose_name="الاجمالي")
    delivery_date = models.DateField(verbose_name="تاريخ التسليم")
    output_number = models.PositiveIntegerField(verbose_name="رقم الاخراج")

    def get_absolute_url(self):
        return reverse("material-order-detail",  args=[str(self.uid)])

    def __str__(self):
        return f"{self.material.name} - {self.invoice.invoice_number}"

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super(InvoiceDetail, self).save(*args, **kwargs)

