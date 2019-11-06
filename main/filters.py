from .models import Company, Branch, Invoice, InvoiceDetail
import django_filters
from django.views import generic
from . import choices

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
# https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html


class CompaniesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="الاسم")
    status = django_filters.ChoiceFilter(label="الحالة", choices=choices.STATUS_CHOICE, empty_label="الكل")

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', '-added')

        # if not data['status']:
        #     data['status'] = choices.ACTIVE

        super().__init__(data, *args, **kwargs)
    class Meta:
        model = Company
        fields = ['name', 'status']





class FilteredListView(generic.ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class InvoiceFilterSet(django_filters.FilterSet):
    invoice_number = django_filters.CharFilter(lookup_expr='icontains', label="رقم الفاتورة")
    status = django_filters.ChoiceFilter(label="الحالة", choices=choices.STATUS_CHOICE, empty_label="الكل")

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', '-added')
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = Invoice
        fields = ['invoice_number']
