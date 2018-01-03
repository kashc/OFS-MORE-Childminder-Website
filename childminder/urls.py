"""morebeta URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from application import views, magic_link, payment


urlpatterns = [
    url(r'^$',views.StartPageView, name='start-page.html'),
    url(r'^task-list/', views.LogInView, name='morebeta'),
    url(r'^childcare/', views.TypeOfChildcareView, name='Type-Of-Childcare-View'),
    url(r'^account/email/', views.ContactEmailView, name='Contact-Email-View'),
    url(r'^account/phone/', views.ContactPhoneView, name='Contact-Phone-View'),
    url(r'^account/summary/', views.ContactSummaryView, name='Contact-Summary-View'),
    url(r'^account/question/', views.QuestionView, name='Question-View'),
    url(r'^personal-details/guidance/', views.PersonalDetailsGuidanceView, name='Personal-Details-Guidance-View'),
    url(r'^personal-details/name/', views.PersonalDetailsNameView, name='Personal-Details-Name-View'),
    url(r'^personal-details/dob/', views.PersonalDetailsDOBView, name='Personal-Details-DOB-View'),
    url(r'^personal-details/home-address/', views.PersonalDetailsHomeAddressView, name='Personal-Details-Home-Address-View'),
    url(r'^first-aid/', views.FirstAidTrainingView, name='First-Aid-Training-View'),
    url(r'^eyfs/', views.EYFSView, name='EYFS-View'),
    url(r'^dbs-check/', views.DBSCheckView, name='DBS-Check-View'),
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
    url(r'^existing-application/',views.existingApplicationView, name='Existing-Application'),
    url(r'^test/', magic_link.start, name='testing'),
    url(r'^test2/', payment.start),
    url(r'^start/', views.StartPageView),

]