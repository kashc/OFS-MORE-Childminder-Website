"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- URLs --

@author: Informed Solutions
"""
import re

from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf import settings

from application import views, magic_link

urlpatterns = [
    url(r'^$', views.start_page, name='start-page.html'),
    url(r'^task-list/', views.log_in, name='morebeta'),
    url(r'^childcare/', views.type_of_childcare, name='Type-Of-Childcare-View'),
    url(r'^account/email/', views.contact_email, name='Contact-Email-View'),
    url(r'^account/phone/', views.contact_phone, name='Contact-Phone-View'),
    url(r'^account/summary/', views.contact_summary, name='Contact-Summary-View'),
    url(r'^account/question/', views.contact_question, name='Question-View'),
    url(r'^account/account/', views.account_selection, name='Account-View'),
    url(r'^personal-details/guidance/', views.personal_details_guidance, name='Personal-Details-Guidance-View'),
    url(r'^personal-details/name/', views.personal_details_name, name='Personal-Details-Name-View'),
    url(r'^personal-details/dob/', views.personal_details_dob, name='Personal-Details-DOB-View'),
    url(r'^personal-details/home-address/', views.personal_details_home_address,
        name='Personal-Details-Home-Address-View'),
    url(r'^personal-details/location-of-care/', views.personal_details_location_of_care,
        name='Personal-Details-Location-Of-Care-View'),
    url(r'^personal-details/childcare-address/', views.personal_details_childcare_address,
        name='Personal-Details-Childcare-Address-View'),
    url(r'^personal-details/summary/', views.personal_details_summary, name='Personal-Details-Summary-View'),
    url(r'^first-aid/guidance/', views.first_aid_training_guidance, name='First-Aid-Training-Guidance-View'),
    url(r'^first-aid/details/', views.first_aid_training_details, name='First-Aid-Training-Details-View'),
    url(r'^first-aid/declaration/', views.first_aid_training_declaration, name='First-Aid-Training-Declaration-View'),
    url(r'^first-aid/renew/', views.first_aid_training_renew, name='First-Aid-Training-Renew-View'),
    url(r'^first-aid/training/', views.first_aid_training_training, name='First-Aid-Training-Training-View'),
    url(r'^first-aid/summary/', views.first_aid_training_summary, name='First-Aid-Training-Summary-View'),
    url(r'^eyfs/', views.eyfs, name='EYFS-View'),
    url(r'^dbs-check/guidance/', views.dbs_check_guidance, name='DBS-Check-Guidance-View'),
    url(r'^dbs-check/dbs-details/', views.dbs_check_dbs_details, name='DBS-Check-DBS-Details-View'),
    url(r'^dbs-check/upload-dbs/', views.dbs_check_upload_dbs, name='DBS-Check-Upload-DBS-View'),
    url(r'^dbs-check/summary/', views.dbs_check_summary, name='DBS-Check-Summary-View'),
    url(r'^health/intro/', views.health_intro, name='Health-Intro-View'),
    url(r'^health/booklet/', views.health_booklet, name='Health-Booklet-View'),
    url(r'^health/check-answers/', views.health_check_answers, name='Health-Check-Answers-View'),
    url(r'^references/', views.references, name='References-View'),
    url(r'^other-people/', views.other_people, name='Other-People-View'),
    url(r'^declaration/', views.declaration, name='Declaration-View'),
    url(r'^confirm-your-answers/', views.confirmation, name='Confirmation-View'),
    url(r'^payment/', views.payment_view, name='Payment-View'),
    url(r'^payment-details/', views.card_payment_details, name='Payment-Details-View'),
    url(r'^application-saved/', views.application_saved, name='Application-Saved-View'),
    url(r'^admin/', admin.site.urls),
    url(r'^reset/', views.reset),
    url(r'^existing-application/', magic_link.existing_application, name='Existing-Application'),
    url(r'^validate/(?P<id>[\w-]+)/$', magic_link.validate_magic_link),
    url(r'^verify-phone/', magic_link.sms_verification),
    url(r'^email-sent/', TemplateView.as_view(template_name='email-sent.html')),
    url(r'^start/', views.start_page),
    url(r'^confirmation/', TemplateView.as_view(template_name='payment-confirmation.html')),
    url(r'^code-expired/', TemplateView.as_view(template_name='code-expired.html')),
    url(r'^bad-link/', TemplateView.as_view(template_name='bad-link.html')),
    url(r'^link-resolution-error/', TemplateView.as_view(template_name='link-resolution-error.html')),
]

if settings.URL_PREFIX:
    prefixed_url_pattern = []
    for pat in urlpatterns:
        pat.regex = re.compile(r"^%s/%s" % (settings.URL_PREFIX[1:], pat.regex.pattern[1:]))
        prefixed_url_pattern.append(pat)
    urlpatterns = prefixed_url_pattern
