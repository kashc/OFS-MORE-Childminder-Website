"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- status.py --

@author: Informed Solutions
"""

from .models import Application


def update(application_id, field_name, status):
    """
    Method to update task status
    :param application_id: application ID
    :param field_name: status to update
    :param status: status
    :return:
    """
    local_application = Application.objects.get(pk=application_id)
    setattr(local_application, field_name, status)
    local_application.save()
