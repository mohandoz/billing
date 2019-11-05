from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Company, Branch, Material, Invoice, InvoiceDetail
from .filters import CompaniesFilter, FilteredListView, InvoiceFilterSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import get_object_or_404
from django.views import generic
from .choices import *
# from .forms import MaterialForm, MaterlModelFormset
from .forms import InvoiceForm, InvoiceDetailForm, InvoiceDetailFormSet, InvoiceUpdateFormSet, MaterialForm
from django.db import transaction

from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import InvoiceMixin, FormsetMixin
from django.views import View


# print
from django.http import HttpResponse, HttpResponseRedirect
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from django.template.loader import render_to_string

from django.conf import settings

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

        companies_list = Company.objects.filter(status=ACTIVE).order_by('name')
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

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)


class BranchUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Branch
    fields = ["name", "status"]
    template_name_suffix = '_update'

    slug_field = 'uid'
    slug_url_kwarg = 'uid'


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


# class InvoiceCreateView(generic.CreateView):
#     model = InvoiceDetail
#     # fields = ["material", "qtn", "price", "delivery_date", "output_number"]
#     template_name = 'main/invoice_form.html'
#     form_class = InvoiceDetailFormSet
#
#
#
#     def dispatch(self, request, *args, **kwargs):
#         branch = kwargs.get("uid")
#         self.branch = get_object_or_404(Branch, uid=branch)
#         print("dispacth")
#         return super().dispatch(request, *args, **kwargs)
#
#     def form_invalid(self, form):
#         print(form.errors)
#         return super(InvoiceCreateView, self).form_invalid(form)


    # def form_valid(self, form):
    #     print("form_valid")
    #     print(self.object)
    #     context = self.get_context_data()
    #     formset = context['formset']
    #
        # branch_uid = self.kwargs.get("uid")
        # branch = get_object_or_404(Branch, uid=branch_uid)
    #
    #
    #
    #     with transaction.atomic():
    #         from uuid import uuid4
    #         x = str(uuid4())
    #         invoice = Invoice.objects.create(branch=self.branch, invoice_number=x[:5])
    #
    #
    #         if  form.is_valid() and formset.is_valid():
    #             formset.save(commit=False)
    #
    #             for form in formset:
    #                 form.save(commit=False)
    #                 form.invoice = invoice
    #                 # form.save()
    #
    #             formset.instance = self.object
    #             formset.save()
    #             print("Valid")
    #         else:
    #             print("invalid")
    #
    #             print(formset.errors)
    #             return self.form_invalid(form)
    #         print("return")
    #     return super(InvoiceCreateView, self).form_valid(form)

    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context['formset']
    #
    #     branch_uid = self.kwargs.get("uid")
    #     branch = get_object_or_404(Branch, uid=branch_uid)
    #
    #     from uuid import uuid4
    #     x = str(uuid4())
    #     invoice = Invoice.objects.create(branch=self.branch, invoice_number=x[:5])
    #
    #     with transaction.atomic():
    #         form.instance.invoice = invoice
    #         self.object = form.save()
    #
    #         if formset.is_valid():
    #             formset.instance.invoice = invoice
    #             formset.save()
    #     return super(InvoiceCreateView, self).form_valid(form)
    #
    #
    # def get_context_data(self, **kwargs):
    #     context = super(InvoiceCreateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['form'] = InvoiceDetailFormSet(self.request.POST)
    #     else:
    #         context['form'] = InvoiceDetailFormSet()
    #     return context


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
        items = self.invoice.invoice_details.all()
        grand_total = Decimal(0.0)

        for item in items:
            grand_total += item.total

        context['grand_total'] = grand_total
        return context




class InvoiceUpdateView(LoginRequiredMixin, InvoiceMixin, FormsetMixin, generic.UpdateView):
    is_update_view = True
    template_name = 'main/invoice_update_form.html'
    model = Invoice
    form_class = InvoiceForm
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
    template_name = 'main/invoice_all_list.html'



class BranchInvoiceListView(LoginRequiredMixin, generic.ListView):
    model = Invoice
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        branch_uid = kwargs.get("uid")
        self.branch = get_object_or_404(Branch, uid=branch_uid)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.branch.invoices.all().order_by("created")

    def get_context_data(self, **kwargs):
        context = super(BranchInvoiceListView, self).get_context_data(**kwargs)
        branch = self.branch
        context['branch'] = branch
        return context

class InvoicePdf(View):
    def get(self, request, uid):
        invoice = get_object_or_404(Invoice, uid=uid)
        invoice_details = invoice.invoice_details.all()
        grand_total = Decimal(0.0)

        for item in invoice_details:
            grand_total += item.total

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f"inline; filename={invoice.invoice_number}.pdf"


        html = render_to_string("main/weasy.html", {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'grand_total': grand_total,
            'settings': settings.STATIC_URL,

        })

        font_config = FontConfiguration()
        HTML(string=html).write_pdf(response, stylesheets=[f"{settings.STATIC_ROOT}/css/invoice.css"],font_config=font_config)

        invoice.print_count += 1
        invoice.save()

        return response




