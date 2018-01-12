"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Forms --

@author: Informed Solutions
"""

import re
from datetime import date
from django.conf import settings
from django import forms
from govuk_forms.fields import SplitDateField
from govuk_forms.forms import GOVUKForm
from govuk_forms.widgets import InlineCheckboxSelectMultiple, InlineRadioSelect, RadioSelect

from .customfields import ExpirySplitDateWidget, ExpirySplitDateField, TimeKnownField
from .models import (Application,
                     ApplicantHomeAddress,
                     ApplicantName,
                     ApplicantPersonalDetails,
                     ChildcareType,
                     CriminalRecordCheck,
                     FirstAidTraining,
                     HealthDeclarationBooklet,
                     Reference,
                     UserDetails)


# Type of childcare form
class TypeOfChildcareForm(forms.Form):
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
        label='',
    )

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(TypeOfChildcareForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if ChildcareType.objects.filter(application_id=self.application_id_local).count() > 0:

            zero_to_five_status = ChildcareType.objects.get(application_id=self.application_id_local).zero_to_five
            five_to_eight_status = ChildcareType.objects.get(application_id=self.application_id_local).five_to_eight
            eight_plus_status = ChildcareType.objects.get(application_id=self.application_id_local).eight_plus

            if (zero_to_five_status is True) & (five_to_eight_status is True) & (eight_plus_status is True):
                self.fields['type_of_childcare'].initial = ['0-5', '5-8', '8over']

            elif (zero_to_five_status is True) & (five_to_eight_status is True) & (eight_plus_status is False):
                self.fields['type_of_childcare'].initial = ['0-5', '5-8']

            elif (zero_to_five_status is True) & (five_to_eight_status is False) & (eight_plus_status is True):
                self.fields['type_of_childcare'].initial = ['0-5', '8over']

            elif (zero_to_five_status is False) & (five_to_eight_status is True) & (eight_plus_status is True):
                self.fields['type_of_childcare'].initial = ['5-8', '8over']

            elif (zero_to_five_status is True) & (five_to_eight_status is False) & (eight_plus_status is False):
                self.fields['type_of_childcare'].initial = ['0-5']

            elif (zero_to_five_status is False) & (five_to_eight_status is True) & (eight_plus_status is False):
                self.fields['type_of_childcare'].initial = ['5-8']

            elif (zero_to_five_status is False) & (five_to_eight_status is False) & (eight_plus_status is True):
                self.fields['type_of_childcare'].initial = ['8over']

            elif (zero_to_five_status is False) & (five_to_eight_status is False) & (eight_plus_status is False):
                self.fields['type_of_childcare'].initial = []


# Form for account selection
class AccountForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Form for login
class EmailLoginForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    email_address = forms.EmailField()

    def clean_email_address(self):
        email_address = self.cleaned_data['email_address']

        if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email_address) is None:
            raise forms.ValidationError('Please enter a valid e-mail address.')

        return email_address


# Your login and contact details form: e-mail address   
class ContactEmailForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    email_address = forms.EmailField()

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(ContactEmailForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Application.objects.filter(application_id=self.application_id_local).count() > 0:

            this_user = Application.objects.get(pk=self.application_id_local)
            login_id = this_user.login_id.login_id

            if UserDetails.objects.get(login_id=login_id).login_id != '':
                self.fields['email_address'].initial = UserDetails.objects.get(login_id=login_id).email

    # Email address validation
    def clean_email_address(self):

        email_address = self.cleaned_data['email_address']

        if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email_address) is None:
            raise forms.ValidationError('TBC')

        if len(email_address) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return email_address

    # Your login and contact details form: phone numbers


class ContactPhoneForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    mobile_number = forms.CharField(label='Mobile phone number')
    add_phone_number = forms.CharField(label='Additional phone number (optional)', required=False)

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(ContactPhoneForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Application.objects.filter(application_id=self.application_id_local).count() > 0:
            this_user = Application.objects.get(pk=self.application_id_local)
            login_id = this_user.login_id.login_id

            self.fields['mobile_number'].initial = UserDetails.objects.get(login_id=login_id).mobile_number
            self.fields['add_phone_number'].initial = UserDetails.objects.get(login_id=login_id).add_phone_number

    # Mobile number validation
    def clean_mobile_number(self):

        mobile_number = self.cleaned_data['mobile_number']
        # Allow for spaces
        no_space_mobile_number = mobile_number.replace(' ', '')

        if re.match("^(07\d{8,12}|447\d{7,11})$", no_space_mobile_number) is None:
            raise forms.ValidationError('TBC')

        if len(no_space_mobile_number) > 11:
            raise forms.ValidationError('TBC')

        return mobile_number

    # Phone number validation
    def clean_add_phone_number(self):

        add_phone_number = self.cleaned_data['add_phone_number']
        # Allow for spaces
        no_space_add_phone_number = add_phone_number.replace(' ', '')

        if add_phone_number != '':

            if re.match("^(0\d{8,12}|447\d{7,11})$", no_space_add_phone_number) is None:
                raise forms.ValidationError('TBC')

            if len(no_space_add_phone_number) > 11:
                raise forms.ValidationError('TBC')

        return add_phone_number


class VerifyPhoneForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    magic_link_sms = forms.CharField(label='Security code', required=True)

    def __init__(self, *args, **kwargs):
        self.magic_link_email = kwargs.pop('id')
        super(VerifyPhoneForm, self).__init__(*args, **kwargs)

    def clean_magic_link_sms(self):
        magic_link_sms = self.cleaned_data['magic_link_sms']

        if (UserDetails.objects.filter(magic_link_sms=magic_link_sms, magic_link_email=self.magic_link_email).count()
                == 0):
            raise forms.ValidationError('TBC')

        return magic_link_sms


# Your login and contact details form: knowledge-based question 
class QuestionForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    question = forms.CharField(label='Knowledge based question', required=True)

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(QuestionForm, self).__init__(*args, **kwargs)


# Your login and contact details form: summary page  
class ContactSummaryForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Your personal details form: guidance page  
class PersonalDetailsGuidanceForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Your personal details form: names   
class PersonalDetailsNameForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    first_name = forms.CharField(label='First name')
    middle_names = forms.CharField(label='Middle names (if you have any)', required=False)
    last_name = forms.CharField(label='Last name')

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsNameForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form        
        if ApplicantPersonalDetails.objects.filter(application_id=self.application_id_local).count() > 0:
            personal_detail_id = ApplicantPersonalDetails.objects.get(
                application_id=self.application_id_local).personal_detail_id

            self.fields['first_name'].initial = ApplicantName.objects.get(
                personal_detail_id=personal_detail_id).first_name
            self.fields['middle_names'].initial = ApplicantName.objects.get(
                personal_detail_id=personal_detail_id).middle_names
            self.fields['last_name'].initial = ApplicantName.objects.get(
                personal_detail_id=personal_detail_id).last_name

    # First name validation
    def clean_first_name(self):

        first_name = self.cleaned_data['first_name']

        if re.match("^[A-Za-z- ]+$", first_name) is None:
            raise forms.ValidationError('TBC')

        if len(first_name) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return first_name

    # Middle names validation
    def clean_middle_names(self):

        middle_names = self.cleaned_data['middle_names']

        if middle_names != '':

            if re.match("^[A-Za-z- ]+$", middle_names) is None:
                raise forms.ValidationError('TBC')

            if len(middle_names) > 100:
                raise forms.ValidationError('Please enter 100 characters or less.')

        return middle_names

    # Last name validation
    def clean_last_name(self):

        last_name = self.cleaned_data['last_name']

        if re.match("^[A-Za-z- ]+$", last_name) is None:
            raise forms.ValidationError('TBC')

        if len(last_name) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return last_name


# Your personal details form: date of birth 
class PersonalDetailsDOBForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    date_of_birth = SplitDateField(label='Date of birth', help_text='For example, 31 03 1980')

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsDOBForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form        
        if ApplicantPersonalDetails.objects.filter(application_id=self.application_id_local).count() > 0:
            self.fields['date_of_birth'].initial = [
                ApplicantPersonalDetails.objects.get(application_id=self.application_id_local).birth_day,
                ApplicantPersonalDetails.objects.get(application_id=self.application_id_local).birth_month,
                ApplicantPersonalDetails.objects.get(application_id=self.application_id_local).birth_year]

    # First name validation
    def clean_date_of_birth(self):

        birth_day = self.cleaned_data['date_of_birth'].day
        birth_month = self.cleaned_data['date_of_birth'].month
        birth_year = self.cleaned_data['date_of_birth'].year

        applicant_dob = date(birth_year, birth_month, birth_day)
        today = date.today()
        age = today.year - applicant_dob.year - ((today.month, today.day) < (applicant_dob.month, applicant_dob.day))

        if age < 18:
            raise forms.ValidationError('You have to be 18 to childmind.')

        return birth_day, birth_month, birth_year


# Your personal details form: home address   
class PersonalDetailsHomeAddressForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode')

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsHomeAddressForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        personal_detail_id = ApplicantPersonalDetails.objects.get(
            application_id=self.application_id_local).personal_detail_id

        if ApplicantHomeAddress.objects.filter(personal_detail_id=personal_detail_id, current_address=True).count() > 0:
            self.fields['postcode'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                               current_address=True).postcode


# Your personal details form: home address   
class PersonalDetailsHomeAddressManualForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    street_name_and_number = forms.CharField(label='Street name and number')
    street_name_and_number2 = forms.CharField(label='Street name and number 2', required=False)
    town = forms.CharField(label='Town or city')
    county = forms.CharField(label='County (optional)', required=False)
    postcode = forms.CharField(label='Postcode')

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsHomeAddressManualForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        personal_detail_id = ApplicantPersonalDetails.objects.get(
            application_id=self.application_id_local).personal_detail_id

        if ApplicantHomeAddress.objects.filter(personal_detail_id=personal_detail_id, current_address=True).count() > 0:
            self.fields['street_name_and_number'].initial = ApplicantHomeAddress.objects.get(
                personal_detail_id=personal_detail_id, current_address=True).street_line1
            self.fields['street_name_and_number2'].initial = ApplicantHomeAddress.objects.get(
                personal_detail_id=personal_detail_id, current_address=True).street_line2
            self.fields['town'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                           current_address=True).town
            self.fields['county'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                             current_address=True).county
            self.fields['postcode'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                               current_address=True).postcode

    # Street name and number validation
    def clean_street_name_and_number(self):

        street_name_and_number = self.cleaned_data['street_name_and_number']

        if len(street_name_and_number) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number

    def clean_street_name_and_number2(self):

        street_name_and_number2 = self.cleaned_data['street_name_and_number2']

        if len(street_name_and_number2) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number2

        # Town validation

    def clean_town(self):

        town = self.cleaned_data['town']

        if re.match("^[A-Za-z- ]+$", town) is None:
            raise forms.ValidationError('TBC.')

        if len(town) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return town

        # County validation

    def clean_county(self):

        county = self.cleaned_data['county']

        if county != '':

            if re.match("^[A-Za-z- ]+$", county) is None:
                raise forms.ValidationError('TBC.')

            if len(county) > 100:
                raise forms.ValidationError('Please enter 100 characters or less.')

        return county

    # Postcode validation
    def clean_postcode(self):

        postcode = self.cleaned_data['postcode']

        if re.match("^[A-Za-z0-9 ]{1,8}$", postcode) is None:
            raise forms.ValidationError('TBC.')

        return postcode


# Your personal details form: location of care  
class PersonalDetailsLocationOfCareForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    options = (('True', 'Yes'), ('False', 'No'))

    location_of_care = forms.ChoiceField(label='Is this where you will be looking after the children?', choices=options,
                                         widget=InlineRadioSelect, required=True)

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsLocationOfCareForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        personal_detail_id = ApplicantPersonalDetails.objects.get(
            application_id=self.application_id_local).personal_detail_id

        if ApplicantHomeAddress.objects.filter(personal_detail_id=personal_detail_id, current_address=True).count() > 0:
            self.fields['location_of_care'].initial = ApplicantHomeAddress.objects.get(
                personal_detail_id=personal_detail_id, current_address=True).childcare_address


# Your personal details form: home address   
class PersonalDetailsChildcareAddressForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode')

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsChildcareAddressForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        personal_detail_id = ApplicantPersonalDetails.objects.get(
            application_id=self.application_id_local).personal_detail_id

        if ApplicantHomeAddress.objects.filter(personal_detail_id=personal_detail_id,
                                               childcare_address='True').count() > 0:
            self.fields['postcode'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                               childcare_address='True').postcode


# Your personal details form: childcare address   
class PersonalDetailsChildcareAddressManualForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    street_name_and_number = forms.CharField(label='Street name and number')
    street_name_and_number2 = forms.CharField(label='Street name and number 2', required=False)
    town = forms.CharField(label='Town or city')
    county = forms.CharField(label='County (optional)', required=False)
    postcode = forms.CharField(label='Postcode')

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(PersonalDetailsChildcareAddressManualForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        personal_detail_id = ApplicantPersonalDetails.objects.get(
            application_id=self.application_id_local).personal_detail_id

        if ApplicantHomeAddress.objects.filter(personal_detail_id=personal_detail_id,
                                               childcare_address='True').count() > 0:
            personal_detail_id = ApplicantPersonalDetails.objects.get(
                application_id=self.application_id_local).personal_detail_id

            self.fields['street_name_and_number'].initial = ApplicantHomeAddress.objects.get(
                personal_detail_id=personal_detail_id, childcare_address='True').street_line1
            self.fields['street_name_and_number2'].initial = ApplicantHomeAddress.objects.get(
                personal_detail_id=personal_detail_id, childcare_address='True').street_line2
            self.fields['town'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                           childcare_address='True').town
            self.fields['county'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                             childcare_address='True').county
            self.fields['postcode'].initial = ApplicantHomeAddress.objects.get(personal_detail_id=personal_detail_id,
                                                                               childcare_address='True').postcode

    # Street name and number validation
    def clean_street_name_and_number(self):

        street_name_and_number = self.cleaned_data['street_name_and_number']

        if len(street_name_and_number) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number

    def clean_street_name_and_number2(self):

        street_name_and_number2 = self.cleaned_data['street_name_and_number2']

        if len(street_name_and_number2) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number2

        # Town validation

    def clean_town(self):

        town = self.cleaned_data['town']

        if re.match("^[A-Za-z-]+$", town) is None:
            raise forms.ValidationError('TBC')

        if len(town) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return town

        # County validation

    def clean_county(self):

        county = self.cleaned_data['county']

        if county != '':

            if re.match("^[A-Za-z-]+$", county) is None:
                raise forms.ValidationError('TBC')

            if len(county) > 100:
                raise forms.ValidationError('Please enter 100 characters or less.')

        return county

    # Postcode validation
    def clean_postcode(self):

        postcode = self.cleaned_data['postcode']

        if re.match("^[A-Za-z0-9 ]{1,8}$", postcode) is None:
            raise forms.ValidationError('TBC')

        return postcode


# Your personal details form: summary page  
class PersonalDetailsSummaryForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# First aid training form: guidance
class FirstAidTrainingGuidanceForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# First aid training form: details
class FirstAidTrainingDetailsForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    first_aid_training_organisation = forms.CharField(label='First aid training organisation')
    title_of_training_course = forms.CharField(label='Title of training course')
    course_date = SplitDateField(label='Course date', help_text='For example, 31 03 2016')

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(FirstAidTrainingDetailsForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form        
        if FirstAidTraining.objects.filter(application_id=self.application_id_local).count() > 0:
            self.fields['first_aid_training_organisation'].initial = FirstAidTraining.objects.get(
                application_id=self.application_id_local).training_organisation
            self.fields['title_of_training_course'].initial = FirstAidTraining.objects.get(
                application_id=self.application_id_local).course_title
            self.fields['course_date'].initial = [
                FirstAidTraining.objects.get(application_id=self.application_id_local).course_day,
                FirstAidTraining.objects.get(application_id=self.application_id_local).course_month,
                FirstAidTraining.objects.get(application_id=self.application_id_local).course_year]


# First aid training form: declaration
class FirstAidTrainingDeclarationForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    declaration = forms.BooleanField(label='I will show my first aid certificate to the inspector', required=True)


# First aid training form: renew
class FirstAidTrainingRenewForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    renew_a = forms.BooleanField(label='I will renew my first aid training in the next few months', required=True)
    renew_b = forms.BooleanField(label='I will show my first aid certificate to the inspector', required=True)


# First aid training form: training
class FirstAidTrainingTrainingForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# First aid training form: summary
class FirstAidTrainingSummaryForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Early Years knowledge form
class EYFSForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Your criminal record (DBS) check: guidance form
class DBSCheckGuidanceForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Your criminal record (DBS) check form   
class DBSCheckDBSDetailsForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    options = (('True', 'Yes'), ('False', 'No'))

    dbs_certificate_number = forms.IntegerField(label='DBS certificate number',
                                                help_text='12-digit number on your certificate',
                                                required=True)
    convictions = forms.ChoiceField(label='Do you have any cautions or convictions?',
                                    help_text='Include any information recorded on your certificate',
                                    choices=options, widget=InlineRadioSelect,
                                    required=True)

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(DBSCheckDBSDetailsForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form 
        if CriminalRecordCheck.objects.filter(application_id=self.application_id_local).count() > 0:
            self.fields['dbs_certificate_number'].initial = CriminalRecordCheck.objects.get(
                application_id=self.application_id_local).dbs_certificate_number
            self.fields['convictions'].initial = CriminalRecordCheck.objects.get(
                application_id=self.application_id_local).cautions_convictions

    # DBS certificate number validation
    def clean_dbs_certificate_number(self):

        dbs_certificate_number = self.cleaned_data['dbs_certificate_number']

        if len(str(dbs_certificate_number)) > 12:
            raise forms.ValidationError('TBC')

        if len(str(dbs_certificate_number)) < 12:
            raise forms.ValidationError('TBC')

        return dbs_certificate_number


# Your criminal record (DBS) check: upload DBS form
class DBSCheckUploadDBSForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    declaration = forms.BooleanField(label='I will send my original DBS certificate to Ofsted', required=True)

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(DBSCheckUploadDBSForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if CriminalRecordCheck.objects.filter(application_id=self.application_id_local).count() > 0:

            if CriminalRecordCheck.objects.get(
                    application_id=self.application_id_local).send_certificate_declare is True:

                self.fields['declaration'].initial = '1'

            elif CriminalRecordCheck.objects.get(
                    application_id=self.application_id_local).send_certificate_declare is False:

                self.fields['declaration'].initial = '0'


# Your criminal record (DBS) check: summary form
class DBSCheckSummaryForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Your health: intro form
class HealthIntroForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Your health: booklet form
class HealthBookletForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    send_hdb_declare = forms.BooleanField(label='I will send the completed booklet to Ofsted', required=True)

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(HealthBookletForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if HealthDeclarationBooklet.objects.filter(application_id=self.application_id_local).count() > 0:

            if HealthDeclarationBooklet.objects.get(
                    application_id=self.application_id_local).send_hdb_declare is True:

                self.fields['send_hdb_declare'].initial = '1'

            elif HealthDeclarationBooklet.objects.get(
                    application_id=self.application_id_local).send_hdb_declare is False:

                self.fields['send_hdb_declare'].initial = '0'


# 2 references: intro form
class ReferenceIntroForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# 2 references form
class FirstReferenceForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    relationship = forms.CharField(label='How do they know you?', help_text='For instance, friend or neighbour',
                                   required=True)
    time_known = TimeKnownField(label='How long have they known you?', required=True)

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(FirstReferenceForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form        
        if Reference.objects.filter(application_id=self.application_id_local, reference=1).count() > 0:
            self.fields['first_name'].initial = Reference.objects.get(
                application_id=self.application_id_local, reference=1).first_name
            self.fields['last_name'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                     reference=1).last_name
            self.fields['relationship'].initial = Reference.objects.get(
                application_id=self.application_id_local, reference=1).relationship
            self.fields['time_known'].initial = [Reference.objects.get(
                application_id=self.application_id_local, reference=1).years_known, Reference.objects.get(
                application_id=self.application_id_local, reference=1).months_known]

    # Time known validation
    def clean_time_known(self):

        years_known = self.cleaned_data['time_known'][1]
        months_known = self.cleaned_data['time_known'][0]
        print('Years:' + str(years_known))
        print('Months:' + str(months_known))

        if months_known != 0:

            reference_known_time = years_known + (months_known / 12)

        elif months_known == 0:

            reference_known_time = years_known

        if reference_known_time < 1:
            print(reference_known_time)
            raise forms.ValidationError('TBC.')

        return years_known, months_known


# 2 reference form: first reference address
class ReferenceFirstReferenceAddressForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode')

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(ReferenceFirstReferenceAddressForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Reference.objects.filter(application_id=self.application_id_local, reference=1).count() > 0:
            self.fields['postcode'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                    reference=1).postcode


# 2 references form: first reference address (manual)
class ReferenceFirstReferenceAddressManualForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    street_name_and_number = forms.CharField(label='Street name and number')
    street_name_and_number2 = forms.CharField(label='Street name and number 2', required=False)
    town = forms.CharField(label='Town or city')
    county = forms.CharField(label='County (optional)', required=False)
    postcode = forms.CharField(label='Postcode')
    country = forms.CharField(label='Country', required=True)

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(ReferenceFirstReferenceAddressManualForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Reference.objects.filter(application_id=self.application_id_local, reference=1).count() > 0:
            self.fields['street_name_and_number'].initial = Reference.objects.get(
                application_id=self.application_id_local,
                reference=1).street_line1
            self.fields['street_name_and_number2'].initial = Reference.objects.get(
                application_id=self.application_id_local,
                reference=1).street_line2
            self.fields['town'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                reference=1).town
            self.fields['county'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                  reference=1).county
            self.fields['postcode'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                    reference=1).postcode
            self.fields['country'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                   reference=1).country

    # Street name and number validation
    def clean_street_name_and_number(self):

        street_name_and_number = self.cleaned_data['street_name_and_number']

        if len(street_name_and_number) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number

    def clean_street_name_and_number2(self):

        street_name_and_number2 = self.cleaned_data['street_name_and_number2']

        if len(street_name_and_number2) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number2

        # Town validation

    def clean_town(self):

        town = self.cleaned_data['town']

        if re.match("^[A-Za-z-]+$", town) is None:
            raise forms.ValidationError('TBC')

        if len(town) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return town

        # County validation

    def clean_county(self):

        county = self.cleaned_data['county']

        if county != '':

            if re.match("^[A-Za-z-]+$", county) is None:
                raise forms.ValidationError('TBC')

            if len(county) > 100:
                raise forms.ValidationError('Please enter 100 characters or less.')

        return county

    # Postcode validation
    def clean_postcode(self):

        postcode = self.cleaned_data['postcode']

        if re.match("^[A-Za-z0-9 ]{1,8}$", postcode) is None:
            raise forms.ValidationError('TBC')

        return postcode


# 2 reference form: first reference contact details
class ReferenceFirstReferenceContactForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    phone_number = forms.CharField(label='Phone number')
    email_address = forms.CharField(label='Email address')

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(ReferenceFirstReferenceContactForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Reference.objects.filter(application_id=self.application_id_local, reference=1).count() > 0:
            self.fields['phone_number'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                        reference=1).phone_number
            self.fields['email_address'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                         reference=1).email

    # Phone number validation
    def clean_phone_number(self):

        phone_number = self.cleaned_data['phone_number']
        # Allow for spaces
        no_space_phone_number = phone_number.replace(' ', '')

        if phone_number != '':

            if re.match("^(0\d{8,12}|447\d{7,11})$", no_space_phone_number) is None:
                raise forms.ValidationError('TBC')

            if len(no_space_phone_number) > 11:
                raise forms.ValidationError('TBC')

        return phone_number

    # Email address validation
    def clean_email_address(self):

        email_address = self.cleaned_data['email_address']

        if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email_address) is None:
            raise forms.ValidationError('TBC')

        if len(email_address) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return email_address


# 2 references form
class SecondReferenceForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    relationship = forms.CharField(label='How do they know you?', help_text='For instance, friend or neighbour',
                                   required=True)
    time_known = TimeKnownField(label='How long have they known you?', required=True)

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(SecondReferenceForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Reference.objects.filter(application_id=self.application_id_local, reference=2).count() > 0:
            self.fields['first_name'].initial = Reference.objects.get(
                application_id=self.application_id_local, reference=2).first_name
            self.fields['last_name'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                     reference=2).last_name
            self.fields['relationship'].initial = Reference.objects.get(
                application_id=self.application_id_local, reference=2).relationship
            self.fields['time_known'].initial = [Reference.objects.get(
                application_id=self.application_id_local, reference=2).years_known, Reference.objects.get(
                application_id=self.application_id_local, reference=2).months_known]

    # Time known validation
    def clean_time_known(self):

        years_known = self.cleaned_data['time_known'][1]
        months_known = self.cleaned_data['time_known'][0]
        print('Years:' + str(years_known))
        print('Months:' + str(months_known))

        if months_known != 0:

            reference_known_time = years_known + (months_known / 12)

        elif months_known == 0:

            reference_known_time = years_known

        if reference_known_time < 1:
            print(reference_known_time)
            raise forms.ValidationError('TBC.')

        return years_known, months_known


# 2 reference form: second reference address
class ReferenceSecondReferenceAddressForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    postcode = forms.CharField(label='Postcode')

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(ReferenceSecondReferenceAddressForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Reference.objects.filter(application_id=self.application_id_local, reference=2).count() > 0:
            self.fields['postcode'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                    reference=2).postcode


# 2 references form: second reference address (manual)
class ReferenceSecondReferenceAddressManualForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    street_name_and_number = forms.CharField(label='Street name and number')
    street_name_and_number2 = forms.CharField(label='Street name and number 2', required=False)
    town = forms.CharField(label='Town or city')
    county = forms.CharField(label='County (optional)', required=False)
    postcode = forms.CharField(label='Postcode')
    country = forms.CharField(label='Country', required=True)

    def __init__(self, *args, **kwargs):

        self.application_id_local = kwargs.pop('id')
        super(ReferenceSecondReferenceAddressManualForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Reference.objects.filter(application_id=self.application_id_local, reference=2).count() > 0:
            self.fields['street_name_and_number'].initial = Reference.objects.get(
                application_id=self.application_id_local,
                reference=2).street_line1
            self.fields['street_name_and_number2'].initial = Reference.objects.get(
                application_id=self.application_id_local,
                reference=2).street_line2
            self.fields['town'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                reference=2).town
            self.fields['county'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                  reference=2).county
            self.fields['postcode'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                    reference=2).postcode
            self.fields['country'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                   reference=2).country

    # Street name and number validation
    def clean_street_name_and_number(self):

        street_name_and_number = self.cleaned_data['street_name_and_number']

        if len(street_name_and_number) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number

    def clean_street_name_and_number2(self):

        street_name_and_number2 = self.cleaned_data['street_name_and_number2']

        if len(street_name_and_number2) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return street_name_and_number2

        # Town validation

    def clean_town(self):

        town = self.cleaned_data['town']

        if re.match("^[A-Za-z-]+$", town) is None:
            raise forms.ValidationError('TBC')

        if len(town) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return town

        # County validation

    def clean_county(self):

        county = self.cleaned_data['county']

        if county != '':

            if re.match("^[A-Za-z-]+$", county) is None:
                raise forms.ValidationError('TBC')

            if len(county) > 100:
                raise forms.ValidationError('Please enter 100 characters or less.')

        return county

    # Postcode validation
    def clean_postcode(self):

        postcode = self.cleaned_data['postcode']

        if re.match("^[A-Za-z0-9 ]{1,8}$", postcode) is None:
            raise forms.ValidationError('TBC')

        return postcode


# 2 reference form: second reference contact details
class ReferenceSecondReferenceContactForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    phone_number = forms.CharField(label='Phone number')
    email_address = forms.CharField(label='Email address')

    def __init__(self, *args, **kwargs):
        self.application_id_local = kwargs.pop('id')
        super(ReferenceSecondReferenceContactForm, self).__init__(*args, **kwargs)

        # If information was previously entered, display it on the form
        if Reference.objects.filter(application_id=self.application_id_local, reference=2).count() > 0:
            self.fields['phone_number'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                        reference=2).phone_number
            self.fields['email_address'].initial = Reference.objects.get(application_id=self.application_id_local,
                                                                         reference=2).email

    # Phone number validation
    def clean_phone_number(self):

        phone_number = self.cleaned_data['phone_number']
        # Allow for spaces
        no_space_phone_number = phone_number.replace(' ', '')

        if phone_number != '':

            if re.match("^(0\d{8,12}|447\d{7,11})$", no_space_phone_number) is None:
                raise forms.ValidationError('TBC')

            if len(no_space_phone_number) > 11:
                raise forms.ValidationError('TBC')

        return phone_number

    # Email address validation
    def clean_email_address(self):

        email_address = self.cleaned_data['email_address']

        if re.match("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email_address) is None:
            raise forms.ValidationError('TBC')

        if len(email_address) > 100:
            raise forms.ValidationError('Please enter 100 characters or less.')

        return email_address


# People in your home form     
class OtherPeopleForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Declaration form
class DeclarationForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Confirm your details form
class ConfirmForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True


# Payment form
class PaymentForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    options = (
        ('Credit', 'Credit or debit card'),
        ('PayPal', 'PayPal')
    )

    payment_method = forms.ChoiceField(label='How would you like to pay?', choices=options,
                                       widget=RadioSelect, required=True)


# Payment Details form
class PaymentDetailsForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True

    options = (
        ('a', 'Alpha'),
        ('b', 'Beta')
    )

    grouped_options = (
        ('First', options),
        ('Second', (('c', 'Gamma'), ('d', 'Delta'))),
    )

    card_type_options = (
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('american_express', 'American Express'),
        ('maestro', 'Maestro')
    )

    card_type = forms.ChoiceField(label='Card type', choices=card_type_options, required=True)
    card_number = forms.CharField(label='Card number', required=True)
    expiry_date = ExpirySplitDateField(label='Expiry date', widget=ExpirySplitDateWidget, required=True)
    cardholders_name = forms.CharField(label="Cardholder's name", required=True)
    card_security_code = forms.CharField(label='Card security code', required=True)

    # Card number validation
    def clean_card_number(self):

        # Retrieve data
        card_type = self.cleaned_data['card_type']
        card_number = self.cleaned_data['card_number']

        # Strip all spaces and dashes from the card number for RegEx purposes
        card_number = re.sub('[ -]+', '', card_number)

        # Cast card_number as an integer to see if the user has entered non-numeric characters            
        try:

            int(card_number)

        except:
            # At the moment this is a catch all error, in the case of there being multiple error
            # types this must be revisited
            raise forms.ValidationError('Please enter a valid card number')
        if settings.VISA_VALIDATION:
            # Card number RegEx checking by type
            if card_type == 'visa':
                # Actual regex
                if re.match("^4[0-9]{12}(?:[0-9]{3})?$", card_number) is None:
                    raise forms.ValidationError('The card number you have entered is not a valid Visa card number')

        if card_type == 'mastercard':

            if re.match("^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$",
                        card_number) is None:
                raise forms.ValidationError('The card number you have entered is not a valid MasterCard card number')

        elif card_type == 'american_express':

            if re.match("^3[47][0-9]{13}$", card_number) is None:
                raise forms.ValidationError(
                    'The card number you have entered is not a valid American Express card number')

        elif card_type == 'maestro':

            if re.match("^(?:5[0678]\d\d|6304|6390|67\d\d)\d{8,15}$", card_number) is None:
                raise forms.ValidationError('The card number you have entered is not a valid Maestro card number')

        return card_number

    # Cardholder's name validation
    def clean_cardholders_name(self):

        cardholders_name = self.cleaned_data['cardholders_name']

        if re.match("^[A-Za-z- ]+$", cardholders_name) is None:
            raise forms.ValidationError('Please enter a valid name.')

    # Card security code validation   
    def clean_card_security_code(self):

        # Get value to be validated
        card_security_code = self.cleaned_data['card_security_code']

        try:

            int(card_security_code)

        except:

            raise forms.ValidationError('The card security code you have entered is invalid')

        if re.match("^[0-9]{3,4}$", card_security_code) is None:
            raise forms.ValidationError('The card security code you have entered is invalid')


# Application saved form
class ApplicationSavedForm(GOVUKForm):
    field_label_classes = 'form-label-bold'
    auto_replace_widgets = True
