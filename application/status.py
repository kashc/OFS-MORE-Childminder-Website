"""
OFS-MORE-CCN3: Apply to be a Childminder Beta
-- Status --

@author: Informed Solutions
"""


from .models import Application


# Function to update task status
def update(application_id, field_name, status):
    
    # Retrieve current application
    local_application = Application.objects.get(pk = application_id)
    
    # Update task status
    setattr(local_application, field_name, status)
    
    # Save to database
    local_application.save()