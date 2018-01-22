from django.conf import settings
from django.contrib.sites import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .middleware import CustomAuthenticationHandler
from .forms import VerifySecurityQuestionForm
from .models import Application, UserDetails


def load(request):
    application_id_local = request.GET['id']
    # Initialise the Your login and contact details form
    form = VerifySecurityQuestionForm(request.POST, id=application_id_local)
    application = Application.objects.get(pk=application_id_local)
    login_id = application.login_id.login_id
    acc = UserDetails.objects.get(login_id=login_id)
    security_question = acc.security_question
    if request.method == 'POST':

        # If the form is successfully submitted (with valid details)
        if form.is_valid():
            # Return to the application's task list

            if acc.security_answer == form.clean_security_answer():
                print("SUCCESS")
                response = HttpResponseRedirect(
                    settings.URL_PREFIX + '/task-list/?id=' + str(application.application_id))
                # Create session issue custom cookie to user
                CustomAuthenticationHandler.create_session(response, application.login_id.email)
                # Forward back onto application
                return response

        # If there are invalid details
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'login_details_status': "true"
            }
            # Return to the same page
            return render(request, 'security_question.html', variables)
    return render(request, 'security_question.html', {'form': form, 'application_id':application_id_local, 'question':security_question})