import json
import random
import requests
import string
import time
import traceback
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import SecurityQuestion
from .models import Application


def start(request):
    id = "5cd88ea2-20c7-464f-895d-ed78166c44cb"
    return HttpResponseRedirect('/security_question?id='+id)


def load(request):
    if request.method == 'GET':
        # If the Your login and contact details form is not completed
        application_id_local = request.GET["id"]
        form = SecurityQuestion(id=application_id_local)
        # Retrieve application from database for Back button/Return to list link logic
        application = Application.objects.get(pk=application_id_local)
        # Access the task page
        return render(request, 'security_question.html', {'form': form, 'application_id': application_id_local,
                                                 'login_details_status': application.login_details_status})

    if request.method == 'POST':
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        # Initialise the Your login and contact details form
        form = SecurityQuestion(request.POST, id=application_id_local)
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            # Return to the application's task list
            return HttpResponseRedirect('/account/summary?id=' + application_id_local)

        # If there are invalid details
        else:
            variables = {
                'form': form,
                'application_id': application_id_local
            }
            # Return to the same page
            return render(request, 'security_question.html', variables)
