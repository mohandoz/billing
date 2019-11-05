from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import Company, Branch, Material, Invoice, InvoiceDetail
from django.forms.models import inlineformset_factory
from django.forms.widgets import Select

from django.forms import BaseInlineFormSet
# https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6

#=================== material form ==========================


# class MaterialForm(ModelForm):
#
#     class Meta:
#         model = Material
#         fields = ('name',)
#
#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if name == "":
#             raise forms.ValidationError("Enter name")
#         return name
#
#     # make sure the that form is not empty
#     def __init__(self, *arg, **kwarg):
#         super(MaterialForm, self).__init__(*arg, **kwarg)
#         self.empty_permitted = False
#
# class InvoiceMaterialForm(ModelForm):
#
#     class Meta:
#         model = InvoiceMaterial
#         fields = ('qtn', 'price', 'delivery_date', 'output_number')
#
#
#     # make sure the that form is not empty
#     def __init__(self, *arg, **kwarg):
#         super(InvoiceMaterialForm, self).__init__(*arg, **kwarg)
#         self.empty_permitted = False
# #
#
# # =================== material formset  ==========================
#
#
# MaterlModelFormset = modelformset_factory(
#     Material,
#     form=MaterialForm,
#     extra=1,
# )


class MaterialForm(ModelForm):

    class Meta:
        model = Material
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == "":
            raise forms.ValidationError("Enter name")
        return name

    # make sure the that form is not empty
    def __init__(self, *arg, **kwarg):
        super(MaterialForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ('branch', 'created_by')
        widgets = {'branch': forms.HiddenInput(), 'created_by': forms.HiddenInput(), }





class InvoiceDetailForm(ModelForm):
    # material = forms.ModelChoiceField(Material.objects.all(), empty_label='None', required=False, label='المادة')


    class Meta:
        model = InvoiceDetail
        fields = ('material','quantity', 'price', 'delivery_date', 'output_number')

    def __init__(self, *arg, **kwarg):
        super(InvoiceDetailForm, self).__init__(*arg, **kwarg)
        # self.empty_permitted = False

        self.fields['material'].choices = lambda: [('', '-- المادة --')] + [
                    (material.id, '%s ' % (material.name)) for material in
                    Material.objects.order_by('name')]


 # fields=[ 'qtn', 'price', 'delivery_date', 'output_number'],
InvoiceDetailFormSet = inlineformset_factory(
    Invoice, InvoiceDetail, form=InvoiceDetailForm, extra=1,    validate_min=True,
    can_delete=False)

InvoiceUpdateFormSet = inlineformset_factory(
    Invoice, InvoiceDetail, form=InvoiceDetailForm, extra=0,    validate_min=True,
    can_delete=True)
