from django.contrib import admin
from .models import Company, Branch, Material, Invoice, MaterialOrder

admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(Material)
admin.site.register(Invoice)
admin.site.register(MaterialOrder)
