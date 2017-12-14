'''
Created on 7 Dec 2017
@author: Informed Solutions
'''
from django import forms

from .models import Application, Criminal_Record_Check, Login_And_Contact_Details, Health_Declaration_Booklet, References, Applicant_Names, Applicant_Personal_Details, First_Aid_Training, Childcare_Type

from govuk_forms.fields import SplitDateField
from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import InlineCheckboxSelectMultiple, InlineRadioSelect, \
    SeparatedCheckboxSelectMultiple, SeparatedRadioSelect


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
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(TypeOfChildcare, self).__init__(*args, **kwargs)
        
        if Childcare_Type.objects.filter(application_id=self.application_id_local).count() > 0:
            
            zero_to_five_status = Childcare_Type.objects.get(application_id=self.application_id_local).zero_to_five
            five_to_eight_status = Childcare_Type.objects.get(application_id=self.application_id_local).five_to_eight
            eight_plus_status = Childcare_Type.objects.get(application_id=self.application_id_local).eight_plus
            
            print(zero_to_five_status)
            print(five_to_eight_status)
            print(eight_plus_status)
            
            if (zero_to_five_status == True) & (five_to_eight_status == True) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['0-5', '5-8', '8over']
            
            elif (zero_to_five_status == True) & (five_to_eight_status == True) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = ['0-5', '5-8']
            
            elif (zero_to_five_status == True) & (five_to_eight_status == False) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['0-5', '8over']

            elif (zero_to_five_status == False) & (five_to_eight_status == True) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['5-8', '8over']

            elif (zero_to_five_status == True) & (five_to_eight_status == False) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = ['0-5']

            elif (zero_to_five_status == False) & (five_to_eight_status == True) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = ['5-8']
                
            elif (zero_to_five_status == False) & (five_to_eight_status == False) & (eight_plus_status == True):
                self.fields['type_of_childcare'].initial = ['8over']

            elif (zero_to_five_status == False) & (five_to_eight_status == False) & (eight_plus_status == False):
                self.fields['type_of_childcare'].initial = []
    
class ContactEmail(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    email_address = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(ContactEmail, self).__init__(*args, **kwargs)
        if Login_And_Contact_Details.objects.filter(application_id=self.application_id_local).count() > 0:
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
        
        if Applicant_Personal_Details.objects.filter(application_id=self.application_id_local).count() > 0:
            
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
    course_date = SplitDateField(label='Course date', help_text='For example, 31 03 1980')
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(FirstAidTraining, self).__init__(*args, **kwargs)
        
        if First_Aid_Training.objects.filter(application_id=self.application_id_local).count() > 0:
            self.fields['first_aid_training_organisation'].initial = First_Aid_Training.objects.get(application_id=self.application_id_local).training_organisation
            self.fields['title_of_training_course'].initial = First_Aid_Training.objects.get(application_id=self.application_id_local).course_title
            self.fields['course_date'].initial = [First_Aid_Training.objects.get(application_id=self.application_id_local).course_day,First_Aid_Training.objects.get(application_id='48629508-b1d6-481f-b528-23538f4022d3').course_month,First_Aid_Training.objects.get(application_id='48629508-b1d6-481f-b528-23538f4022d3').course_year]
    
class DBSCheck(GOVUKForm):
    options = (('True', 'Yes'), ('False', 'No'))
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    dbs_certificate_number = forms.IntegerField(label='DBS certificate number', help_text='12-digit number on your certificate')
    convictions = forms.ChoiceField(label='Do you have any cautions or convictions?', help_text='Include any information recorded on your certificate', choices=options, widget=InlineRadioSelect)
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(DBSCheck, self).__init__(*args, **kwargs)
        
        if Criminal_Record_Check.objects.filter(application_id=self.application_id_local).count() > 0:
        
            self.fields['dbs_certificate_number'].initial = Criminal_Record_Check.objects.get(application_id=self.application_id_local).dbs_certificate_number
            self.fields['convictions'].initial = Criminal_Record_Check.objects.get(application_id=self.application_id_local).cautions_convictions

class EYFS(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

class OtherPeople(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True 

class ReferenceForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    relationship = forms.CharField(label='How do they know you?')
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(ReferenceForm, self).__init__(*args, **kwargs)
        
        if References.objects.filter(application_id=self.application_id_local).count() > 0:
        
            self.fields['first_name'].initial = References.objects.get(application_id=self.application_id_local).first_name
            self.fields['last_name'].initial = References.objects.get(application_id=self.application_id_local).last_name
            self.fields['relationship'].initial = References.objects.get(application_id=self.application_id_local).relationship  

class HealthDeclarationBooklet(GOVUKForm):
    options = (('True', 'Yes'), ('False', 'No'))
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
    walking_bending = forms.ChoiceField(label='Walking, bending, kneeling or lifting a child', choices=options, widget=InlineRadioSelect)
    asthma_breathing = forms.ChoiceField(label='Asthma or breathing difficulties', choices=options, widget=InlineRadioSelect)
    heart_disease = forms.ChoiceField(label='Heart disease', choices=options, widget=InlineRadioSelect)
    blackout_epilepsy = forms.ChoiceField(label='Blackouts, fits, epilepsy or fainting', choices=options, widget=InlineRadioSelect)
    mental_health = forms.ChoiceField(label='Depression, anxiety, panic attacks or mood swings', choices=options, widget=InlineRadioSelect)
    alcohol_drugs = forms.ChoiceField(label='Alcohol or drugs', choices=options, widget=InlineRadioSelect)
    
    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(HealthDeclarationBooklet, self).__init__(*args, **kwargs)
        
        if Health_Declaration_Booklet.objects.filter(application_id=self.application_id_local).count() > 0:
        
            self.fields['walking_bending'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).movement_problems
            self.fields['asthma_breathing'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).breathing_problems
            self.fields['heart_disease'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).heart_disease
            self.fields['blackout_epilepsy'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).blackout_epilepsy
            self.fields['mental_health'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).mental_health_problems
            self.fields['alcohol_drugs'].initial = Health_Declaration_Booklet.objects.get(application_id=self.application_id_local).alcohol_drug_problems 

class Declaration(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

class Confirm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
