from django.shortcuts import redirect
from django.db import transaction


from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

from django.template.loader import render_to_string

from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
from django.conf import settings


from .models import Invoice
import shutil

from django.db import transaction

class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            print("invalid")
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        print(form.errors, formset.errors)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class InvoiceMixin(object):



    def uniquify(self, path):
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = f"{filename}-{counter}{extension}"
            counter += 1

        return path

    def save_invoice_pdf(self, invoice):
        invoice_number = invoice.invoice_number
        branch_folder_path = invoice.branch.folder_path

        pdf_path = f"{branch_folder_path}/{invoice_number}.pdf"

        invoice_details = invoice.get_invoice_details()


        grand_total = Decimal(0.0)

        for item in invoice_details:
            grand_total += item.total

        template = render_to_string("main/weasy.html", {
            'invoice': invoice,
            'invoice_details': invoice_details,
            'grand_total': grand_total,
        })

        html = HTML(string=template)

        # new
        if not os.path.exists(pdf_path):


            html.write_pdf(target=pdf_path, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])

            # copy to backup
            shutil.copy2(pdf_path, settings.BACKUP_ROOT)

        # exist
        else:
            unique_path = self.uniquify(pdf_path)

            html.write_pdf(target=unique_path, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])
            #
            # copy to backup
            shutil.copy2(unique_path, settings.BACKUP_ROOT)




    def form_valid(self, form, formset):

        # formset.saveでインスタンスを取得できるように、既存データに変更が無くても更新対象となるようにする
        for detail_form in formset.forms:
            if detail_form.cleaned_data:
                detail_form.has_changed = lambda: True

        # インスタンスの取得
        invoice = form.save(commit=False)
        formset.instance = invoice
        details = formset.save(commit=False)

        # sub_total = 0
        #
        # # 明細に単価と合計を設定
        # for detail in details:
        #     detail.unit_price = detail.item.unit_price
        #     detail.amount = detail.unit_price * detail.quantity
        #     sub_total += detail.amount
        #
        # # 見出しに小計、消費税、合計、担当者を設定
        # tax = round(sub_total * 0.08)
        # total_amount = sub_total + tax
        #
        # invoice.sub_total = sub_total
        # invoice.tax = tax
        # invoice.total_amount = total_amount
        # invoice.created_by = self.request.user

        # DB更新
        with transaction.atomic():
            invoice.save()
            formset.instance = invoice
            formset.save()
                    

        self.save_invoice_pdf(invoice)
        # 処理後は詳細ページを表示zz


        return redirect(invoice.get_absolute_url())

