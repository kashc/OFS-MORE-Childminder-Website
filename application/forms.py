'''
Created on 7 Dec 2017
@author: Informed Solutions
'''
from django import forms

from .models import Application, Criminal_Record_Check, Login_And_Contact_Details

from govuk_forms.fields import SplitDateField
from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import InlineCheckboxSelectMultiple, InlineRadioSelect, \
    SeparatedCheckboxSelectMultiple, SeparatedRadioSelect
from application.models import Applicant_Names, Applicant_Personal_Details

class TypeOfChildcare(forms.Form):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    CHILDCARE_AGE_CHOICES = (
    ('0-5', 'Birth up to 5 years old'),
    ('5-8', '5 to 8 years old'),
    ('8over', '8 years and over'),
    )    
    type_of_childcare = forms.MultipleChoiceField(
        required=False,
        widget=InlineCheckboxSelectMultiple,
        choices=CHILDCARE_AGE_CHOICES,
        label = '',
        )
    
class ContactEmail(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    email_address = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(ContactEmail, self).__init__(*args, **kwargs)
        self.fields['email_address'].initial = Login_And_Contact_Details.objects.get(application_id=self.application_id_local).email
    
class PersonalDetails(GOVUKForm):
    options = (('yes', 'Yes'), ('no', 'No'))
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    first_name = forms.CharField(label='First name')
    middle_names = forms.CharField(label = 'Middle names (optional)',required=False)
    last_name = forms.CharField(label='Last name')
    name_change = forms.ChoiceField(label='Have you ever changed your name?', choices=options, widget=InlineRadioSelect)
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetails, self).__init__(*args, **kwargs)
        personal_detail_id = Applicant_Personal_Details.objects.get(application_id = self.application_id_local).personal_detail_id
        self.fields['first_name'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).first_name
        self.fields['middle_names'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).middle_names
        self.fields['last_name'].initial = Applicant_Names.objects.get(personal_detail_id=personal_detail_id).last_name
        self.fields['name_change'].initial = 'yes'

class FirstAidTraining(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    first_aid_training_organisation = forms.CharField(label='First aid training organisation')
    title_of_training_course = forms.CharField(label='Title of training course')
    course_date = forms.DateField(label='Course date')#, helptext='For example, 31 03 1980')    
    
class DBSCheck(GOVUKForm):
    options = (('True', 'Yes'), ('False', 'No'))
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    dbs_certificate_number = forms.IntegerField(label='DBS certificate number', help_text='12-digit number on your certificate')
    convictions = forms.ChoiceField(label='Do you have any cautions or convictions?', help_text='Include any information recorded on your certificate', choices=options, widget=InlineRadioSelect)
    
    def __init__(self, *args, **kwargs):
        super(DBSCheck, self).__init__(*args, **kwargs)
        self.fields['dbs_certificate_number'].initial = Criminal_Record_Check.objects.get(application_id='48629508-b1d6-481f-b528-23538f4022d3').dbs_certificate_number
        self.fields['convictions'].initial = Criminal_Record_Check.objects.get(application_id='48629508-b1d6-481f-b528-23538f4022d3').cautions_convictions