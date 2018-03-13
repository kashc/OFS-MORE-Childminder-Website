from django.shortcuts import render
from django.core.urlresolvers import reverse

from application.models import (
        AdultInHome,
        ApplicantHomeAddress,
        ApplicantName,
        ApplicantPersonalDetails,
        Application,
        AuditLog,
        ChildInHome,
        ChildcareType,
        CriminalRecordCheck,
        EYFS,
        FirstAidTraining,
        HealthDeclarationBooklet,
        Reference,
        UserDetails

)

def task_list(request):
    """
    Method returning the template for the task-list (with current task status) for an applicant's application;
    logic is built in to enable the Declarations and Confirm your details tasks when all other tasks are complete
    :param request: a request object used to generate the HttpResponse
    :return: an HttpResponse object with the rendered task list template
    """

    if request.method == 'GET':

        application_id = request.GET["id"]
        application = Application.objects.get(pk=application_id)
        childcare_record = ChildcareType.objects.get(application_id=application_id)
        zero_to_five_status = childcare_record.zero_to_five
        five_to_eight_status = childcare_record.five_to_eight
        eight_plus_status = childcare_record.eight_plus

        if (zero_to_five_status is True) & (five_to_eight_status is True) & (eight_plus_status is True):
            registers = 'Early Years and Childcare Register (both parts)'
            fee = '£35'
        elif (zero_to_five_status is True) & (five_to_eight_status is True) & (eight_plus_status is False):
            registers = 'Early Years and Childcare Register (compulsory part)'
            fee = '£35'
        elif (zero_to_five_status is True) & (five_to_eight_status is False) & (eight_plus_status is True):
            registers = 'Early Years and Childcare Register (voluntary part)'
            fee = '£35'
        elif (zero_to_five_status is False) & (five_to_eight_status is True) & (eight_plus_status is True):
            registers = 'Childcare Register (both parts)'
            fee = '£103'
        elif (zero_to_five_status is True) & (five_to_eight_status is False) & (eight_plus_status is False):
            registers = 'Early Years Register'
            fee = '£35'
        elif (zero_to_five_status is False) & (five_to_eight_status is True) & (eight_plus_status is False):
            registers = 'Childcare Register (compulsory part)'
            fee = '£103'
        elif (zero_to_five_status is False) & (five_to_eight_status is False) & (eight_plus_status is True):
            registers = 'Childcare Register (voluntary part)'
            fee = '£103'

        """
        Variables which are passed to the template
        """

        context = {
            'id': application_id,
            'all_complete': False,
            'confirm_details': False,
            'registers': registers,
            'fee': fee,
            'tasks': [
                 {
                    'name': 'account_details',                                      # This is CSS class (Not recommended to store it here)
                    'status': application.login_details_status,
                    'description': "Your login details",
                    'status_url': None,                                             # Will be filled later                        
                    'status_urls': [                                                # Available urls for each status
                         {'status': 'COMPLETED',  'url': 'Contact-Summary-View'},
                         {'status': 'OTHER',      'url': 'Contact-Email-View'},     # For all other statuses
                     ],
                },
                {
                    'name': 'children',
                    'status': application.childcare_type_status,
                    'description': "Type of childcare",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Type-Of-Childcare-Age-Groups-View'},
                        {'status': 'OTHER',     'url': 'Type-Of-Childcare-Guidance-View'}
                    ],
                },
                {
                    'name': 'personal_details',
                    'status': application.personal_details_status,
                    'description': "Your personal details",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Personal-Details-Summary-View'},
                        {'status': 'OTHER',     'url': 'Personal-Details-Guidance-View'}
                    ],
                },
                {
                    'name': 'first_aid',
                    'status': application.first_aid_training_status,
                    'description': "First aid training",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'First-Aid-Training-Summary-View'},
                        {'status': 'OTHER',     'url': 'First-Aid-Training-Guidance-View'}
                    ],
                },
                {
                    'name': 'health',
                    'status': application.health_status,
                    'description': "Health declaration booklet",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Health-Check-Answers-View'},
                        {'status': 'OTHER',     'url': 'Health-Intro-View'}
                    ],
                },
                {
                    'name': 'dbs',
                    'status': application.criminal_record_check_status,
                    'description': "Criminal record (DBS) check",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'DBS-Check-Summary-View'},
                        {'status': 'OTHER',     'url': 'DBS-Check-Guidance-View'}
                    ],
                },
                {
                    'name': 'other_people',
                    'status': application.people_in_home_status,
                    'description': "People in your home",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Other-People-Summary-View'},
                        {'status': 'OTHER',     'url': 'Other-People-Guidance-View'}
                    ],
                },
                {
                    'name': 'references',
                    'status': application.references_status,
                    'description': "References",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'References-Summary-View'},
                        {'status': 'OTHER',     'url': 'References-Intro-View'}
                    ],
                },
                {
                    'name': 'review',
                    'status': application.declarations_status,
                    'description': "Declaration and payment",
                    'status_url': None,
                    'status_urls': [
                        {'status': 'COMPLETED', 'url': 'Declaration-Summary-View'},
                        {'status': 'OTHER',     'url': 'Declaration-Summary-View'}
                    ],
                },
            ]
    }

    """
    Prepare task links
    """

    for task in context.get('tasks'):              # Iterating through tasks
        
        for url in task.get('status_urls'):        # Iterating through task available urls
            if url['status'] == task['status']:    # Match current task status with url which is in status_urls
                task['status_url'] = url['url']    # Set main task primary url to the one which matched
        
        if not task['status_url']:                 # In case no matches were found by task status 
            for url in task.get('status_urls'):    # Search for link with has status "OTHER"
                if url['status'] == "OTHER":         
                    task['status_url'] = url['url']

    """
    Declaratations state
    """

    # Set declarations state and confirm your details tasks depending on task completion
    if (task['status'] in ['NOT_STARTED', 'IN_PROGRESS'] for task in context['tasks']):
        context['all_complete'] = False
    else:
        context['all_complete'] = True

        # Status is changed by Arc when payment went well
        if(task['name'] == 'review' for task in context['tasks']):
            
            if task['status'] == 'COMPLETED':
                context['confirm_details'] = True
            else:
                context['confirm_details'] = False

    return render(request, 'task-list.html', context)

