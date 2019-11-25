from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Company, Branch, Material, Invoice, InvoiceDetail
from .filters import FilteredListView, CompaniesFilter, BranchFilter, InvoiceFilterSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import get_object_or_404
from django.views import generic
from .choices import *
# from .forms import MaterialForm, MaterlModelFormset
from .forms import InvoiceForm, InvoiceUpdateForm, InvoiceDetailForm, InvoiceDetailFormSet, InvoiceUpdateFormSet, MaterialForm
from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import InvoiceMixin, FormsetMixin
from django.views import View
from django.contrib.auth import get_user_model
USER_MODEL = get_user_model()

from billing.users.forms import UserCreationForm



# print
from django.http import HttpResponse, HttpResponseRedirect
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from django.template.loader import render_to_string

from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
import os
from .utils import check_folder_exist_create

from django.core.exceptions import ValidationError


@login_required
def home(request):
    template_name = "main/home.html"

    if request.method == 'GET':
        # django filter
        search_option = request.GET.get('search-option')
        SEARCH_CHOICE = (10, 25, 50, 100)

        if search_option:
            search_option = int(search_option)
            if search_option not in SEARCH_CHOICE:
                search_option = 10

        else:
            search_option = 10

        companies_list = Company.objects.all().order_by('status')
        companies_filter = CompaniesFilter(request.GET, queryset=companies_list)

        # paginator = Paginator(parent_filter.qs, 20)
        paginator = Paginator(companies_filter.qs, search_option)
        page = request.GET.get('page', 1)

        try:
            response = paginator.page(page)
        except PageNotAnInteger:
            response = paginator.page(1)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        return render(request, template_name,
                      {'search_option': search_option, 'filter': companies_filter, 'page': page, "response": response,
                       "active": "active"})


class CompanyCreateView(LoginRequiredMixin, generic.CreateView):
    model = Company
    fields = ["name", ]
    # template_name_suffix = '_create'



class CompanyDetailView(LoginRequiredMixin, generic.DetailView):
    model = Company
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    # def get_object(self):
    #     copmany = get_object_or_404(Company, stauts=self.kwargs['state'])
    #     return self.model.objects.filter(state=state)

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        company = self.object
        context['branches'] = company.branches.all()
        return context




class CompanyUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Company
    # template_name = "main/company_edit.html"
    fields = ["name", "status"]
    template_name_suffix = '_update'

    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class CompanyDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Company
    # template_name = "main/company_edit.html"
    fields = ["name",]
    template_name_suffix = '_edit'

    slug_field = 'uid'
    slug_url_kwarg = 'uid'

# Branches

class BranchCreateView(LoginRequiredMixin, generic.CreateView):
    model = Branch
    fields = ["name", ]


    def dispatch(self, request, *args, **kwargs):
        company_uid = kwargs.get("uid")
        self.company = get_object_or_404(Company, uid=company_uid)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BranchCreateView, self).get_context_data(**kwargs)
        company = self.company
        context['company'] = company
        return context

    def form_valid(self, form):
        form.instance.company = self.company

        # check branch if exsist
        new_beanch_name = form.cleaned_data.get("name")

        if self.company.branches.filter(name=new_beanch_name).exists():
            messages.error(self.request, f"الفرع موجود")
            return redirect("branch-create", uid=self.company.uid)

        return super().form_valid(form)



class BranchUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Branch
    fields = ["name", "status"]
    template_name_suffix = '_update'

    slug_field = 'uid'
    slug_url_kwarg = 'uid'

class BranchListView(LoginRequiredMixin, FilteredListView):
    model = Branch
    filterset_class = BranchFilter
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("status")




#  Materials

class MaterialListView(LoginRequiredMixin, generic.ListView):
    model = Material
    fields = ["name", "status"]

class MaterialCreateView(LoginRequiredMixin, generic.CreateView):
    model = Material
    fields = ["name", ]


class MaterialUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name_suffix = '_update'
    model = Material
    fields = ["name", "status"]

    slug_field = 'uid'
    slug_url_kwarg = 'uid'




class InvoiceCreateView(LoginRequiredMixin, InvoiceMixin, FormsetMixin, generic.CreateView):
    template_name = 'main/invoice_form.html'
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceDetailFormSet

    def dispatch(self, request, *args, **kwargs):
        branch = kwargs.get("uid")
        self.branch = get_object_or_404(Branch, uid=branch)
        if self.branch.status == INACTIVE:
            messages.error(request, 'المنشئة غير فعالة')

            return redirect('company-detail', uid=self.branch.company.uid)

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        created_by = self.request.user
        return {'branch': self.branch, 'created_by': created_by}

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        branch = self.branch
        company = branch.company
        context['branch'] = branch
        context['company'] = company
        return context

    

class InvoiceDetailView(generic.DetailView):
    model = Invoice
    fields = ["invoice_number", ]

    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def dispatch(self, request, *args, **kwargs):
        invoice_uid = kwargs.get("uid")
        self.invoice = get_object_or_404(Invoice, uid=invoice_uid)
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        items = self.invoice.invoice_details.all().order_by("material__name")
        grand_total = Decimal(0.0)

        for item in items:
            grand_total += item.total

        context['grand_total'] = grand_total
        return context




class InvoiceUpdateView(LoginRequiredMixin, InvoiceMixin, FormsetMixin, generic.UpdateView):
    is_update_view = True
    template_name = 'main/invoice_update_form.html'
    model = Invoice
    form_class = InvoiceUpdateForm
    formset_class = InvoiceUpdateFormSet
    slug_field = 'uid'
    slug_url_kwarg = 'uid'


    def get_context_data(self, **kwargs):
        context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
        branch = self.object.branch
        company = branch.company
        context['branch'] = branch
        context['company'] = company
        return context


# class InvoiceListView(LoginRequiredMixin, generic.ListView):
#     model = Invoice
#     paginate_by = 10
#     template_name = 'main/invoice_all_list.html'
#

class InvoiceListView(FilteredListView):
    model = Invoice
    filterset_class = InvoiceFilterSet
    paginate_by = 10
    template_name = 'main/invoice_list_all.html'



class BranchInvoiceListView(LoginRequiredMixin, FilteredListView):
    model = Invoice
    filterset_class = InvoiceFilterSet
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        branch_uid = kwargs.get("uid")
        self.branch = get_object_or_404(Branch, uid=branch_uid)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(branch=self.branch).order_by("status")

    def get_context_data(self, **kwargs):
        context = super(BranchInvoiceListView, self).get_context_data(**kwargs)
        branch = self.branch
        context['branch'] = branch
        return context


class CompanyInvoiceListView(LoginRequiredMixin, FilteredListView):
    model = Invoice
    filterset_class = InvoiceFilterSet
    paginate_by = 10
    template_name = 'main/invoice_list_company.html'

    def dispatch(self, request, *args, **kwargs):
        company_uid = kwargs.get("uid")
        self.company = get_object_or_404(Company, uid=company_uid)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(branch__company=self.company)


    def get_context_data(self, **kwargs):
        context = super(CompanyInvoiceListView, self).get_context_data(**kwargs)
        company = self.company
        context['company'] = company
        return context


class InvoicePdfView(View):
    def get(self, request, uid):
        invoice = get_object_or_404(Invoice, uid=uid)
        invoice_details = invoice.invoice_details.all().order_by("material")
        grand_total = Decimal(0.0)

        for item in invoice_details:
            grand_total += item.total

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f"inline; filename={invoice.invoice_number}.pdf"


        template = render_to_string("main/weasy.html", {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'grand_total': grand_total,

        })

        html = HTML(string=template)

        html.write_pdf(response, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])

        increment_print = invoice.print_count + 1
        Invoice.objects.filter(id=invoice.id).update(print_count= increment_print)


        return response


class InvoicePdfWithoutPirceًView(View):
    def get(self, request, uid):
        invoice = get_object_or_404(Invoice, uid=uid)
        invoice_details = invoice.invoice_details.all().order_by("material")
        grand_total = Decimal(0.0)

        for item in invoice_details:
            grand_total += item.total

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f"inline; filename={invoice.invoice_number}.pdf"


        html = render_to_string("main/weasy_without_price.html", {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'grand_total': grand_total,

        })

        HTML(string=html).write_pdf(response, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])

        increment_print = invoice.print_count + 1
        Invoice.objects.filter(id=invoice.id).update(print_count= increment_print)

        return response

class InvoiceHtml(View):
    def get(self, request, uid):
        invoice = get_object_or_404(Invoice, uid=uid)
        invoice_details = invoice.invoice_details.all()
        grand_total = Decimal(0.0)

        for item in invoice_details:
            grand_total += item.total

        response = HttpResponse(content_type="application/pdf")
        # response['Content-Disposition'] = f"inline; filename={invoice.invoice_number}.pdf"


        html = render_to_string("main/weasy.html", {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'grand_total': grand_total,
            'settings': settings.STATIC_URL,

        })

        # font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])

        return  render(request, 'main/weasy_preview.html', {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'grand_total': grand_total,
        })




class UsersListView(LoginRequiredMixin, generic.ListView):
    template_name = "main/users_list_app.html"
    model = USER_MODEL
    fields = ["username", "is_active", "is_staff"]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.exclude(username="admin")

class UserCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "main/user_create_app.html"
    form_class = UserCreationForm
    model = USER_MODEL
    # fields = ["username", "password"]

class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "main/user_update_app.html"
    model = USER_MODEL
    fields = ["is_active", ]
