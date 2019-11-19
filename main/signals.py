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


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = f"{filename}-{counter}{extension}"
        counter += 1

    return path

@receiver(post_save, sender=Invoice)
def save_invoice_pdf(sender, instance, created, **kwargs):
    invoice_number = instance.invoice_number
    branch_folder_path = instance.branch.folder_path

    pdf_path = f"{branch_folder_path}/{invoice_number}.pdf"

    invoice_details = instance.invoice_details.all().order_by("material")
    grand_total = Decimal(0.0)

    for item in invoice_details:
        grand_total += item.total

    template = render_to_string("main/weasy.html", {
        'invoice': instance,
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
        unique_path = uniquify(pdf_path)

        html.write_pdf(target=unique_path, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])
        #
        # copy to backup
        shutil.copy2(unique_path, settings.BACKUP_ROOT)



