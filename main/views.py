from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Company, Branch, Material, Invoice, InvoiceMaterial
from .filters import CompaniesFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import get_object_or_404
from django.views import generic
from .choices import *
# from .forms import MaterialForm, MaterlModelFormset
from .forms import InvoiceMaterialForm, InvoiceMaterialFormSet, MaterialForm
from django.db import transaction



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


class CompanyCreateView(generic.CreateView):
    model = Company
    fields = ["name", ]
    # template_name_suffix = '_create'



class CompanyDetailView(generic.DetailView):
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




class CompanyUpdateView(generic.UpdateView):
    model = Company
    # template_name = "main/company_edit.html"
    fields = ["name", "status"]
    template_name_suffix = '_update'

    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class CompanyDeleteView(generic.DeleteView):
    model = Company
    # template_name = "main/company_edit.html"
    fields = ["name",]
    template_name_suffix = '_edit'

    slug_field = 'uid'
    slug_url_kwarg = 'uid'

# Branches

class BranchCreateView(generic.CreateView):
    model = Branch
    fields = ["name", ]

    def dispatch(self, request, *args, **kwargs):
        company_uid = kwargs.get("uid")
        self.company = get_object_or_404(Company, uid=company_uid)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)


class BranchUpdateView(generic.UpdateView):
    model = Branch
    fields = ["name", "status"]
    template_name_suffix = '_update'

    slug_field = 'uid'
    slug_url_kwarg = 'uid'


#  Materials

class MaterialListView(generic.ListView):
    model = Material
    fields = ["name", "status"]

class MaterialCreateView(generic.CreateView):
    model = Material
    fields = ["name", ]

class MaterialUpdateView(generic.UpdateView):
    template_name_suffix = '_update'
    model = Material
    fields = ["name", "status"]

    slug_field = 'uid'
    slug_url_kwarg = 'uid'



class InvoiceCreateView(generic.CreateView):
    model = InvoiceMaterial
    fields = ["material", "qtn", "price", "delivery_date", "output_number"]
    template_name = 'main/invoice_form.html'


    def dispatch(self, request, *args, **kwargs):
        branch = kwargs.get("uid")
        self.branch = get_object_or_404(Branch, uid=branch)
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        branch_uid = self.kwargs.get("uid")
        branch = get_object_or_404(Branch, uid=branch_uid)


        with transaction.atomic():
            from uuid import uuid4
            x = str(uuid4())
            invoice = Invoice.objects.create(branch=self.branch, invoice_number=x[:5])

            form.instance.invoice = invoice

            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                print(formset.errors)

                return self.form_invalid(formset)



            return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = InvoiceMaterialFormSet(self.request.POST)
        else:
            context['formset'] = InvoiceMaterialFormSet()
        return context


class InvoiceDetailView(generic.DetailView):
    model = Invoice
    fields = ["invoice_number", ]

    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class InvoiceUpdateView(generic.UpdateView):
    model = Invoice
    fields = ["invoice_number", ]
    slug_field = 'uid'
    slug_url_kwarg = 'uid'






