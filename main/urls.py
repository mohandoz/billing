from django.urls import path
from .views import home, CompanyCreateView, CompanyDetailView, CompanyUpdateView
from .views import BranchListView, BranchCreateView, BranchUpdateView
from .views import MaterialListView, MaterialCreateView, MaterialUpdateView
from .views import InvoiceCreateView, InvoiceDetailView, InvoiceUpdateView
from .views import InvoiceListView, BranchInvoiceListView, CompanyInvoiceListView
from .views import InvoicePdfView, InvoicePdfWithoutPriceView, InvoiceHtml
from .views import UsersListView, UserCreateView,  UserUpdateView

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

    path("branches", BranchListView.as_view(), name="branch-list"),
    path("branch/<uuid:uid>/invoice_create", InvoiceCreateView.as_view(), name="invoice-create"),
    path("branch/invoice/<uuid:uid>", InvoiceDetailView.as_view(), name="invoice-detail"),
    path("branch/invoice_update/<uuid:uid>", InvoiceUpdateView.as_view(), name="invoice-update"),

    path("invoices/", InvoiceListView.as_view(), name="invoice-list"),
    path("branch/<uuid:uid>/invoices", BranchInvoiceListView.as_view(), name="branch-invoice-list"),
    path("company/<uuid:uid>/invoices", CompanyInvoiceListView.as_view(), name="company-invoice-list"),

    path("branch/invoice/<uuid:uid>/print_no_price", InvoicePdfWithoutPriceView.as_view(), name="invoice-print-without"),
    path("branch/invoice/<uuid:uid>/print", InvoicePdfView.as_view(), name="invoice-print"),
    path("branch/invoice/<uuid:uid>/preview", InvoiceHtml.as_view(), name="invoice-preview"),

    path("users_list", UsersListView.as_view(), name="users-list"),
    path("users_create", UserCreateView.as_view(), name="user-create"),
    path("users_list/<int:pk>/update", UserUpdateView.as_view(), name="user-update"),

]
