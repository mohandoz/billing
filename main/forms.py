from django import forms
from django.forms import ModelForm, modelformset_factory
from .models import Company, Branch, Material, Invoice, InvoiceMaterial
from django.forms.models import inlineformset_factory

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



class InvoiceMaterialForm(ModelForm):
    mat = forms.ModelChoiceField(Material.objects.all(), empty_label='None', required=False, label='المادة')


    class Meta:
        model = InvoiceMaterial
        fields = ('mat', 'qtn', 'price', 'delivery_date', 'output_number')


    # make sure the that form is not empty
    # def __init__(self, *arg, **kwarg):
    #     super(InvoiceMaterialForm, self).__init__(*arg, **kwarg)
    #     self.empty_permitted = False


InvoiceMaterialFormSet = inlineformset_factory(
    Material, InvoiceMaterial, form=InvoiceMaterialForm,
    fields=['mat', 'qtn', 'price', 'delivery_date', 'output_number'], extra=1, can_delete=True
    )
