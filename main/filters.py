from .models import Company, Branch, Invoice, InvoiceMaterial
import django_filters

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
# https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html


class CompaniesFilter(django_filters.FilterSet):
    name = first_name = django_filters.CharFilter(lookup_expr='icontains', label="الاسم")

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        data.setdefault('format', 'paperback')
        data.setdefault('order', '-added')
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = Company
        fields = ['name']



