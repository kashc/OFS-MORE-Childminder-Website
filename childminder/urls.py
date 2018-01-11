"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- URLs --

@author: Informed Solutions
"""


from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from application import magic_link, views


urlpatterns = [
    url(r'^$',views.StartPageView, name='start-page.html'),
    url(r'^task-list/', views.LogInView, name='morebeta'),
    url(r'^childcare/', views.TypeOfChildcareView, name='Type-Of-Childcare-View'),
    url(r'^account/email/', views.ContactEmailView, name='Contact-Email-View'),
    url(r'^account/phone/', views.ContactPhoneView, name='Contact-Phone-View'),
    url(r'^account/summary/', views.ContactSummaryView, name='Contact-Summary-View'),
    url(r'^account/question/', views.QuestionView, name='Question-View'),
    url(r'^account/account/', views.AccountView, name='Account-View'),
    url(r'^personal-details/guidance/', views.PersonalDetailsGuidanceView, name='Personal-Details-Guidance-View'),
    url(r'^personal-details/name/', views.PersonalDetailsNameView, name='Personal-Details-Name-View'),
    url(r'^personal-details/dob/', views.PersonalDetailsDOBView, name='Personal-Details-DOB-View'),
    url(r'^personal-details/home-address/', views.PersonalDetailsHomeAddressView, name='Personal-Details-Home-Address-View'),
    url(r'^personal-details/location-of-care/', views.PersonalDetailsLocationOfCareView, name='Personal-Details-Location-Of-Care-View'),
    url(r'^personal-details/childcare-address/', views.PersonalDetailsChildcareAddressView, name='Personal-Details-Childcare-Address-View'),
    url(r'^personal-details/summary/', views.PersonalDetailsSummaryView, name='Personal-Details-Summary-View'),
    url(r'^first-aid/guidance/', views.FirstAidTrainingGuidanceView, name='First-Aid-Training-Guidance-View'),
    url(r'^first-aid/details/', views.FirstAidTrainingDetailsView, name='First-Aid-Training-Details-View'),
    url(r'^first-aid/declaration/', views.FirstAidTrainingDeclarationView, name='First-Aid-Training-Declaration-View'),
    url(r'^first-aid/renew/', views.FirstAidTrainingRenewView, name='First-Aid-Training-Renew-View'),
    url(r'^first-aid/training/', views.FirstAidTrainingTrainingView, name='First-Aid-Training-Training-View'),
    url(r'^first-aid/summary/', views.FirstAidTrainingSummaryView, name='First-Aid-Training-Summary-View'),    
    url(r'^eyfs/', views.EYFSView, name='EYFS-View'),
    url(r'^dbs-check/guidance/', views.dbs_check_guidance_view, name='DBS-Check-Guidance-View'),
    url(r'^dbs-check/dbs-details/', views.dbs_check_dbs_details_view, name='DBS-Check-DBS-Details-View'),
    url(r'^dbs-check/upload-dbs/', views.dbs_check_upload_dbs_view, name='DBS-Check-Upload-DBS-View'),
    url(r'^dbs-check/summary/', views.dbs_check_summary_view, name='DBS-Check-Summary-View'),
    url(r'^health/', views.HealthView, name='Health-View'),
    url(r'^references/', views.ReferencesView, name='References-View'),
    url(r'^other-people/', views.OtherPeopleView, name='Other-People-View'),
    url(r'^declaration/', views.DeclarationView, name='Declaration-View'),
    url(r'^confirm-your-answers/', views.ConfirmationView, name='Confirmation-View'),
    url(r'^payment/', views.PaymentView, name='Payment-View'),
    url(r'^payment-details/', views.CardPaymentDetailsView, name='Payment-Details-View'),
    url(r'^application-saved/', views.ApplicationSavedView, name='Application-Saved-View'),
    url(r'^admin/', admin.site.urls),
    url(r'^reset/', views.ResetView),
    url(r'^existing-application/',magic_link.existingApplicationView, name='Existing-Application'),
    url(r'^validate/(?P<id>[\w-]+)/$', magic_link.validateMagicLink), #This is curr checking that the parameter is a phone number
    url(r'^verifyPhone/', magic_link.SMSVerification),
    url(r'^email-sent/', TemplateView.as_view(template_name = 'email-sent.html')),
    url(r'^start/', views.StartPageView),
    url(r'^confirmation/', TemplateView.as_view(template_name = 'payment-confirmation.html')),
    url(r'^code-expired/', TemplateView.as_view(template_name='code-expired.html')),
    url(r'^bad-link/', TemplateView.as_view(template_name='bad-link.html')),
    url(r'^link-resolution-error/', TemplateView.as_view(template_name='link-resolution-error.html')),
]