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


def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = f"{filename}-{counter}{extension}"
        counter += 1

    return path

# @receiver(post_save, sender=Invoice)
# def save_invoice_pdf(sender, instance, created, **kwargs):
#     invoice_number = instance.invoice_number
#     branch_folder_path = instance.branch.folder_path

#     pdf_path = f"{branch_folder_path}/{invoice_number}.pdf"

#     invoice_details = instance.get_invoice_details()


#     grand_total = Decimal(0.0)

#     for item in invoice_details:
#         grand_total += item.total

#     template = render_to_string("main/weasy.html", {
#         'invoice': instance,
#         'invoice_details': invoice_details,
#         'grand_total': grand_total,
#     })

#     html = HTML(string=template)

#     # new
#     if not os.path.exists(pdf_path):


#         html.write_pdf(target=pdf_path, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])

#         # copy to backup
#         shutil.copy2(pdf_path, settings.BACKUP_ROOT)

#     # exist
#     else:
#         unique_path = uniquify(pdf_path)

#         html.write_pdf(target=unique_path, stylesheets=[f"{settings.STATIC_ROOT}/css/weasy.css"])
#         #
#         # copy to backup
#         shutil.copy2(unique_path, settings.BACKUP_ROOT)



# https://stackoverflow.com/questions/20895429/how-exactly-do-django-content-types-work
# from django.contrib.contenttypes.models import ContentType


# @receiver(post_save, sender=Invoice)
# def email_notify_orderform(sender, **kwargs):
#     instance = kwargs['instance']
#     ct = ContentType.objects.get_for_model(Invoice)
#     print(ct)
#     print(kwargs)
    
    # if ct.id == instance.content_type.id:
    #     print instance.is_addition()
    #     print instance.is_change()
    #     print instance.is_deletion()
    #     print instance.change_message
    #     print instance.action_time
    #     print instance.get_edited_object().total() # BINGO !
