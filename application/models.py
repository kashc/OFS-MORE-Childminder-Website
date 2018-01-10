"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Models --

@author: Informed Solutions
"""


from django.db import models
from uuid import uuid4


# USER_DETAILS entity
class UserDetails(models.Model):
    
    login_id = models.UUIDField(primary_key=True, default=uuid4)
    email = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    add_phone_number = models.CharField(max_length=20, blank=True)
    email_expiry_date = models.IntegerField(blank=True, null=True)
    sms_expiry_date = models.IntegerField(blank=True, null=True)
    magic_link_email = models.CharField(max_length=100, blank=True, null=True)
    magic_link_sms = models.CharField(max_length=100, blank=True, null=True)
    
    # Set table name
    class Meta:
        
        db_table = 'USER_DETAILS'


# APPLICATION entity
class Application(models.Model):
    
    APP_STATUS = (
        ('ARC_REVIEW', 'ARC_REVIEW'),
        ('CANCELLED', 'CANCELLED'),
        ('CYGNUM_REVIEW', 'CYGNUM_REVIEW'),
        ('DRAFTING', 'DRAFTING'),
        ('FURTHER_INFORMATION', 'FURTHER_INFORMATION'),
        ('NOT_REGISTERED', 'NOT_REGISTERED'),
        ('REGISTERED', 'REGISTERED'),
        ('REJECTED', 'REJECTED'),
        ('SUBMITTED', 'SUBMITTED'),
        ('WITHDRAWN', 'WITHDRAWN')
    )
    
    APP_TYPE = (
        ('CHILDMINDER', 'CHILDMINDER'),
        ('NANNY', 'NANNY'),
        ('NURSERY', 'NURSERY'),
        ('SOCIAL_CARE', 'SOCIAL_CARE')
    )
    
    TASK_STATUS = (
        ('NOT_STARTED', 'NOT_STARTED'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('COMPLETE', 'COMPLETE'),
        ('FURTHER_INFORMATION', 'FURTHER_INFORMATION')
    )
    
    application_id = models.UUIDField(primary_key = True, default = uuid4)
    login_id = models.ForeignKey(UserDetails, on_delete = models.CASCADE, db_column ='login_id', blank = True, null = True)
    application_type = models.CharField(choices = APP_TYPE, max_length = 50, blank = True)
    application_status = models.CharField(choices = APP_STATUS, max_length = 50, blank = True)
    cygnum_urn = models.CharField(max_length = 50, blank = True)
    login_details_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    personal_details_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    childcare_type_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    first_aid_training_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    eyfs_training_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    criminal_record_check_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    health_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    references_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    people_in_home_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    declarations_status = models.CharField(choices = TASK_STATUS, max_length = 50)
    date_created = models.DateTimeField(blank = True, null = True)
    date_updated = models.DateTimeField(blank = True, null = True)
    date_accepted = models.DateTimeField(blank = True, null = True)
    
    # Set table name
    class Meta:
        
        db_table = 'APPLICATION'
        

# CHILDCARE_TYPE entity
class Childcare_Type(models.Model):
    
    childcare_id = models.UUIDField(primary_key = True, default = uuid4)
    application_id = models.ForeignKey(Application, on_delete = models.CASCADE, db_column = 'application_id')
    zero_to_five = models.BooleanField(blank = True)
    five_to_eight = models.BooleanField(blank = True)
    eight_plus = models.BooleanField(blank = True)
    
    # Set table name
    class Meta:
        
        db_table = 'CHILDCARE_TYPE'




# APPLICANT_PERSONAL_DETAILS entity
class Applicant_Personal_Details(models.Model):
    
    personal_detail_id = models.UUIDField(primary_key = True, default = uuid4)
    application_id = models.ForeignKey(Application, on_delete = models.CASCADE, db_column = 'application_id')
    birth_day = models.IntegerField(blank = True, null = True)
    birth_month = models.IntegerField(blank = True, null = True)
    birth_year = models.IntegerField(blank = True, null = True)
    
    # Set table name
    class Meta:
        
        db_table = 'APPLICANT_PERSONAL_DETAILS'


# APPLICANT_NAME entity
class Applicant_Names(models.Model):
    
    name_id = models.UUIDField(primary_key = True, default = uuid4)
    personal_detail_id = models.ForeignKey(Applicant_Personal_Details, on_delete = models.CASCADE, db_column = 'personal_detail_id')
    current_name = models.BooleanField(blank = True)
    first_name = models.CharField(max_length = 100, blank = True)
    middle_names = models.CharField(max_length = 100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    
    # Set table name
    class Meta:
        
        db_table = 'APPLICANT_NAME'


# APPLICANT_HOME_ADDRESS entity
class Applicant_Home_Address(models.Model):
    
    home_address_id = models.UUIDField(primary_key = True, default = uuid4)
    personal_detail_id = models.ForeignKey(Applicant_Personal_Details, on_delete = models.CASCADE, db_column = 'personal_detail_id')
    street_line1 = models.CharField(max_length = 100, blank = True)
    street_line2 = models.CharField(max_length = 100, blank = True)
    town = models.CharField(max_length = 100, blank = True)
    county = models.CharField(max_length = 100, blank = True)
    country = models.CharField(max_length = 100, blank = True)
    postcode = models.CharField(max_length = 8, blank = True)
    childcare_address = models.NullBooleanField(blank = True, null=True)
    current_address = models.NullBooleanField(blank = True, null=True)
    move_in_month = models.IntegerField(blank = True)
    move_in_year = models.IntegerField(blank = True)
    
    # Set table name
    class Meta:
        
        db_table = 'APPLICANT_HOME_ADDRESS'


# FIRST_AID_TRAINING entity
class First_Aid_Training(models.Model):
    
    first_aid_id = models.UUIDField(primary_key = True, default = uuid4)
    application_id = models.ForeignKey(Application, on_delete = models.CASCADE, db_column = 'application_id')
    training_organisation = models.CharField(max_length = 100)
    course_title = models.CharField(max_length = 100)
    course_day = models.IntegerField()
    course_month = models.IntegerField()
    course_year = models.IntegerField()
    
    # Set table name
    class Meta:
        db_table = 'FIRST_AID_TRAINING'

# CRIMINAL_RECORD_CHECK entity
class Criminal_Record_Check(models.Model):
    criminal_record_id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.ForeignKey(Application, on_delete=models.CASCADE, db_column='application_id')
    dbs_certificate_number = models.CharField(max_length=50, blank=True)
    cautions_convictions = models.BooleanField(blank=True)
    
    # Set table name
    class Meta:
        db_table = 'CRIMINAL_RECORD_CHECK'


# HEALTH_DECLARATION_BOOKLET entity
class Health_Declaration_Booklet(models.Model):
    
    hdb_id = models.UUIDField(primary_key = True, default = uuid4)
    application_id = models.ForeignKey(Application, on_delete = models.CASCADE, db_column = 'application_id')
    movement_problems = models.BooleanField(blank = True)
    breathing_problems = models.BooleanField(blank = True)
    heart_disease = models.BooleanField(blank = True)
    blackout_epilepsy = models.BooleanField(blank = True)
    mental_health_problems = models.BooleanField(blank = True)
    alcohol_drug_problems = models.BooleanField(blank = True)
    health_details = models.CharField(max_length = 500, blank = True)
    
    # Set table name
    class Meta:
        
        db_table = 'HEALTH_DECLARATION_BOOKLET'


# REFERENCE entity
class References(models.Model):
    
    reference_id = models.UUIDField(primary_key = True, default = uuid4)
    application_id = models.ForeignKey(Application, on_delete = models.CASCADE, db_column = 'application_id')
    first_name = models.CharField(max_length = 100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    relationship = models.CharField(max_length = 100, blank = True)
    years_known = models.IntegerField(blank = True)
    months_known = models.IntegerField(blank = True)
    street_line1 = models.CharField(max_length = 100, blank = True)
    street_line2 = models.CharField(max_length = 100, blank = True)
    town = models.CharField(max_length = 100, blank = True)
    county = models.CharField(max_length = 100, blank = True)
    country = models.CharField(max_length = 100, blank = True)
    postcode = models.CharField(max_length = 8, blank = True)
    phone_number = models.CharField(max_length = 50, blank = True)
    email = models.CharField(max_length = 100, blank = True)
    
    # Set table name
    class Meta:
        
        db_table = 'REFERENCE'


# ADULT_IN_HOME entity
class Adults_In_Home(models.Model):
    
    adult_id = models.UUIDField(primary_key = True, default = uuid4)
    application_id = models.ForeignKey(Application, on_delete = models.CASCADE, db_column = 'application_id')
    first_name = models.CharField(max_length = 100, blank = True)
    middle_names = models.CharField(max_length = 100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    birth_day = models.IntegerField(blank = True)
    birth_month = models.IntegerField(blank = True)
    birth_year = models.IntegerField(blank = True)
    relationship = models.CharField(max_length = 100, blank = True)
    dbs_certificate_number = models.CharField(max_length = 50, blank = True)
    email = models.CharField(max_length = 100, blank = True)
    
    # Set table name
    class Meta:
        db_table = 'ADULT_IN_HOME'
        

# CHILD_IN_HOME entity
class Children_In_Home(models.Model):
    
    child_id = models.UUIDField(primary_key = True, default = uuid4)
    application_id = models.ForeignKey(Application, on_delete = models.CASCADE, db_column = 'application_id')
    first_name = models.CharField(max_length = 100, blank = True)
    middle_names = models.CharField(max_length = 100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    birth_day = models.IntegerField(blank = True)
    birth_month = models.IntegerField(blank = True)
    birth_year = models.IntegerField(blank = True)
    relationship = models.CharField(max_length = 100, blank = True)
    
    # Set table name
    class Meta:
        
        db_table = 'CHILD_IN_HOME'

