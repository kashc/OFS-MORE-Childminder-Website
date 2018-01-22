from django.conf import settings
from django.contrib.sites import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import VerifySecurityQuestionForm
from .models import Application, UserDetails


def load(request):
    application_id_local = request.GET['id']
    form = VerifySecurityQuestionForm(id=application_id_local)
    if request.method == 'POST':
        # Retrieve the application's ID
        application_id_local = request.POST["id"]
        # Initialise the Your login and contact details form
        form = VerifySecurityQuestionForm(request.POST, id=application_id_local)
        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            # Return to the application's task list
            return HttpResponseRedirect('/account/summary?id=' + application_id_local)

        # If there are invalid details
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'login_details_status': "true"
            }
            # Return to the same page
            return render(request, 'security_question.html', variables)
    return render(request, 'security_question.html', {'form': form, 'application_id':id})