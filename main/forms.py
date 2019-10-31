from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import Company, Branch, Material, Invoice, MaterialOrder
from django.forms.models import inlineformset_factory
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



class MaterialOrderForm(ModelForm):
    # material = forms.ModelChoiceField(Material.objects.all(), empty_label='None', required=False, label='المادة')


    class Meta:
        model = MaterialOrder
        fields = ('qtn', 'price', 'delivery_date', 'output_number')

    # def __init__(self, *args, **kwargs):
    #     super(InvoiceMaterialForm, self).__init__(*args, **kwargs)
    #     self.fields['material'].queryset = Material.objects.all()


    # make sure the that form is not empty
    def __init__(self, *arg, **kwarg):
        super(MaterialOrderForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False


 # fields=[ 'qtn', 'price', 'delivery_date', 'output_number'],
InvoiceMaterialFormSet = inlineformset_factory(
    Material, MaterialOrder, form=MaterialOrderForm, fields=[ 'qtn', 'price', 'delivery_date', 'output_number'],
   extra=1, can_delete=True # fields for child thats why no material
    )

