'''
Created on 13 Dec 2017

@author: geevesh
'''
from application.models import Application



def update(application_id, field_name, status):
    local_application = Application.objects.get(pk = application_id)
    setattr(local_application, field_name, status)
    local_application.save()

