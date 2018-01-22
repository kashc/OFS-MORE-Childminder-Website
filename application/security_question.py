from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import VerifySecurityQuestionForm
from .middleware import CustomAuthenticationHandler
from .models import Application, UserDetails


def load(request):
    """
    Method returning the template for the security question verification page
    and navigating to the corresponding task list when successfully completed
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered security question verification template
    """
    if request.method == 'GET':
        application_id_local = request.GET['id']
        form = VerifySecurityQuestionForm(id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        login_id = application.login_id.login_id
        acc = UserDetails.objects.get(login_id=login_id)
        security_question = acc.security_question
        return render(request, 'security_question.html',
                      {'form': form, 'application_id': application_id_local, 'question': security_question})
    if request.method == 'POST':
        application_id_local = request.POST['id']
        form = VerifySecurityQuestionForm(request.POST, id=application_id_local)
        application = Application.objects.get(pk=application_id_local)
        login_id = application.login_id.login_id
        acc = UserDetails.objects.get(login_id=login_id)
        security_question = acc.security_question
        if form.is_valid():
            if acc.security_answer == form.clean_security_answer():
                print("SUCCESS")
                response = HttpResponseRedirect(
                    settings.URL_PREFIX + '/task-list/?id=' + str(application.application_id))
                # Create session issue custom cookie to user
                CustomAuthenticationHandler.create_session(response, application.login_id.email)
                return response
        else:
            variables = {
                'form': form,
                'application_id': application_id_local,
                'question': security_question
            }
            return render(request, 'security_question.html', variables)
