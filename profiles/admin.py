from django.contrib import admin
from .models import Profile, CandidateProfile, EmployerProfile

admin.site.register(Profile)
admin.site.register(CandidateProfile)
admin.site.register(EmployerProfile)