from django.contrib import admin
from .models import (
    Appointment,
    Doctor,
    Department, 
    ContactMessage, 
    User,
    )

# These are the admin site registrations 
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(ContactMessage)
admin.site.register(User)
