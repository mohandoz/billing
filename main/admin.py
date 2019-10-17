from django.contrib import admin
from .models import Company, Branch, Invoice, InvoiceMaterial

admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Invoice)
admin.site.register(InvoiceMaterial)
