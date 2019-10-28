from django.urls import path
from .views import home, CompanyCreateView, CompanyDetailView, CompanyUpdateView
from .views import BranchCreateView, BranchUpdateView
from .views import MaterialListView, MaterialCreateView, MaterialUpdateView
from .views import InvoiceCreateView, InvoiceDetailView, InvoiceUpdateView

urlpatterns = [
    path("", home, name="home"),
    path("company/create", CompanyCreateView.as_view(), name="company-create"),
    path("company/<uuid:uid>", CompanyDetailView.as_view(), name="company-detail"),
    path("company/<uuid:uid>/edit", CompanyUpdateView.as_view(), name="company-update"),
    path("company/<uuid:uid>/delete", CompanyDetailView.as_view(), name="company-delete"),

    path("company/<uuid:uid>/add_branch", BranchCreateView.as_view(), name="branch-create"),
    path("company/update_branch/<uuid:uid>", BranchUpdateView.as_view(), name="branch-update"),


    path("materials", MaterialListView.as_view(), name="material-list"),
    path("material/create", MaterialCreateView.as_view(), name="material-create"),
    path("material/<uuid:uid>/edit", MaterialUpdateView.as_view(), name="material-update"),

    path("branch/<uuid:uid>/invoice_create", InvoiceCreateView.as_view(), name="invoice-create"),
    path("branch/invoice_create/<uuid:uid>", BranchUpdateView.as_view(), name="invoice-update"),

]
